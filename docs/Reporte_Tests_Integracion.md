# Reporte de Tests de Integracion - ISSE_Termostato

**Fecha de ejecucion:** 2025-11-24
**Branch:** test/integration
**Framework:** pytest 8.4.2
**Python:** 3.12.0

---

## 1. Resumen Ejecutivo

| Metrica | Valor |
|---------|-------|
| **Tests ejecutados** | 57 |
| **Tests pasados** | 57 |
| **Tests fallidos** | 0 |
| **Tasa de exito** | 100% |
| **Tiempo de ejecucion** | 1.55s |
| **Cobertura (componentes testeados)** | 60% |

---

## 2. Cobertura por Componente

### 2.1 Gestores (Casos de Uso)

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `gestores_entidades/gestor_bateria.py` | 19 | 100% | :white_check_mark: |
| `gestores_entidades/gestor_ambiente.py` | 34 | 100% | :white_check_mark: |
| `gestores_entidades/gestor_climatizador.py` | 15 | 100% | :white_check_mark: |

### 2.2 Agentes Sensores (Proxies)

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `agentes_sensores/proxy_bateria.py` | 29 | 90% | :white_check_mark: |
| `agentes_sensores/proxy_sensor_temperatura.py` | 29 | 45% | :warning: |
| `agentes_sensores/proxy_selector_temperatura.py` | 34 | 29% | :x: |
| `agentes_sensores/proxy_seteo_temperatura.py` | 29 | 28% | :x: |

### 2.3 Agentes Actuadores (Visualizadores)

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `agentes_actuadores/visualizador_temperatura.py` | 40 | 95% | :white_check_mark: |
| `agentes_actuadores/visualizador_climatizador.py` | 21 | 48% | :warning: |
| `agentes_actuadores/visualizador_bateria.py` | 36 | 39% | :warning: |
| `agentes_actuadores/actuador_climatizador.py` | 47 | 26% | :x: |

---

## 3. Detalle de Tests por Modulo

### 3.1 Tests de Gestores (26 tests)

#### test_gestor_bateria.py (8 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| GBI-001 | test_lectura_exitosa_actualiza_nivel_e_indicador | :white_check_mark: PASSED |
| GBI-001 | test_lectura_carga_baja_indicador_baja | :white_check_mark: PASSED |
| GBI-002 | test_proxy_retorna_none | :white_check_mark: PASSED |
| GBI-003 | test_proxy_lanza_excepcion | :white_check_mark: PASSED |
| GBI-004 | test_mostrar_nivel_invoca_visualizador | :white_check_mark: PASSED |
| GBI-004 | test_mostrar_indicador_invoca_visualizador | :white_check_mark: PASSED |
| - | test_flujo_completo_bateria_normal | :white_check_mark: PASSED |
| - | test_flujo_completo_bateria_baja | :white_check_mark: PASSED |

#### test_gestor_ambiente.py (9 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| GAM-001 | test_lectura_temperatura_exitosa | :white_check_mark: PASSED |
| GAM-002 | test_sensor_no_disponible_retorna_none | :white_check_mark: PASSED |
| GAM-003 | test_aumentar_temperatura_deseada | :white_check_mark: PASSED |
| GAM-004 | test_disminuir_temperatura_deseada | :white_check_mark: PASSED |
| GAM-005 | test_mostrar_temperatura_ambiente_invoca_visualizador | :white_check_mark: PASSED |
| GAM-006 | test_mostrar_temperatura_deseada_invoca_visualizador | :white_check_mark: PASSED |
| - | test_mostrar_temperatura_modo_ambiente | :white_check_mark: PASSED |
| - | test_mostrar_temperatura_modo_deseada | :white_check_mark: PASSED |
| - | test_flujo_completo_ajuste_temperatura | :white_check_mark: PASSED |

#### test_gestor_climatizador.py (9 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| GCL-001 | test_activar_calefaccion_cuando_temperatura_baja | :white_check_mark: PASSED |
| GCL-002 | test_activar_enfriamiento_cuando_temperatura_alta | :white_check_mark: PASSED |
| GCL-003 | test_mantener_apagado_cuando_temperatura_normal | :white_check_mark: PASSED |
| GCL-004 | test_mostrar_estado_invoca_visualizador | :white_check_mark: PASSED |
| - | test_calefactor_calienta_cuando_temperatura_baja | :white_check_mark: PASSED |
| - | test_calefactor_no_enfria_cuando_temperatura_alta | :white_check_mark: PASSED |
| - | test_ciclo_calentar_y_apagar_por_temperatura_alta | :white_check_mark: PASSED |
| - | test_ciclo_enfriar_y_apagar_por_temperatura_baja | :white_check_mark: PASSED |
| - | test_calentando_mantiene_estado_en_temperatura_normal | :white_check_mark: PASSED |

### 3.2 Tests de Flujos (6 tests)

#### test_ciclo_climatizacion.py

| Escenario | Test | Estado |
|-----------|------|--------|
| Calefaccion | test_ciclo_calefaccion_desde_temperatura_baja | :white_check_mark: PASSED |
| Enfriamiento | test_ciclo_enfriamiento_desde_temperatura_alta | :white_check_mark: PASSED |
| Sin accion | test_ciclo_sin_accion_temperatura_normal | :white_check_mark: PASSED |
| Calefactor frio | test_calefactor_calienta_temperatura_baja | :white_check_mark: PASSED |
| Calefactor caliente | test_calefactor_no_enfria_temperatura_alta | :white_check_mark: PASSED |
| Ciclo completo | test_ciclo_completo_frio_a_caliente | :white_check_mark: PASSED |

### 3.3 Tests de Adaptadores (25 tests)

#### test_proxies.py (11 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| PBA-001 | test_leer_carga_archivo_existe | :white_check_mark: PASSED |
| PBA-001 | test_leer_carga_valores_diversos | :white_check_mark: PASSED |
| PBA-002 | test_leer_carga_archivo_no_existe | :white_check_mark: PASSED |
| PBA-002 | test_leer_carga_error_io | :white_check_mark: PASSED |
| PBA-003 | test_leer_carga_socket_mock | :white_check_mark: PASSED |
| PBA-004 | test_leer_carga_socket_error_bind | :white_check_mark: PASSED |
| PST-001 | test_leer_temperatura_archivo_existe | :white_check_mark: PASSED |
| PST-001 | test_leer_temperatura_valores_diversos | :white_check_mark: PASSED |
| PST-002 | test_leer_temperatura_archivo_no_existe | :white_check_mark: PASSED |
| - | test_proxy_bateria_con_archivo_temporal | :white_check_mark: PASSED |
| - | test_proxy_temperatura_con_archivo_temporal | :white_check_mark: PASSED |

#### test_visualizadores.py (14 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| VIS-001 | test_mostrar_temperatura_ambiente_imprime_valor | :white_check_mark: PASSED |
| VIS-001 | test_mostrar_temperatura_deseada_imprime_valor | :white_check_mark: PASSED |
| VIS-001 | test_mostrar_temperaturas_diversas | :white_check_mark: PASSED |
| VIS-002 | test_mostrar_temperatura_ambiente_envia_a_socket | :white_check_mark: PASSED |
| VIS-002 | test_mostrar_temperatura_deseada_envia_a_socket | :white_check_mark: PASSED |
| VIS-002 | test_formato_mensaje_ambiente | :white_check_mark: PASSED |
| VIS-002 | test_formato_mensaje_deseada | :white_check_mark: PASSED |
| VIS-003 | test_mostrar_temperatura_ambiente_hace_post | :white_check_mark: PASSED |
| VIS-003 | test_mostrar_temperatura_deseada_hace_post | :white_check_mark: PASSED |
| VIS-003 | test_post_con_diferentes_valores | :white_check_mark: PASSED |
| VIS-004 | test_socket_no_disponible_maneja_error | :white_check_mark: PASSED |
| VIS-005 | test_api_no_disponible_lanza_excepcion | :white_check_mark: PASSED |
| - | test_todos_los_visualizadores_aceptan_enteros | :white_check_mark: PASSED |
| - | test_todos_los_visualizadores_aceptan_floats | :white_check_mark: PASSED |

---

## 4. Estructura de Archivos de Test

```
Test/integration/
├── __init__.py
├── conftest.py                              # Fixtures compartidas
├── gestores/
│   ├── __init__.py
│   ├── test_gestor_bateria.py               # 8 tests
│   ├── test_gestor_ambiente.py              # 9 tests
│   └── test_gestor_climatizador.py          # 9 tests
├── flujos/
│   ├── __init__.py
│   └── test_ciclo_climatizacion.py          # 6 tests
└── adaptadores/
    ├── __init__.py
    ├── test_proxies.py                      # 11 tests
    └── test_visualizadores.py               # 14 tests
```

---

## 5. Observaciones del Comportamiento

### 5.1 Comportamiento del Climatizador

Durante las pruebas se identifico el siguiente comportamiento:

| Situacion | Comportamiento |
|-----------|----------------|
| Calentando + temp normal | **No se apaga** (mantiene estado) |
| Calentando + temp alta | Se apaga |
| Enfriando + temp normal | **No se apaga** (mantiene estado) |
| Enfriando + temp baja | Se apaga |

**Nota:** El climatizador solo se apaga cuando la temperatura pasa al extremo opuesto, no cuando alcanza el rango normal.

### 5.2 Proxy de Temperatura

El `ProxySensorTemperaturaArchivo` usa `int()` para leer valores, no `float()`. Los tests fueron ajustados para reflejar este comportamiento.

---

## 6. Metricas vs Objetivos

| Metrica | Objetivo (Plan) | Actual | Estado |
|---------|-----------------|--------|--------|
| Tests integracion | >= 20 | 57 | :white_check_mark: Cumplido |
| Gestores testeados | 100% | 100% | :white_check_mark: Cumplido |
| Tests fallidos | 0 | 0 | :white_check_mark: Cumplido |
| Tiempo ejecucion | < 30s | 1.55s | :white_check_mark: Cumplido |

---

## 7. Cobertura Pendiente

Componentes con baja cobertura que podrian requerir tests adicionales:

| Componente | Cobertura | Motivo |
|------------|-----------|--------|
| `actuador_climatizador.py` | 26% | Requiere mocks de archivos/sockets |
| `proxy_selector_temperatura.py` | 29% | No usado en flujos principales |
| `proxy_seteo_temperatura.py` | 28% | No usado en flujos principales |

---

## 8. Comando de Ejecucion

```bash
# Ejecutar todos los tests de integracion
python -m pytest Test/integration/ -v

# Ejecutar con cobertura
python -m pytest Test/integration/ -v --cov=gestores_entidades --cov=agentes_sensores --cov=agentes_actuadores --cov-report=html

# Ejecutar por categoria
python -m pytest Test/integration/gestores/ -v
python -m pytest Test/integration/flujos/ -v
python -m pytest Test/integration/adaptadores/ -v
```

---

## 9. Resumen Total del Proyecto

| Nivel | Tests | Cobertura |
|-------|-------|-----------|
| Unitarios | 117 | 84% |
| Integracion | 57 | 60% |
| **Total** | **174** | - |

---

*Reporte generado automaticamente*
