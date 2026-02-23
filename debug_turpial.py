import pandas as pd
import os
from src import image_extractor, config

# Create filtered CSV
try:
    df = pd.read_csv('resultado_extraccion.csv', sep=';', encoding='utf-8-sig', dtype=str)
    # Filter for AvaluUo.pdf (Turpial)
    turpial_df = df[df['ARCHIVO'].str.contains('AvaluUo.pdf', case=False, na=False)]
    
    if turpial_df.empty:
        print("TURPIAL not found in CSV!")
    else:
        turpial_df.to_csv('debug_turpial.csv', index=False, sep=';', encoding='utf-8-sig')
        print("Created debug_turpial.csv for AvaluUo.pdf")
        
        # Override config output file
        config.OUTPUT_FILE = 'debug_turpial.csv'
        
        # Run extractor
        print("Running extractor for TURPIAL...")
        extractor = image_extractor.ImageExtractor()
        extractor.process_csv()

except Exception as e:
    print(f"Error: {e}")
