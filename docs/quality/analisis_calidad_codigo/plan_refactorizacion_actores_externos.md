# PLAN DE REFACTORIZACION: actores_externos

**Proyecto**: ISSE_Termostato
**Paquete**: actores_externos
**Fecha**: 2025-12-08
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | Tipo | LOC | Descripcion |
|---------|------|-----|-------------|
| simulador_bateria.py | Script | 87 | Simula sensor de bateria via socket |
| simulador_temperatura.py | Script | 87 | Simula sensor de temperatura via socket |
| simulador_selector_temperatura.py | Script | 104 | Simula selector de modo temperatura |
| simulador_seteo_temperatura_deseada.py | Script | 101 | Simula seteo de temperatura deseada |
| cartel_bateria.py | Script | 34 | Display de tension de bateria |
| cartel_temperatura.py | Script | 33 | Display de temperatura |
| cartel_climatizador.py | Script | 36 | Display de estado climatizador |
| **TOTAL** | **7 scripts** | **~482** | **Simuladores y displays** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| MI Promedio | 71.65 (A) | >= 65 | ✅ Bueno |
| MI Minimo | 59.65 | >= 50 | ✅ Aceptable |
| Pylint Score | 7.80/10 | >= 8.0 | ⚠️ Casi objetivo |

**Detalle MI por archivo**:
| Archivo | MI Score | Rank |
|---------|----------|------|
| cartel_bateria.py | 85.96 | A |
| cartel_climatizador.py | 85.96 | A |
| cartel_temperatura.py | 85.96 | A |
| simulador_bateria.py | 61.75 | A |
| simulador_temperatura.py | 61.78 | A |
| simulador_selector_temperatura.py | 60.50 | A |
| simulador_seteo_temperatura_deseada.py | 59.65 | A |

### 1.3 Distribucion de Issues Pylint

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Convention (C) | 43 | C0114 missing-module-docstring (7), C0103 invalid-name (34), C0413 wrong-import-position (2) |
| Warning (W) | 8 | W0105 pointless-string-statement (4), W1514 unspecified-encoding (4) |
| Refactor (R) | 14 | R0801 duplicate-code (14 bloques similares) |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Missing Module Docstrings (C0114) - 7 archivos - ALTA PRIORIDAD

**Todos los archivos** carecen de docstring de modulo.

```python
# ACTUAL - simulador_bateria.py
import socket
import time
...

"""
Simula la bateria fisica, mediante socket
"""  # <-- Docstring mal ubicado (despues de imports)

# CORRECTO
"""
Simulador de bateria fisica via socket TCP.

Este script simula un sensor de bateria que envia
lecturas de voltaje al termostato via socket.
"""
import socket
import time
...
```

### 2.2 Pointless String Statement (W0105) - 4 archivos - ALTA PRIORIDAD

**Archivos afectados**: simulador_bateria.py, simulador_temperatura.py, simulador_selector_temperatura.py, simulador_seteo_temperatura_deseada.py

```python
# ACTUAL - String que no hace nada (linea 8)
"""
Simula la bateria fisica, mediante socket
"""

# SOLUCION: Mover al inicio del archivo como docstring de modulo
```

### 2.3 Unspecified Encoding (W1514) - 4 archivos - ALTA PRIORIDAD

**Archivos afectados**: Todos los simuladores

```python
# ACTUAL - Sin encoding
with open(config_file, "r") as f:
    config = json.load(f)

# CORRECTO - Con encoding
with open(config_file, "r", encoding="utf-8") as f:
    config = json.load(f)
```

### 2.4 Invalid Names (C0103) - 34 ocurrencias - MEDIA PRIORIDAD

Variables en minusculas dentro de scripts tratadas como constantes por pylint.

**Archivos afectados**: Todos los simuladores

```python
# ACTUAL - pylint espera UPPER_CASE para variables de modulo
config_file = "simuladores_config.json"
contador = 0
conectado = False

# OPCIONES:
# 1. Renombrar a UPPER_CASE (CONFIG_FILE, CONTADOR, CONECTADO)
# 2. Agregar pylint disable al inicio del archivo
```

**Recomendacion**: Agregar `# pylint: disable=invalid-name` al inicio de los scripts, ya que son variables mutables de script, no constantes.

### 2.5 Broad Exception Caught (W0718) - 4 archivos

**Archivos afectados**: Todos los simuladores

```python
# ACTUAL - Captura muy amplia
except Exception as e:
    conectado = False
    print(f"\n✗ Error inesperado: {e}")

# MEJORADO - Excepciones especificas
except (OSError, socket.error) as e:
    conectado = False
    print(f"\n✗ Error inesperado: {e}")
```

### 2.6 Codigo Duplicado (R0801) - 14 bloques - BAJA PRIORIDAD

Hay mucho codigo repetido entre los simuladores:
- Carga de configuracion (8 lineas identicas)
- Interfaz de usuario (prints similares)
- Manejo de conexion socket (10 lineas similares)
- Historial de acciones (6 lineas similares)

**Recomendacion**: Aceptar el codigo duplicado para esta refactorizacion. Una refactorizacion mayor crearia una clase base `SimuladorBase`, pero eso excede el alcance actual.

### 2.7 Wrong Import Position (C0413) - 2 archivos

```python
# ACTUAL - Import despues de codigo
from os import system  # <-- Despues del "docstring" mal ubicado

# CORRECTO - Imports al inicio
from os import system
```

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios por Fase

| Fase | Descripcion | Archivos | Prioridad |
|------|-------------|----------|-----------|
| 1 | Mover docstrings al inicio (C0114, W0105) | 4 | ALTA |
| 2 | Agregar docstrings a carteles | 3 | ALTA |
| 3 | Agregar encoding a open() (W1514) | 4 | ALTA |
| 4 | Agregar pylint disable para invalid-name | 4 | MEDIA |
| 5 | Especificar excepciones (W0718) | 4 | MEDIA |
| 6 | Agregar pylint disable para duplicate-code | 1 | BAJA |

---

### 3.2 Fase 1: Mover Docstrings al Inicio (Simuladores)

#### simulador_bateria.py
```python
# ANTES (lineas 1-10)
import socket
import time
import json
import os
from datetime import datetime
from os import system

"""
Simula la bateria fisica, mediante socket
"""

# DESPUES
"""
Simulador de sensor de bateria via socket TCP.

Este script simula un sensor de bateria que envia lecturas
de voltaje (0-5V) al termostato a traves de conexion socket.
Se conecta al puerto configurado y permite ingresar valores
manualmente para pruebas del sistema.
"""
import socket
import time
import json
import os
from datetime import datetime
from os import system
```

#### simulador_temperatura.py
```python
"""
Simulador de sensor de temperatura via socket TCP.

Este script simula un sensor de temperatura que envia lecturas
en grados Celsius al termostato a traves de conexion socket.
"""
import socket
...
```

#### simulador_selector_temperatura.py
```python
"""
Simulador de selector de modo de temperatura via socket TCP.

Este script simula el boton selector que alterna entre mostrar
la temperatura ambiente o la temperatura deseada en el display.
"""
import socket
...
```

#### simulador_seteo_temperatura_deseada.py
```python
"""
Simulador de control de temperatura deseada via socket TCP.

Este script simula los botones de ajuste de temperatura deseada,
permitiendo enviar comandos de aumentar o disminuir al termostato.
"""
import socket
...
```

---

### 3.3 Fase 2: Agregar Docstrings a Carteles

#### cartel_bateria.py
```python
"""
Display de tension de bateria via socket TCP.

Este script actua como servidor socket que recibe y muestra
en consola las lecturas de tension de bateria enviadas
por el termostato.
"""
import socket
import time
from os import system
...
```

#### cartel_temperatura.py
```python
"""
Display de temperatura via socket TCP.

Este script actua como servidor socket que recibe y muestra
en consola las lecturas de temperatura enviadas por el termostato.
"""
import socket
...
```

#### cartel_climatizador.py
```python
"""
Display de estado del climatizador via socket TCP.

Este script actua como servidor socket que recibe y muestra
en consola el estado actual del climatizador (calentando,
enfriando, apagado).
"""
import socket
...
```

---

### 3.4 Fase 3: Agregar Encoding

Aplicar a todos los simuladores:

```python
# ANTES
with open(config_file, "r") as f:
    config = json.load(f)

# DESPUES
with open(config_file, "r", encoding="utf-8") as f:
    config = json.load(f)
```

**Archivos**: simulador_bateria.py, simulador_temperatura.py, simulador_selector_temperatura.py, simulador_seteo_temperatura_deseada.py

---

### 3.5 Fase 4: Pylint Disable para Invalid-Name

Agregar al inicio de cada simulador (despues del docstring):

```python
"""
Simulador de sensor de bateria via socket TCP.
...
"""
# pylint: disable=invalid-name
# Las variables de script (contador, conectado, etc.) son mutables,
# no constantes, por lo que no requieren UPPER_CASE.

import socket
...
```

**Archivos**: Todos los simuladores (4)

---

### 3.6 Fase 5: Especificar Excepciones

```python
# ANTES
except Exception as e:
    conectado = False
    print(f"\n✗ Error inesperado: {e}")

# DESPUES
except (OSError, socket.error) as e:
    conectado = False
    print(f"\n✗ Error de conexion: {e}")
```

**Archivos**: simulador_bateria.py, simulador_temperatura.py, simulador_selector_temperatura.py, simulador_seteo_temperatura_deseada.py

---

### 3.7 Fase 6: Disable para Duplicate-Code

Agregar en `simuladores_config.json` (archivo de configuracion compartido) o crear `__init__.py`:

```python
# actores_externos/__init__.py
"""
Paquete de actores externos del termostato.

Contiene simuladores de sensores y displays para pruebas
del sistema de termostato.

Note:
    Los simuladores comparten codigo comun (carga de config,
    interfaz de usuario, manejo de socket). Esto es aceptable
    ya que son scripts independientes de prueba.
"""
# pylint: disable=duplicate-code
```

**Alternativa**: No crear __init__.py y aceptar los warnings R0801.

---

## 4. ORDEN DE EJECUCION

### Fase 1: Docstrings Simuladores
1. [ ] Mover docstring en simulador_bateria.py
2. [ ] Mover docstring en simulador_temperatura.py
3. [ ] Mover docstring en simulador_selector_temperatura.py
4. [ ] Mover docstring en simulador_seteo_temperatura_deseada.py

### Fase 2: Docstrings Carteles
5. [ ] Agregar docstring a cartel_bateria.py
6. [ ] Agregar docstring a cartel_temperatura.py
7. [ ] Agregar docstring a cartel_climatizador.py

### Fase 3: Encoding
8. [ ] Agregar encoding en simulador_bateria.py
9. [ ] Agregar encoding en simulador_temperatura.py
10. [ ] Agregar encoding en simulador_selector_temperatura.py
11. [ ] Agregar encoding en simulador_seteo_temperatura_deseada.py

### Fase 4: Invalid-Name Disable
12. [ ] Agregar disable en simulador_bateria.py
13. [ ] Agregar disable en simulador_temperatura.py
14. [ ] Agregar disable en simulador_selector_temperatura.py
15. [ ] Agregar disable en simulador_seteo_temperatura_deseada.py

### Fase 5: Excepciones Especificas
16. [ ] Cambiar Exception por (OSError, socket.error) en simulador_bateria.py
17. [ ] Cambiar Exception por (OSError, socket.error) en simulador_temperatura.py
18. [ ] Cambiar Exception por (OSError, socket.error) en simulador_selector_temperatura.py
19. [ ] Cambiar Exception por (OSError, socket.error) en simulador_seteo_temperatura_deseada.py

### Fase 6: Opcional
20. [ ] Crear __init__.py con disable para duplicate-code (opcional)

---

## 5. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| MI Promedio | 71.65 | >= 70 (mantener) |
| Pylint Score | 7.80 | >= 9.0 |
| Missing Docstrings (C0114) | 7 | 0 |
| Pointless Strings (W0105) | 4 | 0 |
| Unspecified Encoding (W1514) | 4 | 0 |
| Broad Exception (W0718) | 4 | 0 |

---

## 6. NOTAS ADICIONALES

### 6.1 Codigo Duplicado (R0801)
Los 14 bloques de codigo duplicado entre simuladores son aceptables porque:
- Son scripts independientes de prueba, no codigo de produccion
- Extraer una clase base `SimuladorBase` agregaria complejidad innecesaria
- Cada simulador debe poder ejecutarse de forma aislada

### 6.2 Invalid-Name (C0103)
Las variables `contador`, `conectado`, `config_file`, etc. son variables mutables de script, no constantes. Usar `# pylint: disable=invalid-name` es la solucion apropiada.

### 6.3 Carteles vs Simuladores
- **Carteles**: Servidores socket que reciben datos (displays)
- **Simuladores**: Clientes socket que envian datos (sensores simulados)

### 6.4 Sin Tests
Este paquete no tiene tests unitarios ya que son scripts de prueba/simulacion. La verificacion sera manual.

---

*Documento generado: 2025-12-08*
*Herramientas utilizadas: radon (MI), pylint*
