# Guía Maestra: De la Programación Orientada a Objetos a Productos de Software Reales

Esta guía está diseñada para llevarte desde los fundamentos de la Programación Orientada a Objetos (POO) hasta la construcción de sistemas de software robustos. Utilizaremos el proyecto que analizamos previamente como "semilla", expandiendo esos conceptos para mostrarte cómo se aplican en la industria.

---

## Módulo 1: El Corazón del Diseño - Programación Orientada a Objetos (POO)

En tu proyecto, vimos la clase `ImageExtractor`. Pero, ¿por qué usar clases en lugar de funciones sueltas?

### 1.1. Clases y Objetos: La Fábrica y el Producto
**El Concepto**: Una **Clase** es el plano o molde. Un **Objeto** es lo que construyes con ese molde.

**La Analogía**: 
Imagina una fábrica de coches.
- La **Clase** es el plano técnico del modelo "Sedán 2024". Define que tiene 4 ruedas, un motor y color.
- El **Objeto** es el coche rojo con matrícula XYZ-123 que sale de la línea de ensamblaje. Puedes crear miles de coches (objetos) del mismo plano (clase), pero cada uno tiene su propia gasolina y kilometraje.

**Variaciones y Aplicaciones Reales**:
En tu código, `ImageExtractor` encapsulaba la lógica de procesar imágenes. Sin POO, tendrías variables sueltas como `carpeta_salida`, `ancho_minimo`, dispersas por el código.

**Ejemplo de Código: Sistema Bancario**
*Problema*: Necesitamos manejar cuentas bancarias donde el saldo no pueda ser modificado directamente por error.

```python
class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self._saldo = saldo_inicial  # El guion bajo indica "privado" (convención)

    def depositar(self, cantidad):
        if cantidad > 0:
            self._saldo += cantidad
            print(f"Depositados ${cantidad}. Nuevo saldo: ${self._saldo}")

    def retirar(self, cantidad):
        if 0 < cantidad <= self._saldo:
            self._saldo -= cantidad
            return cantidad
        raise ValueError("Fondos insuficientes o cantidad inválida")

# Uso
mi_cuenta = CuentaBancaria("Herlis", 1000)
mi_cuenta.depositar(500)
# mi_cuenta._saldo = 1000000  <-- Posible, pero incorrecto. La clase protege la lógica.
```

### 1.2. Herencia: No Reinventes la Rueda
**El Concepto**: Crear nuevas clases basadas en clases existentes para reutilizar código.

**La Analogía**:
Un "Vehículo" es la clase padre. Tiene motor y ruedas.
Un "Camión" es un "Vehículo" (hereda todo lo anterior) pero añade "capacidad de carga".
Una "Moto" es un "Vehículo" pero añade "manillar".

**Aplicación en Proyectos Grandes**:
Imagina que estás construyendo un extractor para diferentes tipos de documentos, no solo PDFs de avalúos.

```python
class ExtractorBase:
    def __init__(self, archivo):
        self.archivo = archivo

    def validar_archivo(self):
        print(f"Validando existencia de {self.archivo}...")
        return True

class ExtractorPDF(ExtractorBase):
    def extraer_texto(self):
        print("Usando lógica específica para estructurar texto de PDF")

class ExtractorImagen(ExtractorBase):
    def extraer_texto(self):
        print("Usando OCR para leer texto de imagen")

# Ambos hijos tienen 'validar_archivo' gratis.
pdf = ExtractorPDF("documento.pdf")
pdf.validar_archivo() 
```

---

## Módulo 2: Patrones Avanzados y Composición

A veces, la herencia se vuelve complicada. Aquí es donde entra la **Composición**.

### 2.1. Composición sobre Herencia
**El Concepto**: En lugar de decir que un objeto "ES UN" (herencia), decimos que un objeto "TIENE UN" (composición).

**La Analogía**:
Un coche *TIENE UN* motor. No *ES UN* motor. Si cambias el motor, sigue siendo un coche.

**Caso Real**:
En tu proyecto, `ImageExtractor` usaba `config` pero no heredaba de él. Simplemente lo usaba. Esto es una forma simple de colaboración.

```python
class MotorElectrico:
    def mover(self):
        return "Silenciosamente moviendo ruedas..."

class MotorGasolina:
    def mover(self):
        return "Ruum ruum... moviendo ruedas..."

class Coche:
    def __init__(self, motor):
        self.motor = motor  # Inyección de dependencia (Composición)

    def conducir(self):
        print(self.motor.mover())

# Podemos cambiar el comportamiento del coche sin cambiar la clase Coche
tesla = Coche(MotorElectrico())
ford = Coche(MotorGasolina())
```

### 2.2. Polimorfismo y Clases Abstractas ("Interfaces")
**El Concepto**: Definir un "contrato" que todas las clases deben cumplir. Asegura que todos los extractores tengan un método `extract()`.

**Variación**: Uso de `ABC` (Abstract Base Classes).

```python
from abc import ABC, abstractmethod

class ProcesadorPago(ABC):
    @abstractmethod
    def pagar(self, monto):
        pass

class PayPal(ProcesadorPago):
    def pagar(self, monto):
        print(f"Pagando ${monto} vía PayPal API...")

class Stripe(ProcesadorPago):
    def pagar(self, monto):
        print(f"Pagando ${monto} vía Tarjeta de Crédito...")

def procesar_compra(procesador: ProcesadorPago, total):
    # No me importa qué procesador sea, sé que tiene el método .pagar()
    procesador.pagar(total)
```

---

## Módulo 3: Estructuras de Datos y Algoritmos Eficientes

Tu proyecto usaba diccionarios para mapear campos y listas para los PDFs.

### 3.1. Generadores (`yield`): Eficiencia de Memoria
**El Concepto**: En lugar de crear una lista gigante en memoria (e.g., millones de registros), generas uno a uno bajo demanda.

**Analogía**:
Una lista es como comprar 100 botellas de agua y guardarlas en tu mochila (pesado).
Un generador es como tener un grifo: solo obtienes agua cuando abres la llave (ligero).

**Aplicación Real**:
Procesar un archivo CSV de 10GB línea por línea.

```python
def leer_archivo_gigante(ruta):
    with open(ruta) as f:
        for linea in f:
            # Procesamos y "cedemos" el control
            yield linea.strip().upper()

# El bucle pide los datos uno a uno, la memoria se mantiene baja
for dato in leer_archivo_gigante("big_data.csv"):
    procesar(dato)
```

### 3.2. List/Dict Comprehensions
**El Concepto**: Crear listas/diccionarios de forma concisa y rápida (optimizada en C bajo el capó).

**Variación**:
Tu código tenía bucles `for` para crear listas.

```python
# Versión Clásica
cuadrados = []
for i in range(10):
    if i % 2 == 0:
        cuadrados.append(i**2)

# Versión Pythonica (Comprehension)
cuadrados = [i**2 for i in range(10) if i % 2 == 0]

# Dict Comprehension: Invertir un diccionario
pais_capital = {"Chile": "Santiago", "Colombia": "Bogotá"}
capital_pais = {v: k for k, v in pais_capital.items()}
```

---

## Módulo 4: Robustez y Manejo de Errores

En tu `extractor.py`, usaste `try-except` para llamadas a la API.

### 4.1. Excepciones Personalizadas
**El Concepto**: Crear tus propios tipos de error para que sean más descriptivos.

**Aplicación Real**:
Diferenciar entre "El archivo PDF está corrupto" y "La API de Gemini se cayó".

```python
class ErrorDeValidacionPDF(Exception):
    pass

class ErrorDeConexionAPI(Exception):
    pass

def procesar_documento(doc):
    if not doc.es_valido:
        raise ErrorDeValidacionPDF("El PDF no tiene texto seleccionable")
    if api_caida:
        raise ErrorDeConexionAPI("Sin respuesta del servidor 500")

try:
    procesar_documento(mi_doc)
except ErrorDeValidacionPDF as e:
    logger.warning(f"Salatando archivo: {e}") # Error leve
except ErrorDeConexionAPI as e:
    logger.critical(f"ALERTA: El sistema está caído: {e}") # Error grave
```

### 4.2. Context Managers (`with`) Personalizados
**El Concepto**: Ya usas `with open(...)`. Puedes crear tus propios bloques `with` para gestionar recursos (conexiones a BD, timers, bloqueos).

```python
import time

class Cronometro:
    def __enter__(self):
        self.inicio = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fin = time.time()
        print(f"Bloque ejecutado en {self.fin - self.inicio:.4f} segundos")

# Uso: Medir cuánto tarda tu extracción
with Cronometro():
    image_extractor.process_csv() 
    # Al terminar este bloque, se imprime el tiempo automáticamente
```

---

## Módulo 5: Proyecto Integrador - Construyendo un Sistema Real

¿Cómo unimos todos estos conceptos (OOP, Generadores, Excepciones, Patrones)? Imagina que escalamos tu proyecto a una **Plataforma SaaS de Procesamiento de Avalúos**.

### Arquitectura Propuesta

1.  **Core (Modelos)**: Clases que representan el negocio (`Avaluo`, `Inmueble`).
2.  **Servicios (Lógica)**: Clases que hacen el trabajo pesado (`GeminiService`, `PDFParser`).
3.  **Interfaz (API/CLI)**: Como el usuario interactúa (`main.py` o una API web con FastAPI).

### Código de Ejemplo Integrador

```python
# 1. Definición de Modelos (Data Classes para estructura limpia)
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AvaluoData:
    id_referencia: str
    valor_comercial: float
    direccion: str
    croquis_paths: List[str]

# 2. Interfaz Abstracta (Polimorfismo)
class IExtractor(ABC):
    @abstractmethod
    def extraer(self, fuente: str) -> AvaluoData:
        pass

# 3. Implementación Concreta (Herencia y Composición)
class ExtractorInteligente(IExtractor):
    def __init__(self, servicio_ai, servicio_ocr):
        self.ai = servicio_ai   # Inyección de dependencias
        self.ocr = servicio_ocr

    def extraer(self, ruta_pdf: str) -> AvaluoData:
        if not os.path.exists(ruta_pdf):
            raise FileNotFoundError(f"No existe: {ruta_pdf}")
            
        texto = self.ocr.leer_texto(ruta_pdf)
        datos_json = self.ai.analizar(texto)
        
        # Validamos y retornamos un objeto estructurado, no un simple dict
        return AvaluoData(
            id_referencia=datos_json.get("id"),
            valor_comercial=datos_json.get("valor"),
            direccion=datos_json.get("dir"),
            croquis_paths=[]
        )

# 4. Decoradores (Concepto Avanzado para Logging/Retries)
def reintentar(max_intentos=3):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for i in range(max_intentos):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Fallo intento {i+1}: {e}")
            raise Exception("Falló tras reintentos")
        return wrapper
    return decorador

class ServicioGemini:
    @reintentar(max_intentos=5)  # Aplicando el decorador
    def analizar(self, texto):
        # Simulación llamada API
        print("Llamando a Gemini...")
        return {"id": "REF-001", "valor": 500000, "dir": "Calle 123"}

# 5. Ejecución del Sistema (Main)
if __name__ == "__main__":
    servicio_ai = ServicioGemini()
    servicio_ocr = None # Placeholder
    
    # Composición: El extractor usa el servicio
    extractor = ExtractorInteligente(servicio_ai, servicio_ocr)
    
    try:
        resultado = extractor.extraer("avaluo_2024.pdf")
        print(f"Éxito: Avalúo procesado por ${resultado.valor_comercial}")
    except Exception as e:
        print(f"Error crítico en el sistema: {e}")
```

### Conclusión
Has pasado de escribir scripts que "hacen cosas" paso a paso, a diseñar sistemas donde:
1.  **Las Clases** protegen tus datos y organizan tu lógica.
2.  **Las Interfaces** te permiten cambiar componentes (ej. cambiar Gemini por GPT-4) sin romper el resto del código.
3.  **Los Generadores y Context Managers** hacen tu código eficiente y seguro.
4.  **Los Decoradores** añaden funcionalidad (como reintentos) de forma limpia.

Este es el camino para convertirse en un Ingeniero de Software Senior en Python.
