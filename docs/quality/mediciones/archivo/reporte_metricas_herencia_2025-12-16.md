# REPORTE DE MÉTRICAS DE HERENCIA
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-16
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Código de producción (excluye tests y actores externos)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de herencia evalúan cómo se utiliza la herencia orientada a objetos en el diseño del sistema. Un uso adecuado de la herencia mejora la reutilización y el polimorfismo, pero el abuso puede aumentar la complejidad y el acoplamiento.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Clases analizadas** | 53 | Total de clases del proyecto |
| **Clases con herencia** | 20 | 37.7% del total |
| **Clases abstractas/base** | 11 | Clases con hijos (NOC > 0) |
| **Clases hoja** | 42 | Sin subclases |
| **Herencia múltiple** | 2 | Clases con NOP > 1 |
| **DIT Promedio** | 0.38 | ✅ Herencia limitada |
| **NOC Promedio** | 0.43 | ✅ Jerarquía balanceada |
| **DIT Máximo** | 1 | Profundidad máxima de herencia |
| **NOC Máximo** | 3 | Máximo número de hijos |
| **MIF (Factor herencia métodos)** | 0.279 | ✅ Bajo |
| **AIF (Factor herencia atributos)** | 0.083 | ✅ Bajo |
| **POF (Factor polimorfismo)** | 0.010 | ✅ Moderado |

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

**Menor es mejor (generalmente)** - Profundidad máxima desde la clase hasta la raíz.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Sin herencia
  - 1: Herencia directa (un nivel)
  - 2-3: Herencia moderada (aceptable)
  - > 3: Jerarquía profunda (problemático)

### 1.2 NOC (Number of Children)

**Moderado es mejor** - Número de subclases directas.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Clase hoja
  - 1-3: Reutilización moderada (bien)
  - 4-7: Abstracción importante (revisar)
  - > 7: Posible sobre-abstracción

### 1.3 NOP (Number of Parents)

**Menor es mejor** - Número de clases padre directas.

- 0: Sin herencia
- 1: Herencia simple (preferido)
- 2+: Herencia múltiple (usar con cuidado)

### 1.4 MIF (Method Inheritance Factor)

```
MIF = Σ(métodos_heredados) / Σ(métodos_totales)
```

- 0.0-0.2: Baja reutilización
- 0.2-0.5: Reutilización moderada (óptimo)
- 0.5-1.0: Alta reutilización

---

## 2. JERARQUÍAS DE HERENCIA DEL PROYECTO

#### Jerarquía: `AbsClimatizador`

- **Archivo**: `entidades/climatizador.py`
- **Hijos directos**: 2
- **Métodos**: 6 propios

**Subclases**:

- `Climatizador` (DIT=1, métodos=2)
- `Calefactor` (DIT=1, métodos=2)

```
AbsClimatizador
├── Climatizador
└── Calefactor
```

#### Jerarquía: `AbsProxyActuadorClimatizador`

- **Archivo**: `entidades/abs_actuador_climatizador.py`
- **Hijos directos**: 1
- **Métodos**: 1 propios

**Subclases**:

- `ActuadorClimatizadorGeneral` (DIT=1, métodos=4)

```
AbsProxyActuadorClimatizador
└── ActuadorClimatizadorGeneral
```

#### Jerarquía: `AbsProxyBateria`

- **Archivo**: `entidades/abs_bateria.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `ProxyBateriaArchivo` (DIT=1, métodos=1)
- `ProxyBateriaSocket` (DIT=1, métodos=2)

```
AbsProxyBateria
├── ProxyBateriaArchivo
└── ProxyBateriaSocket
```

#### Jerarquía: `AbsVisualizadorBateria`

- **Archivo**: `entidades/abs_visualizador_bateria.py`
- **Hijos directos**: 3
- **Métodos**: 2 propios

**Subclases**:

- `VisualizadorBateria` (DIT=1, métodos=2)
- `VisualizadorBateriaSocket` (DIT=1, métodos=2)
- `VisualizadorBateriaApi` (DIT=1, métodos=3)

```
AbsVisualizadorBateria
├── VisualizadorBateria
├── VisualizadorBateriaSocket
└── VisualizadorBateriaApi
```

#### Jerarquía: `AbsVisualizadorClimatizador`

- **Archivo**: `entidades/abs_visualizador_climatizador.py`
- **Hijos directos**: 3
- **Métodos**: 1 propios

**Subclases**:

- `VisualizadorClimatizador` (DIT=1, métodos=1)
- `VisualizadorClimatizadorSocket` (DIT=1, métodos=1)
- `VisualizadorClimatizadorApi` (DIT=1, métodos=2)

```
AbsVisualizadorClimatizador
├── VisualizadorClimatizador
├── VisualizadorClimatizadorSocket
└── VisualizadorClimatizadorApi
```

#### Jerarquía: `AbsVisualizadorTemperatura`

- **Archivo**: `entidades/abs_visualizador_temperatura.py`
- **Hijos directos**: 3
- **Métodos**: 2 propios

**Subclases**:

- `VisualizadorTemperatura` (DIT=1, métodos=2)
- `VisualizadorTemperaturaSocket` (DIT=1, métodos=2)
- `VisualizadorTemperaturaApi` (DIT=1, métodos=3)

```
AbsVisualizadorTemperatura
├── VisualizadorTemperatura
├── VisualizadorTemperaturaSocket
└── VisualizadorTemperaturaApi
```

#### Jerarquía: `AbsProxySensorTemperatura`

- **Archivo**: `entidades/abs_sensor_temperatura.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `ProxySensorTemperaturaArchivo` (DIT=1, métodos=1)
- `ProxySensorTemperaturaSocket` (DIT=1, métodos=2)

```
AbsProxySensorTemperatura
├── ProxySensorTemperaturaArchivo
└── ProxySensorTemperaturaSocket
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

#### Jerarquía: `AbsRegistrador`

- **Archivo**: `registrador/registrador.py`
- **Hijos directos**: 2
- **Métodos**: 1 propios

**Subclases**:

- `SelectorTemperaturaArchivo` (DIT=1, métodos=3)
- `ActuadorClimatizadorGeneral` (DIT=1, métodos=4)

```
AbsRegistrador
├── SelectorTemperaturaArchivo
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

## 3. TOP 15 CLASES CON MAYOR DIT

| # | Clase | DIT | NOC | NOP | Métodos | Hereda de | Archivo |
|---|-------|-----|-----|-----|---------|-----------|---------|
| 1 | `Climatizador` | 1 | 0 | 1 | 2 | AbsClimatizador | `entidades/climatizador.py` ✅ |
| 2 | `Calefactor` | 1 | 0 | 1 | 2 | AbsClimatizador | `entidades/climatizador.py` ✅ |
| 3 | `ProxyBateriaArchivo` | 1 | 0 | 1 | 1 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` ✅ |
| 4 | `ProxyBateriaSocket` | 1 | 0 | 1 | 2 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` ✅ |
| 5 | `SeteoTemperatura` | 1 | 0 | 1 | 1 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` ✅ |
| 6 | `SeteoTemperaturaSocket` | 1 | 0 | 1 | 3 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` ✅ |
| 7 | `SelectorTemperaturaArchivo` | 1 | 0 | 2 | 3 | AbsSelectorTemperatura, AbsRegistrador | `agentes_sensores/proxy_selector_temperatura.py` ✅ |
| 8 | `SelectorTemperaturaSocket` | 1 | 0 | 1 | 3 | AbsSelectorTemperatura | `agentes_sensores/proxy_selector_temperatura.py` ✅ |
| 9 | `ProxySensorTemperaturaArchivo` | 1 | 0 | 1 | 1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` ✅ |
| 10 | `ProxySensorTemperaturaSocket` | 1 | 0 | 1 | 2 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` ✅ |
| 11 | `VisualizadorClimatizador` | 1 | 0 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 12 | `VisualizadorClimatizadorSocket` | 1 | 0 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 13 | `VisualizadorClimatizadorApi` | 1 | 0 | 1 | 2 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` ✅ |
| 14 | `ActuadorClimatizadorGeneral` | 1 | 0 | 3 | 4 | AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor | `agentes_actuadores/actuador_climatizador.py` ✅ |
| 15 | `VisualizadorTemperatura` | 1 | 0 | 1 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` ✅ |

---

## 4. TOP 15 CLASES CON MAYOR NOC

| # | Clase | NOC | DIT | Métodos | Hijos | Archivo |
|---|-------|-----|-----|---------|-------|---------|
| 1 | `AbsVisualizadorBateria` | 3 | 0 | 2 | VisualizadorBateria, VisualizadorBateriaSocket, VisualizadorBateriaApi | `entidades/abs_visualizador_bateria.py` ✅ |
| 2 | `AbsVisualizadorClimatizador` | 3 | 0 | 1 | VisualizadorClimatizador, VisualizadorClimatizadorSocket, VisualizadorClimatizadorApi | `entidades/abs_visualizador_climatizador.py` ✅ |
| 3 | `AbsVisualizadorTemperatura` | 3 | 0 | 2 | VisualizadorTemperatura, VisualizadorTemperaturaSocket, VisualizadorTemperaturaApi | `entidades/abs_visualizador_temperatura.py` ✅ |
| 4 | `AbsClimatizador` | 2 | 0 | 6 | Climatizador, Calefactor | `entidades/climatizador.py` ✅ |
| 5 | `AbsProxyBateria` | 2 | 0 | 1 | ProxyBateriaArchivo, ProxyBateriaSocket | `entidades/abs_bateria.py` ✅ |
| 6 | `AbsProxySensorTemperatura` | 2 | 0 | 1 | ProxySensorTemperaturaArchivo, ProxySensorTemperaturaSocket | `entidades/abs_sensor_temperatura.py` ✅ |
| 7 | `AbsSeteoTemperatura` | 2 | 0 | 1 | SeteoTemperatura, SeteoTemperaturaSocket | `servicios_aplicacion/abs_seteo_temperatura.py` ✅ |
| 8 | `AbsSelectorTemperatura` | 2 | 0 | 1 | SelectorTemperaturaArchivo, SelectorTemperaturaSocket | `servicios_aplicacion/abs_selector_temperatura.py` ✅ |
| 9 | `AbsRegistrador` | 2 | 0 | 1 | SelectorTemperaturaArchivo, ActuadorClimatizadorGeneral | `registrador/registrador.py` ✅ |
| 10 | `AbsProxyActuadorClimatizador` | 1 | 0 | 1 | ActuadorClimatizadorGeneral | `entidades/abs_actuador_climatizador.py` ✅ |
| 11 | `AbsAuditor` | 1 | 0 | 1 | ActuadorClimatizadorGeneral | `registrador/registrador.py` ✅ |
| 12 | `Ambiente` | 0 | 0 | 8 |  | `entidades/ambiente.py` ✅ |
| 13 | `Climatizador` | 0 | 1 | 2 |  | `entidades/climatizador.py` ✅ |
| 14 | `Calefactor` | 0 | 1 | 2 |  | `entidades/climatizador.py` ✅ |
| 15 | `Bateria` | 0 | 0 | 4 |  | `entidades/bateria.py` ✅ |

---

## 5. CLASES CON HERENCIA MÚLTIPLE (NOP > 1)

Se encontraron **2 clases** con herencia múltiple:

| # | Clase | NOP | Padres | DIT | Archivo |
|---|-------|-----|--------|-----|---------|
| 1 | `SelectorTemperaturaArchivo` | 2 | AbsSelectorTemperatura, AbsRegistrador | 1 | `agentes_sensores/proxy_selector_temperatura.py` |
| 2 | `ActuadorClimatizadorGeneral` | 3 | AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor | 1 | `agentes_actuadores/actuador_climatizador.py` |

**Recomendación**: Verificar que la herencia múltiple sea necesaria

---

## 6. LISTA COMPLETA DE CLASES

| # | Clase | DIT | NOC | NOP | Métodos | Padres | Archivo |
|---|-------|-----|-----|-----|---------|--------|---------|
| 1 | `Climatizador` | 1 | 0 | 1 | 2 | AbsClimatizador | `entidades/climatizador.py` |
| 2 | `Calefactor` | 1 | 0 | 1 | 2 | AbsClimatizador | `entidades/climatizador.py` |
| 3 | `ProxyBateriaArchivo` | 1 | 0 | 1 | 1 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` |
| 4 | `ProxyBateriaSocket` | 1 | 0 | 1 | 2 | AbsProxyBateria | `agentes_sensores/proxy_bateria.py` |
| 5 | `SeteoTemperatura` | 1 | 0 | 1 | 1 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` |
| 6 | `SeteoTemperaturaSocket` | 1 | 0 | 1 | 3 | AbsSeteoTemperatura | `agentes_sensores/proxy_seteo_temperatura.py` |
| 7 | `SelectorTemperaturaArchivo` | 1 | 0 | 2 | 3 | AbsSelectorTemperatura, AbsRegistrador | `agentes_sensores/proxy_selector_temperatura.py` |
| 8 | `SelectorTemperaturaSocket` | 1 | 0 | 1 | 3 | AbsSelectorTemperatura | `agentes_sensores/proxy_selector_temperatura.py` |
| 9 | `ProxySensorTemperaturaArchivo` | 1 | 0 | 1 | 1 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` |
| 10 | `ProxySensorTemperaturaSocket` | 1 | 0 | 1 | 2 | AbsProxySensorTemperatura | `agentes_sensores/proxy_sensor_temperatura.py` |
| 11 | `VisualizadorClimatizador` | 1 | 0 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 12 | `VisualizadorClimatizadorSocket` | 1 | 0 | 1 | 1 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 13 | `VisualizadorClimatizadorApi` | 1 | 0 | 1 | 2 | AbsVisualizadorClimatizador | `agentes_actuadores/visualizador_climatizador.py` |
| 14 | `ActuadorClimatizadorGeneral` | 1 | 0 | 3 | 4 | AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor | `agentes_actuadores/actuador_climatizador.py` |
| 15 | `VisualizadorTemperatura` | 1 | 0 | 1 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 16 | `VisualizadorTemperaturaSocket` | 1 | 0 | 1 | 2 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 17 | `VisualizadorTemperaturaApi` | 1 | 0 | 1 | 3 | AbsVisualizadorTemperatura | `agentes_actuadores/visualizador_temperatura.py` |
| 18 | `VisualizadorBateria` | 1 | 0 | 1 | 2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 19 | `VisualizadorBateriaSocket` | 1 | 0 | 1 | 2 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 20 | `VisualizadorBateriaApi` | 1 | 0 | 1 | 3 | AbsVisualizadorBateria | `agentes_actuadores/visualizador_bateria.py` |
| 21 | `Ambiente` | 0 | 0 | 0 | 8 | - | `entidades/ambiente.py` |
| 22 | `AbsClimatizador` | 0 | 2 | 0 | 6 | - | `entidades/climatizador.py` |
| 23 | `AbsProxyActuadorClimatizador` | 0 | 1 | 0 | 1 | - | `entidades/abs_actuador_climatizador.py` |
| 24 | `AbsProxyBateria` | 0 | 2 | 0 | 1 | - | `entidades/abs_bateria.py` |
| 25 | `Bateria` | 0 | 0 | 0 | 4 | - | `entidades/bateria.py` |
| 26 | `AbsVisualizadorBateria` | 0 | 3 | 0 | 2 | - | `entidades/abs_visualizador_bateria.py` |
| 27 | `AbsVisualizadorClimatizador` | 0 | 3 | 0 | 1 | - | `entidades/abs_visualizador_climatizador.py` |
| 28 | `AbsVisualizadorTemperatura` | 0 | 3 | 0 | 2 | - | `entidades/abs_visualizador_temperatura.py` |
| 29 | `AbsProxySensorTemperatura` | 0 | 2 | 0 | 1 | - | `entidades/abs_sensor_temperatura.py` |
| 30 | `ControladorTemperatura` | 0 | 0 | 0 | 1 | - | `servicios_dominio/controlador_climatizador.py` |
| 31 | `Inicializador` | 0 | 0 | 0 | 1 | - | `servicios_aplicacion/inicializador.py` |
| 32 | `OperadorParalelo` | 0 | 0 | 0 | 7 | - | `servicios_aplicacion/operador_paralelo.py` |
| 33 | `OperadorSecuencial` | 0 | 0 | 0 | 2 | - | `servicios_aplicacion/operador_secuencial.py` |
| 34 | `SelectorEntradaTemperatura` | 0 | 0 | 0 | 4 | - | `servicios_aplicacion/selector_entrada.py` |
| 35 | `Presentador` | 0 | 0 | 0 | 2 | - | `servicios_aplicacion/presentador.py` |
| 36 | `Lanzador` | 0 | 0 | 0 | 2 | - | `servicios_aplicacion/lanzador.py` |
| 37 | `AbsSeteoTemperatura` | 0 | 2 | 0 | 1 | - | `servicios_aplicacion/abs_seteo_temperatura.py` |
| 38 | `AbsSelectorTemperatura` | 0 | 2 | 0 | 1 | - | `servicios_aplicacion/abs_selector_temperatura.py` |
| 39 | `GestorClimatizador` | 0 | 0 | 0 | 4 | - | `gestores_entidades/gestor_climatizador.py` |
| 40 | `GestorAmbiente` | 0 | 0 | 0 | 11 | - | `gestores_entidades/gestor_ambiente.py` |
| 41 | `GestorBateria` | 0 | 0 | 0 | 6 | - | `gestores_entidades/gestor_bateria.py` |
| 42 | `FactoryVisualizadorTemperatura` | 0 | 0 | 0 | 1 | - | `configurador/factory_visualizador_temperatura.py` |
| 43 | `FactoryClimatizador` | 0 | 0 | 0 | 1 | - | `configurador/factory_climatizador.py` |
| 44 | `Configurador` | 0 | 0 | 0 | 19 | - | `configurador/configurador.py` |
| 45 | `FactoryVisualizadorClimatizador` | 0 | 0 | 0 | 1 | - | `configurador/factory_visualizador_climatizador.py` |
| 46 | `FactoryProxySensorTemperatura` | 0 | 0 | 0 | 1 | - | `configurador/factory_sensor_temperatura.py` |
| 47 | `FactoryProxyBateria` | 0 | 0 | 0 | 1 | - | `configurador/factory_proxy_bateria.py` |
| 48 | `FactorySelectorTemperatura` | 0 | 0 | 0 | 1 | - | `configurador/factory_selector_temperatura.py` |
| 49 | `FactorySeteoTemperatura` | 0 | 0 | 0 | 1 | - | `configurador/factory_seteo_temperatura.py` |
| 50 | `FactoryActuadorClimatizador` | 0 | 0 | 0 | 1 | - | `configurador/factory_actuador_climatizador.py` |
| 51 | `FactoryVisualizadorBateria` | 0 | 0 | 0 | 1 | - | `configurador/factory_visualizador_bateria.py` |
| 52 | `AbsRegistrador` | 0 | 2 | 0 | 1 | - | `registrador/registrador.py` |
| 53 | `AbsAuditor` | 0 | 1 | 0 | 1 | - | `registrador/registrador.py` |

---

## 7. CONCLUSIONES Y RECOMENDACIONES

### 7.1 Puntos Fuertes ⭐

1. **Herencia limitada**: DIT promedio de 0.38 evita complejidad excesiva
2. **Jerarquía balanceada**: NOC promedio de 0.43 indica diseño equilibrado
3. **Reutilización óptima**: MIF de 0.279 muestra buen balance
4. **Sin jerarquías profundas**: No hay clases con DIT > 3

### 7.2 Áreas de Mejora ⚠️

1. Documentar las 2 clases con herencia múltiple

### 7.3 Indicadores Clave (KPI)

| Indicador | Valor | Umbral | Estado |
|-----------|-------|--------|--------|
| DIT Promedio | 0.38 | ≤ 2 | ✅ |
| NOC Promedio | 0.43 | ≤ 3 | ✅ |
| DIT Máximo | 1 | ≤ 3 | ✅ |
| Herencia múltiple | 2 | ≤ 2 | ✅ |
| MIF | 0.279 | ≤ 0.5 | ✅ |

### 7.4 Calificación General

**Métricas de Herencia del Proyecto**: **10.0/10** ⭐⭐⭐

---

**Fin del Reporte de Métricas de Herencia**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-16 09:19:54*