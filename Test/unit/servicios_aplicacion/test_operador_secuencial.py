"""
Tests unitarios para servicios_aplicacion/operador_secuencial.py

Casos de prueba:
- OPR-001: Constructor asigna gestores correctamente
- OPR-002: Constructor crea _selector (SelectorEntradaTemperatura) y _presentador (Presentador)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from servicios_aplicacion.operador_secuencial import OperadorSecuencial
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador


@pytest.fixture
def operador_con_mocks():
    """OperadorSecuencial con Configurador mockeado para evitar acceso a infraestructura"""
    gestor_bateria = Mock()
    gestor_ambiente = Mock()
    gestor_climatizador = Mock()

    mock_seteo = Mock()
    mock_selector_temp = Mock()

    with patch("servicios_aplicacion.selector_entrada.Configurador") as mock_cfg:
        mock_cfg.configurar_seteo_temperatura.return_value = mock_seteo
        mock_cfg.configurar_selector_temperatura.return_value = mock_selector_temp
        operador = OperadorSecuencial(gestor_bateria, gestor_ambiente, gestor_climatizador)

    return operador, gestor_bateria, gestor_ambiente, gestor_climatizador


class TestOperadorSecuencial:

    # OPR-001
    def test_constructor_asigna_gestores(self, operador_con_mocks):
        """Constructor asigna _gestor_bateria, _gestor_ambiente y _gestor_climatizador"""
        operador, gestor_bateria, gestor_ambiente, gestor_climatizador = operador_con_mocks
        assert operador._gestor_bateria is gestor_bateria
        assert operador._gestor_ambiente is gestor_ambiente
        assert operador._gestor_climatizador is gestor_climatizador

    # OPR-002
    def test_constructor_crea_selector_y_presentador(self, operador_con_mocks):
        """Constructor crea instancias de SelectorEntradaTemperatura y Presentador"""
        operador, _, _, _ = operador_con_mocks
        assert isinstance(operador._selector, SelectorEntradaTemperatura)
        assert isinstance(operador._presentador, Presentador)
