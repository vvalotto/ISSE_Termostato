"""
Fixtures compartidas para tests de integracion
"""
import pytest
from unittest.mock import Mock, patch


# ============ FIXTURES PARA GESTORES ============

@pytest.fixture
def mock_proxy_bateria():
    """Mock del proxy de bateria"""
    proxy = Mock()
    proxy.leer_carga.return_value = 4.5
    return proxy


@pytest.fixture
def mock_proxy_bateria_baja():
    """Mock del proxy de bateria con carga baja"""
    proxy = Mock()
    proxy.leer_carga.return_value = 2.0
    return proxy


@pytest.fixture
def mock_proxy_temperatura():
    """Mock del proxy de sensor de temperatura"""
    proxy = Mock()
    proxy.leer_temperatura.return_value = 22.0
    return proxy


@pytest.fixture
def mock_visualizador_bateria():
    """Mock del visualizador de bateria"""
    return Mock()


@pytest.fixture
def mock_visualizador_temperatura():
    """Mock del visualizador de temperatura"""
    return Mock()


@pytest.fixture
def mock_visualizador_climatizador():
    """Mock del visualizador de climatizador"""
    return Mock()


@pytest.fixture
def mock_actuador_climatizador():
    """Mock del actuador de climatizador"""
    return Mock()


# ============ FIXTURES PARA CONFIGURADOR ============

@pytest.fixture
def mock_configurador_bateria(mock_proxy_bateria, mock_visualizador_bateria):
    """Patchea el Configurador para GestorBateria"""
    with patch('gestores_entidades.gestor_bateria.Configurador') as mock_config:
        mock_config.return_value.configurar_proxy_bateria.return_value = mock_proxy_bateria
        mock_config.configurar_visualizador_bateria.return_value = mock_visualizador_bateria
        yield mock_config


@pytest.fixture
def mock_configurador_ambiente(mock_proxy_temperatura, mock_visualizador_temperatura):
    """Patchea el Configurador para GestorAmbiente"""
    with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
        mock_config.return_value.configurar_proxy_temperatura.return_value = mock_proxy_temperatura
        mock_config.configurar_visualizador_temperatura.return_value = mock_visualizador_temperatura
        mock_config.configurar_selector_temperatura.return_value = Mock()
        mock_config.configurar_seteo_temperatura.return_value = Mock()
        yield mock_config
