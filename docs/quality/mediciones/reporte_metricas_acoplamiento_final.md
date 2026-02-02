# REPORTE DE MÉTRICAS DE ACOPLAMIENTO
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-11
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de acoplamiento evalúan el grado de interdependencia entre módulos y clases del sistema. Bajo acoplamiento indica un diseño modular y mantenible.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Módulos analizados** | 49 | Archivos Python de producción |
| **CBO Promedio** | 4.96 | ✅ Bajo acoplamiento |
| **Fan-In Promedio** | 4.33 | Módulos que dependen de este |
| **Fan-Out Promedio** | 0.63 | Módulos de los que depende |
| **Instability Promedio** | 0.124 | ✅ Sistema estable |
| **Dependencias Internas** | 31 | Entre módulos del proyecto |
| **Dependencias Externas** | 58 | Librerías de terceros |
| **Ciclos de Dependencias** | 3 | ❌ Ciclos detectados |

### Distribución por Nivel de Acoplamiento

| Nivel | Módulos | Porcentaje | Criterio (CBO) |
|-------|---------|------------|----------------|
| **Bajo** | 28 | 57.1% | CBO ≤ 5 |
| **Medio** | 21 | 42.9% | 5 < CBO ≤ 10 |
| **Alto** | 0 | 0.0% | CBO > 10 |

### Distribución por Estabilidad

| Nivel | Módulos | Porcentaje | Criterio (I) |
|-------|---------|------------|--------------|
| **Estable** | 44 | 89.8% | I < 0.3 |
| **Semi-estable** | 4 | 8.2% | 0.3 ≤ I < 0.7 |
| **Inestable** | 1 | 2.0% | I ≥ 0.7 |

**Interpretación**: ⚠️ Revisar módulos con alto acoplamiento

---

## 1. MÉTRICAS DE ACOPLAMIENTO EXPLICADAS

### 1.1 CBO (Coupling Between Objects)

**Menor es mejor** - Número total de clases/módulos con los que este módulo está acoplado.

```
CBO = Ca + Ce
```

- **Rango**: [0, ∞)
- **Interpretación**:
  - 0-5: Bajo acoplamiento (ideal)
  - 6-10: Acoplamiento moderado
  - > 10: Alto acoplamiento (refactorizar)

### 1.2 Fan-In y Fan-Out

#### Fan-In (Ca - Afferent Coupling)
**Mayor es mejor para módulos centrales** - Número de módulos que dependen de este.

- Indica qué tan "usado" es el módulo
- Alto Fan-In → Módulo central/estable
- Responsabilidad: cambios afectan a muchos

#### Fan-Out (Ce - Efferent Coupling)
**Menor es mejor** - Número de módulos de los que este depende.

- Indica qué tan "dependiente" es el módulo
- Alto Fan-Out → Módulo inestable
- Cambios en dependencias afectan a este módulo

### 1.3 Instability (I)

**Robert C. Martin** - Mide la resistencia al cambio.

```
I = Ce / (Ca + Ce)
```

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0 = Máxima estabilidad (solo Fan-In, no depende de nadie)
  - 0.5 = Equilibrio
  - 1.0 = Máxima inestabilidad (solo Fan-Out, nadie depende de él)

**Principio**: Módulos estables (I bajo) deberían ser abstractos. Módulos inestables (I alto) deberían ser concretos.

### 1.4 Afferent Coupling (Ca) y Efferent Coupling (Ce)

- **Ca (Afferent)**: Responsabilidad - ¿Cuántos dependen de mí?
- **Ce (Efferent)**: Independencia - ¿De cuántos dependo yo?

**Ideal**: Alto Ca, bajo Ce para módulos de dominio (estables y reutilizables).

---

## 2. ESTADÍSTICAS GLOBALES

### 2.1 Resumen de Métricas

| Métrica | Promedio | Mínimo | Máximo | Total | Estado |
|---------|----------|--------|--------|-------|--------|
| **CBO** | 4.96 | 0 | 10 | - | ✅ |
| **Fan-In (Ca)** | 4.33 | 0 | 9 | 212 | - |
| **Fan-Out (Ce)** | 0.63 | 0 | 4 | 31 | ✅ |
| **Instability** | 0.124 | 0.000 | 1.000 | - | ⚠️ |
| **Deps Internas** | 0.6 | - | - | 31 | - |
| **Deps Externas** | 1.2 | - | - | 58 | - |

### 2.2 Ratio de Dependencias

| Tipo | Cantidad | Porcentaje |
|------|----------|------------|
| **Internas** (proyecto) | 31 | 34.8% |
| **Externas** (librerías) | 58 | 65.2% |
| **TOTAL** | 89 | 100% |

---

## 3. TOP 15 MÓDULOS MÁS ACOPLADOS

Módulos con mayor CBO (mayor acoplamiento) que requieren atención:

| # | Módulo | CBO | Fan-In | Fan-Out | I | Deps Int | Deps Ext | Estado |
|---|--------|-----|--------|---------|---|----------|----------|--------|
| 1 | `climatizador` | 10 | 9 | 1 | 0.100 | 1 | 1 | ⚠️ |
| 2 | `__init__` | 9 | 9 | 0 | 0.000 | 0 | 0 | ⚠️ |
| 3 | `lanzador` | 9 | 5 | 4 | 0.444 | 4 | 0 | ⚠️ |
| 4 | `ambiente` | 9 | 9 | 0 | 0.000 | 0 | 0 | ⚠️ |
| 5 | `abs_actuador_climatizador` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 6 | `abs_bateria` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 7 | `bateria` | 9 | 9 | 0 | 0.000 | 0 | 0 | ⚠️ |
| 8 | `abs_visualizador_bateria` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 9 | `abs_visualizador_climatizador` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 10 | `abs_visualizador_temperatura` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 11 | `abs_sensor_temperatura` | 9 | 9 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 12 | `selector_entrada` | 7 | 6 | 1 | 0.143 | 1 | 0 | ⚠️ |
| 13 | `inicializador` | 6 | 6 | 0 | 0.000 | 0 | 1 | ⚠️ |
| 14 | `operador_paralelo` | 6 | 5 | 1 | 0.167 | 1 | 2 | ⚠️ |
| 15 | `operador_secuencial` | 6 | 5 | 1 | 0.167 | 1 | 2 | ⚠️ |

**Observaciones**:
- Módulo con mayor acoplamiento: `climatizador` (CBO=10)
- CBO > 10 indica alto acoplamiento (requiere refactorización)
- **Recomendación**: Aplicar **Dependency Inversion** y **Interface Segregation**

**Análisis del módulo más acoplado**:
- **climatizador**: CBO=10, Fan-In=9, Fan-Out=1
  - Es un módulo central (alto Fan-In)
  - Instability: 0.100 (Estable)

---

## 4. MÓDULOS POR ESTABILIDAD

### 4.1 Top 10 Módulos Más Estables (I < 0.3)

Módulos estables que son usados por otros (alto Fan-In, bajo Fan-Out):

| # | Módulo | I | Ca | Ce | CBO | Interpretación |
|---|--------|---|----|----|-----|----------------|
| 1 | `inicializador` | 0.000 | 6 | 0 | 6 | Núcleo estable |
| 2 | `__init__` | 0.000 | 9 | 0 | 9 | Núcleo estable |
| 3 | `presentador` | 0.000 | 6 | 0 | 6 | Núcleo estable |
| 4 | `abs_seteo_temperatura` | 0.000 | 6 | 0 | 6 | Núcleo estable |
| 5 | `abs_selector_temperatura` | 0.000 | 6 | 0 | 6 | Núcleo estable |
| 6 | `registrador` | 0.000 | 2 | 0 | 2 | Núcleo estable |
| 7 | `gestor_climatizador` | 0.000 | 1 | 0 | 1 | Núcleo estable |
| 8 | `gestor_ambiente` | 0.000 | 1 | 0 | 1 | Núcleo estable |
| 9 | `gestor_bateria` | 0.000 | 1 | 0 | 1 | Núcleo estable |
| 10 | `controlador_climatizador` | 0.000 | 1 | 0 | 1 | Núcleo estable |

**Interpretación**:
- Módulos con I = 0.0 son completamente estables (nadie depende de otros)
- Estos módulos son hojas del sistema
- Cambios en estos módulos no afectan a otros

### 4.2 Top 10 Módulos Más Inestables (I ≥ 0.7)

Módulos inestables que dependen de muchos otros (bajo Fan-In, alto Fan-Out):

| # | Módulo | I | Ca | Ce | CBO | Interpretación |
|---|--------|---|----|----|-----|----------------|
| 1 | `ejecutar` | 1.000 | 0 | 2 | 2 | Alto nivel |

**Interpretación**:
- Módulos con I = 1.0 son completamente inestables (solo dependen, nadie depende de ellos)
- Estos módulos son puntos de entrada o adaptadores
- Cambios en sus dependencias los afectan directamente
- **Normal en servicios de aplicación y adaptadores**

---

## 5. ANÁLISIS POR PAQUETE

Métricas de acoplamiento promedio por paquete/módulo:

| Paquete | Módulos | CBO Avg | Fan-In | Fan-Out | I Avg | Deps Int | Deps Ext |
|---------|---------|---------|--------|---------|-------|----------|----------|
| `actores_externos/` | 7 | 0.00 | 0.0 | 0.0 | 0.000 | 0 | 29 |
| `agentes_actuadores/` | 4 | 5.25 | 4.0 | 1.2 | 0.233 | 5 | 7 |
| `agentes_sensores/` | 4 | 5.25 | 4.0 | 1.2 | 0.233 | 5 | 5 |
| `configurador/` | 10 | 5.00 | 3.9 | 1.1 | 0.218 | 11 | 2 |
| `entidades/` | 10 | 9.10 | 9.0 | 0.1 | 0.010 | 1 | 7 |
| `gestores_entidades/` | 3 | 1.00 | 1.0 | 0.0 | 0.000 | 0 | 0 |
| `registrador/` | 1 | 2.00 | 2.0 | 0.0 | 0.000 | 0 | 1 |
| `root/` | 1 | 2.00 | 0.0 | 2.0 | 1.000 | 2 | 0 |
| `servicios_aplicacion/` | 8 | 6.50 | 5.6 | 0.9 | 0.115 | 7 | 7 |
| `servicios_dominio/` | 1 | 1.00 | 1.0 | 0.0 | 0.000 | 0 | 0 |

**Interpretación**:
- **Paquete más acoplado**: `entidades/` (CBO=9.10)
- **Paquete menos acoplado**: `actores_externos/` (CBO=0.00)
- ⚠️ Revisar paquetes con alto acoplamiento

---

## 6. CICLOS DE DEPENDENCIAS

⚠️ **Se detectaron 3 ciclo(s) de dependencias**

Los ciclos de dependencias son problemáticos porque:
- Dificultan el testing independiente
- Complican el mantenimiento
- Impiden la modularidad
- Causan problemas de compilación/carga

### Ciclos Detectados:

| # | Ciclo | Longitud | Severidad |
|---|-------|----------|-----------|
| 1 | `configurador → configurador` | 2 | Baja |
| 2 | `configurador` | 1 | Baja |
| 3 | `configurador` | 1 | Baja |

**Recomendaciones para romper ciclos**:
1. **Dependency Inversion Principle**: Introducir interfaces/abstracciones
2. **Extract Interface**: Separar dependencias circulares con contratos
3. **Move Method/Class**: Reorganizar responsabilidades
4. **Event-Driven**: Usar eventos en lugar de llamadas directas

---

## 7. DEPENDENCIAS EXTERNAS

Librerías de terceros más utilizadas en el proyecto:

| # | Librería | Uso (módulos) | Tipo |
|---|----------|---------------|------|
| 1 | `socket` | 14 | Network |
| 2 | `os` | 10 | Core |
| 3 | `abc` | 10 | Std Lib |
| 4 | `time` | 9 | Std Lib |
| 5 | `datetime` | 6 | Std Lib |
| 6 | `json` | 5 | Std Lib |
| 7 | `requests` | 3 | HTTP |
| 8 | `threading` | 1 | Std Lib |

**Observaciones**:
- Total de librerías externas únicas: 8
- Librería más usada: `socket` (14 módulos) si sorted_external else 'N/A'
- Dependencias externas bien distribuidas

---

## 8. MATRIZ DE DEPENDENCIAS (Top 10)

Dependencias internas entre los módulos más acoplados:

| Módulo | Depende de (Fan-Out) |
|--------|---------------------|
| `climatizador` | `servicios_dominio` |
| `__init__` | - |
| `lanzador` | `entidades`, `servicios_aplicacion`, `configurador`, `gestores_entidades` |
| `ambiente` | - |
| `abs_actuador_climatizador` | - |
| `abs_bateria` | - |
| `bateria` | - |
| `abs_visualizador_bateria` | - |
| `abs_visualizador_climatizador` | - |
| `abs_visualizador_temperatura` | - |

---

## 9. LISTA COMPLETA DE MÓDULOS

Todos los módulos ordenados por CBO (descendente):

| # | Módulo | CBO | Fan-In | Fan-Out | I | Archivo |
|---|--------|-----|--------|---------|---|---------|
| 1 | `climatizador` | 10 | 9 | 1 | 0.100 | `entidades/climatizador.py` |
| 2 | `__init__` | 9 | 9 | 0 | 0.000 | `entidades/__init__.py` |
| 3 | `lanzador` | 9 | 5 | 4 | 0.444 | `servicios_aplicacion/lanzador.py` |
| 4 | `ambiente` | 9 | 9 | 0 | 0.000 | `entidades/ambiente.py` |
| 5 | `abs_actuador_climatizador` | 9 | 9 | 0 | 0.000 | `entidades/abs_actuador_climatizador.py` |
| 6 | `abs_bateria` | 9 | 9 | 0 | 0.000 | `entidades/abs_bateria.py` |
| 7 | `bateria` | 9 | 9 | 0 | 0.000 | `entidades/bateria.py` |
| 8 | `abs_visualizador_bateria` | 9 | 9 | 0 | 0.000 | `entidades/abs_visualizador_bateria.py` |
| 9 | `abs_visualizador_climatizador` | 9 | 9 | 0 | 0.000 | `entidades/abs_visualizador_climatizador.py` |
| 10 | `abs_visualizador_temperatura` | 9 | 9 | 0 | 0.000 | `entidades/abs_visualizador_temperatura.py` |
| 11 | `abs_sensor_temperatura` | 9 | 9 | 0 | 0.000 | `entidades/abs_sensor_temperatura.py` |
| 12 | `selector_entrada` | 7 | 6 | 1 | 0.143 | `servicios_aplicacion/selector_entrada.py` |
| 13 | `inicializador` | 6 | 6 | 0 | 0.000 | `servicios_aplicacion/inicializador.py` |
| 14 | `operador_paralelo` | 6 | 5 | 1 | 0.167 | `servicios_aplicacion/operador_paralelo.py` |
| 15 | `operador_secuencial` | 6 | 5 | 1 | 0.167 | `servicios_aplicacion/operador_secuencial.py` |
| 16 | `presentador` | 6 | 6 | 0 | 0.000 | `servicios_aplicacion/presentador.py` |
| 17 | `abs_seteo_temperatura` | 6 | 6 | 0 | 0.000 | `servicios_aplicacion/abs_seteo_temperatura.py` |
| 18 | `abs_selector_temperatura` | 6 | 6 | 0 | 0.000 | `servicios_aplicacion/abs_selector_temperatura.py` |
| 19 | `factory_actuador_climatizador` | 6 | 4 | 2 | 0.333 | `configurador/factory_actuador_climatizador.py` |
| 20 | `proxy_selector_temperatura` | 6 | 4 | 2 | 0.333 | `agentes_sensores/proxy_selector_temperatura.py` |
| 21 | `actuador_climatizador` | 6 | 4 | 2 | 0.333 | `agentes_actuadores/actuador_climatizador.py` |
| 22 | `factory_visualizador_temperatura` | 5 | 4 | 1 | 0.200 | `configurador/factory_visualizador_temperatura.py` |
| 23 | `factory_climatizador` | 5 | 4 | 1 | 0.200 | `configurador/factory_climatizador.py` |
| 24 | `factory_visualizador_climatizador` | 5 | 4 | 1 | 0.200 | `configurador/factory_visualizador_climatizador.py` |
| 25 | `factory_sensor_temperatura` | 5 | 4 | 1 | 0.200 | `configurador/factory_sensor_temperatura.py` |
| 26 | `factory_proxy_bateria` | 5 | 4 | 1 | 0.200 | `configurador/factory_proxy_bateria.py` |
| 27 | `factory_selector_temperatura` | 5 | 4 | 1 | 0.200 | `configurador/factory_selector_temperatura.py` |
| 28 | `factory_seteo_temperatura` | 5 | 4 | 1 | 0.200 | `configurador/factory_seteo_temperatura.py` |
| 29 | `factory_visualizador_bateria` | 5 | 4 | 1 | 0.200 | `configurador/factory_visualizador_bateria.py` |
| 30 | `proxy_bateria` | 5 | 4 | 1 | 0.200 | `agentes_sensores/proxy_bateria.py` |
| 31 | `proxy_seteo_temperatura` | 5 | 4 | 1 | 0.200 | `agentes_sensores/proxy_seteo_temperatura.py` |
| 32 | `proxy_sensor_temperatura` | 5 | 4 | 1 | 0.200 | `agentes_sensores/proxy_sensor_temperatura.py` |
| 33 | `visualizador_climatizador` | 5 | 4 | 1 | 0.200 | `agentes_actuadores/visualizador_climatizador.py` |
| 34 | `visualizador_temperatura` | 5 | 4 | 1 | 0.200 | `agentes_actuadores/visualizador_temperatura.py` |
| 35 | `visualizador_bateria` | 5 | 4 | 1 | 0.200 | `agentes_actuadores/visualizador_bateria.py` |
| 36 | `configurador` | 4 | 3 | 1 | 0.250 | `configurador/configurador.py` |
| 37 | `ejecutar` | 2 | 0 | 2 | 1.000 | `ejecutar.py` |
| 38 | `registrador` | 2 | 2 | 0 | 0.000 | `registrador/registrador.py` |
| 39 | `gestor_climatizador` | 1 | 1 | 0 | 0.000 | `gestores_entidades/gestor_climatizador.py` |
| 40 | `gestor_ambiente` | 1 | 1 | 0 | 0.000 | `gestores_entidades/gestor_ambiente.py` |
| 41 | `gestor_bateria` | 1 | 1 | 0 | 0.000 | `gestores_entidades/gestor_bateria.py` |
| 42 | `controlador_climatizador` | 1 | 1 | 0 | 0.000 | `servicios_dominio/controlador_climatizador.py` |
| 43 | `simulador_bateria` | 0 | 0 | 0 | 0.000 | `actores_externos/simulador_bateria.py` |
| 44 | `simulador_seteo_temperatura_deseada` | 0 | 0 | 0 | 0.000 | `actores_externos/simulador_seteo_temperatura_deseada.py` |
| 45 | `simulador_temperatura` | 0 | 0 | 0 | 0.000 | `actores_externos/simulador_temperatura.py` |
| 46 | `cartel_climatizador` | 0 | 0 | 0 | 0.000 | `actores_externos/cartel_climatizador.py` |
| 47 | `cartel_bateria` | 0 | 0 | 0 | 0.000 | `actores_externos/cartel_bateria.py` |
| 48 | `cartel_temperatura` | 0 | 0 | 0 | 0.000 | `actores_externos/cartel_temperatura.py` |
| 49 | `simulador_selector_temperatura` | 0 | 0 | 0 | 0.000 | `actores_externos/simulador_selector_temperatura.py` |

---

## 10. CONCLUSIONES Y RECOMENDACIONES

### 10.1 Puntos Fuertes ⭐

1. **Bajo acoplamiento promedio**: CBO=4.96 indica diseño modular
2. **Mayoría con bajo acoplamiento**: 57% con CBO ≤ 5
3. **Fan-Out controlado**: 0.63 dependencias promedio
4. **3 ciclo(s) detectado(s)**: Requiere atención

### 10.2 Áreas de Mejora ⚠️

1. **Módulos con CBO > 10**: 0 módulos
   - **Acción**: Aplicar **Dependency Inversion**, extraer interfaces

2. **Ciclos de dependencias**: 3 ciclo(s) detectados
   - `configurador -> configurador`
   - `configurador`
   - `configurador`
   - **Acción**: Romper ciclos con abstracciones o eventos

3. **Módulos inestables (I ≥ 0.9)**: 1 módulos
   - `ejecutar` (I=1.000)
   - **Acción**: Revisar si deberían tener más responsabilidad


### 10.3 Plan de Acción Sugerido

#### Prioridad Alta
1. Eliminar 3 ciclo(s) de dependencias
2. Refactorizar 0 módulos con CBO > 10
3. Revisar módulos con alto Fan-Out

#### Prioridad Media
1. Reducir Fan-Out de módulos con Fan-Out > 5
2. Aplicar **Interface Segregation** en módulos muy acoplados
3. Introducir **Dependency Injection** para módulos inestables

#### Prioridad Baja
1. Optimizar módulos con CBO 5-10
2. Establecer umbral máximo CBO = 5 para nuevos módulos
3. Automatizar detección de ciclos en CI/CD

### 10.4 Indicadores Clave (KPI)

| Indicador | Valor Actual | Umbral | Estado |
|-----------|--------------|--------|--------|
| CBO Promedio | 4.96 | ≤ 5 | ✅ |
| Fan-Out Promedio | 0.63 | ≤ 3 | ✅ |
| Instability Promedio | 0.124 | 0.3-0.7 | ⚠️ |
| % Bajo Acoplamiento | 57.1% | ≥ 70% | ❌ |
| Ciclos de Dependencias | 3 | 0 | ❌ |
| Módulos CBO > 10 | 0 | 0 | ✅ |

### 10.5 Calificación General

**Métricas de Acoplamiento del Proyecto**: **6.2/10** 

- ✅ CBO: 8/10
- ❌ Ciclos: 2/10
- ✅ Fan-Out: 10/10
- ⚠️ Distribución: 5/10

---

## 11. REFERENCIAS

### Interpretación de Métricas

#### CBO (Coupling Between Objects)
- **0-5**: Bajo acoplamiento (ideal)
- **6-10**: Acoplamiento moderado
- **11-20**: Alto acoplamiento (refactorizar)
- **> 20**: Muy alto acoplamiento (diseño problemático)

#### Instability (I)
- **0.0-0.3**: Estable (núcleo, dominio, entidades)
- **0.3-0.7**: Semi-estable (servicios, casos de uso)
- **0.7-1.0**: Inestable (adaptadores, UI, puntos de entrada)

#### Fan-In (Afferent Coupling)
- **0**: Módulo hoja, no usado
- **1-3**: Uso moderado
- **> 3**: Módulo central/core

#### Fan-Out (Efferent Coupling)
- **0**: Módulo independiente
- **1-3**: Dependencias controladas
- **> 5**: Muchas dependencias (reducir)

### Principios de Diseño

#### Stable Dependencies Principle (SDP)
- Depender de módulos más estables que uno mismo
- I(dependencia) < I(dependiente)

#### Stable Abstractions Principle (SAP)
- Módulos estables deben ser abstractos
- Módulos inestables deben ser concretos

#### Acyclic Dependencies Principle (ADP)
- El grafo de dependencias debe ser acíclico (DAG)
- Los ciclos indican problemas de diseño

### Técnicas de Refactorización

1. **Dependency Inversion**: Invertir dependencias usando interfaces
2. **Extract Interface**: Crear contratos entre módulos
3. **Facade Pattern**: Simplificar dependencias complejas
4. **Event-Driven**: Desacoplar con eventos/mensajes
5. **Dependency Injection**: Inyectar dependencias desde afuera

---

**Fin del Reporte de Métricas de Acoplamiento**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-11 12:22:21*
*Próximos análisis recomendados: Métricas de Robert C. Martin (Abstractness), Seguridad*
