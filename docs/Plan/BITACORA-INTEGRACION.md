# Bitácora de Testing de Integración — ISSE Termostato

Seguimiento de los tests de integración pendientes identificados tras completar el plan de cobertura.

**Cobertura actual:** 82% | **Objetivo:** ≥ 85%
**Creación:** 2026-03-07

---

## Contexto

El plan de testing anterior (`PLAN-TESTING.md`) cubrió adaptadores, gestores y flujos de climatización.
Quedan sin tests de integración los módulos de orquestación de `servicios_aplicacion/`:

| Módulo | Cobertura actual | Problema |
|--------|-----------------|----------|
| `operador_secuencial.py` | 39% | Solo constructor. `ejecutar()` no cubierto (loop infinito) |
| `operador_paralelo.py` | 0% | Sin ningún test (threads con loops infinitos) |
| `lanzador.py` | 0% | Composition Root. Depende de `Configurador` y toda la infraestructura |
| `registrador/` + `actuador_climatizador` | — | Sin test de integración cruzado entre capas |

---

## Estado general

| ID | Descripción | Tests | Estado |
|----|-------------|-------|--------|
| INT-1 | `OperadorSecuencial.ejecutar()` — ciclo principal con mocks | 5 | Pendiente |
| INT-2 | `OperadorParalelo` — constructor, threads y métodos individuales | 8 | Pendiente |
| INT-3 | `Lanzador` — Composition Root con `Configurador` mockeado | 4 | Pendiente |
| INT-4 | `Registrador` + `ActuadorClimatizador` — integración cruzada | 3 | Pendiente |

**Total:** 20 tests nuevos

---

## Detalle de tareas

---

### INT-1 — OperadorSecuencial.ejecutar()

**Archivo:** `Test/integration/servicios/test_operador_secuencial_integracion.py`

**Estrategia:** Parchear `time.sleep` con `side_effect` que lanza `StopIteration` luego de N llamadas.
Envolver `operador.ejecutar()` en `pytest.raises(StopIteration)`. También parchear `os.system`.

**Prerequisito:** Configurador mockeado en `patch("servicios_aplicacion.selector_entrada.Configurador")`.

| ID | Nombre del test | Qué verifica |
|----|-----------------|--------------|
| OPS-INT-001 | `test_ejecutar_llama_verificar_nivel_de_carga` | En una iteración se llama `gestor_bateria.verificar_nivel_de_carga()` |
| OPS-INT-002 | `test_ejecutar_llama_leer_temperatura_ambiente` | En una iteración se llama `gestor_ambiente.leer_temperatura_ambiente()` |
| OPS-INT-003 | `test_ejecutar_llama_selector_ejecutar` | En una iteración se llama `_selector.ejecutar()` |
| OPS-INT-004 | `test_ejecutar_llama_accionar_climatizador` | En una iteración se llama `gestor_climatizador.accionar_climatizador(ambiente)` |
| OPS-INT-005 | `test_ejecutar_llama_presentador_ejecutar` | En una iteración se llama `_presentador.ejecutar()` |

**Patrón de fixture:**
```python
@pytest.fixture
def operador_integrado():
    gestor_bateria = Mock()
    gestor_ambiente = Mock()
    gestor_climatizador = Mock()
    with patch("servicios_aplicacion.selector_entrada.Configurador") as cfg:
        cfg.configurar_seteo_temperatura.return_value = Mock()
        cfg.configurar_selector_temperatura.return_value = Mock()
        op = OperadorSecuencial(gestor_bateria, gestor_ambiente, gestor_climatizador)
    return op, gestor_bateria, gestor_ambiente, gestor_climatizador

# En cada test:
with patch("time.sleep"), patch("os.system"):
    with patch.object(op._selector, "ejecutar"):
        with pytest.raises(StopIteration):
            with patch("time.sleep", side_effect=[None]*4 + [StopIteration()]):
                op.ejecutar()
```

---

### INT-2 — OperadorParalelo

**Archivo:** `Test/integration/servicios/test_operador_paralelo_integracion.py`

**Estrategia para constructor:** igual que OperadorSecuencial (parchear Configurador).
**Estrategia para `ejecutar()`:** parchear `threading.Thread` con Mock; verificar que se crearon 5 threads y se llamó `start()` en cada uno.
**Estrategia para métodos individuales:** parchear `time.sleep` con `side_effect=[StopIteration()]` para ejecutar exactamente una iteración del loop.

| ID | Nombre del test | Qué verifica |
|----|-----------------|--------------|
| OPP-INT-001 | `test_constructor_asigna_gestores` | `_gestor_bateria`, `_gestor_ambiente`, `_gestor_climatizador` asignados |
| OPP-INT-002 | `test_constructor_crea_selector_y_presentador` | `isinstance(_selector, SelectorEntradaTemperatura)` y `isinstance(_presentador, Presentador)` |
| OPP-INT-003 | `test_ejecutar_crea_cinco_threads` | `threading.Thread` llamado 5 veces |
| OPP-INT-004 | `test_ejecutar_inicia_todos_los_threads` | `hilo.start()` llamado en cada thread creado |
| OPP-INT-005 | `test_lee_carga_bateria_llama_verificar_nivel` | `gestor_bateria.verificar_nivel_de_carga()` llamado en 1 iteración |
| OPP-INT-006 | `test_lee_temperatura_ambiente_llama_gestor` | `gestor_ambiente.leer_temperatura_ambiente()` llamado en 1 iteración |
| OPP-INT-007 | `test_acciona_climatizador_llama_gestor` | `gestor_climatizador.accionar_climatizador(ambiente)` llamado en 1 iteración |
| OPP-INT-008 | `test_muestra_parametros_llama_presentador` | `_presentador.ejecutar()` llamado en 1 iteración |

**Patrón para OPP-INT-003/004:**
```python
with patch("threading.Thread") as mock_thread_cls:
    mock_thread_cls.return_value = Mock()
    operador.ejecutar()
assert mock_thread_cls.call_count == 5
assert mock_thread_cls.return_value.start.call_count == 5
```

**Patrón para OPP-INT-005..008:**
```python
with patch("time.sleep", side_effect=StopIteration()):
    with pytest.raises(StopIteration):
        operador.lee_carga_bateria()
gestor_bateria.verificar_nivel_de_carga.assert_called_once()
```

---

### INT-3 — Lanzador (Composition Root)

**Archivo:** `Test/integration/servicios/test_lanzador_integracion.py`

**Estrategia:** Parchear `Configurador` completo (todos los métodos `configurar_*` y `obtener_*`) para que devuelvan Mocks. También parchear `VisualizadorEstadoConsolidadoSocket` para evitar socket real.

| ID | Nombre del test | Qué verifica |
|----|-----------------|--------------|
| LNZ-INT-001 | `test_constructor_crea_tres_gestores` | `_gestor_bateria`, `_gestor_ambiente`, `_gestor_climatizador` son instancias correctas |
| LNZ-INT-002 | `test_constructor_crea_presentador_y_operador` | `_presentador` es `Presentador`, `_operador` es `OperadorParalelo` |
| LNZ-INT-003 | `test_ejecutar_llama_inicializador_iniciar` | `Inicializador.iniciar` llamado con los 3 gestores |
| LNZ-INT-004 | `test_ejecutar_llama_operador_si_inicializacion_ok` | Si `Inicializador.iniciar` retorna True, se llama `_operador.ejecutar()` |

**Patrón:**
```python
with patch.multiple("configurador.configurador.Configurador",
    cargar_configuracion=Mock(),
    configurar_proxy_bateria=Mock(return_value=Mock()),
    configurar_visualizador_bateria=Mock(return_value=Mock()),
    configurar_proxy_temperatura=Mock(return_value=Mock()),
    ...
):
    with patch("agentes_actuadores.visualizador_estado_consolidado.socket.socket"):
        lanzador = Lanzador()
```

---

### INT-4 — Registrador + ActuadorClimatizador (integración cruzada)

**Archivo:** `Test/integration/servicios/test_registrador_actuador_integracion.py`

**Estrategia:** Instanciar `RegistradorArchivo` y `AuditorArchivo` reales con archivos temporales (`tmp_path`). Instanciar `ActuadorClimatizadorGeneral` con esas dependencias reales. Verificar que tras llamar `accionar`, los archivos de registro contengan las entradas esperadas.

| ID | Nombre del test | Qué verifica |
|----|-----------------|--------------|
| REG-ACT-001 | `test_actuador_escribe_en_archivo_registrador` | Tras `accionar("calentando")`, el archivo de registro contiene la acción |
| REG-ACT-002 | `test_actuador_escribe_en_archivo_auditor` | Tras `accionar("calentando")`, el archivo de auditoría contiene `"ActuadorClimatizadorGeneral"` |
| REG-ACT-003 | `test_actuador_apagar_registra_en_ambos_archivos` | Tras `accionar("apagado")`, ambos archivos tienen entradas |

**Patrón:**
```python
def test_actuador_escribe_en_archivo_registrador(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    registrador = RegistradorArchivo()
    auditor = AuditorArchivo()
    actuador = ActuadorClimatizadorGeneral(registrador, auditor)
    actuador.accionar("calentando")
    contenido = (tmp_path / "climatizador").read_text()
    assert "calentando" in contenido
```

---

## Orden de implementación

```
INT-1 → INT-2 → INT-4 → INT-3
```

- INT-1 primero: patrón más simple (un loop, sin threads)
- INT-2 segundo: extiende el patrón con threads
- INT-4 tercero: no depende de operadores, usa archivos reales
- INT-3 último: más complejo (requiere mockear todo Configurador)

**Branch sugerido:** `testing/integracion-servicios`

---

## Registro de actividad

### 2026-03-07
- Creación de la bitácora. 4 tareas, 20 tests en estado `Pendiente`.
