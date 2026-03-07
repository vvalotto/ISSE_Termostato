"""
Tests de integracion para agentes_sensores/proxy_selector_temperatura.py

Casos de prueba:
- SEL-001: SelectorTemperaturaArchivo.obtener_selector con archivo existente -> retorna contenido
- SEL-002: SelectorTemperaturaArchivo.obtener_selector con archivo inexistente -> lanza IOError
- SEL-003: SelectorTemperaturaArchivo.obtener_selector con valor "ambiente" -> retorna TEMP_AMBIENTE
- SEL-004: SelectorTemperaturaArchivo.obtener_selector con valor "deseada"  -> retorna TEMP_DESEADA
- SEL-005: SelectorTemperaturaSocket instanciacion con host/puerto -> estado inicial TEMP_AMBIENTE
- SEL-006: SelectorTemperaturaSocket.obtener_selector mock socket exitoso -> retorna valor recibido
- SEL-007: SelectorTemperaturaSocket.obtener_selector ConnectionError -> no propaga excepcion
"""
import socket
import pytest
from unittest.mock import Mock, patch
from agentes_sensores.proxy_selector_temperatura import (
    SelectorTemperaturaArchivo,
    SelectorTemperaturaSocket,
)
from entidades.ambiente import TEMP_AMBIENTE, TEMP_DESEADA


class TestSelectorTemperaturaArchivo:

    # SEL-001
    def test_obtener_selector_retorna_contenido_archivo(self, tmp_path, monkeypatch):
        """Cuando el archivo existe, retorna su contenido"""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "tipo_temperatura").write_text("ambiente")
        selector = SelectorTemperaturaArchivo()
        assert selector.obtener_selector() == "ambiente"

    # SEL-002
    def test_obtener_selector_archivo_no_existe_lanza_ioerror(self, tmp_path, monkeypatch):
        """Cuando el archivo no existe, lanza IOError"""
        monkeypatch.chdir(tmp_path)
        selector = SelectorTemperaturaArchivo()
        with pytest.raises(IOError):
            selector.obtener_selector()

    # SEL-003
    def test_obtener_selector_valor_ambiente(self, tmp_path, monkeypatch):
        """Cuando el archivo contiene 'ambiente', retorna TEMP_AMBIENTE"""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "tipo_temperatura").write_text(TEMP_AMBIENTE)
        selector = SelectorTemperaturaArchivo()
        assert selector.obtener_selector() == TEMP_AMBIENTE

    # SEL-004
    def test_obtener_selector_valor_deseada(self, tmp_path, monkeypatch):
        """Cuando el archivo contiene 'deseada', retorna TEMP_DESEADA"""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "tipo_temperatura").write_text(TEMP_DESEADA)
        selector = SelectorTemperaturaArchivo()
        assert selector.obtener_selector() == TEMP_DESEADA


class TestSelectorTemperaturaSocket:

    @pytest.fixture
    def mock_servidor(self):
        """Socket servidor mockeado sin conexiones pendientes por defecto"""
        mock = Mock()
        mock.accept.side_effect = socket.timeout
        return mock

    # SEL-005
    def test_instanciacion_estado_inicial_temp_ambiente(self, mock_servidor):
        """Al instanciar con host/puerto, el estado inicial es TEMP_AMBIENTE y conexion es None"""
        with patch("socket.socket", return_value=mock_servidor):
            selector = SelectorTemperaturaSocket("0.0.0.0", 14000)
        assert selector._estado_actual == TEMP_AMBIENTE
        assert selector._conexion is None

    # SEL-006
    def test_obtener_selector_socket_exitoso_retorna_valor(self, mock_servidor):
        """Con datos recibidos por socket, retorna el valor enviado"""
        mock_conn = Mock()
        mock_conn.recv.return_value = b"deseada"
        mock_servidor.accept.side_effect = None
        mock_servidor.accept.return_value = (mock_conn, ("127.0.0.1", 5000))

        with patch("socket.socket", return_value=mock_servidor):
            selector = SelectorTemperaturaSocket("0.0.0.0", 14000)
            resultado = selector.obtener_selector()

        assert resultado == TEMP_DESEADA

    # SEL-007
    def test_obtener_selector_connection_error_no_propaga(self, mock_servidor):
        """Cuando ocurre ConnectionError en recv, no propaga la excepcion y retorna estado actual"""
        mock_conn = Mock()
        mock_conn.recv.side_effect = ConnectionError("conexion rota")
        mock_servidor.accept.side_effect = None
        mock_servidor.accept.return_value = (mock_conn, ("127.0.0.1", 5000))

        with patch("socket.socket", return_value=mock_servidor):
            selector = SelectorTemperaturaSocket("0.0.0.0", 14000)
            resultado = selector.obtener_selector()

        assert resultado == TEMP_AMBIENTE
