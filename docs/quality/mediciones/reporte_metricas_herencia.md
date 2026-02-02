# REPORTE DE MÉTRICAS DE HERENCIA
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-01
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Código de producción (excluye tests y actores externos)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de herencia evalúan cómo se utiliza la herencia orientada a objetos en el diseño del sistema. Un uso adecuado de la herencia mejora la reutilización y el polimorfismo, pero el abuso puede aumentar la complejidad y el acoplamiento.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Clases analizadas** | 53 | Total de clases del proyecto |
| **Clases con herencia** | 31 | 58.5% del total |
| **Clases abstractas/base** | 11 | Clases con hijos (NOC > 0) |
| **Clases hoja** | 42 | Sin subclases |
| **Herencia múltiple** | 2 | Clases con NOP > 1 |
| **DIT Promedio** | 0.38 | ✅ Herencia limitada |
| **NOC Promedio** | 0.43 | ✅ Jerarquía balanceada |
| **DIT Máximo** | 1 | Profundidad máxima de herencia |
| **NOC Máximo** | 3 | Máximo número de hijos |
| **MIF (Factor herencia métodos)** | 0.281 | ✅ Bajo |
| **AIF (Factor herencia atributos)** | 0.083 | ✅ Bajo |
| **POF (Factor polimorfismo)** | 0.846 | ⚠️ Revisar |

### Distribución por Profundidad de Herencia (DIT)

| Nivel | Clases | Porcentaje |
|-------|--------|------------|
| **Sin herencia (0)** | 33 | 62.3% |
| **Herencia directa (1)** | 20 | 37.7% |
| **Herencia moderada (2-3)** | 0 | 0.0% |
| **Herencia profunda (>3)** | 0 | 0.0% |

---

## 1. MÉTRICAS DE HERENCIA EXPLICADAS

### 1.1 DIT (Depth of Inheritance Tree)

**Menor es mejor (generalmente)** - Profundidad máxima desde la clase hasta la raíz del árbol de herencia.

```
DIT = Distancia máxima a la raíz de la jerarquía
```

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Sin herencia
  - 1: Herencia directa (un nivel)
  - 2-3: Herencia moderada (aceptable)
  - 4-5: Herencia profunda (revisar)
  - > 5: Jerarquía muy profunda (problemático)

**Ventajas de DIT alto**:
- Mayor reutilización de código
- Mayor abstracción

**Desventajas de DIT alto**:
- Mayor complejidad conceptual
- Dificulta el entendimiento
- Mayor acoplamiento a la jerarquía

### 1.2 NOC (Number of Children)

**Moderado es mejor** - Número de subclases directas.

```
NOC = número de clases que heredan directamente
```

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Clase hoja (común)
  - 1-3: Reutilización moderada (bien)
  - 4-7: Abstracción importante (revisar diseño)
  - > 7: Posible sobre-abstracción

### 1.3 NOP (Number of Parents)

**Menor es mejor** - Número de clases padre directas (indica herencia múltiple).

```
NOP = número de clases padre
```

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Sin herencia
  - 1: Herencia simple (preferido)
  - 2-3: Herencia múltiple (usar con cuidado)
  - > 3: Herencia múltiple compleja (problemático)

### 1.4 MIF (Method Inheritance Factor)

**Moderado es mejor** - Factor de herencia de métodos a nivel de proyecto.

```
MIF = Σ(métodos_heredados) / Σ(métodos_totales)
```

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0-0.2: Baja reutilización (posible duplicación)
  - 0.2-0.5: Reutilización moderada (óptimo)
  - 0.5-0.8: Alta reutilización (verificar diseño)
  - 0.8-1.0: Muy alta reutilización (posible sobre-abstracción)

### 1.5 AIF (Attribute Inheritance Factor)

**Moderado es mejor** - Factor de herencia de atributos a nivel de proyecto.

```
AIF = Σ(atributos_heredados) / Σ(atributos_totales)
```

- Similar a MIF pero para atributos de instancia

### 1.6 POF (Polymorphism Factor)

**Moderado es mejor** - Factor de polimorfismo del proyecto.

```
POF = Σ(métodos_sobreescritos) / (Σ(métodos) × NOC)
```

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0-0.1: Bajo polimorfismo (herencia no aprovechada)
  - 0.1-0.5: Polimorfismo moderado (óptimo)
  - 0.5-1.0: Alto polimorfismo (posible complejidad)

---

## 2. JERARQUÍAS DE HERENCIA DEL PROYECTO

### 2.1 Árboles de Herencia

#### Jerarquía: `AbsVisualizadorBateria`

- **Archivo**: `entidades/abs_visualizador_bateria.py`
- **Hijos directos**: 3
- **Métodos**: 2 propios

**Subclases**:

- `VisualizadorBateria` (DIT=1, métodos=2)
- `VisualizadorBateriaApi` (DIT=1, métodos=2)
- `VisualizadorBateriaSocket` (DIT=1, métodos=2)

```
AbsVisualizadorBateria
├── VisualizadorBateria
├── VisualizadorBateriaApi
└── VisualizadorBateriaSocket
```

#### Jerarquía: `AbsVisualizadorClimatizador`

- **Archivo**: `entidades/abs_visualizador_climatizador.py`
- **Hijos directos**: 3
- **Métodos**: 1 propios

**Subclases**:

- `VisualizadorClimatizador` (DIT=1, métodos=1)
- `VisualizadorClimatizadorApi` (DIT=1, métodos=1)
- `VisualizadorClimatizadorSocket` (DIT=1, métodos=1)

```
AbsVisualizadorClimatizador
├── VisualizadorClimatizador
├── VisualizadorClimatizadorApi
└── VisualizadorClimatizadorSocket
```

#### Jerarquía: `AbsVisualizadorTemperatura`

- **Archivo**: `entidades/abs_visualizador_temperatura.py`
- **Hijos directos**: 3
- **Métodos**: 2 propios

**Subclases**:

- `VisualizadorTemperatura` (DIT=1, métodos=2)
- `VisualizadorTemperaturaApi` (DIT=1, métodos=2)
- `VisualizadorTemperaturaSocket` (DIT=1, métodos=2)

```
AbsVisualizadorTemperatura
├── VisualizadorTemperatura
├── VisualizadorTemperaturaApi
└── VisualizadorTemperaturaSocket
```

#### Jerarquía: `AbsClimatizador`

- **Archivo**: `entidades/climatizador.py`
- **Hijos directos**: 2
- **Métodos**: 6 propios

**Subclases**:

- `Calefactor` (DIT=1, métodos=3)
- `Climatizador` (DIT=1, métodos=3)

```
AbsClimatizador
├── Calefactor
└── Climatizador
```

#### Jerarquía: `AbsProxyBateria`

- **Archivo**: `entidades/abs_bateria.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `ProxyBateriaArchivo` (DIT=1, métodos=1)
- `ProxyBateriaSocket` (DIT=1, métodos=1)

```
AbsProxyBateria
├── ProxyBateriaArchivo
└── ProxyBateriaSocket
```

#### Jerarquía: `AbsProxySensorTemperatura`

- **Archivo**: `entidades/abs_sensor_temperatura.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `ProxySensorTemperaturaArchivo` (DIT=1, métodos=1)
- `ProxySensorTemperaturaSocket` (DIT=1, métodos=1)

```
AbsProxySensorTemperatura
├── ProxySensorTemperaturaArchivo
└── ProxySensorTemperaturaSocket
```

#### Jerarquía: `AbsRegistrador`

- **Archivo**: `registrador/registrador.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `ActuadorClimatizadorGeneral` (DIT=1, métodos=4)
- `SelectorTemperaturaArchivo` (DIT=1, métodos=3)

```
AbsRegistrador
├── ActuadorClimatizadorGeneral
└── SelectorTemperaturaArchivo
```

#### Jerarquía: `AbsSelectorTemperatura`

- **Archivo**: `servicios_aplicacion/abs_selector_temperatura.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `SelectorTemperaturaArchivo` (DIT=1, métodos=3)
- `SelectorTemperaturaSocket` (DIT=1, métodos=3)

```
AbsSelectorTemperatura
├── SelectorTemperaturaArchivo
└── SelectorTemperaturaSocket
```

#### Jerarquía: `AbsSeteoTemperatura`

- **Archivo**: `servicios_aplicacion/abs_seteo_temperatura.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `SeteoTemperatura` (DIT=1, métodos=1)
- `SeteoTemperaturaSocket` (DIT=1, métodos=3)

```
AbsSeteoTemperatura
├── SeteoTemperatura
└── SeteoTemperaturaSocket
```

#### Jerarquía: `AbsActuadorClimatizador`

- **Archivo**: `entidades/abs_actuador_climatizador.py`
- **Hijos directos**: 1
- **Métodos**: 1 propios

**Subclases**:

- `ActuadorClimatizadorGeneral` (DIT=1, métodos=4)

```
AbsActuadorClimatizador
└── ActuadorClimatizadorGeneral
```

#### Jerarquía: `AbsAuditor`

- **Archivo**: `registrador/registrador.py`
- **Hijos directos**: 1
- **Métodos**: 1 propios

**Subclases**:

- `ActuadorClimatizadorGeneral` (DIT=1, métodos=4)

```
AbsAuditor
└── ActuadorClimatizadorGeneral
```

---

## 3. TOP 15 CLASES CON MAYOR DIT (PROFUNDIDAD DE HERENCIA)

| # | Clase | DIT | NOC | NOP | Métodos Totales | Métodos Propios | Hereda de | Archivo |
|---|-------|-----|-----|-----|----------------|----------------|-----------|----------|
| 1 | `VisualizadorTemperaturaSocket` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 2 | `VisualizadorTemperaturaApi` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 3 | `VisualizadorTemperatura` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 4 | `VisualizadorClimatizadorSocket` | 1 | 0 | 1 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 5 | `VisualizadorClimatizadorApi` | 1 | 0 | 1 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 6 | `VisualizadorClimatizador` | 1 | 0 | 1 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 7 | `VisualizadorBateriaSocket` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` ✅ |
| 8 | `VisualizadorBateriaApi` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` ✅ |
| 9 | `VisualizadorBateria` | 1 | 0 | 1 | 2 | 2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` ✅ |
| 10 | `SeteoTemperaturaSocket` | 1 | 0 | 1 | 3 | 3 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` ✅ |
| 11 | `SeteoTemperatura` | 1 | 0 | 1 | 1 | 1 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` ✅ |
| 12 | `SelectorTemperaturaSocket` | 1 | 0 | 1 | 3 | 3 | AbsSelectorTemperatura | `agentes_sensores/proxy_selector_temperatura.py` ✅ |
| 13 | `SelectorTemperaturaArchivo` | 1 | 0 | 2 | 3 | 3 | AbsSelectorTemperatura, AbsRegistrador | `agentes_sensores/proxy_selector_temperatura.py` ✅ |
| 14 | `ProxySensorTemperaturaSocket` | 1 | 0 | 1 | 1 | 1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` ✅ |
| 15 | `ProxySensorTemperaturaArchivo` | 1 | 0 | 1 | 1 | 1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` ✅ |

**Observaciones**:
- ✅ No hay clases con herencia profunda (DIT > 3)

---

## 4. TOP 15 CLASES CON MAYOR NOC (NÚMERO DE HIJOS)

Clases base con mayor número de subclases:

| # | Clase | NOC | DIT | Métodos | Hijos | Archivo |
|---|-------|-----|-----|---------|-------|----------|
| 1 | `AbsVisualizadorTemperatura` | 3 | 0 | 2 | VisualizadorTemperatura, VisualizadorTemperaturaApi, VisualizadorTemperaturaSocket | `entidades/abs_visualizador_temperatura.py` ✅ |
| 2 | `AbsVisualizadorClimatizador` | 3 | 0 | 1 | VisualizadorClimatizador, VisualizadorClimatizadorApi, VisualizadorClimatizadorSocket | `entidades/abs_visualizador_climatizador.py` ✅ |
| 3 | `AbsVisualizadorBateria` | 3 | 0 | 2 | VisualizadorBateria, VisualizadorBateriaApi, VisualizadorBateriaSocket | `entidades/abs_visualizador_bateria.py` ✅ |
| 4 | `AbsSeteoTemperatura` | 2 | 0 | 1 | SeteoTemperatura, SeteoTemperaturaSocket | `servicios_aplicacion/abs_seteo_temperatura.py` ✅ |
| 5 | `AbsSelectorTemperatura` | 2 | 0 | 1 | SelectorTemperaturaArchivo, SelectorTemperaturaSocket | `servicios_aplicacion/abs_selector_temperatura.py` ✅ |
| 6 | `AbsRegistrador` | 2 | 0 | 1 | ActuadorClimatizadorGeneral, SelectorTemperaturaArchivo | `registrador/registrador.py` ✅ |
| 7 | `AbsProxySensorTemperatura` | 2 | 0 | 1 | ProxySensorTemperaturaArchivo, ProxySensorTemperaturaSocket | `entidades/abs_sensor_temperatura.py` ✅ |
| 8 | `AbsProxyBateria` | 2 | 0 | 1 | ProxyBateriaArchivo, ProxyBateriaSocket | `entidades/abs_bateria.py` ✅ |
| 9 | `AbsClimatizador` | 2 | 0 | 6 | Calefactor, Climatizador | `entidades/climatizador.py` ✅ |
| 10 | `AbsAuditor` | 1 | 0 | 1 | ActuadorClimatizadorGeneral | `registrador/registrador.py` ✅ |
| 11 | `AbsActuadorClimatizador` | 1 | 0 | 1 | ActuadorClimatizadorGeneral | `entidades/abs_actuador_climatizador.py` ✅ |
| 12 | `VisualizadorTemperaturaSocket` | 0 | 1 | 2 |  | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 13 | `VisualizadorTemperaturaApi` | 0 | 1 | 2 |  | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 14 | `VisualizadorTemperatura` | 0 | 1 | 2 |  | `agentes_actuadores/visualizador_temperatura.py` ✅ |
| 15 | `VisualizadorClimatizadorSocket` | 0 | 1 | 1 |  | `agentes_actuadores/visualizador_climatizador.py` ✅ |

**Observaciones**:
- 11 clases tienen subclases (NOC > 0)
- Promedio de hijos por clase base: 2.1
- **Implicación**: Cambios en clases base afectan a todas sus subclases

---

## 5. CLASES CON HERENCIA MÚLTIPLE (NOP > 1)

Se encontraron **2 clases** con herencia múltiple:

| # | Clase | NOP | Padres | DIT | Archivo |
|---|-------|-----|--------|-----|----------|
| 1 | `ActuadorClimatizadorGeneral` | 3 | AbsActuadorClimatizador, AbsRegistrador, AbsAuditor | 1 | `agentes_actuadores/actuador_climatizador.py` |
| 2 | `SelectorTemperaturaArchivo` | 2 | AbsSelectorTemperatura, AbsRegistrador | 1 | `agentes_sensores/proxy_selector_temperatura.py` |

**Observaciones**:
- La herencia múltiple puede aumentar la complejidad
- **Recomendación**: Verificar que sea necesaria y esté bien documentada
- Considerar composición como alternativa en algunos casos

---

## 6. ANÁLISIS DE REUTILIZACIÓN DE MÉTODOS

### 6.1 Top 15 Clases por Métodos Heredados

| # | Clase | Métodos Heredados | Métodos Propios | Métodos Totales | % Heredados | Archivo |
|---|-------|------------------|----------------|----------------|-------------|----------|
| 1 | `Calefactor` | 6 | 3 | 6 | 100.0% | `entidades/climatizador.py` |
| 2 | `Climatizador` | 6 | 3 | 6 | 100.0% | `entidades/climatizador.py` |
| 3 | `ActuadorClimatizadorGeneral` | 3 | 4 | 4 | 75.0% | `agentes_actuadores/actuador_climatizador.py` |
| 4 | `SelectorTemperaturaArchivo` | 2 | 3 | 3 | 66.7% | `agentes_sensores/proxy_selector_temperatura.py` |
| 5 | `VisualizadorBateria` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_bateria.py` |
| 6 | `VisualizadorBateriaApi` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_bateria.py` |
| 7 | `VisualizadorBateriaSocket` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_bateria.py` |
| 8 | `VisualizadorTemperatura` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_temperatura.py` |
| 9 | `VisualizadorTemperaturaApi` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_temperatura.py` |
| 10 | `VisualizadorTemperaturaSocket` | 2 | 2 | 2 | 100.0% | `agentes_actuadores/visualizador_temperatura.py` |
| 11 | `ProxyBateriaArchivo` | 1 | 1 | 1 | 100.0% | `agentes_sensores/proxy_bateria.py` |
| 12 | `ProxyBateriaSocket` | 1 | 1 | 1 | 100.0% | `agentes_sensores/proxy_bateria.py` |
| 13 | `ProxySensorTemperaturaArchivo` | 1 | 1 | 1 | 100.0% | `agentes_sensores/proxy_sensor_temperatura.py` |
| 14 | `ProxySensorTemperaturaSocket` | 1 | 1 | 1 | 100.0% | `agentes_sensores/proxy_sensor_temperatura.py` |
| 15 | `SelectorTemperaturaSocket` | 1 | 3 | 3 | 33.3% | `agentes_sensores/proxy_selector_temperatura.py` |

### 6.2 Métricas Globales de Reutilización

- **MIF (Method Inheritance Factor)**: 0.281
- **AIF (Attribute Inheritance Factor)**: 0.083
- **POF (Polymorphism Factor)**: 0.846

**Interpretación**:
- ✅ MIF óptimo: Buen balance entre reutilización y especialización
- ⚠️ POF alto: Mucha sobreescritura, verificar complejidad

---

## 7. LISTA COMPLETA DE CLASES

Todas las clases ordenadas por DIT (profundidad) descendente:

| # | Clase | DIT | NOC | NOP | Métodos (T/P/H) | Padres | Archivo |
|---|-------|-----|-----|-----|-----------------|--------|----------|
| 1 | `VisualizadorTemperaturaSocket` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 2 | `VisualizadorTemperaturaApi` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 3 | `VisualizadorTemperatura` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 4 | `VisualizadorClimatizadorSocket` | 1 | 0 | 1 | 1/1/1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 5 | `VisualizadorClimatizadorApi` | 1 | 0 | 1 | 1/1/1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 6 | `VisualizadorClimatizador` | 1 | 0 | 1 | 1/1/1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 7 | `VisualizadorBateriaSocket` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 8 | `VisualizadorBateriaApi` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 9 | `VisualizadorBateria` | 1 | 0 | 1 | 2/2/2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 10 | `SeteoTemperaturaSocket` | 1 | 0 | 1 | 3/3/1 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` |
| 11 | `SeteoTemperatura` | 1 | 0 | 1 | 1/1/1 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` |
| 12 | `SelectorTemperaturaSocket` | 1 | 0 | 1 | 3/3/1 | AbsSelectorTemperatura | `agentes_sensores/proxy_selector_temperatura.py` |
| 13 | `SelectorTemperaturaArchivo` | 1 | 0 | 2 | 3/3/2 | AbsSelectorTemperatura, AbsRegistrador | `agentes_sensores/proxy_selector_temperatura.py` |
| 14 | `ProxySensorTemperaturaSocket` | 1 | 0 | 1 | 1/1/1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` |
| 15 | `ProxySensorTemperaturaArchivo` | 1 | 0 | 1 | 1/1/1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` |
| 16 | `ProxyBateriaSocket` | 1 | 0 | 1 | 1/1/1 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` |
| 17 | `ProxyBateriaArchivo` | 1 | 0 | 1 | 1/1/1 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` |
| 18 | `Climatizador` | 1 | 0 | 1 | 6/3/6 | AbsClimatizador | `entidades/climatizador.py` |
| 19 | `Calefactor` | 1 | 0 | 1 | 6/3/6 | AbsClimatizador | `entidades/climatizador.py` |
| 20 | `ActuadorClimatizadorGeneral` | 1 | 0 | 3 | 4/4/3 | AbsActuadorClimatizador, AbsRegistrador, AbsAuditor | `agentes_actuadores/actuador_climatizador.py` |
| 21 | `SelectorEntradaTemperatura` | 0 | 0 | 0 | 4/4/0 | - | `servicios_aplicacion/selector_entrada.py` |
| 22 | `Presentador` | 0 | 0 | 0 | 2/2/0 | - | `servicios_aplicacion/presentador.py` |
| 23 | `OperadorSecuencial` | 0 | 0 | 0 | 2/2/0 | - | `servicios_aplicacion/operador_secuencial.py` |
| 24 | `OperadorParalelo` | 0 | 0 | 0 | 7/7/0 | - | `servicios_aplicacion/operador_paralelo.py` |
| 25 | `Lanzador` | 0 | 0 | 0 | 2/2/0 | - | `servicios_aplicacion/lanzador.py` |
| 26 | `Inicializador` | 0 | 0 | 0 | 1/1/0 | - | `servicios_aplicacion/inicializador.py` |
| 27 | `GestorClimatizador` | 0 | 0 | 0 | 4/4/0 | - | `gestores_entidades/gestor_climatizador.py` |
| 28 | `GestorBateria` | 0 | 0 | 0 | 6/6/0 | - | `gestores_entidades/gestor_bateria.py` |
| 29 | `GestorAmbiente` | 0 | 0 | 0 | 11/11/0 | - | `gestores_entidades/gestor_ambiente.py` |
| 30 | `FactoryVisualizadorTemperatura` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_visualizador_temperatura.py` |
| 31 | `FactoryVisualizadorClimatizador` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_visualizador_climatizador.py` |
| 32 | `FactoryVisualizadorBateria` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_visualizador_bateria.py` |
| 33 | `FactorySeteoTemperatura` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_seteo_temperatura.py` |
| 34 | `FactorySelectorTemperatura` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_selector_temperatura.py` |
| 35 | `FactoryProxySensorTemperatura` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_sensor_temperatura.py` |
| 36 | `FactoryProxyBateria` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_proxy_bateria.py` |
| 37 | `FactoryClimatizador` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_climatizador.py` |
| 38 | `FactoryActuadorClimatizador` | 0 | 0 | 0 | 1/1/0 | - | `configurador/factory_actuador_climatizador.py` |
| 39 | `ControladorTemperatura` | 0 | 0 | 0 | 1/1/0 | - | `servicios_dominio/controlador_climatizador.py` |
| 40 | `Configurador` | 0 | 0 | 0 | 19/19/0 | - | `configurador/configurador.py` |
| 41 | `Bateria` | 0 | 0 | 0 | 3/3/0 | - | `entidades/bateria.py` |
| 42 | `Ambiente` | 0 | 0 | 0 | 5/5/0 | - | `entidades/ambiente.py` |
| 43 | `AbsVisualizadorTemperatura` | 0 | 3 | 0 | 2/2/0 | - | `entidades/abs_visualizador_temperatura.py` |
| 44 | `AbsVisualizadorClimatizador` | 0 | 3 | 0 | 1/1/0 | - | `entidades/abs_visualizador_climatizador.py` |
| 45 | `AbsVisualizadorBateria` | 0 | 3 | 0 | 2/2/0 | - | `entidades/abs_visualizador_bateria.py` |
| 46 | `AbsSeteoTemperatura` | 0 | 2 | 0 | 1/1/0 | - | `servicios_aplicacion/abs_seteo_temperatura.py` |
| 47 | `AbsSelectorTemperatura` | 0 | 2 | 0 | 1/1/0 | - | `servicios_aplicacion/abs_selector_temperatura.py` |
| 48 | `AbsRegistrador` | 0 | 2 | 0 | 1/1/0 | - | `registrador/registrador.py` |
| 49 | `AbsProxySensorTemperatura` | 0 | 2 | 0 | 1/1/0 | - | `entidades/abs_sensor_temperatura.py` |
| 50 | `AbsProxyBateria` | 0 | 2 | 0 | 1/1/0 | - | `entidades/abs_bateria.py` |
| 51 | `AbsClimatizador` | 0 | 2 | 0 | 6/6/0 | - | `entidades/climatizador.py` |
| 52 | `AbsAuditor` | 0 | 1 | 0 | 1/1/0 | - | `registrador/registrador.py` |
| 53 | `AbsActuadorClimatizador` | 0 | 1 | 0 | 1/1/0 | - | `entidades/abs_actuador_climatizador.py` |

**Leyenda**: T=Total, P=Propios, H=Heredados

---

## 8. CONCLUSIONES Y RECOMENDACIONES

### 8.1 Puntos Fuertes ⭐

1. **Herencia limitada**: DIT promedio de 0.38 evita complejidad excesiva
2. **Jerarquía balanceada**: NOC promedio de 0.43 indica diseño equilibrado
3. **Reutilización óptima**: MIF de 0.281 muestra buen balance

### 8.2 Áreas de Mejora ⚠️

✅ No se identificaron áreas críticas de mejora

### 8.3 Plan de Acción Sugerido

#### Prioridad Alta
✅ No se requieren acciones de alta prioridad

#### Prioridad Media
1. Documentar las 2 clases con herencia múltiple

#### Prioridad Baja
1. Establecer guías de diseño para nuevas jerarquías
2. Automatizar medición de métricas de herencia en CI/CD
3. Crear diagramas UML de las jerarquías principales

### 8.4 Calificación General

**Métricas de Herencia del Proyecto**: **10.0/10** ⭐⭐⭐

---

**Fin del Reporte de Métricas de Herencia**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-01 10:31:20*
