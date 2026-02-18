# Módulo 6: Decoradores - Magia con Funciones

Los decoradores son una de las características más potentes y confusas de Python. Te permiten modificar funciones sin tocar su código.

## 1. El Concepto: Funciones de Orden Superior

En Python, las funciones son objetos. Puedes pasar una función como argumento a otra.

**Un decorador es una función que envuelve a otra función para añadirle "superpoderes".**

### Anatomía de un Decorador

```python
def mi_decorador(funcion_original):
    def funcion_envoltura():
        print("Antes de llamar a la función...")
        funcion_original()
        print("Después de llamar a la función.")
    return funcion_envoltura

@mi_decorador
def saludar():
    print("Hola Mundo")

# Al llamar saludar(), en realidad llamas a funcion_envoltura()
saludar()
# Salida:
# Antes...
# Hola Mundo
# Después...
```

---

## 2. Aplicaciones Reales

### Timing (Medir tiempo)
¿Quieres saber cuánto tarda cada función de tu proyecto? No pongas `time.start` y `time.end` en todas partes. Usa un decorador.

### Autenticación
En servidores web (Flask/Django), usas decoradores para proteger rutas.
`@login_required` chequea si el usuario es admin antes de dejarle entrar a la función `ver_panel_admin()`.

### Logging
Registrar automáticamente cada vez que una función es llamada y con qué argumentos.

---

## 3. Decoradores con Argumentos (`*args`, `**kwargs`)

Para que el decorador sirva para CUALQUIER función (con 0, 1 o 100 parámetros), usamos `*args` y `**kwargs`.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__} con {args}")
        return func(*args, **kwargs)
    return wrapper

@logger
def suma(a, b):
    return a + b

suma(5, 3) # Output: Llamando a suma con (5, 3)
```

---

## 4. Ejercicios Prácticos

### Ejercicio 1: Decorador Básico
Crea `@aviso` que imprima "Cuidado!" antes de ejecutar la función.

<details>
<summary>Ver Solución</summary>

```python
def aviso(f):
    def wrapper():
        print("Cuidado!")
        f()
    return wrapper

@aviso
def boom(): print("Boom!")
boom()
```
</details>

### Ejercicio 2: Decorador que repite
Crea `@dos_veces` que ejecute la función decorada dos veces seguidas.

<details>
<summary>Ver Solución</summary>

```python
def dos_veces(f):
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        f(*args, **kwargs)
    return wrapper

@dos_veces
def saludo(): print("Hola")
saludo()
```
</details>

### Ejercicio 3: Timer simple
Crea `@timer` que mida e imprima cuánto tarda en ejecutarse la función. (Usa `time.time()`).

<details>
<summary>Ver Solución</summary>

```python
import time
def timer(f):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = f(*args, **kwargs)
        print(f"Tiempo: {time.time() - t0}")
        return res
    return wrapper
```
</details>

### Ejercicio 4: Mayúsculas
Crea un decorador `@mayus` para una función que devuelve texto. El decorador debe convertir el resultado a MAYÚSCULAS.

<details>
<summary>Ver Solución</summary>

```python
def mayus(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        return res.upper()
    return wrapper

@mayus
def get_nombre(): return "juan"
print(get_nombre()) # JUAN
```
</details>

### Ejercicio 5: Contador de Llamadas
Crea un decorador que cuente cuántas veces se ha llamado a una función (puedes añadir un atributo a la función wrapper).

<details>
<summary>Ver Solución</summary>

```python
def contador(f):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"Llamada #{wrapper.calls}")
        return f(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@contador
def test(): pass
test(); test()
```
</details>

### Ejercicio 6: Validación de Argumentos
Crea `@solo_enteros`. Si algún argumento de la función no es int, cancela y print error.

<details>
<summary>Ver Solución</summary>

```python
def solo_enteros(f):
    def wrapper(*args):
        for a in args:
            if not isinstance(a, int):
                print("Error: Solo enteros")
                return None
        return f(*args)
    return wrapper

@solo_enteros
def sumar(a, b): return a+b
sumar(1, "2")
```
</details>

### Ejercicio 7: Autenticación Simulada
Variable global `USUARIO_LOGUEADO = False`. Decorador `@login_required` que solo ejecute la función si esa variable es True.

<details>
<summary>Ver Solución</summary>

```python
USUARIO = False
def login_required(f):
    def wrapper(*args):
        if not USUARIO:
            print("Acceso denegado")
        else:
            f(*args)
    return wrapper
```
</details>

### Ejercicio 8: Retraso (Slow Down)
Decorador `@slow` que duerma 1 segundo antes de ejecutar (`time.sleep(1)`).

<details>
<summary>Ver Solución</summary>

```python
import time
def slow(f):
    def wrapper(*args):
        time.sleep(1)
        f(*args)
    return wrapper
```
</details>

### Ejercicio 9: Decorador de Clase (Avanzado)
Sabías que las clases también pueden ser decoradores si implementan `__call__`? Intenta implementar el contador (Ej 5) como clase.

<details>
<summary>Ver Solución</summary>

```python
class CountCalls:
    def __init__(self, f):
        self.f = f
        self.count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Llamada {self.count}")
        return self.f(*args, **kwargs)

@CountCalls
def foo(): pass
foo()
```
</details>

### Ejercicio 10: Caché Simple (Memoization)
Decorador `@cache` que guarde los resultados de una función (en un dict) para no volver a calcularlos si se llaman con los mismos argumentos.

<details>
<summary>Ver Solución</summary>

```python
def cache(f):
    memo = {}
    def wrapper(n):
        if n not in memo:
            memo[n] = f(n)
        return memo[n]
    return wrapper

@cache
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```
</details>
