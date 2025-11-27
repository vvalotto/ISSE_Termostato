# Análisis de Violaciones del Principio OCP (Open/Closed Principle)

**Proyecto:** ISSE_Termostato
**Fecha:** Noviembre 2025
**Análisis realizado por:** Claude Code

---

## Definición del Principio OCP

> "Las entidades de software (clases, módulos, funciones, etc.) deben estar **abiertas para extensión** pero **cerradas para modificación**."
> — Bertrand Meyer

**En otras palabras:** Deberíamos poder agregar nueva funcionalidad sin modificar el código existente.

---

## 🔴 VIOLACIONES CRÍTICAS

### 1. **Todas las Factories usan if/elif (Pattern de Violación Repetido)**

**Archivos afectados:** 9 factories en `configurador/`

#### 1.1 FactoryVisualizadorTemperatura (`factory_visualizador_temperatura.py:13-20`)

```python
if tipo == "archivo":
    return VisualizadorTemperatura()
elif tipo == "socket":
    return VisualizadorTemperaturaSocket()
elif tipo == "api":
    return VisualizadorTemperaturaApi()
else:
    return None
```

**Problema:** Para agregar un nuevo tipo de visualizador (ej: "mqtt", "redis", "kafka"), hay que **modificar** esta clase.

**Impacto:**
- Cada nuevo tipo requiere modificar la factory
- Viola OCP directamente
- Se repite en las 9 factories del sistema

**Factories afectadas:**
1. `FactoryVisualizadorTemperatura` (3 tipos: archivo, socket, api)
2. `FactoryVisualizadorBateria` (3 tipos: archivo, socket, api)
3. `FactoryVisualizadorClimatizador` (3 tipos: archivo, socket, api)
4. `FactoryProxySensorTemperatura` (2 tipos: archivo, socket)
5. `FactoryProxyBateria` (2 tipos: archivo, socket)
6. `FactorySelectorTemperatura` (2 tipos: archivo, socket)
7. `FactorySeteoTemperatura` (2 tipos: consola, socket)
8. `FactoryClimatizador` (2 tipos: climatizador, calefactor)
9. `FactoryActuadorClimatizador` (1 tipo: general)

**Recomendación:** Usar **Registry Pattern** o **Reflection/Introspection**

```python
# Solución propuesta con Registry Pattern
class FactoryVisualizadorTemperatura:
    _registry = {}

    @classmethod
    def register(cls, tipo: str, clase):
        cls._registry[tipo] = clase

    @classmethod
    def crear(cls, tipo: str):
        clase = cls._registry.get(tipo)
        if clase is None:
            raise ValueError(f"Tipo '{tipo}' no registrado")
        return clase()

# Uso (fuera de la factory):
FactoryVisualizadorTemperatura.register("archivo", VisualizadorTemperatura)
FactoryVisualizadorTemperatura.register("socket", VisualizadorTemperaturaSocket)
FactoryVisualizadorTemperatura.register("api", VisualizadorTemperaturaApi)
# Para agregar nuevo tipo, solo agregar una línea (extensión sin modificación):
FactoryVisualizadorTemperatura.register("mqtt", VisualizadorTemperaturaMqtt)
```

---

### 2. **Configurador - Lista Hardcodeada de Claves Requeridas** (`configurador.py:121-129`)

```python
claves_requeridas = [
    "proxy_bateria", "proxy_sensor_temperatura", "climatizador",
    "actuador_climatizador", "selector_temperatura", "seteo_temperatura",
    "visualizador_bateria", "visualizador_temperatura", "visualizador_climatizador"
]

for clave in claves_requeridas:
    if clave not in config:
        raise Exception("ERROR: Falta la clave '{}' en termostato.json".format(clave))
```

**Problema:** Para agregar un nuevo componente configurable (ej: "proxy_humedad", "sensor_co2"), hay que **modificar** esta lista.

**Impacto:**
- No extensible a nuevos sensores o actuadores
- Viola OCP
- Acoplamiento fuerte con componentes específicos

**Recomendación:** Usar **Schema Validation** o **Configuración basada en Componentes Registrados**

```python
# Solución 1: Validación basada en schema
import jsonschema

SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^proxy_.*": {"type": "string"},
        "^visualizador_.*": {"type": "string"},
        "^actuador_.*": {"type": "string"}
    }
}

# Solución 2: Auto-discovery de componentes requeridos
class Configurador:
    _componentes_requeridos = set()

    @classmethod
    def registrar_componente_requerido(cls, nombre):
        cls._componentes_requeridos.add(nombre)

    @staticmethod
    def _validar_configuracion():
        for componente in Configurador._componentes_requeridos:
            if componente not in config:
                raise Exception(f"Falta componente: {componente}")
```

---

## 🟠 VIOLACIONES MODERADAS

### 3. **GestorAmbiente.mostrar_temperatura()** (`gestor_ambiente.py:53-57`)

```python
def mostrar_temperatura(self):
    if self._ambiente.temperatura_a_mostrar == "ambiente":
        self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_ambiente)
    elif self._ambiente.temperatura_a_mostrar == "deseada":
        self._visualizador_temperatura.mostrar_temperatura_deseada(self._ambiente.temperatura_deseada)
```

**Problema:** Para agregar un nuevo tipo de temperatura a mostrar (ej: "promedio", "minima", "maxima"), hay que **modificar** este método.

**Impacto:**
- No extensible sin modificación
- Lógica condicional basada en strings

**Recomendación:** Usar **Strategy Pattern** o **Command Pattern**

```python
# Solución con Strategy Pattern
class EstrategiaVisualizacionTemperatura(ABC):
    @abstractmethod
    def visualizar(self, ambiente, visualizador):
        pass

class VisualizarAmbiente(EstrategiaVisualizacionTemperatura):
    def visualizar(self, ambiente, visualizador):
        visualizador.mostrar_temperatura_ambiente(ambiente.temperatura_ambiente)

class VisualizarDeseada(EstrategiaVisualizacionTemperatura):
    def visualizar(self, ambiente, visualizador):
        visualizador.mostrar_temperatura_deseada(ambiente.temperatura_deseada)

# En GestorAmbiente:
def mostrar_temperatura(self):
    estrategia = self._estrategias[self._ambiente.temperatura_a_mostrar]
    estrategia.visualizar(self._ambiente, self._visualizador_temperatura)
```

---

### 4. **Climatizador._definir_accion()** (`climatizador.py:62-79`)

```python
def _definir_accion(self, temperatura):
    accion = None
    if temperatura == "alta":
        if self._estado == "apagado":
            accion = "enfriar"
        elif self._estado == "calentando":
            accion = "apagar"
        else:
            accion = None
    if temperatura == "baja":
        if self._estado == "apagado":
            accion = "calentar"
        elif self._estado == "enfriando":
            accion = "apagar"
        else:
            accion = None
    return accion
```

**Problema:** Lógica de transición hardcodeada. Para cambiar el comportamiento o agregar nuevos estados/acciones, hay que **modificar** este método.

**Impacto:**
- Lógica condicional compleja
- Difícil de extender con nuevas reglas
- Estado y lógica entrelazados

**Recomendación:** Usar **State Pattern** puro con objetos de estado

```python
# Solución con State Pattern
class EstadoClimatizador(ABC):
    @abstractmethod
    def definir_accion(self, temperatura):
        pass

class EstadoApagado(EstadoClimatizador):
    def definir_accion(self, temperatura):
        if temperatura == "alta":
            return "enfriar"
        elif temperatura == "baja":
            return "calentar"
        return None

class EstadoCalentando(EstadoClimatizador):
    def definir_accion(self, temperatura):
        if temperatura == "alta":
            return "apagar"
        return None

# En Climatizador:
def _definir_accion(self, temperatura):
    return self._estado_actual.definir_accion(temperatura)
```

---

### 5. **SelectorEntradaTemperatura._obtener_seteo_temperatura_deseada()** (`selector_entrada.py:36-46`)

```python
def _obtener_seteo_temperatura_deseada(self):
    opcion = self._seteo_temperatura.obtener_seteo()

    if opcion is None:
        return

    if opcion == "aumentar":
        self._gestor_ambiente.aumentar_temperatura_deseada()
    if opcion == "disminuir":
        self._gestor_ambiente.disminuir_temperatura_deseada()
```

**Problema:** Para agregar nuevas opciones (ej: "resetear", "modo_eco", "modo_turbo"), hay que **modificar** este método.

**Impacto:**
- Condicionales basados en strings
- No extensible

**Recomendación:** Usar **Command Pattern** con diccionario de comandos

```python
# Solución con Command Pattern
class ComandoTemperatura(ABC):
    @abstractmethod
    def ejecutar(self, gestor_ambiente):
        pass

class ComandoAumentar(ComandoTemperatura):
    def ejecutar(self, gestor_ambiente):
        gestor_ambiente.aumentar_temperatura_deseada()

class ComandoDisminuir(ComandoTemperatura):
    def ejecutar(self, gestor_ambiente):
        gestor_ambiente.disminuir_temperatura_deseada()

# En SelectorEntradaTemperatura:
def __init__(self, gestor_ambiente):
    self._comandos = {
        "aumentar": ComandoAumentar(),
        "disminuir": ComandoDisminuir()
    }

def _obtener_seteo_temperatura_deseada(self):
    opcion = self._seteo_temperatura.obtener_seteo()
    if opcion and opcion in self._comandos:
        self._comandos[opcion].ejecutar(self._gestor_ambiente)
```

---

## 🟡 VIOLACIONES MENORES

### 6. **Valores Hardcodeados de Puertos en Visualizadores Socket**

**Archivos afectados:**
- `VisualizadorTemperaturaSocket` (`visualizador_temperatura.py:30,42`) - Puerto 14001
- `VisualizadorBateriaSocket` (`visualizador_bateria.py:30,42`) - Puertos 14000, 13005
- `VisualizadorClimatizadorSocket` (`visualizador_climatizador.py:24`) - Puerto 14002

```python
# Ejemplo en VisualizadorTemperaturaSocket
direccion_servidor = ("localhost", 14001)  # Hardcoded!
```

**Problema:** Para cambiar el puerto o agregar configuración de host, hay que **modificar** estas clases.

**Impacto:**
- No configurable sin modificación de código
- Dificulta testing y deployment

**Recomendación:** Inyectar configuración o usar Configurador

```python
# Solución:
class VisualizadorTemperaturaSocket(AbsVisualizadorTemperatura):
    def __init__(self, host="localhost", puerto=14001):
        self._host = host
        self._puerto = puerto

    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        direccion_servidor = (self._host, self._puerto)
        # ... resto del código
```

---

### 7. **Bateria - Cálculo de Indicador en Setter** (`bateria.py:17-23`)

```python
@nivel_de_carga.setter
def nivel_de_carga(self, valor):
    if valor <= self.__carga_maxima * self.__umbral_de_carga:
        self.__indicador = "BAJA"
        self.__nivel_de_carga = valor
    else:
        self.__indicador = "NORMAL"
    self.__nivel_de_carga = valor
```

**Problema:** La lógica de cálculo está hardcodeada. Para cambiar el algoritmo (ej: agregar estado "CRÍTICA", usar múltiples umbrales), hay que **modificar** la clase.

**Impacto:**
- Algoritmo no extensible
- Lógica de negocio en setter

**Recomendación:** Extraer cálculo a un **Strategy** o **Servicio de Dominio**

```python
# Solución con Strategy
class CalculadorIndicadorBateria(ABC):
    @abstractmethod
    def calcular(self, nivel, carga_maxima, umbral):
        pass

class CalculadorIndicadorSimple(CalculadorIndicadorBateria):
    def calcular(self, nivel, carga_maxima, umbral):
        return "BAJA" if nivel <= carga_maxima * umbral else "NORMAL"

class CalculadorIndicadorAvanzado(CalculadorIndicadorBateria):
    def calcular(self, nivel, carga_maxima, umbral):
        porcentaje = nivel / carga_maxima
        if porcentaje < 0.1:
            return "CRÍTICA"
        elif porcentaje < umbral:
            return "BAJA"
        else:
            return "NORMAL"

# En Bateria:
def __init__(self, carga_maxima, umbral, calculador=CalculadorIndicadorSimple()):
    self._calculador_indicador = calculador

@nivel_de_carga.setter
def nivel_de_carga(self, valor):
    self.__nivel_de_carga = valor
    self.__indicador = self._calculador_indicador.calcular(
        valor, self.__carga_maxima, self.__umbral_de_carga
    )
```

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Componentes Afectados | Esfuerzo Estimado |
|-----------|----------|----------------------|-------------------|
| 🔴 Crítica | 2 | 9 Factories + Configurador._validar_configuracion | 8-12 horas |
| 🟠 Moderada | 3 | GestorAmbiente, Climatizador, SelectorEntradaTemperatura | 6-8 horas |
| 🟡 Menor | 2 | Visualizadores Socket, Bateria | 2-4 horas |
| **TOTAL** | **7** | **15+ clases** | **16-24 horas** |

---

## 💡 Patrones de Diseño Recomendados

### Para Factories (Crítico)
- ✅ **Registry Pattern**: Registro dinámico de tipos
- ✅ **Reflection/Introspection**: Descubrimiento automático de clases
- ✅ **Plugin Architecture**: Carga dinámica de implementaciones

### Para Lógica Condicional (Moderado)
- ✅ **Strategy Pattern**: Algoritmos intercambiables
- ✅ **State Pattern**: Comportamiento basado en estado
- ✅ **Command Pattern**: Encapsular acciones como objetos

### Para Configuración (Crítico)
- ✅ **Schema Validation**: Validación flexible con JSON Schema
- ✅ **Component Registry**: Auto-discovery de componentes requeridos

---

## 📋 Plan de Acción Priorizado

### Fase 1: Factories (Prioridad Alta)

**Objetivo:** Eliminar if/elif de las 9 factories usando Registry Pattern

**Pasos:**
1. Crear clase base `RegistryFactory` con registro dinámico
2. Migrar todas las factories a usar el nuevo patrón
3. Mover registros a un módulo de inicialización
4. Actualizar tests

**Beneficios:**
- Agregar nuevos tipos sin modificar código existente
- Extensibilidad mediante plugins
- Mejor testabilidad

**Esfuerzo:** 8-12 horas

---

### Fase 2: Configurador (Prioridad Alta)

**Objetivo:** Hacer validación extensible

**Pasos:**
1. Implementar auto-discovery de componentes requeridos
2. Permitir registro dinámico de validadores
3. Usar JSON Schema para validación flexible

**Beneficios:**
- Nuevos componentes no requieren cambios en validación
- Configuración más flexible

**Esfuerzo:** 3-4 horas

---

### Fase 3: Lógica Condicional (Prioridad Media)

**Objetivo:** Eliminar if/elif basados en strings

**Componentes a refactorizar:**
1. `GestorAmbiente.mostrar_temperatura()` → Strategy Pattern
2. `Climatizador._definir_accion()` → State Pattern mejorado
3. `SelectorEntradaTemperatura` → Command Pattern

**Esfuerzo:** 6-8 horas

---

### Fase 4: Valores Hardcodeados (Prioridad Baja)

**Objetivo:** Hacer configurables puertos y parámetros

**Componentes:**
- Visualizadores Socket (puertos hardcodeados)
- Bateria (algoritmo de indicador)

**Esfuerzo:** 2-4 horas

---

## 🎯 Ejemplos de Extensión Sin Modificación

### Antes (Violación OCP)

```python
# Para agregar MQTT como visualizador:
# 1. Crear clase VisualizadorTemperaturaMqtt
# 2. MODIFICAR factory_visualizador_temperatura.py:
elif tipo == "mqtt":  # ← Modificación!
    return VisualizadorTemperaturaMqtt()
# 3. MODIFICAR configurador.py:
claves_requeridas.append("visualizador_mqtt")  # ← Modificación!
```

### Después (Cumple OCP)

```python
# Para agregar MQTT como visualizador:
# 1. Crear clase VisualizadorTemperaturaMqtt
# 2. Registrar en inicialización (EXTENSIÓN, no modificación):
FactoryVisualizadorTemperatura.register("mqtt", VisualizadorTemperaturaMqtt)
# ¡No hay que modificar ninguna clase existente!
```

---

## 🔍 Indicadores de Éxito

Después del refactoring, estas operaciones deberían ser posibles **sin modificar código existente**:

1. ✅ Agregar nuevo tipo de visualizador (ej: Kafka, RabbitMQ, WebSocket)
2. ✅ Agregar nuevo tipo de proxy (ej: MQTT, Modbus, HTTP)
3. ✅ Agregar nuevas acciones de temperatura (ej: "resetear", "modo_eco")
4. ✅ Cambiar algoritmo de cálculo de indicador de batería
5. ✅ Agregar nuevos tipos de temperatura a mostrar (ej: "promedio", "máxima")
6. ✅ Agregar nuevo componente configurable (ej: sensor de humedad)

---

## 🎯 Conclusión

El proyecto presenta **7 tipos de violaciones del OCP** que afectan principalmente:

### Problemas Principales:
1. **Factories con if/elif** (9 factories afectadas) - Patrón repetido
2. **Configuración hardcodeada** - Lista fija de componentes
3. **Lógica condicional basada en strings** - No extensible

### Impacto:
- Agregar nuevas funcionalidades requiere modificar código existente
- Difícil testear variaciones
- Acoplamiento alto con implementaciones concretas
- Riesgo de regresión al modificar código estable

### Beneficios del Refactoring:
- **Extensibilidad**: Nuevas funcionalidades sin tocar código existente
- **Mantenibilidad**: Menor riesgo de bugs al agregar features
- **Testabilidad**: Fácil agregar tests para nuevas implementaciones
- **Arquitectura de Plugins**: Posibilidad de cargar componentes dinámicamente

---

## 📚 Referencias

- **Open/Closed Principle**: Robert C. Martin, "Agile Software Development"
- **Registry Pattern**: Martin Fowler, "Patterns of Enterprise Application Architecture"
- **Strategy Pattern**: Gang of Four, "Design Patterns: Elements of Reusable Object-Oriented Software"
- **State Pattern**: Gang of Four, "Design Patterns"
- **Command Pattern**: Gang of Four, "Design Patterns"

---

**Documento generado automáticamente mediante análisis estático del código.**
