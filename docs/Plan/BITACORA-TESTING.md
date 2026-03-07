# Bitácora de Testing — ISSE Termostato

Seguimiento del plan de cobertura definido en `PLAN-TESTING.md`.

**Cobertura inicial:** 63% | **Objetivo:** ≥ 85%
**Actualización:** 2026-03-07

---

## Estado general

| Fase | Descripción | Tareas | Completadas | Cobertura estimada |
|------|-------------|--------|-------------|--------------------|
| Fix  | Corregir tests rotos (previo a todo) | 1 | 0/1 | — |
| A    | Regresión inmediata (código modificado sin tests) | 4 | 0/4 | 63% → 72% |
| B    | Cobertura de adaptadores | 3 | 0/3 | 72% → 80% |
| C    | Completar cobertura de configurador | 1 | 0/1 | 80% → 83% |
| D    | Servicios de aplicación (cobertura básica) | 4 | 0/4 | 83% → 87% |

---

## Tabla de tareas

| ID    | Descripción | Archivo de test | Tests | Cobertura objetivo | Estado |
|-------|-------------|-----------------|-------|--------------------|--------|
| Fix-1 | Corregir tests rotos de ProxyBateriaSocket (PRX-FIX-001, 002) | `Test/integration/adaptadores/test_proxies.py` | 2 fix | — | Pendiente |
| A-1   | Tests para `registrador/registrador.py` (REG-001..005) | `Test/unit/registrador/test_registrador.py` | 5 | 50% → 100% | Pendiente |
| A-2   | Tests para `agentes_actuadores/actuador_climatizador.py` (ACT-001..006) | `Test/unit/agentes_actuadores/test_actuador_climatizador.py` | 6 | 29% → 90% | Pendiente |
| A-3   | Tests para `agentes_sensores/proxy_selector_temperatura.py` (SEL-001..007) | `Test/integration/adaptadores/test_selector_temperatura.py` | 7 | 17% → 85% | Pendiente |
| A-4   | Tests para `configurador/registry_factory.py` + factories (REG-F-001..005, FAC-001..013) | `Test/unit/configurador/test_registry_factory.py` + `test_factories.py` | 18 | 0%/78% → 90% | Pendiente |
| B-1   | Tests visualizadores batería y climatizador (VIS-B-001..006, VIS-C-001..005) | `Test/integration/adaptadores/test_visualizadores.py` | 11 | 37-42% → 90% | Pendiente |
| B-2   | Tests nuevos proxies seteo y batería socket (PRX-SET-001..005, PRX-SNS-001, PRX-BAT-001) | `Test/integration/adaptadores/test_proxies.py` | 7 | 17-41% → 80% | Pendiente |
| B-3   | Tests para `VisualizadorEstadoConsolidadoSocket` (VEC-001..009) | `Test/unit/agentes_actuadores/test_visualizador_estado_consolidado.py` | 9 | 0% → 80% | Pendiente |
| C-1   | Completar cobertura de `configurador/configurador.py` (CFG-001..010) | `Test/unit/configurador/test_configurador.py` | 10 | 78% → 92% | Pendiente |
| D-1   | Tests para `servicios_aplicacion/inicializador.py` (INI-001..005) | `Test/unit/servicios_aplicacion/test_inicializador.py` | 5 | 0% → 80% | Pendiente |
| D-2   | Tests para `servicios_aplicacion/selector_entrada.py` (SEL-ENT-001..004) | `Test/unit/servicios_aplicacion/test_selector_entrada.py` | 4 | 0% → 75% | Pendiente |
| D-3   | Tests para `servicios_aplicacion/presentador.py` (PRE-001..003) | `Test/unit/servicios_aplicacion/test_presentador.py` | 3 | 0% → 70% | Pendiente |
| D-4   | Tests básicos para `operador_secuencial.py` (OPR-001..002) | `Test/unit/servicios_aplicacion/test_operador_secuencial.py` | 2 | 0% → básico | Pendiente |

**Total estimado:** ~87 tests nuevos

**Orden de implementación:** Fix-1 → A (A-1..A-4) → B (B-1..B-3) → C → D

**Estados posibles:** `Pendiente` → `En curso` → `Hecho`

---

## Registro de actividad

### 2026-03-07
- Creación de la bitácora. 13 tareas en estado `Pendiente`.

