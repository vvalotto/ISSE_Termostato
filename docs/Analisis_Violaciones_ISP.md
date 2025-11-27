# Análisis de Violaciones del Principio ISP (Interface Segregation Principle)

**Proyecto:** ISSE_Termostato
**Fecha:** Noviembre 2025
**Análisis realizado por:** Claude Code

---

## Definición del Principio ISP

> "Los clientes no deberían verse forzados a depender de interfaces que no usan."
> — Robert C. Martin

**En otras palabras:** Es mejor tener muchas interfaces específicas orientadas al cliente que una interfaz de propósito general. Ningún cliente debería ser forzado a implementar métodos que no utiliza.

**Señales de violación del ISP:**
1. Clases que implementan interfaces pero dejan métodos vacíos o con `pass`
2. Clases que implementan métodos que lanzan `NotImplementedError`
3. Clientes que dependen de clases/interfaces grandes pero solo usan un subconjunto de métodos
4. Interfaces "gordas" con múltiples responsabilidades no relacionadas
5. Herencia múltiple forzada para agregar funcionalidad ortogonal

---

## 🔴 VIOLACIONES CRÍTICAS

### 1. **SelectorTemperaturaArchivo - Herencia Forzada de AbsRegistrador**

**Archivos afectados:**
- `registrador/registrador.py:8-13`
- `agentes_sensores/proxy_selector_temperatura.py:11-51`
- `agentes_sensores/proxy_selector_temperatura.py:53-118`

#### Análisis de las Interfaces:

```python
# registrador/registrador.py
class AbsRegistrador:
    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        pass
```

#### Implementaciones del Selector:

**Implementación 1: SelectorTemperaturaArchivo** (líneas 11-51)

```python
class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):  # ❌ Hereda AbsRegistrador

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = str(archivo.read()).strip()
            archivo.close()
        except IOError:
            mensaje_error = "Error al leer el tipo de temperatura"
            registro_error = SelectorTemperaturaArchivo._armar_registro_error(...)
            SelectorTemperaturaArchivo.registrar_error(registro_error)  # ← Usa registro
            raise mensaje_error
        return tipo_temperatura

    @staticmethod
    def registrar_error(registro):  # ← Implementa AbsRegistrador
        try:
            with open("registro_errores", "a") as archivo_errores:
                archivo_errores.write(registro)
        except IOError:
            raise "Error al escribir el archivo de errores"
```

**Implementación 2: SelectorTemperaturaSocket** (líneas 53-118)

```python
class SelectorTemperaturaSocket(AbsSelectorTemperatura):  # ✅ NO hereda AbsRegistrador

    def __init__(self):
        self._estado_actual = "ambiente"
        self._servidor = socket.socket(...)
        # ...

    def obtener_selector(self):
        try:
            # ... lógica de socket ...
        except Exception as e:
            print("[Selector] Error: {}".format(e))  # ← Solo imprime, NO registra

        return self._estado_actual
```

**Problema:**
- **Inconsistencia en herencia:** Una implementación hereda `AbsRegistrador`, la otra no
- **Funcionalidad forzada:** El registro de errores no es parte esencial de la interfaz del selector
- **Violación ISP:** `AbsRegistrador` es una preocupación transversal (cross-cutting concern) que se mezcla con la responsabilidad principal del selector
- **Acoplamiento innecesario:** `SelectorTemperaturaArchivo` está acoplado a la mecánica de registro, que debería ser responsabilidad de otra capa

**Impacto:**
- Diferentes implementaciones tienen diferentes interfaces (una más grande que la otra)
- El registro de errores es un concern ortogonal que no debería estar en la interfaz del selector
- Dificulta testing: para probar el selector de archivo necesitas mockear el sistema de archivos de errores
- Viola SRP además de ISP

**Ejemplo de Problema:**

```python
# Si queremos crear una nueva implementación (ej: HTTP)
class SelectorTemperaturaHttp(AbsSelectorTemperatura):
    def obtener_selector(self):
        response = requests.get("http://api/selector")
        return response.text

# ¿Debería heredar de AbsRegistrador?
# - Si NO hereda: inconsistencia con SelectorTemperaturaArchivo
# - Si hereda: forzado a implementar registrar_error() que tal vez no necesita
```

**Recomendación:** Usar **Dependency Injection** para el registro de errores

```python
# Solución: Inyectar registrador como dependencia, no como interfaz

class SelectorTemperaturaArchivo(AbsSelectorTemperatura):
    def __init__(self, registrador=None):
        self._registrador = registrador or RegistradorErrores()

    @staticmethod
    def obtener_selector():
        try:
            # ... lectura ...
        except IOError as e:
            if self._registrador:
                self._registrador.registrar_error(...)
            raise

# Ahora NO hereda AbsRegistrador
# El registro es una dependencia opcional inyectada
```

---

### 2. **ActuadorClimatizadorGeneral - Triple Herencia con Concerns Mezclados**

**Archivos afectados:**
- `entidades/abs_actuador_climatizador.py:8-13`
- `registrador/registrador.py:8-20`
- `agentes_actuadores/actuador_climatizador.py:11-68`

#### Interfaces Involucradas:

```python
# 1. Responsabilidad principal
class AbsActuadorClimatizador(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def accionar_climatizador(accion):
        pass

# 2. Cross-cutting concern: Registro de errores
class AbsRegistrador:
    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        pass

# 3. Cross-cutting concern: Auditoría
class AbsAuditor:
    @staticmethod
    @abstractmethod
    def auditar_funcion(registro):
        pass
```

#### Implementación:

```python
# actuador_climatizador.py:11
class ActuadorClimatizadorGeneral(AbsActuadorClimatizador, AbsRegistrador, AbsAuditor):
    # ❌ Hereda de 3 interfaces!

    @staticmethod
    def accionar_climatizador(accion):
        # Auditoría mezclada con lógica de negocio
        mensaje_accion = "accionando el climatizador"
        ActuadorClimatizadorGeneral.auditar_funcion(
            ActuadorClimatizadorGeneral.__name__,
            mensaje_accion,
            str(datetime.datetime.now())
        )

        try:
            with open("climatizador", "w") as archivo_climatizador:
                archivo_climatizador.write(accion)
        except IOError:
            # Registro de errores mezclado con lógica de negocio
            registro_error = ActuadorClimatizadorGeneral._armar_registro_error(...)
            ActuadorClimatizadorGeneral.registrar_error(registro_error)

    @staticmethod
    def registrar_error(registro):
        # Implementación de AbsRegistrador
        # ...

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        # Implementación de AbsAuditor
        # ...
```

**Problema:**
- **Herencia múltiple para funcionalidad ortogonal:** El actuador está forzado a heredar 3 interfaces
- **Concerns mezclados:** Actuación + Registro + Auditoría en una sola clase
- **Interfaz "gorda":** La clase tiene responsabilidades no relacionadas
- **Violación ISP:** Los clientes que solo quieren accionar el climatizador están forzados a depender de registro y auditoría
- **Violación SRP:** Ya identificada en el análisis anterior

**Impacto:**
- Si queremos crear un `ActuadorClimatizadorMock` para testing, ¿debe implementar registro y auditoría?
- Si queremos un actuador simple sin auditoría, ¿estamos forzados a heredar `AbsAuditor`?
- Acoplamiento innecesario entre actuación y logging
- Dificulta reutilización y testing

**Ejemplo de Problema:**

```python
# Para testing queremos un actuador simple:
class ActuadorClimatizadorMock(AbsActuadorClimatizador):
    def __init__(self):
        self.acciones = []

    def accionar_climatizador(self, accion):
        self.acciones.append(accion)

# ❌ Problema: ¿Debería heredar AbsRegistrador y AbsAuditor también?
# - Si NO hereda: inconsistencia con ActuadorClimatizadorGeneral
# - Si hereda: forzado a implementar métodos que no necesita para testing
```

**Recomendación:** Usar **Decorator Pattern** o **Dependency Injection**

```python
# Solución 1: Decorator Pattern para cross-cutting concerns

class ActuadorClimatizadorSimple(AbsActuadorClimatizador):
    # Solo responsabilidad principal, NO hereda AbsRegistrador ni AbsAuditor
    @staticmethod
    def accionar_climatizador(accion):
        with open("climatizador", "w") as archivo:
            archivo.write(accion)

class ActuadorConAuditoria:
    """Decorator que agrega auditoría"""
    def __init__(self, actuador, auditor):
        self._actuador = actuador
        self._auditor = auditor

    def accionar_climatizador(self, accion):
        self._auditor.auditar_funcion(
            self.__class__.__name__,
            "accionando el climatizador",
            str(datetime.datetime.now())
        )
        self._actuador.accionar_climatizador(accion)

class ActuadorConRegistro:
    """Decorator que agrega registro de errores"""
    def __init__(self, actuador, registrador):
        self._actuador = actuador
        self._registrador = registrador

    def accionar_climatizador(self, accion):
        try:
            self._actuador.accionar_climatizador(accion)
        except Exception as e:
            self._registrador.registrar_error(str(e))
            raise

# Uso: Composición en lugar de herencia
actuador = ActuadorClimatizadorSimple()
actuador = ActuadorConAuditoria(actuador, Auditor())
actuador = ActuadorConRegistro(actuador, RegistradorErrores())

# Para testing: usar solo el actuador simple
actuador_test = ActuadorClimatizadorSimple()
```

---

## 🟠 VIOLACIONES MODERADAS

### 3. **Presentador - Dependencia de Gestores Completos con Interfaces Grandes**

**Archivos afectados:**
- `servicios_aplicacion/presentador.py:6-41`
- `gestores_entidades/gestor_bateria.py:10-44`
- `gestores_entidades/gestor_ambiente.py:12-61`
- `gestores_entidades/gestor_climatizador.py:9-27`

#### Clase Presentador:

```python
class Presentador:

    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        # ❌ Depende de gestores completos
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador

    def ejecutar(self):
        print("-------------- BATERIA -------------")
        self._gestor_bateria.mostrar_nivel_de_carga()        # ← Solo usa este método
        self._gestor_bateria.mostrar_indicador_de_carga()    # ← Y este

        print("------------ TEMPERATURA ----------")
        self._gestor_ambiente.mostrar_temperatura()          # ← Solo usa este método

        print("------------ CLIMATIZADOR ----------")
        self._gestor_climatizador.mostrar_estado_climatizador()  # ← Solo usa este método
```

#### Interfaz de GestorBateria (métodos disponibles):

```python
class GestorBateria:
    def __init__(self): ...
    def verificar_nivel_de_carga(self): ...          # ❌ Presentador NO usa
    def obtener_nivel_de_carga(self): ...            # ❌ Presentador NO usa
    def obtener_indicador_de_carga(self): ...        # ❌ Presentador NO usa
    def mostrar_nivel_de_carga(self): ...            # ✅ Presentador USA
    def mostrar_indicador_de_carga(self): ...        # ✅ Presentador USA
```

**Presentador usa:** 2 de 5 métodos (40%)

#### Interfaz de GestorAmbiente (métodos disponibles):

```python
class GestorAmbiente:
    def __init__(self): ...
    def leer_temperatura_ambiente(self): ...         # ❌ Presentador NO usa
    def obtener_temperatura_ambiente(self): ...      # ❌ Presentador NO usa
    def mostrar_temperatura_ambiente(self): ...      # ❌ Presentador NO usa
    def aumentar_temperatura_deseada(self): ...      # ❌ Presentador NO usa
    def disminuir_temperatura_deseada(self): ...     # ❌ Presentador NO usa
    def obtener_temperatura_deseada(self): ...       # ❌ Presentador NO usa
    def mostrar_temperatura_deseada(self): ...       # ❌ Presentador NO usa
    def mostrar_temperatura(self): ...               # ✅ Presentador USA
    def indicar_temperatura_a_mostrar(self, tipo): ...  # ❌ Presentador NO usa
```

**Presentador usa:** 1 de 9 métodos (11%)

#### Interfaz de GestorClimatizador (métodos disponibles):

```python
class GestorClimatizador:
    def __init__(self): ...
    def accionar_climatizador(self, ambiente): ...   # ❌ Presentador NO usa
    def obtener_estado_climatizador(self): ...       # ❌ Presentador NO usa
    def mostrar_estado_climatizador(self): ...       # ✅ Presentador USA
```

**Presentador usa:** 1 de 3 métodos (33%)

**Problema:**
- **Dependencia de interfaces grandes:** Presentador depende de gestores completos pero usa solo una fracción de sus métodos
- **Acoplamiento innecesario:** Cualquier cambio en los gestores afecta a Presentador, incluso en métodos que no usa
- **Violación ISP:** Cliente forzado a depender de más de lo que necesita
- **Dificulta testing:** Para testear Presentador hay que mockear todos los métodos de los gestores, incluso los no usados

**Impacto:**
- Acoplamiento alto entre Presentador y Gestores
- Cambios en métodos no usados pueden requerir recompilación/testing de Presentador
- Testing complejo: necesitas crear mocks completos de los gestores
- Dificulta entender qué funcionalidad realmente necesita Presentador

**Recomendación:** Crear **interfaces segregadas** específicas para presentación

```python
# Solución: Interfaces pequeñas orientadas al cliente

class InterfazPresentacionBateria(ABC):
    """Interfaz mínima que Presentador necesita de la batería"""
    @abstractmethod
    def mostrar_nivel_de_carga(self): pass

    @abstractmethod
    def mostrar_indicador_de_carga(self): pass

class InterfazPresentacionTemperatura(ABC):
    """Interfaz mínima que Presentador necesita de la temperatura"""
    @abstractmethod
    def mostrar_temperatura(self): pass

class InterfazPresentacionClimatizador(ABC):
    """Interfaz mínima que Presentador necesita del climatizador"""
    @abstractmethod
    def mostrar_estado_climatizador(self): pass

# GestorBateria implementa AMBAS interfaces:
# - La completa (para otros clientes)
# - La de presentación (para Presentador)
class GestorBateria(InterfazPresentacionBateria):
    # Métodos de InterfazPresentacionBateria
    def mostrar_nivel_de_carga(self): ...
    def mostrar_indicador_de_carga(self): ...

    # Otros métodos (no en la interfaz de presentación)
    def verificar_nivel_de_carga(self): ...
    def obtener_nivel_de_carga(self): ...
    # ...

# Presentador ahora depende de interfaces pequeñas
class Presentador:
    def __init__(self,
                 presentacion_bateria: InterfazPresentacionBateria,
                 presentacion_temperatura: InterfazPresentacionTemperatura,
                 presentacion_climatizador: InterfazPresentacionClimatizador):
        self._bateria = presentacion_bateria
        self._temperatura = presentacion_temperatura
        self._climatizador = presentacion_climatizador

# Beneficios:
# - Presentador solo ve los métodos que necesita
# - Testing simple: interfaces pequeñas fáciles de mockear
# - Bajo acoplamiento
# - Principio de mínimo conocimiento (Law of Demeter)
```

---

### 4. **OperadorParalelo - Dependencia de Gestores Completos**

**Archivos afectados:**
- `servicios_aplicacion/operador_paralelo.py:12-79`

#### Clase OperadorParalelo:

```python
class OperadorParalelo:

    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        # ❌ Depende de gestores completos
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador
        self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
        self._presentador = Presentador(...)

    def lee_carga_bateria(self):
        while True:
            self._gestor_bateria.verificar_nivel_de_carga()  # ← Solo usa este método
            time.sleep(1)

    def lee_temperatura_ambiente(self):
        while True:
            self._gestor_ambiente.leer_temperatura_ambiente()  # ← Solo usa este método
            time.sleep(2)

    def acciona_climatizador(self):
        while True:
            self._gestor_climatizador.accionar_climatizador(
                self._gestor_ambiente.ambiente  # ← Accede a propiedad interna
            )
            time.sleep(5)

    def muestra_parametros(self):
        while True:
            self._presentador.ejecutar()  # ← Delega al presentador
            time.sleep(5)

    def setea_temperatura(self):
        while True:
            self._selector.ejecutar()  # ← Delega al selector
            time.sleep(5)
```

**Problema:**
- **Métodos especializados usan solo 1 método del gestor:** Cada thread solo necesita una operación específica
- **Dependencia de interfaz completa:** `lee_carga_bateria()` solo necesita `verificar_nivel_de_carga()` pero depende de todo GestorBateria
- **Violación ISP:** Cada método del OperadorParalelo debería depender solo de la funcionalidad que usa
- **Acoplamiento alto:** Cambios en cualquier método del gestor pueden afectar al OperadorParalelo

**Análisis de uso:**

| Método OperadorParalelo | Gestor usado | Método usado | Total métodos gestor | % usado |
|-------------------------|--------------|--------------|----------------------|---------|
| `lee_carga_bateria()` | GestorBateria | `verificar_nivel_de_carga()` | 5 métodos | 20% |
| `lee_temperatura_ambiente()` | GestorAmbiente | `leer_temperatura_ambiente()` | 9 métodos | 11% |
| `acciona_climatizador()` | GestorClimatizador | `accionar_climatizador()` | 3 métodos | 33% |

**Impacto:**
- Acoplamiento innecesario entre tareas paralelas y gestores completos
- Testing complejo: hay que mockear gestores completos para cada tarea
- Dificulta entender las dependencias reales de cada thread
- Violación del principio de mínimo conocimiento

**Recomendación:** Usar **interfaces segregadas** o **callbacks específicos**

```python
# Solución 1: Interfaces segregadas por tarea

class InterfazLecturaBateria(ABC):
    @abstractmethod
    def verificar_nivel_de_carga(self): pass

class InterfazLecturaTemperatura(ABC):
    @abstractmethod
    def leer_temperatura_ambiente(self): pass

class InterfazAccionamientoClimatizador(ABC):
    @abstractmethod
    def accionar_climatizador(self, ambiente): pass

    @property
    @abstractmethod
    def ambiente(self): pass

# OperadorParalelo con dependencias mínimas
class OperadorParalelo:
    def __init__(self,
                 lectura_bateria: InterfazLecturaBateria,
                 lectura_temperatura: InterfazLecturaTemperatura,
                 accionamiento: InterfazAccionamientoClimatizador,
                 presentador,
                 selector):
        self._lectura_bateria = lectura_bateria
        self._lectura_temperatura = lectura_temperatura
        self._accionamiento = accionamiento
        # ...

    def lee_carga_bateria(self):
        while True:
            self._lectura_bateria.verificar_nivel_de_carga()
            time.sleep(1)

# Solución 2: Inyectar callbacks en lugar de gestores
class OperadorParalelo:
    def __init__(self,
                 verificar_bateria_callback: Callable[[], None],
                 leer_temperatura_callback: Callable[[], None],
                 accionar_climatizador_callback: Callable[[Ambiente], None],
                 # ...
                 ):
        self._verificar_bateria = verificar_bateria_callback
        self._leer_temperatura = leer_temperatura_callback
        # ...

    def lee_carga_bateria(self):
        while True:
            self._verificar_bateria()
            time.sleep(1)

# Uso:
gestor_bateria = GestorBateria()
gestor_ambiente = GestorAmbiente()
gestor_climatizador = GestorClimatizador()

operador = OperadorParalelo(
    verificar_bateria_callback=gestor_bateria.verificar_nivel_de_carga,
    leer_temperatura_callback=gestor_ambiente.leer_temperatura_ambiente,
    accionar_climatizador_callback=lambda: gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente),
    # ...
)

# Testing simple:
def mock_verificar_bateria():
    print("Mock bateria")

operador_test = OperadorParalelo(
    verificar_bateria_callback=mock_verificar_bateria,
    # ...
)
```

---

### 5. **AbsVisualizadorTemperatura - Interfaz con Dos Métodos Usados Selectivamente**

**Archivos afectados:**
- `entidades/abs_visualizador_temperatura.py:8-18`
- `gestores_entidades/gestor_ambiente.py:53-57`

#### Interfaz:

```python
class AbsVisualizadorTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        pass

    @staticmethod
    @abstractmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        pass
```

#### Uso en GestorAmbiente:

```python
def mostrar_temperatura(self):
    if self._ambiente.temperatura_a_mostrar == "ambiente":
        self._visualizador_temperatura.mostrar_temperatura_ambiente(...)  # ← Usa uno
    elif self._ambiente.temperatura_a_mostrar == "deseada":
        self._visualizador_temperatura.mostrar_temperatura_deseada(...)  # ← O el otro
```

**Problema:**
- **Uso mutuamente excluyente:** El método `mostrar_temperatura()` solo usa UNO de los dos métodos en cada invocación
- **Decisión en runtime:** La lógica condicional decide qué método llamar
- **Violación LEVE de ISP:** Si un cliente solo necesita mostrar temperatura ambiente, está forzado a depender también de `mostrar_temperatura_deseada`

**Análisis:**
Esta es una **violación menor** porque:
- Los dos métodos están relacionados (ambos muestran temperatura)
- El gestor eventualmente usa ambos métodos (en diferentes contextos)
- Segregar más esta interfaz podría resultar en sobre-ingeniería

Sin embargo, podría mejorarse si hubiera clientes que realmente solo necesitan uno de los dos métodos.

**Recomendación (opcional):** Si hay clientes que solo usan uno de los métodos:

```python
# Interfaces segregadas
class InterfazVisualizadorTemperaturaAmbiente(ABC):
    @abstractmethod
    def mostrar_temperatura_ambiente(self, temperatura): pass

class InterfazVisualizadorTemperaturaDeseada(ABC):
    @abstractmethod
    def mostrar_temperatura_deseada(self, temperatura): pass

# La implementación completa implementa ambas
class VisualizadorTemperatura(
    InterfazVisualizadorTemperaturaAmbiente,
    InterfazVisualizadorTemperaturaDeseada
):
    def mostrar_temperatura_ambiente(self, temperatura):
        print(f"Ambiente: {temperatura}")

    def mostrar_temperatura_deseada(self, temperatura):
        print(f"Deseada: {temperatura}")

# Clientes especializados pueden depender solo de lo que necesitan
def mostrar_solo_ambiente(visualizador: InterfazVisualizadorTemperaturaAmbiente):
    visualizador.mostrar_temperatura_ambiente(25.0)
```

**Nota:** Esta segregación solo vale la pena si hay clientes reales que usen solo una parte. En el estado actual del proyecto, **no es necesaria** porque GestorAmbiente eventualmente usa ambos métodos.

---

## 🟡 VIOLACIONES MENORES

### 6. **AbsVisualizadorBateria - Similar a AbsVisualizadorTemperatura**

**Archivos afectados:**
- `entidades/abs_visualizador_bateria.py:8-18`
- `gestores_entidades/gestor_bateria.py:38-44`

#### Interfaz:

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

#### Uso en GestorBateria:

```python
def mostrar_nivel_de_carga(self):
    self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)  # ← Solo usa este

def mostrar_indicador_de_carga(self):
    self._visualizador_bateria.mostrar_indicador(self._bateria.indicador)  # ← Solo usa este
```

**Problema:**
- **Métodos separados usan métodos separados:** `mostrar_nivel_de_carga()` solo usa `mostrar_tension()`, `mostrar_indicador_de_carga()` solo usa `mostrar_indicador()`
- **Uso independiente:** Los dos métodos se usan en contextos diferentes
- **Violación LEVE de ISP:** Similar al caso de temperatura

**Análisis:**
- Los métodos están relacionados (ambos visualizan aspectos de la batería)
- El gestor usa ambos métodos (aunque en llamadas separadas)
- Segregar podría ser sobre-ingeniería

**Recomendación:** Mismo análisis que `AbsVisualizadorTemperatura`. Solo segregar si hay clientes que realmente necesitan solo una parte.

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Componentes Afectados | Tipo de Violación |
|-----------|----------|----------------------|-------------------|
| 🔴 Crítica | 2 | SelectorTemperaturaArchivo, ActuadorClimatizadorGeneral | Herencia forzada de cross-cutting concerns |
| 🟠 Moderada | 3 | Presentador, OperadorParalelo, gestores | Dependencia de interfaces grandes (uso < 50%) |
| 🟡 Menor | 2 | AbsVisualizadorTemperatura, AbsVisualizadorBateria | Interfaces con métodos relacionados usados selectivamente |
| **TOTAL** | **7** | **10+ clases** | **Interfaces no segregadas** |

---

## 💡 Patrones de Violación Identificados

### Patrón 1: Cross-Cutting Concerns Mezclados con Herencia

**Clases afectadas:** SelectorTemperaturaArchivo, ActuadorClimatizadorGeneral

**Causa raíz:** Uso de herencia múltiple para agregar funcionalidad ortogonal (logging, auditoría, registro de errores)

**Problema:**
- Las interfaces de cross-cutting concerns (AbsRegistrador, AbsAuditor) se mezclan con las interfaces de dominio
- Diferentes implementaciones tienen diferentes jerarquías de herencia
- Forzado a implementar métodos que pueden no ser necesarios

**Solución recomendada:**
```python
# ❌ Antes: Herencia múltiple
class ActuadorClimatizador(AbsActuadorClimatizador, AbsRegistrador, AbsAuditor):
    pass

# ✅ Después: Decorator Pattern o Dependency Injection
class ActuadorClimatizador(AbsActuadorClimatizador):
    def __init__(self, registrador=None, auditor=None):
        self._registrador = registrador
        self._auditor = auditor

# O usar Decorators:
actuador = ActuadorConAuditoria(
    ActuadorConRegistro(
        ActuadorClimatizadorSimple()
    )
)
```

### Patrón 2: Clientes que Dependen de Interfaces Grandes

**Clases afectadas:** Presentador, OperadorParalelo

**Causa raíz:** Clientes reciben objetos completos (gestores) cuando solo necesitan un subconjunto de funcionalidad

**Problema:**
- Acoplamiento alto: clientes dependen de toda la interfaz del gestor
- Testing complejo: necesitas mockear toda la interfaz
- Dificulta entender las dependencias reales
- Violación del principio de mínimo conocimiento

**Solución recomendada:**
```python
# ❌ Antes: Dependencia de gestor completo
class Presentador:
    def __init__(self, gestor_bateria: GestorBateria):  # 5 métodos
        self._gestor = gestor_bateria

    def ejecutar(self):
        self._gestor.mostrar_nivel_de_carga()  # Usa solo 2 de 5 métodos

# ✅ Después: Interface segregada
class InterfazPresentacionBateria(ABC):
    @abstractmethod
    def mostrar_nivel_de_carga(self): pass

    @abstractmethod
    def mostrar_indicador_de_carga(self): pass

class Presentador:
    def __init__(self, presentacion: InterfazPresentacionBateria):
        self._presentacion = presentacion

    def ejecutar(self):
        self._presentacion.mostrar_nivel_de_carga()

# GestorBateria implementa múltiples interfaces
class GestorBateria(InterfazPresentacionBateria, InterfazLecturaBateria, ...):
    pass
```

### Patrón 3: Interfaces con Métodos Relacionados pero Usados Selectivamente

**Clases afectadas:** AbsVisualizadorTemperatura, AbsVisualizadorBateria

**Causa raíz:** Interfaces que agrupan métodos relacionados pero que se usan en diferentes contextos

**Problema:**
- Métodos relacionados semánticamente pero usados de forma independiente
- Lógica condicional decide qué método usar en runtime
- Clientes potenciales podrían necesitar solo un subconjunto

**Solución (si hay clientes que solo usan una parte):**
```python
# Segregar solo si hay necesidad real
class InterfazVisualizadorTemperaturaAmbiente(ABC):
    @abstractmethod
    def mostrar_temperatura_ambiente(self, temp): pass

class InterfazVisualizadorTemperaturaDeseada(ABC):
    @abstractmethod
    def mostrar_temperatura_deseada(self, temp): pass

# Implementación completa implementa ambas
class VisualizadorTemperatura(
    InterfazVisualizadorTemperaturaAmbiente,
    InterfazVisualizadorTemperaturaDeseada
):
    pass
```

---

## 📋 Plan de Acción Priorizado

### Fase 1: Eliminar Cross-Cutting Concerns de Interfaces (Prioridad Crítica)

**Objetivo:** Separar registro de errores y auditoría de las interfaces de dominio

**Componentes a refactorizar:**
1. `SelectorTemperaturaArchivo` - Remover herencia de `AbsRegistrador`
2. `ActuadorClimatizadorGeneral` - Remover herencia de `AbsRegistrador` y `AbsAuditor`

**Estrategia:** Usar **Dependency Injection** para inyectar registrador y auditor

**Pasos:**
1. Crear clases concretas `RegistradorErrores` y `Auditor`
2. Modificar constructores para aceptar dependencias opcionales:
   ```python
   def __init__(self, registrador=None, auditor=None):
       self._registrador = registrador or RegistradorErrores()
       self._auditor = auditor or Auditor()
   ```
3. Reemplazar llamadas a métodos estáticos por llamadas a instancias inyectadas
4. Remover herencias de `AbsRegistrador` y `AbsAuditor`
5. Actualizar factories para inyectar dependencias si es necesario
6. Actualizar tests

**Esfuerzo estimado:** 4-6 horas

**Beneficios:**
- Interfaces limpias enfocadas en responsabilidad principal
- Cross-cutting concerns configurables y reutilizables
- Testing más simple
- Consistencia entre implementaciones

---

### Fase 2: Crear Interfaces Segregadas para Presentador (Prioridad Alta)

**Objetivo:** Reducir acoplamiento de Presentador con gestores completos

**Componentes a refactorizar:**
1. Crear `InterfazPresentacionBateria` con métodos de visualización
2. Crear `InterfazPresentacionTemperatura` con método de visualización
3. Crear `InterfazPresentacionClimatizador` con método de visualización
4. Modificar `Presentador` para depender de interfaces segregadas
5. Hacer que `GestorBateria`, `GestorAmbiente`, `GestorClimatizador` implementen las nuevas interfaces

**Pasos:**
1. Definir interfaces pequeñas en `servicios_aplicacion/interfaces_presentacion.py`:
   ```python
   class InterfazPresentacionBateria(ABC):
       @abstractmethod
       def mostrar_nivel_de_carga(self): pass

       @abstractmethod
       def mostrar_indicador_de_carga(self): pass

   # ... otras interfaces
   ```

2. Modificar gestores para implementar las interfaces:
   ```python
   class GestorBateria(InterfazPresentacionBateria):
       # Implementación existente
       pass
   ```

3. Modificar constructor de `Presentador`:
   ```python
   def __init__(self,
                bateria: InterfazPresentacionBateria,
                temperatura: InterfazPresentacionTemperatura,
                climatizador: InterfazPresentacionClimatizador):
       self._bateria = bateria
       # ...
   ```

4. Actualizar creación de `Presentador` en `OperadorParalelo`
5. Actualizar tests

**Esfuerzo estimado:** 3-4 horas

**Beneficios:**
- Presentador solo ve los métodos que necesita
- Bajo acoplamiento
- Testing simple con interfaces pequeñas
- Documentación clara de dependencias

---

### Fase 3: Crear Interfaces Segregadas para OperadorParalelo (Prioridad Media)

**Objetivo:** Reducir acoplamiento de tareas paralelas con gestores completos

**Componentes a refactorizar:**
1. Crear interfaces específicas por tarea paralela
2. Modificar `OperadorParalelo` para usar interfaces segregadas o callbacks

**Opción A - Interfaces segregadas:**
```python
class InterfazLecturaBateria(ABC):
    @abstractmethod
    def verificar_nivel_de_carga(self): pass

class InterfazLecturaTemperatura(ABC):
    @abstractmethod
    def leer_temperatura_ambiente(self): pass

# ... modificar OperadorParalelo
```

**Opción B - Callbacks (más simple):**
```python
class OperadorParalelo:
    def __init__(self,
                 verificar_bateria: Callable[[], None],
                 leer_temperatura: Callable[[], None],
                 accionar_climatizador: Callable[[Ambiente], None],
                 presentador,
                 selector):
        # ...
```

**Recomendación:** Opción B (callbacks) es más simple y suficiente para este caso

**Esfuerzo estimado:** 2-3 horas

---

### Fase 4: Documentar Interfaces (Prioridad Baja)

**Objetivo:** Documentar claramente el propósito de cada interfaz

**Pasos:**
1. Agregar docstrings completos a todas las interfaces abstractas
2. Documentar qué clientes usan qué interfaces
3. Crear diagrama de dependencias de interfaces

**Esfuerzo estimado:** 2 horas

---

### Resumen de Esfuerzo

| Fase | Prioridad | Componentes | Esfuerzo estimado |
|------|-----------|-------------|-------------------|
| Fase 1 | Crítica | Cross-cutting concerns | 4-6 horas |
| Fase 2 | Alta | Presentador | 3-4 horas |
| Fase 3 | Media | OperadorParalelo | 2-3 horas |
| Fase 4 | Baja | Documentación | 2 horas |
| **TOTAL** | | | **11-15 horas** |

---

## 🎯 Ejemplos de Refactoring Completo

### Ejemplo 1: Refactoring de ActuadorClimatizadorGeneral

#### Antes (Viola ISP):

```python
# actuador_climatizador.py
class ActuadorClimatizadorGeneral(AbsActuadorClimatizador, AbsRegistrador, AbsAuditor):
    # ❌ Herencia de 3 interfaces

    @staticmethod
    def accionar_climatizador(accion):
        # Auditoría hardcodeada
        ActuadorClimatizadorGeneral.auditar_funcion(...)

        try:
            with open("climatizador", "w") as archivo:
                archivo.write(accion)
        except IOError:
            # Registro hardcodeado
            ActuadorClimatizadorGeneral.registrar_error(...)

    @staticmethod
    def registrar_error(registro):
        # Implementación de logging
        pass

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        # Implementación de auditoría
        pass
```

#### Después (Cumple ISP):

```python
# registrador/registrador_errores.py
class RegistradorErrores:
    """Servicio para registrar errores del sistema"""

    def registrar_error(self, clase, metodo, error):
        registro = self._armar_registro(clase, metodo, error)
        with open("registro_errores", "a") as archivo:
            archivo.write(registro)

    def _armar_registro(self, clase, metodo, error):
        # Formato de registro
        return f"ERROR: {clase}.{metodo} - {error}\n"

# registrador/auditor.py
class Auditor:
    """Servicio para auditar operaciones del sistema"""

    def auditar_funcion(self, clase, mensaje, fecha_hora):
        registro = f"AUDIT: {fecha_hora} - {clase}: {mensaje}\n"
        with open("registro_auditoria", "a") as archivo:
            archivo.write(registro)

# agentes_actuadores/actuador_climatizador.py
class ActuadorClimatizadorGeneral(AbsActuadorClimatizador):
    # ✅ Solo hereda de la interfaz principal

    def __init__(self, registrador=None, auditor=None):
        """
        Args:
            registrador: Opcional. Servicio para registrar errores
            auditor: Opcional. Servicio para auditar operaciones
        """
        self._registrador = registrador or RegistradorErrores()
        self._auditor = auditor or Auditor()

    def accionar_climatizador(self, accion):
        # Auditoría inyectada
        self._auditor.auditar_funcion(
            self.__class__.__name__,
            "accionando el climatizador",
            str(datetime.datetime.now())
        )

        try:
            with open("climatizador", "w") as archivo:
                archivo.write(accion)
        except IOError as e:
            # Registro inyectado
            self._registrador.registrar_error(
                self.__class__.__name__,
                "accionar_climatizador",
                str(e)
            )
            raise

# Factory actualizada
class FactoryActuadorClimatizador:
    @staticmethod
    def crear(tipo: str, registrador=None, auditor=None) -> AbsActuadorClimatizador:
        if tipo == "general":
            return ActuadorClimatizadorGeneral(registrador, auditor)
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")

# Testing simple
def test_actuador_sin_dependencias():
    # Mock de dependencias
    mock_registrador = Mock()
    mock_auditor = Mock()

    actuador = ActuadorClimatizadorGeneral(mock_registrador, mock_auditor)
    actuador.accionar_climatizador("enfriar")

    # Verificar que se llamó a auditoría
    mock_auditor.auditar_funcion.assert_called_once()
```

### Ejemplo 2: Refactoring de Presentador

#### Antes (Viola ISP):

```python
class Presentador:
    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        # ❌ Depende de gestores completos (muchos métodos)
        self._gestor_bateria = gestor_bateria  # 5 métodos, usa 2
        self._gestor_ambiente = gestor_ambiente  # 9 métodos, usa 1
        self._gestor_climatizador = gestor_climatizador  # 3 métodos, usa 1

    def ejecutar(self):
        print("-------------- BATERIA -------------")
        self._gestor_bateria.mostrar_nivel_de_carga()
        self._gestor_bateria.mostrar_indicador_de_carga()
        # ...
```

#### Después (Cumple ISP):

```python
# servicios_aplicacion/interfaces_presentacion.py
"""Interfaces segregadas para presentación"""

class InterfazPresentacionBateria(ABC):
    """Interfaz mínima para presentar estado de batería"""

    @abstractmethod
    def mostrar_nivel_de_carga(self) -> None:
        """Muestra el nivel de carga actual"""
        pass

    @abstractmethod
    def mostrar_indicador_de_carga(self) -> None:
        """Muestra el indicador de carga (NORMAL/BAJA)"""
        pass

class InterfazPresentacionTemperatura(ABC):
    """Interfaz mínima para presentar temperatura"""

    @abstractmethod
    def mostrar_temperatura(self) -> None:
        """Muestra la temperatura según configuración actual"""
        pass

class InterfazPresentacionClimatizador(ABC):
    """Interfaz mínima para presentar estado de climatizador"""

    @abstractmethod
    def mostrar_estado_climatizador(self) -> None:
        """Muestra el estado actual del climatizador"""
        pass

# gestores_entidades/gestor_bateria.py
class GestorBateria(InterfazPresentacionBateria):
    # ✅ Implementa interfaz de presentación + otros métodos

    # Métodos de InterfazPresentacionBateria
    def mostrar_nivel_de_carga(self):
        self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)

    def mostrar_indicador_de_carga(self):
        self._visualizador_bateria.mostrar_indicador(self._bateria.indicador)

    # Otros métodos (no en la interfaz de presentación)
    def verificar_nivel_de_carga(self):
        self._bateria.nivel_de_carga = self._proxy_bateria.leer_carga()

    def obtener_nivel_de_carga(self):
        return self._bateria.nivel_de_carga
    # ...

# servicios_aplicacion/presentador.py
class Presentador:
    def __init__(self,
                 bateria: InterfazPresentacionBateria,
                 temperatura: InterfazPresentacionTemperatura,
                 climatizador: InterfazPresentacionClimatizador):
        """
        Presenta el estado del sistema al usuario.

        Args:
            bateria: Interfaz para presentar estado de batería
            temperatura: Interfaz para presentar temperatura
            climatizador: Interfaz para presentar estado de climatizador
        """
        # ✅ Depende solo de interfaces mínimas
        self._bateria = bateria
        self._temperatura = temperatura
        self._climatizador = climatizador

    def ejecutar(self):
        print("-------------- BATERIA -------------")
        self._bateria.mostrar_nivel_de_carga()
        self._bateria.mostrar_indicador_de_carga()

        print("------------ TEMPERATURA ----------")
        self._temperatura.mostrar_temperatura()

        print("------------ CLIMATIZADOR ----------")
        self._climatizador.mostrar_estado_climatizador()

# Creación (el código cliente pasa los gestores completos)
gestor_bateria = GestorBateria()
gestor_ambiente = GestorAmbiente()
gestor_climatizador = GestorClimatizador()

# ✅ Los gestores implementan las interfaces, por lo que funcionan
presentador = Presentador(gestor_bateria, gestor_ambiente, gestor_climatizador)

# Testing simple
def test_presentador():
    # Mock solo las interfaces pequeñas
    mock_bateria = Mock(spec=InterfazPresentacionBateria)
    mock_temperatura = Mock(spec=InterfazPresentacionTemperatura)
    mock_climatizador = Mock(spec=InterfazPresentacionClimatizador)

    presentador = Presentador(mock_bateria, mock_temperatura, mock_climatizador)
    presentador.ejecutar()

    # Verificar llamadas
    mock_bateria.mostrar_nivel_de_carga.assert_called_once()
    mock_bateria.mostrar_indicador_de_carga.assert_called_once()
    mock_temperatura.mostrar_temperatura.assert_called_once()
    mock_climatizador.mostrar_estado_climatizador.assert_called_once()
```

---

## 🔍 Indicadores de Éxito

Después del refactoring, estas condiciones deberían cumplirse:

1. ✅ **Sin herencia forzada de cross-cutting concerns:**
   ```python
   # Todas las clases heredan solo de su interfaz principal
   class Actuador(AbsActuadorClimatizador):  # NO hereda AbsRegistrador ni AbsAuditor
       pass
   ```

2. ✅ **Clientes dependen de interfaces mínimas:**
   ```python
   # Presentador solo ve los métodos que usa
   class Presentador:
       def __init__(self, bateria: InterfazPresentacionBateria):  # 2 métodos
           self._bateria = bateria  # NO GestorBateria con 5 métodos
   ```

3. ✅ **Testing simple con mocks mínimos:**
   ```python
   # Mock solo la interfaz pequeña
   mock = Mock(spec=InterfazPresentacionBateria)
   presentador = Presentador(mock)
   ```

4. ✅ **Interfaces cohesivas:**
   ```python
   # Cada interfaz tiene un propósito claro y específico
   class InterfazPresentacionBateria(ABC):  # Solo presentación
       @abstractmethod
       def mostrar_nivel_de_carga(self): pass
   ```

5. ✅ **Sin métodos no implementados en clases concretas:**
   ```bash
   # No hay métodos con pass, NotImplementedError, etc.
   $ grep -r "NotImplementedError" agentes_*/
   # Sin resultados
   ```

6. ✅ **Documentación clara de dependencias:**
   ```python
   # Type hints claros que muestran exactamente qué se necesita
   def __init__(self, bateria: InterfazPresentacionBateria):
       """
       Args:
           bateria: Interfaz para presentar estado de batería
                   (solo necesita métodos de visualización)
       """
   ```

---

## 🎯 Conclusión

El proyecto presenta **7 violaciones del ISP** que afectan **10+ clases**:

### Problemas Principales:

1. **Cross-cutting concerns mezclados con herencia** (2 clases críticas)
   - `AbsRegistrador` y `AbsAuditor` forzados como interfaces base
   - Inconsistencia entre implementaciones (unas heredan, otras no)
   - Dificulta testing y reutilización

2. **Clientes que dependen de interfaces grandes** (3 clases moderadas)
   - Presentador usa < 50% de los métodos de los gestores
   - OperadorParalelo usa < 35% de los métodos de los gestores
   - Alto acoplamiento innecesario

3. **Interfaces con métodos usados selectivamente** (2 clases menores)
   - Visualizadores tienen 2 métodos relacionados pero usados independientemente
   - No es problema grave en el estado actual

### Impacto:

- **Testing complejo:** Necesitas mockear interfaces grandes incluso cuando solo usas una parte
- **Alto acoplamiento:** Cambios en métodos no usados afectan a clientes
- **Dificulta comprensión:** No está claro qué dependencias realmente necesita cada clase
- **Inconsistencia:** Diferentes implementaciones tienen diferentes interfaces (herencia múltiple)

### Beneficios del Refactoring:

- **Testing simple:** Mocks pequeños y enfocados
- **Bajo acoplamiento:** Clientes solo ven lo que necesitan
- **Claridad:** Interfaces mínimas documentan dependencias reales
- **Consistencia:** Todas las implementaciones tienen la misma estructura
- **Flexibilidad:** Fácil agregar nuevas implementaciones sin funcionalidad extra

### Esfuerzo Total Estimado: 11-15 horas

El refactoring más importante es la **Fase 1** (eliminar cross-cutting concerns de interfaces), ya que tiene el mayor impacto en la arquitectura y consistencia del código.

---

## 📚 Referencias

- **Interface Segregation Principle**: Robert C. Martin, "Agile Software Development, Principles, Patterns, and Practices"
- **SOLID Principles**: Robert C. Martin, "Clean Architecture"
- **Dependency Injection**: Martin Fowler, "Inversion of Control Containers and the Dependency Injection pattern"
- **Decorator Pattern**: Gang of Four, "Design Patterns: Elements of Reusable Object-Oriented Software"
- **Role Interfaces**: Martin Fowler, "Patterns of Enterprise Application Architecture"

---

**Documento generado automáticamente mediante análisis estático del código.**
