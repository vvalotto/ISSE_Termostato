"""
Tests unitarios para la entidad Ambiente

Casos de prueba del Plan de Pruebas:
- AMB-001: Inicializacion por defecto -> temp_ambiente=0, temp_deseada=0
- AMB-002: Setear temperatura ambiente -> temperatura_ambiente=25.5
- AMB-003: Setear temperatura deseada -> temperatura_deseada=22.0
- AMB-004: Cambiar temperatura a mostrar -> temperatura_a_mostrar="deseada"
- AMB-005: Temperatura negativa -> temperatura_ambiente=-5.0
"""
import pytest
from entidades.ambiente import Ambiente


class TestAmbiente:
    """Tests para la clase Ambiente"""

    # AMB-001: Inicializacion por defecto
    def test_inicializacion_por_defecto(self, ambiente_default):
        """Al crear un Ambiente, los valores deben ser los por defecto"""
        assert ambiente_default.temperatura_ambiente == 0
        assert ambiente_default.temperatura_deseada == 0
        assert ambiente_default.temperatura_a_mostrar == "ambiente"

    # AMB-002: Setear temperatura ambiente
    def test_setear_temperatura_ambiente(self, ambiente_default):
        """Se debe poder setear la temperatura ambiente"""
        ambiente_default.temperatura_ambiente = 25.5
        assert ambiente_default.temperatura_ambiente == 25.5

    # AMB-003: Setear temperatura deseada
    def test_setear_temperatura_deseada(self, ambiente_default):
        """Se debe poder setear la temperatura deseada"""
        ambiente_default.temperatura_deseada = 22.0
        assert ambiente_default.temperatura_deseada == 22.0

    # AMB-004: Cambiar temperatura a mostrar
    def test_cambiar_temperatura_a_mostrar(self, ambiente_default):
        """Se debe poder cambiar la temperatura a mostrar"""
        ambiente_default.temperatura_a_mostrar = "deseada"
        assert ambiente_default.temperatura_a_mostrar == "deseada"

    # AMB-005: Temperatura negativa
    def test_temperatura_negativa(self, ambiente_default):
        """Se deben aceptar temperaturas negativas"""
        ambiente_default.temperatura_ambiente = -5.0
        assert ambiente_default.temperatura_ambiente == -5.0


class TestAmbienteParametrizado:
    """Tests parametrizados para cobertura adicional"""

    @pytest.mark.parametrize("temperatura", [
        0,
        25.5,
        -10,
        100,
        0.1,
        -0.1,
    ])
    def test_temperatura_ambiente_acepta_diversos_valores(self, ambiente_default, temperatura):
        """La temperatura ambiente debe aceptar diversos valores"""
        ambiente_default.temperatura_ambiente = temperatura
        assert ambiente_default.temperatura_ambiente == temperatura

    @pytest.mark.parametrize("temperatura", [
        0,
        22.0,
        18,
        30,
        -5,
    ])
    def test_temperatura_deseada_acepta_diversos_valores(self, ambiente_default, temperatura):
        """La temperatura deseada debe aceptar diversos valores"""
        ambiente_default.temperatura_deseada = temperatura
        assert ambiente_default.temperatura_deseada == temperatura

    @pytest.mark.parametrize("modo", [
        "ambiente",
        "deseada",
    ])
    def test_temperatura_a_mostrar_acepta_modos_validos(self, ambiente_default, modo):
        """La temperatura a mostrar debe aceptar los modos validos"""
        ambiente_default.temperatura_a_mostrar = modo
        assert ambiente_default.temperatura_a_mostrar == modo


class TestAmbienteRepr:
    """Tests para el metodo __repr__"""

    def test_repr_formato_correcto(self, ambiente_default):
        """El __repr__ debe mostrar el formato correcto"""
        ambiente_default.temperatura_ambiente = 25
        ambiente_default.temperatura_deseada = 22
        ambiente_default.temperatura_a_mostrar = "ambiente"

        repr_str = repr(ambiente_default)

        assert "Ambiente: 25" in repr_str
        assert "Deseada: 22" in repr_str
        assert "a mostrar: ambiente" in repr_str
