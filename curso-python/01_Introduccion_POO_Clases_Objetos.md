# Módulo 1: Fundamentos de Clases y Objetos en Python

Bienvenido al primer módulo de tu curso maestro de Python. Aquí es donde transformamos tu forma de pensar: de escribir scripts lineales a pensar en sistemas de objetos interactivos.

## 1. El Concepto: ¿Por qué Objetos?

Imagina que eres un dios creador de mundos.
Si programas con funciones (programación procedural), tienes que crear una lista de todas las personas, otra lista de sus edades, otra de sus trabajos, y funciones separadas para que interactúen. Es caótico.
Con **Programación Orientada a Objetos (POO)**, creas "Personas". Cada "Persona" sabe su nombre, su edad y cómo trabajar.

### Analogía Clave: El Constructor de Casas
*   **La Clase (`class`)**: Es el plano arquitectónico. Define dónde van las paredes y las ventanas. No puedes vivir en el plano.
*   **El Objeto (Instancia)**: Es la casa física construida en la Calle Falsa 123. Puedes vivir ahí. Puedes construir 100 casas diferentes usando el mismo plano.
*   **Atributos**: Son las características. El color de la pintura, el número de puertas.
*   **Métodos**: Son las acciones que la casa "permite". `abrir_puerta()`, `encender_luces()`.

---

## 2. Construyendo una Clase Paso a Paso (¡Hazlo conmigo!)

Vamos a construir nuestra clase `Coche`. Abre tu editor de código o terminal. No leas esto pasivamente: escribe el código a medida que avanzamos.

### Paso 1: Definir el "Plano"
Escribe esto en tu archivo. Le estamos diciendo a Python que vamos a crear un nuevo tipo de objeto llamado `Coche`.

```python
class Coche:
    pass
```
*   `pass` es solo para que Python no nos dé error por dejarlo vacío. Bórralo cuando pasemos al siguiente paso.

### Paso 2: El Nacimiento del Objeto (`__init__`)
Toda clase necesita un método especial para "nacer". Cuando fabricas un coche, este *necesita* tener una marca y un color desde el primer segundo de su existencia.

Añade este método dentro de tu clase (respeta la indentación):

```python
class Coche:
    def __init__(self, marca, color):
        self.marca = marca
        self.color = color
```
**Analicemos qué acabas de escribir:**
1.  `def __init__`: Es la función mágica de inicialización.
2.  `self`: Es la referencia al propio coche que se está creando.
3.  `self.marca = marca`: Significa "Guarda el valor `marca` que recibí, dentro de `mí mismo` (self)".

### Paso 3: Añadiendo Memoria Interna
Ahora, queremos que el coche recuerde cuántos kilómetros ha recorrido. Pero esto NO se lo pasamos al crearlo (un coche nuevo siempre tiene 0 km).

Añade esta línea dentro del `__init__`:

```python
class Coche:
    def __init__(self, marca, color):
        self.marca = marca
        self.color = color
        self._kilometros = 0  # <--- AÑADE ESTO
```
*   Iniciamos la variable en `0`.
*   El guion bajo `_` al principio es una señal para otros programadores: "Oye, no toques esto directamente desde fuera, es para uso interno del coche".

### Paso 4: Enseñándole a Conducir (Métodos)
Un coche estático es aburrido. Vamos a enseñarle una acción: `conducir`.
Fuera del `__init__`, pero dentro de la clase, escribe este nuevo método:

```python
    def conducir(self, distancia):
        self._kilometros += distancia
        return f"Conduciendo el {self.marca} por {distancia}km"
```
*   `self`: De nuevo, necesitamos `self` para saber *qué* coche está conduciendo y acceder a *sus* kilómetros.
*   `+=`: Sumamos la distancia a nuestro contador interno.

### Paso 5: ¡Probarlo!
Sal de la clase (borra la indentación) y añade este código para crear tu primer objeto real:

```python
# Crear una instancia (Objeto)
mi_ferrari = Coche("Ferrari", "Rojo")

# Usar el objeto
print(mi_ferrari.conducir(100))
# Salida esperada: Conduciendo el Ferrari por 100km
```

---

## 3. Ejemplos Prácticos Interactivos

Vamos a resolver 3 problemas reales, construyendo la solución pieza por pieza.

### Nivel 1: El Inventario de Videojuego (Básico)
**El Problema**: Necesitamos ítems (Espada, Poción) que tengan un nombre y un valor en oro.

**Paso 1**: Empieza creando la clase vacía.
```python
class Item:
    pass
```

**Paso 2**: Ahora piensa, ¿qué datos necesita un ítem para existir? Nombre y valor. Añade el constructor para recibir esos datos.
```python
class Item:
    def __init__(self, nombre, valor):
        # ... ¿Qué va aquí? ...
```

**Paso 3**: Asigna los valores a variables del objeto (`self`).
```python
class Item:
    def __init__(self, nombre, valor):
        self.nombre = nombre  # Guardamos el nombre
        self.valor = valor    # Guardamos el valor
```

**Paso 4**: Pruébalo creando una espada.
```python
espada = Item("Espada de Madera", 10)
print(f"Objeto: {espada.nombre}, Valor: {espada.valor}")
```

### Nivel 2: Sistema de Usuarios y Contraseñas (Intermedio)
**El Problema**: Queremos guardar usuarios, pero guardar la contraseña tal cual es inseguro.

**Paso 1**: Estructura básica.
```python
class Usuario:
    def __init__(self, username, password):
        self.username = username
        # ¡ALTO! No hagas self.password = password. Eso es inseguro.
```

**Paso 2**: Vamos a crear un método ayudante *antes* de terminar el constructor. Este método recibirá un texto y lo devolverá "encriptado" (al revés, por simplicidad).
```python
    def _encriptar(self, texto):
        return texto[::-1]
```

**Paso 3**: Ahora sí, volvamos al `__init__`. Usa ese método para guardar la contraseña de forma segura. Fíjate que usamos dos guiones bajos `__` para hacerla muy privada.
```python
    def __init__(self, username, password):
        self.username = username
        self.__password_secreta = self._encriptar(password) # <--- Usamos el método aquí
```

**Paso 4**: Necesitamos una forma de verificar la contraseña, ya que la variable `__password_secreta` está oculta. Añade el método `validar_acceso`.
```python
    def validar_acceso(self, password_input):
        # 1. Encriptamos lo que el usuario acaba de escribir
        input_encriptado = self._encriptar(password_input)
        
        # 2. Comparamos con lo que tenemos guardado
        return input_encriptado == self.__password_secreta
```

**Resultado Final**:
```python
u = Usuario("Herlis", "1234")
print(u.validar_acceso("1234")) # True
print(u.validar_acceso("0000")) # False
```

### Nivel 3: Gestor de Base de Datos (Avanzado)
**El Problema**: Queremos definir a qué base de datos conectarnos, pero NO conectarnos inmediatamente.

**Paso 1**: El constructor. Solo guardamos la configuración (host).
```python
class DatabaseConnection:
    def __init__(self, host):
        self.host = host
        # Todavía no estamos conectados, así que necesitamos una "bandera"
        self.conectado = False 
```

**Paso 2**: Crea el método `conectar`. Este debe cambiar esa bandera a True.
```python
    def conectar(self):
        if not self.conectado:
            print(f"🔌 Conectando a {self.host}...")
            self.conectado = True
        else:
            print("⚠️ Ya estabas conectado.")
```

**Paso 3**: Ahora el método `ejecutar_query(sql)`. Pero espera, ¿qué pasa si intentamos ejecutar sin estar conectados?
Añade una validación al principio del método.
```python
    def ejecutar_query(self, sql):
        # Validación de seguridad
        if not self.conectado:
            raise Exception("❌ Error: Debes conectarte primero.")
            
        return f"✅ Ejecutando '{sql}' en {self.host}"
```

**Paso 4**: Prueba el flujo completo. Intenta romperlo llamando a query sin conectar primero.
```python
db = DatabaseConnection("localhost")
# db.ejecutar_query("SELECT *") # ¡Boom! Error.
db.conectar()
print(db.ejecutar_query("SELECT *")) # ¡Éxito!
```

---

## 4. Ejercicios Prácticos

A continuación tienes 10 ejercicios para afianzar estos conceptos. 
**Instrucción**: Intenta escribir la solución tú mismo antes de abrir la respuesta. Copiar y pegar no te enseñará nada.

### Ejercicio 1: La Clase Libro
Crea una clase `Libro` que tenga `titulo`, `autor` y `paginas`. Añade un método `mostrar_info` que imprima "El libro [titulo] de [autor] tiene [paginas] páginas".

<details>
<summary>Ver Solución</summary>

```python
class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def mostrar_info(self):
        print(f"El libro {self.titulo} de {self.autor} tiene {self.paginas} páginas")

# Prueba
l = Libro("1984", "George Orwell", 300)
l.mostrar_info()
```
</details>

### Ejercicio 2: El Rectángulo
Crea una clase `Rectangulo` que reciba `base` y `altura`. Añade métodos para calcular el `area` y el `perimetro`.

<details>
<summary>Ver Solución</summary>

```python
class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)

r = Rectangulo(5, 3)
print(r.area()) # 15
print(r.perimetro()) # 16
```
</details>

### Ejercicio 3: Calculadora Simple
Crea una clase `Calculadora` que no reciba nada en el `__init__`. Debe tener métodos `sumar(a, b)`, `restar(a, b)`, etc.
*Pista*: Si no necesitas guardar datos, el `__init__` puede estar vacío o no existir.

<details>
<summary>Ver Solución</summary>

```python
class Calculadora:
    def sumar(self, a, b):
        return a + b
        
    def restar(self, a, b):
        return a - b

c = Calculadora()
print(c.sumar(5, 3))
```
</details>

### Ejercicio 4: Contador
Crea una clase `Contador` con un atributo interno que empiece en 0. Métodos: `incrementar()`, `decrementar()`, y `obtener_valor()`.

<details>
<summary>Ver Solución</summary>

```python
class Contador:
    def __init__(self):
        self.valor = 0
        
    def incrementar(self):
        self.valor += 1
        
    def decrementar(self):
        self.valor -= 1
        
    def obtener_valor(self):
        return self.valor

c = Contador()
c.incrementar()
print(c.obtener_valor()) # 1
```
</details>

### Ejercicio 5: El Estudiante
Clase `Estudiante` con `nombre` y `nota`. Método `ha_aprobado()` que devuelve `True` si la nota es >= 3.0.

<details>
<summary>Ver Solución</summary>

```python
class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota
        
    def ha_aprobado(self):
        return self.nota >= 3.0

e = Estudiante("Juan", 2.5)
print(e.ha_aprobado()) # False
```
</details>

### Ejercicio 6: Cafetera (Estado)
Clase `Cafetera` con capacidad máxima (ej. 1000ml) y cantidad actual (empieza en 0). Métodos: `llenar()`, `servir_taza(cantidad)` (que reste y avise si no hay suficiente).

<details>
<summary>Ver Solución</summary>

```python
class Cafetera:
    def __init__(self, capacidad_max):
        self.capacidad_max = capacidad_max
        self.cantidad_actual = 0
        
    def llenar(self):
        self.cantidad_actual = self.capacidad_max
        print("Cafetera llena.")
        
    def servir_taza(self, cantidad):
        if self.cantidad_actual >= cantidad:
            self.cantidad_actual -= cantidad
            print(f"Sirviendo {cantidad}ml. Quedan {self.cantidad_actual}ml.")
            return True
        else:
            print("No hay suficiente café.")
            return False

cafetera = Cafetera(1000)
cafetera.llenar()
cafetera.servir_taza(200)
```
</details>

### Ejercicio 7: Lista de Tareas (Gestión de Listas)
Clase `TaskManager`. Atributo lista vacía. Métodos `add_task(task)`, `show_tasks()`.

<details>
<summary>Ver Solución</summary>

```python
class TaskManager:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, task):
        self.tasks.append(task)
        
    def show_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i+1}. {task}")

tm = TaskManager()
tm.add_task("Aprender Python")
tm.show_tasks()
```
</details>

### Ejercicio 8: Conversor de Moneda (Atributos de Clase)
Clase `Conversor`. Define `tasa_dolar = 4000` fuera del `__init__` (atributo de clase). Método `dolares_a_pesos(dolares)`.
*Reto*: Intenta cambiar `tasa_dolar` para todos los conversores a la vez.

<details>
<summary>Ver Solución</summary>

```python
class Conversor:
    tasa_dolar = 4000 # Atributo de clase compartido
    
    def dolares_a_pesos(self, dolares):
        return dolares * self.tasa_dolar

# Uso
c1 = Conversor()
c2 = Conversor()
print(c1.dolares_a_pesos(10)) # 40000

# Cambiamos la tasa globalmente
Conversor.tasa_dolar = 5000 
print(c2.dolares_a_pesos(10)) # 50000 (afecta a c2 también)
```
</details>

### Ejercicio 9: Punto en el Plano 2D (Matemáticas básicas)
Clase `Punto` con `x`, `y`. Método `distancia_al_origen()` usando Pitágoras (`sqrt(x^2 + y^2)`).

<details>
<summary>Ver Solución</summary>

```python
import math

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distancia_al_origen(self):
        return math.sqrt(self.x**2 + self.y**2)

p = Punto(3, 4)
print(p.distancia_al_origen()) # 5.0
```
</details>

### Ejercicio 10: Sistema de Login Robusto (Lógica compleja)
Clase `Autenticador`. Diccionario interno de `usuarios: contraseña`.
Métodos: `registrar(user, pass)`, `login(user, pass)`. Validar si el usuario ya existe al registrar.

<details>
<summary>Ver Solución</summary>

```python
class Autenticador:
    def __init__(self):
        self.db = {} # Diccionario usuario: password
        
    def registrar(self, user, password):
        if user in self.db:
            print("Error: Usuario ya existe")
            return False
        self.db[user] = password
        print("Usuario registrado")
        return True
        
    def login(self, user, password):
        if user not in self.db:
            print("Usuario no encontrado")
            return False
        if self.db[user] == password:
            print("Login exitoso!")
            return True
        else:
            print("Contraseña incorrecta")
            return False

auth = Autenticador()
auth.registrar("admin", "1234")
auth.login("admin", "1234")
```
</details>
