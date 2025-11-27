qui# Análisis de Violaciones del Principio DIP (Dependency Inversion Principle)

**Proyecto:** ISSE_Termostato
**Fecha:** Noviembre 2025
**Análisis realizado por:** Claude Code

---

## Definición del Principio DIP

> **A. Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.**
>
> **B. Las abstracciones no deben depender de los detalles. Los detalles deben depender de las abstracciones.**
> — Robert C. Martin

**En otras palabras:**
- Las capas superiores de la aplicación (lógica de negocio) no deben conocer detalles de implementación de las capas inferiores (infraestructura)
- Todos deben depender de interfaces/abstracciones
- Las implementaciones concretas se conectan en runtime mediante inyección de dependencias

**Señales de violación del DIP:**
1. Módulos de alto nivel que instancian directamente clases concretas de bajo nivel (`new`, `ClassName()`)
2. Uso de clases estáticas/singleton para acceder a servicios (Service Locator anti-pattern)
3. Imports de clases concretas en lugar de abstracciones
4. Dependencias hardcodeadas que no pueden ser cambiadas sin modificar código
5. Módulos que crean sus propias dependencias en lugar de recibirlas

---

## 🏗️ Capas de la Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│  ALTO NIVEL                                                  │
│                                                              │
│  ejecutar.py  ← Punto de entrada                           │
│       ↓                                                      │
│  servicios_aplicacion/  ← Casos de uso                      │
│       ↓                                                      │
│  gestores_entidades/  ← Coordinación de dominio             │
│       ↓                                                      │
│  entidades/  ← Lógica de dominio pura                       │
│       ↓                                                      │
│  agentes_*/  ← Adaptadores (implementaciones de interfaces) │
│       ↓                                                      │
│  configurador/  ← Infraestructura                           │
│                                                              │
│  BAJO NIVEL                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Regla DIP:** Las flechas de dependencia deben apuntar HACIA ARRIBA (de bajo nivel a alto nivel), no hacia abajo.

---

## 🔴 VIOLACIONES CRÍTICAS

### 1. **Lanzador - Instanciación Directa de Clases Concretas de Alto Nivel**

**Archivo afectado:** `servicios_aplicacion/lanzador.py:12-24`

#### Código Violador:

```python
# lanzador.py
from gestores_entidades.gestor_bateria import *      # ❌ Import de clases concretas
from gestores_entidades.gestor_ambiente import *     # ❌ Import de clases concretas
from gestores_entidades.gestor_climatizador import * # ❌ Import de clases concretas
from servicios_aplicacion.operador_paralelo import *
from servicios_aplicacion.inicializador import *

class Lanzador:

    def __init__(self):
        # ❌ Instanciación directa de clases concretas
        self._gestor_bateria = GestorBateria()
        self._gestor_ambiente = GestorAmbiente()
        self._gestor_climatizador = GestorClimatizador()

        # ❌ Pasa clases concretas, no abstracciones
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)
        self._operador = OperadorParalelo(self._gestor_bateria,
                                          self._gestor_ambiente,
                                          self._gestor_climatizador)
```

**Problema:**
- **Módulo de alto nivel instancia módulos de alto nivel:** `Lanzador` (aplicación) crea directamente `GestorBateria`, `GestorAmbiente`, `GestorClimatizador`
- **Dependencia de clases concretas:** No puede cambiar implementaciones sin modificar código
- **Acoplamiento fuerte:** `Lanzador` conoce los detalles de construcción de los gestores
- **Testing imposible:** No se pueden inyectar mocks o stubs para testing

**Impacto:**
- No se puede testear `Lanzador` sin instanciar todo el sistema real
- No se puede cambiar la implementación de los gestores sin modificar `Lanzador`
- Violación del principio "depende de abstracciones, no de concreciones"
- Dificulta tener múltiples configuraciones (testing, desarrollo, producción)

**Ejemplo de Problema:**

```python
# Para testear Lanzador necesitas:
def test_lanzador():
    lanzador = Lanzador()  # ❌ Crea TODO el sistema real:
                          # - Carga configuración desde archivo
                          # - Crea gestores reales
                          # - Crea proxies reales
                          # - Puede fallar por archivo faltante, socket ocupado, etc.
    lanzador.ejecutar()
```

**Recomendación:** Usar **Inyección de Dependencias** + **Composition Root**

```python
# Solución: Abstracciones + Dependency Injection

# 1. Definir interfaces mínimas (ya existen interfaces, usarlas)
# Ver Análisis ISP para interfaces segregadas

# 2. Lanzador depende de abstracciones
class Lanzador:
    def __init__(self,
                 gestor_bateria: InterfazLecturaBateria,
                 gestor_ambiente: InterfazLecturaTemperatura,
                 gestor_climatizador: InterfazAccionamientoClimatizador,
                 presentador: InterfazPresentador,
                 operador: InterfazOperador):
        # ✅ Recibe dependencias, no las crea
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador
        self._presentador = presentador
        self._operador = operador

    def ejecutar(self):
        todo_ok = Inicializador.iniciar(
            self._gestor_bateria,
            self._gestor_ambiente,
            self._presentador
        )
        if todo_ok:
            self._operador.ejecutar()

# 3. Composition Root (en ejecutar.py o factory)
# Este es el ÚNICO lugar donde se crean objetos concretos
class CompositionRoot:
    @staticmethod
    def crear_aplicacion():
        # Capa de infraestructura
        configurador = Configurador()
        configurador.cargar_configuracion()

        # Capa de adaptadores
        proxy_bateria = configurador.configurar_proxy_bateria()
        proxy_temperatura = configurador.configurar_proxy_temperatura()
        visualizador_bateria = configurador.configurar_visualizador_bateria()
        # ...

        # Capa de dominio (gestores)
        gestor_bateria = GestorBateria(
            proxy_bateria=proxy_bateria,
            visualizador=visualizador_bateria,
            # ... inyectar dependencias
        )
        gestor_ambiente = GestorAmbiente(
            proxy_temperatura=proxy_temperatura,
            # ...
        )
        # ...

        # Capa de aplicación
        presentador = Presentador(gestor_bateria, gestor_ambiente, ...)
        operador = OperadorParalelo(gestor_bateria, gestor_ambiente, ...)

        # Retornar aplicación completamente configurada
        return Lanzador(
            gestor_bateria=gestor_bateria,
            gestor_ambiente=gestor_ambiente,
            gestor_climatizador=gestor_climatizador,
            presentador=presentador,
            operador=operador
        )

# ejecutar.py
if __name__ == "__main__":
    app = CompositionRoot.crear_aplicacion()
    app.ejecutar()

# Testing: Fácil con mocks
def test_lanzador():
    mock_bateria = Mock(spec=InterfazLecturaBateria)
    mock_ambiente = Mock(spec=InterfazLecturaTemperatura)
    mock_climatizador = Mock(spec=InterfazAccionamientoClimatizador)
    mock_presentador = Mock(spec=InterfazPresentador)
    mock_operador = Mock(spec=InterfazOperador)

    lanzador = Lanzador(
        mock_bateria,
        mock_ambiente,
        mock_climatizador,
        mock_presentador,
        mock_operador
    )

    # ✅ Testing aislado sin dependencias reales
    lanzador.ejecutar()
```

---

### 2. **Gestores - Acceso Directo al Configurador Estático (Service Locator Anti-Pattern)**

**Archivos afectados:**
- `gestores_entidades/gestor_bateria.py:12-27`
- `gestores_entidades/gestor_ambiente.py:18-23`
- `gestores_entidades/gestor_climatizador.py:11-14`

#### Violación en GestorBateria:

```python
# gestor_bateria.py
from entidades.bateria import *
from configurador.configurador import *  # ❌ Import de infraestructura

class GestorBateria:

    def __init__(self):
        # ❌ Acceso directo a Configurador estático
        carga_maxima = Configurador.obtener_carga_maxima_bateria()
        umbral = Configurador.obtener_umbral_bateria()
        self._bateria = Bateria(carga_maxima, umbral)

        # ❌ Configurador crea las dependencias (Service Locator)
        self._proxy_bateria = Configurador().configurar_proxy_bateria()
        self._visualizador_bateria = Configurador.configurar_visualizador_bateria()
```

#### Violación en GestorAmbiente:

```python
# gestor_ambiente.py
from entidades.ambiente import *
from configurador.configurador import *  # ❌ Import de infraestructura

class GestorAmbiente:

    def __init__(self):
        # ❌ Acceso directo a Configurador
        temperatura_inicial = Configurador.obtener_temperatura_inicial()
        self._ambiente = Ambiente(temperatura_deseada_inicial=temperatura_inicial)

        # ❌ Configurador crea las dependencias
        self._proxy_sensor_temperatura = Configurador.configurar_proxy_temperatura()
        self._visualizador_temperatura = Configurador().configurar_visualizador_temperatura()
```

#### Violación en GestorClimatizador:

```python
# gestor_climatizador.py
from configurador.configurador import *  # ❌ Import de infraestructura

class GestorClimatizador:

    def __init__(self):
        # ❌ Configurador crea TODAS las dependencias
        self._climatizador = Configurador.configurar_climatizador()
        self._actuador = Configurador.configurar_actuador_climatizador()
        self._visualizador = Configurador.configurar_visualizador_climatizador()
```

**Problema:**
- **Módulos de dominio dependen de infraestructura:** Gestores (dominio) importan y usan `Configurador` (infraestructura)
- **Service Locator anti-pattern:** `Configurador` actúa como un singleton global que localiza servicios
- **Dependencias ocultas:** No está claro qué necesita cada gestor mirando la interfaz
- **Testing imposible:** No se pueden inyectar mocks sin modificar el `Configurador`
- **Violación directa del DIP:** Alto nivel (gestores) depende de bajo nivel (configurador)

**Diagrama de Dependencias (INCORRECTO):**

```
┌──────────────────┐
│ GestorBateria    │ ← Alto nivel (Dominio)
│                  │
│  __init__():     │
│    Configurador. │────┐
│    obtener_...() │    │
└──────────────────┘    │
                        ↓ ❌ DEPENDE DE BAJO NIVEL
                 ┌──────────────┐
                 │ Configurador │ ← Bajo nivel (Infraestructura)
                 │              │
                 │ - Lee JSON   │
                 │ - Crea       │
                 │   objetos    │
                 └──────────────┘
```

**Debería ser (CORRECTO):**

```
┌──────────────────┐          ┌───────────────────┐
│ GestorBateria    │────────→ │ AbsProxyBateria   │ ← Abstracción
│                  │          │ AbsVisualizador   │
│  __init__(       │          └───────────────────┘
│    proxy,        │                    ↑
│    visualizador) │                    │ IMPLEMENTA
└──────────────────┘                    │
                                        │
                                 ┌──────────────┐
                                 │ ProxyBateria │ ← Implementación
                                 │ Socket       │
                                 └──────────────┘

✅ Gestor depende de abstracción, no de implementación
✅ Implementación concreta depende de abstracción (satisface la interfaz)
```

**Impacto:**
- No se puede testear gestores de forma aislada
- Gestores acoplados a la infraestructura de configuración
- Cambiar la forma de configurar requiere modificar todos los gestores
- Violación de capas: dominio conoce infraestructura
- Testing requiere archivo de configuración real

**Ejemplo de Problema:**

```python
# Para testear GestorBateria:
def test_gestor_bateria():
    gestor = GestorBateria()  # ❌ Esto:
                              # 1. Accede a Configurador estático
                              # 2. Lee archivo termostato.json
                              # 3. Crea ProxyBateria real (puede abrir socket!)
                              # 4. Crea VisualizadorBateria real
                              # 5. Puede fallar por archivo faltante, puerto ocupado, etc.

    # No podemos inyectar mocks
    # No podemos controlar las dependencias
```

**Recomendación:** **Constructor Injection** (Inyección por Constructor)

```python
# Solución: Inyectar todas las dependencias

# gestor_bateria.py
from entidades.bateria import Bateria
from entidades.abs_bateria import AbsProxyBateria  # ✅ Abstracción
from entidades.abs_visualizador_bateria import AbsVisualizadorBateria  # ✅ Abstracción

class GestorBateria:

    def __init__(self,
                 proxy_bateria: AbsProxyBateria,
                 visualizador_bateria: AbsVisualizadorBateria,
                 carga_maxima: float,
                 umbral: float):
        """
        Gestor de batería con inyección de dependencias.

        Args:
            proxy_bateria: Abstracción para leer carga de batería
            visualizador_bateria: Abstracción para visualizar estado
            carga_maxima: Capacidad máxima de la batería
            umbral: Umbral de carga baja
        """
        # ✅ Recibe dependencias, no las crea
        # ✅ NO depende de Configurador
        self._bateria = Bateria(carga_maxima, umbral)
        self._proxy_bateria = proxy_bateria
        self._visualizador_bateria = visualizador_bateria

    # Resto de métodos sin cambios...

# Creación en Composition Root:
def crear_gestor_bateria(configurador):
    # Obtener configuración
    carga_maxima = configurador.obtener_carga_maxima_bateria()
    umbral = configurador.obtener_umbral_bateria()

    # Crear dependencias
    proxy = configurador.configurar_proxy_bateria()
    visualizador = configurador.configurar_visualizador_bateria()

    # Inyectar dependencias
    return GestorBateria(
        proxy_bateria=proxy,
        visualizador_bateria=visualizador,
        carga_maxima=carga_maxima,
        umbral=umbral
    )

# Testing simple:
def test_gestor_bateria():
    mock_proxy = Mock(spec=AbsProxyBateria)
    mock_visualizador = Mock(spec=AbsVisualizadorBateria)
    mock_proxy.leer_carga.return_value = 12.5

    gestor = GestorBateria(
        proxy_bateria=mock_proxy,
        visualizador_bateria=mock_visualizador,
        carga_maxima=13.0,
        umbral=0.2
    )

    # ✅ Testing aislado con mocks
    gestor.verificar_nivel_de_carga()
    assert gestor.obtener_nivel_de_carga() == 12.5
```

---

### 3. **SelectorEntradaTemperatura - Acceso Directo al Configurador en Constructor**

**Archivo afectado:** `servicios_aplicacion/selector_entrada.py:8-16`

#### Código Violador:

```python
# selector_entrada.py
from agentes_sensores.proxy_seteo_temperatura import *  # ❌ Clase concreta
from gestores_entidades.gestor_ambiente import *         # ❌ Clase concreta

class SelectorEntradaTemperatura:

    def __init__(self, gestor_ambiente):
        # ❌ Acceso directo a Configurador (Service Locator)
        self._seteo_temperatura = Configurador.configurar_seteo_temperatura()
        self._selector_temperatura = Configurador.configurar_selector_temperatura()
        self._gestor_ambiente = gestor_ambiente
```

**Problema:**
- **Dependencias ocultas:** La interfaz del constructor solo muestra `gestor_ambiente`, pero en realidad necesita `Configurador` configurado globalmente
- **Service Locator:** Usa `Configurador` como localizador de servicios
- **Testing imposible:** No se puede testear sin `Configurador` funcionando
- **Mezcla de inyección y creación:** Recibe `gestor_ambiente` pero crea sus otras dependencias

**Impacto:**
- No se pueden inyectar mocks de `seteo_temperatura` y `selector_temperatura`
- El constructor miente: dice que solo necesita `gestor_ambiente` pero necesita mucho más
- Acoplamiento al `Configurador`

**Recomendación:** Inyectar todas las dependencias

```python
# Solución: Constructor Injection completo

from servicios_aplicacion.abs_seteo_temperatura import AbsSeteoTemperatura
from servicios_aplicacion.abs_selector_temperatura import AbsSelectorTemperatura
# Usar interfaces segregadas del análisis ISP

class SelectorEntradaTemperatura:

    def __init__(self,
                 seteo_temperatura: AbsSeteoTemperatura,
                 selector_temperatura: AbsSelectorTemperatura,
                 gestor_ambiente: InterfazGestorTemperatura):
        """
        Args:
            seteo_temperatura: Servicio para obtener comandos de seteo
            selector_temperatura: Servicio para obtener modo de visualización
            gestor_ambiente: Gestor de ambiente para modificar temperatura
        """
        # ✅ Todas las dependencias inyectadas
        self._seteo_temperatura = seteo_temperatura
        self._selector_temperatura = selector_temperatura
        self._gestor_ambiente = gestor_ambiente

    # Resto sin cambios...

# Creación en Composition Root:
seteo = configurador.configurar_seteo_temperatura()
selector = configurador.configurar_selector_temperatura()
gestor = crear_gestor_ambiente(configurador)

selector_entrada = SelectorEntradaTemperatura(
    seteo_temperatura=seteo,
    selector_temperatura=selector,
    gestor_ambiente=gestor
)

# Testing:
def test_selector_entrada():
    mock_seteo = Mock(spec=AbsSeteoTemperatura)
    mock_selector = Mock(spec=AbsSelectorTemperatura)
    mock_gestor = Mock(spec=InterfazGestorTemperatura)

    mock_seteo.obtener_seteo.return_value = "aumentar"
    mock_selector.obtener_selector.return_value = "deseada"

    selector_entrada = SelectorEntradaTemperatura(
        mock_seteo,
        mock_selector,
        mock_gestor
    )

    # ✅ Testing aislado
```

---

## 🟠 VIOLACIONES MODERADAS

### 4. **Visualizadores y Proxies Socket - Acceso al Configurador en Métodos**

**Archivos afectados:**
- `agentes_actuadores/visualizador_temperatura.py:50-72`
- `agentes_actuadores/visualizador_bateria.py:51-71`
- `agentes_actuadores/visualizador_climatizador.py:32-42`
- `agentes_sensores/proxy_sensor_temperatura.py:21-51`
- `agentes_sensores/proxy_bateria.py:23-53`
- `agentes_sensores/proxy_selector_temperatura.py:53-70`
- `agentes_sensores/proxy_seteo_temperatura.py:19-35`

#### Ejemplo 1: VisualizadorTemperaturaApi

```python
# visualizador_temperatura.py:50-72
class VisualizadorTemperaturaApi(AbsVisualizadorTemperatura):

    @staticmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        from configurador.configurador import Configurador  # ❌ Import interno
        api_url = Configurador.obtener_api_url()            # ❌ Acceso estático
        try:
            requests.post("{}/termostato/temperatura_ambiente".format(api_url),
                         json={"ambiente": int(temperatura_ambiente)},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar temperatura ambiente: {}".format(e))

    @staticmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        from configurador.configurador import Configurador  # ❌ Import interno
        api_url = Configurador.obtener_api_url()            # ❌ Acceso estático
        # ...
```

#### Ejemplo 2: ProxySensorTemperaturaSocket

```python
# proxy_sensor_temperatura.py:21-51
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):

    def leer_temperatura(self):
        from configurador.configurador import Configurador  # ❌ Import interno

        temperatura = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ❌ Acceso al Configurador
        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("temperatura")
        direccion_servidor = (host, puerto)
        # ...
```

#### Ejemplo 3: SeteoTemperaturaSocket

```python
# proxy_seteo_temperatura.py:19-35
class SeteoTemperaturaSocket(AbsSeteoTemperatura):

    def __init__(self):
        """Inicializa el socket persistente"""
        from configurador.configurador import Configurador  # ❌ Import interno

        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ❌ Acceso al Configurador
        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("seteo_temperatura")
        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        # ...
```

**Problema:**
- **Dependencias ocultas:** Los métodos/constructores acceden a dependencias externas sin declararlas en la interfaz
- **Acoplamiento a configuración específica:** Hardcoded a `Configurador`
- **Testing difícil:** Necesitas `Configurador` configurado para testear estas clases
- **Violación del principio de inyección:** Las clases buscan sus dependencias en lugar de recibirlas

**Impacto:**
- No se pueden testear sin `Configurador` funcional
- No se puede cambiar la fuente de configuración sin modificar estas clases
- Acoplamiento entre capa de adaptadores e infraestructura
- Cada visualizador/proxy Socket tiene el mismo problema repetido (violación DRY también)

**Recomendación:** Inyectar configuración en el constructor

```python
# Solución 1: Inyectar parámetros específicos

class VisualizadorTemperaturaApi(AbsVisualizadorTemperatura):

    def __init__(self, api_url: str):
        """
        Args:
            api_url: URL base de la API para enviar temperaturas
        """
        # ✅ Configuración inyectada
        self._api_url = api_url

    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        # ✅ Usa configuración inyectada, no accede a Configurador
        try:
            requests.post("{}/termostato/temperatura_ambiente".format(self._api_url),
                         json={"ambiente": int(temperatura_ambiente)},
                         timeout=5)
        except requests.RequestException as e:
            print("Error: {}".format(e))

    def mostrar_temperatura_deseada(self, temperatura_deseada):
        try:
            requests.post("{}/termostato/temperatura_deseada".format(self._api_url),
                         json={"deseada": int(temperatura_deseada)},
                         timeout=5)
        except requests.RequestException as e:
            print("Error: {}".format(e))

# Solución 2: Inyectar objeto de configuración

class ConfiguracionSocket:
    """Value Object para configuración de socket"""
    def __init__(self, host: str, puerto: int):
        self.host = host
        self.puerto = puerto

class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):

    def __init__(self, config: ConfiguracionSocket):
        """
        Args:
            config: Configuración de host y puerto
        """
        self._config = config

    def leer_temperatura(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ✅ Usa configuración inyectada
        direccion_servidor = (self._config.host, self._config.puerto)
        servidor.bind(direccion_servidor)
        # ...

# Factory actualizada:
class FactoryVisualizadorTemperatura:
    @staticmethod
    def crear(tipo: str, configurador: Configurador) -> AbsVisualizadorTemperatura:
        if tipo == "api":
            # ✅ Factory obtiene configuración y la inyecta
            api_url = configurador.obtener_api_url()
            return VisualizadorTemperaturaApi(api_url)
        elif tipo == "socket":
            return VisualizadorTemperaturaSocket()
        # ...

# Testing:
def test_visualizador_api():
    vis = VisualizadorTemperaturaApi(api_url="http://test.com/api")
    # ✅ Testing con URL de prueba, sin Configurador
    vis.mostrar_temperatura_ambiente(25.0)
```

---

### 5. **Factories - Retornan None en Lugar de Lanzar Excepción**

**Archivos afectados:** 9 factories en `configurador/`

Este problema ya se identificó en el análisis LSP, pero también es relevante para DIP:

```python
class FactoryVisualizadorTemperatura:
    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorTemperatura:
        if tipo == "archivo":
            return VisualizadorTemperatura()
        elif tipo == "socket":
            return VisualizadorTemperaturaSocket()
        elif tipo == "api":
            return VisualizadorTemperaturaApi()
        else:
            return None  # ❌ Retorna None
```

**Problema desde perspectiva DIP:**
- Los clientes que dependen de `AbsVisualizadorTemperatura` pueden recibir `None`
- Fuerza a los clientes a validar si la dependencia es válida
- La abstracción no garantiza que siempre habrá una implementación válida

**Recomendación:** Lanzar excepción (ya cubierto en análisis LSP)

```python
class FactoryVisualizadorTemperatura:
    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorTemperatura:
        # ...
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")
```

---

## 🟡 VIOLACIONES MENORES

### 6. **ejecutar.py - Instanciación Directa sin Composition Root Formal**

**Archivo afectado:** `ejecutar.py:1-6`

```python
from servicios_aplicacion.lanzador import *
from configurador.configurador import *

if __name__ == "__main__":
    Configurador().cargar_configuracion()  # ❌ Configuración como efecto secundario
    Lanzador().ejecutar()                  # ❌ Instanciación directa
```

**Problema:**
- **Sin Composition Root formal:** No hay un lugar centralizado para configurar el grafo de objetos
- **Efecto secundario global:** `Configurador().cargar_configuracion()` muta estado global
- **Instanciación directa:** `Lanzador()` crea todas sus dependencias internamente

**Impacto:**
- No hay separación entre construcción y uso de objetos
- Dificulta tener múltiples configuraciones (test, dev, prod)
- No hay control sobre el grafo de dependencias

**Recomendación:** Crear Composition Root explícito

```python
# ejecutar.py con Composition Root

from configurador.configurador import Configurador
from composition_root import CompositionRoot

def main():
    # 1. Cargar configuración
    configurador = Configurador()
    configurador.cargar_configuracion()

    # 2. Composition Root crea toda la aplicación
    aplicacion = CompositionRoot.crear_aplicacion(configurador)

    # 3. Ejecutar
    aplicacion.ejecutar()

if __name__ == "__main__":
    main()

# composition_root.py - ÚNICO lugar donde se conectan implementaciones

class CompositionRoot:
    """
    Composition Root: punto único donde se ensambla el grafo de objetos.

    Este es el ÚNICO lugar en toda la aplicación donde:
    - Se crean instancias concretas
    - Se conectan implementaciones con abstracciones
    - Se resuelven dependencias

    Todas las demás clases reciben sus dependencias inyectadas.
    """

    @staticmethod
    def crear_aplicacion(configurador: Configurador):
        # Construir de abajo hacia arriba (infraestructura → dominio → aplicación)

        # 1. Capa de adaptadores (agentes)
        proxy_bateria = configurador.configurar_proxy_bateria()
        proxy_temperatura = configurador.configurar_proxy_temperatura()
        visualizador_bateria = configurador.configurar_visualizador_bateria()
        visualizador_temperatura = configurador.configurar_visualizador_temperatura()
        # ...

        # 2. Capa de dominio (gestores)
        gestor_bateria = GestorBateria(
            proxy_bateria=proxy_bateria,
            visualizador_bateria=visualizador_bateria,
            carga_maxima=configurador.obtener_carga_maxima_bateria(),
            umbral=configurador.obtener_umbral_bateria()
        )

        gestor_ambiente = GestorAmbiente(
            proxy_sensor=proxy_temperatura,
            visualizador=visualizador_temperatura,
            temperatura_inicial=configurador.obtener_temperatura_inicial()
        )
        # ...

        # 3. Capa de aplicación
        presentador = Presentador(gestor_bateria, gestor_ambiente, ...)
        operador = OperadorParalelo(gestor_bateria, gestor_ambiente, ...)

        # 4. Lanzador (orquestador principal)
        return Lanzador(
            gestor_bateria=gestor_bateria,
            gestor_ambiente=gestor_ambiente,
            gestor_climatizador=gestor_climatizador,
            presentador=presentador,
            operador=operador
        )

    @staticmethod
    def crear_aplicacion_test():
        """Composition Root para testing con mocks"""
        # Usar mocks en lugar de implementaciones reales
        mock_proxy_bateria = MockProxyBateria()
        # ...
        return Lanzador(...)
```

**Beneficios del Composition Root:**
- **Único punto de creación:** Solo aquí se instancian clases concretas
- **Transparencia:** Fácil ver todo el grafo de dependencias
- **Múltiples configuraciones:** Diferentes roots para prod/test/dev
- **Testing:** Root de testing usa mocks
- **Mantenibilidad:** Cambios de implementación solo aquí

---

### 7. **Imports con Wildcard (`from ... import *`) - Acoplamiento Implícito**

**Archivos afectados:** Múltiples archivos en `servicios_aplicacion/`, `gestores_entidades/`

```python
# lanzador.py
from gestores_entidades.gestor_bateria import *      # ❌
from gestores_entidades.gestor_ambiente import *     # ❌
from gestores_entidades.gestor_climatizador import * # ❌

# gestor_bateria.py
from entidades.bateria import *           # ❌
from configurador.configurador import *   # ❌
```

**Problema:**
- **Dependencias ocultas:** No está claro qué clases se están usando
- **Acoplamiento implícito:** Importa todo el módulo, no solo lo necesario
- **Namespace pollution:** Contamina el espacio de nombres
- **Dificulta refactoring:** No sabes qué clases son realmente necesarias

**Recomendación:** Imports explícitos

```python
# ✅ Imports explícitos

# lanzador.py
from gestores_entidades.gestor_bateria import GestorBateria
from gestores_entidades.gestor_ambiente import GestorAmbiente
from gestores_entidades.gestor_climatizador import GestorClimatizador

# gestor_bateria.py
from entidades.bateria import Bateria
from entidades.abs_bateria import AbsProxyBateria
from entidades.abs_visualizador_bateria import AbsVisualizadorBateria

# ✅ Mejor aún: Depender de abstracciones, no de clases concretas
from typing import Protocol

class ProxyBateria(Protocol):
    def leer_carga(self) -> float: ...

class VisualizadorBateria(Protocol):
    def mostrar_tension(self, tension: float) -> None: ...
    def mostrar_indicador(self, indicador: str) -> None: ...
```

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Componentes Afectados | Tipo de Violación |
|-----------|----------|----------------------|-------------------|
| 🔴 Crítica | 3 | Lanzador, Gestores (3), SelectorEntradaTemperatura | Instanciación directa + Service Locator |
| 🟠 Moderada | 2 | Visualizadores Api/Socket (6), Proxies Socket (4), Factories (9) | Acceso a Configurador en métodos |
| 🟡 Menor | 2 | ejecutar.py, imports wildcard | Sin Composition Root, imports implícitos |
| **TOTAL** | **7 tipos** | **25+ clases** | **Acoplamiento alto-bajo nivel** |

---

## 💡 Patrones de Violación Identificados

### Patrón 1: Service Locator Anti-Pattern

**Componentes afectados:** Gestores, SelectorEntradaTemperatura, Visualizadores/Proxies Socket

**Síntoma:**
```python
# Clase accede a Configurador estático para obtener dependencias
from configurador.configurador import Configurador

class MiClase:
    def __init__(self):
        self._dependencia = Configurador.crear_dependencia()  # ❌
```

**Problema:**
- Dependencias ocultas (no aparecen en la interfaz)
- Acoplamiento a `Configurador`
- Testing imposible sin configuración real

**Solución: Dependency Injection**
```python
from abstracciones import AbsDependencia

class MiClase:
    def __init__(self, dependencia: AbsDependencia):  # ✅
        self._dependencia = dependencia
```

### Patrón 2: Creación en Lugar de Inyección

**Componentes afectados:** Lanzador, Gestores

**Síntoma:**
```python
class Lanzador:
    def __init__(self):
        self._gestor = GestorBateria()  # ❌ Crea dependencia
```

**Problema:**
- Alto nivel crea bajo nivel
- No puede cambiar implementación
- Testing imposible

**Solución: Constructor Injection**
```python
class Lanzador:
    def __init__(self, gestor: InterfazGestor):  # ✅ Recibe abstracción
        self._gestor = gestor
```

### Patrón 3: Dependencia de Módulos de Bajo Nivel

**Componentes afectados:** Gestores → Configurador

**Síntoma:**
```python
# gestor_bateria.py
from configurador.configurador import Configurador  # ❌ Dominio importa infraestructura
```

**Problema:**
- Violación directa del DIP
- Dominio conoce infraestructura
- Inversión de capas

**Solución: Depender de Abstracciones**
```python
# gestor_bateria.py
from entidades.abs_bateria import AbsProxyBateria  # ✅ Dominio importa abstracción

# configurador.py
from entidades.abs_bateria import AbsProxyBateria  # ✅ Infraestructura importa abstracción
from agentes_sensores.proxy_bateria import ProxyBateria  # ✅ Infraestructura crea implementación
```

---

## 📋 Plan de Acción Priorizado

### Fase 1: Inyección de Dependencias en Gestores (Prioridad Crítica)

**Objetivo:** Eliminar acceso directo a `Configurador` desde gestores

**Componentes a refactorizar:**
1. `GestorBateria` - Inyectar `proxy_bateria`, `visualizador`, `carga_maxima`, `umbral`
2. `GestorAmbiente` - Inyectar `proxy_temperatura`, `visualizador`, `temperatura_inicial`
3. `GestorClimatizador` - Inyectar `climatizador`, `actuador`, `visualizador`

**Pasos:**
1. Modificar constructores para recibir dependencias:
   ```python
   def __init__(self,
                proxy: AbsProxyBateria,
                visualizador: AbsVisualizadorBateria,
                carga_maxima: float,
                umbral: float):
   ```

2. Remover imports de `Configurador`

3. Actualizar código que crea gestores (moverlo a Composition Root)

4. Actualizar tests para inyectar mocks

**Esfuerzo estimado:** 5-7 horas

**Beneficios:**
- Gestores testables con mocks
- Sin dependencia de infraestructura
- Cumple DIP: dominio depende de abstracciones

---

### Fase 2: Crear Composition Root (Prioridad Alta)

**Objetivo:** Centralizar creación del grafo de objetos

**Pasos:**
1. Crear archivo `composition_root.py`

2. Implementar `CompositionRoot.crear_aplicacion(configurador)`:
   ```python
   @staticmethod
   def crear_aplicacion(configurador: Configurador):
       # Crear adaptadores
       proxy_bateria = configurador.configurar_proxy_bateria()
       # ...

       # Crear gestores con inyección
       gestor_bateria = GestorBateria(proxy_bateria, ...)

       # Crear servicios de aplicación
       presentador = Presentador(gestor_bateria, ...)

       # Crear lanzador
       return Lanzador(gestor_bateria, ...)
   ```

3. Modificar `ejecutar.py` para usar Composition Root:
   ```python
   if __name__ == "__main__":
       configurador = Configurador()
       configurador.cargar_configuracion()
       app = CompositionRoot.crear_aplicacion(configurador)
       app.ejecutar()
   ```

4. Modificar `Lanzador` para recibir dependencias

**Esfuerzo estimado:** 4-5 horas

**Beneficios:**
- Único punto de creación de objetos
- Fácil tener configuraciones diferentes
- Transparencia en el grafo de dependencias

---

### Fase 3: Inyección en Visualizadores/Proxies Socket (Prioridad Media)

**Objetivo:** Eliminar acceso a `Configurador` desde adaptadores

**Componentes a refactorizar:**
1. Visualizadores Api/Socket (6 clases)
2. Proxies Socket (4 clases)

**Estrategia:**
- Inyectar configuración necesaria en constructores
- Modificar factories para pasar configuración

**Pasos:**
1. Modificar constructores:
   ```python
   class VisualizadorTemperaturaApi:
       def __init__(self, api_url: str):
           self._api_url = api_url

   class ProxySensorSocket:
       def __init__(self, host: str, puerto: int):
           self._host = host
           self._puerto = puerto
   ```

2. Actualizar factories:
   ```python
   @staticmethod
   def crear(tipo: str, configurador: Configurador):
       if tipo == "api":
           return VisualizadorTemperaturaApi(
               api_url=configurador.obtener_api_url()
           )
   ```

3. Actualizar Composition Root para pasar configurador a factories

**Esfuerzo estimado:** 4-6 horas

---

### Fase 4: Inyección en Servicios de Aplicación (Prioridad Media)

**Objetivo:** Eliminar acceso a `Configurador` desde `SelectorEntradaTemperatura`

**Pasos:**
1. Modificar constructor para recibir `seteo_temperatura` y `selector_temperatura`:
   ```python
   def __init__(self,
                seteo_temperatura: AbsSeteoTemperatura,
                selector_temperatura: AbsSelectorTemperatura,
                gestor_ambiente: InterfazGestorTemperatura):
   ```

2. Actualizar creación en Composition Root

**Esfuerzo estimado:** 1-2 horas

---

### Fase 5: Refactoring de Imports (Prioridad Baja)

**Objetivo:** Cambiar wildcard imports a imports explícitos

**Pasos:**
1. Reemplazar `from ... import *` por imports explícitos
2. Importar abstracciones donde sea posible en lugar de clases concretas

**Esfuerzo estimado:** 2-3 horas

---

### Resumen de Esfuerzo

| Fase | Prioridad | Esfuerzo estimado |
|------|-----------|-------------------|
| Fase 1 | Crítica | 5-7 horas |
| Fase 2 | Alta | 4-5 horas |
| Fase 3 | Media | 4-6 horas |
| Fase 4 | Media | 1-2 horas |
| Fase 5 | Baja | 2-3 horas |
| **TOTAL** | | **16-23 horas** |

---

## 🎯 Ejemplo Completo de Refactoring

### Antes (Viola DIP):

```python
# ============================================================
# ANTES: Sistema acoplado con violaciones DIP
# ============================================================

# ejecutar.py
from servicios_aplicacion.lanzador import *
from configurador.configurador import *

if __name__ == "__main__":
    Configurador().cargar_configuracion()  # ❌ Efecto secundario global
    Lanzador().ejecutar()                  # ❌ Crea todo internamente

# lanzador.py
from gestores_entidades.gestor_bateria import *  # ❌ Wildcard
from configurador.configurador import *

class Lanzador:
    def __init__(self):
        # ❌ Instanciación directa de clases concretas
        self._gestor_bateria = GestorBateria()
        self._gestor_ambiente = GestorAmbiente()
        # ...

# gestor_bateria.py
from entidades.bateria import *
from configurador.configurador import *  # ❌ Dominio importa infraestructura

class GestorBateria:
    def __init__(self):
        # ❌ Acceso a Configurador (Service Locator)
        carga_maxima = Configurador.obtener_carga_maxima_bateria()
        umbral = Configurador.obtener_umbral_bateria()
        self._bateria = Bateria(carga_maxima, umbral)

        # ❌ Configurador crea dependencias
        self._proxy = Configurador().configurar_proxy_bateria()
        self._visualizador = Configurador.configurar_visualizador_bateria()

# visualizador_temperatura.py
class VisualizadorTemperaturaApi(AbsVisualizadorTemperatura):
    @staticmethod
    def mostrar_temperatura_ambiente(temp):
        from configurador.configurador import Configurador  # ❌ Import interno
        api_url = Configurador.obtener_api_url()            # ❌ Acceso estático
        requests.post(f"{api_url}/temperatura", ...)

# PROBLEMAS:
# - Testing imposible sin sistema completo
# - Acoplamiento alto entre capas
# - Dependencias ocultas
# - Violación directa del DIP: alto nivel → bajo nivel
```

### Después (Cumple DIP):

```python
# ============================================================
# DESPUÉS: Sistema desacoplado con DIP cumplido
# ============================================================

# ejecutar.py
from configurador.configurador import Configurador
from composition_root import CompositionRoot

def main():
    # ✅ Composición explícita
    configurador = Configurador()
    configurador.cargar_configuracion()

    aplicacion = CompositionRoot.crear_aplicacion(configurador)
    aplicacion.ejecutar()

if __name__ == "__main__":
    main()

# composition_root.py
"""
Composition Root: ÚNICO lugar donde se crean instancias concretas.
Todas las demás clases reciben dependencias inyectadas.
"""
from configurador.configurador import Configurador
from gestores_entidades.gestor_bateria import GestorBateria
from gestores_entidades.gestor_ambiente import GestorAmbiente
from servicios_aplicacion.lanzador import Lanzador
# ... más imports

class CompositionRoot:

    @staticmethod
    def crear_aplicacion(configurador: Configurador):
        """
        Crea el grafo completo de objetos de la aplicación.

        Flujo: Infraestructura → Adaptadores → Dominio → Aplicación
        """

        # 1. CAPA DE ADAPTADORES
        # Configurador crea los adaptadores concretos
        proxy_bateria = configurador.configurar_proxy_bateria()
        proxy_temperatura = configurador.configurar_proxy_temperatura()
        visualizador_bateria = configurador.configurar_visualizador_bateria()
        visualizador_temperatura = configurador.configurar_visualizador_temperatura()
        climatizador = configurador.configurar_climatizador()
        actuador = configurador.configurar_actuador_climatizador()
        visualizador_climatizador = configurador.configurar_visualizador_climatizador()
        seteo_temp = configurador.configurar_seteo_temperatura()
        selector_temp = configurador.configurar_selector_temperatura()

        # 2. CAPA DE DOMINIO
        # Gestores reciben sus dependencias inyectadas
        gestor_bateria = GestorBateria(
            proxy_bateria=proxy_bateria,
            visualizador_bateria=visualizador_bateria,
            carga_maxima=configurador.obtener_carga_maxima_bateria(),
            umbral=configurador.obtener_umbral_bateria()
        )

        gestor_ambiente = GestorAmbiente(
            proxy_sensor_temperatura=proxy_temperatura,
            visualizador_temperatura=visualizador_temperatura,
            temperatura_inicial=configurador.obtener_temperatura_inicial(),
            incremento_temperatura=configurador.obtener_incremento_temperatura()
        )

        gestor_climatizador = GestorClimatizador(
            climatizador=climatizador,
            actuador=actuador,
            visualizador=visualizador_climatizador
        )

        # 3. CAPA DE APLICACIÓN
        presentador = Presentador(
            gestor_bateria=gestor_bateria,
            gestor_ambiente=gestor_ambiente,
            gestor_climatizador=gestor_climatizador
        )

        selector_entrada = SelectorEntradaTemperatura(
            seteo_temperatura=seteo_temp,
            selector_temperatura=selector_temp,
            gestor_ambiente=gestor_ambiente
        )

        operador = OperadorParalelo(
            gestor_bateria=gestor_bateria,
            gestor_ambiente=gestor_ambiente,
            gestor_climatizador=gestor_climatizador,
            presentador=presentador,
            selector_entrada=selector_entrada
        )

        # 4. LANZADOR
        lanzador = Lanzador(
            gestor_bateria=gestor_bateria,
            gestor_ambiente=gestor_ambiente,
            gestor_climatizador=gestor_climatizador,
            presentador=presentador,
            operador=operador
        )

        return lanzador

    @staticmethod
    def crear_aplicacion_test():
        """Composition Root para testing con mocks"""
        from unittest.mock import Mock

        # Mocks en lugar de implementaciones reales
        mock_proxy_bateria = Mock()
        mock_visualizador = Mock()

        gestor_bateria = GestorBateria(
            proxy_bateria=mock_proxy_bateria,
            visualizador_bateria=mock_visualizador,
            carga_maxima=13.0,
            umbral=0.2
        )
        # ... resto con mocks

        return Lanzador(...)

# lanzador.py
from typing import Protocol

# ✅ Depende de abstracciones (Protocols)
class InterfazGestorBateria(Protocol):
    def verificar_nivel_de_carga(self) -> None: ...
    def obtener_nivel_de_carga(self) -> float: ...

class InterfazOperador(Protocol):
    def ejecutar(self) -> None: ...

class Lanzador:
    def __init__(self,
                 gestor_bateria: InterfazGestorBateria,
                 gestor_ambiente,
                 gestor_climatizador,
                 presentador,
                 operador: InterfazOperador):
        """
        Lanzador de la aplicación.

        Args:
            gestor_bateria: Gestor de batería (abstracción)
            gestor_ambiente: Gestor de ambiente (abstracción)
            gestor_climatizador: Gestor de climatizador (abstracción)
            presentador: Presentador (abstracción)
            operador: Operador principal (abstracción)
        """
        # ✅ Recibe todas las dependencias
        # ✅ NO crea nada
        # ✅ NO accede a Configurador
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador
        self._presentador = presentador
        self._operador = operador

    def ejecutar(self):
        from servicios_aplicacion.inicializador import Inicializador

        todo_ok = Inicializador.iniciar(
            self._gestor_bateria,
            self._gestor_ambiente,
            self._presentador
        )

        if todo_ok:
            self._operador.ejecutar()

# gestor_bateria.py
from entidades.bateria import Bateria
from entidades.abs_bateria import AbsProxyBateria  # ✅ Abstracción
from entidades.abs_visualizador_bateria import AbsVisualizadorBateria  # ✅ Abstracción

class GestorBateria:
    def __init__(self,
                 proxy_bateria: AbsProxyBateria,
                 visualizador_bateria: AbsVisualizadorBateria,
                 carga_maxima: float,
                 umbral: float):
        """
        Gestor de batería con inyección de dependencias.

        Args:
            proxy_bateria: Proxy para leer carga de batería
            visualizador_bateria: Visualizador para mostrar estado
            carga_maxima: Capacidad máxima de la batería en voltios
            umbral: Umbral de carga baja (0-1)
        """
        # ✅ Recibe dependencias, NO las crea
        # ✅ NO importa Configurador
        # ✅ Depende de abstracciones
        self._bateria = Bateria(carga_maxima, umbral)
        self._proxy_bateria = proxy_bateria
        self._visualizador_bateria = visualizador_bateria

    def verificar_nivel_de_carga(self):
        carga = self._proxy_bateria.leer_carga()
        self._bateria.nivel_de_carga = carga

    # ... resto de métodos sin cambios

# visualizador_temperatura.py
class VisualizadorTemperaturaApi(AbsVisualizadorTemperatura):
    def __init__(self, api_url: str):
        """
        Args:
            api_url: URL base de la API
        """
        # ✅ Configuración inyectada
        self._api_url = api_url

    def mostrar_temperatura_ambiente(self, temp):
        # ✅ No accede a Configurador
        requests.post(f"{self._api_url}/temperatura", ...)

# factory_visualizador_temperatura.py
class FactoryVisualizadorTemperatura:
    @staticmethod
    def crear(tipo: str, configurador: Configurador = None):
        """
        Args:
            tipo: Tipo de visualizador
            configurador: Opcional. Solo necesario para tipo "api"
        """
        if tipo == "archivo":
            return VisualizadorTemperatura()
        elif tipo == "socket":
            return VisualizadorTemperaturaSocket()
        elif tipo == "api":
            if configurador is None:
                raise ValueError("Configurador requerido para tipo 'api'")
            # ✅ Factory obtiene config y la inyecta
            api_url = configurador.obtener_api_url()
            return VisualizadorTemperaturaApi(api_url)
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")

# BENEFICIOS:
# ✅ Testing fácil con mocks
# ✅ Bajo acoplamiento
# ✅ Cumple DIP: todos dependen de abstracciones
# ✅ Composition Root centraliza creación
# ✅ Dependencias explícitas en constructores
```

### Testing Comparado:

```python
# ============================================================
# TESTING ANTES (imposible)
# ============================================================

def test_lanzador_antes():
    # ❌ Necesita:
    # - Archivo termostato.json con configuración válida
    # - Puertos disponibles para sockets
    # - Sistema completo funcional
    lanzador = Lanzador()  # Crea TODO el sistema real
    # No podemos mockear nada
    # No podemos testear lógica aislada

# ============================================================
# TESTING DESPUÉS (simple)
# ============================================================

def test_lanzador_despues():
    # ✅ Mocks simples
    mock_bateria = Mock(spec=InterfazGestorBateria)
    mock_ambiente = Mock()
    mock_climatizador = Mock()
    mock_presentador = Mock()
    mock_operador = Mock()

    # ✅ Inyectar mocks
    lanzador = Lanzador(
        gestor_bateria=mock_bateria,
        gestor_ambiente=mock_ambiente,
        gestor_climatizador=mock_climatizador,
        presentador=mock_presentador,
        operador=mock_operador
    )

    # ✅ Testing aislado de la lógica de Lanzador
    # Sin archivos, sin sockets, sin nada externo

def test_gestor_bateria():
    # ✅ Mocks de dependencias
    mock_proxy = Mock(spec=AbsProxyBateria)
    mock_visualizador = Mock(spec=AbsVisualizadorBateria)
    mock_proxy.leer_carga.return_value = 12.5

    # ✅ Testing unitario puro
    gestor = GestorBateria(
        proxy_bateria=mock_proxy,
        visualizador_bateria=mock_visualizador,
        carga_maxima=13.0,
        umbral=0.2
    )

    gestor.verificar_nivel_de_carga()

    # ✅ Verificaciones precisas
    assert gestor.obtener_nivel_de_carga() == 12.5
    mock_proxy.leer_carga.assert_called_once()
```

---

## 🔍 Indicadores de Éxito

Después del refactoring, estas condiciones deberían cumplirse:

1. ✅ **Sin acceso a Configurador desde dominio:**
   ```bash
   # No debe haber imports de Configurador en gestores_entidades/
   $ grep -r "from configurador" gestores_entidades/
   # Sin resultados
   ```

2. ✅ **Constructores solo con inyección:**
   ```python
   # Todos los constructores reciben dependencias
   def __init__(self, dependency1: Abstraction1, dependency2: Abstraction2):
       # NO: Configurador.obtener_...()
       # NO: ClaseConcreta()
   ```

3. ✅ **Composition Root único:**
   ```python
   # Solo CompositionRoot crea instancias concretas
   # Todas las demás clases reciben dependencias
   ```

4. ✅ **Testing con mocks:**
   ```python
   # Todos los tests usan mocks, no sistema real
   def test_algo():
       mock = Mock(spec=AbsInterface)
       sut = ClaseATestear(mock)  # ✅
   ```

5. ✅ **Dependencias apuntan hacia arriba:**
   ```python
   # Bajo nivel (agentes) → Abstracción (entidades/abs_*.py)
   # Alto nivel (gestores) → Abstracción (entidades/abs_*.py)
   # ✅ Ambos dependen de la abstracción
   ```

6. ✅ **Sin imports de clases concretas:**
   ```python
   # ✅ Importar abstracciones
   from entidades.abs_bateria import AbsProxyBateria

   # ❌ NO importar implementaciones (excepto en Composition Root)
   # from agentes_sensores.proxy_bateria import ProxyBateriaSocket
   ```

---

## 🎯 Conclusión

El proyecto presenta **7 tipos de violaciones del DIP** que afectan **25+ clases**:

### Problemas Principales:

1. **Service Locator Anti-Pattern** (3 componentes críticos)
   - Gestores acceden a `Configurador` estático para obtener dependencias
   - Dependencias ocultas, testing imposible
   - Acoplamiento directo entre dominio e infraestructura

2. **Instanciación Directa** (1 componente crítico)
   - `Lanzador` crea gestores concretos en lugar de recibir abstracciones
   - No se pueden inyectar mocks
   - Viola "depende de abstracciones, no de concreciones"

3. **Configuración Hardcodeada** (10 componentes moderados)
   - Visualizadores y Proxies acceden a `Configurador` en métodos
   - Testing difícil, acoplamiento innecesario

4. **Sin Composition Root** (1 componente menor)
   - No hay punto centralizado de creación del grafo de objetos
   - Creación dispersa por toda la aplicación

### Impacto:

- **Testing extremadamente difícil:** Necesitas sistema completo funcional para tests unitarios
- **Alto acoplamiento:** Capas superiores dependen de capas inferiores (inversión incorrecta)
- **Dependencias ocultas:** No está claro qué necesita cada clase
- **Rigidez:** Cambiar implementaciones requiere modificar múltiples clases
- **Violación arquitectónica:** Dominio depende de infraestructura

### Beneficios del Refactoring:

- **Testing simple:** Mocks en todos los niveles
- **Bajo acoplamiento:** Todas las capas dependen de abstracciones
- **Flexibilidad:** Cambiar implementaciones sin tocar código cliente
- **Claridad:** Dependencias explícitas en constructores
- **Arquitectura limpia:** Cumple la regla de dependencia (capas externas → internas)

### Esfuerzo Total Estimado: 16-23 horas

El refactoring más importante es **Fase 1 + Fase 2** (inyección en gestores + Composition Root), ya que:
- Elimina el anti-pattern más grave (Service Locator)
- Establece la base para todas las demás mejoras
- Hace el sistema testable
- Cumple la regla fundamental del DIP

---

## 📚 Referencias

- **Dependency Inversion Principle**: Robert C. Martin, "Agile Software Development, Principles, Patterns, and Practices"
- **Dependency Injection**: Martin Fowler, "Inversion of Control Containers and the Dependency Injection pattern"
- **Composition Root**: Mark Seemann, "Dependency Injection in .NET"
- **Clean Architecture**: Robert C. Martin, "Clean Architecture: A Craftsman's Guide to Software Structure and Design"
- **Service Locator Anti-Pattern**: Mark Seemann, "Service Locator is an Anti-Pattern"

---

**Documento generado automáticamente mediante análisis estático del código.**
