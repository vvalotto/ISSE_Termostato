# Bitácora de Tickets — ISSE Termostato

Archivo de trabajo para seguimiento del progreso de mejoras.
El sistema de tracking oficial es **GitHub Issues** (referenciado en columna `#Issue`).

**Actualización:** 2026-03-05

---

## Estado general

| Fase | Descripción | Tickets | Completados |
|------|-------------|---------|-------------|
| 1 | Compliance: Reglas del proyecto y arquitectura | TKT-01, TKT-02 | 0/2 |
| 2 | Diseño: Coherencia y convenciones | TKT-03, TKT-04, TKT-05 | 0/3 |
| 3 | Arquitectura de sockets | TKT-06, TKT-07 | 0/2 |
| 4 | Organización estructural | TKT-08, TKT-09 | 0/2 |
| 5 | Refinamiento | TKT-10, TKT-11, TKT-12, TKT-13, TKT-14 | 0/5 |
| 6 | SOLID: Cross-cutting concerns | TKT-15, TKT-16, TKT-17, TKT-18, TKT-19 | 0/5 |

---

## Tabla de tickets

| Ticket | Título | Fase | Prioridad | Impacto | Esfuerzo | Depende de | #Issue | Estado |
|--------|--------|------|-----------|---------|----------|------------|--------|--------|
| TKT-01 | Eliminar f-strings en configurador | 1 | 1 | Alto | Bajo | — | — | Backlog |
| TKT-02 | Mover interfaces AbsSeteo/AbsSelector a entidades/ | 1 | 1 | Alto | Medio | — | — | Backlog |
| TKT-03 | Unificar uso de Configurador como clase estática | 2 | 2 | Alto | Bajo | — | — | Backlog |
| TKT-04 | Reemplazar wildcard imports en ejecutar.py | 2 | 2 | Medio | Bajo | TKT-03 | — | Backlog |
| TKT-05 | Reemplazar print() por logging en _validar_configuracion | 2 | 2 | Medio | Bajo | — | — | Backlog |
| TKT-06 | Unificar ciclo de vida de sockets | 3 | 3 | Medio | Medio | Decisión diseño | — | Backlog |
| TKT-07 | Context manager para sockets persistentes | 3 | 3 | Medio | Medio | TKT-06 | — | Backlog |
| TKT-08 | Consolidar estructura de tests en subdirectorios | 4 | 2 | Medio | Medio | Fases 1 y 2 | — | Backlog |
| TKT-09 | Separar AbsClimatizador en abs_climatizador.py | 4 | 3 | Medio | Bajo | — | — | Backlog |
| TKT-10 | ControladorTemperatura como función de módulo | 5 | 3 | Medio | Bajo | — | — | Backlog |
| TKT-11 | Constantes para tipos de temperatura | 5 | 3 | Medio | Bajo | — | — | Backlog |
| TKT-12 | Documentar o implementar mostrar_indicador() | 5 | 4 | Bajo | Bajo | — | — | Backlog |
| TKT-13 | Resolver test HAL huérfano | 5 | 4 | Bajo | Bajo | — | — | Backlog |
| TKT-14 | Newline final en ejecutar.py | 5 | 4 | Bajo | Bajo | TKT-04 | — | Backlog |
| TKT-15 | Extraer Registrador/Auditor como dependencias inyectadas | 6 | 2 | Alto | Medio | — | — | Backlog |
| TKT-16 | Quitar herencia de AbsRegistrador en SelectorTemperaturaArchivo | 6 | 3 | Medio | Bajo | TKT-15 | — | Backlog |
| TKT-17 | Corregir @staticmethod en SelectorTemperaturaArchivo | 6 | 3 | Medio | Bajo | TKT-16 | — | Backlog |
| TKT-18 | Inyectar host/puerto en visualizadores socket | 6 | 3 | Medio | Bajo | — | — | Backlog |
| TKT-19 | Registry Pattern en factories (OCP) | 6 | 4 | Bajo | Alto | — | — | Backlog |

**Estados posibles:** `Backlog` → `Listo` → `En curso` → `En revisión` → `Hecho`

---

## Registro de actividad

### 2026-03-05
- Creación de la bitácora.
- Todos los tickets en estado `Backlog`.
- Próximo paso: crear GitHub Issues y actualizar columna `#Issue`.
