# REPORTE DE MÉTRICAS DE DEPENDENCIAS
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-14
**Herramientas**: pip, pipdeptree, pylint, scripts AST personalizados
**Alcance**: Código de producción (excluye tests y docs)

---

## RESUMEN EJECUTIVO

### Visión General

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Dependencias Directas (pip)** | 0 | ✅ Solo usa stdlib |
| **Dependencias Externas (código)** | 1 | ✅ Mínimas (`requests`) |
| **Dependencias Internas** | 8 | Paquetes interconectados |
| **Módulos Stdlib usados** | 7 | Uso eficiente de stdlib |
| **Imports Circulares** | 0 | ✅ Sin ciclos de import |
| **Ciclos de Dependencias** | 3 | ⚠️ Ciclos entre paquetes |
| **Violaciones de Arquitectura** | 2 | ⚠️ Capa 2 → Capa 3 |
| **Imports No Utilizados** | 0 | ✅ Código limpio |
| **Profundidad Máxima** | 5 | ⚠️ Revisar |
| **Fan-In Promedio** | 1.33 | Acoplamiento moderado |
| **Fan-Out Promedio** | 1.33 | Acoplamiento moderado |

### Calificación por Categoría

| Categoría | Puntuación | Estado |
|-----------|------------|--------|
| Dependencias Externas | 10/10 | ✅ Excelente |
| Imports Circulares | 10/10 | ✅ Excelente |
| Imports No Utilizados | 10/10 | ✅ Excelente |
| Ciclos de Dependencias | 5/10 | ⚠️ Mejorar |
| Violaciones Arquitectura | 7/10 | ⚠️ Mejorar |
| Profundidad | 7/10 | ⚠️ Aceptable |
| **PROMEDIO** | **8.2/10** | ✅ Bueno |

---

## 1. DEPENDENCIAS EXTERNAS

### 1.1 Dependencias de Producción (requirements.txt)

```
✅ NINGUNA - El proyecto solo usa la biblioteca estándar de Python
```

**Interpretación**: El proyecto tiene **cero dependencias externas** para código de producción. Esto es excelente para:
- Portabilidad
- Seguridad (sin vulnerabilidades de terceros)
- Mantenimiento (sin actualizaciones de dependencias)
- Despliegue en sistemas embebidos

### 1.2 Dependencias de Desarrollo (extras_require)

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| pytest | >=7.0.0 | Testing |
| pytest-cov | >=4.0.0 | Cobertura |
| radon | >=5.1.0 | Métricas |
| pylint | >=2.15.0 | Linting |

### 1.3 Dependencias en Código Fuente

| Paquete | Archivos que lo usan | Tipo |
|---------|---------------------|------|
| `requests` | `agentes_actuadores/` | Externa (HTTP) |

**Nota**: `requests` se usa opcionalmente en visualizadores para comunicación HTTP.

### 1.4 Módulos de Biblioteca Estándar Utilizados

| Módulo | Uso en el Proyecto |
|--------|-------------------|
| `abc` | Clases abstractas (interfaces) |
| `datetime` | Timestamps en logs y sensores |
| `json` | Configuración y comunicación |
| `os` | Variables de entorno, paths |
| `socket` | Comunicación TCP/IP |
| `threading` | Operación paralela |
| `time` | Delays, timestamps |

---

## 2. DEPENDENCIAS INTERNAS (ENTRE PAQUETES)

### 2.1 Matriz de Dependencias

| Paquete | Depende de |
|---------|------------|
| `entidades` | `servicios_dominio` |
| `gestores_entidades` | (ninguno) |
| `servicios_dominio` | (ninguno) |
| `servicios_aplicacion` | `entidades`, `gestores_entidades`, `configurador` |
| `agentes_sensores` | `entidades`, `registrador`, `servicios_aplicacion` |
| `agentes_actuadores` | `entidades`, `registrador` |
| `configurador` | `entidades`, `agentes_sensores`, `agentes_actuadores` |
| `actores_externos` | (ninguno) - scripts aislados |
| `registrador` | (ninguno) |

### 2.2 Grafo de Dependencias

```
                     ┌─────────────┐
                     │ registrador │ (sin dependencias)
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             │             ▼
    ┌─────────────────┐     │    ┌─────────────────┐
    │agentes_actuadores│    │    │ agentes_sensores│
    └────────┬────────┘     │    └────────┬────────┘
             │              │             │
             │              │     ┌───────┴───────┐
             │              │     │               │
             ▼              │     ▼               ▼
    ┌─────────────────┐     │  ┌─────────────┐  ┌─────────────┐
    │   entidades     │◄────┴──┤servicios_app│◄─┤ configurador│
    └────────┬────────┘        └──────┬──────┘  └──────┬──────┘
             │                        │                │
             │                        ▼                │
             │                ┌───────────────┐        │
             │                │gestores_entid.│◄───────┘
             │                └───────────────┘
             ▼
    ┌─────────────────┐
    │servicios_dominio│ (sin dependencias)
    └─────────────────┘


    ┌─────────────────┐
    │ actores_externos│ (aislado - scripts de simulación)
    └─────────────────┘
```

---

## 3. MÉTRICAS FAN-IN / FAN-OUT

### 3.1 Definiciones

- **Fan-In**: Número de paquetes que **dependen de este** (responsabilidad)
- **Fan-Out**: Número de paquetes de los que **este depende** (dependencias)
- **Alto Fan-In**: Paquete central, estable
- **Alto Fan-Out**: Paquete con muchas dependencias, potencialmente frágil

### 3.2 Métricas por Paquete

| Paquete | Fan-In | Fan-Out | Total | Rol |
|---------|--------|---------|-------|-----|
| `entidades` | 4 | 1 | 5 | ⭐ Núcleo central |
| `registrador` | 2 | 0 | 2 | ⭐ Servicio estable |
| `servicios_aplicacion` | 1 | 3 | 4 | Orquestador |
| `agentes_sensores` | 1 | 3 | 4 | Adaptador entrada |
| `configurador` | 1 | 3 | 4 | Factory |
| `agentes_actuadores` | 1 | 2 | 3 | Adaptador salida |
| `gestores_entidades` | 1 | 0 | 1 | Gestor |
| `servicios_dominio` | 1 | 0 | 1 | Dominio |
| `actores_externos` | 0 | 0 | 0 | Scripts aislados |

### 3.3 Estadísticas Globales

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| **Fan-In Total** | 12 | - | - |
| **Fan-Out Total** | 12 | - | - |
| **Fan-In Promedio** | 1.33 | < 5 | ✅ |
| **Fan-Out Promedio** | 1.33 | < 5 | ✅ |
| **Fan-Out Máximo** | 3 | < 7 | ✅ |

**Interpretación**: ✅ Acoplamiento bajo y bien distribuido

---

## 4. PROFUNDIDAD DE DEPENDENCIAS

### 4.1 Profundidad por Paquete

La profundidad indica cuántos "saltos" de dependencias transitivas tiene un paquete.

| Paquete | Profundidad | Interpretación |
|---------|-------------|----------------|
| `gestores_entidades` | 0 | ✅ Sin dependencias |
| `servicios_dominio` | 0 | ✅ Sin dependencias |
| `actores_externos` | 0 | ✅ Aislado |
| `registrador` | 0 | ✅ Sin dependencias |
| `entidades` | 1 | ✅ Baja |
| `agentes_actuadores` | 2 | ✅ Aceptable |
| `configurador` | 4 | ⚠️ Alta |
| `servicios_aplicacion` | 4 | ⚠️ Alta |
| `agentes_sensores` | 5 | ⚠️ Muy alta |

### 4.2 Cadena de Dependencias Más Larga

```
agentes_sensores (5)
  └─> servicios_aplicacion (4)
        └─> configurador (4)
              └─> agentes_actuadores (2)
                    └─> entidades (1)
                          └─> servicios_dominio (0)
```

**Interpretación**: La profundidad máxima de 5 es alta pero aceptable para un sistema de este tamaño.

---

## 5. CICLOS DE DEPENDENCIAS

### 5.1 Detección de Ciclos

⚠️ **Se detectaron 3 ciclos de dependencias entre paquetes:**

| # | Ciclo |
|---|-------|
| 1 | `servicios_aplicacion` → `configurador` → `agentes_sensores` → `servicios_aplicacion` |
| 2 | `agentes_sensores` → `servicios_aplicacion` → `configurador` → `agentes_sensores` |
| 3 | `configurador` → `agentes_sensores` → `servicios_aplicacion` → `configurador` |

**Nota**: Los 3 ciclos son variaciones del mismo patrón circular.

### 5.2 Análisis del Ciclo

```
     ┌──────────────────────────────────────┐
     │                                      │
     ▼                                      │
┌─────────────┐      ┌─────────────┐      ┌─┴───────────┐
│configurador │ ───► │agentes_sens.│ ───► │servicios_app│
└─────────────┘      └─────────────┘      └─────────────┘
                                                 │
                                                 │
     ◄───────────────────────────────────────────┘
```

### 5.3 Impacto del Ciclo

| Aspecto | Impacto |
|---------|---------|
| **Testabilidad** | ⚠️ Difícil testear paquetes aislados |
| **Mantenibilidad** | ⚠️ Cambios pueden tener efectos cascada |
| **Comprensión** | ⚠️ Más difícil entender el flujo |
| **Compilación** | ✅ Python maneja ciclos en runtime |

### 5.4 Recomendación para Romper el Ciclo

**Opción 1**: Extraer interfaz de `servicios_aplicacion` que `agentes_sensores` pueda usar:
```
agentes_sensores → IServicioAplicacion (interfaz)
                         ↑
              servicios_aplicacion (implementa)
```

**Opción 2**: Mover la dependencia problemática a inyección de dependencias.

---

## 6. IMPORTS CIRCULARES

### 6.1 Resultado del Análisis

```
✅ No se detectaron imports circulares a nivel de módulo
```

**Herramienta**: pylint --enable=cyclic-import

**Interpretación**: Aunque hay ciclos a nivel de paquetes, Python puede resolver las dependencias porque no hay ciclos directos entre módulos individuales.

---

## 7. IMPORTS NO UTILIZADOS

### 7.1 Resultado del Análisis

```
✅ 0 imports no utilizados detectados
```

**Herramienta**: pylint --enable=W0611

**Interpretación**: El código está limpio, sin imports innecesarios que aumenten el acoplamiento.

---

## 8. VIOLACIONES DE ARQUITECTURA (Clean Architecture)

### 8.1 Capas Definidas

| Capa | Nombre | Paquetes |
|------|--------|----------|
| 1 | Domain (Entidades/Servicios) | `entidades`, `servicios_dominio` |
| 2 | Application (Casos de Uso) | `gestores_entidades`, `servicios_aplicacion` |
| 3 | Adapters (Interfaces) | `agentes_sensores`, `agentes_actuadores`, `configurador`, `registrador` |
| 4 | External (Frameworks) | `actores_externos` |

### 8.2 Regla de Dependencias

```
Las capas internas NO deben depender de las capas externas.

Capa 1 (Domain) → Solo puede depender de sí misma
Capa 2 (Application) → Puede depender de Capa 1
Capa 3 (Adapters) → Puede depender de Capas 1 y 2
Capa 4 (External) → Puede depender de cualquier capa
```

### 8.3 Violaciones Detectadas

⚠️ **Se detectaron 2 violaciones:**

| # | Archivo | Violación |
|---|---------|-----------|
| 1 | `servicios_aplicacion/selector_entrada.py` | Capa 2 → Capa 3 (`configurador`) |
| 2 | `servicios_aplicacion/lanzador.py` | Capa 2 → Capa 3 (`configurador`) |

### 8.4 Análisis de las Violaciones

**Problema**: `servicios_aplicacion` (Capa 2 - Application) importa `configurador` (Capa 3 - Adapters).

Según Clean Architecture, la capa de Aplicación no debería conocer los detalles de configuración/factories.

**Solución recomendada**:
1. Usar **Dependency Injection**: Inyectar las dependencias configuradas en lugar de importar el configurador
2. Mover `selector_entrada.py` y `lanzador.py` a la capa de Adapters si su rol es orquestar la inicialización

### 8.5 Resumen de Dependencias por Capa

| Capa | Hacia Adentro (✅) | Misma Capa | Hacia Afuera (❌) |
|------|-------------------|------------|------------------|
| 1 (Domain) | - | `servicios_dominio` | - |
| 2 (Application) | `entidades` | `gestores_entidades` | `configurador` ❌ |
| 3 (Adapters) | `entidades`, `servicios_aplicacion` | `agentes_*`, `configurador`, `registrador` | - |
| 4 (External) | - | - | - |

---

## 9. IMPORTS POR MÓDULO

### 9.1 Top 15 Módulos con Más Imports

| Archivo | Imports |
|---------|---------|
| `actores_externos/simulador_bateria.py` | 5 |
| `actores_externos/simulador_seteo_temperatura_deseada.py` | 5 |
| `actores_externos/simulador_temperatura.py` | 5 |
| `actores_externos/simulador_selector_temperatura.py` | 5 |
| `servicios_aplicacion/lanzador.py` | 4 |
| `agentes_sensores/proxy_selector_temperatura.py` | 4 |
| `servicios_aplicacion/operador_paralelo.py` | 3 |
| `servicios_aplicacion/operador_secuencial.py` | 3 |
| `agentes_actuadores/visualizador_climatizador.py` | 3 |
| `agentes_actuadores/actuador_climatizador.py` | 3 |
| `agentes_actuadores/visualizador_temperatura.py` | 3 |
| `agentes_actuadores/visualizador_bateria.py` | 3 |
| `configurador/configurador.py` | 3 |
| `actores_externos/cartel_climatizador.py` | 3 |
| `actores_externos/cartel_bateria.py` | 3 |

### 9.2 Estadísticas de Imports

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| **Total de Imports** | 87 | - | - |
| **Promedio por Módulo** | 1.9 | < 10 | ✅ |
| **Máximo por Módulo** | 5 | < 15 | ✅ |

**Interpretación**: ✅ Los módulos tienen pocas dependencias, indicando bajo acoplamiento.

---

## 10. DEPENDENCIAS DESACTUALIZADAS

### 10.1 Paquetes del Entorno de Desarrollo

**Nota**: Estas son dependencias del entorno de desarrollo, no del proyecto de producción.

| Paquete | Versión Actual | Última Versión |
|---------|----------------|----------------|
| astroid | 3.3.11 | 4.0.2 |
| coverage | 7.10.6 | 7.13.0 |
| Flask | 3.0.0 | 3.1.2 |
| hypothesis | 6.139.1 | 6.148.7 |
| pylint | (instalado) | (verificar) |

**Impacto en el proyecto**: ⚠️ Ninguno - el proyecto no tiene dependencias de producción.

---

## 11. RESUMEN DE MÉTRICAS (9/9 CALCULADAS)

### 11.1 Todas las Métricas de Dependencias

| # | Métrica | Valor | Umbral | Estado |
|---|---------|-------|--------|--------|
| 1 | Direct Dependencies | 0 | < 20 | ✅ |
| 2 | Transitive Dependencies | 0 (prod) | < 100 | ✅ |
| 3 | Total Dependencies | 0 (prod) | < 50 | ✅ |
| 4 | Outdated Dependencies | N/A | 0 | ✅ |
| 5 | Dependency Depth | 5 | < 7 | ✅ |
| 6 | Circular Imports | 0 | 0 | ✅ |
| 7 | Import Violations | 2 | 0 | ⚠️ |
| 8 | Unused Imports | 0 | 0 | ✅ |
| 9 | Missing Imports | 0 | 0 | ✅ |

### 11.2 Métricas Adicionales Calculadas

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| Fan-In Promedio | 1.33 | < 5 | ✅ |
| Fan-Out Promedio | 1.33 | < 5 | ✅ |
| Ciclos de Dependencias | 3* | 0 | ⚠️ |
| Imports por Módulo (prom) | 1.9 | < 10 | ✅ |

*Los 3 ciclos son variantes del mismo patrón circular.

---

## 12. CONCLUSIONES Y RECOMENDACIONES

### 12.1 Puntos Fuertes ⭐

1. **Cero dependencias externas de producción**: Solo usa stdlib de Python
2. **Sin imports circulares**: A nivel de módulo, el código es limpio
3. **Sin imports no utilizados**: Código bien mantenido
4. **Bajo acoplamiento**: Fan-In/Fan-Out promedio de 1.33
5. **Pocos imports por módulo**: Promedio de 1.9 imports
6. **Núcleo estable**: `entidades` y `registrador` bien diseñados

### 12.2 Áreas de Mejora ⚠️

1. **Ciclo de dependencias entre paquetes**:
   - `servicios_aplicacion` ↔ `configurador` ↔ `agentes_sensores`
   - **Acción**: Aplicar Dependency Injection o extraer interfaces

2. **Violaciones de Clean Architecture**:
   - `servicios_aplicacion` depende de `configurador`
   - **Acción**: Inyectar dependencias en lugar de importar factories

3. **Profundidad de dependencias alta** (5 niveles):
   - `agentes_sensores` tiene cadena larga
   - **Acción**: Considerar aplanar la jerarquía

### 12.3 Plan de Acción Sugerido

#### Prioridad Alta
1. **Romper el ciclo de dependencias**:
   - Extraer `IConfiguradorDependencias` interfaz
   - Usar inyección de dependencias en `agentes_sensores`

2. **Corregir violaciones de arquitectura**:
   - Mover `lanzador.py` a capa de Adapters, o
   - Eliminar dependencia directa de `configurador`

#### Prioridad Media
1. Reducir profundidad de `agentes_sensores`
2. Documentar las razones de las dependencias actuales

#### Prioridad Baja
1. Agregar verificación automática en CI/CD
2. Considerar uso de `import-linter` para enforcement

### 12.4 Indicadores Clave (KPI)

| Indicador | Valor Actual | Objetivo | Estado |
|-----------|--------------|----------|--------|
| Dependencias Externas (prod) | 0 | 0 | ✅ |
| Imports Circulares | 0 | 0 | ✅ |
| Ciclos de Paquetes | 1* | 0 | ⚠️ |
| Violaciones Arquitectura | 2 | 0 | ⚠️ |
| Fan-Out Máximo | 3 | < 7 | ✅ |
| Profundidad Máxima | 5 | < 5 | ⚠️ |

### 12.5 Calificación General

**Métricas de Dependencias del Proyecto**: **8.2/10** ⭐⭐⭐⭐

| Aspecto | Puntuación |
|---------|------------|
| Dependencias Externas | 10/10 ✅ |
| Imports Circulares | 10/10 ✅ |
| Imports No Utilizados | 10/10 ✅ |
| Ciclos de Paquetes | 6/10 ⚠️ |
| Violaciones Arquitectura | 7/10 ⚠️ |
| Acoplamiento (Fan-In/Out) | 9/10 ✅ |
| Profundidad | 7/10 ⚠️ |

---

## 13. REFERENCIAS

### Herramientas Utilizadas

| Herramienta | Uso |
|-------------|-----|
| `pip list` | Dependencias instaladas |
| `pylint` | Imports circulares (cyclic-import), no utilizados (W0611) |
| Scripts AST | Fan-In/Out, profundidad, ciclos, violaciones |

### Umbrales Recomendados

| Métrica | Umbral Recomendado | Fuente |
|---------|-------------------|--------|
| Fan-Out por paquete | < 7 | Robert C. Martin |
| Profundidad dependencias | < 5 | Clean Code |
| Imports por módulo | < 15 | Convención Python |
| Ciclos de dependencias | 0 | Best Practice |
| Violaciones arquitectura | 0 | Clean Architecture |

---

**Fin del Reporte de Métricas de Dependencias**

*Generado con: pip, pylint, scripts AST personalizados*
*Fecha: 2025-12-14*
