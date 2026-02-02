# PLAN DE REFACTORIZACION: gestores_entidades

**Proyecto**: ISSE_Termostato
**Paquete**: gestores_entidades
**Fecha**: 2025-12-06
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| gestor_ambiente.py | 60 | 37 | 1 | 11 |
| gestor_bateria.py | 44 | 21 | 1 | 6 |
| gestor_climatizador.py | 26 | 15 | 1 | 4 |
| **TOTAL** | **130** | **73** | **3** | **21** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 1.29 | <= 2 | ✅ Excelente |
| MI Promedio | 89.53 | >= 65 | ✅ Excelente |
| Documentacion | 18% | >= 70% | ❌ Deficiente |
| Pylint Score | 0.00/10 | >= 8.0 | ❌ Critico |
| Issues Pylint | 51 | <= 10 | ❌ Critico |

### 1.3 Distribucion de Issues Pylint

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Error (E) | 15 | import-error (4), undefined-variable (11) |
| Warning (W) | 6 | wildcard-import (4), broad-exception-caught (1), unnecessary-pass (2) |
| Convention (C) | 18 | missing-docstring (15), line-too-long (4) |
| **TOTAL** | **51** | - |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Violaciones de Principios SOLID

#### DIP (Dependency Inversion Principle) - CRITICO

**Problema**: Los gestores dependen directamente de la clase concreta `Configurador` en lugar de recibir sus dependencias inyectadas.

```python
# ACTUAL - Viola DIP
class GestorBateria:
    def __init__(self):
        carga_maxima = Configurador.obtener_carga_maxima_bateria()
        self._bateria = Bateria(carga_maxima, umbral)
        self._proxy_bateria = Configurador().configurar_proxy_bateria()
```

**Impacto**:
- Imposible testear unitariamente sin el Configurador real
- Acoplamiento fuerte a infraestructura
- Viola la Regla de Dependencia de Clean Architecture

#### SRP (Single Responsibility Principle) - MODERADO

**Problema**: Los gestores mezclan orquestacion con creacion de objetos.

### 2.2 Problemas de Codigo Limpio

| Problema | Ubicacion | Descripcion |
|----------|-----------|-------------|
| Wildcard imports | Todos los archivos | `from X import *` oculta dependencias |
| Sin docstrings | 15 metodos | Falta documentacion de proposito y contratos |
| Exception generica | gestor_ambiente.py:28 | `except Exception` muy amplio |
| Pass innecesarios | gestor_bateria.py:40,44 | Codigo muerto |
| Inconsistencia | Todos | `Configurador.metodo()` vs `Configurador().metodo()` |
| Lineas largas | gestor_ambiente.py | 4 lineas > 100 caracteres |

### 2.3 Violaciones de Clean Architecture

Segun el analisis integral, existen **violaciones de la Regla de Dependencia**:

```
Layer 2 (Use Cases / gestores_entidades)
    ↓ VIOLA
Layer 4 (Frameworks & Drivers / configurador)
```

Los gestores estan en la capa de Casos de Uso pero dependen directamente de la capa de Infraestructura (Configurador).

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios

| # | Cambio | Prioridad | Archivos Afectados |
|---|--------|-----------|-------------------|
| 1 | Inyeccion de dependencias | ALTA | Todos |
| 2 | Eliminar wildcard imports | ALTA | Todos |
| 3 | Documentacion completa | ALTA | Todos |
| 4 | Manejo de excepciones especifico | MEDIA | gestor_ambiente.py |
| 5 | Eliminar codigo innecesario | BAJA | gestor_bateria.py |
| 6 | Formateo y estilo | BAJA | Todos |

---

### 3.2 Cambio 1: Inyeccion de Dependencias

**Objetivo**: Aplicar DIP - Los gestores reciben sus dependencias en el constructor.

#### gestor_ambiente.py

```python
# ANTES
class GestorAmbiente:
    def __init__(self):
        temperatura_inicial = Configurador.obtener_temperatura_inicial()
        self._ambiente = Ambiente(temperatura_deseada_inicial=temperatura_inicial)
        self._proxy_sensor_temperatura = Configurador.configurar_proxy_temperatura()
        self._visualizador_temperatura = Configurador().configurar_visualizador_temperatura()

# DESPUES
class GestorAmbiente:
    def __init__(self, ambiente, proxy_sensor, visualizador, incremento_temperatura=1):
        """
        Inicializa el gestor de ambiente.

        Args:
            ambiente (Ambiente): Entidad de dominio que representa el ambiente.
            proxy_sensor (AbsProxySensorTemperatura): Proxy para leer temperatura.
            visualizador (AbsVisualizadorTemperatura): Visualizador de temperatura.
            incremento_temperatura (float): Incremento para ajustar temperatura deseada.
        """
        self._ambiente = ambiente
        self._proxy_sensor_temperatura = proxy_sensor
        self._visualizador_temperatura = visualizador
        self._incremento_temperatura = incremento_temperatura
```

#### gestor_bateria.py

```python
# ANTES
class GestorBateria:
    def __init__(self):
        carga_maxima = Configurador.obtener_carga_maxima_bateria()
        umbral = Configurador.obtener_umbral_bateria()
        self._bateria = Bateria(carga_maxima, umbral)
        self._proxy_bateria = Configurador().configurar_proxy_bateria()
        self._visualizador_bateria = Configurador.configurar_visualizador_bateria()

# DESPUES
class GestorBateria:
    def __init__(self, bateria, proxy_bateria, visualizador_bateria):
        """
        Inicializa el gestor de bateria.

        Args:
            bateria (Bateria): Entidad de dominio que representa la bateria.
            proxy_bateria (AbsProxyBateria): Proxy para leer carga de bateria.
            visualizador_bateria (AbsVisualizadorBateria): Visualizador de bateria.
        """
        self._bateria = bateria
        self._proxy_bateria = proxy_bateria
        self._visualizador_bateria = visualizador_bateria
```

#### gestor_climatizador.py

```python
# ANTES
class GestorClimatizador:
    def __init__(self):
        self._climatizador = Configurador.configurar_climatizador()
        self._actuador = Configurador.configurar_actuador_climatizador()
        self._visualizador = Configurador.configurar_visualizador_climatizador()

# DESPUES
class GestorClimatizador:
    def __init__(self, climatizador, actuador, visualizador):
        """
        Inicializa el gestor de climatizador.

        Args:
            climatizador (AbsClimatizador): Entidad climatizador (Climatizador o Calefactor).
            actuador (AbsProxyActuadorClimatizador): Actuador para accionar el climatizador.
            visualizador (AbsVisualizadorClimatizador): Visualizador de estado.
        """
        self._climatizador = climatizador
        self._actuador = actuador
        self._visualizador = visualizador
```

**Nota**: Este cambio requiere actualizar el codigo que instancia los gestores (probablemente en `servicios_aplicacion/`).

---

### 3.3 Cambio 2: Eliminar Wildcard Imports

**Objetivo**: Hacer explicitas todas las dependencias.

```python
# ANTES
from entidades.ambiente import *
from configurador.configurador import *

# DESPUES
from entidades.ambiente import Ambiente
from entidades.abs_sensor_temperatura import AbsProxySensorTemperatura
from entidades.abs_visualizador_temperatura import AbsVisualizadorTemperatura
```

---

### 3.4 Cambio 3: Documentacion Completa

**Objetivo**: Documentar clases y metodos con docstrings.

Ejemplo para `GestorAmbiente`:

```python
"""
Gestor de Ambiente - Orquestador de operaciones sobre el ambiente.

Este modulo contiene el gestor responsable de coordinar las operaciones
relacionadas con el ambiente a climatizar: lectura de temperatura desde
sensores, gestion de temperatura deseada, y visualizacion de temperaturas.

Patron de Diseno:
    - Facade: Simplifica la interaccion con multiples componentes
    - Controller (GRASP): Coordina casos de uso relacionados al ambiente

Responsabilidades:
    - Leer temperatura ambiente desde proxy de sensor
    - Gestionar temperatura deseada (aumentar/disminuir)
    - Coordinar visualizacion de temperaturas
    - Controlar que temperatura se muestra (ambiente vs deseada)
"""


class GestorAmbiente:
    """
    Orquestador de operaciones sobre el ambiente a climatizar.

    Coordina la interaccion entre el sensor de temperatura, la entidad
    Ambiente, y el visualizador de temperatura. Actua como Facade para
    simplificar las operaciones de temperatura para las capas superiores.

    Attributes:
        _ambiente (Ambiente): Entidad de dominio con estado del ambiente.
        _proxy_sensor_temperatura: Proxy para lectura de temperatura.
        _visualizador_temperatura: Componente de visualizacion.
        _incremento_temperatura (float): Valor de ajuste de temp. deseada.
    """

    def leer_temperatura_ambiente(self):
        """
        Lee la temperatura actual del sensor y actualiza el ambiente.

        Obtiene la temperatura desde el proxy del sensor y la almacena
        en la entidad Ambiente. Si ocurre un error de lectura, establece
        la temperatura como None.

        Raises:
            IOError: Si hay error fisico en el sensor (manejado internamente).
            ConnectionError: Si el sensor remoto no responde (manejado internamente).
        """
        ...
```

---

### 3.5 Cambio 4: Manejo de Excepciones Especifico

**Objetivo**: Capturar excepciones especificas en lugar de `Exception` generica.

```python
# ANTES
def leer_temperatura_ambiente(self):
    try:
        self._ambiente.temperatura_ambiente = self._proxy_sensor_temperatura.leer_temperatura()
    except Exception:
        self._ambiente.temperatura_ambiente = None

# DESPUES
def leer_temperatura_ambiente(self):
    """
    Lee la temperatura actual del sensor y actualiza el ambiente.

    En caso de error de lectura (sensor desconectado, timeout, etc.),
    establece la temperatura como None para indicar lectura invalida.
    """
    try:
        self._ambiente.temperatura_ambiente = self._proxy_sensor_temperatura.leer_temperatura()
    except (IOError, ConnectionError, ValueError) as e:
        # Log del error para diagnostico (opcional)
        self._ambiente.temperatura_ambiente = None
```

---

### 3.6 Cambio 5: Eliminar Codigo Innecesario

**Objetivo**: Remover sentencias `pass` innecesarias.

```python
# ANTES
def mostrar_nivel_de_carga(self):
    self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)
    pass  # <- Innecesario

# DESPUES
def mostrar_nivel_de_carga(self):
    """Muestra el nivel de carga actual en el visualizador."""
    self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)
```

---

### 3.7 Cambio 6: Formateo y Estilo

**Objetivo**: Cumplir con PEP8 y convenciones del proyecto.

- Ajustar lineas > 100 caracteres
- Agregar newline final en todos los archivos
- Consistencia en espaciado

---

## 4. IMPACTO EN OTROS PAQUETES

### 4.1 Cambios Requeridos en Otros Paquetes

El cambio de inyeccion de dependencias requiere actualizar donde se instancian los gestores:

| Paquete | Archivo Probable | Cambio Requerido |
|---------|------------------|------------------|
| servicios_aplicacion | lanzador.py | Instanciar gestores con dependencias inyectadas |
| servicios_aplicacion | operador*.py | Posiblemente actualizar uso de gestores |

**Ejemplo de cambio en lanzador.py**:

```python
# ANTES (probable)
gestor_ambiente = GestorAmbiente()

# DESPUES
ambiente = Ambiente(temperatura_deseada_inicial=Configurador.obtener_temperatura_inicial())
proxy_sensor = Configurador.configurar_proxy_temperatura()
visualizador = Configurador.configurar_visualizador_temperatura()
incremento = Configurador.obtener_incremento_temperatura()

gestor_ambiente = GestorAmbiente(
    ambiente=ambiente,
    proxy_sensor=proxy_sensor,
    visualizador=visualizador,
    incremento_temperatura=incremento
)
```

---

## 5. ORDEN DE EJECUCION

### Fase 1: Preparacion (sin romper funcionalidad)
1. [ ] Agregar docstrings a clases y metodos (no rompe nada)
2. [ ] Eliminar `pass` innecesarios
3. [ ] Ajustar formateo (lineas largas, newlines)

### Fase 2: Refactorizacion de Imports
4. [ ] Cambiar wildcard imports a imports explicitos
5. [ ] Verificar que tests siguen pasando

### Fase 3: Inyeccion de Dependencias (cambio estructural)
6. [ ] Modificar constructores para recibir dependencias
7. [ ] Actualizar codigo cliente (servicios_aplicacion)
8. [ ] Actualizar tests unitarios
9. [ ] Verificar tests de integracion

### Fase 4: Mejoras Adicionales
10. [ ] Especificar excepciones en manejo de errores
11. [ ] Ejecutar metricas post-refactorizacion

---

## 6. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 1.29 | <= 1.5 (mantener) |
| MI Promedio | 89.53 | >= 80 (mantener) |
| Documentacion | 18% | >= 70% |
| Pylint Score | 0.00 | >= 8.0 |
| Issues Pylint | 51 | <= 10 |

---

## 7. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Romper tests existentes | Media | Alto | Ejecutar tests despues de cada cambio |
| Introducir bugs en inyeccion | Media | Alto | Revisar todos los puntos de instanciacion |
| Cambios en cascada excesivos | Baja | Medio | Limitar cambios en otros paquetes a lo minimo |

---

## 8. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 1.5
- [ ] MI Promedio >= 80
- [ ] Documentacion >= 70%
- [ ] Pylint Score >= 8.0
- [ ] Sin wildcard imports
- [ ] Sin dependencia directa a Configurador en gestores

---

*Documento generado: 2025-12-06*
