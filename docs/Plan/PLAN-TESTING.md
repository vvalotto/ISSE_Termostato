# Plan de Cobertura de Testing — ISSE Termostato

**Fecha:** 2026-03-06
**Cobertura actual:** 63% (2454 statements, 908 sin cubrir)
**Objetivo:** ≥ 85% de cobertura en módulos de producción

---

## Estado Actual por Módulo

| Módulo | Cobertura | Statements | Sin cubrir |
|--------|-----------|------------|------------|
| `entidades/` | ~98% | — | Mínimo |
| `servicios_dominio/` | 100% | 10 | 0 |
| `gestores_entidades/` | 100% | 68 | 0 |
| `configurador/configurador.py` | 78% | 130 | 28 |
| `registrador/registrador.py` | 50% | 30 | 15 |
| `agentes_actuadores/actuador_climatizador.py` | 29% | 24 | 17 |
| `agentes_actuadores/visualizador_bateria.py` | 37% | 38 | 24 |
| `agentes_actuadores/visualizador_climatizador.py` | 42% | 26 | 15 |
| `agentes_actuadores/visualizador_temperatura.py` | 90% | 41 | 4 |
| `agentes_actuadores/visualizador_estado_consolidado.py` | **0%** | 68 | 68 |
| `agentes_sensores/proxy_bateria.py` | 41% | 49 | 29 |
| `agentes_sensores/proxy_sensor_temperatura.py` | 37% | 49 | 31 |
| `agentes_sensores/proxy_selector_temperatura.py` | **17%** | 69 | 57 |
| `agentes_sensores/proxy_seteo_temperatura.py` | **17%** | 65 | 54 |
| `servicios_aplicacion/inicializador.py` | **0%** | 18 | 18 |
| `servicios_aplicacion/lanzador.py` | **0%** | 36 | 36 |
| `servicios_aplicacion/operador_paralelo.py` | **0%** | 40 | 40 |
| `servicios_aplicacion/operador_secuencial.py` | **0%** | 31 | 31 |
| `servicios_aplicacion/presentador.py` | **0%** | 22 | 22 |
| `servicios_aplicacion/selector_entrada.py` | **0%** | 23 | 23 |

---

## Criterios de Priorización

| Criterio | Descripción |
|----------|-------------|
| **Regresión crítica** | Código nuevo o modificado durante el plan de mejoras sin tests |
| **Lógica de dominio** | Reglas de negocio que no deben romperse |
| **Valor/esfuerzo** | Tests que aportan cobertura real con implementación directa |
| **Descartado** | Coordinadores de infraestructura donde el mock supera al valor |

---

## Fase A — Regresión inmediata (código modificado sin tests)

> Prioridad máxima. Cubre código nuevo introducido durante el plan de mejoras.
> Ninguno de estos módulos tiene tests actualmente.

### A-1: `registrador/registrador.py` (50% → 100%)

**Contexto:** `RegistradorArchivo` y `AuditorArchivo` son clases nuevas creadas en TKT-15.
La mitad cubierta es solo la definición de las clases abstractas.

**Archivo a crear:** `Test/unit/registrador/test_registrador.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| REG-001 | `RegistradorArchivo.registrar_error` con mensaje válido | Escribe en `registro_errores` |
| REG-002 | `RegistradorArchivo.registrar_error` con IOError | Lanza `IOError` con mensaje descriptivo |
| REG-003 | `AuditorArchivo.auditar_funcion` con datos válidos | Escribe clase, fecha_hora y mensaje en `registro_auditoria` |
| REG-004 | `AuditorArchivo.auditar_funcion` con IOError | Lanza `IOError` con mensaje descriptivo |
| REG-005 | Contenido del archivo de auditoría | Formato correcto con separador `*************` |

---

### A-2: `agentes_actuadores/actuador_climatizador.py` (29% → 90%)

**Contexto:** `ActuadorClimatizadorGeneral` cambió su interfaz en TKT-15 — ahora recibe
`registrador` y `auditor` por inyección. El 71% no cubierto es toda la lógica de accionamiento.

**Archivo a crear:** `Test/unit/agentes_actuadores/test_actuador_climatizador.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| ACT-001 | `accionar_climatizador("calentar")` | Llama `auditar_funcion` en auditor y escribe en climatizador |
| ACT-002 | `accionar_climatizador("enfriar")` | Ídem para enfriamiento |
| ACT-003 | `accionar_climatizador("apagar")` | Ídem para apagado |
| ACT-004 | Error de escritura en archivo climatizador | Llama `registrar_error` en registrador |
| ACT-005 | Constructor inyecta registrador y auditor | `_registrador` y `_auditor` asignados correctamente |
| ACT-006 | Auditor recibe clase y mensaje correctos | Verificar args de `auditar_funcion` con mock |

---

### A-3: `agentes_sensores/proxy_selector_temperatura.py` (17% → 85%)

**Contexto:** Modificado en TKT-16 (eliminó herencia AbsRegistrador) y TKT-17
(`obtener_selector` pasó de `@staticmethod` a método de instancia). Casi sin cobertura.

**Archivo a crear:** `Test/integration/adaptadores/test_selector_temperatura.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| SEL-001 | `SelectorTemperaturaArchivo.obtener_selector` con archivo existente | Retorna contenido del archivo |
| SEL-002 | `SelectorTemperaturaArchivo.obtener_selector` con archivo inexistente | Lanza `IOError` |
| SEL-003 | `SelectorTemperaturaArchivo.obtener_selector` con valor "ambiente" | Retorna `TEMP_AMBIENTE` |
| SEL-004 | `SelectorTemperaturaArchivo.obtener_selector` con valor "deseada" | Retorna `TEMP_DESEADA` |
| SEL-005 | `SelectorTemperaturaSocket` — instanciación con host/puerto | Almacena correctamente |
| SEL-006 | `SelectorTemperaturaSocket.obtener_selector` — mock socket exitoso | Retorna valor recibido |
| SEL-007 | `SelectorTemperaturaSocket.obtener_selector` — ConnectionError | Maneja error sin propagar |

---

### A-4: `configurador/registry_factory.py` + factories faltantes

**Contexto:** `RegistryFactory` es clase nueva de TKT-19, no tiene ningún test.
Seis factories tampoco tienen tests.

**Archivo a crear:** `Test/unit/configurador/test_registry_factory.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| REG-F-001 | `registrar` + `crear` con tipo registrado | Retorna instancia correcta |
| REG-F-002 | `crear` con tipo no registrado | Retorna `None` |
| REG-F-003 | Dos subclases con `_registry` propio | Registros independientes (no comparten) |
| REG-F-004 | `registrar` sobreescribe tipo existente | Nueva función reemplaza la anterior |
| REG-F-005 | `crear` pasa `**kwargs` a la factory function | kwargs llegan correctamente |

**Agregar a** `Test/unit/configurador/test_factories.py`:

| ID | Caso de prueba | Factory |
|----|---------------|---------|
| FAC-001 | tipo "archivo" → instancia correcta | `FactoryProxySensorTemperatura` |
| FAC-002 | tipo "socket" → instancia correcta | `FactoryProxySensorTemperatura` |
| FAC-003 | tipo "general" → `ActuadorClimatizadorGeneral` con DI | `FactoryActuadorClimatizador` |
| FAC-004 | tipo "archivo" → `VisualizadorBateria` | `FactoryVisualizadorBateria` |
| FAC-005 | tipo "socket" → `VisualizadorBateriaSocket` | `FactoryVisualizadorBateria` |
| FAC-006 | tipo "api" → `VisualizadorBateriaApi` | `FactoryVisualizadorBateria` |
| FAC-007 | tipo "archivo" → `VisualizadorClimatizador` | `FactoryVisualizadorClimatizador` |
| FAC-008 | tipo "socket" → `VisualizadorClimatizadorSocket` | `FactoryVisualizadorClimatizador` |
| FAC-009 | tipo "api" → `VisualizadorClimatizadorApi` | `FactoryVisualizadorClimatizador` |
| FAC-010 | tipo "archivo" → `SelectorTemperaturaArchivo` | `FactorySelectorTemperatura` |
| FAC-011 | tipo "socket" → `SelectorTemperaturaSocket` | `FactorySelectorTemperatura` |
| FAC-012 | tipo "consola" → `SeteoTemperatura` | `FactorySeteoTemperatura` |
| FAC-013 | tipo "socket" → `SeteoTemperaturaSocket` | `FactorySeteoTemperatura` |

---

## Fase B — Cobertura de adaptadores

> Cubre la capa de Interface Adapters que interactúa con el exterior.
> Todos usan mocks para socket y requests.

### B-1: Visualizadores de batería y climatizador (37-42% → 90%)

**Tests faltantes:** `VisualizadorBateriaSocket`, `VisualizadorBateriaApi`,
`VisualizadorClimatizadorSocket`, `VisualizadorClimatizadorApi`, `VisualizadorClimatizador` (consola).

**Agregar a** `Test/integration/adaptadores/test_visualizadores.py`:

| ID | Caso de prueba | Clase |
|----|---------------|-------|
| VIS-B-001 | `mostrar_nivel_carga` imprime en consola | `VisualizadorBateria` |
| VIS-B-002 | `mostrar_indicador` imprime en consola | `VisualizadorBateria` |
| VIS-B-003 | `mostrar_nivel_carga` envía datos al socket | `VisualizadorBateriaSocket` |
| VIS-B-004 | `mostrar_indicador` envía datos al socket | `VisualizadorBateriaSocket` |
| VIS-B-005 | `mostrar_nivel_carga` hace POST a API | `VisualizadorBateriaApi` |
| VIS-B-006 | `mostrar_indicador` hace POST a API | `VisualizadorBateriaApi` |
| VIS-C-001 | `mostrar_estado_climatizador` imprime en consola | `VisualizadorClimatizador` |
| VIS-C-002 | `mostrar_estado_climatizador` envía al socket | `VisualizadorClimatizadorSocket` |
| VIS-C-003 | `mostrar_estado_climatizador` hace POST a API | `VisualizadorClimatizadorApi` |
| VIS-C-004 | Error de conexión socket — no propaga excepción | `VisualizadorBateriaSocket` |
| VIS-C-005 | Error de conexión API — no propaga excepción | `VisualizadorBateriaApi` |

---

### B-2: Proxies de seteo y batería socket (17-41% → 80%)

**Arreglo de tests rotos:**

| ID | Caso de prueba | Archivo |
|----|---------------|---------|
| PRX-FIX-001 | `ProxyBateriaSocket(host, puerto)` con mock socket | `test_proxies.py` — arreglar constructor |
| PRX-FIX-002 | `ProxyBateriaSocket` — ConnectionError manejado | `test_proxies.py` — arreglar constructor |

**Tests nuevos** en `Test/integration/adaptadores/test_proxies.py`:

| ID | Caso de prueba | Clase |
|----|---------------|-------|
| PRX-SET-001 | `SeteoTemperatura.obtener_seteo` desde archivo | `SeteoTemperaturaArchivo` |
| PRX-SET-002 | `SeteoTemperaturaSocket` — init con host/puerto | `SeteoTemperaturaSocket` |
| PRX-SET-003 | `SeteoTemperaturaSocket.obtener_seteo` — mock socket exitoso | `SeteoTemperaturaSocket` |
| PRX-SET-004 | `SeteoTemperaturaSocket` como context manager | `SeteoTemperaturaSocket` |
| PRX-SET-005 | `SeteoTemperaturaSocket.__exit__` cierra recursos | `SeteoTemperaturaSocket` |
| PRX-SNS-001 | `ProxySensorTemperaturaSocket` con mock socket | `ProxySensorTemperaturaSocket` |
| PRX-BAT-001 | `ProxyBateriaSocket` con host y puerto correctos | `ProxyBateriaSocket` |

---

### B-3: `VisualizadorEstadoConsolidadoSocket` (0% → 80%)

**Archivo a crear:** `Test/unit/agentes_actuadores/test_visualizador_estado_consolidado.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| VEC-001 | Constructor con host y puerto | Almacena correctamente |
| VEC-002 | `mostrar_estado_completo` — envía JSON por socket (mock) | Socket conecta y envía bytes |
| VEC-003 | Formato JSON enviado contiene todos los campos requeridos | 8 campos del contrato de API |
| VEC-004 | `_construir_estado` — temperatura None → `falla_sensor=True` y `temp=0.0` | Manejo defensivo |
| VEC-005 | `_construir_estado` — batería BAJA → `bateria_baja=True` | Mapeo correcto |
| VEC-006 | `_mapear_modo_climatizador("apagado")` → `"reposo"` | Traducción de vocabulario |
| VEC-007 | `_mapear_modo_climatizador("calentando")` → `"calentando"` | Sin cambio |
| VEC-008 | `mostrar_estado_completo` — ConnectionError no propaga | Manejo defensivo de red |
| VEC-009 | Timestamp en formato ISO 8601 | `datetime.now().isoformat()` |

---

## Fase C — Completar cobertura de Configurador (78% → 92%)

**Agregar a** `Test/unit/configurador/test_configurador.py`:

| ID | Caso de prueba | Método |
|----|---------------|--------|
| CFG-001 | `_buscar_config` encuentra primera ruta existente | Helper de módulo |
| CFG-002 | `_buscar_config` lanza `FileNotFoundError` si no hay ninguna | Helper de módulo |
| CFG-003 | `_cargar_json` con JSON inválido lanza `JSONDecodeError` | Helper de módulo |
| CFG-004 | `_verificar_claves_requeridas` con clave faltante lanza `KeyError` | Helper de módulo |
| CFG-005 | `_verificar_configuracion_red` con `red=None` emite warning | Helper de módulo |
| CFG-006 | `configurar_proxy_temperatura` retorna proxy correcto | `Configurador` |
| CFG-007 | `configurar_actuador_climatizador` retorna `ActuadorClimatizadorGeneral` | `Configurador` |
| CFG-008 | `configurar_visualizador_bateria` tipo "archivo" | `Configurador` |
| CFG-009 | `configurar_selector_temperatura` tipo "archivo" | `Configurador` |
| CFG-010 | `configurar_seteo_temperatura` tipo "consola" | `Configurador` |

---

## Fase D — Servicios de aplicación (0% → cobertura básica)

> Complejidad alta por dependencias externas (threads, ciclos infinitos, sistema de archivos).
> El objetivo es cobertura básica con mocks, no cobertura exhaustiva.

### D-1: `inicializador.py` (0% → 80%)

**Archivo a crear:** `Test/unit/servicios_aplicacion/test_inicializador.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| INI-001 | Batería en NORMAL y sensor disponible → retorna `True` | Happy path |
| INI-002 | Batería no NORMAL → retorna `False` sin continuar | Cortocircuito |
| INI-003 | Sensor devuelve `None` → retorna `False` | Cortocircuito |
| INI-004 | Temperatura deseada se fija en 24 al inicio | Efecto secundario |
| INI-005 | Presentador se ejecuta si todo es correcto | Verificar llamada |

---

### D-2: `selector_entrada.py` (0% → 75%)

**Archivo a crear:** `Test/unit/servicios_aplicacion/test_selector_entrada.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| SEL-ENT-001 | Selector retorna `TEMP_AMBIENTE` → indicar ambiente | Sin cambio de modo |
| SEL-ENT-002 | Selector retorna `TEMP_DESEADA` → aumentar/disminuir y volver | Ciclo de seteo |
| SEL-ENT-003 | Seteo devuelve incremento positivo → aumentar temperatura | Efecto en gestor |
| SEL-ENT-004 | Seteo devuelve incremento negativo → disminuir temperatura | Efecto en gestor |

---

### D-3: `presentador.py` (0% → 70%)

**Archivo a crear:** `Test/unit/servicios_aplicacion/test_presentador.py`

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| PRE-001 | `ejecutar` — invoca `mostrar_temperatura` en gestor_ambiente | Verificar llamada |
| PRE-002 | `ejecutar` — invoca `mostrar_nivel` en gestor_bateria | Verificar llamada |
| PRE-003 | `ejecutar` — invoca `mostrar_estado` en gestor_climatizador | Verificar llamada |

---

### D-4: `operador_secuencial.py` (0% → básico)

> No se testea el `while True` — demasiado acoplado a infraestructura.
> Solo se testea la inicialización.

| ID | Caso de prueba | Comportamiento esperado |
|----|---------------|------------------------|
| OPR-001 | Constructor asigna gestores correctamente | `_gestor_bateria`, `_gestor_ambiente`, `_gestor_climatizador` |
| OPR-002 | Constructor crea `_selector` y `_presentador` | Instancias correctas |

---

## Resumen de Impacto Esperado

| Fase | Tests nuevos | Cobertura estimada |
|------|-----------|--------------------|
| A (regresión inmediata) | ~30 | 63% → 72% |
| B (adaptadores) | ~25 | 72% → 80% |
| C (configurador) | ~10 | 80% → 83% |
| D (servicios aplicación) | ~15 | 83% → 87% |
| **Total** | **~80** | **63% → ≥85%** |

---

## Convenciones para los Tests Nuevos

- **Mocks:** usar `unittest.mock.Mock` y `patch` para socket, requests y sistema de archivos
- **Fixtures:** agregar al `conftest.py` correspondiente (unit o integration)
- **Archivos temporales:** usar `tmp_path` de pytest (fixture built-in)
- **Naming:** `test_<comportamiento>_<condicion>` en snake_case
- **Estructura:** Arrange → Act → Assert, sin lógica en el test
- **No f-strings:** usar `.format()` en el código de test (Python 3.5 compat)

---

## Orden de Implementación Sugerido

```
Fase A → Fase B (B-2 fix primero) → Fase C → Fase D
```

`B-2 fix` antes que cualquier otra cosa porque los 2 tests rotos
distorsionan el reporte de cobertura de `proxy_bateria.py`.

---

*Plan generado el 2026-03-06 — para implementación ver tickets en GitHub.*
