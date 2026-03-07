"""
Tests unitarios para agentes_actuadores/visualizador_estado_consolidado.py

Casos de prueba:
- VEC-001: Constructor con host y puerto -> almacena correctamente
- VEC-002: mostrar_estado_completo envia JSON por socket (mock)
- VEC-003: Formato JSON contiene los 8 campos del contrato de API
- VEC-004: _construir_estado con temperatura None -> falla_sensor=True y temp=0.0
- VEC-005: _construir_estado con bateria BAJA -> bateria_baja=True
- VEC-006: _mapear_modo_climatizador("apagado") -> "reposo"
- VEC-007: _mapear_modo_climatizador("calentando") -> "calentando"
- VEC-008: mostrar_estado_completo con ConnectionError no propaga excepcion
- VEC-009: timestamp en formato ISO 8601
"""
import json
import pytest
from unittest.mock import Mock, patch
from agentes_actuadores.visualizador_estado_consolidado import VisualizadorEstadoConsolidadoSocket


@pytest.fixture
def gestores():
    """Mocks de los tres gestores con valores por defecto"""
    ambiente = Mock()
    ambiente.obtener_temperatura_ambiente.return_value = 22.5
    ambiente.obtener_temperatura_deseada.return_value = 24.0
    ambiente.ambiente.temperatura_a_mostrar = "ambiente"

    climatizador = Mock()
    climatizador.obtener_estado_climatizador.return_value = "calentando"

    bateria = Mock()
    bateria.obtener_indicador_de_carga.return_value = "NORMAL"

    return ambiente, climatizador, bateria


@pytest.fixture
def mock_socket():
    """Socket cliente mockeado"""
    return Mock()


class TestVisualizadorEstadoConsolidadoConstructor:

    # VEC-001
    def test_constructor_almacena_host_y_puerto(self):
        """El constructor almacena host y puerto correctamente"""
        vis = VisualizadorEstadoConsolidadoSocket("192.168.1.1", 9000)
        assert vis._host == "192.168.1.1"
        assert vis._port == 9000

    def test_constructor_valores_por_defecto(self):
        """El constructor tiene valores por defecto (localhost, 14001)"""
        vis = VisualizadorEstadoConsolidadoSocket()
        assert vis._host == "localhost"
        assert vis._port == 14001


class TestVisualizadorEstadoConsolidadoEnvio:

    # VEC-002
    def test_mostrar_estado_conecta_y_envia_bytes(self, gestores, mock_socket):
        """mostrar_estado_completo conecta al socket y envia bytes"""
        ambiente, climatizador, bateria = gestores
        vis = VisualizadorEstadoConsolidadoSocket("localhost", 14001)

        with patch("socket.socket", return_value=mock_socket), \
             patch("time.sleep"):
            vis.mostrar_estado_completo(ambiente, climatizador, bateria)

        mock_socket.connect.assert_called_once_with(("localhost", 14001))
        mock_socket.send.assert_called_once()
        mock_socket.close.assert_called_once()

    # VEC-003
    def test_json_contiene_8_campos_requeridos(self, gestores, mock_socket):
        """El JSON enviado contiene los 8 campos del contrato de API"""
        ambiente, climatizador, bateria = gestores
        vis = VisualizadorEstadoConsolidadoSocket()
        campos_requeridos = {
            "temperatura_actual", "temperatura_deseada", "modo_climatizador",
            "falla_sensor", "bateria_baja", "encendido", "modo_display", "timestamp"
        }

        with patch("socket.socket", return_value=mock_socket), \
             patch("time.sleep"):
            vis.mostrar_estado_completo(ambiente, climatizador, bateria)

        bytes_enviados = mock_socket.send.call_args[0][0]
        estado = json.loads(bytes_enviados.decode("utf-8").strip())
        assert campos_requeridos == set(estado.keys())

    # VEC-008
    def test_connection_error_no_propaga_excepcion(self, gestores):
        """Cuando el socket falla con ConnectionError, no propaga la excepcion"""
        ambiente, climatizador, bateria = gestores
        vis = VisualizadorEstadoConsolidadoSocket()
        mock_s = Mock()
        mock_s.connect.side_effect = ConnectionError("refused")

        with patch("socket.socket", return_value=mock_s), \
             patch("time.sleep"):
            vis.mostrar_estado_completo(ambiente, climatizador, bateria)  # No debe lanzar


class TestVisualizadorConstruirEstado:

    # VEC-004
    def test_temperatura_none_activa_falla_sensor(self):
        """Cuando temperatura_actual es None, falla_sensor=True y temp_actual=0.0"""
        ambiente = Mock()
        ambiente.obtener_temperatura_ambiente.return_value = None
        ambiente.obtener_temperatura_deseada.return_value = 24.0
        ambiente.ambiente.temperatura_a_mostrar = "ambiente"
        climatizador = Mock()
        climatizador.obtener_estado_climatizador.return_value = "apagado"
        bateria = Mock()
        bateria.obtener_indicador_de_carga.return_value = "NORMAL"

        vis = VisualizadorEstadoConsolidadoSocket()
        estado = vis._construir_estado(ambiente, climatizador, bateria)

        assert estado["falla_sensor"] is True
        assert estado["temperatura_actual"] == 0.0

    # VEC-005
    def test_bateria_baja_activa_flag(self):
        """Cuando indicador de carga es BAJA, bateria_baja=True"""
        ambiente = Mock()
        ambiente.obtener_temperatura_ambiente.return_value = 22.0
        ambiente.obtener_temperatura_deseada.return_value = 24.0
        ambiente.ambiente.temperatura_a_mostrar = "ambiente"
        climatizador = Mock()
        climatizador.obtener_estado_climatizador.return_value = "calentando"
        bateria = Mock()
        bateria.obtener_indicador_de_carga.return_value = "BAJA"

        vis = VisualizadorEstadoConsolidadoSocket()
        estado = vis._construir_estado(ambiente, climatizador, bateria)

        assert estado["bateria_baja"] is True

    # VEC-009
    def test_timestamp_formato_iso_8601(self, gestores):
        """El campo timestamp tiene formato ISO 8601"""
        ambiente, climatizador, bateria = gestores
        vis = VisualizadorEstadoConsolidadoSocket()
        estado = vis._construir_estado(ambiente, climatizador, bateria)
        # ISO 8601 contiene 'T' separando fecha y hora
        assert "T" in estado["timestamp"]
        assert len(estado["timestamp"]) >= 19  # YYYY-MM-DDTHH:MM:SS


class TestMapearModoClimatizador:

    # VEC-006
    def test_apagado_mapea_a_reposo(self):
        """'apagado' se mapea a 'reposo'"""
        assert VisualizadorEstadoConsolidadoSocket._mapear_modo_climatizador("apagado") == "reposo"

    # VEC-007
    def test_calentando_sin_cambio(self):
        """'calentando' se mantiene como 'calentando'"""
        assert VisualizadorEstadoConsolidadoSocket._mapear_modo_climatizador("calentando") == "calentando"

    def test_enfriando_sin_cambio(self):
        """'enfriando' se mantiene como 'enfriando'"""
        assert VisualizadorEstadoConsolidadoSocket._mapear_modo_climatizador("enfriando") == "enfriando"

    def test_desconocido_mapea_a_reposo(self):
        """Un estado desconocido se mapea a 'reposo' como fallback"""
        assert VisualizadorEstadoConsolidadoSocket._mapear_modo_climatizador("otro") == "reposo"
