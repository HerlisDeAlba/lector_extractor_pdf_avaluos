import os
import shutil
import sys
from src import image_extractor, config

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def clean_folder():
    folder = config.IMAGE_OUTPUT_FOLDER
    if os.path.exists(folder):
        print(f"Cleaning {folder}...")
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(folder)

if __name__ == "__main__":
    clean_folder()
    print("Starting Extraction...")
    extractor = image_extractor.ImageExtractor()
    extractor.process_csv()
