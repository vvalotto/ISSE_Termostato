"""
Tests unitarios para ControladorTemperatura

Casos de prueba del Plan de Pruebas:
- CTR-001: temp_actual=22, temp_deseada=22 -> "normal" (iguales)
- CTR-002: temp_actual=24, temp_deseada=22 -> "normal" (dentro de histeresis +2)
- CTR-003: temp_actual=25, temp_deseada=22 -> "alta" (sobre histeresis +3)
- CTR-004: temp_actual=20, temp_deseada=22 -> "normal" (dentro de histeresis -2)
- CTR-005: temp_actual=19, temp_deseada=22 -> "baja" (bajo histeresis -3)
- CTR-006: temp_actual=0, temp_deseada=0 -> "normal" (valores cero)
- CTR-007: temp_actual=-5, temp_deseada=0 -> "baja" (valores negativos)
- CTR-008: temp_actual=100, temp_deseada=50 -> "alta" (valores grandes)

Nota: La histeresis es de 2 grados. El rango "normal" es [deseada-2, deseada+2]
      - "alta" cuando actual > deseada + 2
      - "baja" cuando actual < deseada - 2
"""
import pytest
from servicios_dominio.controlador_climatizador import ControladorTemperatura
from configurador.configurador import Configurador


class TestControladorTemperatura:
    """Tests para ControladorTemperatura.comparar_temperatura()"""

    # CTR-001: Temperaturas iguales
    def test_temperaturas_iguales_retorna_normal(self):
        """Cuando las temperaturas son iguales, debe retornar 'normal'"""
        resultado = ControladorTemperatura.comparar_temperatura(22, 22)
        assert resultado == "normal"

    # CTR-002: Dentro de histeresis superior (+2)
    def test_dentro_histeresis_superior_retorna_normal(self):
        """Cuando esta en el limite superior de histeresis, debe retornar 'normal'"""
        resultado = ControladorTemperatura.comparar_temperatura(24, 22)
        assert resultado == "normal"

    # CTR-003: Sobre histeresis (+3)
    def test_sobre_histeresis_retorna_alta(self):
        """Cuando supera la histeresis superior, debe retornar 'alta'"""
        resultado = ControladorTemperatura.comparar_temperatura(25, 22)
        assert resultado == "alta"

    # CTR-004: Dentro de histeresis inferior (-2)
    def test_dentro_histeresis_inferior_retorna_normal(self):
        """Cuando esta en el limite inferior de histeresis, debe retornar 'normal'"""
        resultado = ControladorTemperatura.comparar_temperatura(20, 22)
        assert resultado == "normal"

    # CTR-005: Bajo histeresis (-3)
    def test_bajo_histeresis_retorna_baja(self):
        """Cuando esta bajo la histeresis inferior, debe retornar 'baja'"""
        resultado = ControladorTemperatura.comparar_temperatura(19, 22)
        assert resultado == "baja"

    # CTR-006: Valores cero
    def test_valores_cero_retorna_normal(self):
        """Con valores cero, debe retornar 'normal'"""
        resultado = ControladorTemperatura.comparar_temperatura(0, 0)
        assert resultado == "normal"

    # CTR-007: Valores negativos
    def test_valores_negativos_retorna_baja(self):
        """Con temperatura actual negativa bajo histeresis, debe retornar 'baja'"""
        resultado = ControladorTemperatura.comparar_temperatura(-5, 0)
        assert resultado == "baja"

    # CTR-008: Valores grandes
    def test_valores_grandes_retorna_alta(self):
        """Con valores grandes sobre histeresis, debe retornar 'alta'"""
        resultado = ControladorTemperatura.comparar_temperatura(100, 50)
        assert resultado == "alta"


class TestControladorTemperaturaParametrizado:
    """Tests parametrizados para cobertura completa de casos limite"""

    @pytest.mark.parametrize("actual,deseada,esperado", [
        # Casos del plan
        (22, 22, "normal"),   # CTR-001: iguales
        (24, 22, "normal"),   # CTR-002: limite superior histeresis
        (25, 22, "alta"),     # CTR-003: sobre histeresis
        (20, 22, "normal"),   # CTR-004: limite inferior histeresis
        (19, 22, "baja"),     # CTR-005: bajo histeresis
        (0, 0, "normal"),     # CTR-006: ceros
        (-5, 0, "baja"),      # CTR-007: negativos
        (100, 50, "alta"),    # CTR-008: grandes
        # Casos limite adicionales
        (24.01, 22, "alta"),  # Justo sobre limite superior
        (19.99, 22, "baja"),  # Justo bajo limite inferior
        (23, 22, "normal"),   # Dentro del rango
        (21, 22, "normal"),   # Dentro del rango
        (-3, 0, "baja"),      # Exactamente en limite inferior con cero
        (3, 0, "alta"),       # Sobre limite superior con cero
        (2, 0, "normal"),     # En limite superior con cero
        (-2, 0, "normal"),    # En limite inferior con cero
    ])
    def test_comparar_temperatura(self, actual, deseada, esperado):
        """Verifica el resultado para diferentes combinaciones de temperaturas"""
        resultado = ControladorTemperatura.comparar_temperatura(actual, deseada)
        assert resultado == esperado


class TestControladorTemperaturaHisteresis:
    """Tests para verificar el valor de histeresis"""

    def test_histeresis_configurada_es_dos(self):
        """La histeresis configurada debe ser 2"""
        assert Configurador.obtener_histeresis() == 2.0

    def test_limite_exacto_superior_es_normal(self):
        """El limite exacto superior (deseada + histeresis) debe ser 'normal'"""
        # Con deseada=20 y histeresis=2, el limite superior es 22
        # actual=22 debe ser "normal", actual=22.01 debe ser "alta"
        assert ControladorTemperatura.comparar_temperatura(22, 20) == "normal"
        assert ControladorTemperatura.comparar_temperatura(22.01, 20) == "alta"

    def test_limite_exacto_inferior_es_normal(self):
        """El limite exacto inferior (deseada - histeresis) debe ser 'normal'"""
        # Con deseada=20 y histeresis=2, el limite inferior es 18
        # actual=18 debe ser "normal", actual=17.99 debe ser "baja"
        assert ControladorTemperatura.comparar_temperatura(18, 20) == "normal"
        assert ControladorTemperatura.comparar_temperatura(17.99, 20) == "baja"
