# PLAN DE REFACTORIZACION: servicios_aplicacion

**Proyecto**: ISSE_Termostato
**Paquete**: servicios_aplicacion
**Fecha**: 2025-12-07
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| lanzador.py | 94 | 53 | 1 | 2 |
| operador_paralelo.py | 78 | 55 | 1 | 8 |
| operador_secuencial.py | 63 | 35 | 1 | 2 |
| selector_entrada.py | 46 | 23 | 1 | 4 |
| presentador.py | 41 | 22 | 1 | 2 |
| inicializador.py | 27 | 18 | 1 | 1 |
| abs_selector_temperatura.py | 9 | 6 | 1 | 1 |
| abs_seteo_temperatura.py | 9 | 6 | 1 | 1 |
| **TOTAL** | **367** | **218** | **8** | **21** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 1.93 (A) | <= 5 | ✅ Excelente |
| MI Promedio | ~94 (A) | >= 65 | ✅ Excelente |
| Pylint Score | 1.94/10 | >= 8.0 | ❌ Critico |

### 1.3 Distribucion de Issues Pylint

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Error (E) | 6 | E0401 import-error, E0602 undefined-variable |
| Warning (W) | 4 | W0401 wildcard-import, W0105 pointless-string-statement |
| Convention (C) | 5 | C0115 missing-class-docstring, C0116 missing-function-docstring, C0304 missing-final-newline |
| Refactor (R) | 5 | R0903 too-few-public-methods, R0801 duplicate-code |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Wildcard Imports (W0401)

**Archivos afectados**: 3

```python
# operador_secuencial.py
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *

# operador_paralelo.py
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *

# selector_entrada.py
from agentes_sensores.proxy_seteo_temperatura import *
from gestores_entidades.gestor_ambiente import *
```

### 2.2 Violacion DIP en selector_entrada.py

**Problema**: Uso de Configurador directamente en constructor.

```python
# ACTUAL - Viola DIP
def __init__(self, gestor_ambiente):
    self._seteo_temperatura = Configurador.configurar_seteo_temperatura()
    self._selector_temperatura = Configurador.configurar_selector_temperatura()
    self._gestor_ambiente = gestor_ambiente

# MEJOR - Inyeccion de dependencias
def __init__(self, gestor_ambiente, seteo_temperatura, selector_temperatura):
    self._seteo_temperatura = seteo_temperatura
    self._selector_temperatura = selector_temperatura
    self._gestor_ambiente = gestor_ambiente
```

### 2.3 Pointless String Statement (W0105)

**Archivo**: operador_secuencial.py linea 37-38

```python
# ACTUAL - String sin efecto
'Ciclo infinito que establece la secuencia de acciones' \
'del termostato'

# MEJOR - Comentario
# Ciclo infinito que establece la secuencia de acciones del termostato
```

### 2.4 Useless Returns (R1711)

**Archivo**: operador_paralelo.py - returns despues de while True

```python
# ACTUAL - return inalcanzable
def lee_carga_bateria(self):
    while True:
        ...
    return  # Nunca se ejecuta

# MEJOR - Sin return
def lee_carga_bateria(self):
    while True:
        ...
```

### 2.5 Missing Docstrings

| Archivo | Clase | Metodos sin docstring |
|---------|-------|----------------------|
| operador_paralelo.py | ❌ | __init__, lee_*, acciona_*, muestra_*, setea_*, ejecutar |
| operador_secuencial.py | ❌ | ejecutar |
| selector_entrada.py | ❌ | - |
| presentador.py | ❌ | - |
| inicializador.py | ❌ | iniciar |
| abs_selector_temperatura.py | ❌ | obtener_selector |
| abs_seteo_temperatura.py | ❌ | obtener_seteo |

### 2.6 Codigo Duplicado (R0801)

**Entre**: operador_paralelo.py y operador_secuencial.py

```python
# Codigo duplicado en __init__
self._gestor_bateria = gestor_bateria
self._gestor_ambiente = gestor_ambiente
self._gestor_climatizador = gestor_climatizador
self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
self._presentador = Presentador(self._gestor_bateria,
                                self._gestor_ambiente,
                                self._gestor_climatizador)
```

**Solucion**: Extraer clase base abstracta `AbsOperador`.

### 2.7 Empty Module Docstring

**Archivo**: operador_paralelo.py tiene docstring vacio `""" """`

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios por Fase

| Fase | Descripcion | Archivos | Prioridad |
|------|-------------|----------|-----------|
| 1 | Reemplazar wildcard imports | 3 | ALTA |
| 2 | Agregar docstrings | 7 | ALTA |
| 3 | Corregir pointless string y useless returns | 2 | MEDIA |
| 4 | Aplicar DIP a selector_entrada.py | 2 | MEDIA |
| 5 | Extraer clase base AbsOperador (opcional) | 3 | BAJA |

---

### 3.2 Fase 1: Imports Explicitos

#### operador_secuencial.py
```python
# ANTES
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *

# DESPUES
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador
```

#### operador_paralelo.py
```python
# ANTES
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *

# DESPUES
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador
```

#### selector_entrada.py
```python
# ANTES
from agentes_sensores.proxy_seteo_temperatura import *
from gestores_entidades.gestor_ambiente import *

# DESPUES
from configurador.configurador import Configurador
# Nota: GestorAmbiente ya no se importa, se recibe por DI
```

---

### 3.3 Fase 2: Docstrings

Agregar docstrings a todas las clases y metodos publicos siguiendo el formato:

```python
class OperadorParalelo:
    """
    Orquestador de operaciones del termostato usando hilos paralelos.

    Ejecuta las operaciones de lectura de sensores, accionamiento del
    climatizador y visualizacion en hilos separados para operacion
    concurrente.

    Attributes:
        _gestor_bateria: Gestor de operaciones de bateria.
        _gestor_ambiente: Gestor de operaciones de ambiente.
        _gestor_climatizador: Gestor de operaciones de climatizador.
    """
```

---

### 3.4 Fase 3: Correcciones Menores

#### operador_secuencial.py - Pointless string
```python
# ANTES
'Ciclo infinito...'

# DESPUES
# Ciclo infinito que establece la secuencia de acciones del termostato
```

#### operador_paralelo.py - Useless returns
```python
# ANTES
def lee_carga_bateria(self):
    while True:
        ...
    return

# DESPUES
def lee_carga_bateria(self):
    """Lee periodicamente la carga de bateria."""
    while True:
        self._gestor_bateria.verificar_nivel_de_carga()
        time.sleep(1)
```

---

### 3.5 Fase 4: DIP en selector_entrada.py

```python
# ANTES
class SelectorEntradaTemperatura:
    def __init__(self, gestor_ambiente):
        self._seteo_temperatura = Configurador.configurar_seteo_temperatura()
        self._selector_temperatura = Configurador.configurar_selector_temperatura()
        self._gestor_ambiente = gestor_ambiente

# DESPUES
class SelectorEntradaTemperatura:
    def __init__(self, gestor_ambiente, seteo_temperatura, selector_temperatura):
        self._seteo_temperatura = seteo_temperatura
        self._selector_temperatura = selector_temperatura
        self._gestor_ambiente = gestor_ambiente
```

**Actualizar llamadores** en operador_paralelo.py y operador_secuencial.py:
```python
# En Lanzador o en operadores
seteo = Configurador.configurar_seteo_temperatura()
selector = Configurador.configurar_selector_temperatura()
self._selector = SelectorEntradaTemperatura(gestor_ambiente, seteo, selector)
```

---

## 4. ORDEN DE EJECUCION

### Fase 1: Imports Explicitos
1. [ ] Actualizar operador_secuencial.py
2. [ ] Actualizar operador_paralelo.py
3. [ ] Actualizar selector_entrada.py
4. [ ] Verificar que tests pasan

### Fase 2: Docstrings
5. [ ] Agregar docstrings a operador_paralelo.py
6. [ ] Agregar docstrings a operador_secuencial.py
7. [ ] Agregar docstrings a selector_entrada.py
8. [ ] Agregar docstrings a presentador.py
9. [ ] Agregar docstrings a inicializador.py
10. [ ] Agregar docstrings a abs_selector_temperatura.py
11. [ ] Agregar docstrings a abs_seteo_temperatura.py
12. [ ] Verificar que tests pasan

### Fase 3: Correcciones Menores
13. [ ] Corregir pointless string en operador_secuencial.py
14. [ ] Eliminar useless returns en operador_paralelo.py
15. [ ] Agregar final newline en presentador.py
16. [ ] Verificar que tests pasan

### Fase 4: DIP (Opcional)
17. [ ] Modificar SelectorEntradaTemperatura para inyeccion
18. [ ] Actualizar operador_paralelo.py
19. [ ] Actualizar operador_secuencial.py
20. [ ] Verificar que tests pasan

---

## 5. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 1.93 | <= 2 (mantener) |
| MI Promedio | ~94 | >= 90 (mantener) |
| Pylint Score | 1.94 | >= 9.0 |
| Wildcard Imports | 4 | 0 |
| Docstrings | ~30% | >= 90% |

---

## 6. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| DIP rompe operadores | Media | Alto | Actualizar todos los llamadores |
| Codigo duplicado persiste | Baja | Bajo | Fase 5 opcional para extraer base |

---

## 7. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 2
- [ ] MI >= 90
- [ ] Pylint Score >= 9.0
- [ ] Sin wildcard imports
- [ ] Todas las clases con docstrings

---

## 8. NOTAS ADICIONALES

### 8.1 Lanzador.py
Este archivo ya fue refactorizado como Composition Root en la fase de
gestores_entidades. Tiene buena calidad de codigo con docstrings completos.

### 8.2 Codigo Duplicado
La extraccion de clase base AbsOperador se deja como fase opcional (5)
porque requiere mayor refactorizacion y el beneficio es marginal dado
que solo hay 2 operadores.

---

*Documento generado: 2025-12-07*
