# Módulo 8: Proyecto Integrador - Sistema de Biblioteca

Has aprendido Clases, Herencia, Composición, Excepciones, Generadores, Decoradores y Context Managers.
Ahora vamos a construir algo real.

## El Reto: Sistema de Gestión de Biblioteca

Queremos un sistema que gestione libros, usuarios y préstamos.
Requisitos:
1.  **Libros y Revistas**: Ambos son "Items". Las revistas tienen número de edición.
2.  **Usuarios**: Tienen nombre y lista de préstamos.
3.  **Log**: Decorador que registre cada préstamo.
4.  **Base de Datos**: Simular conexión con Context Manager.
5.  **Búsqueda**: Iterador eficiente para buscar libros por título.

---

## Implementación Paso a Paso

### 1. Modelos (Inmutables con Dataclasses)

```python
from abc import ABC, abstractmethod
from datetime import datetime

class ItemBiblioteca(ABC):
    def __init__(self, titulo, id):
        self.titulo = titulo
        self.id = id
        self.prestado = False

    def __str__(self):
        return f"{self.titulo} ({'Prestado' if self.prestado else 'Disponible'})"

class Libro(ItemBiblioteca):
    def __init__(self, titulo, id, autor):
        super().__init__(titulo, id)
        self.autor = autor

class Revista(ItemBiblioteca):
    def __init__(self, titulo, id, edicion):
        super().__init__(titulo, id)
        self.edicion = edicion
```

### 2. Helpers (Decoradores y Errores)

```python
class ItemNoDisponibleError(Exception):
    pass

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {datetime.now()}: Ejecutando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### 3. El Sistema Principal (Gestor)

```python
class Biblioteca:
    def __init__(self):
        self.items = [] # Composición: La biblioteca TIENE items
        self.usuarios = []

    def agregar_item(self, item):
        self.items.append(item)

    # Generador para búsqueda eficiente
    def buscar(self, query):
        for item in self.items:
            if query.lower() in item.titulo.lower():
                yield item

    @logger
    def prestar(self, item_id, usuario):
        # List comprehension para encontrar item
        found = [i for i in self.items if i.id == item_id]
        if not found:
            raise ValueError("Item no existe")
        
        item = found[0]
        if item.prestado:
            raise ItemNoDisponibleError(f"El item {item.titulo} ya está prestado")
            
        item.prestado = True
        usuario.prestamos.append(item)
        print(f"Prestado {item.titulo} a {usuario.nombre}")
```

---

## ejercicios finales: Arquitectura y Diseño

A continuación, 10 retos de diseño para mejorar este sistema.

### Ejercicio 1: Devolver Libro
Implementa el método `devolver(item_id, usuario)` en `Biblioteca`. Debe marcar `prestado=False`.

<details>
<summary>Ver Solución</summary>

```python
def devolver(self, item_id, usuario):
    # Buscar, marcar prestado=False, remover de lista usuario
    item = [i for i in self.items if i.id == item_id][0]
    item.prestado = False
    usuario.prestamos.remove(item)
    print("Devuelto")
```
</details>

### Ejercicio 2: Límite de Préstamos
Modifica `prestar` para lanzar error si el usuario ya tiene más de 3 libros.

<details>
<summary>Ver Solución</summary>

```python
if len(usuario.prestamos) >= 3:
    raise Exception("Límite de préstamos excedido")
```
</details>

### Ejercicio 3: Multas (Herencia)
Crea una interfaz `IMulta` y clases `MultaLeve` y `MultaGrave`. Añade un sistema de cálculo de multas por retraso.

<details>
<summary>Ver Solución</summary>

```python
class Multa:
    def calcular(self, dias): return dias * 1

class MultaGrave(Multa):
    def calcular(self, dias): return dias * 5
```
</details>

### Ejercicio 4: Reporte en CSV (Context Manager)
Crea método `generar_reporte()` que use `with open(...)` para guardar todos los libros en un CSV.

<details>
<summary>Ver Solución</summary>

```python
def generar_reporte(self):
    with open("libros.csv", "w") as f:
        f.write("ID,Titulo,Estado\n")
        for i in self.items:
            f.write(f"{i.id},{i.titulo},{i.prestado}\n")
```
</details>

### Ejercicio 5: Singleton para Config
Asegura que solo exista una instancia de `ConfiguracionBiblioteca` (singleton pattern).

<details>
<summary>Ver Solución</summary>

```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
</details>

### Ejercicio 6: Notificaciones (Observer Pattern)
Haz que cuando se preste un libro, se notifique a un sistema de email simulado.

<details>
<summary>Ver Solución</summary>

```python
# Lista de observadores
def prestar(...):
    # ... logica ...
    for obs in self.observadores:
        obs.notificar(f"Libro prestado: {item.titulo}")
```
</details>

### Ejercicio 7: Filtros Avanzados (Funcional)
Usa `filter()` y `lambda` para obtener todos los libros que NO están prestados.

<details>
<summary>Ver Solución</summary>

```python
disponibles = list(filter(lambda x: not x.prestado, biblioteca.items))
```
</details>

### Ejercicio 8: Decorador de Permisos
Crea `@admin_required`. Solo permite agregar items si el usuario actual es admin.

<details>
<summary>Ver Solución</summary>

```python
def admin_required(f):
    def wrapper(self, *args, **kwargs):
        if not self.current_user.is_admin:
            raise Exception("Acceso denegado")
        return f(self, *args, **kwargs)
    return wrapper
```
</details>

### Ejercicio 9: Serialización JSON
Añade método `to_json()` a `ItemBiblioteca` y sus hijos para poder guardar el estado completo en archivo JSON.

<details>
<summary>Ver Solución</summary>

```python
import json
def to_json(self):
    return json.dumps(self.__dict__)
```
</details>

### Ejercicio 10: Pruebas Unitarias (UnitTest)
Escribe un test simple usando `unittest` que verifique que `prestar` cambia el estado del libro.

<details>
<summary>Ver Solución</summary>

```python
import unittest
class TestBiblio(unittest.TestCase):
    def test_prestar(self):
        b = Biblioteca()
        l = Libro("Test", 1, "Yo")
        b.agregar_item(l)
        u = Usuario("Pepe")
        b.prestar(1, u)
        self.assertTrue(l.prestado)
```
</details>
