# REPORTE DE MÉTRICAS CK (CHIDAMBER-KEMERER)
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-16
**Herramientas**: Script personalizado basado en AST de Python + radon
**Alcance**: Código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas CK (Chidamber-Kemerer) son un conjunto de 6 métricas fundamentales para evaluar el diseño orientado a objetos. Fueron propuestas por Shyam Chidamber y Chris Kemerer en 1994 y son ampliamente aceptadas como indicadores de calidad de software.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Clases analizadas** | 53 | Clases del proyecto |
| **WMC Promedio** | 7.58 | ✅ Baja complejidad |
| **DIT Promedio** | 0.38 | ✅ Herencia limitada |
| **NOC Promedio** | 0.43 | ✅ Jerarquía balanceada |
| **CBO Promedio** | 2.04 | ✅ Bajo acoplamiento |
| **RFC Promedio** | 5.32 | ✅ Complejidad de respuesta baja |
| **LCOM Promedio** | 0.077 | ✅ Alta cohesión |

### Distribución por Nivel de Complejidad (WMC)

| Nivel | Clases | Porcentaje | Criterio (WMC) |
|-------|--------|------------|----------------|
| **Baja** | 20 | 37.7% | WMC ≤ 5 |
| **Media** | 28 | 52.8% | 5 < WMC ≤ 15 |
| **Alta** | 5 | 9.4% | WMC > 15 |

### Distribución por Nivel de Acoplamiento (CBO)

| Nivel | Clases | Porcentaje | Criterio (CBO) |
|-------|--------|------------|----------------|
| **Bajo** | 37 | 69.8% | CBO ≤ 2 |
| **Medio** | 14 | 26.4% | 2 < CBO ≤ 5 |
| **Alto** | 2 | 3.8% | CBO > 5 |

**Interpretación**: ⚠️ Revisar diseño

---

## 1. MÉTRICAS CK EXPLICADAS

### 1.1 WMC (Weighted Methods per Class)

**Menor es mejor** - Suma de la complejidad ciclomática de todos los métodos de la clase.

```
WMC = Σ CC(método_i)
```

- **CC**: Complejidad Ciclomática de cada método
- **Rango**: [1, ∞)
- **Interpretación**:
  - 1-5: Clase simple (excelente)
  - 6-15: Complejidad moderada (aceptable)
  - 16-30: Complejidad alta (revisar)
  - > 30: Complejidad muy alta (refactorizar)

### 1.2 DIT (Depth of Inheritance Tree)

**Menor es mejor (generalmente)** - Profundidad máxima desde la clase hasta la raíz.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0-1: Sin herencia o herencia directa (simple)
  - 2-3: Herencia moderada (aceptable)
  - 4-5: Herencia profunda (revisar)
  - > 5: Jerarquía muy profunda (problemático)

### 1.3 NOC (Number of Children)

**Moderado es mejor** - Número de subclases directas.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0: Clase hoja (común)
  - 1-3: Reutilización moderada (bien)
  - 4-7: Abstracción importante (revisar diseño)
  - > 7: Posible sobre-abstracción

### 1.4 CBO (Coupling Between Objects)

**Menor es mejor** - Número de clases con las que una clase está acoplada.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0-2: Bajo acoplamiento (excelente)
  - 3-7: Acoplamiento moderado (aceptable)
  - 8-15: Alto acoplamiento (revisar)
  - > 15: Acoplamiento excesivo (refactorizar)

### 1.5 RFC (Response for Class)

**Menor es mejor** - Conjunto de métodos que pueden ser invocados en respuesta a un mensaje.

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0-20: Complejidad baja (excelente)
  - 21-50: Complejidad moderada (aceptable)
  - 51-100: Complejidad alta (revisar)
  - > 100: Complejidad muy alta (refactorizar)

### 1.6 LCOM (Lack of Cohesion of Methods)

**Menor es mejor** - Falta de cohesión entre métodos.

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0-0.3: Alta cohesión
  - 0.3-0.5: Cohesión moderada
  - 0.5-0.8: Baja cohesión
  - 0.8-1.0: Muy baja cohesión

---

## 2. ESTADÍSTICAS GLOBALES

### 2.1 Resumen de Métricas

| Métrica | Promedio | Mínimo | Máximo | Umbral | Estado |
|---------|----------|--------|--------|--------|--------|
| **WMC** | 7.58 | 3 | 38 | ≤ 15 | ✅ |
| **DIT** | 0.38 | 0 | 1 | ≤ 3 | ✅ |
| **NOC** | 0.43 | 0 | 3 | ≤ 3 | ✅ |
| **CBO** | 2.04 | 0 | 12 | ≤ 5 | ✅ |
| **RFC** | 5.32 | 1 | 37 | ≤ 30 | ✅ |
| **LCOM** | 0.077 | 0.000 | 1.000 | ≤ 0.5 | ✅ |

### 2.2 Análisis de Distribuciones

**WMC (Complejidad)**:
- 20 clases (38%) con complejidad baja
- 28 clases (53%) con complejidad media
- 5 clases (9%) con complejidad alta

**CBO (Acoplamiento)**:
- 37 clases (70%) con bajo acoplamiento
- 14 clases (26%) con acoplamiento medio
- 2 clases (4%) con alto acoplamiento

---

## 3. TOP 15 CLASES CON MAYOR WMC (COMPLEJIDAD)

Clases más complejas que requieren atención prioritaria:

| # | Clase | WMC | Métodos | DIT | NOC | CBO | RFC | LCOM | Estado |
|---|-------|-----|---------|-----|-----|-----|-----|------|--------|
| 1 | `Configurador` | 38 | 19 | 0 | 0 | 12 | 37 | 0.000 | ⚠️ |
| 2 | `SeteoTemperaturaSocket` | 17 | 3 | 1 | 0 | 3 | 7 | 0.000 | ⚠️ |
| 3 | `SelectorTemperaturaSocket` | 17 | 3 | 1 | 0 | 3 | 7 | 0.000 | ⚠️ |
| 4 | `OperadorParalelo` | 16 | 7 | 0 | 0 | 2 | 13 | 0.714 | ⚠️ |
| 5 | `GestorAmbiente` | 16 | 11 | 0 | 0 | 3 | 11 | 0.182 | ⚠️ |
| 6 | `Ambiente` | 11 | 8 | 0 | 0 | 0 | 8 | 0.429 | ✅ |
| 7 | `SelectorEntradaTemperatura` | 11 | 4 | 0 | 0 | 1 | 5 | 0.000 | ✅ |
| 8 | `Bateria` | 10 | 4 | 0 | 0 | 1 | 6 | 0.000 | ✅ |
| 9 | `ActuadorClimatizadorGeneral` | 10 | 4 | 1 | 0 | 5 | 11 | 0.000 | ✅ |
| 10 | `AbsClimatizador` | 9 | 6 | 0 | 2 | 3 | 9 | 0.733 | ✅ |
| 11 | `ProxyBateriaSocket` | 9 | 2 | 1 | 0 | 2 | 8 | 0.000 | ✅ |
| 12 | `ProxySensorTemperaturaSocket` | 9 | 2 | 1 | 0 | 2 | 8 | 0.000 | ✅ |
| 13 | `FactoryVisualizadorTemperatura` | 9 | 1 | 0 | 0 | 4 | 4 | 0.000 | ✅ |
| 14 | `FactoryVisualizadorClimatizador` | 9 | 1 | 0 | 0 | 4 | 4 | 0.000 | ✅ |
| 15 | `FactoryVisualizadorBateria` | 9 | 1 | 0 | 0 | 4 | 4 | 0.000 | ✅ |

---

## 4. TOP 15 CLASES CON MAYOR CBO (ACOPLAMIENTO)

Clases con mayor acoplamiento que afectan la modularidad:

| # | Clase | CBO | RFC | WMC | Archivo |
|---|-------|-----|-----|-----|---------|
| 1 | `Configurador` | 12 | 37 | 38 | `configurador/configurador.py` |
| 2 | `Lanzador` | 9 | 12 | 6 | `servicios_aplicacion/lanzador.py` |
| 3 | `ActuadorClimatizadorGeneral` | 5 | 11 | 10 | `agentes_actuadores/actuador_climatizador.py` |
| 4 | `SelectorTemperaturaArchivo` | 4 | 9 | 8 | `agentes_sensores/proxy_selector_temperatura.py` |
| 5 | `FactoryVisualizadorTemperatura` | 4 | 4 | 9 | `configurador/factory_visualizador_temperatura.py` |
| 6 | `FactoryVisualizadorClimatizador` | 4 | 4 | 9 | `configurador/factory_visualizador_climatizador.py` |
| 7 | `FactoryVisualizadorBateria` | 4 | 4 | 9 | `configurador/factory_visualizador_bateria.py` |
| 8 | `AbsClimatizador` | 3 | 9 | 9 | `entidades/climatizador.py` |
| 9 | `GestorAmbiente` | 3 | 11 | 16 | `gestores_entidades/gestor_ambiente.py` |
| 10 | `SeteoTemperaturaSocket` | 3 | 7 | 17 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 11 | `SelectorTemperaturaSocket` | 3 | 7 | 17 | `agentes_sensores/proxy_selector_temperatura.py` |
| 12 | `FactoryClimatizador` | 3 | 3 | 7 | `configurador/factory_climatizador.py` |
| 13 | `FactoryProxySensorTemperatura` | 3 | 3 | 7 | `configurador/factory_sensor_temperatura.py` |
| 14 | `FactoryProxyBateria` | 3 | 3 | 7 | `configurador/factory_proxy_bateria.py` |
| 15 | `FactorySelectorTemperatura` | 3 | 3 | 7 | `configurador/factory_selector_temperatura.py` |

---

## 5. TOP 15 CLASES CON MAYOR RFC (COMPLEJIDAD DE RESPUESTA)

| # | Clase | RFC | WMC | CBO | Métodos | Estado |
|---|-------|-----|-----|-----|---------|--------|
| 1 | `Configurador` | 37 | 38 | 12 | 19 | ✅ |
| 2 | `OperadorParalelo` | 13 | 16 | 2 | 7 | ✅ |
| 3 | `Lanzador` | 12 | 6 | 9 | 2 | ✅ |
| 4 | `GestorAmbiente` | 11 | 16 | 3 | 11 | ✅ |
| 5 | `ActuadorClimatizadorGeneral` | 11 | 10 | 5 | 4 | ✅ |
| 6 | `AbsClimatizador` | 9 | 9 | 3 | 6 | ✅ |
| 7 | `SelectorTemperaturaArchivo` | 9 | 8 | 4 | 3 | ✅ |
| 8 | `Ambiente` | 8 | 11 | 0 | 8 | ✅ |
| 9 | `ProxyBateriaSocket` | 8 | 9 | 2 | 2 | ✅ |
| 10 | `ProxySensorTemperaturaSocket` | 8 | 9 | 2 | 2 | ✅ |
| 11 | `OperadorSecuencial` | 7 | 6 | 2 | 2 | ✅ |
| 12 | `SeteoTemperaturaSocket` | 7 | 17 | 3 | 3 | ✅ |
| 13 | `SelectorTemperaturaSocket` | 7 | 17 | 3 | 3 | ✅ |
| 14 | `VisualizadorTemperaturaSocket` | 7 | 7 | 2 | 2 | ✅ |
| 15 | `VisualizadorBateriaSocket` | 7 | 7 | 2 | 2 | ✅ |

---

## 6. ANÁLISIS POR PAQUETE

Métricas CK promedio por paquete/módulo:

| Paquete | Clases | WMC | DIT | NOC | CBO | RFC | LCOM |
|---------|--------|-----|-----|-----|-----|-----|------|
| `agentes_actuadores/` | 10 | 6.2 | 1.00 | 0.00 | 1.7 | 5.7 | 0.000 |
| `agentes_sensores/` | 8 | 9.6 | 1.00 | 0.00 | 2.4 | 6.2 | 0.000 |
| `configurador/` | 10 | 10.5 | 0.00 | 0.00 | 4.1 | 6.6 | 0.000 |
| `entidades/` | 11 | 5.3 | 0.18 | 1.45 | 1.1 | 3.4 | 0.287 |
| `gestores_entidades/` | 3 | 10.3 | 0.00 | 0.00 | 1.0 | 7.0 | 0.061 |
| `registrador/` | 2 | 3.0 | 0.00 | 1.50 | 0.0 | 1.0 | 0.000 |
| `servicios_aplicacion/` | 8 | 7.0 | 0.00 | 0.50 | 2.0 | 6.0 | 0.089 |
| `servicios_dominio/` | 1 | 7.0 | 0.00 | 0.00 | 0.0 | 1.0 | 0.000 |

---

## 7. LISTA COMPLETA DE CLASES

Todas las clases ordenadas por WMC (complejidad) descendente:

| # | Clase | WMC | DIT | NOC | CBO | RFC | LCOM | Archivo |
|---|-------|-----|-----|-----|-----|-----|------|---------|
| 1 | `Configurador` | 38 | 0 | 0 | 12 | 37 | 0.000 | `configurador/configurador.py` |
| 2 | `SeteoTemperaturaSocket` | 17 | 1 | 0 | 3 | 7 | 0.000 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 3 | `SelectorTemperaturaSocket` | 17 | 1 | 0 | 3 | 7 | 0.000 | `agentes_sensores/proxy_selector_temperatura.py` |
| 4 | `OperadorParalelo` | 16 | 0 | 0 | 2 | 13 | 0.714 | `servicios_aplicacion/operador_paralelo.py` |
| 5 | `GestorAmbiente` | 16 | 0 | 0 | 3 | 11 | 0.182 | `gestores_entidades/gestor_ambiente.py` |
| 6 | `Ambiente` | 11 | 0 | 0 | 0 | 8 | 0.429 | `entidades/ambiente.py` |
| 7 | `SelectorEntradaTemperatura` | 11 | 0 | 0 | 1 | 5 | 0.000 | `servicios_aplicacion/selector_entrada.py` |
| 8 | `Bateria` | 10 | 0 | 0 | 1 | 6 | 0.000 | `entidades/bateria.py` |
| 9 | `ActuadorClimatizadorGeneral` | 10 | 1 | 0 | 5 | 11 | 0.000 | `agentes_actuadores/actuador_climatizador.py` |
| 10 | `AbsClimatizador` | 9 | 0 | 2 | 3 | 9 | 0.733 | `entidades/climatizador.py` |
| 11 | `ProxyBateriaSocket` | 9 | 1 | 0 | 2 | 8 | 0.000 | `agentes_sensores/proxy_bateria.py` |
| 12 | `ProxySensorTemperaturaSocket` | 9 | 1 | 0 | 2 | 8 | 0.000 | `agentes_sensores/proxy_sensor_temperatura.py` |
| 13 | `FactoryVisualizadorTemperatura` | 9 | 0 | 0 | 4 | 4 | 0.000 | `configurador/factory_visualizador_temperatura.py` |
| 14 | `FactoryVisualizadorClimatizador` | 9 | 0 | 0 | 4 | 4 | 0.000 | `configurador/factory_visualizador_climatizador.py` |
| 15 | `FactoryVisualizadorBateria` | 9 | 0 | 0 | 4 | 4 | 0.000 | `configurador/factory_visualizador_bateria.py` |
| 16 | `GestorBateria` | 8 | 0 | 0 | 0 | 6 | 0.000 | `gestores_entidades/gestor_bateria.py` |
| 17 | `SelectorTemperaturaArchivo` | 8 | 1 | 0 | 4 | 9 | 0.000 | `agentes_sensores/proxy_selector_temperatura.py` |
| 18 | `VisualizadorTemperaturaApi` | 8 | 1 | 0 | 1 | 6 | 0.000 | `agentes_actuadores/visualizador_temperatura.py` |
| 19 | `VisualizadorBateriaApi` | 8 | 1 | 0 | 1 | 5 | 0.000 | `agentes_actuadores/visualizador_bateria.py` |
| 20 | `ControladorTemperatura` | 7 | 0 | 0 | 0 | 1 | 0.000 | `servicios_dominio/controlador_climatizador.py` |
| 21 | `Inicializador` | 7 | 0 | 0 | 0 | 6 | 0.000 | `servicios_aplicacion/inicializador.py` |
| 22 | `GestorClimatizador` | 7 | 0 | 0 | 0 | 4 | 0.000 | `gestores_entidades/gestor_climatizador.py` |
| 23 | `SeteoTemperatura` | 7 | 1 | 0 | 1 | 2 | 0.000 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 24 | `VisualizadorTemperaturaSocket` | 7 | 1 | 0 | 2 | 7 | 0.000 | `agentes_actuadores/visualizador_temperatura.py` |
| 25 | `VisualizadorBateriaSocket` | 7 | 1 | 0 | 2 | 7 | 0.000 | `agentes_actuadores/visualizador_bateria.py` |
| 26 | `FactoryClimatizador` | 7 | 0 | 0 | 3 | 3 | 0.000 | `configurador/factory_climatizador.py` |
| 27 | `FactoryProxySensorTemperatura` | 7 | 0 | 0 | 3 | 3 | 0.000 | `configurador/factory_sensor_temperatura.py` |
| 28 | `FactoryProxyBateria` | 7 | 0 | 0 | 3 | 3 | 0.000 | `configurador/factory_proxy_bateria.py` |
| 29 | `FactorySelectorTemperatura` | 7 | 0 | 0 | 3 | 3 | 0.000 | `configurador/factory_selector_temperatura.py` |
| 30 | `FactorySeteoTemperatura` | 7 | 0 | 0 | 3 | 3 | 0.000 | `configurador/factory_seteo_temperatura.py` |
| 31 | `OperadorSecuencial` | 6 | 0 | 0 | 2 | 7 | 0.000 | `servicios_aplicacion/operador_secuencial.py` |
| 32 | `Lanzador` | 6 | 0 | 0 | 9 | 12 | 0.000 | `servicios_aplicacion/lanzador.py` |
| 33 | `VisualizadorClimatizadorApi` | 6 | 1 | 0 | 1 | 4 | 0.000 | `agentes_actuadores/visualizador_climatizador.py` |
| 34 | `ProxyBateriaArchivo` | 5 | 1 | 0 | 2 | 4 | 0.000 | `agentes_sensores/proxy_bateria.py` |
| 35 | `ProxySensorTemperaturaArchivo` | 5 | 1 | 0 | 2 | 5 | 0.000 | `agentes_sensores/proxy_sensor_temperatura.py` |
| 36 | `VisualizadorClimatizadorSocket` | 5 | 1 | 0 | 2 | 6 | 0.000 | `agentes_actuadores/visualizador_climatizador.py` |
| 37 | `FactoryActuadorClimatizador` | 5 | 0 | 0 | 2 | 2 | 0.000 | `configurador/factory_actuador_climatizador.py` |
| 38 | `Climatizador` | 4 | 1 | 0 | 1 | 3 | 1.000 | `entidades/climatizador.py` |
| 39 | `Calefactor` | 4 | 1 | 0 | 1 | 3 | 1.000 | `entidades/climatizador.py` |
| 40 | `AbsVisualizadorBateria` | 4 | 0 | 3 | 1 | 2 | 0.000 | `entidades/abs_visualizador_bateria.py` |
| 41 | `AbsVisualizadorTemperatura` | 4 | 0 | 3 | 1 | 2 | 0.000 | `entidades/abs_visualizador_temperatura.py` |
| 42 | `Presentador` | 4 | 0 | 0 | 0 | 3 | 0.000 | `servicios_aplicacion/presentador.py` |
| 43 | `VisualizadorTemperatura` | 4 | 1 | 0 | 1 | 4 | 0.000 | `agentes_actuadores/visualizador_temperatura.py` |
| 44 | `VisualizadorBateria` | 4 | 1 | 0 | 1 | 4 | 0.000 | `agentes_actuadores/visualizador_bateria.py` |
| 45 | `AbsProxyActuadorClimatizador` | 3 | 0 | 1 | 1 | 1 | 0.000 | `entidades/abs_actuador_climatizador.py` |
| 46 | `AbsProxyBateria` | 3 | 0 | 2 | 1 | 1 | 0.000 | `entidades/abs_bateria.py` |
| 47 | `AbsVisualizadorClimatizador` | 3 | 0 | 3 | 1 | 1 | 0.000 | `entidades/abs_visualizador_climatizador.py` |
| 48 | `AbsProxySensorTemperatura` | 3 | 0 | 2 | 1 | 1 | 0.000 | `entidades/abs_sensor_temperatura.py` |
| 49 | `AbsSeteoTemperatura` | 3 | 0 | 2 | 1 | 1 | 0.000 | `servicios_aplicacion/abs_seteo_temperatura.py` |
| 50 | `AbsSelectorTemperatura` | 3 | 0 | 2 | 1 | 1 | 0.000 | `servicios_aplicacion/abs_selector_temperatura.py` |
| 51 | `VisualizadorClimatizador` | 3 | 1 | 0 | 1 | 3 | 0.000 | `agentes_actuadores/visualizador_climatizador.py` |
| 52 | `AbsRegistrador` | 3 | 0 | 2 | 0 | 1 | 0.000 | `registrador/registrador.py` |
| 53 | `AbsAuditor` | 3 | 0 | 1 | 0 | 1 | 0.000 | `registrador/registrador.py` |

---

## 8. CONCLUSIONES Y RECOMENDACIONES

### 8.1 Puntos Fuertes ⭐

1. **Baja complejidad promedio**: WMC=7.58 indica clases simples y mantenibles
2. **Bajo acoplamiento promedio**: CBO=2.04 muestra buen diseño modular
3. **Herencia limitada**: DIT=0.38 evita complejidad conceptual excesiva
4. **Baja complejidad de respuesta**: RFC=5.32 facilita testing
6. **Alta cohesión**: LCOM=0.077 indica responsabilidades bien definidas

### 8.2 Áreas de Mejora ⚠️

1. **Clases con WMC > 15**: 5 clases muy complejas
   - `Configurador` (WMC=38)
   - `SeteoTemperaturaSocket` (WMC=17)
   - `SelectorTemperaturaSocket` (WMC=17)
   - **Acción**: Aplicar **Extract Method** o **Extract Class**

2. **Clases con CBO > 5**: 2 clases con alto acoplamiento
   - `Configurador` (CBO=12)
   - `Lanzador` (CBO=9)
   - **Acción**: Aplicar **Dependency Injection**

### 8.3 Indicadores Clave (KPI)

| Indicador | Valor Actual | Umbral | Estado |
|-----------|--------------|--------|--------|
| WMC Promedio | 7.58 | ≤ 10 | ✅ |
| CBO Promedio | 2.04 | ≤ 5 | ✅ |
| RFC Promedio | 5.32 | ≤ 20 | ✅ |
| DIT Promedio | 0.38 | ≤ 3 | ✅ |
| LCOM Promedio | 0.077 | ≤ 0.5 | ✅ |
| % Clases WMC ≤ 5 | 37.7% | ≥ 60% | ❌ |
| % Clases CBO ≤ 2 | 69.8% | ≥ 60% | ✅ |

### 8.4 Calificación General

**Métricas CK del Proyecto**: **8.0/10** ✅

- ✅ WMC: 8/10
- ✅ CBO: 8/10
- ✅ RFC: 10/10
- ✅ DIT: 10/10
- ✅ LCOM: 10/10

---

**Fin del Reporte de Métricas CK**

*Generado con: Script personalizado basado en AST de Python + radon*
*Fecha: 2025-12-16 09:07:41*