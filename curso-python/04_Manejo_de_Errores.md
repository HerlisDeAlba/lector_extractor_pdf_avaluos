# Módulo 4: Programación Robusta - Manejo de Errores

Un programa junior crashea cuando algo sale mal. Un programa senior sabe qué hacer cuando algo sale mal.

## 1. El Concepto: Excepciones

En Python, los errores no son fatalidades, son objetos. Se llaman `Exceptions`. Cuando ocurre un error (división por cero, archivo no encontrado), Python "lanza" (`raise`) una excepción. Tú puedes "atraparla" (`catch`) y manejarla.

### Estructura Básica

```python
try:
    # Código peligroso (puede fallar)
    resultado = 10 / 0
except ZeroDivisionError:
    # Plan B (qué hacer si falla)
    print("¡No puedes dividir por cero!")
except Exception as e:
    # Plan C (para cualquier otro error inesperado)
    print(f"Ocurrió algo raro: {e}")
else:
    # Se ejecuta SI NO hubo errores
    print("Todo salió bien.")
finally:
    # Se ejecuta SIEMPRE (haya error o no). Útil para cerrar archivos/conexiones.
    print("Operación finalizada.")
```

---

## 2. Lanzar tus propios errores (`raise`)

A veces quieres detener el programa intencionalmente porque los datos no son válidos.

```python
def registrar_edad(edad):
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    if edad < 18:
        raise PermissionError("Debes ser mayor de edad")
    print(f"Edad registrada: {edad}")

try:
    registrar_edad(-5)
except ValueError as e:
    print(f"Error de validación: {e}")
```

---

## 3. Excepciones Personalizadas

Para proyectos profesionales, crea tus propios tipos de error.
*Nota*: Esto usa **Herencia** (Módulo 2).

```python
class SaldoInsuficienteError(Exception):
    """Se lanza cuando intentas retirar más dinero del que tienes."""
    pass

class Banco:
    def retirar(self, cantidad):
        if cantidad > self.saldo:
            raise SaldoInsuficienteError(f"Te faltan {cantidad - self.saldo}")

# Ahora el código que usa tu Banco puede ser muy específico:
try:
    banco.retirar(1000)
except SaldoInsuficienteError:
    mostrar_alerta_roja()
except Exception:
    llamar_al_tecnico()
```

---

## 4. Ejercicios Prácticos

### Ejercicio 1: División Segura
Crea una función `dividir(a, b)` que maneje `ZeroDivisionError` y retorne `None` si hay error.

<details>
<summary>Ver Solución</summary>

```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: División por 0")
        return None
```
</details>

### Ejercicio 2: Conversión de Enteros
Pide al usuario un número (`input`). Intenta convertirlo a `int`. Si falla (`ValueError`), imprime "Eso no es un número".

<details>
<summary>Ver Solución</summary>

```python
texto = input("Dame un número: ")
try:
    num = int(texto)
    print(f"Doble: {num*2}")
except ValueError:
    print("Eso no es un número válido")
```
</details>

### Ejercicio 3: Acceso a Lista Seguro
Función `obtener_elemento(lista, indice)`. Maneja `IndexError` si el índice está fuera de rango.

<details>
<summary>Ver Solución</summary>

```python
def obtener_elemento(lista, indice):
    try:
        return lista[indice]
    except IndexError:
        print("Índice fuera de rango")
        return None
```
</details>

### Ejercicio 4: Diccionario Key Error
Dado `d = {"a": 1}`, intenta acceder a `d["b"]`. Usa `try/except KeyError` para imprimir "Clave no encontrada".

<details>
<summary>Ver Solución</summary>

```python
d = {"a": 1}
try:
    print(d["b"])
except KeyError:
    print("Clave no encontrada")
```
</details>

### Ejercicio 5: Validación de Contraseña (Raise)
Función `validar_pass(p)`. Si longitud < 8, `raise ValueError`. Prueba llamándola dentro de un try/except.

<details>
<summary>Ver Solución</summary>

```python
def validar_pass(p):
    if len(p) < 8:
        raise ValueError("Muy corta")
    return True

try:
    validar_pass("123")
except ValueError as e:
    print(e)
```
</details>

### Ejercicio 6: Excepción Personalizada
Define `ErrorDeJuego(Exception)`. Lánzalo si un jugador intenta moverse fuera del tablero.

<details>
<summary>Ver Solución</summary>

```python
class ErrorDeJuego(Exception): pass

def mover(x, y):
    if x > 100:
        raise ErrorDeJuego("Fuera de límites")

try:
    mover(101, 0)
except ErrorDeJuego as e:
    print(f"Juego detenido: {e}")
```
</details>

### Ejercicio 7: Archivos (FileNotFound)
Intenta abrir un archivo `no_existe.txt`. Captura `FileNotFoundError`.

<details>
<summary>Ver Solución</summary>

```python
try:
    with open("no_existe.txt") as f:
        print(f.read())
except FileNotFoundError:
    print("El archivo no existe, creando uno nuevo...")
```
</details>

### Ejercicio 8: Múltiples Excepciones
Haz una operación que pueda fallar por tipo (`TypeError`) o por valor (`ValueError`). Captura ambas en bloques separados.

<details>
<summary>Ver Solución</summary>

```python
def op(a, b):
    # Imagina una lógica compleja
    return int(a) + int(b)

try:
    op("a", "b")
except ValueError:
    print("No se pueden convertir a números")
except TypeError:
    print("Tipos incompatibles")
```
</details>

### Ejercicio 9: Bloque Finally
Simula una conexión a base de datos. En el `try` conecta, haz algo que falle. En el `finally` imprime "Cerrando conexión" (simulando limpieza).

<details>
<summary>Ver Solución</summary>

```python
try:
    print("Conectando DB...")
    raise Exception("Fallo crítico")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Cerrando conexión DB (Liberando recursos)")
```
</details>

### Ejercicio 10: Re-lanzar Excepción (Reraise)
Captura un error, loguealo (print) y vuelve a lanzarlo (`raise`) para que el programa superior se entere.

<details>
<summary>Ver Solución</summary>

```python
def proceso_interno():
    try:
        1 / 0
    except ZeroDivisionError:
        print("Log interno: Ocurrió error div0")
        raise # Vuelve a lanzar el error hacia arriba

try:
    proceso_interno()
except ZeroDivisionError:
    print("El programa principal se enteró del fallo")
```
</details>
