"""
Tests unitarios para servicios_aplicacion/inicializador.py

Casos de prueba:
- INI-001: Bateria NORMAL y sensor disponible -> retorna True (happy path)
- INI-002: Bateria no NORMAL -> retorna False sin continuar (cortocircuito)
- INI-003: Sensor devuelve None -> retorna False (cortocircuito)
- INI-004: Temperatura deseada se fija en 24 al inicio
- INI-005: Presentador se ejecuta si todo es correcto
"""
import pytest
from unittest.mock import Mock, patch
from servicios_aplicacion.inicializador import Inicializador


@pytest.fixture
def mocks_ok():
    """Gestores y presentador configurados para inicializacion exitosa"""
    gestor_bateria = Mock()
    gestor_bateria.obtener_indicador_de_carga.return_value = "NORMAL"

    gestor_ambiente = Mock()
    gestor_ambiente.obtener_temperatura_ambiente.return_value = 22.5

    presentador = Mock()
    return gestor_bateria, gestor_ambiente, presentador


class TestInicializador:

    # INI-001
    def test_iniciar_exitoso_retorna_true(self, mocks_ok):
        """Bateria NORMAL y sensor disponible -> retorna True"""
        gestor_bateria, gestor_ambiente, presentador = mocks_ok
        with patch("os.system"):
            resultado = Inicializador.iniciar(gestor_bateria, gestor_ambiente, presentador)
        assert resultado is True

    # INI-002
    def test_iniciar_bateria_no_normal_retorna_false(self):
        """Bateria no NORMAL -> retorna False sin llamar al presentador"""
        gestor_bateria = Mock()
        gestor_bateria.obtener_indicador_de_carga.return_value = "BAJA"
        gestor_ambiente = Mock()
        presentador = Mock()

        resultado = Inicializador.iniciar(gestor_bateria, gestor_ambiente, presentador)

        assert resultado is False
        presentador.ejecutar.assert_not_called()

    # INI-003
    def test_iniciar_sensor_none_retorna_false(self):
        """Sensor devuelve None -> retorna False sin llamar al presentador"""
        gestor_bateria = Mock()
        gestor_bateria.obtener_indicador_de_carga.return_value = "NORMAL"
        gestor_ambiente = Mock()
        gestor_ambiente.obtener_temperatura_ambiente.return_value = None
        presentador = Mock()

        resultado = Inicializador.iniciar(gestor_bateria, gestor_ambiente, presentador)

        assert resultado is False
        presentador.ejecutar.assert_not_called()

    # INI-004
    def test_iniciar_fija_temperatura_deseada_en_24(self, mocks_ok):
        """Al iniciar, temperatura_deseada del ambiente se fija en 24"""
        gestor_bateria, gestor_ambiente, presentador = mocks_ok
        with patch("os.system"):
            Inicializador.iniciar(gestor_bateria, gestor_ambiente, presentador)
        assert gestor_ambiente.ambiente.temperatura_deseada == 24

    # INI-005
    def test_iniciar_ejecuta_presentador_si_todo_ok(self, mocks_ok):
        """Si bateria y sensor estan ok, el presentador se ejecuta"""
        gestor_bateria, gestor_ambiente, presentador = mocks_ok
        with patch("os.system"):
            Inicializador.iniciar(gestor_bateria, gestor_ambiente, presentador)
        presentador.ejecutar.assert_called_once()
