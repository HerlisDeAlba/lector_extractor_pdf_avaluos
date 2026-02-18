# Avaluos PDF Extractor Studio

Modular system for extracting data and croquis images from Real Estate Appraisal PDFs (Avalúos).

## Features
1.  **Data Extraction**: Extracts technical fields (Coefficient, Finishes, Equipment, etc.) into a CSV file using Gemini 2.5 Flash.
2.  **Croquis Extraction**: Automatically identifies, crops, and saves clean images of the property map (Croquis) based on the extracted CSV data.

## Setup

1.  **Prerequisites**:
    -   Python 3.10+
    -   Google Cloud API Key (Gemini)

2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment**:
    Create a `.env` file in the root directory:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

4.  **Folder Structure**:
    -   `Avaluos_PDF/`: Place your input PDF files here.
    -   `diccionario_maestro_avaluos_opt.csv`: Configuration of fields to extract.
    -   `src/`: Source code modules.

## Usage

Run the main studio script:

```bash
python main.py
```

Select an option from the menu:
-   **1. Extract Data Only**: Generates `resultado_extraccion.csv`.
-   **2. Extract Images Only**: Reads the CSV and generates images in `Croquis_Extraidos/`.
-   **3. Run Both**: Executes the full workflow.

## Output
-   **CSV**: `resultado_extraccion.csv`
-   **Images**: `Croquis_Extraidos/` containing clean PNG/JPEG files named as `[CONJUNTO]_[TIPO]_[AREA]m2_[HAB]hab.png`.
