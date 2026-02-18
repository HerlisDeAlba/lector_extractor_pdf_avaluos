# Módulo 7: Context Managers - El Arte de Limpiar

En Python, abrir recursos (archivos, conexiones a base de datos, sockets) es fácil. Lo difícil es acordarse de cerrarlos, especialmente si hay errores de por medio.

## 1. El Concepto: `with`

La declaración `with` crea un contexto de ejecución. Garantiza que, pase lo que pase (incluso si hay un error), se ejecutarán acciones de limpieza al salir.

**Manera Fea:**
```python
f = open("archivo.txt", "w")
try:
    f.write("Hola")
finally:
    f.close() # Si te olvidas de esto, el archivo queda bloqueado
```

**Manera Elegante:**
```python
with open("archivo.txt", "w") as f:
    f.write("Hola")
# Aquí f.close() se llama automáticamente
```

---

## 2. Creando tus propios Context Managers

Puedes hacer que tus clases soporten `with` implementando `__enter__` y `__exit__`.

```python
class Cronometro:
    def __enter__(self):
        print("Iniciando cronómetro...")
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Se ejecuta siempre al salir del bloque
        end = time.time()
        print(f"Tiempo total: {end - self.start:.2f}s")
        # Si hubo una excepción, exc_type no sería None.
        # Retornar False (defecto) hace que el error se propague.

with Cronometro():
    time.sleep(1)
```

También puedes usar un generador con decorador `@contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def abrir_archivo_seguro(nombre):
    print("Abriendo...")
    f = open(nombre, "w")
    try:
        yield f
    finally:
        print("Cerrando...")
        f.close()
```

---

## 4. Ejercicios Prácticos

### Ejercicio 1: Etiqueta HTML
Crea un CM `Etiqueta` que imprima `<tag>` al entrar y `</tag>` al salir.

<details>
<summary>Ver Solución</summary>

```python
class Etiqueta:
    def __init__(self, tag): self.tag = tag
    
    def __enter__(self):
        print(f"<{self.tag}>")
        
    def __exit__(self, t, v, tr):
        print(f"</{self.tag}>")

with Etiqueta("h1"):
    print("Hola Mundo")
```
</details>

### Ejercicio 2: Silenciador de Errores
Crea `Suprimir` que capture y oculte cualquier excepción que ocurra dentro del bloque (`__exit__` debe devolver `True`).

<details>
<summary>Ver Solución</summary>

```python
class Suprimir:
    def __enter__(self): pass
    
    def __exit__(self, t, v, tr):
        print(f"Error suprimido: {v}")
        return True # Evita que el programa explote

with Suprimir():
    1 / 0
print("Vivo!")
```
</details>

### Ejercicio 3: Cambio de Directorio (cd)
Crea `MiCD` que cambie de directorio (`os.chdir`) al entrar, y vuelva al original al salir.

<details>
<summary>Ver Solución</summary>

```python
import os
class MiCD:
    def __init__(self, nuevo_dir):
        self.nuevo = nuevo_dir
        self.origen = os.getcwd()
        
    def __enter__(self):
        os.chdir(self.nuevo)
        
    def __exit__(self, t, v, tr):
        os.chdir(self.origen)
```
</details>

### Ejercicio 4: Archivo Temporal
Crea `TempFile` que cree un archivo, deje escribir en él, y lo borre (`os.remove`) al salir.

<details>
<summary>Ver Solución</summary>

```python
import os
class TempFile:
    def __init__(self, nombre): self.nombre = nombre
    
    def __enter__(self):
        self.f = open(self.nombre, 'w')
        return self.f
    
    def __exit__(self, t, v, tr):
        self.f.close()
        os.remove(self.nombre)
        print("Archivo borrado")
```
</details>

### Ejercicio 5: Indentador
Crea `Indent`. Variable global `nivel = 0`. Al entrar `nivel += 1`, al salir `nivel -= 1`. Crea función `print_ind` que imprima con espacios según nivel.

<details>
<summary>Ver Solución</summary>

```python
nivel = 0
def print_ind(s): print("  "*nivel + s)

class Indent:
    def __enter__(self):
        global nivel
        nivel += 1
    def __exit__(self, t, v, tr):
        global nivel
        nivel -= 1

with Indent():
    print_ind("Nivel 1")
    with Indent():
        print_ind("Nivel 2")
```
</details>

### Ejercicio 6: Medidor de Tiempo (Contextlib)
Usa `@contextmanager` para crear una versión simple del Ejercicio 3 del módulo anterior (Timer).

<details>
<summary>Ver Solución</summary>

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    t0 = time.time()
    yield
    print(time.time() - t0)
```
</details>

### Ejercicio 7: Bloqueo (Lock) Simulado
Simula un sistema de exclusión. Clase `Lock` imprime "Bloqueando recurso" al entrar y "Liberando" al salir.

<details>
<summary>Ver Solución</summary>

```python
class Lock:
    def __enter__(self): print("Bloqueando...")
    def __exit__(self, t, v, tr): print("Liberando...")
```
</details>

### Ejercicio 8: Base de Datos Fake
Clase `DBContext`. `__enter__` retorna una "conexión" (string "Connected"). `__exit__` imprime "Disconnected". Si hubo error, imprime "Rollback", si no "Commit".

<details>
<summary>Ver Solución</summary>

```python
class DBContext:
    def __enter__(self):
        print("Connected")
        return "Conexión"
    
    def __exit__(self, t, v, tr):
        if t is None:
            print("Commit")
        else:
            print("Rollback")
        print("Disconnected")
```
</details>

### Ejercicio 9: Redirección de stdout (Avanzado)
Haz que `with CapturarImpresion() as logs:` guarde todo lo que se imprima con `print` dentro del bloque en una lista, en vez de salir a consola. (Pista: `sys.stdout`).

<details>
<summary>Ver Solución</summary>

```python
import sys
from io import StringIO

class Capturar:
    def __enter__(self):
        self.old = sys.stdout
        self.buffer = StringIO()
        sys.stdout = self.buffer
        return self.buffer
    
    def __exit__(self, t, v, tr):
        sys.stdout = self.old

with Capturar() as cap:
    print("Hola secreto")
    
print("Capturado:", cap.getvalue())
```
</details>

### Ejercicio 10: Multi-contexto
Python permite `with A() as a, B() as b:`. Crea dos CM simples y úsalos juntos.

<details>
<summary>Ver Solución</summary>

```python
class A:
    def __enter__(self): print("A entra")
    def __exit__(self, *a): print("A sale")

class B:
    def __enter__(self): print("B entra")
    def __exit__(self, *a): print("B sale")

with A(), B():
    print("Dentro")
```
</details>
