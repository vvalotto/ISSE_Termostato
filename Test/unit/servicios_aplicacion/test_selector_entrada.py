"""
Tests unitarios para servicios_aplicacion/selector_entrada.py

Casos de prueba:
- SEL-ENT-001: Selector retorna TEMP_AMBIENTE -> indicar ambiente (sin cambio de modo)
- SEL-ENT-002: Selector retorna TEMP_DESEADA una vez, luego TEMP_AMBIENTE -> ciclo de seteo
- SEL-ENT-003: Seteo devuelve "aumentar" -> aumentar temperatura en gestor
- SEL-ENT-004: Seteo devuelve "disminuir" -> disminuir temperatura en gestor
"""
import pytest
from unittest.mock import Mock, patch
from entidades.ambiente import TEMP_AMBIENTE, TEMP_DESEADA
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura


@pytest.fixture
def selector_con_mocks():
    """SelectorEntradaTemperatura con Configurador mockeado"""
    mock_seteo = Mock()
    mock_selector = Mock()
    gestor_ambiente = Mock()

    with patch("servicios_aplicacion.selector_entrada.Configurador") as mock_cfg:
        mock_cfg.configurar_seteo_temperatura.return_value = mock_seteo
        mock_cfg.configurar_selector_temperatura.return_value = mock_selector
        selector = SelectorEntradaTemperatura(gestor_ambiente)

    return selector, mock_seteo, mock_selector, gestor_ambiente


class TestSelectorEntradaTemperatura:

    # SEL-ENT-001
    def test_ejecutar_selector_ambiente_indica_ambiente(self, selector_con_mocks):
        """Cuando el selector retorna TEMP_AMBIENTE, el loop no entra y se indica ambiente"""
        selector, mock_seteo, mock_selector, gestor_ambiente = selector_con_mocks
        mock_selector.obtener_selector.return_value = TEMP_AMBIENTE

        selector.ejecutar()

        gestor_ambiente.indicar_temperatura_a_mostrar.assert_called_with(TEMP_AMBIENTE)

    # SEL-ENT-002
    def test_ejecutar_selector_deseada_luego_ambiente(self, selector_con_mocks):
        """Cuando el selector retorna TEMP_DESEADA una vez luego TEMP_AMBIENTE, el loop itera una vez"""
        selector, mock_seteo, mock_selector, gestor_ambiente = selector_con_mocks
        mock_selector.obtener_selector.side_effect = [TEMP_DESEADA, TEMP_AMBIENTE]
        mock_seteo.obtener_seteo.return_value = None

        selector.ejecutar()

        gestor_ambiente.mostrar_temperatura.assert_called_once()
        gestor_ambiente.indicar_temperatura_a_mostrar.assert_called_with(TEMP_AMBIENTE)

    # SEL-ENT-003
    def test_seteo_aumentar_llama_aumentar_temperatura(self, selector_con_mocks):
        """Cuando el seteo devuelve 'aumentar', se llama aumentar_temperatura_deseada"""
        selector, mock_seteo, mock_selector, gestor_ambiente = selector_con_mocks
        mock_selector.obtener_selector.side_effect = [TEMP_DESEADA, TEMP_AMBIENTE]
        mock_seteo.obtener_seteo.return_value = "aumentar"

        selector.ejecutar()

        gestor_ambiente.aumentar_temperatura_deseada.assert_called_once()
        gestor_ambiente.disminuir_temperatura_deseada.assert_not_called()

    # SEL-ENT-004
    def test_seteo_disminuir_llama_disminuir_temperatura(self, selector_con_mocks):
        """Cuando el seteo devuelve 'disminuir', se llama disminuir_temperatura_deseada"""
        selector, mock_seteo, mock_selector, gestor_ambiente = selector_con_mocks
        mock_selector.obtener_selector.side_effect = [TEMP_DESEADA, TEMP_AMBIENTE]
        mock_seteo.obtener_seteo.return_value = "disminuir"

        selector.ejecutar()

        gestor_ambiente.disminuir_temperatura_deseada.assert_called_once()
        gestor_ambiente.aumentar_temperatura_deseada.assert_not_called()
