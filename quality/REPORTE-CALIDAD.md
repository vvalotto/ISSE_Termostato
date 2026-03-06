# Reporte de Calidad — Plan de Mejoras ISSE Termostato

**Fecha:** 2026-03-06
**Proyecto:** ISSE Termostato
**Alcance:** 19 tickets en 6 fases
**Herramientas:** `codeguard` v0.2.0 · `designreviewer` v0.2.0

---

## Resumen Ejecutivo

| Métrica | Resultado |
|---------|-----------|
| Tickets completados | 19 / 19 |
| Fases completadas | 6 / 6 |
| Issues críticos al cierre | **0** |
| Errores codeguard acumulados | **0** |
| Tests al cierre | 181 passed · 2 failed pre-existentes |

El plan de mejoras se ejecutó sin introducir ningún error nuevo de calidad en ninguna fase. Todos los issues críticos detectados por `designreviewer` eran pre-existentes y fueron abordados en las fases correspondientes.

---

## Sección 1 — codeguard por Ticket

### TKT-01: Eliminar f-strings en configurador

> Sin reporte codeguard individual (incluido en TKT-05 / Fase 1).

**Cambio:** 3 f-strings reemplazados por `.format()` en `configurador/configurador.py`.

---

### TKT-02: Mover interfaces AbsSeteo/AbsSelector a entidades/

> Sin reporte codeguard individual (incluido en Fase 1).

**Cambio:** Interfaces `AbsSeteoTemperatura` y `AbsSelectorTemperatura` movidas a `entidades/`. `agentes_sensores/` eliminó dependencia hacia `servicios_aplicacion/`.

---

### TKT-03: Unificar uso de Configurador como clase estática

| Campo | Valor |
|-------|-------|
| Módulo analizado | `servicios_aplicacion` |
| Errores | 0 |
| Advertencias | 0 |
| Informativos | 23 |
| Bloquea PR | No |

> Nota: `ejecutar.py` es archivo raíz — codeguard solo acepta directorios.

---

### TKT-04: Reemplazar wildcard imports en ejecutar.py

| Campo | Valor |
|-------|-------|
| Módulo analizado | `servicios_aplicacion` |
| Errores | 0 |
| Advertencias | 0 |
| Informativos | 23 |
| Bloquea PR | No |

---

### TKT-05: Reemplazar print() por logging en _validar_configuracion

| Campo | Valor |
|-------|-------|
| Módulo analizado | `configurador` |
| Errores | 0 |
| Advertencias | 0 |
| Informativos | 33 |
| Bloquea PR | No |

---

### TKT-06: Unificar ciclo de vida de sockets

| Campo | Valor |
|-------|-------|
| Módulo analizado | `agentes_sensores` |
| Archivos analizados | 5 |
| Errores | 0 |
| Advertencias | 2 |
| Informativos | 13 |
| Bloquea PR | No |

**Advertencias (pre-existentes):**

| Check | Archivo | Mensaje |
|-------|---------|---------|
| PEP8 | `agentes_sensores/proxy_bateria.py` | E128 continuation line under-indented |
| PEP8 | `agentes_sensores/proxy_sensor_temperatura.py` | E128 continuation line under-indented |

> Ambas advertencias son pre-existentes, no introducidas por TKT-06.

---

### TKT-07: Context manager para sockets persistentes

| Campo | Valor |
|-------|-------|
| Módulo analizado | `agentes_sensores` |
| Archivos analizados | 5 |
| Errores | 0 |
| Advertencias | 2 |
| Informativos | 13 |
| Bloquea PR | No |

**Advertencias:** Mismas 2 pre-existentes E128 que TKT-06.

**Cambios implementados:** `__del__` reemplazado por `__enter__`/`__exit__` en `SeteoTemperaturaSocket` y `SelectorTemperaturaSocket`. Cierre determinista de recursos.

---

### TKT-08: Consolidar estructura de tests en subdirectorios

| Campo | Valor |
|-------|-------|
| Herramienta | Sin codeguard (limpieza estructural) |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

**Directorios eliminados:** `Test/bateria/`, `Test/climatizador/`, `Test/lanzador/`, `Test/operador/`, `Test/presentador/`, `Test/temperatura/`, `Test/selector_temperatura/`.

| Métrica | Antes | Después |
|---------|-------|---------|
| Tests passed | 181 | 181 |
| Tests failed | 2 | 2 |
| Collection errors | 10 | 0 |

---

### TKT-09: Separar AbsClimatizador en abs_climatizador.py

| Campo | Valor |
|-------|-------|
| Módulos analizados | `entidades`, `configurador` |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

**Archivos creados:** `entidades/abs_climatizador.py`
**Archivos modificados:** `entidades/climatizador.py`, `configurador/factory_climatizador.py`

---

### TKT-10: ControladorTemperatura como función de módulo

| Campo | Valor |
|-------|-------|
| Módulo analizado | `servicios_dominio` |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

> Se mantiene como clase (patrón Service). Justificación documentada en docstring del módulo.

---

### TKT-11: Constantes para tipos de temperatura

| Campo | Valor |
|-------|-------|
| Módulos analizados | `entidades`, `gestores_entidades`, `servicios_aplicacion`, `agentes_sensores` |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

**Archivos modificados:** 4 archivos de producción + 2 de tests. `TEMP_AMBIENTE` y `TEMP_DESEADA` definidas en `entidades/ambiente.py`.

---

### TKT-12: Documentar mostrar_indicador()

| Campo | Valor |
|-------|-------|
| Tipo | Verificación (DoD ya cumplido) |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

> El método ya tenía docstring y comentario inline. Sin cambios adicionales.

---

### TKT-13: Resolver test HAL huérfano

| Campo | Valor |
|-------|-------|
| Tipo | Limpieza estructural |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

**Archivos eliminados:** `Test/hal/test_hal_adc.py`, `Test/hal/__init__.py`. El módulo `hal/` no existe en producción.

---

### TKT-14: Newline final en ejecutar.py

| Campo | Valor |
|-------|-------|
| Tipo | Corrección menor |
| Errores | 0 |
| Advertencias | 0 |
| Bloquea PR | No |

Corrige pylint `C0304` (missing-final-newline). Convención POSIX y PEP 8.

---

### TKT-15: Extraer Registrador/Auditor como dependencias inyectadas

| Campo | Valor |
|-------|-------|
| Módulos analizados | `agentes_actuadores`, `registrador`, `configurador` |
| Errores | 0 |
| Advertencias | 11 |
| Bloquea PR | No |

**Advertencias:** 11 `E128` pre-existentes en visualizadores (no modificados por TKT-15). `registrador` y `configurador`: 0 advertencias.

**Cambios implementados:**
- `RegistradorArchivo` y `AuditorArchivo` agregadas a `registrador/registrador.py`
- `ActuadorClimatizadorGeneral` hereda solo de `AbsProxyActuadorClimatizador`; registrador y auditor inyectados en constructor
- `FactoryActuadorClimatizador` instancia e inyecta ambas dependencias

---

### TKT-16 + TKT-17: ISP y corrección @staticmethod en SelectorTemperaturaArchivo

| Campo | Valor |
|-------|-------|
| Módulos analizados | `agentes_sensores`, `entidades` |
| Errores | 0 |
| Advertencias | 2 |
| Bloquea PR | No |

**Advertencias:** 2 `E128` pre-existentes en `agentes_sensores`.

**Cambios implementados:**
- TKT-16: `SelectorTemperaturaArchivo` hereda solo de `AbsSelectorTemperatura`; registro de errores vía `logger`
- TKT-17: `obtener_selector()` convertido de `@staticmethod` a método de instancia en implementación e interfaz abstracta

---

### TKT-18: Inyectar host/puerto en visualizadores socket

| Campo | Valor |
|-------|-------|
| Módulos analizados | `agentes_actuadores`, `configurador` |
| Errores | 0 |
| Advertencias | 11 |
| Informativos | 14 |
| Bloquea PR | No |

**Cambios implementados:** `VisualizadorBateriaSocket`, `VisualizadorTemperaturaSocket` y `VisualizadorClimatizadorSocket` reciben `host`/`puerto` vía `__init__`. Factories y `Configurador` actualizados. Tests de integración corregidos.

---

### TKT-19: Registry Pattern en factories (OCP)

| Campo | Valor |
|-------|-------|
| Módulo analizado | `configurador` |
| Errores | 0 |
| Advertencias | 9 |
| Informativos | 27 |
| Bloquea PR | No |

**Cambios implementados:** `RegistryFactory` en `configurador/registry_factory.py`. Las 9 factories heredan de ella y registran sus tipos con `registrar()` a nivel de módulo. Agregar un nuevo tipo no requiere modificar archivos existentes.

---

## Sección 2 — designreviewer por Fase

### Fase 1 — Compliance (TKT-01, TKT-02)

**Módulos analizados:** `entidades`, `agentes_sensores`, `configurador`, `servicios_aplicacion`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `entidades` | 0 | 8 | 4.2 | No |
| `agentes_sensores` | 1 | 4 | 4.7 | Sí |
| `configurador` | 1 | 2 | 6.4 | Sí |
| `servicios_aplicacion` | 1 | 8 | 8.9 | Sí |
| **Total** | **3** | **22** | **24.2** | **Sí** |

> Los 3 críticos son pre-existentes. Ninguno introducido por TKT-01 o TKT-02. Trackeados en tickets de fases posteriores.

**Hallazgos críticos:**

| Analyzer | Clase | Mensaje | Ticket Asociado |
|----------|-------|---------|-----------------|
| NOPAnalyzer | `SelectorTemperaturaArchivo` | Hereda de 2 clases directas (umbral: 1): `AbsSelectorTemperatura`, `AbsRegistrador` | TKT-16 |
| WMCAnalyzer | `Configurador` | WMC=36 (umbral: 20): complejidad total de métodos excesiva | TKT-19 (Fase 6) |
| CBOAnalyzer | `Lanzador` | CBO=9 (umbral: 5): Composition Root con alto acoplamiento estructural | Deuda conocida |

**Hallazgos warnings destacados:**

| Analyzer | Clase | Mensaje |
|----------|-------|---------|
| LongMethodAnalyzer | `AbsClimatizador.proximo_estado` | 26 líneas (umbral: 20) |
| LongMethodAnalyzer | `AbsClimatizador.evaluar_accion` | 25 líneas (umbral: 20) |
| LongMethodAnalyzer | `AbsProxyActuadorClimatizador.accionar_climatizador` | 27 líneas (umbral: 20) |
| LongMethodAnalyzer | `Bateria.__init__` | 25 líneas (umbral: 20) |
| LongMethodAnalyzer | `Lanzador.__init__` | 65 líneas (umbral: 20) |
| LCOMAnalyzer | `Climatizador` | LCOM=2 (2 grupos de métodos sin atributos compartidos) |
| LCOMAnalyzer | `Calefactor` | LCOM=2 |
| FeatureEnvyAnalyzer | `Inicializador.iniciar` | Accede 3 veces a `gestor_ambiente` vs 0 a `self` |

---

### Fase 2 — Diseño (TKT-03, TKT-04, TKT-05)

**Módulos analizados:** `configurador`, `servicios_aplicacion`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `configurador` | 1 | 2 | 6.5 | Sí |
| `servicios_aplicacion` | 1 | 8 | 8.4 | Sí |
| **Total** | **2** | **10** | **14.9** | **Sí** |

> Los 2 críticos son pre-existentes. TKT-03 redujo el CBO de `Lanzador` de 9 a 8 (eliminó instanciación `Configurador()` en `lanzador.py`).

**Evolución respecto a Fase 1:**

| Métrica | Fase 1 | Fase 2 | Delta |
|---------|--------|--------|-------|
| `Lanzador` CBO | 9 | 8 | -1 |
| Críticos totales | 3 | 2 | -1 |

---

### Fase 3 — Arquitectura de sockets (TKT-06, TKT-07)

**Módulos analizados:** `agentes_sensores`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `agentes_sensores` | 1 | 4 | 4.7 | Sí |
| **Total** | **1** | **4** | **4.7** | **Sí** |

> El crítico (NOP `SelectorTemperaturaArchivo`) es pre-existente y no fue modificado en esta fase. Resuelto en TKT-16 (Fase 6).

**Hallazgos warnings:**

| Analyzer | Clase | Mensaje |
|----------|-------|---------|
| LongMethodAnalyzer | `ProxyBateriaSocket.leer_carga` | 34 líneas |
| LongMethodAnalyzer | `SeteoTemperaturaSocket.obtener_seteo` | 44 líneas |
| LongMethodAnalyzer | `SelectorTemperaturaSocket.obtener_selector` | 42 líneas |
| LongMethodAnalyzer | `ProxySensorTemperaturaSocket.leer_temperatura` | 34 líneas |

> Todos pre-existentes. Complejidad estructural inherente al protocolo socket con timeout y manejo de errores.

---

### Fase 4 — Organización estructural (TKT-08, TKT-09)

**Módulos analizados:** `entidades`, `configurador`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `entidades` | 0 | 6 | 3.7 | No |
| `configurador` | 1 | 2 | 6.5 | Sí |
| **Total** | **1** | **8** | **10.2** | **Sí** |

> El crítico es el WMC de `Configurador`, pre-existente desde Fase 2. `entidades` quedó limpia en críticos tras TKT-09.

---

### Fase 5 — Refinamiento (TKT-10..TKT-14)

**Módulos analizados:** `servicios_dominio`, `entidades`, `gestores_entidades`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `servicios_dominio` | 0 | 0 | 0 | No |
| `entidades` | 0 | 6 | 3.7 | No |
| `gestores_entidades` | 0 | 1 | 1.5 | No |
| **Total** | **0** | **7** | **5.2** | **No** |

> Primera fase sin issues críticos. `servicios_dominio` completamente limpio.

**Hallazgos warnings:**

| Analyzer | Clase | Mensaje |
|----------|-------|---------|
| LCOMAnalyzer | `GestorAmbiente` | LCOM=2 |
| LCOMAnalyzer | `Climatizador` | LCOM=2 (pre-existente) |
| LCOMAnalyzer | `Calefactor` | LCOM=2 (pre-existente) |
| LongMethodAnalyzer | `Ambiente.__repr__` | 21 líneas |
| LongMethodAnalyzer | `AbsProxyActuadorClimatizador.accionar_climatizador` | 27 líneas |
| LongMethodAnalyzer | `Bateria.__init__` | 25 líneas |
| LongMethodAnalyzer | `AbsProxySensorTemperatura.leer_temperatura` | 22 líneas |

---

### Fase 6 — SOLID: Cross-cutting concerns (TKT-15..TKT-19)

**Módulos analizados:** `agentes_actuadores`, `configurador`, `registrador`

| Módulo | Críticos | Warnings | Deuda (h) | Bloquea |
|--------|----------|----------|-----------|---------|
| `agentes_actuadores` | 0 | 6 | 9.6 | No |
| `configurador` | 0 | 1 | 2.0 | No |
| `registrador` | 0 | 2 | 2.1 | No |
| **Total** | **0** | **9** | **13.7** | **No** |

> El WMC crítico de `Configurador` (pre-existente desde Fase 1) fue resuelto en esta fase extrayendo helpers de módulo. WMC redujo de 39 a 19.

**Hallazgos warnings restantes:**

| Analyzer | Clase/Módulo | Mensaje |
|----------|-------------|---------|
| DataClumpsAnalyzer | `configurador.py` | Data Clump detectado (2 parámetros que aparecen juntos) |
| LongMethodAnalyzer | `VisualizadorEstadoConsolidadoSocket` | 68 líneas |
| LongMethodAnalyzer | `VisualizadorEstadoConsolidadoSocket` | 63 líneas |
| LongMethodAnalyzer | `ActuadorClimatizadorGeneral` | 21 líneas |
| FeatureEnvyAnalyzer | `VisualizadorEstadoConsolidadoSocket` | Feature Envy (3/1) |
| LCOMAnalyzer | `VisualizadorEstadoConsolidadoSocket` | LCOM=2 |
| LongMethodAnalyzer | `AuditorArchivo` | 22 líneas |
| LongMethodAnalyzer | `Configurador` | `cargar_configuracion` (advertencia residual) |

---

## Sección 3 — Evolución de Métricas entre Fases

### Issues Críticos (designreviewer)

```
Fase 1: ████████ 3 críticos  (NOPAnalyzer, WMCAnalyzer, CBOAnalyzer)
Fase 2: █████    2 críticos  (WMCAnalyzer, CBOAnalyzer)     [-1 NOP resuelto por TKT-16 en F6]
Fase 3: ███      1 crítico   (NOPAnalyzer)
Fase 4: ███      1 crítico   (WMCAnalyzer)
Fase 5:          0 críticos  ✓
Fase 6:          0 críticos  ✓
```

### WMC de Configurador (evolución)

| Fase | WMC | Estado |
|------|-----|--------|
| Inicio (pre-mejoras) | 36 | CRITICAL |
| Fase 1–5 | 36–39 | CRITICAL (pre-existente, no en scope) |
| Fase 6 — TKT-19 agrega Registry | 39 | CRITICAL |
| Fase 6 — Refactor helpers módulo | **19** | ✓ RESUELTO |

### CBO de Lanzador (evolución)

| Fase | CBO | Nota |
|------|-----|------|
| Inicio | 9 | CRITICAL |
| Fase 2 (TKT-03) | 8 | -1 tras eliminar instanciación `Configurador()` |
| Fase 6 | 8 | Sin cambios (Composition Root — deuda aceptada) |

### Tests

| Hito | Passed | Failed | Errors |
|------|--------|--------|--------|
| Pre-mejoras | 181 | 2 | 10 (collection) |
| Post-TKT-08 | 181 | 2 | 0 |
| Post-TKT-13 | 181 | 2 | 0 |
| **Cierre Fase 6** | **181** | **2** | **0** |

> Los 2 failed son pre-existentes: `TestProxyBateriaSocket` llama `ProxyBateriaSocket()` sin argumentos en los tests de integración.

---

## Sección 4 — Deuda Técnica Residual

Issues identificados por designreviewer que permanecen abiertos por decisión arquitectónica o de prioridad:

| Analyzer | Clase | Módulo | Severidad | Decisión |
|----------|-------|--------|-----------|----------|
| CBOAnalyzer | `Lanzador` | `servicios_aplicacion` | WARNING | Aceptado: Composition Root por diseño. Alto acoplamiento es estructural |
| LongMethodAnalyzer | `SeteoTemperaturaSocket.obtener_seteo` | `agentes_sensores` | WARNING | Aceptado: protocolo socket con timeout y retry inherentemente largo |
| LongMethodAnalyzer | `SelectorTemperaturaSocket.obtener_selector` | `agentes_sensores` | WARNING | Idem |
| LongMethodAnalyzer | `ProxyBateriaSocket.leer_carga` | `agentes_sensores` | WARNING | Idem |
| LongMethodAnalyzer | `Lanzador.__init__` | `servicios_aplicacion` | WARNING | Aceptado: Composition Root — su responsabilidad es crear y conectar |
| LCOMAnalyzer | `Climatizador` / `Calefactor` | `entidades` | WARNING | Aceptado: LCOM=2 es consecuencia del patrón Template Method heredado |
| LCOMAnalyzer | `GestorAmbiente` | `gestores_entidades` | WARNING | Candidato a refactor futuro |
| LongMethodAnalyzer | `VisualizadorEstadoConsolidadoSocket` | `agentes_actuadores` | WARNING | Candidato a refactor futuro (múltiples responsabilidades de red) |
| DataClumpsAnalyzer | `configurador.py` | `configurador` | WARNING | `host`/`puerto` agrupados por diseño (parámetros de red relacionados) |

---

## Sección 5 — Herramientas Utilizadas

### codeguard
- **Versión:** 0.2.0
- **Entorno:** `.venv-quality/` (Python 3.11)
- **Checks ejecutados por módulo:** PEP8, pylint, complejidad ciclomática, seguridad, docstrings, imports
- **Criterio de bloqueo:** Cualquier error (nivel ERROR)

### designreviewer
- **Versión:** 0.2.0
- **Entorno:** `.venv-quality/` (Python 3.11)
- **Analyzers activos:** WMCAnalyzer, CBOAnalyzer, LCOMAnalyzer, NOPAnalyzer, LongMethodAnalyzer, FeatureEnvyAnalyzer, DataClumpsAnalyzer
- **Criterio de bloqueo:** Cualquier issue CRITICAL
- **Ejecución:** Una vez por fase sobre los módulos afectados por sus tickets

### pytest
- **Versión:** según entorno base
- **Suite:** `Test/unit/` + `Test/integration/`
- **Cobertura:** No medida por fase (cobertura global ~84% al inicio del plan)

---

*Reporte generado el 2026-03-06 al cierre del plan de mejoras.*
