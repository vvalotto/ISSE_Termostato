# REPORTE DE MÉTRICAS DE COMPLEJIDAD
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-10
**Herramientas**: radon v6.x (cyclomatic complexity), cognitive_complexity v1.3.0
**Alcance**: Solo código de producción (excluye `Test/`, `docs/`, `build/`)

---

## RESUMEN EJECUTIVO

### Indicadores Clave de Complejidad

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| **Average CC** | 2.08 | ≤ 5 | ✅ Excelente |
| **Max CC** | 8 | ≤ 10 | ✅ Aceptable |
| **Total CC** | 403 | — | — |
| **Funciones Analizadas (CC)** | 194 | — | — |
| **Average Cognitive Complexity** | 0.86 | ≤ 7 | ✅ Excelente |
| **Max Cognitive Complexity** | 11 | ≤ 15 | ✅ Aceptable |
| **Funciones Analizadas (Cog)** | 141 | — | — |

### Distribución de Complejidad Ciclomática

| Rango | CC | Cantidad | Porcentaje | Estado |
|-------|----|----|------------|--------|
| **A** | 1-5 | 191 | 98.5% | ✅ Bajo riesgo |
| **B** | 6-10 | 3 | 1.5% | ✅ Bajo riesgo |
| **C** | 11-20 | 0 | 0% | — |
| **D** | 21-30 | 0 | 0% | — |
| **E** | 31-40 | 0 | 0% | — |
| **F** | >40 | 0 | 0% | — |

**Interpretación**: **98.5%** de las funciones tienen complejidad baja (A), **1.5%** tienen complejidad aceptable (B). No hay funciones con complejidad alta o muy alta.

### Distribución de Complejidad Cognitiva

| Rango | Cantidad | Porcentaje | Estado |
|-------|----------|------------|--------|
| **Simple (0-5)** | 138 | 97.9% | ✅ Excelente |
| **Moderado (6-10)** | 2 | 1.4% | ✅ Aceptable |
| **Complejo (11-15)** | 1 | 0.7% | ✅ Aceptable |
| **Muy complejo (>15)** | 0 | 0% | ✅ Ninguno |

---

## 1. MÉTRICAS DE COMPLEJIDAD CICLOMÁTICA

### 1.1 Estadísticas Globales

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Total CC** | 403 | Suma de complejidad de todas las funciones |
| **Average CC** | 2.08 | CC promedio del proyecto |
| **Max CC** | 8 | Complejidad máxima encontrada |
| **Blocks Analyzed** | 194 | Funciones, métodos y clases analizadas |

### 1.2 Funciones con Mayor Complejidad Ciclomática

| # | Función | Archivo | CC | Rango | Línea |
|---|---------|---------|----|----|-------|
| 1 | `obtener_seteo` | `agentes_sensores/proxy_seteo_temperatura.py` | **8** | B | 65 |
| 2 | `obtener_selector` | `agentes_sensores/proxy_selector_temperatura.py` | **8** | B | 104 |
| 3 | `_validar_configuracion` | `configurador/configurador.py` | **7** | B | 215 |

**Observaciones**:
- Solo **3 funciones** tienen CC > 5 (rango B)
- Todas están por debajo del umbral crítico (CC ≤ 10)
- Las funciones más complejas están en:
  - Proxies de entrada (manejo de sockets)
  - Configuración (validación)

### 1.3 Análisis Detallado de Funciones Complejas

#### 1. `obtener_seteo` - CC: 8 (proxy_seteo_temperatura.py:65)

```
Razón: Manejo de múltiples condiciones para comunicación socket
Estructura: if/elif/else con excepciones
Recomendación: ✅ Aceptable - Manejo de I/O requiere validaciones
```

#### 2. `obtener_selector` - CC: 8 (proxy_selector_temperatura.py:104)

```
Razón: Similar a obtener_seteo, comunicación socket con validaciones
Estructura: if/elif/else con excepciones
Recomendación: ✅ Aceptable - Patrón consistente en proxies
```

#### 3. `_validar_configuracion` - CC: 7 (configurador.py:215)

```
Razón: Validación de múltiples parámetros de configuración
Estructura: Múltiples if para validar campos
Recomendación: ⚠️ Considerar extraer validaciones a funciones específicas
```

---

## 2. MÉTRICAS DE COMPLEJIDAD COGNITIVA

### 2.1 Descripción

La **Complejidad Cognitiva** mide qué tan difícil es para un humano entender el código. A diferencia de la complejidad ciclomática que cuenta caminos de ejecución, la complejidad cognitiva penaliza estructuras que dificultan la comprensión: anidamiento profundo, saltos de flujo, recursión, etc.

### 2.2 Estadísticas Globales

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Total Cognitive Complexity** | 121 | Suma de complejidad cognitiva de todas las funciones |
| **Average Cognitive Complexity** | 0.86 | Complejidad cognitiva promedio |
| **Max Cognitive Complexity** | 11 | Complejidad cognitiva máxima encontrada |
| **Functions Analyzed** | 141 | Funciones y métodos analizados |

### 2.3 Funciones con Mayor Complejidad Cognitiva (Top 15)

| # | Función | Archivo | Cognitive CC | Línea | Estado |
|---|---------|---------|--------------|-------|--------|
| 1 | `_validar_configuracion` | `configurador/configurador.py` | **11** | 215 | ✅ |
| 2 | `obtener_seteo` | `agentes_sensores/proxy_seteo_temperatura.py` | **10** | 65 | ✅ |
| 3 | `obtener_selector` | `agentes_sensores/proxy_selector_temperatura.py` | **10** | 104 | ✅ |
| 4 | `cargar_configuracion` | `configurador/configurador.py` | 5 | 45 | ✅ |
| 5 | `leer_carga` | `agentes_sensores/proxy_bateria.py` | 4 | 63 | ✅ |
| 6 | `leer_temperatura` | `agentes_sensores/proxy_sensor_temperatura.py` | 4 | 63 | ✅ |
| 7 | `_obtener_seteo_temperatura_deseada` | `servicios_aplicacion/selector_entrada.py` | 3 | 55 | ✅ |
| 8 | `crear` | `configurador/factory_visualizador_temperatura.py` | 3 | 20 | ✅ |
| 9 | `crear` | `configurador/factory_visualizador_climatizador.py` | 3 | 20 | ✅ |
| 10 | `crear` | `configurador/factory_visualizador_bateria.py` | 3 | 20 | ✅ |
| 11 | `iniciar` | `servicios_aplicacion/inicializador.py` | 2 | 20 | ✅ |
| 12 | `mostrar_temperatura` | `gestores_entidades/gestor_ambiente.py` | 2 | 121 | ✅ |
| 13 | `comparar_temperatura` | `servicios_dominio/controlador_climatizador.py` | 2 | 34 | ✅ |
| 14 | `crear` | `configurador/factory_climatizador.py` | 2 | 18 | ✅ |
| 15 | `crear` | `configurador/factory_sensor_temperatura.py` | 2 | 19 | ✅ |

**Observaciones**:
- Las mismas 3 funciones identificadas con alta CC ciclomática también tienen alta complejidad cognitiva
- Todas las funciones están **por debajo del umbral crítico** de 15
- La complejidad cognitiva promedio es **muy baja** (0.86), indicando código muy legible

### 2.4 Comparación CC vs Cognitive Complexity

| Función | CC Ciclomática | Cognitive CC | Diferencia |
|---------|---------------|--------------|------------|
| `_validar_configuracion` | 7 | 11 | +4 |
| `obtener_seteo` | 8 | 10 | +2 |
| `obtener_selector` | 8 | 10 | +2 |

**Interpretación**: La complejidad cognitiva es ligeramente mayor que la ciclomática en las funciones más complejas, lo que indica que hay algo de anidamiento que aumenta la dificultad de comprensión.

---

## 3. COMPARACIÓN CON MEDICIÓN ANTERIOR

### 3.1 Evolución de Métricas

| Métrica | 2025-11-28 | 2025-12-10 | Cambio | Estado |
|---------|------------|------------|--------|--------|
| **CC Promedio** | 2.11 | 2.08 | -0.03 | ✅ Mejora |
| **CC Máximo** | 8 | 8 | = | ✅ Estable |
| **CC Total** | 400 | 403 | +3 | ✅ Estable |
| **Bloques Analizados** | 190 | 194 | +4 | — |
| **Funciones Rank A** | 186 (97.9%) | 191 (98.5%) | +0.6% | ✅ Mejora |
| **Funciones Rank B** | 4 (2.1%) | 3 (1.5%) | -0.6% | ✅ Mejora |
| **Cog. CC Promedio** | 0.96 | 0.86 | -0.10 | ✅ Mejora |
| **Cog. CC Máximo** | 11 | 11 | = | ✅ Estable |

### 3.2 Resumen de Cambios

- ✅ **Mejora en CC promedio**: 2.11 → 2.08 (-1.4%)
- ✅ **Mejora en distribución**: 98.5% funciones en Rank A (vs 97.9%)
- ✅ **Reducción de funciones complejas**: 4 → 3 funciones en Rank B
- ✅ **Mejora en complejidad cognitiva promedio**: 0.96 → 0.86 (-10.4%)
- ✅ **Refactorización exitosa**: La función `_definir_accion` de `climatizador.py` ya no aparece en Rank B

---

## 4. EVALUACIÓN POR ESTÁNDARES DE INDUSTRIA

| Estándar | Criterio | Proyecto | Estado |
|----------|----------|----------|--------|
| **McCabe** | CC promedio ≤ 5 | 2.08 | ✅ Excelente |
| **McCabe** | CC máximo ≤ 10 | 8 | ✅ Cumple |
| **SonarQube** | >80% funciones con CC ≤ 5 | 98.5% | ✅ Excelente |
| **MISRA** | CC ≤ 10 por función | 100% | ✅ Cumple |
| **Cognitive** | CC cognitivo ≤ 15 | Máx: 11 | ✅ Cumple |

---

## 5. CONCLUSIONES Y RECOMENDACIONES

### 5.1 Puntos Fuertes

1. **Complejidad ciclomática excelente**:
   - CC promedio: 2.08 (muy por debajo de 5)
   - 98.5% de funciones en rango A (simple)
   - 100% de funciones bajo el umbral crítico (≤ 10)

2. **Complejidad cognitiva muy baja**:
   - Promedio: 0.86 (excelente)
   - 97.9% de funciones son simples de entender
   - Solo 1 función con complejidad cognitiva > 10

3. **Mejora respecto a medición anterior**:
   - Reducción de funciones complejas
   - Mejora en promedios de CC y cognitiva

### 5.2 Áreas de Mejora

1. **Validación de configuración compleja**:
   - `_validar_configuracion` tiene CC = 7 y Cog = 11
   - **Acción sugerida**: Extraer validadores específicos por campo

2. **Proxies de entrada con lógica de I/O**:
   - CC = 8 en funciones de socket
   - **Acción sugerida**: Considerar patrón Strategy o Template Method

### 5.3 Calificación General

**Métricas de Complejidad del Proyecto**: **9.5/10**

| Aspecto | Calificación |
|---------|--------------|
| Complejidad ciclomática | 10/10 |
| Complejidad cognitiva | 10/10 |
| Distribución de complejidad | 10/10 |
| Cumplimiento de estándares | 10/10 |
| Evolución temporal | 9/10 |

**Veredicto**: El código de producción tiene **complejidad excepcionalmente baja** y está muy bien estructurado. La refactorización realizada entre el 28 de noviembre y el 10 de diciembre ha mejorado las métricas.

---

**Fin del Reporte de Métricas de Complejidad**

*Generado con: radon v6.x, cognitive_complexity v1.3.0*
*Fecha: 2025-12-10*
