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
MIN_IMG_WIDTH = 100
MIN_IMG_HEIGHT = 100
MIN_IMG_SIZE_KB = 5             # Min size in KB. Maps can be small (~6KB).
EXCLUDE_TOP_PCT = 0.08
EXCLUDE_BOTTOM_PCT = 0.08

# Croquis Validation Filters
MAX_DOMINANT_COLOR_RATIO = 0.94  # Skip if one color covers >94% of image (blank pages).
MAX_TEXT_WORDS_ON_PAGE = 800     # Skip if page has >800 words (text-heavy pages)
MIN_UNIQUE_COLORS = 10           # Skip if image has <10 unique colors (simple logos)
MIN_DRAWING_ELEMENTS = 1         # Skip if page has <1 drawing elements (not a floor plan)

# Filters for False Positives
MAX_ASPECT_RATIO = 4.0           # Skip images wider than 4x height (footers/headers)
MIN_COLORS_FOR_WIDE_MAP = 70     # Exception: wide images with >= 70 colors are panoramic maps (not footers)
MIN_BRIGHTNESS_MEAN = 80         # Skip very dark images. Maps can be ~88.
MAX_LOCAL_TEXTURE_STD = 50.0     # Skip images with high LOCAL variation (room photos). Floor plans/maps score <35.

# Proximity Keywords
PHOTO_KEYWORDS = [
    "baño", "social", "patio", "interior", "cocina", "sala", "comedor", 
    "alcoba", "fachada", "gas", "contador", "parqueadero", "depósito",
    "piso", "techo", "muro", "ventana", "puerta"
]
CROQUIS_KEYWORDS = [
    "croquis", "localización", "microlocalización", "macrolocalización", 
    "plano", "mapa", "distribución", "ubicación", "entorno"
]


def get_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Error: GOOGLE_API_KEY environment variable not set.")
    return api_key
