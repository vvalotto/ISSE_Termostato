"""
Test del gestor de batería con HAL mock
"""
from gestores_entidades.gestor_bateria import GestorBateria
from hal.hal_adc_mock import HAL_ADC_Mock

print("=== Test Gestor Batería con HAL ===\n")

# Test con diferentes niveles de carga
niveles_test = [
    (1023, 5.0, "NORMAL"),   # 100% carga → NORMAL
    (819, 4.0, "NORMAL"),    # 80% carga → NORMAL (justo en el límite, pero > 80%)
    (716, 3.5, "BAJA"),      # 70% carga → BAJA
    (512, 2.5, "BAJA"),      # 50% carga → BAJA
    (205, 1.0, "BAJA"),      # 20% carga → BAJA
]

for adc, carga_esperada, indicador_esperado in niveles_test:
    hal_mock = HAL_ADC_Mock(valores_adc=[adc])
    gestor = GestorBateria(hal_adc=hal_mock)

    gestor.verificar_nivel_de_carga()
    nivel = gestor.obtener_nivel_de_carga()
    indicador = gestor.obtener_indicador_de_carga()

    print(f"ADC={adc} → Carga={nivel:.2f}V, Indicador={indicador}")

    # Verifica valores aproximados
    assert abs(nivel - carga_esperada) < 0.1, f"Carga incorrecta: {nivel} vs {carga_esperada}"
    assert indicador == indicador_esperado, f"Indicador incorrecto: {indicador} vs {indicador_esperado}"

print("\n✅ Todos los tests de batería pasaron correctamente")
