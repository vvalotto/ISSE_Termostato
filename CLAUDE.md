# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Descripción del Proyecto

Sistema de control de termostato inteligente desarrollado como proyecto educativo. Implementa **Clean Architecture** con Python 3.5+ (compatible con Raspberry Pi OS Lite), patrones GRASP/GoF y principios SOLID.

## Comandos Esenciales

```bash
# Ejecutar el sistema
python ejecutar.py

# Lanzar simuladores externos (macOS)
cd actores_externos && ./lanzar_simuladores.sh

# Tests
pytest Test/ -v
pytest Test/unit/ -v
pytest Test/integration/ -v
pytest Test/ --cov=. --cov-report=html

# Un test específico
pytest Test/unit/entidades/test_bateria.py -v

# Instalar dependencias de desarrollo
pip install -e ".[dev]"
```

No hay dependencias externas en runtime (solo stdlib). `requests` se usa únicamente en los visualizadores de tipo `api`. Dependencias de dev: `pytest`, `pytest-cov`, `radon`, `pylint`.

## Arquitectura Clean Architecture

Las dependencias apuntan **solo hacia adentro**. Las capas internas no conocen las externas.

```
actores_externos/          ← Frameworks & Drivers (simuladores, displays)
agentes_sensores/          ← Interface Adapters: Proxies de entrada
agentes_actuadores/        ← Interface Adapters: Visualizadores de salida
gestores_entidades/        ← Use Cases: Orquestación
servicios_aplicacion/      ← Use Cases: Coordinación de la app
  └── lanzador.py          ← Composition Root (inyección de dependencias)
entidades/                 ← Entities: Lógica de dominio pura + interfaces ABC
servicios_dominio/         ← Entities: Reglas de negocio (histeresis)
configurador/              ← Abstract Factory (9 factories + termostato.json)
registrador/               ← Auditoría y logging
```

**`servicios_aplicacion/lanzador.py`** es el Composition Root: crea todas las entidades, adaptadores y gestores, inyecta dependencias, y lanza el operador principal.

**`configurador/configurador.py`** carga `configurador/termostato.json` y provee métodos estáticos factory para crear todos los componentes según la configuración.

## Configuración: `configurador/termostato.json`

```json
{
  "proxy_bateria": "archivo | socket",
  "proxy_sensor_temperatura": "archivo | socket",
  "climatizador": "climatizador | calefactor",
  "actuador_climatizador": "general",
  "selector_temperatura": "archivo | socket",
  "seteo_temperatura": "archivo | socket",
  "visualizador_bateria": "consola | socket | api",
  "visualizador_temperatura": "consola | socket | api",
  "visualizador_climatizador": "consola | socket | api",
  "bateria": {
    "carga_maxima": 5.0,
    "umbral_carga_baja": 0.95
  },
  "ambiente": {
    "histeresis": 2.0,
    "temperatura_inicial": 24.0,
    "incremento_ajuste": 1.0
  },
  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": {
      "bateria": 11000,
      "temperatura": 12000,
      "seteo_temperatura": 13000,
      "selector_temperatura": 14000
    },
    "api_url": "https://..."
  }
}
```

Puertos TCP de referencia: `11000` batería, `12000` temperatura, `13000` seteo, `14000` selector, `14001` display consolidado UX, `14002` display climatizador.

## Convenciones de Código

- **NO usar f-strings** → usar `.format()` (Python 3.5 no soporta f-strings)
- Interfaces abstractas usan `metaclass=ABCMeta` (no herencia de `ABC`):
  ```python
  from abc import ABCMeta, abstractmethod
  class AbsProxySensor(metaclass=ABCMeta):
      @abstractmethod
      def leer_temperatura(self):
          pass
  ```
- Docstrings en español; `snake_case` funciones/variables; `PascalCase` clases
- Nombres de archivos: `abs_*.py`, `factory_*.py`, `proxy_*.py`, `visualizador_*.py`

## Reglas de Arquitectura

**NUNCA** poner lógica de dominio fuera de `entidades/` y `servicios_dominio/`:
- Proxies (`agentes_sensores/`) → solo lectura/escritura de fuentes externas
- Visualizadores (`agentes_actuadores/`) → solo presentación de datos
- Gestores (`gestores_entidades/`) → solo orquestación entre componentes

Lógica de histeresis: `servicios_dominio/controlador_climatizador.py` (constante `histeresis` viene de configuración).

## Extender el Sistema

Para agregar un nuevo visualizador/proxy:
1. Crear clase en `agentes_actuadores/` o `agentes_sensores/` implementando la interfaz abstracta de `entidades/`
2. Crear `factory_*.py` en `configurador/`
3. Agregar opción en `configurador/termostato.json`
4. Registrar la opción en `configurador/configurador.py`

## Tests

Estructura en `Test/`:
- `unit/entidades/` — tests de entidades de dominio
- `unit/servicios_dominio/` — tests de lógica de negocio
- `unit/configurador/` — tests de factories y configuración
- `integration/gestores/` — tests de gestores con dependencias mockeadas
- `integration/flujos/` — tests de ciclos completos de climatización
- `integration/adaptadores/` — tests de proxies y visualizadores
- `conftest.py` en `unit/` e `integration/` con fixtures compartidos (incluyendo `setup_configurador` con `autouse=True`)

## Herramientas de Calidad (software_limpio)

Entorno dedicado: `.venv-quality/` (Python 3.11). Activar antes de usar.

```bash
source .venv-quality/bin/activate
```

### codeguard — por ticket (Fase 7 de /implement-us)
Análisis estático pre-commit. Se ejecuta sobre los módulos afectados por el ticket.

```bash
codeguard <modulo>          # ej: codeguard configurador
codeguard <modulo> --fix    # con corrección automática
```

**Reporte obligatorio:** el resultado de cada ejecución de quality gates debe persistirse en disco, independientemente de la herramienta usada. Guardar en `quality/reports/TKT-XX-quality.json` con el siguiente formato mínimo:

```json
{
  "us_id": "TKT-01",
  "fecha": "YYYY-MM-DD",
  "herramienta": "codeguard",
  "modulos": ["configurador"],
  "errores": 0,
  "advertencias": 0,
  "informativos": 33,
  "hallazgos": []
}
```

Si la herramienta soporta salida JSON (`codeguard --format json`), usarla. Si no, generar el archivo manualmente con los datos del output. Crear el directorio `quality/reports/` si no existe.

Ref: vvalotto/claude-dev-kit#36

### designreviewer — por PR de fase
Gate obligatorio antes de crear el PR de cierre de cada fase de mejoras.
Analiza las capas afectadas por los tickets de esa fase.

```bash
designreviewer <modulo>     # ej: designreviewer entidades agentes_sensores
```

El PR **no se crea** hasta que designreviewer no reporte 0 issues críticos.

## Gestión de Tickets de Mejora

Los tickets del plan de mejoras tienen correspondencia directa con **GitHub Issues**:

- `docs/Plan/MEJORAS.md` — descripción detallada de cada ticket
- `docs/Plan/BITACORA.md` — estado actual de cada ticket (columna `#Issue` con el número de issue)
- GitHub Issues `#17`–`#35` — fuente oficial de estado; cerrar el issue al completar cada ticket

**Al completar un ticket:**
1. Actualizar `BITACORA.md`: estado → `Hecho`
2. Cerrar el GitHub Issue con `gh issue close <N> --comment "<resumen>"`
3. Hacer commit referenciando el issue (`Closes #N`)

## Workflow de PR por Fase de Mejoras

1. Completar todos los tickets de la fase (cada uno con su `/implement-us`)
2. Ejecutar `designreviewer` sobre las capas afectadas
3. Resolver issues críticos si los hay
4. Crear PR con título `mejora/fase-N-descripcion` y referenciar los issues cerrados
5. Actualizar `docs/Plan/BITACORA.md` con estado `Hecho` para cada ticket

## Archivos de Runtime (NO commitear)

Generados durante ejecución, en `.gitignore`: `bateria`, `climatizador`, `temperatura`, `tipo_temperatura`, `registro_auditoria`, `termostato.log`.
