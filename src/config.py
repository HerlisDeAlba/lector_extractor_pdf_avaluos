# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
PDF_FOLDER = 'Avaluos_PDF'
DICTIONARY_FILE = 'diccionario_maestro_avaluos_opt.csv'
OUTPUT_FILE = 'resultado_extraccion.csv'
MODEL_NAME = 'gemini-2.5-flash'

# Image Extraction Constants
IMAGE_OUTPUT_FOLDER = 'Croquis_Extraidos'
IMG_PADDING_PX = 20
IMG_CLUSTER_DISTANCE = 50
MIN_IMG_WIDTH = 250
MIN_IMG_HEIGHT = 200
MIN_IMG_SIZE_KB = 15
EXCLUDE_TOP_PCT = 0.08
EXCLUDE_BOTTOM_PCT = 0.08

# Croquis Validation Filters
MAX_DOMINANT_COLOR_RATIO = 0.85  # Skip if one color covers >85% of image (black pages, blank pages)
MAX_TEXT_WORDS_ON_PAGE = 100     # Skip if page has >100 words (text-heavy pages)
MIN_UNIQUE_COLORS = 50          # Skip if image has <50 unique colors (simple logos)
MIN_DRAWING_ELEMENTS = 5        # Skip if page has <5 drawing elements (not a floor plan)

def get_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Error: GOOGLE_API_KEY environment variable not set.")
    return api_key
