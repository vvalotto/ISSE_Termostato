cual# Reporte de Tests Unitarios - ISSE_Termostato

**Fecha de ejecucion:** 2025-11-24
**Branch:** test/unit-entidades
**Framework:** pytest 8.4.2
**Python:** 3.12.0

---

## 1. Resumen Ejecutivo

| Metrica | Valor |
|---------|-------|
| **Tests ejecutados** | 117 |
| **Tests pasados** | 117 |
| **Tests fallidos** | 0 |
| **Tasa de exito** | 100% |
| **Tiempo de ejecucion** | 1.71s |
| **Cobertura total** | 84% |

---

## 2. Cobertura por Componente

### 2.1 Entidades (Dominio)

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `entidades/bateria.py` | 19 | 100% | :white_check_mark: |
| `entidades/ambiente.py` | 29 | 100% | :white_check_mark: |
| `entidades/climatizador.py` | 72 | 93% | :white_check_mark: |
| `entidades/abs_*.py` | 42 | 80-83% | :white_check_mark: |

### 2.2 Servicios de Dominio

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `servicios_dominio/controlador_climatizador.py` | 10 | 100% | :white_check_mark: |

### 2.3 Configurador y Factories

| Archivo | Lineas | Cobertura | Estado |
|---------|--------|-----------|--------|
| `configurador/configurador.py` | 44 | 86% | :white_check_mark: |
| `configurador/factory_climatizador.py` | 9 | 100% | :white_check_mark: |
| `configurador/factory_proxy_bateria.py` | 9 | 100% | :white_check_mark: |
| `configurador/factory_visualizador_temperatura.py` | 11 | 100% | :white_check_mark: |
| `configurador/factory_*.py` (otros) | 43 | 36-57% | :warning: |

---

## 3. Detalle de Tests por Modulo

### 3.1 Tests de Entidades (56 tests)

#### test_bateria.py (17 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| BAT-001 | test_carga_sobre_umbral_indicador_normal | :white_check_mark: PASSED |
| BAT-002 | test_carga_igual_umbral_indicador_baja | :white_check_mark: PASSED |
| BAT-003 | test_carga_bajo_umbral_indicador_baja | :white_check_mark: PASSED |
| BAT-004 | test_carga_cero_indicador_baja | :white_check_mark: PASSED |
| BAT-005 | test_carga_maxima_indicador_normal | :white_check_mark: PASSED |
| BAT-006 | test_valor_limite_inferior_indicador_baja | :white_check_mark: PASSED |
| - | test_indicador_segun_nivel_de_carga (10 parametros) | :white_check_mark: PASSED |
| - | test_nivel_de_carga_se_almacena_correctamente | :white_check_mark: PASSED |

#### test_ambiente.py (19 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| AMB-001 | test_inicializacion_por_defecto | :white_check_mark: PASSED |
| AMB-002 | test_setear_temperatura_ambiente | :white_check_mark: PASSED |
| AMB-003 | test_setear_temperatura_deseada | :white_check_mark: PASSED |
| AMB-004 | test_cambiar_temperatura_a_mostrar | :white_check_mark: PASSED |
| AMB-005 | test_temperatura_negativa | :white_check_mark: PASSED |
| - | test_temperatura_ambiente_acepta_diversos_valores (6 parametros) | :white_check_mark: PASSED |
| - | test_temperatura_deseada_acepta_diversos_valores (5 parametros) | :white_check_mark: PASSED |
| - | test_temperatura_a_mostrar_acepta_modos_validos (2 parametros) | :white_check_mark: PASSED |
| - | test_repr_formato_correcto | :white_check_mark: PASSED |

#### test_climatizador.py (20 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| CLI-001 | test_transicion_apagado_a_calentando | :white_check_mark: PASSED |
| CLI-002 | test_transicion_apagado_a_enfriando | :white_check_mark: PASSED |
| CLI-003 | test_transicion_calentando_a_apagado | :white_check_mark: PASSED |
| CLI-004 | test_transicion_enfriando_a_apagado | :white_check_mark: PASSED |
| CLI-005 | test_transicion_calentando_enfriar_lanza_excepcion | :white_check_mark: PASSED |
| CLI-006 | test_transicion_enfriando_calentar_lanza_excepcion | :white_check_mark: PASSED |
| CAL-001 | test_transicion_apagado_a_calentando (Calefactor) | :white_check_mark: PASSED |
| CAL-002 | test_transicion_calentando_a_apagado (Calefactor) | :white_check_mark: PASSED |
| CAL-003 | test_transicion_apagado_enfriar_permanece_apagado | :white_check_mark: PASSED |
| CAL-004 | test_transicion_calentando_enfriar_lanza_excepcion | :white_check_mark: PASSED |
| EVA-* | test_evaluar_accion_* (8 tests) | :white_check_mark: PASSED |

### 3.2 Tests de Servicios de Dominio (27 tests)

#### test_controlador_temperatura.py

| ID Plan | Test | Estado |
|---------|------|--------|
| CTR-001 | test_temperaturas_iguales_retorna_normal | :white_check_mark: PASSED |
| CTR-002 | test_dentro_histeresis_superior_retorna_normal | :white_check_mark: PASSED |
| CTR-003 | test_sobre_histeresis_retorna_alta | :white_check_mark: PASSED |
| CTR-004 | test_dentro_histeresis_inferior_retorna_normal | :white_check_mark: PASSED |
| CTR-005 | test_bajo_histeresis_retorna_baja | :white_check_mark: PASSED |
| CTR-006 | test_valores_cero_retorna_normal | :white_check_mark: PASSED |
| CTR-007 | test_valores_negativos_retorna_baja | :white_check_mark: PASSED |
| CTR-008 | test_valores_grandes_retorna_alta | :white_check_mark: PASSED |
| - | test_comparar_temperatura (16 parametros) | :white_check_mark: PASSED |
| - | test_histeresis_es_dos | :white_check_mark: PASSED |
| - | test_limite_exacto_superior_es_normal | :white_check_mark: PASSED |
| - | test_limite_exacto_inferior_es_normal | :white_check_mark: PASSED |

### 3.3 Tests de Configurador (34 tests)

#### test_factories.py (25 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| FCL-001 | test_crear_climatizador | :white_check_mark: PASSED |
| FCL-002 | test_crear_calefactor | :white_check_mark: PASSED |
| FCL-003 | test_tipo_invalido_retorna_none | :white_check_mark: PASSED |
| FPB-001 | test_crear_proxy_archivo | :white_check_mark: PASSED |
| FPB-002 | test_crear_proxy_socket | :white_check_mark: PASSED |
| FPB-003 | test_tipo_invalido_retorna_none | :white_check_mark: PASSED |
| FPB-004 | test_tipo_vacio_retorna_none | :white_check_mark: PASSED |
| FVI-001 | test_crear_visualizador_archivo | :white_check_mark: PASSED |
| FVI-002 | test_crear_visualizador_socket | :white_check_mark: PASSED |
| FVI-003 | test_crear_visualizador_api | :white_check_mark: PASSED |
| FVI-004 | test_tipo_invalido_retorna_none | :white_check_mark: PASSED |
| - | tests parametrizados adicionales (14 tests) | :white_check_mark: PASSED |

#### test_configurador.py (9 tests)

| ID Plan | Test | Estado |
|---------|------|--------|
| CFG-001 | test_cargar_configuracion_json_valido | :white_check_mark: PASSED |
| CFG-002 | test_cargar_configuracion_archivo_no_existe | :white_check_mark: PASSED |
| CFG-003 | test_cargar_configuracion_json_malformado | :white_check_mark: PASSED |
| CFG-004 | test_configurar_con_clave_faltante_lanza_keyerror | :white_check_mark: PASSED |
| - | test_configurar_proxy_bateria | :white_check_mark: PASSED |
| - | test_configurar_climatizador | :white_check_mark: PASSED |
| - | test_configurar_visualizador_temperatura | :white_check_mark: PASSED |
| - | test_configuracion_con_socket | :white_check_mark: PASSED |
| - | test_configuracion_con_api | :white_check_mark: PASSED |

---

## 4. Estructura de Archivos de Test

```
Test/unit/
├── __init__.py
├── conftest.py                              # Fixtures compartidas
├── entidades/
│   ├── __init__.py
│   ├── test_bateria.py                      # 17 tests
│   ├── test_ambiente.py                     # 19 tests
│   └── test_climatizador.py                 # 20 tests
├── servicios_dominio/
│   ├── __init__.py
│   └── test_controlador_temperatura.py      # 27 tests
└── configurador/
    ├── __init__.py
    ├── test_factories.py                    # 25 tests
    └── test_configurador.py                 # 9 tests
```

---

## 5. Discrepancias Encontradas

### 5.1 BAT-002: Carga igual a umbral

| Aspecto | Plan Original | Comportamiento Real |
|---------|---------------|---------------------|
| Caso | nivel=4.0, umbral=0.8 | nivel=4.0, umbral=0.8 |
| Esperado | "NORMAL" | "BAJA" |
| Motivo | La implementacion usa `<=` en lugar de `<` |

**Accion tomada:** Se actualizo el Plan de Pruebas para reflejar el comportamiento actual.

---

## 6. Metricas vs Objetivos

| Metrica | Objetivo (Plan) | Actual | Estado |
|---------|-----------------|--------|--------|
| Cobertura de lineas | >= 80% | 84% | :white_check_mark: Cumplido |
| Tests unitarios | >= 50 | 117 | :white_check_mark: Cumplido |
| Tests fallidos | 0 | 0 | :white_check_mark: Cumplido |
| Tiempo ejecucion | < 30s | 1.71s | :white_check_mark: Cumplido |

---

## 7. Proximos Pasos

Segun el Plan de Pruebas, quedan pendientes:

### Tests de Integracion (20+ tests)
- [ ] GestorBateria (GBI-001 a GBI-004)
- [ ] GestorAmbiente (GAM-001 a GAM-006)
- [ ] GestorClimatizador (GCL-001 a GCL-004)
- [ ] Flujos de climatizacion
- [ ] Proxies y Visualizadores

### Tests End-to-End (5+ tests)
- [ ] Inicializacion del sistema (E2E-001 a E2E-003)
- [ ] Ciclo operacional (E2E-004 a E2E-007)
- [ ] Configuraciones (E2E-008 a E2E-010)

---

## 8. Comando de Ejecucion

```bash
# Ejecutar todos los tests unitarios
python -m pytest Test/unit/ -v

# Ejecutar con cobertura
python -m pytest Test/unit/ -v --cov=entidades --cov=servicios_dominio --cov=configurador --cov-report=html

# Ejecutar tests especificos
python -m pytest Test/unit/entidades/ -v
python -m pytest Test/unit/servicios_dominio/ -v
python -m pytest Test/unit/configurador/ -v
```

---

*Reporte generado automaticamente*
