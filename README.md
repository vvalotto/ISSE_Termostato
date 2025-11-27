# ISSE_Termostato

Sistema de control de termostato inteligente desarrollado como proyecto educativo para demostrar principios de arquitectura de software y patrones de diseño.

![Python Version](https://img.shields.io/badge/python-3.5%2B-blue)
![Status](https://img.shields.io/badge/status-production-green)
![Architecture](https://img.shields.io/badge/architecture-clean-orange)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red)
![License](https://img.shields.io/badge/license-educational-yellow)

## Tabla de Contenidos

- [Estado del Proyecto](#estado-del-proyecto)
- [Quick Start](#quick-start)
- [Descripcion General](#descripcion-general)
- [Mejoras Recientes](#mejoras-recientes)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Patrones de Diseno](#patrones-de-diseno-implementados)
- [Componentes Principales](#componentes-principales)
- [Flujos de Datos](#flujos-de-datos)
- [Actores Externos](#actores-externos)
- [Simulacion Distribuida](#simulacion-distribuida)
- [API REST](#api-rest)
- [Configuracion](#configuracion)
- [Ejecucion Concurrente](#ejecucion-concurrente)
- [Tests](#tests)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Ejecucion](#ejecucion)
- [Tecnologias](#tecnologias)
- [Caracteristicas del Diseno](#caracteristicas-del-diseno)
- [Arquitectura de Despliegue](#arquitectura-de-despliegue)
- [Troubleshooting](#troubleshooting)
- [Documentacion Adicional](#documentacion-adicional)
- [Licencia y Contribuciones](#licencia-y-contribuciones)

## Estado del Proyecto

**Version actual:** 2.0 (Simulacion Distribuida + Python 3.5)
**Ultima actualizacion:** Noviembre 2025
**Estado:** Produccion - Funcional en Raspberry Pi + API REST desplegada

### Features Principales
- ✅ Clean Architecture con separacion de capas
- ✅ Patrones GRASP, GoF y SOLID
- ✅ Simulacion distribuida (Raspberry Pi + MacBook via sockets TCP)
- ✅ API REST integrada (desplegada en Render)
- ✅ Compatible Python 3.5+ (Raspberry Pi OS Lite)
- ✅ 3 modos de visualizacion: consola, socket, API REST
- ✅ Sistema de auditoria y logging
- ✅ Tests unitarios y de integracion
- ✅ Script de lanzamiento automatico de simuladores (macOS)

## Descripcion General

El proyecto implementa un sistema de control de temperatura con las siguientes funcionalidades:
- Lectura de temperatura ambiente desde sensores
- Control de climatizacion (calefactor/enfriador) con logica de histeresis
- Monitoreo de nivel de bateria
- Visualizacion de parametros del sistema
- Configuracion flexible mediante archivo JSON
- **Simulacion distribuida** via sockets TCP (Raspberry Pi + MacBook)
- **API REST** para visualizacion remota

## Quick Start

### Opcion 1: Ejecucion Local (Prueba Rapida)

```bash
# 1. Clonar el repositorio
git clone https://github.com/vvalotto/ISSE_Termostato.git
cd ISSE_Termostato

# 2. Instalar dependencias (opcional, solo para visualizadores API)
pip install requests

# 3. Configurar para modo local
# Editar termostato.json: cambiar todos los visualizadores a "consola"

# 4. Ejecutar
python ejecutar.py
```

### Opcion 2: Simulacion Distribuida (Raspberry Pi + MacBook)

**En Raspberry Pi:**
```bash
# 1. Configurar termostato.json
{
  "red": {
    "host_escucha": "0.0.0.0",
    "api_url": "https://termostato-api.onrender.com"
  }
}

# 2. Ejecutar sistema
python ejecutar.py
```

**En MacBook:**
```bash
# 1. Configurar actores_externos/simuladores_config.json con IP de Raspberry
# 2. Lanzar simuladores
cd actores_externos
./lanzar_simuladores.sh
```

## Mejoras Recientes

### Simulacion Distribuida (Sprint Actual)
- Soporte para ejecucion en arquitectura distribuida (Raspberry Pi + MacBook)
- Configuracion centralizada de red en `termostato.json`
- Archivo `simuladores_config.json` para configurar IP remota
- Script `lanzar_simuladores.sh` para macOS (lanza 4 terminales automaticamente)
- Mejoras en manejo de errores y reconexion
- Soporte para `SO_REUSEADDR` en sockets (evita "Address already in use")

### Compatibilidad Python 3.5
- Migracion completa a Python 3.5+ (compatible con Raspberry Pi OS Lite)
- Reemplazo de f-strings por `.format()` (21 cambios en 8 archivos)
- Validacion de configuracion al inicio del sistema

### Visualizacion y API
- Integracion con API REST desplegada en Render (https://termostato-api.onrender.com)
- Visualizadores con timeout y manejo robusto de errores
- Soporte para 3 modos: consola, socket, API REST

## Arquitectura

El sistema implementa **Clean Architecture** (Arquitectura Limpia) de Robert C. Martin, donde las dependencias apuntan hacia el centro:

```
+===========================================================================+
|                        FRAMEWORKS & DRIVERS                               |
|  actores_externos/                                                        |
|  sensor_temperatura.py, bateria.py, cartel_*.py                          |
|                                                                           |
|  +=====================================================================+  |
|  |                    INTERFACE ADAPTERS                               |  |
|  |  agentes_sensores/              agentes_actuadores/                 |  |
|  |  - ProxySensorTemperatura       - VisualizadorTemperatura           |  |
|  |  - ProxyBateria                 - VisualizadorBateria               |  |
|  |  - ProxySelectorTemperatura     - VisualizadorClimatizador          |  |
|  |                                 - ActuadorClimatizador              |  |
|  |                                                                     |  |
|  |  +===============================================================+  |  |
|  |  |                    USE CASES (Application)                    |  |  |
|  |  |  gestores_entidades/           servicios_aplicacion/          |  |  |
|  |  |  - GestorAmbiente              - Presentador                  |  |  |
|  |  |  - GestorBateria               - OperadorParalelo             |  |  |
|  |  |  - GestorClimatizador          - Inicializador                |  |  |
|  |  |                                                               |  |  |
|  |  |  +=========================================================+  |  |  |
|  |  |  |                    ENTITIES (Domain)                    |  |  |  |
|  |  |  |  entidades/                 servicios_dominio/          |  |  |  |
|  |  |  |  - Ambiente                 - ControladorTemperatura    |  |  |  |
|  |  |  |  - Bateria                                              |  |  |  |
|  |  |  |  - Climatizador                                         |  |  |  |
|  |  |  |  - Interfaces abstractas (abs_*.py)                     |  |  |  |
|  |  |  +=========================================================+  |  |  |
|  |  |                             ^                                 |  |  |
|  |  +===============================================================+  |  |
|  |                                ^                                    |  |
|  +=====================================================================+  |
|                                   ^                                       |
+===========================================================================+
                    (las dependencias apuntan hacia el centro)
```

### Regla de Dependencia

La regla fundamental de Clean Architecture: **las dependencias solo apuntan hacia adentro**.

- **Entities**: Logica de negocio pura, sin dependencias externas
- **Use Cases**: Orquestan entidades, definen interfaces para adaptadores
- **Interface Adapters**: Implementan interfaces, convierten datos entre capas
- **Frameworks & Drivers**: Detalles de infraestructura (sockets, archivos, API)

## Estructura del Proyecto

```
ISSE_Termostato/
|
+-- entidades/                    # Capa de Dominio
|   +-- abs_*.py                  # Interfaces abstractas
|   +-- ambiente.py               # Entidad de ambiente
|   +-- bateria.py                # Entidad de bateria
|   +-- climatizador.py           # Maquina de estados
|
+-- gestores_entidades/           # Capa de Aplicacion
|   +-- gestor_ambiente.py        # Orquesta temperatura
|   +-- gestor_bateria.py         # Orquesta bateria
|   +-- gestor_climatizador.py    # Orquesta climatizacion
|
+-- agentes_sensores/             # Capa de Infraestructura (Proxies)
|   +-- proxy_sensor_temperatura.py
|   +-- proxy_bateria.py
|   +-- proxy_selector_temperatura.py
|   +-- proxy_seteo_temperatura.py
|
+-- agentes_actuadores/           # Capa de Presentacion
|   +-- actuador_climatizador.py
|   +-- visualizador_temperatura.py
|   +-- visualizador_bateria.py
|   +-- visualizador_climatizador.py
|
+-- servicios_aplicacion/         # Servicios de Aplicacion
|   +-- lanzador.py               # Punto de entrada principal
|   +-- presentador.py            # Orquesta visualizacion
|   +-- operador_paralelo.py      # Ejecucion con threads
|   +-- operador_secuencial.py    # Ejecucion secuencial
|   +-- inicializador.py          # Inicializacion del sistema
|
+-- servicios_dominio/            # Servicios de Dominio
|   +-- controlador_climatizador.py  # Logica de histeresis
|
+-- configurador/                 # Capa de Configuracion
|   +-- configurador.py           # Cargador centralizado
|   +-- factory_*.py              # Factories (9 factories)
|
+-- registrador/                  # Sistema de Auditoria
|   +-- registrador.py            # Registro de operaciones y eventos
|
+-- registro_auditoria            # Archivo de logs de auditoria
|
+-- actores_externos/             # Simuladores y Displays
|   +-- simuladores_config.json   # Configuracion de IP remota (Raspberry Pi)
|   +-- lanzar_simuladores.sh     # Script para lanzar 4 simuladores (macOS)
|   +-- simulador_temperatura.py  # Simulador sensor (cliente, puerto 12000)
|   +-- simulador_bateria.py      # Simulador bateria (cliente, puerto 11000)
|   +-- simulador_seteo_temperatura_deseada.py  # Selector temp (cliente, puerto 13000)
|   +-- simulador_selector_temperatura.py  # Selector temperatura (cliente, puerto 14000)
|   +-- cartel_temperatura.py     # Display temperatura (servidor, puerto 14001)
|   +-- cartel_bateria.py         # Display bateria (servidor, puerto 14000)
|   +-- cartel_climatizador.py    # Display climatizador (servidor, puerto 14002)
|
+-- Test/                         # Tests unitarios e integración
|   +-- unit/                     # Tests unitarios
|   +-- integration/              # Tests de integración
|   +-- hal/
|   +-- bateria/
|   +-- temperatura/
|   +-- climatizador/
|   +-- operador/
|   +-- presentador/
|   +-- lanzador/
|   +-- selector_temperatura/
|
+-- docs/                         # Documentacion
+-- termostato.json               # Configuracion
+-- ejecutar.py                   # Punto de entrada
```

## Patrones de Diseno Implementados

### Patrones GRASP

| Patron | Ubicacion | Descripcion |
|--------|-----------|-------------|
| **Information Expert** | `Ambiente`, `Bateria` | Clases contienen informacion para sus decisiones |
| **Creator** | `GestorAmbiente`, `GestorBateria` | Gestores crean entidades que manipulan |
| **Controller** | Gestores | Coordinan casos de uso |
| **Low Coupling** | Sistema completo | Inyeccion de dependencias + interfaces |
| **High Cohesion** | Cada clase | Responsabilidad unica y enfocada |
| **Polymorphism** | Proxies, Visualizadores | Implementaciones intercambiables |
| **Pure Fabrication** | Proxies | Clases tecnicas no existentes en dominio |
| **Indirection** | Capas | Capas intermediarias desacoplan componentes |
| **Protected Variations** | Interfaces abstractas | Protegen contra cambios futuros |

### Patrones GoF

| Patron | Implementacion | Ubicacion |
|--------|----------------|-----------|
| **Proxy** | ProxySensorTemperatura, ProxyBateria | `agentes_sensores/` |
| **Factory Method** | Factories para componentes | `configurador/factory_*.py` |
| **Strategy** | Multiples implementaciones de proxies | Intercambiables por config |
| **State** | Maquina de estados del climatizador | `entidades/climatizador.py` |
| **Template Method** | Metodos abstractos en clases base | Interfaces abstractas |

### Principios SOLID

| Principio | Aplicacion |
|-----------|------------|
| **S**ingle Responsibility | Cada clase tiene una responsabilidad unica |
| **O**pen/Closed | Extensible sin modificacion (nuevas factories) |
| **L**iskov Substitution | Implementaciones intercambiables |
| **I**nterface Segregation | Interfaces minimas y especificas |
| **D**ependency Inversion | Dependen de abstracciones, no implementaciones |

## Componentes Principales

### Capa de Dominio

**Ambiente** (`entidades/ambiente.py`)
- Mantiene estado: temperatura_ambiente, temperatura_deseada
- Encapsula propiedades con getters/setters

**Bateria** (`entidades/bateria.py`)
- Propiedades: nivel_de_carga, indicador (NORMAL/BAJA)
- Actualiza indicador segun umbral (80%)

**Climatizador** (`entidades/climatizador.py`)
- Maquina de estados: apagado, calentando, enfriando
- Transiciones validadas segun temperatura comparada
- Variantes: Climatizador (calienta/enfria), Calefactor (solo calienta)

### Capa de Aplicacion

**GestorAmbiente** (`gestores_entidades/gestor_ambiente.py`)
- Coordina lectura de sensor -> almacenamiento en entidad -> visualizacion
- Metodos: leer_temperatura_ambiente(), aumentar/disminuir_temperatura_deseada()

**GestorBateria** (`gestores_entidades/gestor_bateria.py`)
- Coordina lectura de carga -> almacenamiento -> visualizacion
- Metodos: verificar_nivel_de_carga(), obtener_indicador_de_carga()

**GestorClimatizador** (`gestores_entidades/gestor_climatizador.py`)
- Coordina evaluacion -> transicion de estado -> actuacion
- Implementa logica de histeresis (DELTA_TEMP = 2 grados C)

### Servicios de Dominio

**ControladorTemperatura** (`servicios_dominio/controlador_climatizador.py`)
- Metodo estatico: comparar_temperatura(actual, deseada)
- Implementa logica de histeresis (+/- 2 grados C)
- Retorna: "alta", "baja" o "normal"

### Capa de Infraestructura

**Proxies** (`agentes_sensores/`)
- ProxySensorTemperaturaArchivo: Lee de archivo
- ProxySensorTemperaturaSocket: Lee de socket TCP
- ProxyBateriaArchivo/Socket: Similar para bateria
- Abstraccion del origen de datos

### Capa de Presentacion

**Visualizadores** (`agentes_actuadores/`)

Cada visualizador tiene 3 implementaciones intercambiables:

| Clase | Tipo | Descripcion |
|-------|------|-------------|
| `VisualizadorTemperatura` | Consola | Imprime en terminal |
| `VisualizadorTemperaturaSocket` | Socket | Envia a puerto 14001 |
| `VisualizadorTemperaturaApi` | API REST | POST a localhost:5050 |
| `VisualizadorBateria` | Consola | Imprime en terminal |
| `VisualizadorBateriaSocket` | Socket | Envia a puertos 14000/13005 |
| `VisualizadorBateriaApi` | API REST | POST a localhost:5050 |
| `VisualizadorClimatizador` | Consola | Imprime en terminal |
| `VisualizadorClimatizadorSocket` | Socket | Envia a puerto 14002 |
| `VisualizadorClimatizadorApi` | API REST | POST a localhost:5050 |

**ActuadorClimatizador** (`agentes_actuadores/actuador_climatizador.py`)
- Ejecuta acciones en climatizador
- Implementa auditoria y registro de errores

## Flujos de Datos

### Lectura de Temperatura
```
Operador -> GestorAmbiente.leer_temperatura_ambiente()
         -> ProxySensorTemperatura.leer_temperatura()
         -> Archivo/Socket
         -> Ambiente.temperatura_ambiente (setter)
```

### Control de Climatizacion
```
Operador -> GestorClimatizador.accionar_climatizador(ambiente)
         -> Climatizador.evaluar_accion()
         -> ControladorTemperatura.comparar_temperatura()
         -> ActuadorClimatizador.accionar_climatizador(accion)
         -> Archivo "climatizador"
```

### Verificacion de Bateria
```
Operador -> GestorBateria.verificar_nivel_de_carga()
         -> ProxyBateria.leer_carga()
         -> Archivo/Socket
         -> Bateria.nivel_de_carga (setter)
         -> Bateria.indicador (NORMAL/BAJA)
```

## Actores Externos

Los actores externos simulan dispositivos fisicos y displays para pruebas. Se comunican via sockets TCP.

### Simuladores de Entrada (Clientes)

Envian datos al sistema principal:

| Actor | Archivo | Puerto | Descripcion |
|-------|---------|--------|-------------|
| Sensor Temperatura | `simulador_temperatura.py` | 12000 | Simula sensor fisico, envia temperatura en grados C |
| Bateria | `simulador_bateria.py` | 11000 | Simula bateria, envia nivel de carga (0-5V) |
| Seteo Temperatura | `simulador_seteo_temperatura_deseada.py` | 13000 | Botones para aumentar/disminuir temperatura deseada |
| Selector Temperatura | `simulador_selector_temperatura.py` | 14000 | Selector de modo de operacion (manual/auto) |

### Displays de Salida (Servidores)

Reciben datos del sistema para visualizacion:

| Actor | Archivo | Puerto | Descripcion |
|-------|---------|--------|-------------|
| Cartel Temperatura | `cartel_temperatura.py` | 14001 | Muestra temperatura actual |
| Cartel Bateria | `cartel_bateria.py` | 14000 | Muestra tension de bateria |
| Cartel Climatizador | `cartel_climatizador.py` | 14002 | Muestra estado del climatizador |

### Diagrama de Comunicacion

```
SIMULADORES (Clientes)                 SISTEMA                    DISPLAYS (Servidores)
                                    TERMOSTATO
+-------------------+                                          +---------------------+
| sensor_temperatura|---[12000]-->| ProxySensor   |            |                     |
+-------------------+             | Temperatura   |            |                     |
                                  +---------------+            |                     |
+-------------------+                                          |                     |
| bateria           |---[11000]-->| ProxyBateria  |            |                     |
+-------------------+             +---------------+            |                     |
                                                               |                     |
+-------------------+             +---------------+            |                     |
| seteo_temperatura |---[13000]-->| ProxySelector |            |                     |
+-------------------+             +---------------+            |                     |
                                                               |                     |
                                  +---------------+--[14001]-->| cartel_temperatura  |
                                  | Visualizador  |            +---------------------+
                                  | Temperatura   |
                                  +---------------+--[14000]-->| cartel_bateria      |
                                  | Visualizador  |            +---------------------+
                                  | Bateria       |
                                  +---------------+--[14002]-->| cartel_climatizador |
                                  | Visualizador  |            +---------------------+
                                  | Climatizador  |
                                  +---------------+
```

## Simulacion Distribuida

El sistema soporta **arquitectura distribuida** donde los simuladores pueden ejecutarse en una maquina diferente (ej: MacBook) mientras el sistema principal corre en otra (ej: Raspberry Pi).

### Configuracion para Simulacion Distribuida

**En el sistema principal (Raspberry Pi):**

Configurar `termostato.json` con:
```json
{
  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": { ... },
    "api_url": "https://tu-servidor-api.com"
  }
}
```

**En la maquina de simuladores (MacBook):**

Configurar `actores_externos/simuladores_config.json`:
```json
{
  "raspberry_pi": {
    "host": "192.168.0.14",
    "puertos": {
      "bateria": 11000,
      "temperatura": 12000,
      "seteo_temperatura": 13000,
      "selector_temperatura": 14000
    }
  }
}
```

### Lanzar Simuladores Automaticamente

En macOS, usar el script de lanzamiento automatico:

```bash
cd actores_externos
./lanzar_simuladores.sh
```

Este script abre 4 terminales automaticamente, una para cada simulador:
- `simulador_bateria.py`
- `simulador_temperatura.py`
- `simulador_seteo_temperatura_deseada.py`
- `simulador_selector_temperatura.py`

### Ejecucion de Actores Externos

**Opcion 1: Script automatico (macOS)**

```bash
cd actores_externos
./lanzar_simuladores.sh
```

Este script abre automaticamente 4 terminales con los simuladores.

**Opcion 2: Manual**

Para pruebas con comunicacion por socket, ejecutar en terminales separadas:

```bash
# Terminal 1: Sistema principal (Raspberry Pi o local)
python ejecutar.py

# Terminal 2: Simulador de temperatura
python actores_externos/simulador_temperatura.py

# Terminal 3: Simulador de bateria
python actores_externos/simulador_bateria.py

# Terminal 4: Seteo de temperatura
python actores_externos/simulador_seteo_temperatura_deseada.py

# Terminal 5: Selector de temperatura
python actores_externos/simulador_selector_temperatura.py

# Terminal 6: Display de temperatura (opcional, solo testing local)
python actores_externos/cartel_temperatura.py

# Terminal 7: Display de bateria (opcional, solo testing local)
python actores_externos/cartel_bateria.py

# Terminal 8: Display de climatizador (opcional, solo testing local)
python actores_externos/cartel_climatizador.py
```

**Nota:** Los displays (carteles) solo son necesarios para testing local con visualizadores tipo "socket". Si usas visualizadores tipo "api", no son necesarios.

## API REST

Los visualizadores con sufijo `Api` envian datos via HTTP POST a un servidor REST. La URL del servidor se configura en `termostato.json`:

```json
{
  "red": {
    "api_url": "https://termostato-api.onrender.com"
  }
}
```

### Endpoints

| Endpoint | Metodo | Payload | Descripcion |
|----------|--------|---------|-------------|
| `/termostato/temperatura_ambiente` | POST | `{"ambiente": valor}` | Temperatura actual |
| `/termostato/temperatura_deseada` | POST | `{"deseada": valor}` | Temperatura objetivo |
| `/termostato/bateria` | POST | `{"bateria": valor}` | Nivel de carga |
| `/bateria/indicador` | POST | `{"indicador": valor}` | Estado NORMAL/BAJA |
| `/termostato/estado_climatizador` | POST | `{"climatizador": valor}` | Estado del climatizador |

### Servidor API Desplegado

El proyecto incluye integracion con un servidor API REST desplegado en:
- **URL de produccion**: https://termostato-api.onrender.com
- **Timeout**: 5 segundos
- **Manejo de errores**: Reintentos automaticos y logging

### Dependencias

Para usar los visualizadores API se requiere la libreria `requests`:

```bash
pip install requests
```

## Configuracion

El sistema se configura mediante `termostato.json`:

```json
{
  "proxy_bateria": "socket",
  "proxy_sensor_temperatura": "socket",
  "climatizador": "calefactor",
  "actuador_climatizador": "general",
  "selector_temperatura": "socket",
  "seteo_temperatura": "socket",
  "visualizador_bateria": "api",
  "visualizador_temperatura": "api",
  "visualizador_climatizador": "api",

  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": {
      "bateria": 11000,
      "temperatura": 12000,
      "seteo_temperatura": 13000,
      "selector_temperatura": 14000
    },
    "api_url": "https://termostato-api.onrender.com"
  }
}
```

Opciones disponibles:
- **proxy_bateria/proxy_sensor_temperatura**: "archivo" | "socket"
- **climatizador**: "climatizador" | "calefactor"
- **selector_temperatura**: "archivo" | "socket"
- **seteo_temperatura**: "archivo" | "socket"
- **visualizadores**: "consola" | "socket" | "api"

### Configuracion de Red (Simulacion Distribuida)

La seccion `"red"` permite ejecutar el sistema en modo distribuido:
- **host_escucha**: IP donde escuchar conexiones (`0.0.0.0` para aceptar conexiones remotas, `localhost` para solo locales)
- **puertos**: Puertos para cada sensor/actuador
- **api_url**: URL del servidor API REST para visualizacion

## Ejecucion Concurrente

El sistema utiliza **5 threads paralelos** en `OperadorParalelo`:

1. `lee_carga_bateria()` - cada 1 segundo
2. `lee_temperatura_ambiente()` - cada 2 segundos
3. `acciona_climatizador()` - cada 5 segundos
4. `muestra_parametros()` - cada 5 segundos
5. `setea_temperatura()` - cada 5 segundos

## Tests

El proyecto incluye tests unitarios en `Test/`:

```bash
# Ejecutar todos los tests
pytest Test/ -v

# Ejecutar tests especificos
pytest Test/hal/test_hal_adc.py -v
pytest Test/climatizador/ -v
```

### Cobertura de Tests
- Capa HAL (simulado, mock)
- Capa de Dominio (entidades)
- Servicios de Dominio (controlador)
- Capa de Aplicacion (gestores)
- Servicios de Aplicacion (operadores, presentador)
- Casos de error

## Requisitos del Sistema

### Hardware
- **Sistema principal**: Raspberry Pi 3/4 con Raspberry Pi OS Lite, o cualquier PC con Linux/macOS/Windows
- **Simuladores**: Cualquier PC (recomendado: MacBook para usar `lanzar_simuladores.sh`)
- **Red**: Conexion LAN entre dispositivos para modo distribuido

### Software
- **Python**: 3.5+ (Raspberry Pi) o 3.8+ (desarrollo)
- **Librerias**: `requests` (opcional, para visualizadores API)
- **Sistema operativo**: Linux, macOS, Windows

### Puertos de Red (para simulacion distribuida)
- 11000: Sensor de bateria
- 12000: Sensor de temperatura
- 13000: Seteo de temperatura
- 14000: Selector de temperatura
- 14001, 14002: Displays (opcional, solo testing local)

## Ejecucion

### Instalacion

```bash
# Instalar dependencias
./instalar_termostato.sh

# O manualmente
pip install requests  # Solo si usas visualizadores API
```

### Ejecucion Local

```bash
# Ejecutar el sistema
python ejecutar.py

# O usar el script de build
./build_termostato.sh
```

### Ejecucion Distribuida

**En Raspberry Pi:**
```bash
# 1. Configurar termostato.json con host_escucha: "0.0.0.0"
# 2. Ejecutar el sistema
python ejecutar.py
```

**En MacBook:**
```bash
# 1. Configurar actores_externos/simuladores_config.json con IP de Raspberry
# 2. Lanzar simuladores
cd actores_externos
./lanzar_simuladores.sh  # macOS
# O manualmente ejecutar cada simulador en terminales separadas
```

## Tecnologias

- **Python 3.5+** (compatible con Raspberry Pi)
- **ABC (Abstract Base Classes)** para interfaces
- **threading** para ejecucion paralela
- **socket** para comunicacion TCP distribuida
- **json** para configuracion
- **requests** para comunicacion API REST (opcional)
- **pytest** para testing unitario

## Caracteristicas del Diseno

- **Arquitectura limpia**: Separacion clara de responsabilidades
- **Extensibilidad**: Facil agregar nuevas implementaciones
- **Testabilidad**: Cada componente se puede probar aisladamente
- **Bajo acoplamiento**: Interfaces abstractas desacoplan capas
- **Alta cohesion**: Responsabilidades enfocadas por clase
- **Configuracion flexible**: termostato.json permite cambios sin codigo

## Arquitectura de Despliegue

```
┌─────────────────────────────────────────────────────────────────┐
│                          INTERNET                                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Servidor API REST (Render)                            │     │
│  │  https://termostato-api.onrender.com                   │     │
│  │  - Endpoints REST                                      │     │
│  │  - Almacenamiento de metricas                          │     │
│  └────────────────────────────────────────────────────────┘     │
│                            ▲                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ HTTPS POST
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                      RED LOCAL (LAN)                             │
│                            │                                     │
│  ┌─────────────────────────┴──────────────────────────────┐     │
│  │  RASPBERRY PI (Sistema Principal)                      │     │
│  │  - Python 3.5+                                         │     │
│  │  - Termostato (ejecutar.py)                            │     │
│  │  - Escucha en 0.0.0.0:11000-14000                      │     │
│  │  - VisualizadoresApi -> Envia a Render                 │     │
│  └────────────────────────────────────────────────────────┘     │
│                            ▲                                     │
│                            │ Socket TCP                          │
│                            │                                     │
│  ┌─────────────────────────┴──────────────────────────────┐     │
│  │  MACBOOK (Simuladores)                                 │     │
│  │  - Python 3.8+                                         │     │
│  │  - 4 simuladores (bateria, temp, seteo, selector)     │     │
│  │  - Conectan a IP Raspberry via TCP                     │     │
│  │  - Script lanzar_simuladores.sh                        │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

**Componentes:**
1. **Raspberry Pi**: Sistema embebido ejecutando el termostato principal
2. **MacBook**: Desarrollo y simuladores remotos
3. **API REST (Render)**: Visualizacion web y almacenamiento de metricas
4. **Red Local**: Comunicacion entre Raspberry y simuladores via TCP

## Troubleshooting

### Error: "Address already in use"

**Problema:** Al ejecutar el sistema aparece este error.

**Solucion:** El sistema ahora incluye `SO_REUSEADDR` en todos los sockets. Si persiste:
```bash
# Encontrar proceso usando el puerto
lsof -i :11000  # Reemplazar con el puerto que falla
# Matar el proceso
kill -9 <PID>
```

### Error: "Connection refused" en simulacion distribuida

**Problema:** Los simuladores no pueden conectar a Raspberry Pi.

**Soluciones:**
1. Verificar que `termostato.json` tenga `"host_escucha": "0.0.0.0"`
2. Verificar IP correcta en `simuladores_config.json`
3. Verificar que el firewall permita los puertos (11000-14002)
4. Probar conectividad: `ping <IP_RASPBERRY>`

### Error: "No module named 'requests'"

**Problema:** Los visualizadores API no funcionan.

**Solucion:**
```bash
pip install requests
# O en Raspberry Pi
pip3 install requests
```

### Timeout en visualizadores API

**Problema:** Demoras o timeouts al enviar a la API.

**Causa:** El servidor API puede estar en cold start (Render free tier).

**Solucion:** El sistema tiene timeout de 5 segundos y manejo de errores. Los datos se pierden pero el sistema continua funcionando.

### Simuladores no se conectan automaticamente

**Problema:** `lanzar_simuladores.sh` no funciona.

**Soluciones:**
1. Verificar permisos de ejecucion: `chmod +x lanzar_simuladores.sh`
2. Solo funciona en macOS (usa AppleScript para Terminal)
3. En Linux/Windows, ejecutar simuladores manualmente

## Documentacion Adicional

### Documentos de Arquitectura y Diseno
- `docs/Patrones_y_Decisiones_de_Diseno.md` - Analisis detallado de patrones GRASP, GoF y SOLID
- `docs/Elicitacion_Requerimientos.md` - Requerimientos funcionales y no funcionales del sistema

### Documentos de Testing y Calidad
- `docs/Plan_de_Pruebas.md` - Estrategia y plan de pruebas
- `docs/Reporte_Tests_Unitarios.md` - Resultados de tests unitarios
- `docs/Reporte_Tests_Integracion.md` - Resultados de tests de integracion
- `docs/Informe_Calidad_Codigo_ISSE_Termostato.pdf` - Analisis de calidad del codigo
- `docs/Reporte_Analisis_Tecnico_ISSE_Termostato.pdf` - Analisis tecnico completo

### Planes de Migracion y Mejoras
- `docs/plan_simulacion_distribuida.md` - Plan completo de implementacion distribuida
- `docs/plan_migracion_python35.md` - Guia de migracion a Python 3.5 (Raspberry Pi)

### Historias de Usuario
- `Historias Sprint 1.md` - Historias de usuario del primer sprint

## Licencia y Contribuciones

### Autor
- **Victor Valotto** - [@vvalotto](https://github.com/vvalotto)

### Proyecto Educativo
Este proyecto fue desarrollado como parte del curso de Ingenieria de Software de Sistemas Embebidos (ISSE) con propositos educativos, demostrando:
- Principios de Clean Architecture
- Patrones de diseno GRASP, GoF y SOLID
- Testing y calidad de codigo
- Simulacion distribuida en sistemas embebidos
- Integracion con APIs REST

### Contribuciones
Este es un proyecto educativo. Si encuentras algun problema o tienes sugerencias:
1. Abre un [Issue](https://github.com/vvalotto/ISSE_Termostato/issues)
2. Envia un Pull Request con mejoras
3. Contacta al autor

### Agradecimientos
- Curso de Ingenieria de Software de Sistemas Embebidos
- Documentacion de Clean Architecture (Robert C. Martin)
- Comunidad de Python

---

**Proyecto desarrollado con fines educativos | 2025**
