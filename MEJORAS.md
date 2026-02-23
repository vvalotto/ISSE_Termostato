# MEJORAS.md

Registro de propuestas de mejora identificadas durante el análisis de calidad del proyecto.

**Análisis base:** pylint 9.84/10 · radon complejidad promedio A (2.1) · todos los MI en rango A
**Fecha:** 2026-02-23

---

## Convenciones

| Impacto | Significado |
|---------|-------------|
| Alto    | Viola reglas del proyecto / afecta mantenibilidad significativamente |
| Medio   | Inconsistencia o code smell notable |
| Bajo    | Mejora menor de estilo o legibilidad |

| Esfuerzo | Significado |
|----------|-------------|
| Bajo     | < 30 min, cambio localizado |
| Medio    | 1–2 hs, afecta múltiples archivos |
| Alto     | > 2 hs, requiere refactor o migración |

| Estado   | Significado |
|----------|-------------|
| Pendiente | No iniciado |
| En curso  | Siendo trabajado |
| Resuelto  | Implementado y verificado |

---

## Hallazgos

### Código

| ID    | Descripción | Archivo(s) | Impacto | Esfuerzo | Estado |
|-------|-------------|------------|---------|----------|--------|
| C-001 | **f-strings en configurador** — `cargar_configuracion()` y `_validar_configuracion()` usan f-strings (líneas 71, 79, 233) en violación directa de la regla de Python 3.5+ | `configurador/configurador.py` | Alto | Bajo | Pendiente |
| C-002 | **Wildcard imports en ejecutar.py** — `from servicios_aplicacion.lanzador import *` y `from configurador.configurador import *` importan decenas de símbolos innecesarios; solo se usan `Configurador` y `Lanzador` | `ejecutar.py` | Medio | Bajo | Pendiente |
| C-003 | **`print()` para advertencias en `_validar_configuracion`** — usa `print()` en lugar de `logging.warning()`, inconsistente con el resto del sistema | `configurador/configurador.py:238-246` | Medio | Bajo | Pendiente |
| C-004 | **`pass` innecesario** — `VisualizadorBateriaApi.mostrar_indicador()` contiene un `pass` que silencia comportamiento sin explicación | `agentes_actuadores/visualizador_bateria.py:142` | Bajo | Bajo | Pendiente |
| C-005 | **`__del__` para cierre de sockets** — `SeteoTemperaturaSocket.__del__` y `SelectorTemperaturaSocket.__del__` usan `__del__` para liberar recursos; no garantiza ejecución determinista. Preferir context manager (`__enter__`/`__exit__`) | `agentes_sensores/proxy_seteo_temperatura.py:118` `agentes_sensores/proxy_selector_temperatura.py:156` | Medio | Medio | Pendiente |
| C-006 | **Newline final faltante** — `ejecutar.py` no termina con newline | `ejecutar.py:25` | Bajo | Bajo | Pendiente |

---

### Diseño

| ID    | Descripción | Archivo(s) | Impacto | Esfuerzo | Estado |
|-------|-------------|------------|---------|----------|--------|
| D-001 | **Singleton implícito e incoherente en `Configurador`** — `configuracion_termostato` es un atributo de clase usado como estado global. El código lo instancia (`Configurador().cargar_configuracion()`) pero luego accede como clase (`Configurador.configuracion_termostato`). Si es Singleton, debería serlo explícitamente o eliminarse la instanciación innecesaria | `configurador/configurador.py` | Alto | Medio | Pendiente |
| D-002 | **Clase con un solo método estático** — `ControladorTemperatura` no tiene estado y expone un único `@staticmethod`. En Python idiomático es más natural como función de módulo. Como clase aporta overhead sin beneficio real | `servicios_dominio/controlador_climatizador.py` | Medio | Bajo | Pendiente |
| D-003 | **`AbsClimatizador` y sus concretas en el mismo archivo** — El proyecto separa las interfaces abstractas en `abs_*.py` (ej: `abs_bateria.py`, `abs_sensor_temperatura.py`), pero `AbsClimatizador`, `Climatizador` y `Calefactor` conviven en `climatizador.py`. Inconsistencia estructural | `entidades/climatizador.py` | Medio | Bajo | Pendiente |
| D-004 | **Inconsistencia en ciclo de vida de sockets** — `ProxyBateriaSocket` y `ProxySensorTemperaturaSocket` crean y destruyen el socket TCP en cada llamada a `leer_*()`. `SeteoTemperaturaSocket` y `SelectorTemperaturaSocket` mantienen conexión persistente. Sin justificación documentada para esta diferencia de diseño | `agentes_sensores/proxy_bateria.py` `agentes_sensores/proxy_sensor_temperatura.py` `agentes_sensores/proxy_seteo_temperatura.py` | Medio | Medio | Pendiente |
| D-005 | **Discriminación por string sin constantes** — `GestorAmbiente.mostrar_temperatura()` usa los literals `"ambiente"` y `"deseada"` como discriminador. Un typo no produce error en tiempo de ejecución. Candidato a constantes de módulo o enum | `gestores_entidades/gestor_ambiente.py:128` `entidades/ambiente.py` | Medio | Bajo | Pendiente |

---

### Arquitectura

| ID    | Descripción | Archivo(s) | Impacto | Esfuerzo | Estado |
|-------|-------------|------------|---------|----------|--------|
| A-001 | **Interfaces de entrada en capa incorrecta** — `AbsSeteoTemperatura` y `AbsSelectorTemperatura` están definidas en `servicios_aplicacion/`. Las interfaces que las capas internas implementan deben vivir en `entidades/`, igual que `AbsProxyBateria`, `AbsProxySensorTemperatura`, etc. | `servicios_aplicacion/abs_seteo_temperatura.py` `servicios_aplicacion/abs_selector_temperatura.py` | Alto | Medio | Pendiente |
| A-002 | **`agentes_sensores` depende de `servicios_aplicacion`** — Como consecuencia directa de A-001, `proxy_seteo_temperatura.py` y `proxy_selector_temperatura.py` importan desde `servicios_aplicacion/`. Las capas de Interface Adapters solo deben depender de `entidades/` (hacia adentro) | `agentes_sensores/proxy_seteo_temperatura.py:13` `agentes_sensores/proxy_selector_temperatura.py:~13` | Alto | Medio | Pendiente |

---

### Tests

| ID    | Descripción | Archivo(s) | Impacto | Esfuerzo | Estado |
|-------|-------------|------------|---------|----------|--------|
| T-001 | **Dos estructuras de tests paralelas** — Existen tests en la raíz de `Test/` (estructura vieja: `test_bateria_desde_archivo.py`, `test_climatizador.py`, etc.) y en `Test/unit/` + `Test/integration/` (estructura nueva). Los tests viejos deberían migrarse o eliminarse para evitar ambigüedad | `Test/*.py` (raíz) | Medio | Medio | Pendiente |
| T-002 | **`Test/hal/test_hal_adc.py` sin implementación correspondiente** — Existe un test de HAL (Hardware Abstraction Layer) pero no hay módulo `hal/` en el código de producción | `Test/hal/test_hal_adc.py` | Bajo | Bajo | Pendiente |

### Principios SOLID (nuevos hallazgos — revisión de docs/Analisis_Violaciones_*.md)

> Los documentos en `docs/` fueron generados en Noviembre 2025 sobre una versión anterior del código.
> Cada hallazgo fue verificado contra el código actual antes de incluirlo.

| ID    | Principio | Descripción | Archivo(s) | Impacto | Esfuerzo | Estado |
|-------|-----------|-------------|------------|---------|----------|--------|
| S-001 | ISP + SRP | **`ActuadorClimatizadorGeneral` hereda de 3 interfaces** — La clase implementa `AbsProxyActuadorClimatizador` + `AbsRegistrador` + `AbsAuditor`. El logging y la auditoría son cross-cutting concerns que no deberían imponerse como interfaces a implementar: hay que inyectarlos como dependencias. | `agentes_actuadores/actuador_climatizador.py:11` | Alto | Medio | Pendiente |
| S-002 | ISP       | **`SelectorTemperaturaArchivo` hereda `AbsRegistrador`** — La clase de selección implementa también la interfaz de registro de errores. El concern de logging es ortogonal a la responsabilidad del selector; debería inyectarse. `SelectorTemperaturaSocket` (misma familia) no hereda `AbsRegistrador`, evidenciando la inconsistencia. | `agentes_sensores/proxy_selector_temperatura.py:25` | Medio | Bajo | Pendiente |
| S-003 | LSP       | **`SelectorTemperaturaArchivo.obtener_selector()` usa `@staticmethod`** — Dentro de la misma familia, `SelectorTemperaturaArchivo` implementa el método como estático (sin estado) y `SelectorTemperaturaSocket` lo implementa como método de instancia (con estado). La interfaz abstracta (`AbsSelectorTemperatura`) debería reflejar el contrato correcto de instancia. | `agentes_sensores/proxy_selector_temperatura.py:33` | Medio | Bajo | Pendiente |
| S-004 | OCP       | **Puertos hardcodeados en visualizadores socket** — `VisualizadorBateriaSocket`, `VisualizadorTemperaturaSocket` y `VisualizadorClimatizadorSocket` tienen host y puerto hardcodeados (`"localhost"`, `14000`, `14001`, `14002`). Para cambiar la topología de red hay que modificar el código fuente. Deberían recibirse por constructor. | `agentes_actuadores/visualizador_bateria.py:65` `agentes_actuadores/visualizador_temperatura.py` `agentes_actuadores/visualizador_climatizador.py` | Medio | Bajo | Pendiente |
| S-005 | OCP       | **Factories con if/elif** — Las 9 factories del `configurador/` seleccionan la implementación con cadenas if/elif sobre el tipo como string. Agregar un nuevo tipo requiere modificar el archivo de la factory. Un Registry Pattern permitiría extensión sin modificación. | `configurador/factory_*.py` (9 archivos) | Bajo | Alto | Pendiente |

---

#### Hallazgos de los docs descartados o ya resueltos

| Hallazgo del doc | Estado | Motivo |
|-----------------|--------|--------|
| LSP: `@staticmethod` en `AbsVisualizadorBateria` | **Ya resuelto** | El código actual define los métodos como instancia (`def mostrar_tension(self, ...)`), no como `@staticmethod`. El doc analizó una versión anterior. |
| LSP: `AbsSeteoTemperatura` define `@staticmethod` | **Ya resuelto** | El código actual usa `@abstractmethod def obtener_seteo(self)`. Contrato de instancia correcto. |
| OCP: `Climatizador._definir_accion()` usa if/elif | **Ya resuelto** | La implementación actual usa un diccionario de decisiones (`decisiones = {("alta", "apagado"): "enfriar", ...}`), no if/elif. |
| SRP: `OperadorParalelo` como God Class | **No válido** | Orquestar ejecución paralela ES su responsabilidad única. El documento `Buenos_Ejemplos_SOLID.md` corrige este error de análisis. |
| SRP: `Bateria.indicador` debería ir a un servicio de dominio | **Debatable / no se agrega** | El patrón Information Expert justifica que la entidad calcule su propio indicador dado que tiene toda la información necesaria (nivel, umbral). Extraerlo a un servicio solo agrega indirección sin beneficio real a esta escala. |
| SRP: Dividir `Configurador` en 3 clases | **Over-engineered / no se agrega** | Para el tamaño actual del proyecto, dividir en `CargadorConfiguracion`, `ValidadorConfiguracion` y `ProveedorConfiguracion` agrega complejidad sin beneficio proporcional. |

---

## Resumen por prioridad

| Prioridad | IDs | Criterio |
|-----------|-----|----------|
| 1 — Corregir primero | C-001, A-001, A-002 | Viola reglas explícitas del proyecto o la arquitectura |
| 2 — Mejora importante | D-001, C-002, C-003, D-004, S-001, T-001 | Inconsistencias de diseño o estructura |
| 3 — Mejora incremental | D-002, D-003, D-005, C-005, S-002, S-003, S-004, T-002 | Calidad de código y organización |
| 4 — Cosmético / bajo impacto | C-004, C-006, S-005 | Estilo menor o esfuerzo/beneficio bajo |

---

## Plan de Trabajo — Flujo Kanban

### Tablero de estado

| Ticket | Título | Fase | Estado |
|--------|--------|------|--------|
| TKT-01 | Eliminar f-strings en configurador | 1 | Backlog |
| TKT-02 | Mover interfaces AbsSeteo/AbsSelector a entidades/ | 1 | Backlog |
| TKT-03 | Unificar uso de Configurador como clase estática | 2 | Backlog |
| TKT-04 | Reemplazar wildcard imports en ejecutar.py | 2 | Backlog |
| TKT-05 | Reemplazar print() por logging en _validar_configuracion | 2 | Backlog |
| TKT-06 | Unificar ciclo de vida de sockets | 3 | Backlog |
| TKT-07 | Context manager para sockets persistentes | 3 | Backlog |
| TKT-08 | Consolidar estructura de tests en subdirectorios | 4 | Backlog |
| TKT-09 | Separar AbsClimatizador en abs_climatizador.py | 4 | Backlog |
| TKT-10 | ControladorTemperatura como función de módulo | 5 | Backlog |
| TKT-11 | Constantes para tipos de temperatura | 5 | Backlog |
| TKT-12 | Documentar o implementar mostrar_indicador() | 5 | Backlog |
| TKT-13 | Resolver test HAL huérfano | 5 | Backlog |
| TKT-14 | Newline final en ejecutar.py | 5 | Backlog |
| TKT-15 | Extraer Registrador/Auditor como dependencias inyectadas | 6 | Backlog |
| TKT-16 | Quitar herencia de AbsRegistrador en SelectorTemperaturaArchivo | 6 | Backlog |
| TKT-17 | Corregir @staticmethod en SelectorTemperaturaArchivo | 6 | Backlog |
| TKT-18 | Inyectar host/puerto en visualizadores socket | 6 | Backlog |
| TKT-19 | Registry Pattern en factories (OCP) | 6 | Backlog |

**Estados posibles:** `Backlog` → `Listo` → `En curso` → `En revisión` → `Hecho`

---

### Fase 1 — Compliance: Reglas del proyecto y arquitectura

> Prerrequisito para todas las fases siguientes. Corrige violaciones explícitas de las reglas definidas en CLAUDE.md y de la arquitectura Clean Architecture.

---

#### TKT-01: Eliminar f-strings en configurador

| Campo | Valor |
|-------|-------|
| Hallazgos | C-001 |
| Impacto | Alto |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`configurador/configurador.py` usa f-strings en tres lugares (líneas 71, 79, 233), violando la regla explícita del proyecto de usar `.format()` para mantener compatibilidad con Python 3.5.

**Archivos afectados:**
- `configurador/configurador.py`

**Criterios de aceptación (DoD):**
- [ ] No existe ningún f-string en el archivo
- [ ] Los mensajes de error mantienen la misma información
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-02: Mover interfaces AbsSeteo/AbsSelector a entidades/

| Campo | Valor |
|-------|-------|
| Hallazgos | A-001, A-002 |
| Impacto | Alto |
| Esfuerzo | Medio |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`AbsSeteoTemperatura` y `AbsSelectorTemperatura` están definidas en `servicios_aplicacion/`, pero son interfaces que `agentes_sensores/` implementa. Esto invierte la dirección de dependencias: un adaptador (capa externa) depende de la capa de aplicación en lugar de depender del dominio.

La corrección es mover ambas interfaces a `entidades/` (como ya ocurre con `AbsProxyBateria`, `AbsProxySensorTemperatura`, etc.) y actualizar todos los imports que las referencian.

**Archivos afectados:**
- `servicios_aplicacion/abs_seteo_temperatura.py` → mover a `entidades/abs_seteo_temperatura.py`
- `servicios_aplicacion/abs_selector_temperatura.py` → mover a `entidades/abs_selector_temperatura.py`
- `agentes_sensores/proxy_seteo_temperatura.py` — actualizar import
- `agentes_sensores/proxy_selector_temperatura.py` — actualizar import
- `servicios_aplicacion/lanzador.py` — verificar si importa estas interfaces directamente
- `configurador/factory_seteo_temperatura.py` — verificar imports
- `configurador/factory_selector_temperatura.py` — verificar imports

**Criterios de aceptación (DoD):**
- [ ] Ningún archivo en `agentes_sensores/` importa desde `servicios_aplicacion/`
- [ ] Los archivos `abs_*.py` movidos siguen el naming convention del proyecto
- [ ] `pytest Test/ -v` pasa sin regresiones
- [ ] `grep -r "from servicios_aplicacion" agentes_sensores/` no devuelve resultados

---

### Fase 2 — Diseño: Coherencia y convenciones

> Mejoras de diseño que no rompen arquitectura pero generan inconsistencias. Se pueden trabajar en paralelo entre sí una vez finalizada la Fase 1.

---

#### TKT-03: Unificar uso de Configurador como clase estática

| Campo | Valor |
|-------|-------|
| Hallazgos | D-001 |
| Impacto | Alto |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`Configurador` tiene todos sus métodos como `@staticmethod` y usa un atributo de clase (`configuracion_termostato = None`) como estado global. Sin embargo, `ejecutar.py` lo llama instanciando: `Configurador().cargar_configuracion()`. Esta mezcla de acceso por instancia y por clase es confusa y no corresponde a ningún patrón explícito.

La corrección más simple: eliminar la instanciación innecesaria en `ejecutar.py` usando `Configurador.cargar_configuracion()` directamente. Si en el futuro se quiere Singleton real, ese sería un ticket separado.

**Archivos afectados:**
- `ejecutar.py`

**Criterios de aceptación (DoD):**
- [ ] `ejecutar.py` llama `Configurador.cargar_configuracion()` sin instanciar
- [ ] No existe `Configurador()` (con paréntesis de instanciación) en el código
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-04: Reemplazar wildcard imports en ejecutar.py

| Campo | Valor |
|-------|-------|
| Hallazgos | C-002 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | TKT-03 (porque cambia qué se importa de configurador) |
| Estado | Backlog |

**Descripción:**
`ejecutar.py` importa con `*` dos módulos completos. Pylint detecta decenas de símbolos no usados. Solo se necesitan `Lanzador` y `Configurador`.

**Archivos afectados:**
- `ejecutar.py`

**Criterios de aceptación (DoD):**
- [ ] Imports explícitos: `from servicios_aplicacion.lanzador import Lanzador` y `from configurador.configurador import Configurador`
- [ ] Pylint no reporta W0401 ni W0614 en `ejecutar.py`

---

#### TKT-05: Reemplazar print() por logging en _validar_configuracion

| Campo | Valor |
|-------|-------|
| Hallazgos | C-003 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`Configurador._validar_configuracion()` emite advertencias con `print()` mientras todo el resto del sistema usa `logging`. Las advertencias de configuración deben ir al log para ser visibles en `termostato.log`.

**Archivos afectados:**
- `configurador/configurador.py`

**Criterios de aceptación (DoD):**
- [ ] No hay `print()` en `configurador/configurador.py`
- [ ] Las advertencias usan `logging.warning()`
- [ ] El logger se inicializa con `logging.getLogger(__name__)` al inicio del módulo

---

### Fase 3 — Arquitectura de sockets

> Requiere una decisión de diseño explícita antes de implementar. Ambos tickets son dependientes entre sí conceptualmente.

---

#### TKT-06: Unificar ciclo de vida de sockets

| Campo | Valor |
|-------|-------|
| Hallazgos | D-004 |
| Impacto | Medio |
| Esfuerzo | Medio |
| Depende de | Decisión de diseño previa |
| Estado | Backlog |

**Descripción:**
Existe una inconsistencia no documentada entre los proxies de sensores:
- `ProxyBateriaSocket` y `ProxySensorTemperaturaSocket`: crean y destruyen el socket TCP **en cada llamada** a `leer_*()`
- `SeteoTemperaturaSocket` y `SelectorTemperaturaSocket`: mantienen una **conexión persistente** entre llamadas

Ambos enfoques son válidos pero responden a casos de uso distintos (sensores que envían datos periódicamente vs. comandos esporádicos del usuario). La diferencia debe documentarse o unificarse.

**Decisión a tomar antes de implementar:**
- Opción A: Mantener la diferencia, documentarla con comentarios explícitos en cada clase
- Opción B: Unificar hacia conexión persistente para todos los sockets de lectura

**Archivos afectados:**
- `agentes_sensores/proxy_bateria.py`
- `agentes_sensores/proxy_sensor_temperatura.py`

**Criterios de aceptación (DoD):**
- [ ] La decisión de diseño está documentada en los docstrings de las clases
- [ ] El comportamiento es consistente o la diferencia está justificada explícitamente
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-07: Context manager para sockets persistentes

| Campo | Valor |
|-------|-------|
| Hallazgos | C-005 |
| Impacto | Medio |
| Esfuerzo | Medio |
| Depende de | TKT-06 (define qué clases tienen sockets persistentes) |
| Estado | Backlog |

**Descripción:**
`SeteoTemperaturaSocket` y `SelectorTemperaturaSocket` mantienen un socket abierto entre llamadas y usan `__del__` para cerrarlo. `__del__` en Python no garantiza ejecución determinista (el GC puede llamarlo tarde o nunca en CPython bajo ciertas condiciones). El patrón correcto es implementar context manager (`__enter__` / `__exit__`) para garantizar el cierre de recursos.

**Archivos afectados:**
- `agentes_sensores/proxy_seteo_temperatura.py`
- `agentes_sensores/proxy_selector_temperatura.py`
- `servicios_aplicacion/lanzador.py` — adaptar el uso si se adopta `with`

**Criterios de aceptación (DoD):**
- [ ] Las clases implementan `__enter__` y `__exit__`
- [ ] `__del__` eliminado o reducido a fallback de última instancia
- [ ] `pytest Test/ -v` pasa sin regresiones

---

### Fase 4 — Organización estructural

> Mejoras de organización de archivos que no cambian comportamiento. Apropiadas para trabajar en una rama separada.

---

#### TKT-08: Consolidar estructura de tests en subdirectorios

| Campo | Valor |
|-------|-------|
| Hallazgos | T-001 |
| Impacto | Medio |
| Esfuerzo | Medio |
| Depende de | Fases 1 y 2 completadas (los tests deben pasar antes de migrar) |
| Estado | Backlog |

**Descripción:**
Coexisten dos estructuras de tests:
- **Vieja** (raíz de `Test/`): `test_bateria_desde_archivo.py`, `test_climatizador.py`, `test_lanzador.py`, etc.
- **Nueva** (`Test/unit/`, `Test/integration/`): estructura organizada por capa con `conftest.py`

Los tests en la raíz deben analizarse caso por caso: migrarlos a la estructura nueva si agregan cobertura, eliminarlos si son redundantes con los tests existentes en subdirectorios.

**Archivos afectados:**
- `Test/*.py` (todos los archivos .py en raíz de Test/)

**Criterios de aceptación (DoD):**
- [ ] No hay archivos `test_*.py` directamente en `Test/` (solo en subdirectorios)
- [ ] `pytest Test/ -v` reporta al menos la misma cantidad de tests que antes
- [ ] Cobertura no disminuye respecto al baseline

---

#### TKT-09: Separar AbsClimatizador en abs_climatizador.py

| Campo | Valor |
|-------|-------|
| Hallazgos | D-003 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
El proyecto tiene la convención de separar interfaces abstractas en archivos `abs_*.py`. Esta convención se aplica en `abs_bateria.py`, `abs_sensor_temperatura.py`, `abs_actuador_climatizador.py`, etc., pero `AbsClimatizador` convive con `Climatizador` y `Calefactor` en `climatizador.py`.

Extraer `AbsClimatizador` a `entidades/abs_climatizador.py` para coherencia.

**Archivos afectados:**
- `entidades/climatizador.py` — queda solo con `Climatizador` y `Calefactor`
- `entidades/abs_climatizador.py` — nuevo archivo con `AbsClimatizador`
- Todos los imports de `AbsClimatizador` en el proyecto

**Criterios de aceptación (DoD):**
- [ ] `entidades/abs_climatizador.py` existe y contiene solo `AbsClimatizador`
- [ ] `entidades/climatizador.py` importa desde `abs_climatizador.py`
- [ ] `pytest Test/ -v` pasa sin regresiones

---

### Fase 5 — Refinamiento

> Mejoras incrementales de calidad. Pueden tomarse en cualquier orden y son independientes entre sí.

---

#### TKT-10: ControladorTemperatura como función de módulo

| Campo | Valor |
|-------|-------|
| Hallazgos | D-002 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`ControladorTemperatura` es una clase sin estado con un único `@staticmethod`. En Python idiomático, esto es simplemente una función de módulo. Mantenerlo como clase no aporta extensibilidad real y agrega ruido visual.

Alternativa: si se quiere mantener como clase por razones pedagógicas (demostrar el patrón Service), documentarlo explícitamente. Si se convierte a función, actualizar todos los call sites.

**Archivos afectados:**
- `servicios_dominio/controlador_climatizador.py`
- `entidades/climatizador.py` — principal consumidor

**Criterios de aceptación (DoD):**
- [ ] La función `comparar_temperatura()` se expone a nivel de módulo O la clase mantiene el patrón con justificación documentada
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-11: Constantes para tipos de temperatura

| Campo | Valor |
|-------|-------|
| Hallazgos | D-005 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
Los valores `"ambiente"` y `"deseada"` se usan como discriminador en `Ambiente.temperatura_a_mostrar` y `GestorAmbiente.mostrar_temperatura()`. Un typo en cualquier lugar de uso pasa silenciosamente sin error. Definir constantes de módulo o un `Enum` en `entidades/ambiente.py`.

**Archivos afectados:**
- `entidades/ambiente.py`
- `gestores_entidades/gestor_ambiente.py`
- `servicios_aplicacion/` (si consume estos valores)

**Criterios de aceptación (DoD):**
- [ ] Existen constantes o Enum para los tipos de temperatura a mostrar
- [ ] No hay string literals `"ambiente"` ni `"deseada"` fuera de la definición de constantes
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-12: Documentar o implementar VisualizadorBateriaApi.mostrar_indicador()

| Campo | Valor |
|-------|-------|
| Hallazgos | C-004 |
| Impacto | Bajo |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`VisualizadorBateriaApi.mostrar_indicador()` solo tiene un `pass`. Puede ser intencional (la API calcula el indicador a partir del nivel de carga), pero no está documentado. Si es intencional, agregar un comentario explicativo. Si es un olvido, implementarlo.

**Archivos afectados:**
- `agentes_actuadores/visualizador_bateria.py`

**Criterios de aceptación (DoD):**
- [ ] El método tiene un docstring o comentario que explica por qué no hace nada, o tiene implementación

---

#### TKT-13: Resolver test HAL huérfano

| Campo | Valor |
|-------|-------|
| Hallazgos | T-002 |
| Impacto | Bajo |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`Test/hal/test_hal_adc.py` existe pero no hay módulo `hal/` en el código de producción. Decidir: implementar la capa HAL o eliminar el test.

**Archivos afectados:**
- `Test/hal/test_hal_adc.py`

**Criterios de aceptación (DoD):**
- [ ] El test tiene un módulo correspondiente en producción, o el archivo fue eliminado con justificación en el commit

---

#### TKT-14: Newline final en ejecutar.py

| Campo | Valor |
|-------|-------|
| Hallazgos | C-006 |
| Impacto | Bajo |
| Esfuerzo | Bajo |
| Depende de | TKT-04 (se edita el mismo archivo, mejor hacerlo junto) |
| Estado | Backlog |

**Descripción:**
`ejecutar.py` no termina con newline. Pylint reporta C0304. Convención POSIX y PEP 8.

**Archivos afectados:**
- `ejecutar.py`

**Criterios de aceptación (DoD):**
- [ ] Pylint no reporta C0304 en `ejecutar.py`

---

### Fase 6 — SOLID: Cross-cutting concerns y extensibilidad

> Hallazgos surgidos de la revisión de `docs/Analisis_Violaciones_*.md`, verificados contra el código actual.
> Los items descartados de esos docs están documentados en la sección "Hallazgos descartados".

---

#### TKT-15: Extraer Registrador/Auditor como dependencias inyectadas en ActuadorClimatizadorGeneral

| Campo | Valor |
|-------|-------|
| Hallazgos | S-001 |
| Impacto | Alto |
| Esfuerzo | Medio |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`ActuadorClimatizadorGeneral` hereda de tres interfaces: `AbsProxyActuadorClimatizador`, `AbsRegistrador` y `AbsAuditor`. El logging y la auditoría son cross-cutting concerns que la clase no debería "ser" — debería "tener". La herencia múltiple para incorporar estos concerns viola ISP (la clase está forzada a implementar interfaces de responsabilidades ortogonales) y SRP (tiene 3 razones para cambiar: lógica de actuación, formato de error, formato de auditoría).

La solución es recibir un registrador y un auditor por inyección de dependencia, eliminando la herencia de `AbsRegistrador` y `AbsAuditor`.

**Archivos afectados:**
- `agentes_actuadores/actuador_climatizador.py`
- `configurador/factory_actuador_climatizador.py` — inyectar dependencias al crear
- `registrador/registrador.py` — verificar si las interfaces permanecen o se simplifican

**Criterios de aceptación (DoD):**
- [ ] `ActuadorClimatizadorGeneral` hereda solo de `AbsProxyActuadorClimatizador`
- [ ] El registrador y el auditor se reciben en el constructor
- [ ] La factory inyecta las implementaciones concretas
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-16: Quitar herencia de AbsRegistrador en SelectorTemperaturaArchivo

| Campo | Valor |
|-------|-------|
| Hallazgos | S-002 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | TKT-15 (si se crea un servicio de Registrador reutilizable, usarlo aquí) |
| Estado | Backlog |

**Descripción:**
`SelectorTemperaturaArchivo` hereda de `AbsSelectorTemperatura` y `AbsRegistrador`. Su implementación hermana `SelectorTemperaturaSocket` no hereda `AbsRegistrador`. Esta inconsistencia evidencia que el registro de errores no es parte del contrato del selector sino un detalle de implementación. Inyectar el registrador como dependencia opcional en el constructor.

**Archivos afectados:**
- `agentes_sensores/proxy_selector_temperatura.py`

**Criterios de aceptación (DoD):**
- [ ] `SelectorTemperaturaArchivo` hereda solo de `AbsSelectorTemperatura`
- [ ] El registro de errores se realiza a través de una dependencia inyectada o directamente con `logging`
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-17: Corregir @staticmethod en SelectorTemperaturaArchivo

| Campo | Valor |
|-------|-------|
| Hallazgos | S-003 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | TKT-16 (se edita el mismo archivo) |
| Estado | Backlog |

**Descripción:**
Dentro de la misma familia, `SelectorTemperaturaArchivo.obtener_selector()` es `@staticmethod` (sin estado, sin `self`), mientras que `SelectorTemperaturaSocket.obtener_selector()` es un método de instancia (requiere `self` para acceder al socket). La interfaz abstracta `AbsSelectorTemperatura` debería definir el contrato correcto (método de instancia), y `SelectorTemperaturaArchivo` debería adoptarlo para ser intercambiable de forma transparente.

**Archivos afectados:**
- `agentes_sensores/proxy_selector_temperatura.py`
- `servicios_aplicacion/abs_selector_temperatura.py` (verificar contrato)

**Criterios de aceptación (DoD):**
- [ ] `SelectorTemperaturaArchivo.obtener_selector(self)` es método de instancia
- [ ] `AbsSelectorTemperatura.obtener_selector(self)` define contrato de instancia
- [ ] Ambas implementaciones son intercambiables sin que el cliente deba saber cuál usa
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-18: Inyectar host/puerto en visualizadores socket

| Campo | Valor |
|-------|-------|
| Hallazgos | S-004 |
| Impacto | Medio |
| Esfuerzo | Bajo |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
`VisualizadorBateriaSocket`, `VisualizadorTemperaturaSocket` y `VisualizadorClimatizadorSocket` tienen host y puertos hardcodeados (`"localhost"`, `14000`, `14001`, `14002`). Para desplegar en una topología diferente (Raspberry Pi + Mac, por ejemplo) hay que modificar código fuente. El host y puerto deberían inyectarse en el constructor, igual que ya se hace en los proxies de sensores (`ProxyBateriaSocket`, `ProxySensorTemperaturaSocket`).

**Archivos afectados:**
- `agentes_actuadores/visualizador_bateria.py`
- `agentes_actuadores/visualizador_temperatura.py`
- `agentes_actuadores/visualizador_climatizador.py`
- `configurador/factory_visualizador_bateria.py` — pasar host/puerto al crear
- `configurador/factory_visualizador_temperatura.py`
- `configurador/factory_visualizador_climatizador.py`

**Criterios de aceptación (DoD):**
- [ ] Los tres visualizadores reciben `host` y `puerto` en el constructor
- [ ] Las factories leen los valores desde `Configurador` (igual que los proxies)
- [ ] No hay strings `"localhost"` ni números de puerto literales en los visualizadores
- [ ] `pytest Test/ -v` pasa sin regresiones

---

#### TKT-19: Registry Pattern en factories (OCP)

| Campo | Valor |
|-------|-------|
| Hallazgos | S-005 |
| Impacto | Bajo |
| Esfuerzo | Alto |
| Depende de | — |
| Estado | Backlog |

**Descripción:**
Las 9 factories del `configurador/` seleccionan implementaciones con cadenas `if/elif` sobre un string de tipo. Agregar una nueva implementación (ej: visualizador MQTT) requiere modificar el archivo de la factory, violando OCP. Un Registry Pattern permite registrar nuevas implementaciones desde fuera de la factory, sin modificar código existente.

Este ticket tiene **esfuerzo alto** en relación a su impacto práctico actual, ya que el sistema tiene un número reducido de tipos y la extensión es infrecuente. Se recomienda abordar solo si el proyecto crece o si se busca demostrar el patrón explícitamente con fines educativos.

**Archivos afectados:**
- Todos los `configurador/factory_*.py` (9 archivos)
- `configurador/configurador.py` — inicialización del registry

**Criterios de aceptación (DoD):**
- [ ] Existe una clase base `RegistryFactory` con métodos `register()` y `crear()`
- [ ] Todas las factories heredan de `RegistryFactory`
- [ ] Los tipos se registran en el módulo `configurador/__init__.py` o en un módulo de inicialización
- [ ] Agregar un nuevo tipo NO requiere modificar ningún archivo existente
- [ ] `pytest Test/ -v` pasa sin regresiones
