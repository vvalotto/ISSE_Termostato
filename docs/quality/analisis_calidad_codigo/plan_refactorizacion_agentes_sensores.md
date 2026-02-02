# PLAN DE REFACTORIZACION: agentes_sensores

**Proyecto**: ISSE_Termostato
**Paquete**: agentes_sensores
**Fecha**: 2025-12-07
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| proxy_bateria.py | 53 | 40 | 2 | 2 |
| proxy_sensor_temperatura.py | 51 | 38 | 2 | 2 |
| proxy_selector_temperatura.py | 118 | 85 | 2 | 6 |
| proxy_seteo_temperatura.py | 86 | 62 | 2 | 5 |
| **TOTAL** | **304** | **211** | **8** | **15** |

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 3.50 (A) | <= 5 | ✅ Bueno |
| CC Maximo | 8 (B) | <= 10 | ⚠️ Aceptable |
| MI Promedio | 76.94 (A) | >= 65 | ✅ Bueno |
| Pylint Score | 6.57/10 | >= 8.0 | ❌ Necesita mejora |

### 1.3 Distribucion de Issues Pylint (54 issues)

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Error (E) | 2 | E0702 raising-bad-type |
| Warning (W) | 16 | W0401 wildcard-import, W0614 unused-wildcard-import, W0718 broad-exception |
| Convention (C) | 18 | C0115 missing-class-docstring, C0209 consider-using-f-string, C0415 import-outside-toplevel |
| Refactor (R) | 10 | R0903 too-few-public-methods, R0801 duplicate-code, R1732 consider-using-with |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Wildcard Imports (W0401) - 5 ocurrencias

**Archivos afectados**: Todos

```python
# proxy_bateria.py
from entidades.abs_bateria import *

# proxy_sensor_temperatura.py
from entidades.abs_sensor_temperatura import *

# proxy_selector_temperatura.py
from registrador.registrador import *
from servicios_aplicacion.abs_selector_temperatura import *

# proxy_seteo_temperatura.py
from servicios_aplicacion.abs_seteo_temperatura import *
```

### 2.2 Missing Class Docstrings (C0115) - 8 clases

| Archivo | Clases sin docstring |
|---------|---------------------|
| proxy_bateria.py | ProxyBateriaArchivo, ProxyBateriaSocket |
| proxy_sensor_temperatura.py | ProxySensorTemperaturaArchivo, ProxySensorTemperaturaSocket |
| proxy_selector_temperatura.py | SelectorTemperaturaArchivo, SelectorTemperaturaSocket |
| proxy_seteo_temperatura.py | SeteoTemperatura, SeteoTemperaturaSocket |

### 2.3 Raising Bad Type (E0702) - CRITICO

**Archivo**: proxy_selector_temperatura.py

```python
# ACTUAL - Error: raise de string
except IOError:
    mensaje_error = "Error al leer el tipo de temperatura"
    ...
    raise mensaje_error  # E0702: Raising str

# ACTUAL - Error: raise de string concatenado
except IOError:
    raise "Error al escribir el archivo de errores: " + str(IOError.errno)
```

### 2.4 Open sin Context Manager (R1732) - 4 ocurrencias

```python
# ACTUAL - Sin with
archivo = open("bateria", "r")
carga = float(archivo.read())
archivo.close()

# MEJOR - Con with
with open("bateria", "r", encoding="utf-8") as archivo:
    carga = float(archivo.read())
```

### 2.5 Import Outside Toplevel (C0415) - 4 ocurrencias

```python
# ACTUAL - Import dentro de metodo
def leer_carga(self):
    from configurador.configurador import Configurador
    ...
```

**Nota**: Estos imports internos son intencionales para evitar imports circulares. Se mantendran pero se documentaran.

### 2.6 Codigo Duplicado (R0801)

**Entre**: proxy_bateria.py y proxy_sensor_temperatura.py

```python
# Codigo duplicado en ambos archivos (lineas 33-44 y 45-51)
direccion_servidor = (host, puerto)
servidor.bind(direccion_servidor)
servidor.listen(1)
conexion, direccion_cliente = servidor.accept()
try:
    while True:
        datos = conexion.recv(4096)
        if not datos:
            break
        ...
except ConnectionError as e:
    print("Error de conexion: {}".format(e))
finally:
    conexion.close()
    servidor.close()
```

**Solucion**: Extraer clase base `ProxySocketBase` con logica comun.

### 2.7 Broad Exception (W0718) - 2 ocurrencias

```python
# ACTUAL - Captura muy amplia
except Exception as e:
    print("[Selector] Error: {}".format(e))

# MEJOR - Excepciones especificas
except (socket.error, socket.timeout, ConnectionError) as e:
    print("[Selector] Error: {}".format(e))
```

### 2.8 Wrong Import Order (C0411)

**Archivo**: proxy_selector_temperatura.py

```python
# ACTUAL - Orden incorrecto
from registrador.registrador import *
from servicios_aplicacion.abs_selector_temperatura import *
import datetime
import socket

# CORRECTO - Orden PEP8
import datetime
import socket
from registrador.registrador import AbsRegistrador
from servicios_aplicacion.abs_selector_temperatura import AbsSelectorTemperatura
```

### 2.9 Arguments Differ (W0221) - 2 ocurrencias

Las clases Socket tienen `self` como parametro mientras las interfaces abstractas usan `@staticmethod`.

```python
# Interface abstracta
@staticmethod
@abstractmethod
def obtener_selector():
    pass

# Implementacion - Viola el contrato
def obtener_selector(self):  # W0221: arguments-differ
    ...
```

**Solucion**: Las interfaces abstractas deberian usar metodos de instancia, no estaticos.

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios por Fase

| Fase | Descripcion | Archivos | Prioridad |
|------|-------------|----------|-----------|
| 1 | Reemplazar wildcard imports | 4 | ALTA |
| 2 | Corregir errores criticos (E0702) | 1 | ALTA |
| 3 | Agregar docstrings de clase | 4 | ALTA |
| 4 | Usar context managers (with) | 3 | MEDIA |
| 5 | Corregir broad exceptions | 2 | MEDIA |
| 6 | Agregar encoding a open() | 3 | MEDIA |
| 7 | Corregir orden de imports | 1 | BAJA |
| 8 | Agregar pylint disables justificados | 4 | BAJA |
| 9 | Extraer clase base ProxySocketBase (opcional) | 3 | BAJA |

---

### 3.2 Fase 1: Imports Explicitos

#### proxy_bateria.py
```python
# ANTES
from entidades.abs_bateria import *

# DESPUES
from entidades.abs_bateria import AbsProxyBateria
```

#### proxy_sensor_temperatura.py
```python
# ANTES
from entidades.abs_sensor_temperatura import *

# DESPUES
from entidades.abs_sensor_temperatura import AbsProxySensorTemperatura
```

#### proxy_selector_temperatura.py
```python
# ANTES
from registrador.registrador import *
from servicios_aplicacion.abs_selector_temperatura import *

# DESPUES
from registrador.registrador import AbsRegistrador
from servicios_aplicacion.abs_selector_temperatura import AbsSelectorTemperatura
```

#### proxy_seteo_temperatura.py
```python
# ANTES
from servicios_aplicacion.abs_seteo_temperatura import *

# DESPUES
from servicios_aplicacion.abs_seteo_temperatura import AbsSeteoTemperatura
```

---

### 3.3 Fase 2: Corregir Errores Criticos

#### proxy_selector_temperatura.py - Raising Bad Type

```python
# ANTES - Error
except IOError:
    mensaje_error = "Error al leer el tipo de temperatura"
    ...
    raise mensaje_error

# DESPUES - Correcto
except IOError as exc:
    mensaje_error = "Error al leer el tipo de temperatura"
    ...
    raise IOError(mensaje_error) from exc
```

```python
# ANTES - Error
except IOError:
    raise "Error al escribir el archivo de errores: " + str(IOError.errno)

# DESPUES - Correcto
except IOError as exc:
    raise IOError("Error al escribir el archivo de errores") from exc
```

---

### 3.4 Fase 3: Docstrings de Clase

Agregar docstrings a todas las clases siguiendo el formato:

```python
class ProxyBateriaArchivo(AbsProxyBateria):
    """
    Proxy para lectura de bateria desde archivo.

    Implementa la interfaz AbsProxyBateria leyendo el nivel de carga
    desde un archivo local llamado 'bateria'.

    Patron de Diseno:
        - Proxy: Representa el sensor de bateria real
    """
```

```python
class ProxyBateriaSocket(AbsProxyBateria):
    """
    Proxy para lectura de bateria via socket TCP.

    Implementa la interfaz AbsProxyBateria escuchando conexiones
    TCP para recibir el nivel de carga de un cliente remoto.

    Patron de Diseno:
        - Proxy: Representa el sensor de bateria remoto
    """
```

---

### 3.5 Fase 4: Context Managers

#### proxy_bateria.py
```python
# ANTES
archivo = open("bateria", "r")
carga = float(archivo.read())
archivo.close()

# DESPUES
with open("bateria", "r", encoding="utf-8") as archivo:
    carga = float(archivo.read())
```

#### proxy_sensor_temperatura.py
```python
# ANTES
archivo = open("temperatura", "r")
temperatura = int(archivo.read())
archivo.close()

# DESPUES
with open("temperatura", "r", encoding="utf-8") as archivo:
    temperatura = int(archivo.read())
```

#### proxy_selector_temperatura.py
```python
# ANTES
archivo = open("tipo_temperatura", "r")
tipo_temperatura = str(archivo.read()).strip()
archivo.close()

# DESPUES
with open("tipo_temperatura", "r", encoding="utf-8") as archivo:
    tipo_temperatura = archivo.read().strip()
```

---

### 3.6 Fase 5: Excepciones Especificas

#### proxy_selector_temperatura.py
```python
# ANTES
except Exception as e:
    print("[Selector] Error: {}".format(e))

# DESPUES
except (socket.error, socket.timeout, ConnectionError, OSError) as e:
    print("[Selector] Error: {}".format(e))
```

#### proxy_seteo_temperatura.py
```python
# ANTES
except Exception as e:
    print("[Seteo] Error: {}".format(e))

# DESPUES
except (socket.error, socket.timeout, ConnectionError, OSError) as e:
    print("[Seteo] Error: {}".format(e))
```

---

### 3.7 Fase 6: Agregar Pylint Disables Justificados

```python
# Para clases con un solo metodo publico (es correcto para proxies)
# pylint: disable=too-few-public-methods
class ProxyBateriaArchivo(AbsProxyBateria):
    ...

# Para imports dentro de metodos (evita imports circulares)
def leer_carga(self):
    # pylint: disable=import-outside-toplevel
    from configurador.configurador import Configurador
    ...
```

---

## 4. ORDEN DE EJECUCION

### Fase 1: Imports Explicitos
1. [ ] Actualizar proxy_bateria.py
2. [ ] Actualizar proxy_sensor_temperatura.py
3. [ ] Actualizar proxy_selector_temperatura.py
4. [ ] Actualizar proxy_seteo_temperatura.py
5. [ ] Verificar que tests pasan

### Fase 2: Errores Criticos
6. [ ] Corregir raise de string en proxy_selector_temperatura.py (linea 29)
7. [ ] Corregir raise de string en proxy_selector_temperatura.py (linea 50)
8. [ ] Verificar que tests pasan

### Fase 3: Docstrings
9. [ ] Agregar docstrings a proxy_bateria.py (2 clases)
10. [ ] Agregar docstrings a proxy_sensor_temperatura.py (2 clases)
11. [ ] Agregar docstrings a proxy_selector_temperatura.py (2 clases)
12. [ ] Agregar docstrings a proxy_seteo_temperatura.py (2 clases)
13. [ ] Verificar que tests pasan

### Fase 4: Context Managers
14. [ ] Actualizar proxy_bateria.py - usar with
15. [ ] Actualizar proxy_sensor_temperatura.py - usar with
16. [ ] Actualizar proxy_selector_temperatura.py - usar with (2 lugares)
17. [ ] Verificar que tests pasan

### Fase 5: Excepciones Especificas
18. [ ] Actualizar proxy_selector_temperatura.py
19. [ ] Actualizar proxy_seteo_temperatura.py
20. [ ] Verificar que tests pasan

### Fase 6: Orden de Imports
21. [ ] Corregir orden en proxy_selector_temperatura.py
22. [ ] Verificar que tests pasan

### Fase 7: Pylint Disables
23. [ ] Agregar disables justificados a todos los archivos
24. [ ] Verificar Pylint score final

### Fase 8 (Opcional): Extraer Clase Base
25. [ ] Crear ProxySocketBase con logica comun de sockets
26. [ ] Refactorizar ProxyBateriaSocket
27. [ ] Refactorizar ProxySensorTemperaturaSocket
28. [ ] Verificar que tests pasan

---

## 5. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 3.50 | <= 4 (mantener) |
| MI Promedio | 76.94 | >= 75 (mantener) |
| Pylint Score | 6.57 | >= 9.0 |
| Wildcard Imports | 5 | 0 |
| Docstrings Clases | 0% | 100% |
| Errores (E) | 2 | 0 |

---

## 6. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Cambio de excepciones rompe flujo | Media | Medio | Verificar manejo en llamadores |
| Imports circulares | Baja | Alto | Mantener imports internos documentados |
| Codigo duplicado persiste | Baja | Bajo | Fase 8 opcional para extraer base |

---

## 7. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 4
- [ ] MI >= 75
- [ ] Pylint Score >= 9.0
- [ ] Sin wildcard imports
- [ ] Todas las clases con docstrings
- [ ] Sin errores E0702 (raising-bad-type)

---

## 8. NOTAS ADICIONALES

### 8.1 Imports Dentro de Metodos
Los imports de `Configurador` dentro de los metodos `leer_*` son intencionales
para evitar imports circulares entre paquetes. Se documentaran con comentarios
pylint disable.

### 8.2 Too Few Public Methods
Las clases Proxy tienen un solo metodo publico por diseno (patron Proxy).
Esto es correcto y se documentara con pylint disable.

### 8.3 Arguments Differ (W0221)
Este warning indica que las implementaciones Socket usan `self` mientras
las interfaces abstractas usan `@staticmethod`. La solucion correcta seria
modificar las interfaces abstractas, pero eso esta fuera del alcance de
este paquete. Se documentara con pylint disable.

### 8.4 Codigo Duplicado
La extraccion de clase base `ProxySocketBase` se deja como fase opcional (8)
porque requiere mayor refactorizacion y testing adicional.

---

*Documento generado: 2025-12-07*
