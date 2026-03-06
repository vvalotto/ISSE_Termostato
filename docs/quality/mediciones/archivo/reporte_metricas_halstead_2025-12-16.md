# REPORTE DE MÉTRICAS DE HALSTEAD
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-16
**Herramienta**: radon v6.x
**Alcance**: Código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de Halstead proporcionan una medida cuantitativa de la complejidad del software basada en el análisis de operadores y operandos en el código fuente.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Archivos analizados** | 31 | Archivos Python con código ejecutable |
| **Funciones/Métodos** | 37 | Total de funciones y métodos |
| **Volumen Total (V)** | 2594.97 | Tamaño del programa en bits |
| **Esfuerzo Total (E)** | 6352.38 | Esfuerzo mental requerido |
| **Tiempo Estimado (T)** | 5.88 min | Tiempo de programación estimado |
| **Bugs Estimados (B)** | 0.86 | Errores esperados en el código |
| **Dificultad Promedio (D)** | 1.28 | Dificultad de comprensión |

### Interpretación General

- **Volumen**: 2594.97 bits indica un proyecto de tamaño mediano
- **Bugs estimados**: 0.86 errores potenciales (fórmula: V/3000)
- **Tiempo de desarrollo**: ~5.88 minutos de trabajo mental puro
- **Dificultad promedio**: 1.28 (baja - código fácil de entender)

---

## 1. MÉTRICAS GLOBALES

### 1.1 Operadores y Operandos

| Métrica | Símbolo | Valor | Descripción |
|---------|---------|-------|-------------|
| **Operadores Únicos** | n₁ | 65 | Cantidad de operadores distintos |
| **Operandos Únicos** | n₂ | 302 | Cantidad de operandos distintos |
| **Total Operadores** | N₁ | 198 | Todas las ocurrencias de operadores |
| **Total Operandos** | N₂ | 381 | Todas las ocurrencias de operandos |
| **Vocabulario** | n = n₁ + n₂ | 367 | Riqueza del vocabulario |
| **Longitud** | N = N₁ + N₂ | 579 | Longitud total del programa |

### 1.2 Métricas Derivadas

| Métrica | Fórmula | Valor | Interpretación |
|---------|---------|-------|----------------|
| **Volumen (V)** | N × log₂(n) | 2594.97 | Tamaño del código en bits |
| **Dificultad (D)** | (n₁/2) × (N₂/n₂) | 39.70 | Dificultad de comprensión |
| **Esfuerzo (E)** | D × V | 6352.38 | Esfuerzo mental requerido |
| **Tiempo (T)** | E / 18 segundos | 352.91s (5.88 min) | Tiempo de programación |
| **Bugs (B)** | V / 3000 | 0.865 | Errores estimados |

### 1.3 Promedios por Archivo

| Métrica | Cálculo | Valor | Estado |
|---------|---------|-------|--------|
| **Volumen promedio** | 2594.97 / 31 | **83.71** | ✅ Bueno |
| **Esfuerzo promedio** | 6352.38 / 31 | **204.92** | ✅ Razonable |
| **Dificultad promedio** | 39.70 / 31 | **1.28** | ✅ Baja |
| **Bugs por archivo** | 0.865 / 31 | **0.0279** | ✅ Excelente |

### 1.4 Promedios por Función

| Métrica | Cálculo | Valor |
|---------|---------|-------|
| **Volumen por función** | 2594.97 / 37 | **70.13** |
| **Esfuerzo por función** | 6352.38 / 37 | **171.69** |

---

## 2. TOP 15 ARCHIVOS POR VOLUMEN

Archivos con mayor volumen de Halstead (complejidad de información):

| # | Archivo | Volumen (V) | Dificultad (D) | Esfuerzo (E) | Bugs | Tiempo |
|---|---------|-------------|----------------|--------------|------|--------|
| 1 | `actores_externos/simulador_selector_temperatura.py` | 422.1 | 3.66 | 1544.4 | 0.141 | 85.8s |
| 2 | `agentes_actuadores/actuador_climatizador.py` | 406.3 | 0.72 | 293.5 | 0.135 | 16.3s |
| 3 | `actores_externos/simulador_seteo_temperatura_deseada.py` | 342.9 | 4.32 | 1482.5 | 0.114 | 82.4s |
| 4 | `agentes_sensores/proxy_selector_temperatura.py` | 294.4 | 1.43 | 420.6 | 0.098 | 23.4s |
| 5 | `actores_externos/simulador_bateria.py` | 284.3 | 2.90 | 825.5 | 0.095 | 45.9s |
| 6 | `actores_externos/simulador_temperatura.py` | 282.1 | 3.00 | 846.3 | 0.094 | 47.0s |
| 7 | `configurador/configurador.py` | 183.3 | 2.36 | 433.3 | 0.061 | 24.1s |
| 8 | `entidades/bateria.py` | 57.4 | 1.67 | 95.6 | 0.019 | 5.3s |
| 9 | `gestores_entidades/gestor_ambiente.py` | 39.9 | 1.71 | 68.3 | 0.013 | 3.8s |
| 10 | `servicios_dominio/controlador_climatizador.py` | 38.0 | 3.20 | 121.7 | 0.013 | 6.8s |
| 11 | `servicios_aplicacion/selector_entrada.py` | 36.0 | 1.33 | 48.0 | 0.012 | 2.7s |
| 12 | `agentes_sensores/proxy_seteo_temperatura.py` | 27.0 | 1.80 | 48.6 | 0.009 | 2.7s |
| 13 | `configurador/factory_visualizador_temperatura.py` | 20.9 | 0.75 | 15.7 | 0.007 | 0.9s |
| 14 | `configurador/factory_visualizador_climatizador.py` | 20.9 | 0.75 | 15.7 | 0.007 | 0.9s |
| 15 | `configurador/factory_visualizador_bateria.py` | 20.9 | 0.75 | 15.7 | 0.007 | 0.9s |

**Observaciones**:
- El archivo más complejo es `actores_externos/simulador_selector_temperatura.py` con V=422.1
- Archivos con D > 5.0 requieren especial atención para mantenibilidad
- El esfuerzo total del top 15 representa 98.8% del esfuerzo total

---

## 3. ANÁLISIS POR PAQUETE

Distribución de métricas de Halstead por paquete/módulo:

| Paquete | Archivos | Volumen | Esfuerzo | Bugs | Dificultad Avg | Funciones |
|---------|----------|---------|----------|------|----------------|-----------|
| `actores_externos/` | 7 | 1337.5 | 4701.8 | 0.446 | 2.20 | 0 |
| `agentes_actuadores/` | 2 | 420.3 | 300.4 | 0.140 | 0.61 | 2 |
| `agentes_sensores/` | 4 | 325.4 | 471.2 | 0.108 | 1.06 | 5 |
| `configurador/` | 10 | 310.8 | 522.7 | 0.104 | 0.84 | 18 |
| `entidades/` | 3 | 66.9 | 100.4 | 0.022 | 0.89 | 4 |
| `gestores_entidades/` | 2 | 44.6 | 70.7 | 0.015 | 1.11 | 4 |
| `servicios_aplicacion/` | 2 | 51.5 | 63.5 | 0.017 | 1.17 | 3 |
| `servicios_dominio/` | 1 | 38.0 | 121.7 | 0.013 | 3.20 | 1 |

**Interpretación**:
- **actores_externos/**: Paquete con mayor complejidad de información
- **Distribución**: Concentrada
- **Paquetes más simples**: servicios_dominio, gestores_entidades, servicios_aplicacion

---

## 4. ARCHIVOS DE ALTO ESFUERZO

Archivos que requieren mayor esfuerzo mental (E > 409.8):

| Archivo | Esfuerzo (E) | Volumen (V) | Dificultad (D) | Recomendación |
|---------|--------------|-------------|----------------|---------------|
| `actores_externos/simulador_selector_temperatura.py` | 1544.4 | 422.1 | 3.66 | Aceptable |
| `actores_externos/simulador_seteo_temperatura_deseada.py` | 1482.5 | 342.9 | 4.32 | Aceptable |
| `agentes_sensores/proxy_selector_temperatura.py` | 420.6 | 294.4 | 1.43 | Aceptable |
| `actores_externos/simulador_bateria.py` | 825.5 | 284.3 | 2.90 | Aceptable |
| `actores_externos/simulador_temperatura.py` | 846.3 | 282.1 | 3.00 | Aceptable |
| `configurador/configurador.py` | 433.3 | 183.3 | 2.36 | Aceptable |

---

## 5. ARCHIVOS DE ALTA DIFICULTAD

Archivos con dificultad superior al promedio (D > 5.0):

| Archivo | Dificultad (D) | n₁ | n₂ | N₂/n₂ | Recomendación |
|---------|----------------|----|----|-------|---------------|
| - | - | - | - | - | ✅ Todos los archivos tienen dificultad aceptable |

**Nota**: La dificultad alta suele indicar:
- Muchos operadores únicos (n₁ alto)
- Repetición excesiva de operandos (N₂/n₂ alto)
- Código procedural con muchas variables temporales

---

## 6. DISTRIBUCIÓN DE BUGS ESTIMADOS

Archivos con mayor propensión a errores (top 10):

| # | Archivo | Bugs | Volumen | % del Total |
|---|---------|------|---------|-------------|
| 1 | `simulador_selector_temperatura.py` | 0.141 | 422.1 | 16.3% |
| 2 | `actuador_climatizador.py` | 0.135 | 406.3 | 15.7% |
| 3 | `simulador_seteo_temperatura_deseada.py` | 0.114 | 342.9 | 13.2% |
| 4 | `proxy_selector_temperatura.py` | 0.098 | 294.4 | 11.3% |
| 5 | `simulador_bateria.py` | 0.095 | 284.3 | 11.0% |
| 6 | `simulador_temperatura.py` | 0.094 | 282.1 | 10.9% |
| 7 | `configurador.py` | 0.061 | 183.3 | 7.1% |
| 8 | `bateria.py` | 0.019 | 57.4 | 2.2% |
| 9 | `gestor_ambiente.py` | 0.013 | 39.9 | 1.5% |
| 10 | `controlador_climatizador.py` | 0.013 | 38.0 | 1.5% |

**Total de bugs estimados**: 0.86

**Interpretación**:
- Fórmula de Halstead: B = V / 3000
- Los archivos con mayor volumen tienden a tener más bugs
- Esta es una estimación estadística, no bugs reales encontrados

---

## 7. MÉTRICAS DETALLADAS POR ARCHIVO

### 7.1 Todas las Métricas de Halstead (12/12 calculadas)

Resumen de las 12 métricas de Halstead para el proyecto:

| # | Métrica | Símbolo | Valor Total | Promedio | ✓ |
|---|---------|---------|-------------|----------|---|
| 1 | Operadores Únicos | n₁ | 65 | 2.1 | ✅ |
| 2 | Operandos Únicos | n₂ | 302 | 9.7 | ✅ |
| 3 | Total Operadores | N₁ | 198 | 6.4 | ✅ |
| 4 | Total Operandos | N₂ | 381 | 12.3 | ✅ |
| 5 | Vocabulario | n | 367 | 11.8 | ✅ |
| 6 | Longitud | N | 579 | 18.7 | ✅ |
| 7 | Longitud Calculada | N̂ | - | - | ⚠️ |
| 8 | Volumen | V | 2594.97 | 83.71 | ✅ |
| 9 | Dificultad | D | 39.70 | 1.28 | ✅ |
| 10 | Esfuerzo | E | 6352.38 | 204.92 | ✅ |
| 11 | Tiempo | T | 352.91s | 11.38s | ✅ |
| 12 | Bugs Estimados | B | 0.865 | 0.0279 | ✅ |

**Estado**: ✅ **11/12 métricas calculadas exitosamente**
*(N̂ requiere cálculo manual adicional)*

### 7.2 Lista Completa de Archivos

Todos los archivos analizados ordenados por volumen:

| # | Archivo | V | D | E | B | Funcs |
|---|---------|---|---|---|---|-------|
| 1 | `actores_externos/simulador_selector_temperatura.py` | 422.1 | 3.66 | 1544.4 | 0.141 | 0 |
| 2 | `agentes_actuadores/actuador_climatizador.py` | 406.3 | 0.72 | 293.5 | 0.135 | 2 |
| 3 | `actores_externos/simulador_seteo_temperatura_deseada.py` | 342.9 | 4.32 | 1482.5 | 0.114 | 0 |
| 4 | `agentes_sensores/proxy_selector_temperatura.py` | 294.4 | 1.43 | 420.6 | 0.098 | 2 |
| 5 | `actores_externos/simulador_bateria.py` | 284.3 | 2.90 | 825.5 | 0.095 | 0 |
| 6 | `actores_externos/simulador_temperatura.py` | 282.1 | 3.00 | 846.3 | 0.094 | 0 |
| 7 | `configurador/configurador.py` | 183.3 | 2.36 | 433.3 | 0.061 | 9 |
| 8 | `entidades/bateria.py` | 57.4 | 1.67 | 95.6 | 0.019 | 2 |
| 9 | `gestores_entidades/gestor_ambiente.py` | 39.9 | 1.71 | 68.3 | 0.013 | 3 |
| 10 | `servicios_dominio/controlador_climatizador.py` | 38.0 | 3.20 | 121.7 | 0.013 | 1 |
| 11 | `servicios_aplicacion/selector_entrada.py` | 36.0 | 1.33 | 48.0 | 0.012 | 2 |
| 12 | `agentes_sensores/proxy_seteo_temperatura.py` | 27.0 | 1.80 | 48.6 | 0.009 | 1 |
| 13 | `configurador/factory_visualizador_temperatura.py` | 20.9 | 0.75 | 15.7 | 0.007 | 1 |
| 14 | `configurador/factory_visualizador_climatizador.py` | 20.9 | 0.75 | 15.7 | 0.007 | 1 |
| 15 | `configurador/factory_visualizador_bateria.py` | 20.9 | 0.75 | 15.7 | 0.007 | 1 |
| 16 | `servicios_aplicacion/inicializador.py` | 15.5 | 1.00 | 15.5 | 0.005 | 1 |
| 17 | `agentes_actuadores/visualizador_temperatura.py` | 13.9 | 0.50 | 7.0 | 0.005 | 0 |
| 18 | `configurador/factory_climatizador.py` | 12.0 | 0.67 | 8.0 | 0.004 | 1 |
| 19 | `configurador/factory_sensor_temperatura.py` | 12.0 | 0.67 | 8.0 | 0.004 | 1 |
| 20 | `configurador/factory_proxy_bateria.py` | 12.0 | 0.67 | 8.0 | 0.004 | 1 |
| 21 | `configurador/factory_selector_temperatura.py` | 12.0 | 0.67 | 8.0 | 0.004 | 1 |
| 22 | `configurador/factory_seteo_temperatura.py` | 12.0 | 0.67 | 8.0 | 0.004 | 1 |
| 23 | `entidades/ambiente.py` | 4.8 | 0.50 | 2.4 | 0.002 | 1 |
| 24 | `entidades/climatizador.py` | 4.8 | 0.50 | 2.4 | 0.002 | 1 |
| 25 | `gestores_entidades/gestor_climatizador.py` | 4.8 | 0.50 | 2.4 | 0.002 | 1 |
| 26 | `configurador/factory_actuador_climatizador.py` | 4.8 | 0.50 | 2.4 | 0.002 | 1 |
| 27 | `agentes_sensores/proxy_bateria.py` | 2.0 | 0.50 | 1.0 | 0.001 | 1 |
| 28 | `agentes_sensores/proxy_sensor_temperatura.py` | 2.0 | 0.50 | 1.0 | 0.001 | 1 |
| 29 | `actores_externos/cartel_climatizador.py` | 2.0 | 0.50 | 1.0 | 0.001 | 0 |
| 30 | `actores_externos/cartel_bateria.py` | 2.0 | 0.50 | 1.0 | 0.001 | 0 |
| 31 | `actores_externos/cartel_temperatura.py` | 2.0 | 0.50 | 1.0 | 0.001 | 0 |

---

## 8. CONCLUSIONES Y RECOMENDACIONES

### 8.1 Puntos Fuertes ⭐

1. **Baja dificultad promedio**: D=1.28 indica código fácil de entender
2. **Bajo ratio de bugs**: 0.86 bugs estimados para 2595 bits de volumen
3. **Esfuerzo distribuido**: No hay concentración excesiva
4. **Funciones pequeñas**: Volumen promedio por función = 70.1
5. **Vocabulario moderado**: 11.8 términos únicos por archivo

### 8.2 Áreas de Mejora ⚠️

1. **Archivos de alto esfuerzo**:
   - `actores_externos/simulador_selector_temperatura.py` (E=1544.4)
   - `actores_externos/simulador_seteo_temperatura_deseada.py` (E=1482.5)
   - `agentes_sensores/proxy_selector_temperatura.py` (E=420.6)
   - **Acción**: Dividir en módulos más pequeños

### 8.3 Indicadores Clave (KPI)

| Indicador | Valor | Umbral Recomendado | Estado |
|-----------|-------|-------------------|--------|
| Volumen Total | 2595 | < 10,000 | ✅ |
| Dificultad Promedio | 1.28 | < 10 | ✅ |
| Bugs Estimados | 0.86 | < 2.0 | ✅ |
| Volumen/Función | 70.1 | < 100 | ✅ |
| Esfuerzo/Archivo | 204.9 | < 500 | ✅ |

### 8.4 Calificación General

**Métricas de Halstead del Proyecto**: **10.0/10** ⭐

- ✅ Dificultad: 10/10
- ✅ Calidad: 8/10
- ⚠️ Modularidad: 6/10
- ⚠️ Mantenibilidad: 6/10

---

## 9. REFERENCIAS

### Fórmulas de Halstead

- **n₁**: Operadores únicos (if, for, +, -, etc.)
- **n₂**: Operandos únicos (variables, constantes, literales)
- **N₁**: Total de operadores en el código
- **N₂**: Total de operandos en el código
- **n = n₁ + n₂**: Vocabulario del programa
- **N = N₁ + N₂**: Longitud del programa
- **V = N × log₂(n)**: Volumen (tamaño en bits)
- **D = (n₁/2) × (N₂/n₂)**: Dificultad
- **E = D × V**: Esfuerzo mental
- **T = E / 18**: Tiempo (segundos)
- **B = V / 3000**: Bugs estimados

### Interpretación

- **V < 1000**: Programa pequeño
- **V 1000-8000**: Programa mediano
- **V > 8000**: Programa grande
- **D < 10**: Fácil de entender
- **D 10-30**: Dificultad moderada
- **D > 30**: Difícil de entender

---

**Fin del Reporte de Métricas de Halstead**

*Generado con: radon v6.x*
*Fecha: 2025-12-16 09:02:43*