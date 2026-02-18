# Módulo 2: Herencia y Jerarquías en Python

En el módulo anterior aprendiste a crear objetos aislados. Pero el mundo real es una jerarquía. Un "Gato" es un "Animal". Un "Gerente" es un "Empleado". La **Herencia** nos permite modelar esto y evitar repetir código.

## 1. El Concepto: "Es un..." (IS-A)

Si tienes una clase `Vehiculo` con método `arrancar()`, y creas una clase `Moto`, no quieres volver a escribir `arrancar()`. Quieres que `Moto` **herede** eso de `Vehiculo`.

### Anatomía de la Herencia

```python
# Clase Padre (Superclase)
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def comer(self):
        print(f"{self.nombre} está comiendo.")

# Clase Hija (Subclase) -> Hereda de Animal
class Perro(Animal):
    def ladrar(self):
        print("¡Guau!")

# Uso
firulais = Perro("Firulais")
firulais.comer()  # Heredado de Animal!
firulais.ladrar() # Propio de Perro
```

---

## 2. Sobreescritura (Overriding) y `super()`

A veces, el hijo quiere hacer lo mismo que el padre, pero *un poco diferente*. O quiere hacer lo del padre *más* algo extra.

### El Problema de `__init__`
Si la clase hija define su propio `__init__`, sobreescribe el del padre. Para mantener la inicialización del padre, usamos `super()`.

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def trabajar(self):
        return f"{self.nombre} está trabajando."

class Gerente(Empleado):
    def __init__(self, nombre, salario, departamento):
        # Llamamos al constructor del padre para name/salario
        super().__init__(nombre, salario) 
        self.departamento = departamento # Inicializamos lo nuevo

    # Sobreescritura de método
    def trabajar(self):
        # Podemos llamar al comportamiento original también
        base = super().trabajar()
        return f"{base} Supervisando el dpto {self.departamento}."

g = Gerente("Ana", 5000, "Ventas")
print(g.trabajar()) 
# Salida: Ana está trabajando. Supervisando el dpto Ventas.
```

---

## 3. Ejemplos Prácticos de Menor a Mayor Complejidad

### Nivel 1: Figuras Geométricas (Básico)
*Problema*: Cuadrados y Círculos son Figuras.

```python
import math

class Figura:
    def area(self):
        pass # Definido en hijos

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado
    def area(self):
        return self.lado * self.lado

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio
    def area(self):
        return math.pi * (self.radio ** 2)
```

### Nivel 2: Sistema de Notificaciones (Intermedio)
*Problema*: Enviar mensajes por Email, SMS o Push, todos tienen un método `enviar`.

```python
class Notificacion:
    def enviar(self, mensaje):
        print(f"Enviando genérico: {mensaje}")

class Email(Notificacion):
    def enviar(self, mensaje):
        print(f"Conectando a SMTP... Email enviado: {mensaje}")

class SMS(Notificacion):
    def enviar(self, mensaje):
        print(f"Enviando SMS por Twilio: {mensaje}")

def alertar_usuarios(notificadores, msg):
    for n in notificadores:
        n.enviar(msg) # Polimorfismo: funciona igual para todos

lista = [Email(), SMS(), Email()]
alertar_usuarios(lista, "Hola Mundo")
```

### Nivel 3: RPG Character System (Avanzado)
*Problema*: Guerreros y Magos comparten vida/nombre, pero atacan diferente. El Mago usa maná.

```python
class Personaje:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self.hp = hp
        self.vivo = True

    def recibir_dano(self, puntos):
        self.hp -= puntos
        if self.hp <= 0:
            self.vivo = False
            print(f"{self.nombre} ha muerto.")

class Guerrero(Personaje):
    def __init__(self, nombre, hp, fuerza):
        super().__init__(nombre, hp)
        self.fuerza = fuerza

    def atacar(self, otro):
        print(f"{self.nombre} ataca con espada!")
        otro.recibir_dano(self.fuerza)

class Mago(Personaje):
    def __init__(self, nombre, hp, mana):
        super().__init__(nombre, hp)
        self.mana = mana

    def lanzar_hechizo(self, otro):
        if self.mana >= 10:
            self.mana -= 10
            print(f"{self.nombre} lanza bola de fuego!")
            otro.recibir_dano(25)
        else:
            print("No hay maná suficiente.")
```

---

## 4. Ejercicios Prácticos

### Ejercicio 1: Instrumentos Musicales
Clase base `Instrumento` con método `tocar()`. Subclases `Guitarra` ("rasgueando cuerdas") y `Tambor` ("golpeando parche").

<details>
<summary>Ver Solución</summary>

```python
class Instrumento:
    def tocar(self):
        print("Sonido genérico")

class Guitarra(Instrumento):
    def tocar(self):
        print("Rasgueando cuerdas...")

class Tambor(Instrumento):
    def tocar(self):
        print("Golpeando parche...")
```
</details>

### Ejercicio 2: Superhéroes
Clase `Persona` (nombre). Clase `Superheroe` hereda de `Persona` y añade `poder`. Método `usar_poder()`.

<details>
<summary>Ver Solución</summary>

```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Superheroe(Persona):
    def __init__(self, nombre, poder):
        super().__init__(nombre)
        self.poder = poder
        
    def usar_poder(self):
        print(f"{self.nombre} usa {self.poder}!")

s = Superheroe("Clark", "Vuelo")
s.usar_poder()
```
</details>

### Ejercicio 3: Vehículos y Ruedas
Clase `Vehiculo` (marca). Subclases `Coche` (4 ruedas) y `Moto` (2 ruedas). Sobreescribe un método `info_ruedas()`.

<details>
<summary>Ver Solución</summary>

```python
class Vehiculo:
    def __init__(self, marca):
        self.marca = marca
    
    def info_ruedas(self):
        return "Desconocido"

class Coche(Vehiculo):
    def info_ruedas(self):
        return 4

class Moto(Vehiculo):
    def info_ruedas(self):
        return 2
```
</details>

### Ejercicio 4: Cuentas Bancarias Especializadas
Clase `Cuenta` (saldo). Subclase `CuentaAhorro` con interés del 5% al depositar (Sobreescribe `depositar`).

<details>
<summary>Ver Solución</summary>

```python
class Cuenta:
    def __init__(self):
        self.saldo = 0
    
    def depositar(self, cantidad):
        self.saldo += cantidad

class CuentaAhorro(Cuenta):
    def depositar(self, cantidad):
        cantidad_con_interes = cantidad * 1.05
        super().depositar(cantidad_con_interes)
```
</details>

### Ejercicio 5: Animales que hablan
Lista de diferentes animales. Bucle for que llame a `hacer_sonido()` en todos. (Polimorfismo).

<details>
<summary>Ver Solución</summary>

```python
class Perro:
    def hacer_sonido(self): print("Guau")
class Gato:
    def hacer_sonido(self): print("Miau")
class Vaca:
    def hacer_sonido(self): print("Muu")

zoo = [Perro(), Gato(), Vaca()]
for animal in zoo:
    animal.hacer_sonido()
```
</details>

### Ejercicio 6: Empleados y Bonos
`Empleado` base gana `salario`. `Gerente` gana `salario + bono`. Implementa `calcular_pago()`. Usa `super()`.

<details>
<summary>Ver Solución</summary>

```python
class Empleado:
    def __init__(self, salario):
        self.salario = salario
    def calcular_pago(self):
        return self.salario

class Gerente(Empleado):
    def __init__(self, salario, bono):
        super().__init__(salario)
        self.bono = bono
    def calcular_pago(self):
        return super().calcular_pago() + self.bono
```
</details>

### Ejercicio 7: Dispositivos Electrónicos
Clase `Dispositivo` (`encendido = False`). Método `toggle()`. Subclase `Telefono` añade `llamar()`, pero solo si está encendido.

<details>
<summary>Ver Solución</summary>

```python
class Dispositivo:
    def __init__(self):
        self.encendido = False
    def toggle(self):
        self.encendido = not self.encendido

class Telefono(Dispositivo):
    def llamar(self, numero):
        if self.encendido:
            print(f"Llamando a {numero}...")
        else:
            print("Enciéndelo primero.")
```
</details>

### Ejercicio 8: Formas de Pago
Clase `Pago`. Subclases `PagoTarjeta` y `PagoEfectivo`. `PagoTarjeta` recibe `numero` en `__init__`. Ambos tienen `procesar()`.

<details>
<summary>Ver Solución</summary>

```python
class Pago:
    def procesar(self): pass

class PagoEfectivo(Pago):
    def procesar(self):
        print("Recibiendo billetes...")

class PagoTarjeta(Pago):
    def __init__(self, numero):
        self.numero = numero
    def procesar(self):
        print(f"Procesando tarjeta terminada en {self.numero[-4:]}")
```
</details>

### Ejercicio 9: Herencia Multinivel (Abuelo -> Padre -> Hijo)
Clase `A` -> `B` -> `C`. Crea métodos que impriman quién soy. Llama al método de `A` desde `C`.

<details>
<summary>Ver Solución</summary>

```python
class A:
    def quien_soy(self): print("Soy A")

class B(A):
    def quien_soy(self): 
        super().quien_soy()
        print("Soy B")

class C(B):
    def quien_soy(self):
        super().quien_soy()
        print("Soy C")

obj = C()
obj.quien_soy() # Imprime A, luego B, luego C
```
</details>

### Ejercicio 10: Sistema de Archivos
Clase `ElementoFS` (nombre). Subclases `Archivo` (`contenido`) y `Directorio` (`lista_de_elementos`). `Directorio` debe tener método `agregar(elemento)`.
*Nota*: Este ejercicio toca el patrón **Composite**, muy usado en estructuras de árbol.

<details>
<summary>Ver Solución</summary>

```python
class ElementoFS:
    def __init__(self, nombre):
        self.nombre = nombre

class Archivo(ElementoFS):
    def __init__(self, nombre, contenido):
        super().__init__(nombre)
        self.contenido = contenido

class Directorio(ElementoFS):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.elementos = []
        
    def agregar(self, elemento):
        self.elementos.append(elemento)
        print(f"Agregado {elemento.nombre} a {self.nombre}")

root = Directorio("root")
f1 = Archivo("foto.jpg", "bytes")
root.agregar(f1)
```
</details>
