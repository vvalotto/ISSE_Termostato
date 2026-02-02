# REPORTE DE MÉTRICAS DE CLEAN ARCHITECTURE
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-16
**Herramientas**: Script personalizado basado en AST de Python
**Alcance**: Código de producción (excluye tests y actores externos)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de Clean Architecture evalúan qué tan bien el proyecto sigue los principios arquitectónicos de Robert C. Martin. Se enfoca en la dirección de dependencias, abstracción, estabilidad y la Regla de Dependencia.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Paquetes analizados** | 9 | Total de paquetes del proyecto |
| **Abstractness promedio** | 0.210 | ⚠️ Revisar nivel de abstracción |
| **Instability promedio** | 0.346 | ✅ Estable |
| **Distance promedio** | 0.444 | ⚠️ Lejos de secuencia principal |
| **Score promedio** | 5.6/10 | Calidad arquitectónica |
| **Paquetes en Main Sequence** | 3 | 33.3% en posición ideal |
| **Paquetes en Zone of Pain** | 3 | ❌ Rígidos y difíciles de cambiar |
| **Paquetes en Zone of Uselessness** | 0 | ✅ Abstractos pero inútiles |
| **Violaciones de capas** | 24 | ❌ Dependencias incorrectas |
| **Ciclos entre paquetes** | 1 | ❌ Viola ADP |

### Distribución por Zona Arquitectónica

| Zona | Paquetes | Porcentaje | Interpretación |
|------|----------|------------|----------------|
| Zone of Pain (Rigid) | 3 | 33.3% | ⚠️ |
| Suboptimal (Needs adjustment) | 3 | 33.3% | ⚠️ |
| Main Sequence (Ideal) | 3 | 33.3% | ✅ |

---

## 1. MÉTRICAS DE CLEAN ARCHITECTURE EXPLICADAS

### 1.1 Abstractness (A)

**Proporción de abstracción en un paquete**

```
A = Na / Nc
```

Donde:
- **Na** = Número de clases/interfaces abstractas
- **Nc** = Número total de clases

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0 = Completamente concreto
  - 1.0 = Completamente abstracto
  - 0.3-0.7 = Balance ideal

### 1.2 Instability (I)

**Resistencia al cambio de un paquete**

```
I = Ce / (Ca + Ce)
```

Donde:
- **Ce** = Efferent Coupling (dependencias salientes)
- **Ca** = Afferent Coupling (dependencias entrantes)

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0 = Máxima estabilidad (muchos dependen de él)
  - 1.0 = Máxima inestabilidad (depende de muchos)

### 1.3 Distance from Main Sequence (D)

**Distancia a la secuencia principal ideal**

```
D = |A + I - 1|
```

- **Rango**: [0, 1]
- **Interpretación**:
  - 0.0 = En la secuencia principal (ideal)
  - < 0.2 = Muy cerca (excelente)
  - 0.2-0.5 = Distancia aceptable
  - > 0.5 = Muy lejos (problemático)

### 1.4 Main Sequence (Secuencia Principal)

La línea ideal donde **A + I = 1**

**Principio**: Paquetes estables (I bajo) deben ser abstractos (A alto).
Paquetes inestables (I alto) deben ser concretos (A bajo).

### 1.5 Zonas Arquitectónicas

#### Zone of Pain (Zona de Dolor)
- **Características**: A ≈ 0, I ≈ 0
- **Problema**: Concreto y estable = rígido, difícil de cambiar
- **Solución**: Introducir abstracciones

#### Zone of Uselessness (Zona de Inutilidad)
- **Características**: A ≈ 1, I ≈ 1
- **Problema**: Abstracto e inestable = sin uso real
- **Solución**: Eliminar o hacer más estable

---

## 2. MÉTRICAS POR PAQUETE

| # | Paquete | A | I | D | Ca | Ce | Score | Zona | Estado |
|---|---------|---|---|---|----|----|-|------|--------|
| 1 | `registrador` | 1.000 | 0.000 | 0.000 | 2 | 0 | 10.0 | Main Sequence (Ideal) | ✅ |
| 2 | `servicios_aplicacion` | 0.250 | 0.750 | 0.000 | 1 | 3 | 10.0 | Main Sequence (Ideal) | ✅ |
| 3 | `entidades` | 0.636 | 0.200 | 0.164 | 4 | 1 | 8.4 | Main Sequence (Ideal) | ✅ |
| 4 | `agentes_sensores` | 0.000 | 0.750 | 0.250 | 1 | 3 | 7.5 | Suboptimal (Needs adjustment) | ✅ |
| 5 | `configurador` | 0.000 | 0.750 | 0.250 | 1 | 3 | 7.5 | Suboptimal (Needs adjustment) | ✅ |
| 6 | `agentes_actuadores` | 0.000 | 0.667 | 0.333 | 1 | 2 | 6.7 | Suboptimal (Needs adjustment) | ⚠️ |
| 7 | `actores_externos` | 0.000 | 0.000 | 1.000 | 0 | 0 | 0.0 | Zone of Pain (Rigid) | ❌ |
| 8 | `gestores_entidades` | 0.000 | 0.000 | 1.000 | 1 | 0 | 0.0 | Zone of Pain (Rigid) | ❌ |
| 9 | `servicios_dominio` | 0.000 | 0.000 | 1.000 | 1 | 0 | 0.0 | Zone of Pain (Rigid) | ❌ |

**Leyenda**:
- **A** = Abstractness (abstracción)
- **I** = Instability (inestabilidad)
- **D** = Distance (distancia a secuencia principal)
- **Ca** = Afferent Coupling (dependencias entrantes)
- **Ce** = Efferent Coupling (dependencias salientes)

---

## 3. ANÁLISIS POR CAPA ARQUITECTÓNICA

Distribución de módulos por capa de Clean Architecture:

| Capa | Módulos | Paquetes | Descripción |
|------|---------|----------|-------------|
| Layer 1: Entities | 10 | entidades | Entidades de negocio (núcleo) |
| Layer 2: Use Cases | 6 | servicios_dominio, gestores_entidades | Casos de uso y lógica de negocio |
| Layer 3: Interface Adapters | 21 | agentes_sensores, servicios_aplicacion, agentes_actuadores, registrador | Adaptadores de interfaz |
| Layer 4: Frameworks & Drivers | 19 | configurador, actores_externos | Frameworks y drivers externos |

---

## 4. VIOLACIONES DE LA REGLA DE DEPENDENCIA

Se detectaron **24 violaciones** de la Regla de Dependencia.

**Regla**: Las dependencias deben apuntar hacia adentro (capas internas).

### 4.2 Violaciones Moderadas (24)

Dependencias de una capa interna a una externa:

| # | Origen | Capa Origen | Destino | Capa Destino |
|---|--------|-------------|---------|--------------|\ n| 1 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_visualizador_temperatura` | Layer 4: Frameworks & Drivers ⚠️ |
| 2 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.__init__` | Layer 4: Frameworks & Drivers ⚠️ |
| 3 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_climatizador` | Layer 4: Frameworks & Drivers ⚠️ |
| 4 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.configurador` | Layer 4: Frameworks & Drivers ⚠️ |
| 5 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_visualizador_climatizador` | Layer 4: Frameworks & Drivers ⚠️ |
| 6 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_sensor_temperatura` | Layer 4: Frameworks & Drivers ⚠️ |
| 7 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_proxy_bateria` | Layer 4: Frameworks & Drivers ⚠️ |
| 8 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_selector_temperatura` | Layer 4: Frameworks & Drivers ⚠️ |
| 9 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_seteo_temperatura` | Layer 4: Frameworks & Drivers ⚠️ |
| 10 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_actuador_climatizador` | Layer 4: Frameworks & Drivers ⚠️ |
| 11 | `servicios_aplicacion.selector_entrada` | Layer 3: Interface Adapters | `configurador.factory_visualizador_bateria` | Layer 4: Frameworks & Drivers ⚠️ |
| 12 | `servicios_aplicacion.lanzador` | Layer 3: Interface Adapters | `configurador.factory_visualizador_temperatura` | Layer 4: Frameworks & Drivers ⚠️ |
| 13 | `servicios_aplicacion.lanzador` | Layer 3: Interface Adapters | `configurador.__init__` | Layer 4: Frameworks & Drivers ⚠️ |
| 14 | `servicios_aplicacion.lanzador` | Layer 3: Interface Adapters | `configurador.factory_climatizador` | Layer 4: Frameworks & Drivers ⚠️ |
| 15 | `servicios_aplicacion.lanzador` | Layer 3: Interface Adapters | `configurador.configurador` | Layer 4: Frameworks & Drivers ⚠️ |

*...y 9 violaciones moderadas más*

**Recomendaciones**:
1. Aplicar Dependency Inversion Principle (DIP)
2. Crear abstracciones en capas internas
3. Inyectar dependencias desde capas externas
4. Usar eventos/mensajes para desacoplar capas

---

## 5. ACYCLIC DEPENDENCIES PRINCIPLE (ADP)

Se detectaron **1 ciclos** entre paquetes.

**Principio violado**: Los paquetes no deben formar ciclos de dependencias.

### 5.1 Ciclo 1

```
configurador
  ↓
agentes_sensores
  ↓
servicios_aplicacion
  ↓
configurador
```

**Impacto**: Los ciclos hacen difícil:
- Compilar/probar paquetes de forma independiente
- Entender el orden de construcción
- Reutilizar paquetes en otros proyectos

**Soluciones**:
1. Aplicar Dependency Inversion Principle
2. Crear nuevo paquete con abstracciones comunes
3. Mover clases entre paquetes
4. Usar patrón Observer/Mediator

---

## 6. DIAGRAMA ABSTRACTNESS vs INSTABILITY

Posición de cada paquete en el gráfico A vs I:

```
A (Abstractness)
1.0 │                    Zone of
    │                   Uselessness
    │                  ╱
    │                ╱
0.5 │              ╱  Main Sequence
    │            ╱
    │          ╱
    │  Zone  ╱
    │  of   ╱
    │ Pain ╱
0.0 └────────────────────────────────
    0.0    0.5                    1.0
           I (Instability)
```

| Paquete | A | I | Posición |
|---------|---|---|----------|
| `registrador` | 1.000 | 0.000 | Main Sequence (Ideal) |
| `servicios_aplicacion` | 0.250 | 0.750 | Main Sequence (Ideal) |
| `entidades` | 0.636 | 0.200 | Main Sequence (Ideal) |
| `agentes_sensores` | 0.000 | 0.750 | Suboptimal (Needs adjustment) |
| `configurador` | 0.000 | 0.750 | Suboptimal (Needs adjustment) |
| `agentes_actuadores` | 0.000 | 0.667 | Suboptimal (Needs adjustment) |
| `actores_externos` | 0.000 | 0.000 | Zone of Pain (Rigid) |
| `gestores_entidades` | 0.000 | 0.000 | Zone of Pain (Rigid) |
| `servicios_dominio` | 0.000 | 0.000 | Zone of Pain (Rigid) |

---

## 7. CONCLUSIONES Y RECOMENDACIONES

### 7.1 Puntos Fuertes ⭐

4. **Sin paquetes en Zone of Uselessness**: No hay abstracciones innecesarias

### 7.2 Áreas de Mejora ⚠️

1. **3 paquetes en Zone of Pain**: Introducir abstracciones
3. **24 violaciones de capas**: Invertir dependencias
4. **1 ciclos entre paquetes**: Romper ciclos

### 7.3 Plan de Acción

#### Prioridad Alta
1. Resolver violaciones críticas de la Regla de Dependencia
2. Eliminar ciclos entre paquetes
3. Extraer interfaces de paquetes en Zone of Pain

#### Prioridad Media
2. Mejorar balance A/I en paquetes con D > 0.3
3. Documentar decisiones arquitectónicas

#### Prioridad Baja
1. Crear diagramas de arquitectura por capas
2. Establecer métricas objetivo para nuevos paquetes
3. Automatizar verificación de métricas en CI/CD

### 7.4 Calificación General

**Clean Architecture del Proyecto**: **3.0/10** ⚠️

| Indicador | Valor | Umbral | Estado |
|-----------|-------|--------|--------|
| Distance promedio | 0.444 | ≤ 0.3 | ❌ |
| Paquetes en Main Seq. | 3/9 | ≥ 50% | ❌ |
| Zone of Pain | 3 | 0 | ❌ |
| Violaciones de capas | 24 | 0 | ❌ |
| Ciclos entre paquetes | 1 | 0 | ❌ |

---

**Fin del Reporte de Clean Architecture**

*Generado con: Script personalizado basado en AST de Python*
*Fecha: 2025-12-16 08:49:18*
