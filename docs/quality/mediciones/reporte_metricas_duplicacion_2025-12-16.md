# REPORTE DE MÉTRICAS DE DUPLICACIÓN
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-16
**Herramientas**: jscpd v4.0.5
**Alcance**: Código de producción (excluye tests, docs, build, actores_externos)

---

## RESUMEN EJECUTIVO

### Visión General

Las métricas de duplicación detectan código repetido (clones) que puede indicar oportunidades de refactorización. Un bajo porcentaje de duplicación mejora la mantenibilidad y reduce el riesgo de inconsistencias.

| Concepto | Valor | Interpretación |
|----------|-------|----------------|
| **Archivos analizados** | 58 | Archivos Python del proyecto |
| **Líneas totales** | 3,504 | LOC del código de producción |
| **Tokens totales** | 12,057 | Unidades léxicas analizadas |
| **Clones encontrados** | 3 | Bloques de código duplicado |
| **Líneas duplicadas** | 40 (1.14%) | ✅ Muy bajo |
| **Tokens duplicados** | 307 (2.55%) | ✅ Bajo |

### Interpretación de Umbrales

| Nivel | Porcentaje | Interpretación |
|-------|------------|----------------|
| **Excelente** | < 3% | ✅ Duplicación mínima |
| **Bueno** | 3-5% | Duplicación aceptable |
| **Moderado** | 5-10% | Requiere atención |
| **Alto** | 10-20% | Refactorización recomendada |
| **Crítico** | > 20% | Refactorización urgente |

**Estado actual: EXCELENTE** (1.14% líneas duplicadas)

---

## 1. MÉTRICAS DE DUPLICACIÓN EXPLICADAS

### 1.1 Tipos de Clones

| Tipo | Descripción | Detección |
|------|-------------|-----------|
| **Tipo 1** | Clones idénticos (copia exacta) | jscpd detecta |
| **Tipo 2** | Clones con variaciones de nombres | jscpd detecta |
| **Tipo 3** | Clones con modificaciones estructurales | Parcialmente |
| **Tipo 4** | Clones semánticos (lógica similar) | No detectado |

### 1.2 Parámetros de Detección

```
Configuración jscpd:
- min-lines: 5 (mínimo 5 líneas para considerar clon)
- min-tokens: 50 (mínimo 50 tokens para considerar clon)
- format: python
```

---

## 2. CLONES DETECTADOS

### Clon #1: Inicialización de Operadores

| Atributo | Valor |
|----------|-------|
| **Tipo** | Tipo 2 (estructural) |
| **Líneas** | 17 |
| **Tokens** | 91 |
| **Severidad** | Baja |

**Archivos involucrados:**

| Archivo | Líneas | % Duplicado |
|---------|--------|-------------|
| `servicios_aplicacion/operador_paralelo.py` | 35-52 | 16.04% |
| `servicios_aplicacion/operador_secuencial.py` | 33-50 | 20.48% |

**Fragmento duplicado:**
```python
def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
    """
    Inicializa el operador con los gestores necesarios.
    """
    self._gestor_bateria = gestor_bateria
    self._gestor_ambiente = gestor_ambiente
    self._gestor_climatizador = gestor_climatizador
    self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
    self._presentador = Presentador(self._gestor_bateria,
                                    self._gestor_ambiente,
                                    self._gestor_climatizador)
```

**Análisis**: Ambos operadores comparten la misma inicialización. Es un patrón de diseño válido donde ambas clases heredan comportamiento similar. Podría extraerse a una clase base abstracta, pero el costo de refactorización supera el beneficio dado el bajo impacto.

---

### Clon #2: Configuración de Socket (Selector/Seteo)

| Atributo | Valor |
|----------|-------|
| **Tipo** | Tipo 1 (idéntico) |
| **Líneas** | 8 |
| **Tokens** | 90 |
| **Severidad** | Baja |

**Archivos involucrados:**

| Archivo | Líneas | % Duplicado |
|---------|--------|-------------|
| `agentes_sensores/proxy_selector_temperatura.py` | 93-101 | 5.41% |
| `agentes_sensores/proxy_seteo_temperatura.py` | 55-63 | 7.14% |

**Fragmento duplicado:**
```python
self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

direccion_servidor = (host, puerto)
self._servidor.bind(direccion_servidor)
self._servidor.listen(1)

self._conexion = None
self._servidor.settimeout(1.0)
```

**Análisis**: Código de infraestructura para sockets TCP. Es un patrón técnico común que podría extraerse a una clase `SocketServer` base, pero la duplicación es mínima.

---

### Clon #3: Configuración de Socket (Batería/Temperatura)

| Atributo | Valor |
|----------|-------|
| **Tipo** | Tipo 2 (estructural) |
| **Líneas** | 15 |
| **Tokens** | 126 |
| **Severidad** | Baja |

**Archivos involucrados:**

| Archivo | Líneas | % Duplicado |
|---------|--------|-------------|
| `agentes_sensores/proxy_bateria.py` | 65-80 | 17.44% |
| `agentes_sensores/proxy_sensor_temperatura.py` | 65-80 | 17.44% |

**Fragmento duplicado:**
```python
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

direccion_servidor = (self._host, self._puerto)
servidor.bind(direccion_servidor)

servidor.listen(1)
conexion, _ = servidor.accept()

try:
    while True:
        datos = conexion.recv(4096)
        if not datos:
            break
```

**Análisis**: Similar al clon #2, código de infraestructura de sockets. Ambos proxies socket comparten el patrón de recepción de datos.

---

## 3. ANÁLISIS POR PAQUETE

### Distribución de Duplicación por Paquete

| Paquete | Archivos | Líneas | Clones | Líneas Dup. | % |
|---------|----------|--------|--------|-------------|---|
| `agentes_sensores` | 5 | 442 | 3 | 31 | 7.01% |
| `servicios_aplicacion` | 11 | 496 | 1 | 17 | 3.43% |
| `agentes_actuadores` | 5 | 493 | 0 | 0 | 0.00% |
| `entidades` | 13 | 892 | 0 | 0 | 0.00% |
| `configurador` | 11 | 503 | 0 | 0 | 0.00% |
| `gestores_entidades` | 4 | 304 | 0 | 0 | 0.00% |
| `servicios_dominio` | 2 | 58 | 0 | 0 | 0.00% |
| `registrador` | 2 | 68 | 0 | 0 | 0.00% |
| Otros (setup, ejecutar) | 9 | 178 | 0 | 0 | 0.00% |
| **TOTAL** | **58** | **3,504** | **3** | **40** | **1.14%** |

### Archivos con Mayor Duplicación

| # | Archivo | % Tokens Dup. | Líneas Dup. |
|---|---------|---------------|-------------|
| 1 | `proxy_bateria.py` | 34.90% | 15 |
| 2 | `proxy_sensor_temperatura.py` | 34.05% | 15 |
| 3 | `operador_secuencial.py` | 28.89% | 17 |
| 4 | `operador_paralelo.py` | 19.83% | 17 |
| 5 | `proxy_seteo_temperatura.py` | 16.19% | 8 |
| 6 | `proxy_selector_temperatura.py` | 10.39% | 8 |

### Archivos Sin Duplicación (52 de 58)

El 89.7% de los archivos no tienen código duplicado, incluyendo:
- Todas las entidades del dominio
- Todo el configurador y factories
- Todos los gestores de entidades
- Todos los visualizadores (agentes_actuadores)
- Servicios de dominio

---

## 4. COMPARACIÓN CON ESTÁNDARES

### Benchmarks de la Industria

| Proyecto | % Duplicación | Referencia |
|----------|---------------|------------|
| **ISSE_Termostato** | **1.14%** | ✅ Este proyecto |
| Proyectos bien mantenidos | 3-5% | Bueno |
| Proyectos típicos | 5-15% | Normal |
| Proyectos legacy | 15-30% | Problemático |
| Código copy-paste | > 30% | Crítico |

### Umbrales SonarQube

| Métrica | Umbral | Valor Actual | Estado |
|---------|--------|--------------|--------|
| Duplicated Lines | < 3% | 1.14% | ✅ A |
| Duplicated Blocks | < 10 | 3 | ✅ A |

---

## 5. OPORTUNIDADES DE REFACTORIZACIÓN

### 5.1 Prioridad Baja - Socket Infrastructure

**Descripción**: Extraer la lógica común de sockets a una clase base.

**Archivos afectados**:
- `proxy_bateria.py`
- `proxy_sensor_temperatura.py`
- `proxy_selector_temperatura.py`
- `proxy_seteo_temperatura.py`

**Posible solución**:
```python
class ProxySocketBase:
    def _crear_servidor_socket(self, host, puerto):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, puerto))
        servidor.listen(1)
        return servidor
```

**Impacto**: Reduciría ~23 líneas duplicadas
**Recomendación**: OPCIONAL - El beneficio es marginal

### 5.2 Prioridad Baja - Operadores Base

**Descripción**: Crear clase base para operadores.

**Archivos afectados**:
- `operador_paralelo.py`
- `operador_secuencial.py`

**Impacto**: Reduciría ~17 líneas duplicadas
**Recomendación**: OPCIONAL - La duplicación actual es aceptable

---

## 6. MÉTRICAS COMPLEMENTARIAS

### Densidad de Código por Archivo

| Métrica | Valor |
|---------|-------|
| Promedio LOC/archivo | 60.4 |
| Mediana LOC/archivo | 36 |
| Máximo LOC/archivo | 266 (climatizador.py) |
| Mínimo LOC/archivo | 6 (__init__.py) |

### Distribución de Tokens

| Rango Tokens | Archivos | % |
|--------------|----------|---|
| 0-50 | 15 | 25.9% |
| 51-150 | 17 | 29.3% |
| 151-300 | 12 | 20.7% |
| 301-500 | 9 | 15.5% |
| > 500 | 5 | 8.6% |

---

## 7. CONCLUSIONES Y RECOMENDACIONES

### 7.1 Puntos Fuertes

1. **Duplicación mínima**: Solo 1.14% de líneas duplicadas
2. **Clones localizados**: Los 3 clones están en código de infraestructura
3. **Dominio limpio**: Las entidades y servicios de dominio no tienen duplicación
4. **Factories sin duplicación**: A pesar de ser estructuralmente similares

### 7.2 Áreas de Mejora

1. **Considerar clase base para proxies socket** (mejora opcional)
2. **Documentar la duplicación intencional** en operadores

### 7.3 Indicadores Clave (KPI)

| Indicador | Valor | Umbral | Estado |
|-----------|-------|--------|--------|
| % Líneas Duplicadas | 1.14% | < 3% | ✅ |
| % Tokens Duplicados | 2.55% | < 5% | ✅ |
| Clones Totales | 3 | < 10 | ✅ |
| Archivos con Dup. | 6/58 (10.3%) | < 20% | ✅ |

### 7.4 Calificación General

**Métricas de Duplicación del Proyecto**: **9.5/10**

| Aspecto | Puntuación |
|---------|------------|
| Porcentaje de duplicación | 10/10 |
| Localización de clones | 9/10 |
| Impacto en mantenibilidad | 10/10 |
| Oportunidades de mejora | 9/10 |

---

## 8. COMPARACIÓN HISTÓRICA

### Evolución (si hubiera mediciones anteriores)

| Fecha | Clones | % Líneas | % Tokens |
|-------|--------|----------|----------|
| 2025-12-16 | 3 | 1.14% | 2.55% |

---

**Fin del Reporte de Métricas de Duplicación**

*Generado con: jscpd v4.0.5*
*Fecha: 2025-12-16*
*Configuración: min-lines=5, min-tokens=50*
