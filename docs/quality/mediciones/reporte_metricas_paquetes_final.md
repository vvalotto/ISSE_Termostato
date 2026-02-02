# REPORTE DE MÉTRICAS DE PAQUETES (ROBERT C. MARTIN)
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-14
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Paquetes de código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de paquetes de Robert C. Martin evalúan la salud arquitectónica del sistema a nivel de módulos/paquetes, analizando el balance entre abstracción y estabilidad.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Paquetes analizados** | 9 | Módulos principales del proyecto |
| **Ca Promedio** | 1.33 | Paquetes que dependen de este |
| **Ce Promedio** | 1.33 | Paquetes de los que depende |
| **Instability Promedio (I)** | 0.35 | ✅ Sistema muy estable |
| **Abstractness Promedio (A)** | 0.21 | ⚠️ Nivel bajo de abstracción |
| **Distance Promedio (D)** | 0.44 | ⚠️ Revisar diseño |
| **Total de Clases** | 53 | Clases en todos los paquetes |
| **Clases Abstractas** | 11 (20.8%) | Nivel de abstracción global |

### Distribución por Zonas (Diagrama A-I)

| Zona | Paquetes | Porcentaje | Interpretación |
|------|----------|------------|----------------|
| **Zona Principal** | 4 | 44.4% | ✅ Equilibrio ideal A + I ≈ 1 |
| **Aceptable** | 2 | 22.2% | ✅ Cerca de la secuencia |
| **Zona de Dolor** | 3 | 33.3% | ⚠️ Concreto y estable (difícil cambiar) |
| **Zona de Inutilidad** | 0 | 0.0% | ✅ Sin código muerto |

**Interpretación**: ⚠️ Distribución mejorable - algunos paquetes en Zona de Dolor

---

## 1. MÉTRICAS DE PAQUETES EXPLICADAS

### 1.1 La Secuencia Principal (Main Sequence)

**Principio fundamental**: Los paquetes deben estar en la línea donde **A + I = 1**

Esta línea representa el balance ideal entre:
- **Abstracción (A)**: Cuánto del paquete son interfaces/abstracciones
- **Inestabilidad (I)**: Qué tan susceptible es el paquete a cambios

```
  A (Abstractness)
  1 │ * registrador (ideal)
    │  Zona de          Secuencia
    │  Inutilidad ↗    Principal
0.5 │    * entidades  ↗  (A + I = 1)
    │  ↗
  0 └──────────────────────────────
    0               0.5           1
                        I (Instability)
```

### 1.2 Métricas Individuales

#### Ca (Afferent Coupling)
**Mayor es mejor para paquetes centrales** - Número de paquetes que dependen de este.

- Mide la responsabilidad del paquete
- Alto Ca → Paquete estable y central
- Cambios afectan a muchos dependientes

#### Ce (Efferent Coupling)
**Menor es mejor** - Número de paquetes de los que este depende.

- Mide la independencia del paquete
- Alto Ce → Paquete inestable
- Afectado por cambios en dependencias

#### I (Instability)
```
I = Ce / (Ca + Ce)
```

- **Rango**: [0, 1]
- **0.0**: Máxima estabilidad (solo dependientes, no depende de nadie)
- **1.0**: Máxima inestabilidad (solo dependencias, nadie depende de él)

#### A (Abstractness)
```
A = Na / Nc
```

- **Na**: Número de clases abstractas (ABC, Protocol, interfaces)
- **Nc**: Número total de clases
- **Rango**: [0, 1]
- **0.0**: Totalmente concreto
- **1.0**: Totalmente abstracto

#### D (Distance from Main Sequence)
```
D = |A + I - 1|
```

- **Rango**: [0, 1]
- **0.0**: En la secuencia principal (ideal)
- **Interpretación**:
  - D < 0.2: Excelente
  - D < 0.3: Bueno
  - D ≥ 0.5: Problemático

#### D' (Normalized Distance)
```
D' = D / √2
```

- **Rango**: [0, ~0.71]
- Normaliza D para visualización

### 1.3 Las Cuatro Zonas

#### 🟢 Zona Principal (A + I ≈ 1, D ≈ 0)
- Balance ideal entre abstracción e inestabilidad
- Paquetes con buen diseño
- **Objetivo**: Maximizar paquetes aquí

#### 🟡 Zona Aceptable (D < 0.4)
- Cerca de la secuencia principal
- Diseño aceptable
- Puede optimizarse

#### 🔴 Zona de Dolor (A ≈ 0, I ≈ 0)
- Concreto y estable
- Difícil de cambiar
- Muchos dependen, pero es implementación
- **Problema**: Cambios son costosos

#### 🔴 Zona de Inutilidad (A ≈ 1, I ≈ 1)
- Abstracto e inestable
- Nadie lo usa
- **Problema**: Código muerto o mal diseñado

---

## 2. ESTADÍSTICAS GLOBALES

### 2.1 Resumen de Métricas por Paquete

| Métrica | Promedio | Mínimo | Máximo | Estado |
|---------|----------|--------|--------|--------|
| **Ca** | 1.33 | 0 | 4 | - |
| **Ce** | 1.33 | 0 | 3 | - |
| **I** | 0.35 | 0.00 | 0.75 | ✅ |
| **A** | 0.21 | 0.00 | 1.00 | ⚠️ |
| **D** | 0.44 | 0.00 | 1.00 | ⚠️ |

### 2.2 Distribución de Clases

| Tipo | Cantidad | Porcentaje |
|------|----------|------------|
| **Clases Concretas** | 42 | 79.2% |
| **Clases Abstractas** | 11 | 20.8% |
| **TOTAL** | 53 | 100% |

**Interpretación**: ✅ Nivel aceptable de abstracción

---

## 3. ANÁLISIS DE TODOS LOS PAQUETES

Visión completa de las métricas de Robert C. Martin para cada paquete:

| # | Paquete | Ca | Ce | I | A | D | D' | Zona |
|---|---------|----|----|---|---|---|----|----|
| 1 | `entidades` | 4 | 1 | 0.20 | 0.64 | 0.16 | 0.11 | ✅ Zona Principal |
| 2 | `registrador` | 2 | 0 | 0.00 | 1.00 | 0.00 | 0.00 | ✅ Zona Principal |
| 3 | `servicios_aplicacion` | 1 | 3 | 0.75 | 0.25 | 0.00 | 0.00 | ✅ Zona Principal |
| 4 | `agentes_sensores` | 1 | 3 | 0.75 | 0.00 | 0.25 | 0.18 | ✅ Zona Principal |
| 5 | `configurador` | 1 | 3 | 0.75 | 0.00 | 0.25 | 0.18 | 🟡 Aceptable |
| 6 | `agentes_actuadores` | 1 | 2 | 0.67 | 0.00 | 0.33 | 0.23 | 🟡 Aceptable |
| 7 | `gestores_entidades` | 1 | 0 | 0.00 | 0.00 | 1.00 | 0.71 | 🔴 Zona de Dolor |
| 8 | `servicios_dominio` | 1 | 0 | 0.00 | 0.00 | 1.00 | 0.71 | 🔴 Zona de Dolor |
| 9 | `actores_externos` | 0 | 0 | 0.00 | 0.00 | 1.00 | 0.71 | 🔴 Zona de Dolor* |

*`actores_externos` contiene scripts de simulación, no clases OO.

**Lectura de la tabla**:
- **Ca alto, Ce bajo** → Paquete estable y central (núcleo)
- **Ce alto, Ca bajo** → Paquete inestable (adaptadores, puntos de entrada)
- **A alto** → Muchas abstracciones (interfaces, protocolos)
- **D bajo** → Cerca de la secuencia principal (buen diseño)

---

## 4. PAQUETES EN LA ZONA PRINCIPAL

Paquetes con diseño arquitectónico ideal (D < 0.3, A + I ≈ 1):

| Paquete | I | A | D | Ca | Ce | Clases | Abstractas |
|---------|---|---|---|----|----|--------|------------|
| `registrador` | 0.00 | 1.00 | 0.00 | 2 | 0 | 2 | 2 |
| `servicios_aplicacion` | 0.75 | 0.25 | 0.00 | 1 | 3 | 8 | 2 |
| `entidades` | 0.20 | 0.64 | 0.16 | 4 | 1 | 11 | 7 |
| `agentes_sensores` | 0.75 | 0.00 | 0.25 | 1 | 3 | 8 | 0 |

**Análisis**:
- ✅ 4 paquete(s) en la zona principal (44.4%)
- Estos paquetes tienen el balance ideal entre abstracción e inestabilidad
- **Mantener este diseño** como referencia para otros paquetes

---

## 5. PAQUETES EN ZONA DE DOLOR

Paquetes concretos y estables (A ≈ 0, I ≈ 0, difíciles de cambiar):

| Paquete | I | A | D | Ca | Ce | Problema | Recomendación |
|---------|---|---|---|----|----|----------|---------------|
| `gestores_entidades` | 0.00 | 0.00 | 1.00 | 1 | 0 | Estable sin abstracciones | Extraer interfaces |
| `servicios_dominio` | 0.00 | 0.00 | 1.00 | 1 | 0 | Estable sin abstracciones | Extraer interfaces |
| `actores_externos` | 0.00 | 0.00 | 1.00 | 0 | 0 | Scripts aislados | N/A (scripts) |

**Análisis**:
- ⚠️ 3 paquete(s) en zona de dolor (pero 1 es scripts de simulación)
- **Problema**: Son estables (muchos dependen) pero concretos (sin abstracciones)
- **Impacto**: Cambios son costosos porque afectan a muchos dependientes
- **Acción**: Aplicar **Dependency Inversion** - extraer interfaces/abstracciones

**Nota**: `actores_externos` contiene scripts de simulación independientes, no código OO tradicional. Su presencia en la Zona de Dolor es aceptable.

---

## 6. PAQUETES EN ZONA DE INUTILIDAD

Paquetes abstractos e inestables (A ≈ 1, I ≈ 1, no usados):

✅ No hay paquetes en la Zona de Inutilidad


---

## 7. ANÁLISIS DE ESTABILIDAD

### 7.1 Paquetes Más Estables (I ≈ 0)

Paquetes núcleo que deberían ser abstractos:

| # | Paquete | I | A | Ca | Ce | Cumple SAP* |
|---|---------|---|---|----|----|-----------  |
| 1 | `registrador` | 0.00 | 1.00 | 2 | 0 | ✅ |
| 2 | `gestores_entidades` | 0.00 | 0.00 | 1 | 0 | ⚠️ |
| 3 | `servicios_dominio` | 0.00 | 0.00 | 1 | 0 | ⚠️ |
| 4 | `entidades` | 0.20 | 0.64 | 4 | 1 | ✅ |

*SAP: Stable Abstractions Principle - Paquetes estables deben ser abstractos

**Interpretación**:
- Paquetes con I ≈ 0 son muy estables (muchos dependen de ellos)
- **Deberían tener A alto** (muchas abstracciones) según SAP
- `gestores_entidades` y `servicios_dominio` violan SAP

### 7.2 Paquetes Más Inestables (I ≈ 1)

Paquetes que deberían ser concretos (adaptadores, UI):

| # | Paquete | I | A | Ca | Ce | Cumple SAP* |
|---|---------|---|---|----|----|-----------  |
| 1 | `servicios_aplicacion` | 0.75 | 0.25 | 1 | 3 | ✅ |
| 2 | `agentes_sensores` | 0.75 | 0.00 | 1 | 3 | ✅ |
| 3 | `configurador` | 0.75 | 0.00 | 1 | 3 | ✅ |
| 4 | `agentes_actuadores` | 0.67 | 0.00 | 1 | 2 | ✅ |

*SAP: Paquetes inestables deben ser concretos (implementaciones)

**Interpretación**:
- Paquetes con I ≈ 1 son muy inestables (puntos de entrada, adaptadores)
- **Deberían tener A bajo** (pocas abstracciones) según SAP ✅
- Todos los paquetes inestables cumplen SAP correctamente

---

## 8. ANÁLISIS DE ABSTRACCIÓN

### 8.1 Paquetes Más Abstractos

| # | Paquete | A | Abstractas | Concretas | Total | Uso |
|---|---------|---|------------|-----------|-------|-----|
| 1 | `registrador` | 1.00 | 2 | 0 | 2 | 2 dependientes |
| 2 | `entidades` | 0.64 | 7 | 4 | 11 | 4 dependientes |
| 3 | `servicios_aplicacion` | 0.25 | 2 | 6 | 8 | 1 dependiente |

**Observaciones**:
- Paquete más abstracto: `registrador` (A=1.00) - 100% abstracciones
- `entidades` bien balanceado (A=0.64) - núcleo del dominio
- Total de abstracciones en el sistema: 11 (21%)
- ✅ Nivel saludable de abstracción en paquetes centrales

### 8.2 Paquetes Más Concretos

| # | Paquete | A | Abstractas | Concretas | Total | Estabilidad |
|---|---------|---|------------|-----------|-------|-------------|
| 1 | `gestores_entidades` | 0.00 | 0 | 3 | 3 | I=0.00 ⚠️ |
| 2 | `servicios_dominio` | 0.00 | 0 | 1 | 1 | I=0.00 ⚠️ |
| 3 | `agentes_sensores` | 0.00 | 0 | 8 | 8 | I=0.75 ✅ |
| 4 | `agentes_actuadores` | 0.00 | 0 | 10 | 10 | I=0.67 ✅ |
| 5 | `configurador` | 0.00 | 0 | 10 | 10 | I=0.75 ✅ |

**Observaciones**:
- Paquetes concretos son aceptables si son inestables (I alto) ✅
- Paquetes concretos Y estables (I bajo) están en Zona de Dolor ⚠️

---

## 9. DEPENDENCIAS ENTRE PAQUETES

### 9.1 Grafo de Dependencias

```
                    ┌─────────────────┐
                    │   registrador   │ A=1.0, I=0.0, D=0.0
                    │   (abstracto,   │
                    │    estable)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              │              ▼
    ┌─────────────────┐      │    ┌─────────────────┐
    │agentes_actuadores│     │    │ agentes_sensores│
    │  I=0.67, D=0.33 │      │    │  I=0.75, D=0.25 │
    └────────┬────────┘      │    └────────┬────────┘
             │               │             │
             │               │             ├───────────────────┐
             │               │             │                   │
             ▼               │             ▼                   ▼
    ┌─────────────────┐      │    ┌─────────────────┐  ┌───────────────┐
    │   entidades     │◄─────┴────┤servicios_aplicac│  │  configurador │
    │ A=0.64, I=0.20  │           │  I=0.75, D=0.00 │  │ I=0.75, D=0.25│
    │  D=0.16 (ideal) │           └────────┬────────┘  └───────┬───────┘
    └────────┬────────┘                    │                   │
             │                             │                   │
             ▼                             ▼                   │
    ┌─────────────────┐           ┌─────────────────┐          │
    │servicios_dominio│           │gestores_entidades│◄─────────┘
    │  I=0.0, D=1.0   │           │   I=0.0, D=1.0  │
    │  (zona dolor)   │           │   (zona dolor)  │
    └─────────────────┘           └─────────────────┘


    ┌─────────────────┐
    │ actores_externos│  (Aislado - simuladores/scripts)
    │   (no OO)       │
    └─────────────────┘
```

### 9.2 Dependencias Detalladas

| Paquete | Depende de (Ce) |
|---------|-----------------|
| `entidades` | `servicios_dominio` |
| `servicios_aplicacion` | `entidades`, `gestores_entidades`, `configurador` |
| `agentes_sensores` | `entidades`, `registrador`, `servicios_aplicacion` |
| `agentes_actuadores` | `entidades`, `registrador` |
| `configurador` | `entidades`, `agentes_sensores`, `agentes_actuadores` |
| `gestores_entidades` | (ninguno) |
| `servicios_dominio` | (ninguno) |
| `actores_externos` | (ninguno - scripts aislados) |
| `registrador` | (ninguno) |

### 9.3 Paquetes Más Utilizados (Mayor Ca)

| # | Paquete | Ca | Usado por |
|---|---------|----|----|
| 1 | `entidades` | 4 | `servicios_aplicacion`, `agentes_sensores`, `agentes_actuadores`, `configurador` |
| 2 | `registrador` | 2 | `agentes_sensores`, `agentes_actuadores` |
| 3 | `servicios_aplicacion` | 1 | `agentes_sensores` |
| 4 | `gestores_entidades` | 1 | `servicios_aplicacion` |
| 5 | `configurador` | 1 | `servicios_aplicacion` |
| 6 | `servicios_dominio` | 1 | `entidades` |

---

## 10. LA SECUENCIA PRINCIPAL - VISUALIZACIÓN

```
    Abstractness (A)
         1.0 │  * registrador (D=0.00)    ╲
             │     Zona de                  ╲  Secuencia
             │     Inutilidad                 ╲  Principal
             │                                  ╲
         0.5 │           * entidades (D=0.16)     ╲
             │                                      ╲
             │    * servicios_aplicacion (D=0.00)    ╲
         0.0 │──●────────────────●────────────●───────╲
             │  ↑ gestores_ent   │            ↑
             │  ↑ servicios_dom  │            agentes (D=0.25-0.33)
             │  Zona de          │            configurador
             │  Dolor            │
             └──────────────────────────────────────────
                0.0             0.5            1.0
                          Instability (I)

    ● = Paquetes concretos (A=0)
    * = Paquetes con abstracción

    Paquetes en la diagonal (A+I≈1) tienen diseño ideal
```

---

## 11. CONCLUSIONES Y RECOMENDACIONES

### 11.1 Puntos Fuertes ⭐

1. **44% en Zona Principal**: 4 de 9 paquetes tienen diseño ideal
2. **Sin código muerto**: 0 paquetes en Zona de Inutilidad
3. **Núcleo bien diseñado**: `entidades` (D=0.16) y `registrador` (D=0.00)
4. **Adaptadores correctos**: Paquetes inestables son concretos (cumplen SAP)
5. **Paquete de logging ideal**: `registrador` es 100% abstracto y estable

### 11.2 Áreas de Mejora ⚠️

1. **Paquetes en Zona de Dolor**: 2 paquetes OO
   - `gestores_entidades` (A=0.00, I=0.00)
   - `servicios_dominio` (A=0.00, I=0.00)
   - **Acción**: Extraer interfaces con **Dependency Inversion Principle**

2. **Distance Promedio alto**: D=0.44
   - **Acción**: Aumentar abstracción en paquetes estables

3. **Abstracción Global baja**: A=0.21
   - **Acción**: Agregar interfaces en paquetes centrales

### 11.3 Plan de Acción Sugerido

#### Prioridad Alta (Corto plazo)
1. **`gestores_entidades`**: Extraer `IGestorAmbiente`, `IGestorBateria`, `IGestorClimatizador`
2. **`servicios_dominio`**: Extraer `IControladorClimatizador`

#### Prioridad Media (Mediano plazo)
1. Reducir D en paquetes con D > 0.4
2. Incrementar abstracción global al 30%

#### Prioridad Baja (Largo plazo)
1. Establecer umbral D < 0.3 para todos los paquetes
2. Automatizar verificación de SAP y SDP en CI/CD

### 11.4 Indicadores Clave (KPI)

| Indicador | Valor Actual | Umbral | Estado |
|-----------|--------------|--------|--------|
| Distance Promedio (D) | 0.44 | < 0.3 | ⚠️ |
| Abstractness Promedio (A) | 0.21 | ≥ 0.3 | ⚠️ |
| Instability Promedio (I) | 0.35 | 0.3-0.7 | ✅ |
| % en Zona Principal | 44.4% | ≥ 30% | ✅ |
| Paquetes en Zona Dolor (OO) | 2 | 0 | ⚠️ |
| Paquetes en Zona Inutilidad | 0 | 0 | ✅ |

### 11.5 Calificación General

**Métricas de Paquetes del Proyecto**: **7.2/10** ⭐⭐⭐

| Aspecto | Puntuación | Observación |
|---------|------------|-------------|
| Distance | 6/10 | D=0.44 > umbral 0.3 |
| Abstractness | 6/10 | A=0.21 < umbral 0.3 |
| Zonas | 7/10 | 44% en zona ideal |
| Distribución | 8/10 | Sin código muerto |
| Núcleo | 9/10 | `entidades` bien diseñado |

---

## 12. COMPARATIVA CON MEDICIÓN ANTERIOR

| Métrica | 2025-11-28 | 2025-12-14 | Cambio |
|---------|------------|------------|--------|
| **I Promedio** | 0.431 | 0.35 | -0.08 (mejor) |
| **A Promedio** | 0.210 | 0.21 | = |
| **D Promedio** | 0.359 | 0.44 | +0.08 (peor) |
| **% Zona Principal** | 33.3% | 44.4% | +11% (mejor) |
| **Paquetes Zona Dolor** | 1 | 2* | +1 |
| **Calificación** | 6.8/10 | 7.2/10 | +0.4 |

*La diferencia en Zona de Dolor se debe a cambios en las dependencias detectadas entre paquetes.

**Observaciones**:
- Mejoró el porcentaje de paquetes en Zona Principal (+11%)
- El sistema es más estable (I menor)
- La abstracción se mantiene igual
- Se recomienda extraer interfaces en `gestores_entidades` y `servicios_dominio`

---

## 13. REFERENCIAS

### Principios de Robert C. Martin

#### Stable Dependencies Principle (SDP)
- Depender de paquetes más estables que uno mismo
- **Regla**: I(dependencia) ≤ I(dependiente)

#### Stable Abstractions Principle (SAP)
- Paquetes estables deben ser abstractos
- Paquetes inestables deben ser concretos
- **Regla**: A debe aumentar cuando I disminuye

#### Main Sequence
- La línea ideal donde **A + I = 1**
- Representa el balance perfecto
- **Objetivo**: Minimizar distancia D

### Interpretación de Métricas

#### Distance (D)
- **0.0-0.2**: Excelente (en la secuencia)
- **0.2-0.3**: Bueno (cerca de la secuencia)
- **0.3-0.5**: Aceptable (revisar)
- **> 0.5**: Problemático (refactorizar)

#### Instability (I)
- **0.0-0.3**: Estable (núcleo, dominio)
- **0.3-0.7**: Semi-estable (servicios)
- **0.7-1.0**: Inestable (adaptadores, UI)

#### Abstractness (A)
- **0.0-0.3**: Concreto (implementaciones)
- **0.3-0.7**: Mixto (servicios)
- **0.7-1.0**: Abstracto (interfaces, contratos)

---

**Fin del Reporte de Métricas de Paquetes**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-14*
*Nota: Estas métricas representan la arquitectura a nivel de paquetes según Robert C. Martin*
