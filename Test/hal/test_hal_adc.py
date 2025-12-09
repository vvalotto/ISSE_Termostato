"""
Tests unitarios de las implementaciones del HAL ADC
"""
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from hal.hal_adc_simulado import HAL_ADC_Simulado
from hal.hal_adc_mock import HAL_ADC_Mock


def test_hal_adc_simulado_inicializacion():
    """Test: HAL simulado se inicializa correctamente"""
    hal = HAL_ADC_Simulado()
    hal.inicializar()

    # Debería poder leer sin errores
    valor = hal.leer_adc(0)
    assert 0 <= valor <= 1023, f"Valor ADC fuera de rango: {valor}"

    hal.finalizar()
    print("✅ Test HAL simulado inicialización: OK")


def test_hal_adc_simulado_lectura():
    """Test: HAL simulado genera valores dentro del rango esperado"""
    hal = HAL_ADC_Simulado(temperatura_base=22.0, ruido_std=0.5)
    hal.inicializar()

    # Realiza múltiples lecturas
    valores = [hal.leer_adc(0) for _ in range(10)]

    # Verifica que todos estén en rango válido
    for valor in valores:
        assert 0 <= valor <= 1023, f"Valor fuera de rango: {valor}"

    # Verifica que haya variación (no todos iguales)
    assert len(set(valores)) > 1, "Los valores no varían (sin ruido)"

    hal.finalizar()
    print(f"✅ Test HAL simulado lectura: OK (valores: {min(valores)}-{max(valores)})")


def test_hal_adc_simulado_error_sin_inicializar():
    """Test: HAL lanza error si se lee sin inicializar"""
    hal = HAL_ADC_Simulado()

    try:
        hal.leer_adc(0)
        assert False, "Debería haber lanzado IOError"
    except IOError as e:
        assert "no inicializado" in str(e).lower()
        print("✅ Test HAL error sin inicializar: OK")


def test_hal_adc_mock_valores_predefinidos():
    """Test: Mock retorna valores predefinidos correctamente"""
    valores_esperados = [200, 250, 300]
    hal = HAL_ADC_Mock(valores_adc=valores_esperados)
    hal.inicializar()

    # Lee los valores
    valores_leidos = [hal.leer_adc(0) for _ in range(3)]

    assert valores_leidos == valores_esperados, \
        f"Valores leídos {valores_leidos} != esperados {valores_esperados}"

    # Verifica que es circular (vuelve al principio)
    valor_circular = hal.leer_adc(0)
    assert valor_circular == valores_esperados[0], "No es circular"

    hal.finalizar()
    print("✅ Test Mock valores predefinidos: OK")


def test_hal_adc_mock_contador_llamadas():
    """Test: Mock cuenta correctamente las llamadas"""
    hal = HAL_ADC_Mock([100])
    hal.inicializar()

    # Realiza varias lecturas
    for _ in range(5):
        hal.leer_adc(0)

    assert hal.obtener_llamadas_leer() == 5, "Contador de llamadas incorrecto"

    hal.finalizar()
    print("✅ Test Mock contador llamadas: OK")


if __name__ == "__main__":
    print("=== Tests HAL ADC ===\n")

    test_hal_adc_simulado_inicializacion()
    test_hal_adc_simulado_lectura()
    test_hal_adc_simulado_error_sin_inicializar()
    test_hal_adc_mock_valores_predefinidos()
    test_hal_adc_mock_contador_llamadas()

    print("\n✅ Todos los tests HAL pasaron correctamente")
