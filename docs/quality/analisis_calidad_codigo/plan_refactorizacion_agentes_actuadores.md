# PLAN DE REFACTORIZACION: agentes_actuadores

**Proyecto**: ISSE_Termostato
**Paquete**: agentes_actuadores
**Fecha**: 2025-12-08
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| actuador_climatizador.py | 66 | 51 | 1 | 4 |
| visualizador_bateria.py | 71 | 50 | 3 | 6 |
| visualizador_climatizador.py | 42 | 28 | 3 | 3 |
| visualizador_temperatura.py | 72 | 54 | 3 | 6 |
| **TOTAL** | **251** | **183** | **10** | **19** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 2.03 (A) | <= 5 | ✅ Excelente |
| CC Maximo | 3 (A) | <= 10 | ✅ Excelente |
| MI Promedio | 82.92 (A) | >= 65 | ✅ Muy Bueno |
| Pylint Score | 0.00/10 | >= 8.0 | ❌ Critico |

**Detalle MI por archivo**:
| Archivo | MI Score | Rank |
|---------|----------|------|
| visualizador_climatizador.py | 100.00 | A |
| visualizador_bateria.py | 100.00 | A |
| visualizador_temperatura.py | 70.14 | A |
| actuador_climatizador.py | 61.54 | A |

### 1.3 Distribucion de Issues Pylint (73 issues)

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Error (E) | 20 | E0401 import-error (14), E0602 undefined-variable (4), E0702 raising-bad-type (2) |
| Warning (W) | 7 | W0401 wildcard-import (4), W1514 unspecified-encoding (3), W0707 raise-missing-from (2) |
| Convention (C) | 34 | C0115 missing-class-docstring (10), C0116 missing-function-docstring (19), C0209 consider-using-f-string (8), C0415 import-outside-toplevel (6), C0304 missing-final-newline (1), C0301 line-too-long (1) |
| Refactor (R) | 12 | R0903 too-few-public-methods (3), R1711 useless-return (4), R0801 duplicate-code (1) |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Wildcard Imports (W0401) - 4 ocurrencias - ALTA PRIORIDAD

**Archivos afectados**: Todos

```python
# actuador_climatizador.py
from registrador.registrador import *

# visualizador_bateria.py
from entidades.abs_visualizador_bateria import *

# visualizador_climatizador.py
from entidades.abs_visualizador_climatizador import *

# visualizador_temperatura.py
from entidades.abs_visualizador_temperatura import *
```

**Causa de E0602**: Los wildcard imports causan que pylint no pueda resolver las variables importadas (AbsVisualizadorBateria, AbsVisualizadorClimatizador, etc.)

### 2.2 Raising Bad Type (E0702) - 2 ocurrencias - CRITICO

**Archivo**: actuador_climatizador.py (lineas 49 y 65)

```python
# ACTUAL - Error: raise de string
except IOError:
    raise "Error al escribir el archivo de errores: " + str(IOError.errno)

except IOError:
    raise "Error al escribir el archivo de auditoria: " + str(IOError.errno)
```

### 2.3 Missing Class Docstrings (C0115) - 10 clases

| Archivo | Clases sin docstring |
|---------|---------------------|
| actuador_climatizador.py | ActuadorClimatizadorGeneral |
| visualizador_bateria.py | VisualizadorBateria, VisualizadorBateriaSocket, VisualizadorBateriaApi |
| visualizador_climatizador.py | VisualizadorClimatizador, VisualizadorClimatizadorSocket, VisualizadorClimatizadorApi |
| visualizador_temperatura.py | VisualizadorTemperatura, VisualizadorTemperaturaSocket, VisualizadorTemperaturaApi |

### 2.4 Missing Function Docstrings (C0116) - 19 metodos

Todos los metodos de todas las clases carecen de docstrings.

### 2.5 Unspecified Encoding (W1514) - 3 ocurrencias

**Archivo**: actuador_climatizador.py (lineas 21, 45, 61)

```python
# ACTUAL - Sin encoding
with open("climatizador", "w") as archivo_climatizador:
with open("registro_errores", "a") as archivo_errores:
with open("registro_auditoria", "a") as archivo_auditoria:

# CORRECTO - Con encoding
with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
```

### 2.6 Useless Return (R1711) - 4 ocurrencias

**Archivos**: visualizador_bateria.py (2), visualizador_temperatura.py (2), actuador_climatizador.py (2)

```python
# ACTUAL - Return innecesario
def mostrar_tension(tension_bateria):
    print(str(tension_bateria))
    return  # <-- Innecesario

# CORRECTO - Sin return
def mostrar_tension(tension_bateria):
    print(str(tension_bateria))
```

### 2.7 Import Outside Toplevel (C0415) - 6 ocurrencias

**Archivos**: visualizador_bateria.py (2), visualizador_climatizador.py (1), visualizador_temperatura.py (2), actuador_climatizador.py (1)

```python
# ACTUAL - Import dentro de metodo
def mostrar_tension(self, tension_bateria):
    from configurador.configurador import Configurador
    ...
```

**Nota**: Estos imports internos son intencionales para evitar imports circulares. Se mantendran pero se documentaran.

### 2.8 Codigo Duplicado (R0801)

**Entre**: visualizador_bateria.py y visualizador_temperatura.py

```python
# Codigo duplicado en ambos archivos (lineas 33-41)
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    def mostrar_indicador(self, indicador_bateria):

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

**Solucion potencial**: Extraer clase base `VisualizadorSocketBase` con logica comun (fase opcional).

### 2.9 Too Few Public Methods (R0903) - 3 clases

Las clases con un solo metodo publico (patron Visualizador/Proxy). Es aceptable por diseno.

### 2.10 Close Redundante dentro de Context Manager

**Archivo**: actuador_climatizador.py (lineas 23, 47, 63)

```python
# ACTUAL - close() redundante con 'with'
with open("climatizador", "w") as archivo_climatizador:
    archivo_climatizador.write(accion)
    archivo_climatizador.close()  # <-- Innecesario

# CORRECTO - 'with' cierra automaticamente
with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
    archivo_climatizador.write(accion)
```

### 2.11 Otras Issues Menores

| Issue | Archivo | Linea | Descripcion |
|-------|---------|-------|-------------|
| C0304 | visualizador_climatizador.py | 42 | Falta newline final |
| C0301 | actuador_climatizador.py | 7 | Linea muy larga (101/100) |

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios por Fase

| Fase | Descripcion | Archivos | Prioridad |
|------|-------------|----------|-----------|
| 1 | Reemplazar wildcard imports | 4 | ALTA |
| 2 | Corregir errores criticos (E0702) | 1 | ALTA |
| 3 | Agregar encoding a open() | 1 | ALTA |
| 4 | Eliminar close() redundantes | 1 | MEDIA |
| 5 | Eliminar useless returns | 3 | MEDIA |
| 6 | Agregar docstrings de clase | 4 | MEDIA |
| 7 | Agregar docstrings de metodos | 4 | MEDIA |
| 8 | Corregir issues menores (newline, line-too-long) | 2 | BAJA |
| 9 | Agregar pylint disables justificados | 4 | BAJA |

---

### 3.2 Fase 1: Imports Explicitos

#### actuador_climatizador.py
```python
# ANTES
from registrador.registrador import *

# DESPUES
from registrador.registrador import AbsRegistrador, AbsAuditor
```

#### visualizador_bateria.py
```python
# ANTES
from entidades.abs_visualizador_bateria import *

# DESPUES
from entidades.abs_visualizador_bateria import AbsVisualizadorBateria
```

#### visualizador_climatizador.py
```python
# ANTES
from entidades.abs_visualizador_climatizador import *

# DESPUES
from entidades.abs_visualizador_climatizador import AbsVisualizadorClimatizador
```

#### visualizador_temperatura.py
```python
# ANTES
from entidades.abs_visualizador_temperatura import *

# DESPUES
from entidades.abs_visualizador_temperatura import AbsVisualizadorTemperatura
```

---

### 3.3 Fase 2: Corregir Errores Criticos

#### actuador_climatizador.py - Raising Bad Type (linea 49)

```python
# ANTES - Error
except IOError:
    raise "Error al escribir el archivo de errores: " + str(IOError.errno)

# DESPUES - Correcto
except IOError as exc:
    raise IOError("Error al escribir el archivo de errores") from exc
```

#### actuador_climatizador.py - Raising Bad Type (linea 65)

```python
# ANTES - Error
except IOError:
    raise "Error al escribir el archivo de auditoria: " + str(IOError.errno)

# DESPUES - Correcto
except IOError as exc:
    raise IOError("Error al escribir el archivo de auditoria") from exc
```

---

### 3.4 Fase 3: Agregar Encoding

#### actuador_climatizador.py

```python
# ANTES
with open("climatizador", "w") as archivo_climatizador:
with open("registro_errores", "a") as archivo_errores:
with open("registro_auditoria", "a") as archivo_auditoria:

# DESPUES
with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
with open("registro_errores", "a", encoding="utf-8") as archivo_errores:
with open("registro_auditoria", "a", encoding="utf-8") as archivo_auditoria:
```

---

### 3.5 Fase 4: Eliminar close() Redundantes

#### actuador_climatizador.py

```python
# ANTES - close() redundante
with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
    archivo_climatizador.write(accion)
    archivo_climatizador.close()

# DESPUES - Sin close()
with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
    archivo_climatizador.write(accion)
```

Aplicar en lineas 23, 47, 63.

---

### 3.6 Fase 5: Eliminar Useless Returns

#### visualizador_bateria.py, visualizador_temperatura.py, actuador_climatizador.py

```python
# ANTES
def mostrar_tension(tension_bateria):
    print(str(tension_bateria))
    return

# DESPUES
def mostrar_tension(tension_bateria):
    """Muestra la tension de la bateria en consola."""
    print(str(tension_bateria))
```

---

### 3.7 Fase 6: Docstrings de Clase

Agregar docstrings a todas las clases siguiendo el formato:

```python
class ActuadorClimatizadorGeneral(AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor):
    """
    Actuador que controla el climatizador mediante escritura en archivo.

    Implementa las interfaces AbsProxyActuadorClimatizador, AbsRegistrador
    y AbsAuditor para accionar el climatizador y registrar eventos.

    Patron de Diseno:
        - Proxy: Representa el actuador real del climatizador
        - Observer: Registra eventos de auditoria y errores
    """
```

```python
class VisualizadorBateria(AbsVisualizadorBateria):
    """
    Visualizador de bateria que imprime en consola.

    Implementa la interfaz AbsVisualizadorBateria mostrando
    la tension e indicador de bateria por salida estandar.

    Patron de Diseno:
        - Presenter: Presenta datos de bateria al usuario
    """
```

```python
class VisualizadorBateriaSocket(AbsVisualizadorBateria):
    """
    Visualizador de bateria via socket TCP.

    Implementa la interfaz AbsVisualizadorBateria enviando
    los datos a un servidor remoto via socket.

    Patron de Diseno:
        - Proxy: Envia datos a visualizador remoto
    """
```

```python
class VisualizadorBateriaApi(AbsVisualizadorBateria):
    """
    Visualizador de bateria via API REST.

    Implementa la interfaz AbsVisualizadorBateria enviando
    los datos a una API REST mediante peticiones HTTP POST.

    Patron de Diseno:
        - Adapter: Adapta la visualizacion a protocolo HTTP
    """
```

---

### 3.8 Fase 7: Docstrings de Metodos

Agregar docstrings a todos los metodos:

```python
def accionar_climatizador(self, accion):
    """
    Acciona el climatizador escribiendo la accion en archivo.

    Args:
        accion: Accion a ejecutar en el climatizador (str).

    Raises:
        IOError: Si no se puede escribir en el archivo del climatizador.
    """
```

```python
def mostrar_tension(self, tension_bateria):
    """
    Muestra la tension de la bateria.

    Args:
        tension_bateria: Valor de tension a mostrar.
    """
```

---

### 3.9 Fase 8: Issues Menores

#### visualizador_climatizador.py - Agregar newline final

Asegurar que el archivo termine con una linea en blanco.

#### actuador_climatizador.py - Linea muy larga (linea 7)

```python
# ANTES (101 caracteres)
from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador, AbsActuadorClimatizador

# DESPUES (separado en dos lineas)
from entidades.abs_actuador_climatizador import (
    AbsProxyActuadorClimatizador,
    AbsActuadorClimatizador
)
```

---

### 3.10 Fase 9: Pylint Disables Justificados

```python
# Para clases con pocos metodos publicos (es correcto para visualizadores)
# pylint: disable=too-few-public-methods
class VisualizadorClimatizador(AbsVisualizadorClimatizador):
    ...

# Para imports dentro de metodos (evita imports circulares)
def mostrar_tension(self, tension_bateria):
    # pylint: disable=import-outside-toplevel
    from configurador.configurador import Configurador
    ...
```

---

## 4. ORDEN DE EJECUCION

### Fase 1: Imports Explicitos
1. [ ] Actualizar actuador_climatizador.py
2. [ ] Actualizar visualizador_bateria.py
3. [ ] Actualizar visualizador_climatizador.py
4. [ ] Actualizar visualizador_temperatura.py
5. [ ] Verificar que tests pasan

### Fase 2: Errores Criticos
6. [ ] Corregir raise de string en actuador_climatizador.py (linea 49)
7. [ ] Corregir raise de string en actuador_climatizador.py (linea 65)
8. [ ] Verificar que tests pasan

### Fase 3: Encoding
9. [ ] Agregar encoding a open() en actuador_climatizador.py (3 lugares)
10. [ ] Verificar que tests pasan

### Fase 4: Close Redundantes
11. [ ] Eliminar close() redundantes en actuador_climatizador.py (3 lugares)
12. [ ] Verificar que tests pasan

### Fase 5: Useless Returns
13. [ ] Eliminar returns innecesarios en visualizador_bateria.py (2)
14. [ ] Eliminar returns innecesarios en visualizador_temperatura.py (2)
15. [ ] Eliminar returns innecesarios en actuador_climatizador.py (2)
16. [ ] Verificar que tests pasan

### Fase 6: Docstrings de Clase
17. [ ] Agregar docstrings a actuador_climatizador.py (1 clase)
18. [ ] Agregar docstrings a visualizador_bateria.py (3 clases)
19. [ ] Agregar docstrings a visualizador_climatizador.py (3 clases)
20. [ ] Agregar docstrings a visualizador_temperatura.py (3 clases)
21. [ ] Verificar que tests pasan

### Fase 7: Docstrings de Metodos
22. [ ] Agregar docstrings a actuador_climatizador.py (4 metodos)
23. [ ] Agregar docstrings a visualizador_bateria.py (6 metodos)
24. [ ] Agregar docstrings a visualizador_climatizador.py (3 metodos)
25. [ ] Agregar docstrings a visualizador_temperatura.py (6 metodos)
26. [ ] Verificar que tests pasan

### Fase 8: Issues Menores
27. [ ] Agregar newline final a visualizador_climatizador.py
28. [ ] Corregir linea larga en actuador_climatizador.py
29. [ ] Verificar que tests pasan

### Fase 9: Pylint Disables
30. [ ] Agregar disables justificados a todos los archivos
31. [ ] Verificar Pylint score final

---

## 5. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 2.03 | <= 3 (mantener) |
| MI Promedio | 82.92 | >= 80 (mantener) |
| Pylint Score | 0.00 | >= 9.0 |
| Wildcard Imports | 4 | 0 |
| Docstrings Clases | 0% | 100% |
| Docstrings Metodos | 0% | 100% |
| Errores (E) | 6 | 0 |
| Warnings (W) | 7 | 0 |

---

## 6. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Cambio de excepciones rompe flujo | Media | Medio | Verificar manejo en llamadores |
| Imports circulares | Baja | Alto | Mantener imports internos documentados |
| Codigo duplicado persiste | Baja | Bajo | Refactorizacion opcional de clase base |

---

## 7. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 3
- [ ] MI >= 80
- [ ] Pylint Score >= 9.0
- [ ] Sin wildcard imports
- [ ] Todas las clases con docstrings
- [ ] Todos los metodos con docstrings
- [ ] Sin errores E0702 (raising-bad-type)
- [ ] Sin errores W1514 (unspecified-encoding)

---

## 8. NOTAS ADICIONALES

### 8.1 Imports Dentro de Metodos
Los imports de `Configurador` dentro de los metodos de las clases Api son intencionales
para evitar imports circulares entre paquetes. Se documentaran con comentarios
pylint disable.

### 8.2 Too Few Public Methods
Las clases Visualizador tienen uno o dos metodos publicos por diseno (patron Presenter).
Esto es correcto y se documentara con pylint disable.

### 8.3 Codigo Duplicado (R0801)
El codigo duplicado entre visualizadores Socket es minimo y la extraccion de clase
base agregaria complejidad innecesaria. Se acepta este warning.

### 8.4 Herencia Multiple en ActuadorClimatizadorGeneral
La clase hereda de tres interfaces (AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor).
Esto cumple con el principio de Interface Segregation (ISP) de SOLID.

---

*Documento generado: 2025-12-08*
*Herramientas utilizadas: radon (CC, MI, raw), pylint*
