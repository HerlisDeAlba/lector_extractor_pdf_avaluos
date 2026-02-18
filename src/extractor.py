# src/extractor.py
import json
import time
from . import gemini_service
from . import config

def extract_from_pdf(client, pdf_path, fields):
    """Extracts data from a single PDF using Gemini with retry logic."""
    max_retries = 5
    base_delay = 30
    
    for attempt in range(max_retries):
        try:
            pdf_file = gemini_service.upload_file(client, pdf_path)
            gemini_service.wait_for_file_active(client, pdf_file)

            prompt_text = f"""
            Role: Expert Data Extractor.
            Task: Extract technical information from the real estate appraisal (Avalúo) provided in the PDF.
            
            Constraint:
            - Return ONLY a valid JSON object.
            - Keys MUST be exactly these fields: {json.dumps(fields)}
            - If a field is not found in the document, use an empty string "".
            - Do not include markdown formatting (like ```json ... ```) in the response if possible, just the raw JSON.
            - Ensure all values are strings.

            Specific Field Instructions:
            1. COEFICIENTE: Extract the value EXACTLY as shown in the document, preserving all decimal places and the percentage symbol (e.g., "1.7890%"). Do NOT round or format as integer.
            2. DESC_EQUIPAMIENTO: detailed descriptive narrative consolidating all equipment info (Type, Level, Distance) into one natural language text. Example: "El nivel de ÁREAS VERDES es suficiente a 200m..."
            3. ACABADOS_PISOS: A consolidated narrative describing the floor finishes for ALL rooms/areas. Group by finish type. Example: "Pisos de alcobas y sala en madera laminada, cocina y baños en cerámica."
            4. ACABADOS_MUROS: A consolidated narrative describing the wall finishes for ALL rooms/areas. Group by finish type.
            5. COMPONENTE_EDIF: A consolidated narrative summary of the Valuation/Edification table (Componente, Unidad, Valor). Avoid list dumping. Describe it like: "La estructura principal de 120m2 tiene un valor unitario de X..."
            6. For other fields, be precise with numbers and dates.
            """

            response = gemini_service.generate_content(
                client, 
                config.MODEL_NAME, 
                [pdf_file, prompt_text]
            )
            
            # Clean up extraction result
            # Clean up extraction result
            text_response = response.text.strip()
            # Handle markdown code blocks
            if text_response.startswith("```"):
                # Find the first newline to skip the language identifier (e.g. ```json)
                first_newline = text_response.find('\n')
                if first_newline != -1:
                    text_response = text_response[first_newline+1:]
                
                # Check for closing fences
                last_fence = text_response.rfind("```")
                if last_fence != -1:
                    text_response = text_response[:last_fence]
            
            text_response = text_response.strip()

            try:
                data = json.loads(text_response)
            except json.JSONDecodeError:
                # Fallback: Try ast.literal_eval for single-quoted dictionaries
                import ast
                try:
                    data = ast.literal_eval(text_response)
                    if not isinstance(data, dict):
                         raise ValueError("Parsed data is not a dictionary")
                except Exception as parse_error:
                    print(f"JSON Parsing failed. Raw response snippet: {text_response[:200]}...")
                    raise parse_error

            # Post-processing
            clean_data = {}
            for field in fields:
                clean_data[field] = str(data.get(field, "")).strip()
                
            return clean_data

        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "resource exhausted" in error_str or "503" in error_str or "overloaded" in error_str:
                delay = base_delay * (2 ** attempt)
                print(f"Transient error (Rate limit/Overloaded) for {pdf_path}. Retrying in {delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
            else:
                print(f"Error extracting from {pdf_path}: {e}")
                return {field: "ERROR" for field in fields}
    
    print(f"Failed to extract from {pdf_path} after {max_retries} retries.")
    return {field: "ERROR" for field in fields}
