# Análisis de Violaciones del Principio LSP (Liskov Substitution Principle)

**Proyecto:** ISSE_Termostato
**Fecha:** Noviembre 2025
**Análisis realizado por:** Claude Code

---

## Definición del Principio LSP

> "Los objetos de una clase derivada deben poder reemplazar objetos de la clase base sin alterar el comportamiento correcto del programa."
> — Barbara Liskov

**En otras palabras:** Las subclases deben comportarse de manera que no rompan las expectativas establecidas por la clase base. Si una clase B es subtipo de A, entonces los objetos de tipo A pueden ser reemplazados por objetos de tipo B sin alterar las propiedades deseables del programa.

**Señales de violación del LSP:**
1. Subclases que cambian la signature de métodos (de `@staticmethod` a método de instancia)
2. Subclases que lanzan excepciones que la clase base no lanza
3. Subclases que fortalecen precondiciones o debilitan postcondiciones
4. Subclases con comportamiento fundamentalmente diferente al esperado
5. Métodos que retornan `None` cuando el tipo de retorno promete un objeto específico

---

## 🔴 VIOLACIONES CRÍTICAS

### 1. **VisualizadorBateria - Cambio de Signature de Métodos**

**Archivos afectados:**
- `entidades/abs_visualizador_bateria.py:8-18`
- `agentes_actuadores/visualizador_bateria.py:11-71`

#### Clase Base: `AbsVisualizadorBateria`

```python
class AbsVisualizadorBateria(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def mostrar_tension(tension_bateria):
        pass

    @staticmethod
    @abstractmethod
    def mostrar_indicador(indicador_bateria):
        pass
```

**Contrato:** Métodos estáticos que no requieren instancia.

#### Implementación 1: `VisualizadorBateria` ✅

```python
class VisualizadorBateria(AbsVisualizadorBateria):

    @staticmethod
    def mostrar_tension(tension_bateria):
        print(str(tension_bateria))
        return

    @staticmethod
    def mostrar_indicador(indicador_bateria):
        print(str(indicador_bateria))
        return
```

**Cumple LSP:** Mantiene la signature correctamente.

#### Implementación 2: `VisualizadorBateriaSocket` ❌ (líneas 24-48)

```python
class VisualizadorBateriaSocket(AbsVisualizadorBateria):

    def mostrar_tension(self, tension_bateria):  # ❌ Ya NO es @staticmethod
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14000)
            cliente.connect(direccion_servidor)
            # ...
        except ConnectionError:
            print("Intentar de vuelta")

    def mostrar_indicador(self, indicador_bateria):  # ❌ Ya NO es @staticmethod
        # ...
```

#### Implementación 3: `VisualizadorBateriaApi` ❌ (líneas 51-71)

```python
class VisualizadorBateriaApi(AbsVisualizadorBateria):

    def mostrar_tension(self, tension_bateria):  # ❌ Ya NO es @staticmethod
        # ...

    def mostrar_indicador(self, indicador_bateria):  # ❌ Ya NO es @staticmethod
        # ...
```

**Problema:**
- La clase base define métodos `@staticmethod` (sin `self`)
- Las subclases `VisualizadorBateriaSocket` y `VisualizadorBateriaApi` usan métodos de instancia (con `self`)
- **No son intercambiables**: El código que llama `AbsVisualizadorBateria.mostrar_tension(valor)` funcionará con `VisualizadorBateria` pero fallará con las versiones Socket/Api

**Impacto:**
- Viola el contrato de la clase base
- El código cliente no puede usar polimorfismo correctamente
- Requiere conocer la implementación concreta para invocar correctamente

**Ejemplo de Fallo:**

```python
# Si el configurador retorna VisualizadorBateriaSocket:
visualizador = FactoryVisualizadorBateria.crear("socket")

# Este código funcionaría con VisualizadorBateria:
visualizador.mostrar_tension(12.5)  # ✅ OK con VisualizadorBateria

# Pero con VisualizadorBateriaSocket:
visualizador.mostrar_tension(12.5)
# TypeError: mostrar_tension() missing 1 required positional argument: 'tension_bateria'
# ❌ self se asigna a 12.5, y falta tension_bateria!
```

**Recomendación:** Hacer todos los métodos de instancia o todos estáticos consistentemente.

```python
# Solución: Cambiar clase base a métodos de instancia
class AbsVisualizadorBateria(metaclass=ABCMeta):

    @abstractmethod
    def mostrar_tension(self, tension_bateria):
        pass

    @abstractmethod
    def mostrar_indicador(self, indicador_bateria):
        pass
```

---

### 2. **VisualizadorClimatizador - Cambio de Signature de Métodos**

**Archivos afectados:**
- `entidades/abs_visualizador_climatizador.py:8-13`
- `agentes_actuadores/visualizador_climatizador.py:10-42`

**Problema idéntico al anterior:**

```python
# Clase base
class AbsVisualizadorClimatizador(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def mostrar_estado_climatizador(tension_bateria):
        pass

# ✅ VisualizadorClimatizador: usa @staticmethod correctamente
# ❌ VisualizadorClimatizadorSocket (línea 20): usa self
# ❌ VisualizadorClimatizadorApi (línea 34): usa self
```

**Impacto:** Mismo problema que `VisualizadorBateria` - no intercambiables.

**Recomendación:** Misma solución - unificar todas las implementaciones a métodos de instancia.

---

### 3. **SeteoTemperatura - Cambio Radical de Comportamiento**

**Archivos afectados:**
- `servicios_aplicacion/abs_seteo_temperatura.py:4-9`
- `agentes_sensores/proxy_seteo_temperatura.py:8-86`

#### Clase Base: `AbsSeteoTemperatura`

```python
class AbsSeteoTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def obtener_seteo():
        pass
```

**Contrato:** Método estático que obtiene el seteo.

#### Implementación 1: `SeteoTemperatura` ✅ (líneas 8-16)

```python
class SeteoTemperatura(AbsSeteoTemperatura):

    @staticmethod
    def obtener_seteo():
        opcion = "0"
        while opcion not in ["1", "2"]:
            opcion = input(">")
        diferencia = "aumentar" if opcion == "1" else "disminuir"
        return diferencia
```

**Comportamiento:**
- Método estático
- Bloqueante (espera input del usuario)
- Siempre retorna un string válido ("aumentar" o "disminuir")

#### Implementación 2: `SeteoTemperaturaSocket` ❌ (líneas 19-86)

```python
class SeteoTemperaturaSocket(AbsSeteoTemperatura):

    def __init__(self):  # ❌ Requiere instanciación
        """Inicializa el socket persistente"""
        self._servidor = socket.socket(...)
        self._conexion = None
        self._servidor.settimeout(2.0)

    def obtener_seteo(self):  # ❌ Ya NO es @staticmethod
        """
        Consulta no-bloqueante del selector.
        Retorna None si no hay comando disponible.
        """
        diferencia = None
        try:
            # Lógica asíncrona con timeouts...
            if self._conexion is None:
                try:
                    self._conexion, direccion_cliente = self._servidor.accept()
                except socket.timeout:
                    return None  # ❌ Puede retornar None!
            # ...
        except Exception as e:
            print("[Seteo] Error: {}".format(e))

        return diferencia  # ❌ Puede ser None

    def __del__(self):
        """Limpieza al destruir el objeto"""
        # ...
```

**Problemas múltiples:**

1. **Cambio de signature:** De `@staticmethod` a método de instancia
2. **Requiere estado:** Tiene `__init__` con socket persistente
3. **Comportamiento diferente:**
   - `SeteoTemperatura`: Bloqueante, siempre retorna un valor válido
   - `SeteoTemperaturaSocket`: No bloqueante, puede retornar `None`
4. **Postcondición diferente:**
   - Base espera: siempre retorna string con comando
   - Socket retorna: `None` o string
5. **Ciclo de vida diferente:** Socket requiere limpieza (`__del__`)

**Impacto:**
- **Totalmente no intercambiable**
- Código que asume retorno no-None fallará
- Código que llama como método estático fallará

**Ejemplo de Fallo:**

```python
# Con SeteoTemperatura:
comando = SeteoTemperatura.obtener_seteo()  # ✅ "aumentar" o "disminuir"
print(comando.upper())  # ✅ Funciona

# Con SeteoTemperaturaSocket:
seteo = SeteoTemperaturaSocket()  # ❌ Requiere instanciación
comando = seteo.obtener_seteo()  # Puede retornar None
print(comando.upper())  # ❌ AttributeError: 'NoneType' has no attribute 'upper'
```

**Recomendación:**
- Separar responsabilidades: crear una abstracción para "fuente de comandos" que no asuma bloqueante/no-bloqueante
- O usar un patrón Adapter que unifique el comportamiento
- O hacer que ambas implementaciones sean no-bloqueantes y retornen `Optional[str]`

---

### 4. **SelectorTemperatura - Cambio de Comportamiento de Errores**

**Archivos afectados:**
- `servicios_aplicacion/abs_selector_temperatura.py:4-9`
- `agentes_sensores/proxy_selector_temperatura.py:11-118`

#### Clase Base: `AbsSelectorTemperatura`

```python
class AbsSelectorTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def obtener_selector():
        pass
```

#### Implementación 1: `SelectorTemperaturaArchivo` ❌ (líneas 11-51)

```python
class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = str(archivo.read()).strip()
            archivo.close()
        except IOError:
            mensaje_error = "Error al leer el tipo de temperatura"
            # ... logging ...
            raise mensaje_error  # ❌ Lanza excepción en error
        return tipo_temperatura
```

**Comportamiento:**
- Método estático
- **Lanza excepción** si no puede leer el archivo
- Retorna string si tiene éxito

#### Implementación 2: `SelectorTemperaturaSocket` ❌ (líneas 53-118)

```python
class SelectorTemperaturaSocket(AbsSelectorTemperatura):

    def __init__(self):  # ❌ Requiere instanciación
        """Inicializa el socket persistente y el estado"""
        self._estado_actual = "ambiente"  # ❌ Estado interno
        self._servidor = socket.socket(...)
        # ...

    def obtener_selector(self):  # ❌ Ya NO es @staticmethod
        """
        Consulta no-bloqueante del selector.
        Retorna el estado actual sin bloquearse si no hay cambios.
        """
        try:
            # Lógica asíncrona...
            if self._conexion is None:
                try:
                    self._conexion, _ = self._servidor.accept()
                except socket.timeout:
                    return self._estado_actual  # ✅ Retorna valor, no lanza
            # ...
        except Exception as e:
            print("[Selector] Error: {}".format(e))  # ✅ No lanza excepción

        return self._estado_actual  # ✅ Siempre retorna, nunca lanza
```

**Problemas múltiples:**

1. **Cambio de signature:** De `@staticmethod` a método de instancia
2. **Comportamiento de errores inconsistente:**
   - `SelectorTemperaturaArchivo`: **Lanza excepción** en error
   - `SelectorTemperaturaSocket`: **Nunca lanza excepción**, siempre retorna valor
3. **Estado interno:** Socket mantiene `_estado_actual`, Archivo no tiene estado
4. **Semántica diferente:**
   - Archivo: Lee cada vez desde fuente externa
   - Socket: Retorna último estado conocido si no hay conexión

**Impacto:**
- Código que espera excepción para manejar errores no funcionará con Socket
- Código que no espera excepción fallará con Archivo
- **No son intercambiables en absoluto**

**Ejemplo de Fallo:**

```python
# Código que espera excepción:
try:
    selector = SelectorTemperaturaArchivo()
    tipo = selector.obtener_selector()
    # Usar tipo...
except Exception as e:
    print("Error crítico: {}".format(e))  # ✅ Funciona con Archivo
    # Tomar acción de emergencia

# Con Socket:
try:
    selector = SelectorTemperaturaSocket()
    tipo = selector.obtener_selector()
    # Usar tipo... ❌ tipo puede ser valor antiguo, no hay señal de error!
except Exception as e:
    # ❌ Nunca se ejecuta, no se detecta el problema
    pass
```

**Recomendación:**
- Unificar manejo de errores: ambas deberían lanzar excepción en error crítico
- O ambas deberían retornar `Optional[str]` y nunca lanzar
- Documentar claramente el contrato en la clase base

---

## 🟠 VIOLACIONES MODERADAS

### 5. **ProxySensorTemperatura - Inconsistencia en Manejo de Errores**

**Archivos afectados:**
- `entidades/abs_sensor_temperatura.py:1-8`
- `agentes_sensores/proxy_sensor_temperatura.py:9-51`

#### Clase Base: `AbsProxySensorTemperatura`

```python
class AbsProxySensorTemperatura(metaclass=ABCMeta):

    @abstractmethod
    def leer_temperatura(self):
        pass
```

**Contrato:** Lee temperatura. **No especifica comportamiento de errores.**

#### Implementación 1: `ProxySensorTemperaturaArchivo` (líneas 9-18)

```python
class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):

    def leer_temperatura(self):
        try:
            archivo = open("temperatura", "r")
            temperatura = int(archivo.read())
            archivo.close()
        except IOError:
            raise Exception("Error de Lectura de Sensor")  # ❌ Lanza Exception
        return temperatura
```

**Comportamiento:** Lanza `Exception` en caso de error de I/O.

#### Implementación 2: `ProxySensorTemperaturaSocket` (líneas 21-51)

```python
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):

    def leer_temperatura(self):
        temperatura = None  # ❌ Inicializa como None
        servidor = socket.socket(...)
        # ... configuración ...

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                temperatura = float(datos.decode("utf-8"))
        except ConnectionError as e:
            print("Error de conexión: {}".format(e))  # ❌ No lanza, solo imprime
        finally:
            conexion.close()
            servidor.close()

        return temperatura  # ❌ Puede retornar None si hubo error
```

**Comportamiento:** Retorna `None` en caso de error de conexión.

**Problema:**
- **Postcondiciones diferentes:**
  - `ProxySensorTemperaturaArchivo`: Lanza excepción en error
  - `ProxySensorTemperaturaSocket`: Retorna `None` en error
- El código cliente debe manejar ambos casos de manera diferente

**Impacto:**
- Código que solo maneja excepciones no detectará errores de Socket
- Código que solo valida `None` fallará con errores de Archivo

**Ejemplo de Fallo:**

```python
# Código que espera excepciones:
def obtener_temperatura_con_retry(proxy):
    for intento in range(3):
        try:
            temp = proxy.leer_temperatura()
            return temp  # ✅ Funciona con Archivo
        except Exception:
            print("Reintentando...")
            time.sleep(1)
    raise Exception("No se pudo leer temperatura")

# Con Socket:
proxy_socket = ProxySensorTemperaturaSocket()
temp = obtener_temperatura_con_retry(proxy_socket)
# ❌ Si falla la lectura, retorna None (no lanza excepción)
# ❌ La función retorna None sin detectar el error
# ❌ No hay retry!
```

**Recomendación:** Unificar manejo de errores:
- Opción 1: Ambas lanzan excepción en error
- Opción 2: Ambas retornan `Optional[float]` (documentado en la base)
- Opción 3: Crear tipo de retorno `Result[float, Error]`

---

### 6. **ProxyBateria - Retorno de None Ambiguo**

**Archivos afectados:**
- `entidades/abs_bateria.py:1-8`
- `agentes_sensores/proxy_bateria.py:10-53`

#### Clase Base: `AbsProxyBateria`

```python
class AbsProxyBateria(metaclass=ABCMeta):

    @abstractmethod
    def leer_carga(self):
        pass
```

#### Implementación 1: `ProxyBateriaArchivo` (líneas 10-20)

```python
class ProxyBateriaArchivo(AbsProxyBateria):

    def leer_carga(self):
        try:
            archivo = open("bateria", "r")
            carga = float(archivo.read())
            archivo.close()
        except IOError:
            carga = None  # ❌ None en error
        return carga
```

#### Implementación 2: `ProxyBateriaSocket` (líneas 23-53)

```python
class ProxyBateriaSocket(AbsProxyBateria):

    def leer_carga(self):
        carga = None  # ❌ Inicializa como None
        servidor = socket.socket(...)
        # ... configuración ...

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                carga = float(datos.decode("utf-8"))
        except ConnectionError as e:
            print("Error de conexión: {}".format(e))
        finally:
            conexion.close()
            servidor.close()

        return carga  # ❌ None si hubo error o no hubo datos
```

**Problema:**
- Ambas implementaciones retornan `None` en error
- **Semántica ambigua:** ¿`None` significa "error" o "sin datos" o "batería desconectada"?
- No hay forma de distinguir entre diferentes condiciones de error
- **Debilita postcondiciones:** El código cliente no puede confiar en el tipo de retorno

**Impacto:**
- El código cliente debe asumir que `None` puede ocurrir
- No puede diferenciar entre tipos de error
- Dificulta debugging y logging
- Propaga `None` a través del sistema

**Ejemplo de Problema:**

```python
proxy = ProxyBateriaArchivo()
carga = proxy.leer_carga()

if carga is None:
    # ¿Qué pasó?
    # - ¿El archivo no existe?
    # - ¿El archivo está vacío?
    # - ¿El archivo tiene formato inválido?
    # - ¿No hay batería conectada?
    # ❌ No hay forma de saberlo
    print("Error indeterminado")  # Mensaje poco útil
else:
    print("Carga: {}".format(carga))
```

**Recomendación:** Hacer el error explícito:
- Opción 1: Lanzar excepciones específicas
- Opción 2: Retornar `Optional[float]` + logging detallado
- Opción 3: Usar tipo `Result[float, ErrorType]` para manejar errores explícitamente

---

## 🟡 VIOLACIONES MENORES

### 7. **Factories Retornan None - Violación de Type Hints**

**Archivos afectados:** 9 factories en `configurador/`

#### Ejemplo: `FactoryVisualizadorBateria` (líneas 8-20)

```python
class FactoryVisualizadorBateria:

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorBateria:  # ❌ Type hint promete AbsVisualizadorBateria

        if tipo == "archivo":
            return VisualizadorBateria()
        elif tipo == "socket":
            return VisualizadorBateriaSocket()
        elif tipo == "api":
            return VisualizadorBateriaApi()
        else:
            return None  # ❌ Retorna None, rompiendo el contrato del type hint!
```

**Problema:**
- El type hint promete: `-> AbsVisualizadorBateria` (nunca None)
- Pero retorna `None` cuando el tipo no es reconocido
- El código cliente que confía en el type hint fallará

**Factories afectadas:**
1. `FactoryVisualizadorBateria` (línea 20)
2. `FactoryVisualizadorTemperatura` (línea 20)
3. `FactoryVisualizadorClimatizador` (línea 18)
4. `FactoryProxySensorTemperatura` (línea 18)
5. `FactoryProxyBateria` (línea 18)
6. `FactorySelectorTemperatura` (línea 17)
7. `FactorySeteoTemperatura` (línea 18)
8. `FactoryClimatizador` (línea 18)
9. `FactoryActuadorClimatizador` (línea 14)

**Impacto:**
- Type checkers (mypy, pyright) reportarán errores
- IDEs darán autocompletado incorrecto
- Código que no valida `None` fallará en runtime con `AttributeError`

**Ejemplo de Fallo:**

```python
# Código que confía en type hints:
visualizador: AbsVisualizadorBateria = FactoryVisualizadorBateria.crear("mqtt")
# visualizador es None, pero el type hint dice que es AbsVisualizadorBateria

visualizador.mostrar_tension(12.5)
# ❌ AttributeError: 'NoneType' object has no attribute 'mostrar_tension'
```

**Recomendación:** Hacer explícito el retorno opcional:

```python
# Opción 1: Type hint correcto
@staticmethod
def crear(tipo: str) -> Optional[AbsVisualizadorBateria]:
    # ...
    return None

# Opción 2: Lanzar excepción en lugar de retornar None
@staticmethod
def crear(tipo: str) -> AbsVisualizadorBateria:
    if tipo == "archivo":
        return VisualizadorBateria()
    elif tipo == "socket":
        return VisualizadorBateriaSocket()
    elif tipo == "api":
        return VisualizadorBateriaApi()
    else:
        raise ValueError(f"Tipo de visualizador no soportado: {tipo}")
```

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Componentes Afectados | Impacto Principal |
|-----------|----------|----------------------|-------------------|
| 🔴 Crítica | 4 | VisualizadorBateria, VisualizadorClimatizador, SeteoTemperatura, SelectorTemperatura | No intercambiables - cambio de signature y comportamiento |
| 🟠 Moderada | 2 | ProxySensorTemperatura, ProxyBateria | Inconsistencia en manejo de errores |
| 🟡 Menor | 1 (9 instancias) | Todas las Factories | Type hints incorrectos - retornan None |
| **TOTAL** | **7 tipos** | **15+ clases** | **Polimorfismo roto** |

---

## 💡 Patrones de Violación Identificados

### Patrón 1: Inconsistencia @staticmethod vs método de instancia

**Clases afectadas:** VisualizadorBateria, VisualizadorClimatizador, SeteoTemperatura, SelectorTemperatura

**Causa raíz:** Diseño inicial asumió métodos estáticos, pero implementaciones Socket/Api requieren estado interno (socket persistente)

**Solución:**
```python
# ❌ Antes (inconsistente):
class Base:
    @staticmethod
    @abstractmethod
    def metodo(): pass

class Impl1:
    @staticmethod
    def metodo(): pass  # OK

class Impl2:
    def metodo(self): pass  # ❌ Rompe LSP

# ✅ Después (consistente):
class Base:
    @abstractmethod
    def metodo(self): pass  # Todos son métodos de instancia

class Impl1:
    def metodo(self): pass  # OK

class Impl2:
    def metodo(self): pass  # OK
```

### Patrón 2: Inconsistencia en manejo de errores (Excepción vs None)

**Clases afectadas:** ProxySensorTemperatura, SelectorTemperatura

**Problema:** Algunas implementaciones lanzan excepciones, otras retornan None

**Solución:**
```python
# Opción 1: Todas lanzan excepciones
class Base:
    @abstractmethod
    def metodo(self) -> float:
        """
        Retorna valor.
        Raises: Exception si hay error
        """
        pass

# Opción 2: Todas retornan Optional
class Base:
    @abstractmethod
    def metodo(self) -> Optional[float]:
        """
        Retorna valor o None si hay error.
        Nunca lanza excepciones.
        """
        pass

# Opción 3: Result type (más explícito)
class Base:
    @abstractmethod
    def metodo(self) -> Result[float, Error]:
        """
        Retorna Ok(valor) o Err(error).
        """
        pass
```

### Patrón 3: Type hints que prometen más de lo que cumplen

**Clases afectadas:** Todas las Factories (9)

**Problema:** Type hint dice `-> Tipo` pero retorna `None`

**Solución:**
```python
# Opción 1: Type hint honesto
def crear(tipo: str) -> Optional[Tipo]:
    # ... puede retornar None

# Opción 2: Lanzar excepción (más Pythonic)
def crear(tipo: str) -> Tipo:
    # ...
    if tipo_invalido:
        raise ValueError(f"Tipo no soportado: {tipo}")
```

---

## 📋 Plan de Acción Priorizado

### Fase 1: Unificar Signatures (Prioridad Crítica)

**Objetivo:** Eliminar inconsistencias @staticmethod vs método de instancia

**Componentes a refactorizar:**
1. `AbsVisualizadorBateria` + implementaciones → métodos de instancia
2. `AbsVisualizadorClimatizador` + implementaciones → métodos de instancia
3. `AbsSeteoTemperatura` + implementaciones → métodos de instancia
4. `AbsSelectorTemperatura` + implementaciones → métodos de instancia

**Pasos:**
1. Cambiar clases base de `@staticmethod @abstractmethod` a `@abstractmethod`
2. Actualizar `VisualizadorBateria` para usar `self` (aunque no lo necesite)
3. Actualizar todas las llamadas en el código cliente para usar instancias
4. Actualizar factories para retornar instancias correctamente creadas
5. Actualizar tests

**Esfuerzo estimado:** 6-8 horas

**Beneficios:**
- Todas las subclases son intercambiables
- Polimorfismo funciona correctamente
- Consistencia en el código

---

### Fase 2: Unificar Manejo de Errores (Prioridad Alta)

**Objetivo:** Consistencia en cómo se reportan errores

**Componentes a refactorizar:**
1. `ProxySensorTemperatura` + implementaciones
2. `ProxyBateria` + implementaciones
3. `SelectorTemperatura` + implementaciones

**Decisión de diseño requerida:**
- **Opción A:** Todas lanzan excepciones (más explícito, mejor para errores críticos)
- **Opción B:** Todas retornan `Optional[T]` (más funcional, mejor para errores esperados)

**Recomendación:** Opción A para errores de I/O (son excepcionales), Opción B para "sin datos" (es normal)

**Pasos:**
1. Documentar contrato de error en clases base
2. Actualizar implementaciones para seguir el contrato
3. Actualizar código cliente para manejar errores consistentemente
4. Agregar logging apropiado
5. Actualizar tests

**Esfuerzo estimado:** 4-6 horas

---

### Fase 3: Corregir Type Hints en Factories (Prioridad Media)

**Objetivo:** Type hints honestos que reflejen la realidad

**Componentes a refactorizar:** 9 factories

**Recomendación:** Lanzar excepción en lugar de retornar None

**Pasos:**
1. Cambiar `return None` por `raise ValueError(f"Tipo no soportado: {tipo}")`
2. Mantener type hints como `-> Tipo` (sin Optional)
3. Actualizar código cliente para manejar excepción si es necesario
4. Agregar validación en Configurador para detectar tipos inválidos tempranamente
5. Actualizar tests

**Esfuerzo estimado:** 2-3 horas

**Beneficios:**
- Type checkers felices
- Errores detectados tempranamente
- Código más seguro

---

### Fase 4: Documentar Contratos (Prioridad Media)

**Objetivo:** Documentación clara de comportamiento esperado

**Componentes:** Todas las clases abstractas

**Pasos:**
1. Agregar docstrings completos a todas las clases abstractas
2. Documentar:
   - Qué retorna cada método
   - Qué excepciones lanza (si aplica)
   - Precondiciones y postcondiciones
   - Invariantes
3. Validar que implementaciones cumplan contrato

**Esfuerzo estimado:** 3-4 horas

---

## 🎯 Ejemplos de Refactoring

### Ejemplo 1: Refactoring de VisualizadorBateria

#### Antes (Viola LSP):

```python
# Clase base
class AbsVisualizadorBateria(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def mostrar_tension(tension_bateria): pass

# Implementación 1
class VisualizadorBateria(AbsVisualizadorBateria):
    @staticmethod
    def mostrar_tension(tension_bateria):
        print(str(tension_bateria))

# Implementación 2 - ❌ ROMPE LSP
class VisualizadorBateriaSocket(AbsVisualizadorBateria):
    def mostrar_tension(self, tension_bateria):  # ❌ Ya no es static
        cliente = socket.socket(...)
        # ...

# Uso - ❌ FALLA
visualizador = factory.crear("socket")
visualizador.mostrar_tension(12.5)  # ❌ Error!
```

#### Después (Cumple LSP):

```python
# Clase base - TODOS son métodos de instancia
class AbsVisualizadorBateria(metaclass=ABCMeta):
    @abstractmethod
    def mostrar_tension(self, tension_bateria: float) -> None:
        """
        Muestra la tensión de la batería.

        Args:
            tension_bateria: Tensión en voltios

        Raises:
            IOError: Si no se puede mostrar (subclases pueden lanzar)
        """
        pass

# Implementación 1 - Ahora usa self
class VisualizadorBateria(AbsVisualizadorBateria):
    def mostrar_tension(self, tension_bateria: float) -> None:
        print(str(tension_bateria))

# Implementación 2 - ✅ CONSISTENTE
class VisualizadorBateriaSocket(AbsVisualizadorBateria):
    def __init__(self, host: str = "localhost", puerto: int = 14000):
        self._host = host
        self._puerto = puerto

    def mostrar_tension(self, tension_bateria: float) -> None:
        cliente = socket.socket(...)
        direccion = (self._host, self._puerto)
        cliente.connect(direccion)
        # ...

# Uso - ✅ FUNCIONA
visualizador = factory.crear("socket")
visualizador.mostrar_tension(12.5)  # ✅ OK!
```

### Ejemplo 2: Refactoring de ProxySensorTemperatura

#### Antes (Manejo inconsistente de errores):

```python
# Implementación 1 - Lanza excepción
class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):
    def leer_temperatura(self):
        try:
            archivo = open("temperatura", "r")
            return int(archivo.read())
        except IOError:
            raise Exception("Error de Lectura de Sensor")  # ❌ Lanza

# Implementación 2 - Retorna None
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):
    def leer_temperatura(self):
        temperatura = None
        try:
            # ... lectura ...
            temperatura = float(datos.decode())
        except ConnectionError:
            pass  # ❌ No lanza, retorna None
        return temperatura
```

#### Después (Manejo consistente):

```python
# Clase base - Contrato explícito
class AbsProxySensorTemperatura(metaclass=ABCMeta):
    @abstractmethod
    def leer_temperatura(self) -> float:
        """
        Lee la temperatura del sensor.

        Returns:
            Temperatura en grados Celsius

        Raises:
            IOError: Si no se puede leer el sensor
            ConnectionError: Si hay problema de conexión (implementaciones remotas)
        """
        pass

# Implementación 1 - ✅ Lanza IOError (estándar)
class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):
    def leer_temperatura(self) -> float:
        try:
            with open("temperatura", "r") as archivo:
                return float(archivo.read())
        except (IOError, ValueError) as e:
            raise IOError(f"Error leyendo sensor de archivo: {e}")

# Implementación 2 - ✅ Lanza ConnectionError
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):
    def leer_temperatura(self) -> float:
        try:
            # ... configuración socket ...
            datos = conexion.recv(4096)
            if not datos:
                raise ConnectionError("Socket cerrado sin datos")
            return float(datos.decode("utf-8"))
        except (socket.error, ValueError) as e:
            raise ConnectionError(f"Error leyendo sensor remoto: {e}")
        finally:
            conexion.close()
            servidor.close()

# Uso - ✅ CONSISTENTE
def leer_con_retry(proxy: AbsProxySensorTemperatura, max_reintentos: int = 3) -> float:
    for intento in range(max_reintentos):
        try:
            return proxy.leer_temperatura()  # ✅ Funciona con ambas implementaciones
        except (IOError, ConnectionError) as e:
            if intento == max_reintentos - 1:
                raise
            print(f"Reintento {intento + 1}/{max_reintentos}: {e}")
            time.sleep(1)
```

### Ejemplo 3: Refactoring de Factories

#### Antes (Type hint mentiroso):

```python
class FactoryVisualizadorBateria:
    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorBateria:  # ❌ Miente
        if tipo == "archivo":
            return VisualizadorBateria()
        elif tipo == "socket":
            return VisualizadorBateriaSocket()
        else:
            return None  # ❌ Retorna None!

# Uso
vis = FactoryVisualizadorBateria.crear("mqtt")  # None
vis.mostrar_tension(12.5)  # ❌ AttributeError!
```

#### Después (Type hint honesto):

```python
class FactoryVisualizadorBateria:
    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorBateria:  # ✅ Promesa real
        """
        Crea un visualizador de batería según el tipo.

        Args:
            tipo: Tipo de visualizador ("archivo", "socket", "api")

        Returns:
            Instancia de AbsVisualizadorBateria

        Raises:
            ValueError: Si el tipo no es soportado
        """
        if tipo == "archivo":
            return VisualizadorBateria()
        elif tipo == "socket":
            return VisualizadorBateriaSocket()
        elif tipo == "api":
            return VisualizadorBateriaApi()
        else:
            raise ValueError(
                f"Tipo de visualizador no soportado: '{tipo}'. "
                f"Tipos válidos: 'archivo', 'socket', 'api'"
            )

# Uso - ✅ Falla temprano con mensaje claro
try:
    vis = FactoryVisualizadorBateria.crear("mqtt")
except ValueError as e:
    print(f"Error de configuración: {e}")  # ✅ Mensaje útil
    sys.exit(1)
```

---

## 🔍 Indicadores de Éxito

Después del refactoring, estas operaciones deberían funcionar correctamente:

1. ✅ **Polimorfismo verdadero:**
   ```python
   def mostrar_bateria(visualizador: AbsVisualizadorBateria, tension: float):
       visualizador.mostrar_tension(tension)

   # Funciona con CUALQUIER implementación:
   mostrar_bateria(VisualizadorBateria(), 12.5)
   mostrar_bateria(VisualizadorBateriaSocket(), 12.5)
   mostrar_bateria(VisualizadorBateriaApi(), 12.5)
   ```

2. ✅ **Manejo de errores consistente:**
   ```python
   try:
       temp = proxy.leer_temperatura()  # Cualquier proxy
   except (IOError, ConnectionError) as e:
       # Manejo único para todas las implementaciones
       log_error(e)
   ```

3. ✅ **Type checking sin errores:**
   ```bash
   $ mypy configurador/
   Success: no issues found
   ```

4. ✅ **Tests intercambiables:**
   ```python
   @pytest.mark.parametrize("proxy_class", [
       ProxySensorTemperaturaArchivo,
       ProxySensorTemperaturaSocket
   ])
   def test_leer_temperatura(proxy_class):
       proxy = proxy_class()
       temp = proxy.leer_temperatura()
       assert isinstance(temp, float)  # ✅ Funciona con ambas
   ```

---

## 🎯 Conclusión

El proyecto presenta **7 tipos de violaciones del LSP** que afectan **15+ clases**:

### Problemas Principales:

1. **Inconsistencia @staticmethod vs instancia** (4 jerarquías)
   - Subclases cambian signature de métodos
   - Imposible intercambiar implementaciones
   - Rompe polimorfismo completamente

2. **Manejo inconsistente de errores** (2 jerarquías)
   - Unas lanzan excepciones, otras retornan None
   - Código cliente debe conocer implementación concreta
   - Dificulta testing y mantenimiento

3. **Type hints incorrectos** (9 factories)
   - Prometen un tipo pero pueden retornar None
   - Type checkers reportan errores
   - Fallos en runtime difíciles de debuggear

### Impacto:

- **Polimorfismo roto:** No se pueden usar abstracciones con confianza
- **Código frágil:** Cambiar implementación puede romper el sistema
- **Testing difícil:** Cada implementación requiere pruebas específicas
- **Violación del principio de diseño:** "Program to an interface, not an implementation"

### Beneficios del Refactoring:

- **Intercambiabilidad real:** Cualquier implementación funciona igual
- **Código más robusto:** Menos sorpresas en runtime
- **Testing simplificado:** Tests polimórficos que funcionan con todas las implementaciones
- **Type safety:** Type checkers pueden garantizar corrección
- **Mantenibilidad:** Cambios localizados, sin efectos inesperados

### Esfuerzo Total Estimado:

- Fase 1 (Crítica): 6-8 horas
- Fase 2 (Alta): 4-6 horas
- Fase 3 (Media): 2-3 horas
- Fase 4 (Media): 3-4 horas
- **Total: 15-21 horas**

---

## 📚 Referencias

- **Liskov Substitution Principle**: Barbara Liskov & Jeannette Wing, "A Behavioral Notion of Subtyping" (1994)
- **Design by Contract**: Bertrand Meyer, "Object-Oriented Software Construction"
- **SOLID Principles**: Robert C. Martin, "Agile Software Development"
- **Python Type Hints**: PEP 484, PEP 526
- **Effective Python**: Brett Slatkin, Item 37: "Compose Classes Instead of Nesting Many Levels of Built-in Types"

---

**Documento generado automáticamente mediante análisis estático del código.**
