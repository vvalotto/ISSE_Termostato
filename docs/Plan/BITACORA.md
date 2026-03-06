# Bitácora de Tickets — ISSE Termostato

Archivo de trabajo para seguimiento del progreso de mejoras.
El sistema de tracking oficial es **GitHub Issues** (referenciado en columna `#Issue`).

**Actualización:** 2026-03-05

---

## Estado general

| Fase | Descripción | Tickets | Completados |
|------|-------------|---------|-------------|
| 1 | Compliance: Reglas del proyecto y arquitectura | TKT-01, TKT-02 | 2/2 |
| 2 | Diseño: Coherencia y convenciones | TKT-03, TKT-04, TKT-05 | 2/3 |
| 3 | Arquitectura de sockets | TKT-06, TKT-07 | 0/2 |
| 4 | Organización estructural | TKT-08, TKT-09 | 0/2 |
| 5 | Refinamiento | TKT-10, TKT-11, TKT-12, TKT-13, TKT-14 | 0/5 |
| 6 | SOLID: Cross-cutting concerns | TKT-15, TKT-16, TKT-17, TKT-18, TKT-19 | 0/5 |

---

## Tabla de tickets

| Ticket | Título | Fase | Prioridad | Impacto | Esfuerzo | Depende de | #Issue | Estado |
|--------|--------|------|-----------|---------|----------|------------|--------|--------|
| TKT-01 | Eliminar f-strings en configurador | 1 | 1 | Alto | Bajo | — | #17 | Hecho |
| TKT-02 | Mover interfaces AbsSeteo/AbsSelector a entidades/ | 1 | 1 | Alto | Medio | — | #18 | Hecho |
| TKT-03 | Unificar uso de Configurador como clase estática | 2 | 2 | Alto | Bajo | — | #19 | Hecho |
| TKT-04 | Reemplazar wildcard imports en ejecutar.py | 2 | 2 | Medio | Bajo | TKT-03 | #20 | Hecho |
| TKT-05 | Reemplazar print() por logging en _validar_configuracion | 2 | 2 | Medio | Bajo | — | #21 | Backlog |
| TKT-06 | Unificar ciclo de vida de sockets | 3 | 3 | Medio | Medio | Decisión diseño | #22 | Backlog |
| TKT-07 | Context manager para sockets persistentes | 3 | 3 | Medio | Medio | TKT-06 | #23 | Backlog |
| TKT-08 | Consolidar estructura de tests en subdirectorios | 4 | 2 | Medio | Medio | Fases 1 y 2 | #24 | Backlog |
| TKT-09 | Separar AbsClimatizador en abs_climatizador.py | 4 | 3 | Medio | Bajo | — | #25 | Backlog |
| TKT-10 | ControladorTemperatura como función de módulo | 5 | 3 | Medio | Bajo | — | #26 | Backlog |
| TKT-11 | Constantes para tipos de temperatura | 5 | 3 | Medio | Bajo | — | #27 | Backlog |
| TKT-12 | Documentar o implementar mostrar_indicador() | 5 | 4 | Bajo | Bajo | — | #28 | Backlog |
| TKT-13 | Resolver test HAL huérfano | 5 | 4 | Bajo | Bajo | — | #29 | Backlog |
| TKT-14 | Newline final en ejecutar.py | 5 | 4 | Bajo | Bajo | TKT-04 | #30 | Backlog |
| TKT-15 | Extraer Registrador/Auditor como dependencias inyectadas | 6 | 2 | Alto | Medio | — | #31 | Backlog |
| TKT-16 | Quitar herencia de AbsRegistrador en SelectorTemperaturaArchivo | 6 | 3 | Medio | Bajo | TKT-15 | #32 | Backlog |
| TKT-17 | Corregir @staticmethod en SelectorTemperaturaArchivo | 6 | 3 | Medio | Bajo | TKT-16 | #33 | Backlog |
| TKT-18 | Inyectar host/puerto en visualizadores socket | 6 | 3 | Medio | Bajo | — | #34 | Backlog |
| TKT-19 | Registry Pattern en factories (OCP) | 6 | 4 | Bajo | Alto | — | #35 | Backlog |

**Estados posibles:** `Backlog` → `Listo` → `En curso` → `En revisión` → `Hecho`

---

## Registro de actividad

### 2026-03-05
- Creación de la bitácora.
- 19 GitHub Issues creados (#17 al #35).
- 12 etiquetas creadas en GitHub (fase-1..6, impacto-alto/medio/bajo, esfuerzo-bajo/medio/alto).
- Todos los tickets en estado `Backlog`.

### 2026-03-06
- TKT-01: Eliminar f-strings en configurador — **Hecho**. 3 f-strings reemplazados por `.format()` en `configurador/configurador.py`. codeguard: 0 errores, 0 advertencias.
- TKT-02: Mover interfaces AbsSeteo/AbsSelector a entidades/ — **Hecho**. Interfaces movidas a `entidades/`, imports actualizados en proxies. `agentes_sensores/` ya no depende de `servicios_aplicacion/`. codeguard: 0 errores.
- TKT-03: Unificar uso de Configurador como clase estática — **Hecho**. Eliminadas 4 instanciaciones `Configurador()` en `ejecutar.py`, `lanzador.py` y test. codeguard: 0 errores.
- TKT-04: Reemplazar wildcard imports en ejecutar.py — **Hecho**. Imports explícitos: `Lanzador` y `Configurador`. codeguard: 0 errores.
