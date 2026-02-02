# PLAN DE REFACTORIZACION: configurador

**Proyecto**: ISSE_Termostato
**Paquete**: configurador
**Fecha**: 2025-12-07
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| configurador.py | 160 | 115 | 1 | 18 |
| factory_climatizador.py | 33 | 9 | 1 | 1 |
| factory_proxy_bateria.py | 18 | 10 | 1 | 1 |
| factory_sensor_temperatura.py | 18 | 10 | 1 | 1 |
| factory_actuador_climatizador.py | 17 | 9 | 1 | 1 |
| factory_selector_temperatura.py | 18 | 10 | 1 | 1 |
| factory_seteo_temperatura.py | 18 | 10 | 1 | 1 |
| factory_visualizador_bateria.py | 20 | 12 | 1 | 1 |
| factory_visualizador_climatizador.py | 20 | 12 | 1 | 1 |
| factory_visualizador_temperatura.py | 20 | 12 | 1 | 1 |
| **TOTAL** | **342** | **209** | **10** | **27** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 2.58 | <= 5 | ✅ Excelente |
| CC Maximo | B (7) | <= B | ✅ Aceptable |
| MI Promedio | ~89 | >= 65 | ✅ Excelente |
| MI Minimo | 55.31 | >= 50 | ✅ Bueno |
| Pylint Score | 0.00/10 | >= 8.0 | ❌ Critico |

### 1.3 Distribucion de Issues Pylint

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Error (E) | ~30 | E0602 undefined-variable (wildcard imports), E0401 import-error |
| Warning (W) | 9 | W0401 wildcard-import |
| Convention (C) | ~12 | C0115 missing-class-docstring, C0116 missing-function-docstring, C0304 missing-final-newline |
| Refactor (R) | ~18 | R0903 too-few-public-methods, R1705 no-else-return |

**Nota**: Muchos E0602 y E0401 son falsos positivos de pylint que no puede resolver imports dinamicos.

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Wildcard Imports (W0401)

**Problema**: Uso de `from module import *` en configurador.py y factories.

```python
# ACTUAL - configurador.py
from configurador.factory_proxy_bateria import *
from configurador.factory_sensor_temperatura import *
# ... 7 mas

# ACTUAL - factories
from agentes_sensores.proxy_bateria import *
from agentes_actuadores.visualizador_temperatura import *
```

**Impacto**:
- Pylint no puede resolver variables (E0602)
- Namespace contaminado
- No es claro que se importa
- Dificil de mantener

### 2.2 Missing Docstrings (C0115, C0116)

**Problema**: 8 de 9 factories sin docstrings en clase y metodo.

| Archivo | Clase Docstring | Metodo Docstring |
|---------|-----------------|------------------|
| factory_climatizador.py | ✅ | ✅ |
| factory_proxy_bateria.py | ❌ | ❌ |
| factory_sensor_temperatura.py | ❌ | ❌ |
| factory_actuador_climatizador.py | ❌ | ❌ |
| factory_selector_temperatura.py | ❌ | ❌ |
| factory_seteo_temperatura.py | ❌ | ❌ |
| factory_visualizador_bateria.py | ❌ | ❌ |
| factory_visualizador_climatizador.py | ❌ | ❌ |
| factory_visualizador_temperatura.py | ❌ | ❌ |

### 2.3 Elif After Return (R1705)

**Problema**: Uso de `elif` despues de `return` en factories.

```python
# ACTUAL - No pythonico
if tipo == "archivo":
    return ProxyBateriaArchivo()
elif tipo == "socket":
    return ProxyBateriaSocket()
else:
    return None

# MEJOR - Pythonico
if tipo == "archivo":
    return ProxyBateriaArchivo()
if tipo == "socket":
    return ProxyBateriaSocket()
return None
```

### 2.4 Missing Final Newline (C0304)

**Archivos afectados**: factory_visualizador_climatizador.py, factory_proxy_bateria.py

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios por Fase

| Fase | Descripcion | Archivos | Prioridad |
|------|-------------|----------|-----------|
| 1 | Reemplazar wildcard imports por imports explicitos | Todos | ALTA |
| 2 | Agregar docstrings a factories | 8 factories | ALTA |
| 3 | Corregir elif after return | 8 factories | MEDIA |
| 4 | Agregar final newline y pylint disables | Varios | BAJA |

---

### 3.2 Fase 1: Imports Explicitos

**Objetivo**: Eliminar todos los wildcard imports.

#### 3.2.1 configurador.py

```python
# ANTES
from configurador.factory_proxy_bateria import *
from configurador.factory_sensor_temperatura import *
from configurador.factory_actuador_climatizador import *
from configurador.factory_visualizador_bateria import *
from configurador.factory_visualizador_climatizador import *
from configurador.factory_climatizador import *
from configurador.factory_visualizador_temperatura import *
from configurador.factory_selector_temperatura import *
from configurador.factory_seteo_temperatura import *

# DESPUES
from configurador.factory_proxy_bateria import FactoryProxyBateria
from configurador.factory_sensor_temperatura import FactoryProxySensorTemperatura
from configurador.factory_actuador_climatizador import FactoryActuadorClimatizador
from configurador.factory_visualizador_bateria import FactoryVisualizadorBateria
from configurador.factory_visualizador_climatizador import FactoryVisualizadorClimatizador
from configurador.factory_climatizador import FactoryClimatizador
from configurador.factory_visualizador_temperatura import FactoryVisualizadorTemperatura
from configurador.factory_selector_temperatura import FactorySelectorTemperatura
from configurador.factory_seteo_temperatura import FactorySeteoTemperatura
```

#### 3.2.2 Factories (ejemplo factory_proxy_bateria.py)

```python
# ANTES
from agentes_sensores.proxy_bateria import *

# DESPUES
from agentes_sensores.proxy_bateria import (
    AbsProxyBateria,
    ProxyBateriaArchivo,
    ProxyBateriaSocket
)
```

---

### 3.3 Fase 2: Docstrings

**Objetivo**: Agregar docstrings a todas las factories.

```python
# Plantilla para factories
"""
Factory para crear instancias de [componente].

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""

# pylint: disable=too-few-public-methods
class Factory[Componente]:
    """Factory para crear instancias de [componente]."""

    @staticmethod
    def crear(tipo: str) -> Abs[Componente]:
        """
        Crea una instancia del [componente] segun el tipo especificado.

        Args:
            tipo (str): Tipo de [componente] a crear.

        Returns:
            Abs[Componente]: Instancia del [componente] o None si tipo invalido.
        """
```

---

### 3.4 Fase 3: Formateo Pythonico

**Objetivo**: Eliminar `elif` despues de `return`.

```python
# ANTES
if tipo == "archivo":
    return VisualizadorTemperatura()
elif tipo == "socket":
    return VisualizadorTemperaturaSocket()
elif tipo == "api":
    return VisualizadorTemperaturaApi()
else:
    return None

# DESPUES
if tipo == "archivo":
    return VisualizadorTemperatura()
if tipo == "socket":
    return VisualizadorTemperaturaSocket()
if tipo == "api":
    return VisualizadorTemperaturaApi()
return None
```

---

### 3.5 Fase 4: Ajustes Finales

**Objetivo**: Agregar final newlines y pylint disables donde corresponda.

- Agregar `# pylint: disable=too-few-public-methods` a factories
- Asegurar final newline en todos los archivos

---

## 4. ORDEN DE EJECUCION

### Fase 1: Imports Explicitos
1. [ ] Actualizar configurador.py con imports explicitos
2. [ ] Actualizar factory_proxy_bateria.py
3. [ ] Actualizar factory_sensor_temperatura.py
4. [ ] Actualizar factory_selector_temperatura.py
5. [ ] Actualizar factory_seteo_temperatura.py
6. [ ] Actualizar factory_visualizador_bateria.py
7. [ ] Actualizar factory_visualizador_climatizador.py
8. [ ] Actualizar factory_visualizador_temperatura.py
9. [ ] Verificar que tests pasan

### Fase 2: Docstrings
10. [ ] Agregar docstrings a factory_proxy_bateria.py
11. [ ] Agregar docstrings a factory_sensor_temperatura.py
12. [ ] Agregar docstrings a factory_actuador_climatizador.py
13. [ ] Agregar docstrings a factory_selector_temperatura.py
14. [ ] Agregar docstrings a factory_seteo_temperatura.py
15. [ ] Agregar docstrings a factory_visualizador_bateria.py
16. [ ] Agregar docstrings a factory_visualizador_climatizador.py
17. [ ] Agregar docstrings a factory_visualizador_temperatura.py
18. [ ] Verificar que tests pasan

### Fase 3: Formateo Pythonico
19. [ ] Corregir elif en factory_proxy_bateria.py
20. [ ] Corregir elif en factory_sensor_temperatura.py
21. [ ] Corregir elif en factory_selector_temperatura.py
22. [ ] Corregir elif en factory_seteo_temperatura.py
23. [ ] Corregir elif en factory_visualizador_bateria.py
24. [ ] Corregir elif en factory_visualizador_climatizador.py
25. [ ] Corregir elif en factory_visualizador_temperatura.py
26. [ ] Verificar que tests pasan

### Fase 4: Ajustes Finales
27. [ ] Agregar pylint disables a factories
28. [ ] Asegurar final newlines
29. [ ] Verificar metricas finales

---

## 5. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 2.58 | <= 3 (mantener) |
| MI Promedio | ~89 | >= 80 (mantener) |
| Pylint Score | 0.00 | >= 9.0 |
| Wildcard Imports | 9 | 0 |
| Docstrings | ~20% | >= 80% |

---

## 6. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Imports incorrectos | Media | Alto | Verificar cada import con tests |
| Olvidar alguna clase | Baja | Medio | Revisar uso de cada factory |
| Tests fallen | Baja | Alto | Ejecutar tests despues de cada fase |

---

## 7. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 3
- [ ] MI >= 80
- [ ] Pylint Score >= 9.0
- [ ] Sin wildcard imports
- [ ] Todas las factories con docstrings

---

*Documento generado: 2025-12-07*
