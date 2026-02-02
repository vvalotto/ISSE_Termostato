# CLAUDE.md - Guía para Claude Code

Este archivo proporciona contexto y guías para trabajar eficientemente con el proyecto ISSE_Termostato usando Claude Code.

## 📋 Descripción del Proyecto

**ISSE_Termostato** es un sistema de control de termostato inteligente desarrollado como proyecto educativo para demostrar principios de arquitectura de software y patrones de diseño. Implementa **Clean Architecture** con separación estricta de capas y uso exhaustivo de patrones GRASP, GoF y principios SOLID.

### Características Principales
- Clean Architecture con 4 capas bien definidas
- Sistema de logging centralizado
- Simulación distribuida (Raspberry Pi + MacBook via TCP sockets)
- API REST integrada (Google Cloud Run)
- Visualizador consolidado JSON para UX
- Python 3.5+ (compatible con Raspberry Pi OS Lite)
- Sistema de auditoría y registro de eventos

## 🏗️ Arquitectura del Proyecto

### Clean Architecture - Capas

El proyecto sigue Clean Architecture de Robert C. Martin con dependencias apuntando hacia el centro:

```
┌─────────────────────────────────────────────────────────────┐
│ FRAMEWORKS & DRIVERS (actores_externos/)                    │
│   - Simuladores de entrada (temperatura, batería, etc.)     │
│   - Displays de salida (carteles vía socket)                │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ INTERFACE ADAPTERS                                    │   │
│ │   agentes_sensores/ - Proxies (Archivo, Socket)      │   │
│ │   agentes_actuadores/ - Visualizadores (Consola,     │   │
│ │                         Socket, API)                  │   │
│ │ ┌─────────────────────────────────────────────────┐   │   │
│ │ │ USE CASES (Application)                         │   │   │
│ │ │   gestores_entidades/ - Gestores de dominio    │   │   │
│ │ │   servicios_aplicacion/ - Lanzador, Operador   │   │   │
│ │ │ ┌───────────────────────────────────────────┐   │   │   │
│ │ │ │ ENTITIES (Domain)                         │   │   │   │
│ │ │ │   entidades/ - Ambiente, Bateria,         │   │   │   │
│ │ │ │                Climatizador               │   │   │   │
│ │ │ │   servicios_dominio/ - Lógica de negocio │   │   │   │
│ │ │ └───────────────────────────────────────────┘   │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Regla fundamental:** Las dependencias SOLO apuntan hacia adentro. Las capas internas NO conocen las externas.

### Estructura de Carpetas

```
ISSE_Termostato/
├── entidades/              # Dominio - Lógica de negocio pura
│   ├── abs_*.py           # Interfaces abstractas (ABC)
│   ├── ambiente.py        # Entidad de temperatura
│   ├── bateria.py         # Entidad de batería
│   └── climatizador.py    # Máquina de estados
├── servicios_dominio/      # Lógica de dominio (histeresis)
├── gestores_entidades/     # Casos de uso - Orquestación
├── agentes_sensores/       # Adaptadores de entrada (Proxies)
├── agentes_actuadores/     # Adaptadores de salida (Visualizadores)
├── servicios_aplicacion/   # Coordinación de la app
├── configurador/           # Factories y configuración
├── registrador/            # Sistema de auditoría
├── actores_externos/       # Simuladores y displays
├── Test/                   # Tests unitarios e integración
└── docs/                   # Documentación técnica
    ├── quality/            # Documentación de calidad
    └── Despliegue/         # Estrategias de despliegue
```

## 🎨 Patrones de Diseño Implementados

### Patrones GRASP
- **Information Expert:** Entidades contienen su lógica
- **Creator:** Gestores crean las entidades que manipulan
- **Controller:** Gestores coordinan casos de uso
- **Low Coupling:** Inyección de dependencias + interfaces
- **High Cohesion:** Responsabilidades enfocadas
- **Polymorphism:** Implementaciones intercambiables
- **Pure Fabrication:** Proxies (no existen en dominio)
- **Indirection:** Capas intermedias
- **Protected Variations:** Interfaces abstractas

### Patrones GoF
- **Proxy:** ProxySensorTemperatura, ProxyBateria
- **Factory Method:** 9 factories en configurador/
- **Strategy:** Múltiples implementaciones de proxies/visualizadores
- **State:** Máquina de estados en Climatizador
- **Facade:** VisualizadorEstadoConsolidadoSocket
- **Adapter:** Adaptadores entre capas

### Principios SOLID
- **S**ingle Responsibility: Una responsabilidad por clase
- **O**pen/Closed: Extensible sin modificación
- **L**iskov Substitution: Implementaciones intercambiables
- **I**nterface Segregation: Interfaces mínimas
- **D**ependency Inversion: Depende de abstracciones

## 🔧 Configuración del Sistema

### Archivo Principal: `termostato.json`

**Ubicación:** Raíz del proyecto

**Opciones disponibles:**
```json
{
  "proxy_bateria": "archivo" | "socket",
  "proxy_sensor_temperatura": "archivo" | "socket",
  "climatizador": "climatizador" | "calefactor",
  "visualizador_bateria": "consola" | "socket" | "api",
  "visualizador_temperatura": "consola" | "socket" | "api",
  "visualizador_climatizador": "consola" | "socket" | "api",
  "red": {
    "host_escucha": "0.0.0.0" | "localhost",
    "puertos": { ... },
    "api_url": "https://..."
  }
}
```

### Sistema de Logging

**Configuración:** `ejecutar.py` (líneas 8-16)
- Log file: `termostato.log` (⚠️ ignorado en git)
- Formato: timestamp - módulo - nivel - mensaje
- Niveles: INFO, DEBUG, ERROR
- Handlers: Archivo + Consola

## 💡 Convenciones de Código

### Estilo
- **Python 3.5+** compatible (Raspberry Pi)
- **NO usar f-strings** (usar `.format()`)
- **snake_case** para funciones y variables
- **PascalCase** para clases
- **Docstrings** en español para todos los módulos/clases
- **Type hints** opcionales (no en Python 3.5)

### Nombres de Archivos
- Clases abstractas: `abs_*.py`
- Factories: `factory_*.py`
- Proxies: `proxy_*.py`
- Visualizadores: `visualizador_*.py`

### Importaciones
```python
# Orden:
# 1. Biblioteca estándar
import json
import socket

# 2. Terceros
import requests

# 3. Locales
from entidades.ambiente import Ambiente
```

### Interfaces Abstractas (ABC)
Todas las interfaces usan `ABC` y `abstractmethod`:
```python
from abc import ABC, abstractmethod

class AbsProxySensor(ABC):
    @abstractmethod
    def leer_temperatura(self):
        pass
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest Test/ -v

# Tests específicos
pytest Test/unit/ -v
pytest Test/integration/ -v

# Con cobertura
pytest Test/ --cov=. --cov-report=html
```

### Estructura de Tests
- `Test/unit/` - Tests unitarios
- `Test/integration/` - Tests de integración
- Usar mocks para dependencias externas
- Cobertura objetivo: >80%

## 🚀 Comandos Útiles

### Ejecución Local
```bash
# Ejecutar sistema
python ejecutar.py

# Lanzar simuladores (macOS)
cd actores_externos
./lanzar_simuladores.sh
```

### Git Workflow
```bash
# Crear branch de feature
git checkout -b feature/nombre-descriptivo

# Commits descriptivos
git commit -m "tipo(scope): descripción"
# Tipos: feat, fix, refactor, docs, chore, test

# Push y PR
git push -u origin feature/nombre-descriptivo
```

### Limpieza
```bash
# Limpiar archivos generados
rm -rf build/ dist/ *.egg-info/ .coverage
rm bateria climatizador temperatura tipo_temperatura
rm termostato.log registro_auditoria
```

## 📝 Guías de Desarrollo

### Agregar un Nuevo Visualizador

1. **Crear clase en `agentes_actuadores/`:**
   ```python
   class VisualizadorNuevo(AbsVisualizador):
       def mostrar(self, valor):
           # Implementación
   ```

2. **Crear factory en `configurador/`:**
   ```python
   class FactoryVisualizadorNuevo:
       @staticmethod
       def crear():
           return VisualizadorNuevo()
   ```

3. **Agregar opción en `termostato.json`:**
   ```json
   "visualizador_X": "nuevo"
   ```

4. **Registrar en `configurador.py`**

### Agregar un Nuevo Proxy

Similar al visualizador, pero en `agentes_sensores/` extendiendo la interfaz abstracta correspondiente.

### Modificar Lógica de Dominio

⚠️ **IMPORTANTE:** La lógica de dominio está en:
- `entidades/` - Estado y comportamiento de entidades
- `servicios_dominio/` - Reglas de negocio (ej: histeresis)

**NUNCA** poner lógica de dominio en:
- Proxies (solo lectura/escritura)
- Visualizadores (solo presentación)
- Gestores (solo orquestación)

## 🔍 Debugging

### Archivos de Runtime (NO commitear)
Estos archivos se generan durante la ejecución y están en `.gitignore`:
- `bateria` - Valor actual de batería
- `climatizador` - Estado del climatizador
- `temperatura` - Temperatura actual
- `tipo_temperatura` - Tipo de temperatura
- `registro_auditoria` - Log de auditoría
- `termostato.log` - Log de aplicación

### Puertos TCP
- 11000: Sensor de batería
- 12000: Sensor de temperatura
- 13000: Seteo de temperatura
- 14000: Selector de temperatura
- 14001: Display de temperatura / UX consolidada
- 14002: Display de climatizador

## 📚 Documentación Adicional

- **README.md** - Documentación completa del proyecto
- **DEPLOYMENT.md** - Guía de despliegue
- **docs/quality/** - Análisis de calidad y métricas
- **docs/Despliegue/** - Estrategias de despliegue

## ⚠️ Advertencias Importantes

### NO hacer:
1. ❌ NO usar f-strings (incompatible con Python 3.5)
2. ❌ NO commitear archivos de runtime (bateria, climatizador, etc.)
3. ❌ NO modificar `.gitignore` para trackear logs
4. ❌ NO poner lógica de dominio fuera de entidades/servicios_dominio
5. ❌ NO crear dependencias desde capas internas hacia externas
6. ❌ NO usar `git push --force` a main/master

### SÍ hacer:
1. ✅ Usar `.format()` en lugar de f-strings
2. ✅ Crear tests para código nuevo
3. ✅ Documentar con docstrings
4. ✅ Seguir la arquitectura en capas
5. ✅ Usar inyección de dependencias
6. ✅ Crear branches descriptivos para features

## 🎯 Tareas Comunes

### "Agregar nueva feature de visualización"
1. Leer la arquitectura de visualizadores existentes
2. Crear nueva clase extendiendo interfaz abstracta
3. Crear factory correspondiente
4. Actualizar configurador
5. Agregar tests
6. Documentar en README.md

### "Debugging de problemas de conexión"
1. Verificar puertos en `termostato.json`
2. Revisar logs en `termostato.log`
3. Verificar que simuladores estén ejecutándose
4. Probar con `netstat -an | grep <puerto>`

### "Cambiar lógica de histeresis"
1. Ir a `servicios_dominio/controlador_climatizador.py`
2. Modificar constante `DELTA_TEMP`
3. Actualizar tests en `Test/climatizador/`
4. Documentar cambio en commit

## 🤝 Colaboración

- El proyecto usa **conventional commits**
- Cada PR debe pasar los tests
- Mantener cobertura >80%
- Documentar cambios en README.md si aplica

---

**Última actualización:** 2026-02-02
**Versión del proyecto:** 2.0
**Python:** 3.5+
