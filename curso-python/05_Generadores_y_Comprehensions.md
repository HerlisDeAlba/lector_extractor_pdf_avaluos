# Módulo 5: Eficiencia de Datos - Iteradores y Generadores

Aquí es donde Python brilla. Pasaremos de bucles `for` estilo C/Java a bucles "Pythonicos" elegantes y eficientes en memoria.

## 1. List Comprehensions (Comprensión de Listas)

Es una forma de crear listas en una sola línea. Es más rápido y legible que usar `.append()` en un bucle.

**Estilo Viejo:**
```python
cuadrados = []
for i in range(10):
    if i % 2 == 0:
        cuadrados.append(i * i)
```

**Estilo Pythonico:**
```python
# [expresion FOR elemento IN iterable IF condicion]
cuadrados = [i * i for i in range(10) if i % 2 == 0]
```

También existe para diccionarios y conjuntos:
```python
nombres = ["juan", "ana", "pedro"]
# Dict comprehension
mapa = {nombre: len(nombre) for nombre in nombres}
# {'juan': 4, 'ana': 3, ...}
```

---

## 2. Generadores (`yield`)

¿Qué pasa si tienes que procesar 1 millón de registros?
*   Con lista: Python carga el millón en RAM. Tu PC explota.
*   Con **Generador**: Python carga 1 registro, lo procesa, lo olvida. RAM feliz.

### La sentencia `yield`

Cuando una función usa `yield` en vez de `return`, se convierte en un generador. No devuelve un valor, devuelve una "fábrica de valores". Pausa su ejecución y la reanuda cuando le pides el siguiente dato.

```python
def contador_infinito():
    n = 0
    while True:
        yield n
        n += 1

gen = contador_infinito()
print(next(gen)) # 0
print(next(gen)) # 1
# No infinite loop crash, porque solo corre hasta el yield!
```

---

## 3. Función `zip` y `enumerate`

Herramientas esenciales para iterar.

*   `enumerate(lista)`: Te da el índice y el valor a la vez.
*   `zip(lista1, lista2)`: Une dos listas par a par.

```python
nombres = ["Ana", "Bob"]
edades = [25, 30]

for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad}")
```

---

## 4. Ejercicios Prácticos

### Ejercicio 1: Cuadrados Simples
Usa List Comprehension para generar una lista con los cuadrados de los números del 1 al 10.

<details>
<summary>Ver Solución</summary>

```python
res = [x**2 for x in range(1, 11)]
print(res)
```
</details>

### Ejercicio 2: Filtrar Pares
Dada una lista `[1, 2, 3, 4, 5, 6]`, usa LC para obtener solo los pares.

<details>
<summary>Ver Solución</summary>

```python
nums = [1, 2, 3, 4, 5, 6]
pares = [x for x in nums if x % 2 == 0]
```
</details>

### Ejercicio 3: Palabras Cortas
Dada una lista de palabras, crea una nueva lista solo con las que tengan menos de 5 letras.

<details>
<summary>Ver Solución</summary>

```python
words = ["hola", "esternocleidomastoideo", "sol", "python"]
short = [w for w in words if len(w) < 5]
```
</details>

### Ejercicio 4: Generador de Fibonacci
Crea una función generadora `fib(n)` que use `yield` para producir los primeros n números de Fibonacci.

<details>
<summary>Ver Solución</summary>

```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fib(5))) # [0, 1, 1, 2, 3]
```
</details>

### Ejercicio 5: Diccionario de Cuadrados
Usa Dict Comprehension para crear `{1: 1, 2: 4, 3: 9...}` hasta 5.

<details>
<summary>Ver Solución</summary>

```python
d = {x: x**2 for x in range(1, 6)}
```
</details>

### Ejercicio 6: Aplanar Lista (Flatten)
Dada `[[1,2], [3,4], [5,6]]`, usa LC doble para obtener `[1,2,3,4,5,6]`. (Avanzado).

<details>
<summary>Ver Solución</summary>

```python
matriz = [[1,2], [3,4], [5,6]]
plana = [num for fila in matriz for num in fila]
```
</details>

### Ejercicio 7: Enumerate Manual
Usa `enumerate` en un for loop para imprimir "Índice: X, Valor: Y" de una lista de frutas.

<details>
<summary>Ver Solución</summary>

```python
frutas = ["Manzana", "Pera"]
for i, fruta in enumerate(frutas):
    print(f"Índice: {i}, Valor: {fruta}")
```
</details>

### Ejercicio 8: Zip de Notas
Dada lista `alumnos` y lista `notas`, crea un diccionario que los una usando `zip` y `dict()`.

<details>
<summary>Ver Solución</summary>

```python
alumnos = ["Ana", "Luis"]
notas = [10, 8]
boletin = dict(zip(alumnos, notas))
```
</details>

### Ejercicio 9: Generador de Archivos Grandes (Simulado)
Crea generador `leer_logs()` que `yield` líneas simuladas ("Log 1", "Log 2"...) hasta un limite dado. Itera sobre él.

<details>
<summary>Ver Solución</summary>

```python
def leer_logs(total):
    for i in range(total):
        yield f"Log entry {i}"

for log in leer_logs(3):
    print(log)
```
</details>

### Ejercicio 10: Invertir Diccionario
Dado `{'a': 1, 'b': 2}`, usa Dict Comprehension para obtener `{1: 'a', 2: 'b'}`.

<details>
<summary>Ver Solución</summary>

```python
orig = {'a': 1, 'b': 2}
dest = {v: k for k, v in orig.items()}
```
</details>
