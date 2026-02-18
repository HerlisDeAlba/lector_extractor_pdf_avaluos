# Análisis de Conceptos de Python en el Proyecto

Este documento detalla los conceptos de Python identificados en el proyecto `lector_extractor_pdf_avaluos`, explicando qué es cada concepto y cómo se aplica específicamente en este código.

## 1. Modularización y Organización de Código

### Importación de Módulos
Python permite dividir el código en múltiples archivos para mantenerlo organizado.
- **Concepto**: Uso de `import` y `from ... import ...`.
- **Aplicación en el Proyecto**:
  - `main.py` importa módulos locales ubicados en la carpeta `src`: `from src import config, gemini_service, data_manager...`.
  - Se utilizan rutas relativas dentro de `src` (e.g., `from . import config` en `extractor.py`).
  - Se importan librerías estándar (`os`, `json`, `time`) y externas (`pandas`, `fitz`).

### Variables de Entorno y Configuración
Separar la configuración del código lógico.
- **Concepto**: Uso de archivos `.env` y librerías como `dotenv`.
- **Aplicación en el Proyecto**:
  - Archivo `src/config.py` carga variables con `load_dotenv()` y define constantes globales (`PDF_FOLDER`, `MODEL_NAME`) que son accesadas por otros módulos.
  - Se protege información sensible (API KEY) usando `os.environ.get("GOOGLE_API_KEY")`.

---

## 2. Programación Orientada a Objetos (OOP)

### Clases y Objetos
Encapsulamiento de lógica relacionada y estado.
- **Concepto**: Definición de `class` con `__init__` y métodos.
- **Aplicación en el Proyecto**:
  - **`ImageExtractor` (en `src/image_extractor.py`)**:
    - **Encapsulamiento**: Agrupa toda la lógica compleja de procesamiento de imágenes.
    - **Constructor (`__init__`)**: Inicializa carpetas de salida.
    - **Métodos de Instancia**: `process_csv`, `extract_primary_image`, etc., manipulan el estado y realizan acciones específicas del objeto.

---

## 3. Manejo de Archivos (File I/O)

### Context Managers (`with`)
Garantiza que los archivos se cierren correctamente después de usarse.
- **Concepto**: Bloque `with open(...) as f:`.
- **Aplicación en el Proyecto**:
  - **CSV**: Lectura y escritura segura en `src/data_manager.py` (`with open(csv_path, ...)`).
  - **Imágenes**: Escritura binaria de imágenes extraídas en `src/image_extractor.py` (`with open(out_path, "wb") as f:`).

### Manipulación de Archivos y Rutas
Interacción con el sistema de archivos del sistema operativo.
- **Concepto**: Librería `os` y `glob`.
- **Aplicación en el Proyecto**:
  - `os.path.join`: Construcción de rutas compatibles con cualquier SO (Windows/Linux).
  - `os.path.exists`: Verificación de existencia de archivos antes de procesar.
  - `glob.glob`: Búsqueda de patrones de archivos (`*.pdf`).
  - `os.makedirs`: Creación de directorios si no existen.

---

## 4. Estructuras de Datos y Tipos

### Listas y Diccionarios
Almacenamiento y manipulación de colecciones de datos.
- **Concepto**: `[]` (listas) y `{}` (diccionarios).
- **Aplicación en el Proyecto**:
  - **Diccionarios**: Usados extensivamente para pasar datos entre funciones (e.g., el resultado de la extracción de Gemini es un diccionario JSON convertido).
  - **Listas**: Almacenamiento de los campos (headers) del CSV y lista de PDFs a procesar.

### Conjuntos (Sets)
Colecciones desordenadas de elementos únicos.
- **Concepto**: `set()`.
- **Aplicación en el Proyecto**:
  - `src/image_extractor.py`: Usado en `parse_pages` para evitar procesar la misma página dos veces si el usuario la ingresa repetida (`pages = set()`).

---

## 5. Control de Flujo

### Bucles (Loops)
Repetición de tareas.
- **Concepto**: `for` y `while`.
- **Aplicación en el Proyecto**:
  - `main.py`: Itera sobre cada archivo PDF (`for pdf_path in pdf_files:`).
  - `src/extractor.py`: Implementa lógica de reintento (`retry`) con un bucle `for attempt in range(max_retries):`.
  - `src/gemini_service.py`: Espera activa (`polling`) mientras un archivo se procesa (`while file.state == "PROCESSING":`).

### Manejo de Errores (Try/Except)
Gestión de excepciones para evitar que el programa colapse.
- **Concepto**: Bloques `try...except`.
- **Aplicación en el Proyecto**:
  - **Robustez**: En `src/extractor.py`, si falla la API de Gemini, se captura la excepción, se espera un tiempo y se reintenta.
  - **Validación de Datos**: En `src/data_manager.py`, se manejan errores si el archivo CSV no tiene el formato correcto o está bloqueado.
  - **Parsing**: `json.loads` está protegido para manejar respuestas mal formadas del LLM (`json.JSONDecodeError`), con un fallback a `ast.literal_eval`.

---

## 6. Integración de Librerías Externas

### Pandas (Análisis de Datos)
- **Concepto**: DataFrames para manipulación tabular.
- **Aplicación**: En `src/image_extractor.py`, se usa `pd.read_csv` para leer el archivo de control y filtrar qué croquis extraer (`df.iterrows()`).

### PyMuPDF (fitz) (Procesamiento de PDF)
- **Concepto**: Manipulación de documentos PDF a bajo nivel.
- **Aplicación**:
  - Extracción de texto y coordenadas (`page.get_drawings()`).
  - Renderizado de páginas a imágenes (`page.get_pixmap()`).
  - Extracción de imágenes incrustadas (`doc.extract_image()`).

### Google Generative AI (LLM)
- **Concepto**: Uso de APIs de Inteligencia Artificial.
- **Aplicación**: En `src/src/gemini_service.py` y `extractor.py`, se configura el cliente, se suben archivos y se envían prompts para extracción de información no estructurada.

### Pillow (PIL) y Numpy (Procesamiento de Imágenes)
- **Concepto**: Manipulación de arrays numéricos y procesamiento de imágenes.
- **Aplicación**:
  - Validación de imágenes: Convertir imagen a array (`np.array(img)`).
  - Análisis de píxeles: Contar colores únicos para determinar si una imagen es un plano válido o un logo simple (`np.unique`).

---

## 7. Técnicas Avanzadas y Algoritmos

### Lógica de Reintentos (Exponential Backoff)
- **Aplicación**: En `src/extractor.py`, si la API falla por límite de velocidad (error 429), el tiempo de espera se duplica en cada intento (`delay = base_delay * (2 ** attempt)`).

### Prompt Engineering
- **Aplicación**: En `src/extractor.py`, se construye un prompt dinámico inyectando la lista de campos requeridos y dando instrucciones precisas ("Role: Expert Data Extractor") para obtener una salida JSON limpia.

### Algoritmos Geométricos
- **Aplicación**: En `src/image_extractor.py`, se implementa lógica para agrupar trazos cercanos (`rect_distance`, clustering) y determinar el área de recorte óptima para un plano arquitectónico.

### Validación de Datos con AST
- **Aplicación**: Uso de `ast.literal_eval` como mecanismo de seguridad si `json.loads` falla, permitiendo parsear diccionarios de Python que parezcan JSON pero tengan comillas simples.
