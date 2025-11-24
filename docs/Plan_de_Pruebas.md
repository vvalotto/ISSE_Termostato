# Plan de Pruebas - ISSE_Termostato

## 1. Introduccion

### 1.1 Proposito
Este documento define el plan de pruebas para el sistema ISSE_Termostato, un sistema de control de termostato inteligente que implementa Clean Architecture.

### 1.2 Alcance
El plan cubre pruebas unitarias, de integracion y end-to-end para todas las capas del sistema:
- Entidades (Dominio)
- Gestores (Casos de Uso), 
- Proxies y Visualizadores (Adaptadores)
- Servicios de Aplicacion
- Configuracion y Factories

### 1.3 Estado Actual de Tests
Cobertura actual estimada: **20-30%**

| Componente | Estado | Tipo de Test |
|------------|--------|--------------|
| ControladorTemperatura | Completo | Manual |
| HAL ADC | Completo | pytest con mocks |
| Gestores | Parcial | Manual sin assertions |
| Proxies | Basico | Manual |
| Visualizadores | Sin tests | - |
| Factories | Sin tests | - |

---

## 2. Estrategia de Pruebas

### 2.1 Niveles de Prueba

```
+------------------------------------------------------------------+
|                        END-TO-END (E2E)                          |
|  Ciclo completo: Inicializacion -> Operacion -> Visualizacion    |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                        INTEGRACION                               |
|  Gestor + Proxy + Visualizador | Flujos de climatizacion        |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                        UNITARIAS                                 |
|  Entidades | Servicios Dominio | Factories | Controladores       |
+------------------------------------------------------------------+
```

### 2.2 Distribucion del Esfuerzo

| Nivel | Esfuerzo | Cantidad Estimada |
|-------|----------|-------------------|
| Unitarias | 40% | 50+ tests |
| Integracion | 40% | 20+ tests |
| End-to-End | 20% | 5+ tests |

### 2.3 Herramientas

- **pytest**: Framework principal de testing
- **pytest-mock**: Mocks de dependencias
- **pytest-cov**: Medicion de cobertura
- **pytest-timeout**: Control de timeouts para loops
- **unittest.mock**: Mocks de sockets/archivos

---

## 3. Pruebas Unitarias

### 3.1 Entidades

#### 3.1.1 Bateria (`entidades/bateria.py`)

| ID | Caso de Prueba | Entrada | Resultado Esperado |
|----|----------------|---------|-------------------|
| BAT-001 | Carga sobre umbral | nivel=4.5, max=5, umbral=0.8 | indicador="NORMAL" |
| BAT-002 | Carga igual a umbral | nivel=4.0, max=5, umbral=0.8 | indicador="BAJA" |
| BAT-003 | Carga bajo umbral | nivel=3.9, max=5, umbral=0.8 | indicador="BAJA" |
| BAT-004 | Carga cero | nivel=0 | indicador="BAJA" |
| BAT-005 | Carga maxima | nivel=5, max=5 | indicador="NORMAL" |
| BAT-006 | Valor limite inferior | nivel=0.01 | indicador="BAJA" |

```python
# Ejemplo de implementacion
def test_bateria_carga_sobre_umbral():
    bateria = Bateria(carga_maxima=5, umbral=0.8)
    bateria.nivel_de_carga = 4.5
    assert bateria.indicador == "NORMAL"

def test_bateria_carga_bajo_umbral():
    bateria = Bateria(carga_maxima=5, umbral=0.8)
    bateria.nivel_de_carga = 3.9
    assert bateria.indicador == "BAJA"
```

#### 3.1.2 Ambiente (`entidades/ambiente.py`)

| ID | Caso de Prueba | Entrada | Resultado Esperado |
|----|----------------|---------|-------------------|
| AMB-001 | Inicializacion por defecto | - | temp_ambiente=0, temp_deseada=0 |
| AMB-002 | Setear temperatura ambiente | temp=25.5 | temperatura_ambiente=25.5 |
| AMB-003 | Setear temperatura deseada | temp=22.0 | temperatura_deseada=22.0 |
| AMB-004 | Cambiar temperatura a mostrar | "deseada" | temperatura_a_mostrar="deseada" |
| AMB-005 | Temperatura negativa | temp=-5.0 | temperatura_ambiente=-5.0 |

#### 3.1.3 Climatizador (`entidades/climatizador.py`)

**Maquina de Estados - Climatizador (calienta/enfria)**

| ID | Estado Inicial | Accion | Estado Final |
|----|---------------|--------|--------------|
| CLI-001 | apagado | calentar | calentando |
| CLI-002 | apagado | enfriar | enfriando |
| CLI-003 | calentando | apagar | apagado |
| CLI-004 | enfriando | apagar | apagado |
| CLI-005 | calentando | enfriar | enfriando |
| CLI-006 | enfriando | calentar | calentando |
| CLI-007 | apagado | None | apagado (sin cambio) |

**Maquina de Estados - Calefactor (solo calienta)**

| ID | Estado Inicial | Accion | Estado Final |
|----|---------------|--------|--------------|
| CAL-001 | apagado | calentar | calentando |
| CAL-002 | calentando | apagar | apagado |
| CAL-003 | apagado | enfriar | apagado (accion ignorada) |
| CAL-004 | calentando | enfriar | calentando (accion ignorada) |

**Evaluacion de Accion**

| ID | Estado | Temperatura | Accion Esperada |
|----|--------|-------------|-----------------|
| EVA-001 | apagado | baja | calentar |
| EVA-002 | apagado | alta | enfriar |
| EVA-003 | apagado | normal | None |
| EVA-004 | calentando | normal | apagar |
| EVA-005 | calentando | alta | apagar |
| EVA-006 | enfriando | normal | apagar |
| EVA-007 | enfriando | baja | apagar |

```python
# Ejemplo de implementacion
def test_climatizador_transicion_apagado_a_calentando():
    climatizador = Climatizador()
    assert climatizador.estado == "apagado"
    climatizador.proximo_estado("calentar")
    assert climatizador.estado == "calentando"

def test_calefactor_ignora_accion_enfriar():
    calefactor = Calefactor()
    calefactor.proximo_estado("enfriar")
    assert calefactor.estado == "apagado"  # No cambia
```

### 3.2 Servicios de Dominio

#### 3.2.1 ControladorTemperatura (`servicios_dominio/controlador_climatizador.py`)

| ID | Temp Actual | Temp Deseada | Resultado | Descripcion |
|----|-------------|--------------|-----------|-------------|
| CTR-001 | 22 | 22 | "normal" | Temperaturas iguales |
| CTR-002 | 24 | 22 | "normal" | Dentro de histeresis (+2) |
| CTR-003 | 25 | 22 | "alta" | Sobre histeresis (+3) |
| CTR-004 | 20 | 22 | "normal" | Dentro de histeresis (-2) |
| CTR-005 | 19 | 22 | "baja" | Bajo histeresis (-3) |
| CTR-006 | 0 | 0 | "normal" | Valores cero |
| CTR-007 | -5 | 0 | "baja" | Valores negativos |
| CTR-008 | 100 | 50 | "alta" | Valores grandes |

```python
# Ejemplo con parametrizacion
@pytest.mark.parametrize("actual,deseada,esperado", [
    (22, 22, "normal"),
    (25, 22, "alta"),
    (19, 22, "baja"),
    (24, 22, "normal"),  # limite superior
    (20, 22, "normal"),  # limite inferior
])
def test_comparar_temperatura(actual, deseada, esperado):
    resultado = ControladorTemperatura.comparar_temperatura(actual, deseada)
    assert resultado == esperado
```

### 3.3 Factories

#### 3.3.1 FactoryProxyBateria

| ID | Tipo | Resultado Esperado |
|----|------|-------------------|
| FPB-001 | "archivo" | ProxyBateriaArchivo |
| FPB-002 | "socket" | ProxyBateriaSocket |
| FPB-003 | "invalido" | None |
| FPB-004 | "" | None |

#### 3.3.2 FactoryClimatizador

| ID | Tipo | Resultado Esperado |
|----|------|-------------------|
| FCL-001 | "climatizador" | Climatizador |
| FCL-002 | "calefactor" | Calefactor |
| FCL-003 | "invalido" | None |

#### 3.3.3 FactoryVisualizador*

| ID | Tipo | Resultado Esperado |
|----|------|-------------------|
| FVI-001 | "consola" | Visualizador* (consola) |
| FVI-002 | "socket" | Visualizador*Socket |
| FVI-003 | "api" | Visualizador*Api |
| FVI-004 | "invalido" | None |

### 3.4 Configurador

| ID | Caso de Prueba | Resultado Esperado |
|----|----------------|-------------------|
| CFG-001 | JSON valido | Configuracion cargada |
| CFG-002 | Archivo no existe | FileNotFoundError |
| CFG-003 | JSON malformado | JSONDecodeError |
| CFG-004 | Clave faltante | KeyError |

---

## 4. Pruebas de Integracion

### 4.1 Gestores con Dependencias

#### 4.1.1 GestorBateria

| ID | Escenario | Mocks | Validacion |
|----|-----------|-------|------------|
| GBI-001 | Lectura exitosa | ProxyBateria retorna 4.5 | nivel_de_carga=4.5, indicador="NORMAL" |
| GBI-002 | Proxy retorna None | ProxyBateria retorna None | nivel_de_carga=None |
| GBI-003 | Proxy lanza excepcion | ProxyBateria lanza IOError | Excepcion manejada |
| GBI-004 | Visualizacion correcta | Mock de Visualizador | mostrar_tension() invocado |

```python
# Ejemplo con mocks
def test_gestor_bateria_lectura_exitosa(mocker):
    mock_proxy = mocker.Mock()
    mock_proxy.leer_carga.return_value = 4.5
    mock_visualizador = mocker.Mock()

    gestor = GestorBateria(mock_proxy, mock_visualizador)
    gestor.verificar_nivel_de_carga()

    assert gestor.obtener_nivel_de_carga() == 4.5
    assert gestor.obtener_indicador_de_carga() == "NORMAL"
```

#### 4.1.2 GestorAmbiente

| ID | Escenario | Mocks | Validacion |
|----|-----------|-------|------------|
| GAM-001 | Lectura temperatura exitosa | Proxy retorna 25.0 | temperatura_ambiente=25.0 |
| GAM-002 | Sensor no disponible | Proxy lanza Exception | temperatura_ambiente=None |
| GAM-003 | Aumentar temperatura | - | temperatura_deseada += 1 |
| GAM-004 | Disminuir temperatura | - | temperatura_deseada -= 1 |
| GAM-005 | Mostrar temp ambiente | Mock visualizador | mostrar_temperatura_ambiente() invocado |
| GAM-006 | Mostrar temp deseada | Mock visualizador | mostrar_temperatura_deseada() invocado |

#### 4.1.3 GestorClimatizador

| ID | Escenario | Estado Inicial | Ambiente | Resultado |
|----|-----------|---------------|----------|-----------|
| GCL-001 | Activar calefaccion | apagado | temp_baja | estado="calentando" |
| GCL-002 | Activar enfriamiento | apagado | temp_alta | estado="enfriando" |
| GCL-003 | Mantener estado | calentando | temp_normal | estado="apagado" |
| GCL-004 | Actuador invocado | apagado | temp_baja | accionar_climatizador("calentar") |

### 4.2 Flujos de Climatizacion

#### 4.2.1 Ciclo Completo de Calefaccion

```
Precondiciones:
- temperatura_ambiente = 18
- temperatura_deseada = 22
- estado_climatizador = "apagado"

Pasos:
1. GestorAmbiente.leer_temperatura_ambiente() -> 18
2. ControladorTemperatura.comparar_temperatura(18, 22) -> "baja"
3. Climatizador.evaluar_accion("baja") -> "calentar"
4. Climatizador.proximo_estado("calentar") -> "calentando"
5. ActuadorClimatizador.accionar_climatizador("calentar")

Postcondiciones:
- estado_climatizador = "calentando"
- archivo "climatizador" contiene "calentar"
- registro_auditoria actualizado
```

#### 4.2.2 Ciclo Completo de Enfriamiento

```
Precondiciones:
- temperatura_ambiente = 28
- temperatura_deseada = 22
- estado_climatizador = "apagado"

Pasos:
1. GestorAmbiente.leer_temperatura_ambiente() -> 28
2. ControladorTemperatura.comparar_temperatura(28, 22) -> "alta"
3. Climatizador.evaluar_accion("alta") -> "enfriar"
4. Climatizador.proximo_estado("enfriar") -> "enfriando"
5. ActuadorClimatizador.accionar_climatizador("enfriar")

Postcondiciones:
- estado_climatizador = "enfriando"
- archivo "climatizador" contiene "enfriar"
```

### 4.3 Proxies

#### 4.3.1 ProxyBateria

| ID | Escenario | Setup | Resultado |
|----|-----------|-------|-----------|
| PBA-001 | Archivo existe | archivo "bateria" con "4.5" | retorna 4.5 |
| PBA-002 | Archivo no existe | sin archivo | retorna None |
| PBA-003 | Socket disponible | servidor en puerto 11000 | lectura exitosa |
| PBA-004 | Socket no disponible | sin servidor | ConnectionError |

#### 4.3.2 ProxySensorTemperatura

| ID | Escenario | Setup | Resultado |
|----|-----------|-------|-----------|
| PST-001 | Archivo existe | archivo "temperatura" con "25.0" | retorna 25.0 |
| PST-002 | Archivo no existe | sin archivo | Exception("Error de Lectura") |
| PST-003 | Socket disponible | servidor en puerto 12000 | lectura exitosa |
| PST-004 | Socket no disponible | sin servidor | ConnectionError |

### 4.4 Visualizadores

| ID | Tipo | Escenario | Validacion |
|----|------|-----------|------------|
| VIS-001 | Consola | mostrar_temperatura(25) | stdout contiene "25" |
| VIS-002 | Socket | mostrar_temperatura(25) | datos enviados a puerto |
| VIS-003 | API | mostrar_temperatura(25) | POST a endpoint correcto |
| VIS-004 | Socket no disponible | mostrar_* | ConnectionError manejado |
| VIS-005 | API no disponible | mostrar_* | RequestException manejado |

---

## 5. Pruebas End-to-End

### 5.1 Inicializacion del Sistema

| ID | Escenario | Precondiciones | Resultado |
|----|-----------|----------------|-----------|
| E2E-001 | Inicio exitoso | Bateria NORMAL, sensor OK | Sistema operativo |
| E2E-002 | Falla por bateria | Bateria BAJA | Sistema no inicia |
| E2E-003 | Falla por sensor | Sensor no disponible | Sistema no inicia |

### 5.2 Ciclo Operacional

| ID | Escenario | Configuracion | Validacion |
|----|-----------|---------------|------------|
| E2E-004 | Ciclo secuencial | OperadorSecuencial | Flujo completo ejecutado |
| E2E-005 | Ciclo paralelo | OperadorParalelo | 5 threads ejecutando |
| E2E-006 | Config Climatizador | climatizador="climatizador" | Calienta y enfria |
| E2E-007 | Config Calefactor | climatizador="calefactor" | Solo calienta |

### 5.3 Configuraciones

| ID | Configuracion | Componentes | Validacion |
|----|---------------|-------------|------------|
| E2E-008 | Todo archivo | proxies=archivo, vis=consola | Sin red |
| E2E-009 | Todo socket | proxies=socket, vis=socket | Comunicacion TCP |
| E2E-010 | Hibrido API | proxies=archivo, vis=api | REST endpoints |

---

## 6. Casos de Error y Excepciones

### 6.1 Errores de I/O

| ID | Componente | Error | Comportamiento Esperado |
|----|------------|-------|------------------------|
| ERR-001 | ProxyBateriaArchivo | FileNotFoundError | Retorna None |
| ERR-002 | ProxySensorTemperatura | IOError | Lanza Exception |
| ERR-003 | ActuadorClimatizador | IOError escritura | Registra en registro_errores |
| ERR-004 | Configurador | FileNotFoundError | Lanza excepcion |

### 6.2 Errores de Conexion

| ID | Componente | Error | Comportamiento Esperado |
|----|------------|-------|------------------------|
| ERR-005 | ProxyBateriaSocket | ConnectionError | Excepcion propagada |
| ERR-006 | VisualizadorSocket | ConnectionError | Print "Intentar de vuelta" |
| ERR-007 | VisualizadorApi | RequestException | Silencioso (sin manejo) |

### 6.3 Errores de Logica

| ID | Componente | Error | Comportamiento Esperado |
|----|------------|-------|------------------------|
| ERR-008 | Climatizador | Transicion invalida | Excepcion o estado sin cambio |
| ERR-009 | Factory | Tipo desconocido | Retorna None |

---

## 7. Estructura de Archivos de Test

```
Test/
|
+-- unit/
|   +-- entidades/
|   |   +-- test_bateria.py
|   |   +-- test_ambiente.py
|   |   +-- test_climatizador.py
|   |
|   +-- servicios_dominio/
|   |   +-- test_controlador_temperatura.py
|   |
|   +-- configurador/
|   |   +-- test_configurador.py
|   |   +-- test_factories.py
|   |
|   +-- servicios_aplicacion/
|       +-- test_inicializador.py
|
+-- integration/
|   +-- gestores/
|   |   +-- test_gestor_bateria.py
|   |   +-- test_gestor_ambiente.py
|   |   +-- test_gestor_climatizador.py
|   |
|   +-- flujos/
|   |   +-- test_ciclo_climatizacion.py
|   |   +-- test_presentador.py
|   |
|   +-- adaptadores/
|       +-- test_proxies.py
|       +-- test_visualizadores.py
|
+-- e2e/
|   +-- test_inicializacion.py
|   +-- test_ciclo_operacional.py
|   +-- test_configuraciones.py
|
+-- fixtures/
|   +-- conftest.py
|   +-- mock_proxies.py
|   +-- mock_visualizadores.py
|   +-- datos_prueba.json
|
+-- pytest.ini
```

---

## 8. Fixtures y Mocks

### 8.1 conftest.py

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_proxy_bateria():
    proxy = Mock()
    proxy.leer_carga.return_value = 4.5
    return proxy

@pytest.fixture
def mock_proxy_temperatura():
    proxy = Mock()
    proxy.leer_temperatura.return_value = 22.0
    return proxy

@pytest.fixture
def mock_visualizador_bateria():
    return Mock()

@pytest.fixture
def mock_visualizador_temperatura():
    return Mock()

@pytest.fixture
def mock_visualizador_climatizador():
    return Mock()

@pytest.fixture
def mock_actuador_climatizador():
    return Mock()

@pytest.fixture
def ambiente_frio():
    from entidades.ambiente import Ambiente
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 18
    ambiente.temperatura_deseada = 22
    return ambiente

@pytest.fixture
def ambiente_caliente():
    from entidades.ambiente import Ambiente
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 28
    ambiente.temperatura_deseada = 22
    return ambiente

@pytest.fixture
def ambiente_normal():
    from entidades.ambiente import Ambiente
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 22
    ambiente.temperatura_deseada = 22
    return ambiente

@pytest.fixture
def archivo_temporal(tmp_path):
    """Crea archivos temporales para tests de proxies"""
    def _crear_archivo(nombre, contenido):
        archivo = tmp_path / nombre
        archivo.write_text(contenido)
        return str(archivo)
    return _crear_archivo
```

### 8.2 Mock de Sockets

```python
@pytest.fixture
def mock_socket(mocker):
    mock = mocker.patch('socket.socket')
    instance = mock.return_value
    instance.recv.return_value = b"25.0"
    return instance
```

---

## 9. Metricas de Exito

| Metrica | Meta | Prioridad |
|---------|------|-----------|
| Cobertura de lineas | >= 80% | Alta |
| Cobertura de ramas | >= 70% | Alta |
| Tests unitarios | >= 50 | Alta |
| Tests integracion | >= 20 | Media |
| Tests E2E | >= 5 | Media |
| Tiempo ejecucion total | < 30 segundos | Media |
| Tests fallidos | 0 | Alta |
| Falsos positivos | 0 | Alta |

---

## 10. Ejecucion de Tests

### 10.1 Comandos

```bash
# Ejecutar todos los tests
pytest Test/ -v

# Ejecutar con cobertura
pytest Test/ --cov=. --cov-report=html

# Ejecutar solo unitarios
pytest Test/unit/ -v

# Ejecutar solo integracion
pytest Test/integration/ -v

# Ejecutar solo E2E
pytest Test/e2e/ -v

# Ejecutar con timeout (para loops)
pytest Test/ --timeout=10

# Ejecutar tests especificos
pytest Test/unit/entidades/test_bateria.py -v

# Ejecutar por marca
pytest -m "not slow" -v
```

### 10.2 pytest.ini

```ini
[pytest]
testpaths = Test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
timeout = 10
```

---

## 11. Cronograma Sugerido

| Fase | Actividad | Duracion |
|------|-----------|----------|
| 1 | Setup pytest y conftest.py | 1 dia |
| 2 | Tests unitarios entidades | 2 dias |
| 3 | Tests unitarios servicios dominio | 1 dia |
| 4 | Tests unitarios factories | 1 dia |
| 5 | Tests integracion gestores | 2 dias |
| 6 | Tests integracion flujos | 2 dias |
| 7 | Tests E2E | 2 dias |
| 8 | Revision y ajustes | 1 dia |
| **Total** | | **12 dias** |

---

## 12. Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigacion |
|--------|---------|------------|
| Loops infinitos en operadores | Tests colgados | Usar pytest-timeout |
| Dependencia de sockets | Tests fragiles | Usar mocks |
| Archivos temporales | Conflictos entre tests | Usar tmp_path fixture |
| Threads en OperadorParalelo | Race conditions | Tests con timeouts y sincronizacion |
| API externa no disponible | Tests fallidos | Mock de requests |

---

## 13. Apendice: Checklist de Implementacion

### Tests Unitarios
- [ ] test_bateria.py (6 casos)
- [ ] test_ambiente.py (5 casos)
- [ ] test_climatizador.py (7 casos maquina estados)
- [ ] test_calefactor.py (4 casos)
- [ ] test_controlador_temperatura.py (8 casos)
- [ ] test_factories.py (12 casos)
- [ ] test_configurador.py (4 casos)

### Tests Integracion
- [ ] test_gestor_bateria.py (4 casos)
- [ ] test_gestor_ambiente.py (6 casos)
- [ ] test_gestor_climatizador.py (4 casos)
- [ ] test_ciclo_climatizacion.py (2 flujos)
- [ ] test_proxies.py (8 casos)
- [ ] test_visualizadores.py (5 casos)

### Tests E2E
- [ ] test_inicializacion.py (3 casos)
- [ ] test_ciclo_operacional.py (4 casos)
- [ ] test_configuraciones.py (3 casos)

### Fixtures
- [ ] conftest.py con fixtures base
- [ ] mock_proxies.py
- [ ] mock_visualizadores.py
