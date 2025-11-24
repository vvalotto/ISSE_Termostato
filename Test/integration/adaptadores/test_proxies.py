"""
Tests de integracion para Proxies

Casos de prueba del Plan de Pruebas:
- PBA-001: Archivo existe -> retorna valor
- PBA-002: Archivo no existe -> retorna None
- PBA-003: Socket disponible -> lectura exitosa (mock)
- PBA-004: Socket no disponible -> ConnectionError (mock)

- PST-001: Archivo existe -> retorna valor
- PST-002: Archivo no existe -> Exception
"""
import pytest
from unittest.mock import Mock, patch, mock_open
from agentes_sensores.proxy_bateria import ProxyBateriaArchivo, ProxyBateriaSocket
from agentes_sensores.proxy_sensor_temperatura import ProxySensorTemperaturaArchivo


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
            proxy = ProxyBateriaSocket()
            carga = proxy.leer_carga()
            assert carga == 4.5

    # PBA-004: Socket error (mock)
    def test_leer_carga_socket_error_bind(self):
        """Cuando el socket no puede hacer bind, debe lanzar excepcion"""
        mock_socket = Mock()
        mock_socket.bind.side_effect = OSError("Address already in use")

        with patch('socket.socket', return_value=mock_socket):
            proxy = ProxyBateriaSocket()
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
