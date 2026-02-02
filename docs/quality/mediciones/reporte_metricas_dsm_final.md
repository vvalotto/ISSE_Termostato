# REPORTE DE MÉTRICAS DSM (Design Structure Matrix)
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-14
**Herramientas**: Scripts AST personalizados, NumPy
**Alcance**: Paquetes de código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

La Design Structure Matrix (DSM) es una herramienta para visualizar y analizar dependencias entre componentes de software. Permite identificar ciclos, clusters y violaciones de arquitectura.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Paquetes analizados** | 9 | Módulos principales |
| **Matrix Density** | 16.7% | ✅ Baja (< 20%) |
| **Dependencias Totales** | 12 | Entre paquetes |
| **Dependencias Correctas** | 10 | Hacia capas internas |
| **Dependencias Feedback** | 2 | ⚠️ Hacia capas externas |
| **Bandwidth Máximo** | 7 | ⚠️ Alto |
| **Propagation Cost Prom.** | 1.33 | ✅ Bajo |
| **Clusters** | 2 | 1 principal + 1 aislado |
| **Layering Violations** | 2 | ⚠️ Revisar |

### Calificación

| Aspecto | Puntuación | Estado |
|---------|------------|--------|
| Densidad de Matriz | 9/10 | ✅ |
| Dependencias Feedback | 7/10 | ⚠️ |
| Bandwidth | 5/10 | ⚠️ |
| Propagation Cost | 9/10 | ✅ |
| Layering | 7/10 | ⚠️ |
| **PROMEDIO** | **7.4/10** | ⭐⭐⭐ |

---

## 1. MATRIZ DSM ORIGINAL

### 1.1 Matriz de Dependencias (Orden Alfabético)

```
                          enti serv gest serv regi agen agen conf acto
                          dade _dom _ent _apl istr _sen _act figu _ext
----------------------------------------------------------------------
entidades                    ■    X    ·    ·    ·    ·    ·    ·    ·
servicios_dominio            ·    ■    ·    ·    ·    ·    ·    ·    ·
gestores_entidades           ·    ·    ■    ·    ·    ·    ·    ·    ·
servicios_aplicacion         X    ·    X    ■    ·    ·    ·    X    ·
registrador                  ·    ·    ·    ·    ■    ·    ·    ·    ·
agentes_sensores             X    ·    ·    X    X    ■    ·    ·    ·
agentes_actuadores           X    ·    ·    ·    X    ·    ■    ·    ·
configurador                 X    ·    ·    ·    ·    X    X    ■    ·
actores_externos             ·    ·    ·    ·    ·    ·    ·    ·    ■
----------------------------------------------------------------------

Leyenda: ■ = diagonal, X = dependencia, · = sin dependencia
         Fila i depende de Columna j si hay X en posición (i,j)
```

### 1.2 Lectura de la Matriz

- **Fila**: Paquete que tiene la dependencia (depende de...)
- **Columna**: Paquete del que se depende
- **X en (i,j)**: El paquete i importa del paquete j

---

## 2. MATRIZ DSM OPTIMIZADA (Por Capas)

### 2.1 Reordenamiento según Clean Architecture

Orden de capas (externa → interna):
1. **Capa 4 - External**: `actores_externos`
2. **Capa 3 - Adapters**: `configurador`, `agentes_actuadores`, `agentes_sensores`, `registrador`
3. **Capa 2 - Application**: `servicios_aplicacion`, `gestores_entidades`
4. **Capa 1 - Domain**: `servicios_dominio`, `entidades`

### 2.2 Matriz Reordenada

```
                          acto conf a_ac a_se regi s_ap gest s_do enti
                          _ext igur tuad sens istr _apl _ent _dom dade
----------------------------------------------------------------------
actores_externos             ■    ·    ·    ·    ·    ·    ·    ·    ·
configurador                 ·    ■    ✓    ✓    ·    ·    ·    ·    ✓
agentes_actuadores           ·    ·    ■    ·    ✓    ·    ·    ·    ✓
agentes_sensores             ·    ·    ·    ■    ✓    ✓    ·    ·    ✓
registrador                  ·    ·    ·    ·    ■    ·    ·    ·    ·
servicios_aplicacion         ·    ✗    ·    ·    ·    ■    ✓    ·    ✓
gestores_entidades           ·    ·    ·    ·    ·    ·    ■    ·    ·
servicios_dominio            ·    ·    ·    ·    ·    ·    ·    ■    ·
entidades                    ·    ·    ·    ·    ·    ·    ·    ✗    ■
----------------------------------------------------------------------

Leyenda:
  ■ = diagonal (el paquete mismo)
  ✓ = dependencia CORRECTA (hacia capas más internas)
  ✗ = dependencia FEEDBACK (hacia capas más externas) ⚠️
  · = sin dependencia
```

### 2.3 Análisis Visual

```
        Externa    Adapters           Application    Domain
        ┌─────┐   ┌─────────────────┐ ┌───────────┐ ┌──────────────┐
        │acto │   │conf a_ac a_sen  │ │s_ap  gest │ │s_dom   enti  │
        │_ext │   │                 │ │           │ │              │
        └─────┘   └─────────────────┘ └───────────┘ └──────────────┘
           │              │                 │              │
           │              │    ─────────────┘              │
           │              │    │                           │
           │              └────┼───────────────────────────┘
           │                   │
           │              ✗ servicios_aplicacion -> configurador (FEEDBACK)
           │              ✗ entidades -> servicios_dominio (FEEDBACK)
           │
           └─── actores_externos está AISLADO (sin dependencias)
```

---

## 3. MÉTRICAS DSM CALCULADAS

### 3.1 Matrix Density (Densidad de Matriz)

| Métrica | Valor |
|---------|-------|
| Celdas totales (sin diagonal) | 72 |
| Celdas con dependencia | 12 |
| **Densidad** | **16.7%** |
| Umbral recomendado | < 20% |
| Estado | ✅ Baja |

**Interpretación**: Una densidad baja indica bajo acoplamiento general entre paquetes.

### 3.2 Dependencias Feedforward vs Feedback

| Tipo | Cantidad | % | Interpretación |
|------|----------|---|----------------|
| **Feedforward** (correctas) | 10 | 83.3% | ✅ Hacia capas internas |
| **Feedback** (problemas) | 2 | 16.7% | ⚠️ Hacia capas externas |
| **Total** | 12 | 100% | |

**Dependencias Feedback identificadas:**
1. `servicios_aplicacion` → `configurador` (Capa 2 → Capa 3)
2. `entidades` → `servicios_dominio` (misma capa, pero invertida)

### 3.3 Bandwidth (Ancho de Banda)

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| **Bandwidth Máximo** | 7 | ≤ 3 | ⚠️ Alto |

**Dependencias con mayor distancia:**

| Desde | Hacia | Distancia |
|-------|-------|-----------|
| `configurador` | `entidades` | 7 |
| `agentes_actuadores` | `entidades` | 6 |
| `agentes_sensores` | `entidades` | 5 |
| `servicios_aplicacion` | `configurador` | 4 |
| `servicios_aplicacion` | `entidades` | 3 |

**Interpretación**: Un bandwidth alto indica que hay dependencias que "saltan" muchas capas. Esto es esperado ya que `entidades` es el núcleo y todos dependen de él.

### 3.4 Propagation Cost (Costo de Propagación)

Si un paquete cambia, ¿cuántos paquetes se ven afectados directamente?

| Paquete | Dependientes | Impacto |
|---------|--------------|---------|
| `entidades` | 4 | ⚠️ Alto |
| `registrador` | 2 | Medio |
| `servicios_dominio` | 1 | ✅ Bajo |
| `gestores_entidades` | 1 | ✅ Bajo |
| `servicios_aplicacion` | 1 | ✅ Bajo |
| `agentes_sensores` | 1 | ✅ Bajo |
| `agentes_actuadores` | 1 | ✅ Bajo |
| `configurador` | 1 | ✅ Bajo |
| `actores_externos` | 0 | ✅ Ninguno |

| Estadística | Valor |
|-------------|-------|
| **Promedio** | 1.33 |
| **Total** | 12 |
| **Máximo** | 4 (`entidades`) |

**Interpretación**: ✅ El costo de propagación es bajo. `entidades` tiene el mayor impacto, lo cual es correcto para un paquete de dominio central.

### 3.5 Cluster Count (Componentes Conectados)

| # | Cluster | Paquetes | Tamaño |
|---|---------|----------|--------|
| 1 | Principal | `entidades`, `servicios_dominio`, `gestores_entidades`, `servicios_aplicacion`, `registrador`, `agentes_sensores`, `agentes_actuadores`, `configurador` | 8 |
| 2 | Aislado | `actores_externos` | 1 |

**Interpretación**:
- El cluster principal contiene todos los paquetes del sistema core
- `actores_externos` está aislado (scripts de simulación independientes)

### 3.6 Layering Violations (Violaciones de Capas)

| # | Desde | Hacia | Capas | Problema |
|---|-------|-------|-------|----------|
| 1 | `servicios_aplicacion` | `configurador` | 2 → 3 | Application depende de Adapter |
| 2 | `entidades` | `servicios_dominio` | 1 → 1 | Dependencia invertida en Domain |

**Total de violaciones**: 2

---

## 4. VISUALIZACIÓN DE DEPENDENCIAS

### 4.1 Grafo de Dependencias por Capas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAPA 4 - EXTERNAL                                  │
│  ┌─────────────────┐                                                        │
│  │ actores_externos│  (Aislado - scripts de simulación)                     │
│  └─────────────────┘                                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAPA 3 - ADAPTERS                                  │
│                                                                             │
│  ┌────────────┐    ┌─────────────────┐    ┌─────────────────┐              │
│  │registrador │◄───┤ agentes_sensores│◄───┤  configurador   │              │
│  └────────────┘    └────────┬────────┘    └────────┬────────┘              │
│        ▲                    │                      │                        │
│        │           ┌────────┴────────┐             │                        │
│        └───────────┤agentes_actuadores│◄───────────┘                        │
│                    └─────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                         │           │
                         ▼           │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CAPA 2 - APPLICATION                                  │
│                                                                             │
│  ┌─────────────────────┐         ┌───────────────────┐                     │
│  │servicios_aplicacion │─────────┤gestores_entidades │                     │
│  └──────────┬──────────┘         └───────────────────┘                     │
│             │                                                               │
│             └────────────────────► configurador (⚠️ VIOLACIÓN)             │
└─────────────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CAPA 1 - DOMAIN                                     │
│                                                                             │
│  ┌─────────────────┐         ┌───────────────┐                             │
│  │servicios_dominio│◄────────┤   entidades   │  (⚠️ dep. invertida)        │
│  └─────────────────┘         └───────────────┘                             │
│                                     ▲                                       │
│                                     │                                       │
│                    (Todos dependen de entidades)                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Matriz de Alcanzabilidad

Muestra qué paquetes pueden alcanzar a otros transitivamente:

```
Si cambio...        Afecta directamente a...
─────────────────   ─────────────────────────
entidades           configurador, agentes_actuadores, agentes_sensores, servicios_aplicacion
registrador         agentes_actuadores, agentes_sensores
servicios_dominio   entidades
gestores_entidades  servicios_aplicacion
servicios_aplicacion agentes_sensores
agentes_sensores    configurador
agentes_actuadores  configurador
configurador        (nadie depende)
actores_externos    (aislado)
```

---

## 5. ANÁLISIS DE CICLOS EN DSM

### 5.1 Ciclos Detectados

El ciclo principal involucra 3 paquetes:

```
┌─────────────────────────────────────────┐
│                                         │
▼                                         │
configurador ───► agentes_sensores ───► servicios_aplicacion
                                         │
                                         │
◄────────────────────────────────────────┘
```

### 5.2 Impacto del Ciclo en DSM

- Aumenta las dependencias **bajo la diagonal** (feedback)
- Incrementa el **bandwidth**
- Reduce la **modularidad** del sistema

---

## 6. COMPARACIÓN CON UMBRALES

| Métrica | Valor Actual | Umbral Ideal | Estado |
|---------|--------------|--------------|--------|
| Matrix Density | 16.7% | < 20% | ✅ |
| Feedback Ratio | 16.7% | < 10% | ⚠️ |
| Bandwidth | 7 | ≤ 3 | ⚠️ |
| Propagation Cost (avg) | 1.33 | < 2.0 | ✅ |
| Clusters | 2 | 1-3 | ✅ |
| Layer Violations | 2 | 0 | ⚠️ |

---

## 7. CONCLUSIONES Y RECOMENDACIONES

### 7.1 Puntos Fuertes ⭐

1. **Densidad de matriz baja (16.7%)**: Indica bajo acoplamiento general
2. **Propagation cost bajo (1.33)**: Cambios tienen impacto limitado
3. **Núcleo estable**: `entidades` correctamente es el más referenciado
4. **Paquete aislado correcto**: `actores_externos` está separado

### 7.2 Áreas de Mejora ⚠️

1. **Dependencias feedback (2)**:
   - `servicios_aplicacion` → `configurador`
   - `entidades` → `servicios_dominio`

2. **Bandwidth alto (7)**:
   - Dependencias que saltan muchas capas
   - Considerar capas intermedias

3. **Ciclo de dependencias**:
   - `configurador` ↔ `agentes_sensores` ↔ `servicios_aplicacion`

### 7.3 Acciones Recomendadas

#### Prioridad Alta
1. **Romper ciclo**: Usar Dependency Injection en `servicios_aplicacion`
2. **Corregir violación**: Eliminar import de `configurador` desde capa Application

#### Prioridad Media
1. Revisar dependencia `entidades` → `servicios_dominio`
2. Documentar las razones de dependencias largas

#### Prioridad Baja
1. Considerar reordenar paquetes según DSM optimizada
2. Automatizar verificación de DSM en CI/CD

### 7.4 Calificación General

**Métricas DSM del Proyecto**: **7.4/10** ⭐⭐⭐

| Aspecto | Puntuación |
|---------|------------|
| Densidad | 9/10 ✅ |
| Feedback | 7/10 ⚠️ |
| Bandwidth | 5/10 ⚠️ |
| Propagation Cost | 9/10 ✅ |
| Layering | 7/10 ⚠️ |

---

## 8. MÉTRICAS DETALLADAS (7/7 CALCULADAS)

| # | Métrica | Valor | Umbral | Estado |
|---|---------|-------|--------|--------|
| 1 | Dependency Matrix | 9x9 | - | ✅ |
| 2 | Propagation Cost | 1.33 (avg) | < 2.0 | ✅ |
| 3 | Cluster Count | 2 | 1-3 | ✅ |
| 4 | Cyclic Dependencies | 10 feedback | < 5 | ⚠️ |
| 5 | Layering Violations | 2 | 0 | ⚠️ |
| 6 | Matrix Density | 16.7% | < 20% | ✅ |
| 7 | Bandwidth | 7 | ≤ 3 | ⚠️ |

---

## 9. REFERENCIAS

### Conceptos DSM

- **DSM (Design Structure Matrix)**: Matriz cuadrada que muestra dependencias entre componentes
- **Feedforward**: Dependencias hacia componentes "abajo" en la jerarquía (correctas)
- **Feedback**: Dependencias hacia componentes "arriba" en la jerarquía (problemas/ciclos)
- **Bandwidth**: Distancia máxima de una dependencia respecto a la diagonal
- **Propagation Cost**: Impacto de un cambio en el sistema

### Interpretación de la Matriz

- Matriz triangular superior: Sistema bien estratificado
- Dependencias bajo diagonal: Indican ciclos o violaciones de arquitectura
- Clusters: Grupos de componentes altamente relacionados

---

**Fin del Reporte de Métricas DSM**

*Generado con: Scripts AST personalizados, NumPy*
*Fecha: 2025-12-14*
