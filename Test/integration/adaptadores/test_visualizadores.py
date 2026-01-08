"""
Tests de integracion para Visualizadores

Casos de prueba del Plan de Pruebas:
- VIS-001: Consola -> stdout contiene valor
- VIS-002: Socket -> datos enviados a puerto
- VIS-003: API -> POST a endpoint correcto
- VIS-004: Socket no disponible -> ConnectionError manejado
- VIS-005: API no disponible -> RequestException manejado
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from agentes_actuadores.visualizador_temperatura import (
    VisualizadorTemperatura,
    VisualizadorTemperaturaSocket,
    VisualizadorTemperaturaApi
)


class TestVisualizadorTemperaturaConsola:
    """Tests para VisualizadorTemperatura (consola/print)"""

    # VIS-001: Consola muestra valor
    def test_mostrar_temperatura_ambiente_imprime_valor(self, capsys):
        """mostrar_temperatura_ambiente debe imprimir el valor"""
        visualizador = VisualizadorTemperatura()
        visualizador.mostrar_temperatura_ambiente(25)
        captured = capsys.readouterr()
        assert "25" in captured.out

    def test_mostrar_temperatura_deseada_imprime_valor(self, capsys):
        """mostrar_temperatura_deseada debe imprimir el valor"""
        visualizador = VisualizadorTemperatura()
        visualizador.mostrar_temperatura_deseada(22)
        captured = capsys.readouterr()
        assert "22" in captured.out

    def test_mostrar_temperaturas_diversas(self, capsys):
        """Debe mostrar correctamente diversos valores"""
        visualizador = VisualizadorTemperatura()
        test_values = [0, 25, -5, 100, 22.5]

        for valor in test_values:
            visualizador.mostrar_temperatura_ambiente(valor)
            captured = capsys.readouterr()
            assert str(valor) in captured.out


class TestVisualizadorTemperaturaSocket:
    """Tests para VisualizadorTemperaturaSocket"""

    # VIS-002: Socket envia datos
    def test_mostrar_temperatura_ambiente_envia_a_socket(self):
        """Debe enviar datos al socket"""
        mock_socket = Mock()
        visualizador = VisualizadorTemperaturaSocket()

        with patch('socket.socket', return_value=mock_socket):
            visualizador.mostrar_temperatura_ambiente(25)

            mock_socket.connect.assert_called_once_with(("localhost", 14001))
            mock_socket.send.assert_called_once()
            mock_socket.close.assert_called_once()

    def test_mostrar_temperatura_deseada_envia_a_socket(self):
        """Debe enviar datos al socket"""
        mock_socket = Mock()
        visualizador = VisualizadorTemperaturaSocket()

        with patch('socket.socket', return_value=mock_socket):
            visualizador.mostrar_temperatura_deseada(22)

            mock_socket.connect.assert_called_once_with(("localhost", 14001))
            mock_socket.send.assert_called_once()
            mock_socket.close.assert_called_once()

    def test_formato_mensaje_ambiente(self):
        """El mensaje debe tener el formato correcto"""
        mock_socket = Mock()
        visualizador = VisualizadorTemperaturaSocket()

        with patch('socket.socket', return_value=mock_socket):
            visualizador.mostrar_temperatura_ambiente(25)

            # Verificar que el mensaje contiene "ambiente: 25"
            call_args = mock_socket.send.call_args[0][0]
            assert b"ambiente: 25" in call_args

    def test_formato_mensaje_deseada(self):
        """El mensaje debe tener el formato correcto"""
        mock_socket = Mock()
        visualizador = VisualizadorTemperaturaSocket()

        with patch('socket.socket', return_value=mock_socket):
            visualizador.mostrar_temperatura_deseada(22)

            call_args = mock_socket.send.call_args[0][0]
            assert b"deseada: 22" in call_args

    # VIS-004: Socket no disponible
    def test_socket_no_disponible_maneja_error(self, capsys):
        """Cuando el socket no esta disponible, debe manejar el error"""
        mock_socket = Mock()
        mock_socket.connect.side_effect = ConnectionError("Connection refused")
        visualizador = VisualizadorTemperaturaSocket()

        with patch('socket.socket', return_value=mock_socket):
            # No debe lanzar excepcion
            visualizador.mostrar_temperatura_ambiente(25)

            captured = capsys.readouterr()
            assert "Intentar de vuelta" in captured.out


class TestVisualizadorTemperaturaApi:
    """Tests para VisualizadorTemperaturaApi"""

    # VIS-003: API POST correcto
    def test_mostrar_temperatura_ambiente_hace_post(self):
        """Debe hacer POST al endpoint correcto"""
        visualizador = VisualizadorTemperaturaApi("http://localhost:5050")

        with patch('requests.post') as mock_post:
            visualizador.mostrar_temperatura_ambiente(25)

            mock_post.assert_called_once_with(
                "http://localhost:5050/termostato/temperatura_ambiente/",
                json={"ambiente": 25},
                timeout=5
            )

    def test_mostrar_temperatura_deseada_hace_post(self):
        """Debe hacer POST al endpoint correcto"""
        visualizador = VisualizadorTemperaturaApi("http://localhost:5050")

        with patch('requests.post') as mock_post:
            visualizador.mostrar_temperatura_deseada(22)

            mock_post.assert_called_once_with(
                "http://localhost:5050/termostato/temperatura_deseada/",
                json={"deseada": 22},
                timeout=5
            )

    def test_post_con_diferentes_valores(self):
        """Debe enviar correctamente diferentes valores"""
        visualizador = VisualizadorTemperaturaApi("http://localhost:5050")
        test_values = [0, 25, -5, 100]

        for valor in test_values:
            with patch('requests.post') as mock_post:
                visualizador.mostrar_temperatura_ambiente(valor)
                mock_post.assert_called_once()
                call_args = mock_post.call_args
                assert call_args[1]['json']['ambiente'] == valor

    # VIS-005: API no disponible
    def test_api_no_disponible_maneja_error(self, capsys):
        """Cuando la API no esta disponible, maneja el error e imprime mensaje"""
        import requests
        visualizador = VisualizadorTemperaturaApi("http://localhost:5050")

        with patch('requests.post', side_effect=requests.exceptions.ConnectionError("API no disponible")):
            # No debe lanzar excepcion, debe manejarlo
            visualizador.mostrar_temperatura_ambiente(25)

            # Verificar que se imprimio mensaje de error
            captured = capsys.readouterr()
            assert "Error al enviar temperatura ambiente" in captured.out


class TestVisualizadoresIntegracion:
    """Tests de integracion adicionales"""

    def test_todos_los_visualizadores_aceptan_enteros(self, capsys):
        """Todos los visualizadores deben aceptar enteros"""
        # Consola
        vis_consola = VisualizadorTemperatura()
        vis_consola.mostrar_temperatura_ambiente(25)
        captured = capsys.readouterr()
        assert "25" in captured.out

        # Socket (mock)
        mock_socket = Mock()
        vis_socket = VisualizadorTemperaturaSocket()
        with patch('socket.socket', return_value=mock_socket):
            vis_socket.mostrar_temperatura_ambiente(25)
            mock_socket.send.assert_called()

        # API (mock)
        vis_api = VisualizadorTemperaturaApi("http://localhost:5050")
        with patch('requests.post') as mock_post:
            vis_api.mostrar_temperatura_ambiente(25)
            mock_post.assert_called()

    def test_todos_los_visualizadores_aceptan_floats(self, capsys):
        """Todos los visualizadores deben aceptar floats"""
        # Consola
        vis_consola = VisualizadorTemperatura()
        vis_consola.mostrar_temperatura_ambiente(25.5)
        captured = capsys.readouterr()
        assert "25.5" in captured.out

        # Socket (mock)
        mock_socket = Mock()
        vis_socket = VisualizadorTemperaturaSocket()
        with patch('socket.socket', return_value=mock_socket):
            vis_socket.mostrar_temperatura_ambiente(25.5)
            mock_socket.send.assert_called()

        # API (mock)
        vis_api = VisualizadorTemperaturaApi("http://localhost:5050")
        with patch('requests.post') as mock_post:
            vis_api.mostrar_temperatura_ambiente(25.5)
            mock_post.assert_called()
