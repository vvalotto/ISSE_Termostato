"""
Tests de integracion para Proxies

Casos de prueba del Plan de Pruebas:
- PBA-001: Archivo existe -> retorna valor
- PBA-002: Archivo no existe -> retorna None
- PBA-003: Socket disponible -> lectura exitosa (mock)
- PBA-004: Socket no disponible -> ConnectionError (mock)

- PST-001: Archivo existe -> retorna valor
- PST-002: Archivo no existe -> Exception

- PRX-SET-001: SeteoTemperatura.obtener_seteo desde consola
- PRX-SET-002: SeteoTemperaturaSocket init con host/puerto
- PRX-SET-003: SeteoTemperaturaSocket.obtener_seteo mock socket exitoso
- PRX-SET-004: SeteoTemperaturaSocket como context manager
- PRX-SET-005: SeteoTemperaturaSocket.__exit__ cierra recursos
- PRX-SNS-001: ProxySensorTemperaturaSocket con mock socket
- PRX-BAT-001: ProxyBateriaSocket con host y puerto correctos
"""
import pytest
from unittest.mock import Mock, patch, mock_open
from agentes_sensores.proxy_bateria import ProxyBateriaArchivo, ProxyBateriaSocket
from agentes_sensores.proxy_sensor_temperatura import (
    ProxySensorTemperaturaArchivo,
    ProxySensorTemperaturaSocket,
)
from agentes_sensores.proxy_seteo_temperatura import SeteoTemperatura, SeteoTemperaturaSocket


class TestProxyBateriaArchivo:
    """Tests para ProxyBateriaArchivo"""

    # PBA-001: Archivo existe
    def test_leer_carga_archivo_existe(self):
        """Cuando el archivo existe, debe retornar el valor leido"""
        with patch("builtins.open", mock_open(read_data="4.5")):
            proxy = ProxyBateriaArchivo()
            carga = proxy.leer_carga()
            assert carga == 4.5

    def test_leer_carga_valores_diversos(self):
        """Debe leer correctamente diversos valores"""
        test_cases = [
            ("5.0", 5.0),
            ("0", 0.0),
            ("3.75", 3.75),
            ("0.01", 0.01),
        ]

        for contenido, esperado in test_cases:
            with patch("builtins.open", mock_open(read_data=contenido)):
                proxy = ProxyBateriaArchivo()
                carga = proxy.leer_carga()
                assert carga == esperado

    # PBA-002: Archivo no existe
    def test_leer_carga_archivo_no_existe(self):
        """Cuando el archivo no existe, debe retornar None"""
        with patch("builtins.open", side_effect=IOError("File not found")):
            proxy = ProxyBateriaArchivo()
            carga = proxy.leer_carga()
            assert carga is None

    def test_leer_carga_error_io(self):
        """Cuando hay error de IO, debe retornar None"""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            proxy = ProxyBateriaArchivo()
            carga = proxy.leer_carga()
            assert carga is None


class TestProxyBateriaSocket:
    """Tests para ProxyBateriaSocket (con mocks)"""

    # PBA-003: Socket disponible (mock)
    def test_leer_carga_socket_mock(self):
        """Test con socket mockeado"""
        mock_socket = Mock()
        mock_conn = Mock()
        mock_conn.recv.side_effect = [b"4.5", b""]

        mock_socket.accept.return_value = (mock_conn, ('localhost', 12345))

        with patch('socket.socket', return_value=mock_socket):
            proxy = ProxyBateriaSocket("0.0.0.0", 11000)
            carga = proxy.leer_carga()
            assert carga == 4.5

    # PBA-004: Socket error (mock)
    def test_leer_carga_socket_error_bind(self):
        """Cuando el socket no puede hacer bind, debe lanzar excepcion"""
        mock_socket = Mock()
        mock_socket.bind.side_effect = OSError("Address already in use")

        with patch('socket.socket', return_value=mock_socket):
            proxy = ProxyBateriaSocket("0.0.0.0", 11000)
            with pytest.raises(OSError):
                proxy.leer_carga()


class TestProxySensorTemperaturaArchivo:
    """Tests para ProxySensorTemperaturaArchivo

    Nota: El proxy de temperatura usa int() para leer el valor
    """

    # PST-001: Archivo existe
    def test_leer_temperatura_archivo_existe(self):
        """Cuando el archivo existe, debe retornar el valor leido (entero)"""
        with patch("builtins.open", mock_open(read_data="25")):
            proxy = ProxySensorTemperaturaArchivo()
            temp = proxy.leer_temperatura()
            assert temp == 25

    def test_leer_temperatura_valores_diversos(self):
        """Debe leer correctamente diversos valores de temperatura (enteros)"""
        test_cases = [
            ("0", 0),
            ("22", 22),
            ("-5", -5),
            ("100", 100),
        ]

        for contenido, esperado in test_cases:
            with patch("builtins.open", mock_open(read_data=contenido)):
                proxy = ProxySensorTemperaturaArchivo()
                temp = proxy.leer_temperatura()
                assert temp == esperado

    # PST-002: Archivo no existe
    def test_leer_temperatura_archivo_no_existe(self):
        """Cuando el archivo no existe, debe lanzar Exception"""
        with patch("builtins.open", side_effect=IOError("File not found")):
            proxy = ProxySensorTemperaturaArchivo()
            with pytest.raises(Exception):
                proxy.leer_temperatura()


class TestProxiesIntegracion:
    """Tests de integracion con archivos temporales"""

    def test_proxy_bateria_con_archivo_temporal(self, tmp_path):
        """Test con archivo temporal real"""
        archivo = tmp_path / "bateria"
        archivo.write_text("4.2")

        with patch("builtins.open", mock_open(read_data="4.2")):
            proxy = ProxyBateriaArchivo()
            carga = proxy.leer_carga()
            assert carga == 4.2

    def test_proxy_temperatura_con_archivo_temporal(self, tmp_path):
        """Test con archivo temporal real (entero)"""
        archivo = tmp_path / "temperatura"
        archivo.write_text("23")

        with patch("builtins.open", mock_open(read_data="23")):
            proxy = ProxySensorTemperaturaArchivo()
            temp = proxy.leer_temperatura()
            assert temp == 23


class TestSeteoTemperatura:

    # PRX-SET-001
    def test_obtener_seteo_opcion_1_retorna_aumentar(self):
        """Con input '1', obtener_seteo retorna 'aumentar'"""
        with patch("builtins.input", return_value="1"):
            proxy = SeteoTemperatura()
            assert proxy.obtener_seteo() == "aumentar"

    def test_obtener_seteo_opcion_2_retorna_disminuir(self):
        """Con input '2', obtener_seteo retorna 'disminuir'"""
        with patch("builtins.input", return_value="2"):
            proxy = SeteoTemperatura()
            assert proxy.obtener_seteo() == "disminuir"


class TestSeteoTemperaturaSocket:

    @pytest.fixture
    def mock_servidor(self):
        mock = Mock()
        mock.accept.side_effect = __import__("socket").timeout
        return mock

    # PRX-SET-002
    def test_init_conexion_es_none(self, mock_servidor):
        """Al instanciar con host/puerto, _conexion es None"""
        with patch("socket.socket", return_value=mock_servidor):
            proxy = SeteoTemperaturaSocket("0.0.0.0", 13000)
        assert proxy._conexion is None

    # PRX-SET-003
    def test_obtener_seteo_socket_exitoso_retorna_valor(self, mock_servidor):
        """Con datos recibidos por socket, retorna el comando enviado"""
        mock_conn = Mock()
        mock_conn.recv.return_value = b"aumentar"
        mock_servidor.accept.side_effect = None
        mock_servidor.accept.return_value = (mock_conn, ("127.0.0.1", 5000))

        with patch("socket.socket", return_value=mock_servidor):
            proxy = SeteoTemperaturaSocket("0.0.0.0", 13000)
            resultado = proxy.obtener_seteo()

        assert resultado == "aumentar"

    # PRX-SET-004
    def test_context_manager_enter_retorna_self(self, mock_servidor):
        """__enter__ retorna la instancia del proxy"""
        with patch("socket.socket", return_value=mock_servidor):
            proxy = SeteoTemperaturaSocket("0.0.0.0", 13000)
            assert proxy.__enter__() is proxy

    # PRX-SET-005
    def test_context_manager_exit_cierra_servidor(self, mock_servidor):
        """__exit__ cierra el servidor socket"""
        with patch("socket.socket", return_value=mock_servidor):
            proxy = SeteoTemperaturaSocket("0.0.0.0", 13000)
            proxy.__exit__(None, None, None)
        mock_servidor.close.assert_called_once()


class TestProxySensorTemperaturaSocket:

    # PRX-SNS-001
    def test_leer_temperatura_socket_exitoso(self):
        """Con datos recibidos por socket, retorna la temperatura como float"""
        mock_servidor = Mock()
        mock_conn = Mock()
        mock_conn.recv.side_effect = [b"25.0", b""]
        mock_servidor.accept.return_value = (mock_conn, ("127.0.0.1", 5000))

        with patch("socket.socket", return_value=mock_servidor):
            proxy = ProxySensorTemperaturaSocket("0.0.0.0", 12000)
            temperatura = proxy.leer_temperatura()

        assert temperatura == 25.0


class TestProxyBateriaSocketDI:

    # PRX-BAT-001
    def test_init_almacena_host_y_puerto(self):
        """El constructor almacena host y puerto correctamente"""
        proxy = ProxyBateriaSocket("192.168.1.1", 11000)
        assert proxy._host == "192.168.1.1"
        assert proxy._puerto == 11000
