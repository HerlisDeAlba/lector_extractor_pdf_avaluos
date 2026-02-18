# Módulo 3: Composición - Construyendo Sistemas Complejos

La herencia es un martillo, pero no todo es un clavo. A veces, la mejor forma de reutilizar código no es heredando, sino **teniendo** otros objetos dentro. Esto se llama **Composición**.

## 1. El Concepto: "Tiene un..." (HAS-A)

*   **Herencia**: Un `Perro` **ES UN** `Animal`.
*   **Composición**: Un `Coche` **TIENE UN** `Motor`. Un `Coche` no es un tipo de motor.

Si usas herencia para todo, terminarás con estructuras rígidas imposibles de cambiar. La composición es flexible como piezas de LEGO.

### Comparativa Visual

**Herencia (Rígido)**
```python
class MotorV8:
    def arrancar(self): print("V8 rugiendo!")

class CocheDeportivo(MotorV8): # El coche "es un" motor? Raro.
    pass
```

**Composición (Flexible)**
```python
class Coche:
    def __init__(self, motor):
        self.motor = motor # Tiene un motor
    
    def arrancar(self):
        self.motor.encender()

class MotorElectrico:
    def encender(self): print("Silencio...")

class MotorGasolina:
    def encender(self): print("Ruuun...")

# Puedo cambiar el motor en tiempo de ejecución!
mi_coche = Coche(MotorElectrico())
mi_coche.arrancar()
```

---

## 2. Ejemplos Prácticos

### Nivel 1: Computadora y sus Componentes
Una computadora `TIENE` CPU, RAM y Disco.

```python
class CPU:
    def procesar(self): print("Procesando datos...")

class RAM:
    def cargar(self): print("Cargando en memoria...")

class Computadora:
    def __init__(self):
        self.cpu = CPU() # Composición fuerte: si muere la PC, muere la CPU interna
        self.ram = RAM()
        
    def iniciar(self):
        self.ram.cargar()
        self.cpu.procesar()
```

### Nivel 2: Sistema de Autenticación en Web App
En lugar de que `Usuario` herede de `AutenticacionGoogle`, el usuario *usa* un servicio de autenticación.

```python
class ServicioAuth:
    def loguear(self, user): pass

class AuthGoogle(ServicioAuth):
    def loguear(self, user): print(f"Logueando a {user} con Google")

class AuthFacebook(ServicioAuth):
    def loguear(self, user): print(f"Logueando a {user} con Facebook")

class PaginaLogin:
    def __init__(self, servicio):
        self.servicio = servicio # Inyección de dependencia
        
    def click_login(self, usuario):
        self.servicio.loguear(usuario)

pagina = PaginaLogin(AuthGoogle())
pagina.click_login("pepe")
```

---

## 3. Ejercicios Prácticos

### Ejercicio 1: El Cuerpo Humano
Crea clases `Corazon` y `Cerebro`. Crea clase `Cuerpo` que instancie ambos en su `__init__`.

<details>
<summary>Ver Solución</summary>

```python
class Corazon:
    def latir(self): print("Pum pum")

class Cerebro:
    def pensar(self): print("Pensando...")

class Cuerpo:
    def __init__(self):
        self.corazon = Corazon()
        self.cerebro = Cerebro()
    
    def vivir(self):
        self.corazon.latir()
        self.cerebro.pensar()
```
</details>

### Ejercicio 2: El Equipo de Fútbol
Clase `Jugador` (nombre). Clase `Equipo` que tenga una lista de jugadores. Método `fichar_jugador(jugador)`.

<details>
<summary>Ver Solución</summary>

```python
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre

class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []
        
    def fichar(self, jugador):
        self.jugadores.append(jugador)

e = Equipo("Real Python")
e.fichar(Jugador("Messi"))
```
</details>

### Ejercicio 3: Curso y Estudiantes (Agregación)
Similar al anterior, pero un `Estudiante` puede existir sin el `Curso`. Relación más débil.

<details>
<summary>Ver Solución</summary>

```python
class Estudiante:
    def __init__(self, nombre): self.nombre = nombre

class Curso:
    def __init__(self, titulo):
        self.titulo = titulo
        self.estudiantes = []
        
    def matricular(self, estudiante):
        self.estudiantes.append(estudiante)

# El estudiante existe fuera del curso
juan = Estudiante("Juan")
curso = Curso("Python")
curso.matricular(juan)
```
</details>

### Ejercicio 4: Coche y Ruedas
Clase `Rueda` con `presion`. `Coche` tiene lista de 4 ruedas. Método `inflar_ruedas()` que itere y actúe sobre cada una.

<details>
<summary>Ver Solución</summary>

```python
class Rueda:
    def __init__(self): self.presion = 0
    def inflar(self): self.presion = 32

class Coche:
    def __init__(self):
        self.ruedas = [Rueda() for _ in range(4)]
        
    def preparar_viaje(self):
        for r in self.ruedas:
            r.inflar()
```
</details>

### Ejercicio 5: Factura y Líneas de Detalle
Clase `LineaDetalle` (producto, precio, cantidad). Clase `Factura` contiene varias líneas y calcula `total()`.

<details>
<summary>Ver Solución</summary>

```python
class LineaDetalle:
    def __init__(self, prod, precio, cant):
        self.precio = precio
        self.cant = cant
    def subtotal(self):
        return self.precio * self.cant

class Factura:
    def __init__(self):
        self.lineas = []
    
    def agregar(self, linea):
        self.lineas.append(linea)
        
    def total(self):
        return sum(l.subtotal() for l in self.lineas)
```
</details>

### Ejercicio 6: Ordenador y Sistema Operativo
Crea `SistemaOperativo` con método `arrancar()`. `Ordenador` recibe un SO en su constructor (inyección) y lo usa.

<details>
<summary>Ver Solución</summary>

```python
class Windows:
    def arrancar(self): print("Pantalla azul...")

class Linux:
    def arrancar(self): print("Tux saludando...")

class PC:
    def __init__(self, so):
        self.so = so
    def encender(self):
        self.so.arrancar()

PC(Linux()).encender()
```
</details>

### Ejercicio 7: Biblioteca (Composición de Niveles)
`Biblioteca` tiene `Estanterias`. `Estanteria` tiene `Libros`. Método en biblioteca `buscar_libro(titulo)` que delegue hacia abajo.

<details>
<summary>Ver Solución</summary>

```python
class Libro:
    def __init__(self, titulo): self.titulo = titulo

class Estanteria:
    def __init__(self): self.libros = []
    def buscar(self, titulo):
        for l in self.libros:
            if l.titulo == titulo: return True
        return False

class Biblioteca:
    def __init__(self): self.estanterias = []
    def tiene_libro(self, titulo):
        for e in self.estanterias:
            if e.buscar(titulo): return True
        return False
```
</details>

### Ejercicio 8: Robot con Batería
Clase `Bateria` (`carga`). Clase `Robot` tiene una `Bateria`. `Robot.mover()` consume batería. Si batería vacía, no mueve.

<details>
<summary>Ver Solución</summary>

```python
class Bateria:
    carga = 100
    def gastar(self, cantidad):
        self.carga -= cantidad

class Robot:
    def __init__(self): self.bat = Bateria()
    def mover(self):
        if self.bat.carga > 10:
            self.bat.gastar(10)
            print("Moviendo...")
        else:
            print("Batería baja")
```
</details>

### Ejercicio 9: Menú de Restaurante
`Plato` (nombre, precio). `Menu` tiene lista de platos. `Restaurante` tiene `Menu`. `Restaurante.mostrar_carta()`.

<details>
<summary>Ver Solución</summary>

```python
class Plato:
    def __init__(self, n, p): 
        self.nombre, self.precio = n, p

class Menu:
    def __init__(self): self.platos = []
    def agregar(self, p): self.platos.append(p)

class Restaurante:
    def __init__(self): self.menu = Menu()
    def mostrar_carta(self):
        for p in self.menu.platos:
            print(f"{p.nombre} - ${p.precio}")
```
</details>

### Ejercicio 10: GameManager y SaveSystem (Patrón Estrategia)
`GameManager` necesita guardar partida. Tiene un `SaveSystem`. Puede ser `SaveToDisk` o `SaveToCloud`.

<details>
<summary>Ver Solución</summary>

```python
class SaveToDisk:
    def guardar(self, datos): print("Guardando en C:/...")

class SaveToCloud:
    def guardar(self, datos): print("Subiendo a AWS S3...")

class GameManager:
    def __init__(self, saver):
        self.saver = saver
        self.data = "Player Lvl 99"
        
    def save_game(self):
        self.saver.guardar(self.data)

gm = GameManager(SaveToCloud())
gm.save_game()
```
</details>
