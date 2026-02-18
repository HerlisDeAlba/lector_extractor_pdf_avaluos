import os
import glob
import time
from src import config, gemini_service, data_manager, extractor, image_extractor

def run_data_extraction():
    print("\n--- STEP 1: DATA EXTRACTION ---")
    try:
        client = gemini_service.setup_client()
    except Exception as e:
        print(f"Setup failed: {e}")
        return

    print(f"Loading dictionary from {config.DICTIONARY_FILE}...")
    fields = data_manager.load_dictionary_fields(config.DICTIONARY_FILE)
    if not fields:
        print("No fields found.")
        return

    pdf_files = glob.glob(os.path.join(config.PDF_FOLDER, "*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {config.PDF_FOLDER}.")
        return
    print(f"Found {len(pdf_files)} PDFs.")

    if not data_manager.initialize_csv(config.OUTPUT_FILE, fields):
        return

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        data = extractor.extract_from_pdf(client, pdf_path, fields)
        if 'ARCHIVO' in fields:
            data['ARCHIVO'] = os.path.basename(pdf_path)
        
        data_manager.append_to_csv(config.OUTPUT_FILE, fields, data)
        print(f"Finished {pdf_path}")
        print("Waiting 10 seconds...")
        time.sleep(10)
        
    print(f"Data Extraction complete. Results saved to {config.OUTPUT_FILE}")

def run_image_extraction():
    print("\n--- STEP 2: IMAGE EXTRACTION (CROQUIS) ---")
    if not os.path.exists(config.OUTPUT_FILE):
        print(f"Error: CSV file {config.OUTPUT_FILE} not found. Run Data Extraction first.")
        return
        
    img_extractor = image_extractor.ImageExtractor()
    img_extractor.process_csv()

def main():
    print("=== AVALUO EXTRACTOR STUDIO ===")
    print("Mode: AUTOMATIC FULL WORKFLOW (Data + Images)")
    
    # Step 1: Data
    run_data_extraction()
    
    # Step 2: Images
    run_image_extraction()
    
    print("\nAll tasks completed successfully.")

#if __name__ == "__main__":
#    main()

main()
