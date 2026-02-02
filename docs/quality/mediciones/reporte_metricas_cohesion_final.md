# REPORTE DE MÉTRICAS DE COHESIÓN
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-11
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de cohesión evalúan el grado en que los métodos de una clase están relacionados entre sí a través del uso de atributos compartidos. Alta cohesión indica clases bien diseñadas con responsabilidades claras.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Clases analizadas** | 51 | Clases con métodos públicos |
| **LCOM1 Promedio** | 0.231 | ✅ Baja falta de cohesión |
| **TCC Promedio** | 0.769 | ✅ Alta cohesión |
| **LCC Promedio** | 0.769 | ✅ Alta cohesión transitiva |
| **LCOM4 Promedio** | 1.7 componentes | ✅ Bien conectado |
| **Cohesion Ratio** | 0.264 | Uso promedio de atributos por método |
| **Métodos promedio/clase** | 2.0 | Tamaño promedio de clases |
| **Atributos promedio/clase** | 1.2 | Estado promedio de clases |

### Distribución por Nivel de Cohesión

| Nivel | Clases | Porcentaje | Criterio (TCC) |
|-------|--------|------------|----------------|
| **Alta** | 39 | 76.5% | TCC ≥ 0.7 |
| **Media** | 1 | 2.0% | 0.3 ≤ TCC < 0.7 |
| **Baja** | 11 | 21.6% | TCC < 0.3 |

**Interpretación**: ✅ Mayoría de clases bien cohesionadas

---

## 1. MÉTRICAS DE COHESIÓN EXPLICADAS

### 1.1 LCOM (Lack of Cohesion of Methods)

**Menor es mejor** - Mide la falta de cohesión entre métodos.

#### LCOM1 (Henderson-Sellers)
```
LCOM1 = P / (P + Q)
```
- **P**: Pares de métodos sin atributos comunes
- **Q**: Pares de métodos con atributos comunes
- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0 = Perfectamente cohesionado
  - 0.5 = Cohesión moderada
  - 1.0 = Sin cohesión (ningún par comparte atributos)

#### LCOM2
```
LCOM2 = P - Q si P > Q, sino 0
```
- **Valor absoluto** de la diferencia entre pares
- **Rango**: [0, ∞)
- **Interpretación**:
  - 0 = Alta cohesión
  - > 0 = Número de pares "desconectados"

#### LCOM3
```
LCOM3 = (m - Σ(mA)/a) / (m-1)
```
- **m**: Número de métodos
- **a**: Número de atributos
- **mA**: Métodos que acceden cada atributo
- **Rango**: [0, 1]

#### LCOM4
```
LCOM4 = Número de componentes conexos
```
- Cuenta componentes **desconectados** en el grafo método-atributo
- **Interpretación**:
  - 1 = Clase completamente cohesionada (todos los métodos conectados)
  - > 1 = Clase fragmentada (sugiere dividir en múltiples clases)

### 1.2 TCC (Tight Class Cohesion)

**Mayor es mejor** - Mide la proporción de pares de métodos directamente conectados.

```
TCC = NDC / NP
```
- **NDC**: Pares de métodos que comparten atributos
- **NP**: Total de pares posibles
- **Rango**: [0, 1]
- **Interpretación**:
  - 1.0 = Perfecta cohesión (todos los métodos comparten atributos)
  - 0.7-0.9 = Alta cohesión
  - 0.5-0.7 = Cohesión moderada
  - < 0.5 = Baja cohesión (considerar refactorización)

### 1.3 LCC (Loose Class Cohesion)

**Mayor es mejor** - Mide pares conectados directa o indirectamente.

```
LCC = NIC / NP
```
- **NIC**: Pares conectados (directa o transitivamente)
- **NP**: Total de pares posibles
- **Rango**: [0, 1]
- **Nota**: LCC ≥ TCC siempre

### 1.4 Cohesion Ratio

```
Cohesion Ratio = (Σ atributos_usados / atributos_totales) / métodos
```
- Promedio de qué porción de atributos usa cada método
- **Rango**: [0, 1]
- **Interpretación**:
  - 1.0 = Cada método usa todos los atributos
  - 0.5 = Cada método usa la mitad de los atributos
  - < 0.3 = Métodos usan pocos atributos (baja cohesión)

---

## 2. ESTADÍSTICAS GLOBALES

### 2.1 Resumen de Métricas

| Métrica | Promedio | Mínimo | Máximo | Estado |
|---------|----------|--------|--------|--------|
| **LCOM1** | 0.231 | 0.000 | 1.000 | ✅ |
| **LCOM2** | 3.5 | 0 | 153 | ✅ |
| **LCOM3** | 0.112 | 0.000 | 1.000 | ✅ |
| **LCOM4** | 1.7 | 1 | 18 | ✅ |
| **TCC** | 0.769 | 0.000 | 1.000 | ✅ |
| **LCC** | 0.769 | 0.000 | 1.000 | ✅ |
| **Cohesion Ratio** | 0.264 | 0.000 | 1.000 | ⚠️ |

### 2.2 Estructura de Clases

| Aspecto | Valor |
|---------|-------|
| **Total de clases** | 51 |
| **Métodos promedio** | 2.0 |
| **Atributos promedio** | 1.2 |
| **Ratio métodos/atributos** | 1.65 |

---

## 3. TOP 15 CLASES CON MENOR COHESIÓN

Clases con mayor LCOM1 (mayor falta de cohesión) que requieren atención:

| # | Clase | LCOM1 | LCOM4 | TCC | LCC | Cohesion Ratio | Métodos | Attrs | Estado |
|---|-------|-------|-------|-----|-----|----------------|---------|-------|--------|
| 1 | `Configurador` | 1.000 | 18 | 0.000 | 0.000 | 0.000 | 18 | 0 | ❌ |
| 2 | `SelectorTemperaturaArchivo` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 3 | `ActuadorClimatizadorGeneral` | 1.000 | 3 | 0.000 | 0.000 | 0.000 | 3 | 0 | ❌ |
| 4 | `VisualizadorTemperatura` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 5 | `VisualizadorTemperaturaSocket` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 6 | `VisualizadorBateria` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 7 | `VisualizadorBateriaSocket` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 8 | `Ambiente` | 1.000 | 3 | 0.000 | 0.000 | 0.333 | 3 | 3 | ❌ |
| 9 | `AbsVisualizadorBateria` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 10 | `AbsVisualizadorTemperatura` | 1.000 | 2 | 0.000 | 0.000 | 0.000 | 2 | 0 | ❌ |
| 11 | `OperadorParalelo` | 0.933 | 5 | 0.067 | 0.067 | 0.183 | 6 | 10 | ❌ |
| 12 | `AbsClimatizador` | 0.667 | 2 | 0.333 | 0.333 | 0.333 | 3 | 5 | ⚠️ |
| 13 | `GestorAmbiente` | 0.200 | 2 | 0.800 | 0.800 | 0.320 | 10 | 5 | ✅ |
| 14 | `Inicializador` | 0.000 | 1 | 1.000 | 1.000 | 0.000 | 1 | 0 | ✅ |
| 15 | `OperadorSecuencial` | 0.000 | 1 | 1.000 | 1.000 | 1.000 | 1 | 5 | ✅ |

**Observaciones**:
- Clases con LCOM1 = 1.0 indican **nula cohesión** (ningún par de métodos comparte atributos)
- LCOM4 > 1 sugiere que la clase tiene **componentes desconectados**
- **Recomendación**: Clases con LCOM1 > 0.8 deberían dividirse en múltiples clases

**Análisis de patrones comunes**:
- **Clases sin atributos de instancia**: 33 (pueden ser utilidades o factories)
- **Clases con muchos métodos (>10)**: 1 (candidatas a división)
- **Clases fragmentadas (LCOM4 > 1)**: 13 (contienen componentes desconectados)

---

## 4. TOP 15 CLASES CON MEJOR COHESIÓN

Clases con mayor TCC (alta cohesión) - ejemplos de buen diseño:

| # | Clase | TCC | LCC | LCOM1 | LCOM4 | Cohesion Ratio | Métodos | Attrs | Estado |
|---|-------|-----|-----|-------|-------|----------------|---------|-------|--------|
| 1 | `Inicializador` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 2 | `OperadorSecuencial` | 1.000 | 1.000 | 0.000 | 1 | 1.000 | 1 | 5 | ✅ |
| 3 | `SelectorEntradaTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 0.800 | 1 | 5 | ✅ |
| 4 | `Presentador` | 1.000 | 1.000 | 0.000 | 1 | 1.000 | 1 | 3 | ✅ |
| 5 | `Lanzador` | 1.000 | 1.000 | 0.000 | 1 | 0.800 | 1 | 5 | ✅ |
| 6 | `AbsSeteoTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 7 | `AbsSelectorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 8 | `AbsRegistrador` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 9 | `AbsAuditor` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 10 | `GestorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 0.556 | 3 | 3 | ✅ |
| 11 | `GestorBateria` | 1.000 | 1.000 | 0.000 | 1 | 0.533 | 5 | 3 | ✅ |
| 12 | `ControladorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 13 | `FactoryVisualizadorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 14 | `FactoryClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |
| 15 | `FactoryVisualizadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 0.000 | 1 | 0 | ✅ |

**Observaciones**:
- Clases con TCC = 1.0 tienen **cohesión perfecta** (todos los métodos comparten atributos)
- LCOM1 = 0.0 y LCOM4 = 1 confirman alta cohesión
- Estas clases son ejemplos de **diseño cohesivo** con responsabilidad única

---

## 5. ANÁLISIS POR PAQUETE

Métricas de cohesión promedio por paquete/módulo:

| Paquete | Clases | LCOM1 | TCC | LCC | Cohesion Ratio | Métodos Total | Attrs Total |
|---------|--------|-------|-----|-----|----------------|---------------|-------------|
| `agentes_actuadores/` | 10 | 0.500 | 0.500 | 0.500 | 0.300 | 18 | 3 |
| `agentes_sensores/` | 8 | 0.125 | 0.875 | 0.875 | 0.500 | 9 | 9 |
| `configurador/` | 10 | 0.100 | 0.900 | 0.900 | 0.000 | 27 | 0 |
| `entidades/` | 9 | 0.407 | 0.593 | 0.593 | 0.144 | 16 | 12 |
| `gestores_entidades/` | 3 | 0.067 | 0.933 | 0.933 | 0.470 | 18 | 11 |
| `registrador/` | 2 | 0.000 | 1.000 | 1.000 | 0.000 | 2 | 0 |
| `servicios_aplicacion/` | 8 | 0.117 | 0.883 | 0.883 | 0.473 | 13 | 28 |
| `servicios_dominio/` | 1 | 0.000 | 1.000 | 1.000 | 0.000 | 1 | 0 |

**Interpretación**:
- **Mejor paquete**: `registrador/` (TCC=1.000)
- **Paquete que necesita atención**: `agentes_actuadores/` (TCC=0.500)
- **Distribución general**: ✅ Buena cohesión en la mayoría de paquetes

---

## 6. CLASES FRAGMENTADAS (LCOM4 > 1)

Clases con componentes desconectados que sugieren división:

| # | Clase | LCOM4 | LCOM1 | TCC | LCC | Métodos | Attrs | Archivo |
|---|-------|-------|-------|-----|-----|---------|-------|---------|
| 1 | `Configurador` | 18 | 1.000 | 0.000 | 0.000 | 18 | 0 | `configurador/configurador.py` |
| 2 | `OperadorParalelo` | 5 | 0.933 | 0.067 | 0.067 | 6 | 10 | `servicios_aplicacion/operador_paralelo.py` |
| 3 | `ActuadorClimatizadorGeneral` | 3 | 1.000 | 0.000 | 0.000 | 3 | 0 | `agentes_actuadores/actuador_climatizador.py` |
| 4 | `Ambiente` | 3 | 1.000 | 0.000 | 0.000 | 3 | 3 | `entidades/ambiente.py` |
| 5 | `GestorAmbiente` | 2 | 0.200 | 0.800 | 0.800 | 10 | 5 | `gestores_entidades/gestor_ambiente.py` |
| 6 | `SelectorTemperaturaArchivo` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `agentes_sensores/proxy_selector_temperatura.py` |
| 7 | `VisualizadorTemperatura` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `agentes_actuadores/visualizador_temperatura.py` |
| 8 | `VisualizadorTemperaturaSocket` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `agentes_actuadores/visualizador_temperatura.py` |
| 9 | `VisualizadorBateria` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `agentes_actuadores/visualizador_bateria.py` |
| 10 | `VisualizadorBateriaSocket` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `agentes_actuadores/visualizador_bateria.py` |
| 11 | `AbsClimatizador` | 2 | 0.667 | 0.333 | 0.333 | 3 | 5 | `entidades/climatizador.py` |
| 12 | `AbsVisualizadorBateria` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `entidades/abs_visualizador_bateria.py` |
| 13 | `AbsVisualizadorTemperatura` | 2 | 1.000 | 0.000 | 0.000 | 2 | 0 | `entidades/abs_visualizador_temperatura.py` |

**Interpretación**:
- LCOM4 > 1 indica que la clase tiene **13 clases fragmentadas**
- Cada componente conexo podría ser una clase separada
- **Acción recomendada**: Aplicar **Extract Class** refactoring

---

## 7. DISTRIBUCIÓN DE COHESIÓN

### 7.1 Por Nivel de LCOM1

| Nivel | Rango LCOM1 | Clases | Porcentaje |
|-------|-------------|--------|------------|
| Excelente | < 0.3 | 39 | 76.5% |
| Bueno | 0.3-0.5 | 0 | 0.0% |
| Moderado | 0.5-0.8 | 1 | 2.0% |
| Malo | ≥ 0.8 | 11 | 21.6% |

### 7.2 Por Nivel de TCC

| Nivel | Rango TCC | Clases | Porcentaje |
|-------|-----------|--------|------------|
| Alta | ≥ 0.7 | 39 | 76.5% |
| Media | 0.5-0.7 | 0 | 0.0% |
| Baja | 0.3-0.5 | 1 | 2.0% |
| Muy Baja | < 0.3 | 11 | 21.6% |

---

## 8. LISTA COMPLETA DE CLASES

Todas las clases ordenadas por cohesión (TCC descendente):

| # | Clase | TCC | LCC | LCOM1 | LCOM4 | Métodos | Attrs | Archivo |
|---|-------|-----|-----|-------|-------|---------|-------|---------|
| 1 | `Inicializador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `servicios_aplicacion/inicializador.py` |
| 2 | `OperadorSecuencial` | 1.000 | 1.000 | 0.000 | 1 | 1 | 5 | `servicios_aplicacion/operador_secuencial.py` |
| 3 | `SelectorEntradaTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 5 | `servicios_aplicacion/selector_entrada.py` |
| 4 | `Presentador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 3 | `servicios_aplicacion/presentador.py` |
| 5 | `Lanzador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 5 | `servicios_aplicacion/lanzador.py` |
| 6 | `AbsSeteoTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `servicios_aplicacion/abs_seteo_temperatura.py` |
| 7 | `AbsSelectorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `servicios_aplicacion/abs_selector_temperatura.py` |
| 8 | `AbsRegistrador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `registrador/registrador.py` |
| 9 | `AbsAuditor` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `registrador/registrador.py` |
| 10 | `GestorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 3 | 3 | `gestores_entidades/gestor_climatizador.py` |
| 11 | `GestorBateria` | 1.000 | 1.000 | 0.000 | 1 | 5 | 3 | `gestores_entidades/gestor_bateria.py` |
| 12 | `ControladorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `servicios_dominio/controlador_climatizador.py` |
| 13 | `FactoryVisualizadorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_visualizador_temperatura.py` |
| 14 | `FactoryClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_climatizador.py` |
| 15 | `FactoryVisualizadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_visualizador_climatizador.py` |
| 16 | `FactoryProxySensorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_sensor_temperatura.py` |
| 17 | `FactoryProxyBateria` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_proxy_bateria.py` |
| 18 | `FactorySelectorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_selector_temperatura.py` |
| 19 | `FactorySeteoTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_seteo_temperatura.py` |
| 20 | `FactoryActuadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_actuador_climatizador.py` |
| 21 | `FactoryVisualizadorBateria` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `configurador/factory_visualizador_bateria.py` |
| 22 | `ProxyBateriaArchivo` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `agentes_sensores/proxy_bateria.py` |
| 23 | `ProxyBateriaSocket` | 1.000 | 1.000 | 0.000 | 1 | 1 | 2 | `agentes_sensores/proxy_bateria.py` |
| 24 | `SeteoTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 25 | `SeteoTemperaturaSocket` | 1.000 | 1.000 | 0.000 | 1 | 1 | 2 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 26 | `SelectorTemperaturaSocket` | 1.000 | 1.000 | 0.000 | 1 | 1 | 3 | `agentes_sensores/proxy_selector_temperatura.py` |
| 27 | `ProxySensorTemperaturaArchivo` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `agentes_sensores/proxy_sensor_temperatura.py` |
| 28 | `ProxySensorTemperaturaSocket` | 1.000 | 1.000 | 0.000 | 1 | 1 | 2 | `agentes_sensores/proxy_sensor_temperatura.py` |
| 29 | `VisualizadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `agentes_actuadores/visualizador_climatizador.py` |
| 30 | `VisualizadorClimatizadorSocket` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `agentes_actuadores/visualizador_climatizador.py` |
| 31 | `VisualizadorClimatizadorApi` | 1.000 | 1.000 | 0.000 | 1 | 1 | 1 | `agentes_actuadores/visualizador_climatizador.py` |
| 32 | `VisualizadorTemperaturaApi` | 1.000 | 1.000 | 0.000 | 1 | 2 | 1 | `agentes_actuadores/visualizador_temperatura.py` |
| 33 | `VisualizadorBateriaApi` | 1.000 | 1.000 | 0.000 | 1 | 2 | 1 | `agentes_actuadores/visualizador_bateria.py` |
| 34 | `AbsProxyActuadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `entidades/abs_actuador_climatizador.py` |
| 35 | `AbsProxyBateria` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `entidades/abs_bateria.py` |
| 36 | `Bateria` | 1.000 | 1.000 | 0.000 | 1 | 2 | 4 | `entidades/bateria.py` |
| 37 | `AbsVisualizadorClimatizador` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `entidades/abs_visualizador_climatizador.py` |
| 38 | `AbsProxySensorTemperatura` | 1.000 | 1.000 | 0.000 | 1 | 1 | 0 | `entidades/abs_sensor_temperatura.py` |
| 39 | `GestorAmbiente` | 0.800 | 0.800 | 0.200 | 2 | 10 | 5 | `gestores_entidades/gestor_ambiente.py` |
| 40 | `AbsClimatizador` | 0.333 | 0.333 | 0.667 | 2 | 3 | 5 | `entidades/climatizador.py` |
| 41 | `OperadorParalelo` | 0.067 | 0.067 | 0.933 | 5 | 6 | 10 | `servicios_aplicacion/operador_paralelo.py` |
| 42 | `Configurador` | 0.000 | 0.000 | 1.000 | 18 | 18 | 0 | `configurador/configurador.py` |
| 43 | `SelectorTemperaturaArchivo` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `agentes_sensores/proxy_selector_temperatura.py` |
| 44 | `ActuadorClimatizadorGeneral` | 0.000 | 0.000 | 1.000 | 3 | 3 | 0 | `agentes_actuadores/actuador_climatizador.py` |
| 45 | `VisualizadorTemperatura` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `agentes_actuadores/visualizador_temperatura.py` |
| 46 | `VisualizadorTemperaturaSocket` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `agentes_actuadores/visualizador_temperatura.py` |
| 47 | `VisualizadorBateria` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `agentes_actuadores/visualizador_bateria.py` |
| 48 | `VisualizadorBateriaSocket` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `agentes_actuadores/visualizador_bateria.py` |
| 49 | `Ambiente` | 0.000 | 0.000 | 1.000 | 3 | 3 | 3 | `entidades/ambiente.py` |
| 50 | `AbsVisualizadorBateria` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `entidades/abs_visualizador_bateria.py` |
| 51 | `AbsVisualizadorTemperatura` | 0.000 | 0.000 | 1.000 | 2 | 2 | 0 | `entidades/abs_visualizador_temperatura.py` |

---

## 9. CONCLUSIONES Y RECOMENDACIONES

### 9.1 Puntos Fuertes ⭐

1. **Alta cohesión promedio**: TCC=0.769 indica clases bien diseñadas
2. **Baja falta de cohesión**: LCOM1=0.231 muestra buen acoplamiento interno
3. **Mayoría de clases cohesionadas**: 76% con TCC ≥ 0.7
4. **Clases bien conectadas**: LCOM4=1.7 (cercano a 1 es ideal)

### 9.2 Áreas de Mejora ⚠️

1. **Clases con LCOM1 ≥ 0.8**: 11 clases sin cohesión
   - `OperadorParalelo`
   - `Configurador`
   - `SelectorTemperaturaArchivo`
   - `ActuadorClimatizadorGeneral`
   - `VisualizadorTemperatura`
   - **Acción**: Aplicar **Extract Class** o **Extract Module** refactoring

2. **Clases fragmentadas (LCOM4 > 1)**: 13 clases
   - `Configurador` (18 componentes)
   - `OperadorParalelo` (5 componentes)
   - `ActuadorClimatizadorGeneral` (3 componentes)
   - `Ambiente` (3 componentes)
   - `GestorAmbiente` (2 componentes)
   - **Acción**: Dividir en clases separadas por componente

3. **Clases sin atributos**: 33 clases (65%)
   - Pueden ser utilities, factories o servicios sin estado
   - **Acción**: Revisar si deberían ser módulos en lugar de clases

4. **Clases con TCC < 0.3**: 11 clases con baja cohesión
   - **Acción**: Revisar si métodos pertenecen realmente a la misma clase


### 9.3 Plan de Acción Sugerido

#### Prioridad Alta
1. Refactorizar 11 clases con LCOM1 ≥ 0.8
2. Dividir 13 clases fragmentadas (LCOM4 > 1)
3. Revisar 11 clases con TCC < 0.3

#### Prioridad Media
1. Mejorar cohesión de 1 clases con LCOM1 entre 0.5-0.8
2. Analizar 33 clases sin atributos (¿deben ser módulos?)
3. Aplicar **Single Responsibility Principle** a clases con muchos métodos

#### Prioridad Baja
1. Optimizar clases con cohesión media (TCC 0.5-0.7)
2. Establecer umbral mínimo TCC = 0.5 para nuevas clases
3. Automatizar medición de cohesión en CI/CD

### 9.4 Indicadores Clave (KPI)

| Indicador | Valor Actual | Umbral | Estado |
|-----------|--------------|--------|--------|
| LCOM1 Promedio | 0.231 | < 0.5 | ✅ |
| TCC Promedio | 0.769 | ≥ 0.7 | ✅ |
| LCC Promedio | 0.769 | ≥ 0.7 | ✅ |
| LCOM4 Promedio | 1.7 | < 2 | ✅ |
| % Clases Alta Cohesión | 76.5% | ≥ 70% | ✅ |
| Clases Fragmentadas | 13 | 0 | ❌ |
| Métodos Promedio/Clase | 2.0 | < 10 | ✅ |

### 9.5 Calificación General

**Métricas de Cohesión del Proyecto**: **9.0/10** ⭐

- ✅ LCOM1: 10/10
- ✅ TCC: 9/10
- ✅ LCOM4: 8/10
- ✅ Distribución: 9/10

---

## 10. REFERENCIAS

### Interpretación de Métricas

#### LCOM1 (Lack of Cohesion of Methods)
- **0.0-0.3**: Excelente cohesión
- **0.3-0.5**: Buena cohesión
- **0.5-0.8**: Cohesión moderada, considerar refactorización
- **0.8-1.0**: Baja cohesión, requiere refactorización

#### TCC (Tight Class Cohesion)
- **0.8-1.0**: Cohesión excelente
- **0.7-0.8**: Alta cohesión
- **0.5-0.7**: Cohesión moderada
- **0.3-0.5**: Baja cohesión
- **< 0.3**: Muy baja cohesión, revisar diseño

#### LCC (Loose Class Cohesion)
- **0.8-1.0**: Excelente conectividad transitiva
- **0.6-0.8**: Buena conectividad
- **< 0.6**: Revisar estructura de la clase

#### LCOM4 (Componentes Conexos)
- **1**: Ideal - clase completamente cohesionada
- **2**: Clase tiene 2 componentes desconectados
- **≥ 3**: Clase altamente fragmentada

### Técnicas de Refactorización

1. **Extract Class**: Dividir clase con LCOM4 > 1 en múltiples clases
2. **Move Method**: Mover métodos a clases donde usan más atributos
3. **Extract Module**: Convertir clases sin estado en módulos/funciones
4. **Inline Class**: Fusionar clases muy pequeñas con baja cohesión

### Principios de Diseño

- **Single Responsibility Principle (SRP)**: Cada clase debe tener una sola razón para cambiar
- **High Cohesion, Low Coupling**: Clases cohesivas son más fáciles de entender y mantener
- **Cohesión como indicador**: TCC > 0.7 sugiere buena aplicación de SRP

---

**Fin del Reporte de Métricas de Cohesión**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-11 12:12:45*
*Próximos análisis recomendados: Acoplamiento (CBO, Fan-In/Fan-Out), Métricas CK*
