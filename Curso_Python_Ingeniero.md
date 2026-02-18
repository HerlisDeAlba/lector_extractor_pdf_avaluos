# Curso Maestro de Python: De Cero a Ingeniero (Versión Definitiva)
*Todos los temas del proyecto, explicados paso a paso con ejemplos universales.*

Esta guía está diseñada para que aprendas **toda** la tecnología aplicada en tu proyecto "Lector de Avalúos", pero en un orden lógico: desde lo más básico hasta la ingeniería avanzada.

---

## FASE 1: FUNDAMENTOS DE PROGRAMACIÓN
*La base absoluta. Sin esto, no puedes leer el código.*

### Nivel 1: Variables y Tipos de Datos
**Concepto:** Guardar información en la memoria.
*   **En tu proyecto:** Guardar nombres de archivos, claves API, contadores.
*   **Ejemplo Genérico:**
    ```python
    nombre = "Carlos"  # Texto (String)
    edad = 30          # Entero (Integer)
    altura = 1.75      # Decimal (Float)
    es_estudiante = True # Booleano
    ```
*   **Ejercicio:**
    Crea una variable `ciudad` con el nombre de tu ciudad y `temperatura` con un número decimal. Imprime: "En [ciudad] hace [temperatura] grados".
    <details><summary>Ver Solución</summary>

    ```python
    ciudad = "Bogotá"
    temperatura = 18.5
    print(f"En {ciudad} hace {temperatura} grados")
    ```
    </details>

### Nivel 2: Listas (`list`)
**Concepto:** Colecciones ordenadas de cosas.
*   **En tu proyecto:** La lista de archivos PDF encontrados (`pdf_files`), la lista de páginas a procesar.
*   **Ejemplo Genérico:**
    ```python
    compras = ["Huevos", "Pan", "Leche"]
    compras.append("Café")  # Agregar al final
    print(compras[0])       # Ver el primero: "Huevos"
    ```
*   **Ejercicio:**
    Tienes una lista `amigos = ["Ana", "Luis"]`. Agrega a "Pedro" y luego imprime el último nombre de la lista.
    <details><summary>Ver Solución</summary>

    ```python
    amigos = ["Ana", "Luis"]
    amigos.append("Pedro")
    print(amigos[-1])
    ```
    </details>

### Nivel 3: Diccionarios (`dict`)
**Concepto:** Datos con nombre (Clave: Valor).
*   **En tu proyecto:** **CRÍTICO**. Toda la data extraída del PDF viaja en un diccionario (`clean_data`).
*   **Ejemplo Genérico:**
    ```python
    usuario = {
        "nombre": "Ana",
        "email": "ana@test.com",
        "puntos": 500
    }
    print(usuario["email"])
    ```
*   **Ejercicio:**
    Crea un diccionario `libro` con `titulo` y `autor`. Imprime una frase con esos datos.
    <details><summary>Ver Solución</summary>

    ```python
    libro = {"titulo": "El Principito", "autor": "Saint-Exupéry"}
    print(f"Leo {libro['titulo']} de {libro['autor']}")
    ```
    </details>

### Nivel 4: Condicionales (`if`, `else`)
**Concepto:** Tomar decisiones.
*   **En tu proyecto:** ¿El archivo existe? ¿La imagen es oscura? ¿Tiene croquis?
*   **Ejemplo Genérico:**
    ```python
    bateria = 10
    if bateria < 20:
        print("Recargar")
    else:
        print("Todo bien")
    ```
*   **Ejercicio:**
    Variable `edad = 15`. Si es menor de 18 imprime "Menor", si no "Mayor".
    <details><summary>Ver Solución</summary>

    ```python
    edad = 15
    if edad < 18:
        print("Menor")
    else:
        print("Mayor")
    ```
    </details>

### Nivel 5: Bucles (`for`)
**Concepto:** Repetir tareas automáticamente.
*   **En tu proyecto:** Procesar *cada* PDF de la carpeta, procesar *cada* página del documento.
*   **Ejemplo Genérico:**
    ```python
    for i in range(3):
        print(f"Intento #{i}")
    ```
*   **Ejercicio:**
    Tienes `numeros = [2, 4, 5]`. Multiplica cada uno por 10 e imprímelo.
    <details><summary>Ver Solución</summary>

    ```python
    numeros = [2, 4, 5]
    for n in numeros:
        print(n * 10)
    ```
    </details>

### Nivel 6: Funciones (`def`)
**Concepto:** Empaquetar código para reusarlo.
*   **En tu proyecto:** `load_dictionary_fields`, `clean_number`, `setup_client`.
*   **Ejemplo Genérico:**
    ```python
    def saludar(nombre):
        return f"Hola {nombre}!"
    
    msg = saludar("Maria")
    ```
*   **Ejercicio:**
    Crea una función `es_par(numero)` que retorne `True` si el número es par (usa `% 2 == 0`) y `False` si no.
    <details><summary>Ver Solución</summary>

    ```python
    def es_par(numero):
        if numero % 2 == 0:
            return True
        else:
            return False
    ```
    </details>

---

## FASE 2: MANEJO DE DATOS Y ARCHIVOS (Intermedio)

### Nivel 7: Archivos y Rutas (`os`, `glob`)
**Concepto:** Hablar con el Sistema Operativo.
*   **En tu proyecto:** Buscar todos los `.pdf` y crear carpetas de salida.
*   **Ejemplo Genérico:**
    ```python
    import os
    if not os.path.exists("backup"):
        os.makedirs("backup")
    ```
*   **Ejercicio:**
    Verifica si existe el archivo "test.txt". Si no existe, imprime "Falta archivo".
    <details><summary>Ver Solución</summary>

    ```python
    import os
    if not os.path.exists("test.txt"):
        print("Falta archivo")
    ```
    </details>

### Nivel 8: Pandas (`pandas`)
**Concepto:** Excel programable.
*   **En tu proyecto:** Leer el CSV de resultados, filtrar qué PDFs ya tienen croquis (`df.iterrows`).
*   **Ejemplo Genérico:**
    ```python
    import pandas as pd
    df = pd.DataFrame({"Nombre": ["A", "B"], "Edad": [20, 30]})
    mayores = df[df["Edad"] > 25]
    ```
*   **Ejercicio:**
    Crea un DataFrame de `Ventas` con [100, 50, 200]. Filtra y muestra solo las ventas mayores a 80.
    <details><summary>Ver Solución</summary>

    ```python
    import pandas as pd
    df = pd.DataFrame({"Ventas": [100, 50, 200]})
    print(df[df["Ventas"] > 80])
    ```
    </details>

### Nivel 9: Expresiones Regulares (`re`)
**Concepto:** Búsqueda avanzada de texto.
*   **En tu proyecto:** Encontrar "Página 12" o limpiar nombres de archivos raros.
*   **Ejemplo Genérico:**
    ```python
    import re
    texto = "Mi código es ABC-123"
    match = re.search(r'\d+', texto) # Busca números
    print(match.group()) # "123"
    ```
*   **Ejercicio:**
    Extrae el email de: "Contactar a soporte@web.com hoy".
    <details><summary>Ver Solución</summary>

    ```python
    import re
    texto = "Contactar a soporte@web.com hoy"
    match = re.search(r'[\w]+@[\w\.]+', texto)
    if match: print(match.group())
    ```
    </details>

---

## FASE 3: INGENIERÍA DE SOFTWARE (Avanzado)

### Nivel 10: Manejo de Errores y Resiliencia (`try/except`, `time`)
**Concepto:** Programas que no se rinden.
*   **En tu proyecto:** Cuando la API de Gemini falla (`429 Overloaded`), tu código espera y reintenta (Backoff exponencial).
*   **Ejemplo Genérico:**
    ```python
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Error matemático")
    ```
*   **Ejercicio:**
    Haz un bucle `for` de 3 intentos. En cada intento usa `time.sleep(1)` para simular una espera.
    <details><summary>Ver Solución</summary>

    ```python
    import time
    for i in range(3):
        print("Reintentando...")
        time.sleep(1)
    ```
    </details>

### Nivel 11: Seguridad y Configuración (`dotenv`)
**Concepto:** Proteger secretos.
*   **En tu proyecto:** La `GOOGLE_API_KEY` nunca está en el código, vive en `.env`.
*   **Ejemplo Genérico:**
    ```python
    import os
    # Simular lectura de variable de entorno
    # os.environ["CLAVE"] = "secreto"
    clave = os.getenv("CLAVE")
    ```

### Nivel 12: Programación Orientada a Objetos (`class`)
**Concepto:** Estructurar programas grandes.
*   **En tu proyecto:** La clase `ImageExtractor` empaqueta toda la lógica de imágenes.
*   **Ejemplo Genérico:**
    ```python
    class Perro:
        def __init__(self, nombre):
            self.nombre = nombre
        def ladrar(self):
            print("Guau!")
    ```
*   **Ejercicio:**
    Crea una clase `Coche` con método `arrancar` que imprima "Brum brum". Instancia uno y úsalo.
    <details><summary>Ver Solución</summary>

    ```python
    class Coche:
        def arrancar(self):
            print("Brum brum")
    mi_coche = Coche()
    mi_coche.arrancar()
    ```
    </details>

---

## FASE 4: TECNOLOGÍAS ESPECIALIZADAS (Nivel Experto)

### Nivel 13: PDFs y Coordenadas (`pymupdf`)
**Concepto:** Entender documentos estructuralmente.
*   **En tu proyecto:** Extraer imágenes (`doc.extract_image`) y renderizar páginas (`page.get_pixmap`).
*   **Detalle:** Entender que una página tiene ancho/alto y las cosas están en coordenadas (x, y).

### Nivel 14: Visión por Computadora y Matrices (`numpy`, `PIL`)
**Concepto:** Las imágenes son matemáticas.
*   **En tu proyecto:** `is_image_valid_croquis` convierte la imagen a números (`numpy.array`) para contar colores únicos y decidir si es un plano válido.
*   **Ejercicio Conceptual:**
    Si tienes una matriz de ceros (negro) y le sumas 255, obtienes blanco. Así se manipula el brillo.

### Nivel 15: Integración con IA (`google-genai`)
**Concepto:** Usar cerebros externos.
*   **En tu proyecto:** Subir archivos, esperar a que estén listos (Polling), y enviar prompts estructurados (JSON).
*   **Clave:** La IA no es mágica, es una función que recibe texto/archivo y devuelve texto.

---

### Tu Plan de Acción
Tienes 15 Niveles. No te saltes ninguno.
1.  Empieza hoy con los **Niveles 1 al 3**.
2.  Usa `practica.py`.
3.  Cuando llegues al **Nivel 8 (Pandas)**, sentirás el verdadero poder.
