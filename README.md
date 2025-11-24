# ISSE_Termostato

Sistema de control de termostato inteligente desarrollado como proyecto educativo para demostrar principios de arquitectura de software y patrones de diseño.

## Descripcion General

El proyecto implementa un sistema de control de temperatura con las siguientes funcionalidades:
- Lectura de temperatura ambiente desde sensores
- Control de climatizacion (calefactor/enfriador) con logica de histeresis
- Monitoreo de nivel de bateria
- Visualizacion de parametros del sistema
- Configuracion flexible mediante archivo JSON

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
|   +-- registrador.py            # Registro de operaciones
|
+-- actores_externos/             # Simuladores y Displays
|   +-- sensor_temperatura.py     # Simulador sensor (cliente, puerto 12000)
|   +-- bateria.py                # Simulador bateria (cliente, puerto 11000)
|   +-- seteo_temperatura_deseada.py  # Selector temp (cliente, puerto 13000)
|   +-- cartel_temperatura.py     # Display temperatura (servidor, puerto 14001)
|   +-- cartel_bateria.py         # Display bateria (servidor, puerto 14000)
|   +-- cartel_climatizador.py    # Display climatizador (servidor, puerto 14002)
|
+-- Test/                         # Tests unitarios
|   +-- hal/
|   +-- bateria/
|   +-- temperatura/
|   +-- climatizador/
|   +-- operador/
|   +-- presentador/
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
| Sensor Temperatura | `sensor_temperatura.py` | 12000 | Simula sensor fisico, envia temperatura en grados C |
| Bateria | `bateria.py` | 11000 | Simula bateria, envia nivel de carga (0-5V) |
| Selector Temperatura | `seteo_temperatura_deseada.py` | 13000 | Botones para aumentar/disminuir temperatura deseada |

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

### Ejecucion de Actores Externos

Para pruebas con comunicacion por socket, ejecutar en terminales separadas:

```bash
# Terminal 1: Sistema principal
python ejecutar.py

# Terminal 2: Simulador de temperatura
python actores_externos/sensor_temperatura.py

# Terminal 3: Simulador de bateria
python actores_externos/bateria.py

# Terminal 4: Display de temperatura
python actores_externos/cartel_temperatura.py

# Terminal 5: Display de bateria
python actores_externos/cartel_bateria.py

# Terminal 6: Display de climatizador
python actores_externos/cartel_climatizador.py
```

## API REST

Los visualizadores con sufijo `Api` envian datos via HTTP POST a un servidor REST en `localhost:5050`.

### Endpoints

| Endpoint | Metodo | Payload | Descripcion |
|----------|--------|---------|-------------|
| `/termostato/temperatura_ambiente` | POST | `{"ambiente": valor}` | Temperatura actual |
| `/termostato/temperatura_deseada` | POST | `{"deseada": valor}` | Temperatura objetivo |
| `/termostato/bateria` | POST | `{"bateria": valor}` | Nivel de carga |
| `/bateria/indicador` | POST | `{"indicador": valor}` | Estado NORMAL/BAJA |
| `/termostato/estado_climatizador` | POST | `{"climatizador": valor}` | Estado del climatizador |

### Dependencias

Para usar los visualizadores API se requiere la libreria `requests`:

```bash
pip install requests
```

## Configuracion

El sistema se configura mediante `termostato.json`:

```json
{
  "proxy_bateria": "archivo",
  "proxy_sensor_temperatura": "socket",
  "climatizador": "calefactor",
  "actuador_climatizador": "general",
  "selector_temperatura": "archivo",
  "seteo_temperatura": "socket",
  "visualizador_bateria": "socket",
  "visualizador_temperatura": "socket",
  "visualizador_climatizador": "socket"
}
```

Opciones disponibles:
- **proxy_bateria/proxy_sensor_temperatura**: "archivo" | "socket"
- **climatizador**: "climatizador" | "calefactor"
- **visualizadores**: "consola" | "socket" | "api"

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

## Ejecucion

```bash
# Instalar dependencias
./instalar_termostato.sh

# Ejecutar el sistema
python ejecutar.py

# O usar el script de build
./build_termostato.sh
```

## Tecnologias

- **Python 3.x**
- **ABC (Abstract Base Classes)** para interfaces
- **threading** para ejecucion paralela
- **socket** para comunicacion TCP
- **json** para configuracion
- **requests** para comunicacion API REST (opcional)

## Caracteristicas del Diseno

- **Arquitectura limpia**: Separacion clara de responsabilidades
- **Extensibilidad**: Facil agregar nuevas implementaciones
- **Testabilidad**: Cada componente se puede probar aisladamente
- **Bajo acoplamiento**: Interfaces abstractas desacoplan capas
- **Alta cohesion**: Responsabilidades enfocadas por clase
- **Configuracion flexible**: termostato.json permite cambios sin codigo

## Documentacion Adicional

- `docs/Patrones_y_Decisiones_de_Diseno.md` - Analisis detallado de patrones
- `docs/Elicitacion_Requerimientos.md` - Requerimientos del sistema
- `docs/Diagramas_Con_Capa_HAL.md` - Diagramas de arquitectura
- `docs/Migracion_Capa_HAL.md` - Guia de migracion a capa HAL
