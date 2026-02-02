# PLAN DE REVISION TRANSVERSAL PYLINT

**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-09
**Score Actual**: 9.41/10
**Objetivo**: >= 9.80/10

---

## 0. RESTRICCIONES DEL PROYECTO

### 0.1 Compatibilidad Python 3.5 (Raspberry Pi)

El proyecto debe mantener compatibilidad con Python 3.5 para su ejecucion en Raspberry Pi.

**Issues EXCLUIDOS de correccion:**
- **C0209 (consider-using-f-string)**: Los f-strings requieren Python 3.6+. Se mantendra el uso de `.format()` para compatibilidad.

### 0.2 Paquetes sin `__init__.py`

Los siguientes paquetes requieren `__init__.py` para ser reconocidos correctamente:

| Paquete | Estado |
|---------|--------|
| servicios_aplicacion | ✗ FALTA |
| gestores_entidades | ✗ FALTA |
| servicios_dominio | ✗ FALTA |
| configurador | ✗ FALTA |
| agentes_sensores | ✗ FALTA |
| agentes_actuadores | ✗ FALTA |
| entidades | ✗ FALTA |
| registrador | ✓ OK |
| actores_externos | ✓ OK |

---

## 1. RESUMEN DE ISSUES POR TIPO

| Tipo | Codigo | Descripcion | Cantidad | Prioridad | Accion |
|------|--------|-------------|----------|-----------|--------|
| Convention | C0209 | consider-using-f-string | 22 | - | **IGNORAR** (compatibilidad Python 3.5) |
| Convention | C0304 | missing-final-newline | 3 | ALTA | Corregir |
| Convention | C0301 | line-too-long | 3 | ALTA | Corregir |
| Convention | C0411 | wrong-import-order | 1 | ALTA | Corregir |
| Warning | W0221 | arguments-differ | 12 | MEDIA | Corregir |
| Warning | W0107 | unnecessary-pass | 10 | MEDIA | Corregir |
| Warning | W0611 | unused-import | 1 | ALTA | Corregir |
| Refactor | R0903 | too-few-public-methods | 4 | BAJA | Disable |
| Refactor | R0801 | duplicate-code | 6 | BAJA | Disable |

---

## 2. ISSUES POR PAQUETE (Excluyendo C0209)

### 2.1 agentes_sensores (1 issue real)

| Archivo | Linea | Issue | Descripcion |
|---------|-------|-------|-------------|
| proxy_seteo_temperatura.py | 66 | W0221 | arguments-differ |

### 2.2 agentes_actuadores (10 issues reales)

| Archivo | Linea | Issue | Descripcion |
|---------|-------|-------|-------------|
| actuador_climatizador.py | 7 | W0611 | unused-import |
| actuador_climatizador.py | 11 | C0411 | wrong-import-order |
| actuador_climatizador.py | 88 | W0221 | arguments-differ |
| visualizador_climatizador.py | 45,88 | W0221 | arguments-differ (2) |
| visualizador_temperatura.py | 141 | C0304 | missing-final-newline |
| visualizador_temperatura.py | 115,129 | W0221 | arguments-differ (2) |
| visualizador_bateria.py | 54,71,113,127 | W0221 | arguments-differ (4) |

### 2.3 entidades (14 issues reales)

| Archivo | Linea | Issue | Descripcion |
|---------|-------|-------|-------------|
| ambiente.py | 107 | C0301 | line-too-long (115 chars) |
| ambiente.py | 130 | C0304 | missing-final-newline |
| climatizador.py | 93 | C0301 | line-too-long (103 chars) |
| climatizador.py | 114,162 | W0107 | unnecessary-pass (2) |
| abs_actuador_climatizador.py | 71 | C0304 | missing-final-newline |
| abs_actuador_climatizador.py | 66 | W0107 | unnecessary-pass |
| abs_actuador_climatizador.py | 21 | R0903 | too-few-public-methods |
| abs_bateria.py | 49 | W0107 | unnecessary-pass |
| abs_bateria.py | 19 | R0903 | too-few-public-methods |
| bateria.py | 95 | C0301 | line-too-long (107 chars) |
| abs_visualizador_bateria.py | 58,74 | W0107 | unnecessary-pass (2) |
| abs_visualizador_climatizador.py | 67 | W0107 | unnecessary-pass |
| abs_visualizador_climatizador.py | 33 | R0903 | too-few-public-methods |
| abs_visualizador_temperatura.py | 60,78 | W0107 | unnecessary-pass (2) |
| abs_sensor_temperatura.py | 56 | W0107 | unnecessary-pass |
| abs_sensor_temperatura.py | 19 | R0903 | too-few-public-methods |

---

## 3. PLAN DE CORRECCION POR FASES

### FASE 0: Crear `__init__.py` en paquetes faltantes
**Prioridad: CRITICA**

Crear archivos `__init__.py` en los siguientes paquetes:

- [ ] servicios_aplicacion/__init__.py
- [ ] gestores_entidades/__init__.py
- [ ] servicios_dominio/__init__.py
- [ ] configurador/__init__.py
- [ ] agentes_sensores/__init__.py
- [ ] agentes_actuadores/__init__.py
- [ ] entidades/__init__.py

---

### FASE 1: Correcciones Rapidas (Alta Prioridad)

#### 1.1 Missing Final Newline (C0304) - 3 archivos
- [ ] agentes_actuadores/visualizador_temperatura.py:141
- [ ] entidades/ambiente.py:130
- [ ] entidades/abs_actuador_climatizador.py:71

#### 1.2 Wrong Import Order (C0411) - 1 archivo
- [ ] agentes_actuadores/actuador_climatizador.py:11
  - Mover `import datetime` antes de imports locales

#### 1.3 Unused Import (W0611) - 1 archivo
- [ ] agentes_actuadores/actuador_climatizador.py:7
  - Eliminar `AbsActuadorClimatizador` del import

---

### FASE 2: Line Too Long (C0301) - 3 ocurrencias

- [ ] entidades/ambiente.py:107 (115 chars)
- [ ] entidades/climatizador.py:93 (103 chars)
- [ ] entidades/bateria.py:95 (107 chars)

---

### FASE 3: Arguments Differ (W0221) - 12 ocurrencias

Este issue indica que las clases hijas tienen firmas diferentes a las clases base abstractas.

**Solucion recomendada**: Actualizar las clases base abstractas para incluir los parametros adicionales.

| Archivo | Metodo Base | Params Base | Params Override |
|---------|-------------|-------------|-----------------|
| proxy_seteo_temperatura.py:66 | AbsSeteoTemperatura.obtener_seteo | 0 | 1 |
| visualizador_climatizador.py:45 | AbsVisualizadorClimatizador.mostrar_estado_climatizador | 1 | 2 |
| visualizador_climatizador.py:88 | AbsVisualizadorClimatizador.mostrar_estado_climatizador | 1 | 2 |
| actuador_climatizador.py:88 | AbsAuditor.auditar_funcion | 1 | 3 |
| visualizador_temperatura.py:115 | AbsVisualizadorTemperatura.mostrar_temperatura_ambiente | 1 | 2 |
| visualizador_temperatura.py:129 | AbsVisualizadorTemperatura.mostrar_temperatura_deseada | 1 | 2 |
| visualizador_bateria.py:54 | AbsVisualizadorBateria.mostrar_tension | 1 | 2 |
| visualizador_bateria.py:71 | AbsVisualizadorBateria.mostrar_indicador | 1 | 2 |
| visualizador_bateria.py:113 | AbsVisualizadorBateria.mostrar_tension | 1 | 2 |
| visualizador_bateria.py:127 | AbsVisualizadorBateria.mostrar_indicador | 1 | 2 |

---

### FASE 4: Unnecessary Pass (W0107) - 10 ocurrencias

En metodos abstractos, el `pass` es innecesario si hay un docstring.

```python
# ANTES
@abstractmethod
def metodo(self):
    """Docstring."""
    pass

# DESPUES
@abstractmethod
def metodo(self):
    """Docstring."""
```

- [ ] entidades/climatizador.py:114,162
- [ ] entidades/abs_actuador_climatizador.py:66
- [ ] entidades/abs_bateria.py:49
- [ ] entidades/abs_visualizador_bateria.py:58,74
- [ ] entidades/abs_visualizador_climatizador.py:67
- [ ] entidades/abs_visualizador_temperatura.py:60,78
- [ ] entidades/abs_sensor_temperatura.py:56

---

### FASE 5: Disable para Issues Aceptables

#### 5.1 Too Few Public Methods (R0903) - 4 archivos
Agregar `# pylint: disable=too-few-public-methods` en clases abstractas:

- [ ] entidades/abs_actuador_climatizador.py:21
- [ ] entidades/abs_bateria.py:19
- [ ] entidades/abs_visualizador_climatizador.py:33
- [ ] entidades/abs_sensor_temperatura.py:19

#### 5.2 Duplicate Code (R0801)
Agregar `# pylint: disable=duplicate-code` en archivos con codigo duplicado aceptable.

#### 5.3 Consider Using F-String (C0209)
Agregar en `.pylintrc` o en cada paquete:
```
# pylint: disable=consider-using-f-string
```

---

## 4. ORDEN DE EJECUCION RECOMENDADO

| Fase | Descripcion | Issues | Archivos |
|------|-------------|--------|----------|
| 0 | Crear __init__.py | - | 7 |
| 1 | Correcciones rapidas | 5 | 3 |
| 2 | Line too long | 3 | 3 |
| 3 | Arguments differ | 12 | 6 |
| 4 | Unnecessary pass | 10 | 8 |
| 5 | Disables para issues aceptables | ~30 | varios |

---

## 5. METRICAS OBJETIVO

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| Pylint Score | 9.41/10 | >= 9.80/10 |
| C0304 (newline) | 3 | 0 |
| C0301 (line-too-long) | 3 | 0 |
| W0221 (arguments-differ) | 12 | 0 |
| W0107 (unnecessary-pass) | 10 | 0 |
| W0611 (unused-import) | 1 | 0 |
| C0411 (wrong-import-order) | 1 | 0 |

**Nota**: C0209 (f-strings) sera deshabilitado globalmente por compatibilidad con Python 3.5.

---

## 6. CONFIGURACION PYLINT RECOMENDADA

Crear o actualizar `.pylintrc` con:

```ini
[MESSAGES CONTROL]
disable=
    consider-using-f-string,  # Compatibilidad Python 3.5
    duplicate-code,           # Aceptable en este proyecto
    too-few-public-methods    # Normal en ABCs
```

---

*Documento generado: 2025-12-09*
*Actualizado: 2025-12-09 - Restricciones Python 3.5 y __init__.py*
*Herramienta: pylint*
