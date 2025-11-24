"""
Tests de integracion para GestorAmbiente

Casos de prueba del Plan de Pruebas:
- GAM-001: Lectura temperatura exitosa -> temperatura_ambiente=25.0
- GAM-002: Sensor no disponible -> temperatura_ambiente=None
- GAM-003: Aumentar temperatura -> temperatura_deseada += 1
- GAM-004: Disminuir temperatura -> temperatura_deseada -= 1
- GAM-005: Mostrar temp ambiente -> mostrar_temperatura_ambiente() invocado
- GAM-006: Mostrar temp deseada -> mostrar_temperatura_deseada() invocado
"""
import pytest
from unittest.mock import Mock, patch
from gestores_entidades.gestor_ambiente import GestorAmbiente


class TestGestorAmbienteIntegracion:
    """Tests de integracion para GestorAmbiente"""

    # GAM-001: Lectura temperatura exitosa
    def test_lectura_temperatura_exitosa(self):
        """Cuando el proxy retorna un valor, debe actualizar temperatura_ambiente"""
        mock_proxy = Mock()
        mock_proxy.leer_temperatura.return_value = 25.0
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.leer_temperatura_ambiente()

            assert gestor.obtener_temperatura_ambiente() == 25.0
            mock_proxy.leer_temperatura.assert_called_once()

    # GAM-002: Sensor no disponible
    def test_sensor_no_disponible_retorna_none(self):
        """Cuando el sensor lanza excepcion, temperatura_ambiente debe ser None"""
        mock_proxy = Mock()
        mock_proxy.leer_temperatura.side_effect = Exception("Sensor no disponible")
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.leer_temperatura_ambiente()

            assert gestor.obtener_temperatura_ambiente() is None

    # GAM-003: Aumentar temperatura
    def test_aumentar_temperatura_deseada(self):
        """aumentar_temperatura_deseada debe incrementar en 1"""
        mock_proxy = Mock()
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            temp_inicial = gestor.obtener_temperatura_deseada()

            gestor.aumentar_temperatura_deseada()

            assert gestor.obtener_temperatura_deseada() == temp_inicial + 1

    # GAM-004: Disminuir temperatura
    def test_disminuir_temperatura_deseada(self):
        """disminuir_temperatura_deseada debe decrementar en 1"""
        mock_proxy = Mock()
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            # Primero aumentamos para tener un valor positivo
            gestor.aumentar_temperatura_deseada()
            gestor.aumentar_temperatura_deseada()
            temp_antes = gestor.obtener_temperatura_deseada()

            gestor.disminuir_temperatura_deseada()

            assert gestor.obtener_temperatura_deseada() == temp_antes - 1

    # GAM-005: Mostrar temp ambiente
    def test_mostrar_temperatura_ambiente_invoca_visualizador(self):
        """mostrar_temperatura_ambiente debe invocar al visualizador"""
        mock_proxy = Mock()
        mock_proxy.leer_temperatura.return_value = 25.0
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.leer_temperatura_ambiente()
            gestor.mostrar_temperatura_ambiente()

            mock_visualizador.mostrar_temperatura_ambiente.assert_called_once_with(25.0)

    # GAM-006: Mostrar temp deseada
    def test_mostrar_temperatura_deseada_invoca_visualizador(self):
        """mostrar_temperatura_deseada debe invocar al visualizador"""
        mock_proxy = Mock()
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.aumentar_temperatura_deseada()  # temp = 1
            gestor.aumentar_temperatura_deseada()  # temp = 2
            gestor.mostrar_temperatura_deseada()

            mock_visualizador.mostrar_temperatura_deseada.assert_called_once_with(2)


class TestGestorAmbienteMostrarTemperatura:
    """Tests para mostrar_temperatura segun modo"""

    def test_mostrar_temperatura_modo_ambiente(self):
        """Con modo 'ambiente', debe mostrar temperatura ambiente"""
        mock_proxy = Mock()
        mock_proxy.leer_temperatura.return_value = 22.0
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.leer_temperatura_ambiente()
            gestor.indicar_temperatura_a_mostrar("ambiente")
            gestor.mostrar_temperatura()

            mock_visualizador.mostrar_temperatura_ambiente.assert_called_with(22.0)

    def test_mostrar_temperatura_modo_deseada(self):
        """Con modo 'deseada', debe mostrar temperatura deseada"""
        mock_proxy = Mock()
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()
            gestor.aumentar_temperatura_deseada()  # temp = 1
            gestor.indicar_temperatura_a_mostrar("deseada")
            gestor.mostrar_temperatura()

            mock_visualizador.mostrar_temperatura_deseada.assert_called_with(1)


class TestGestorAmbienteFlujoCompleto:
    """Tests del flujo completo de GestorAmbiente"""

    def test_flujo_completo_ajuste_temperatura(self):
        """Flujo completo: lectura -> ajuste -> visualizacion"""
        mock_proxy = Mock()
        mock_proxy.leer_temperatura.return_value = 18.0
        mock_visualizador = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config:
            mock_config.configurar_proxy_temperatura.return_value = mock_proxy
            mock_config.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador

            gestor = GestorAmbiente()

            # Paso 1: Leer temperatura ambiente
            gestor.leer_temperatura_ambiente()
            assert gestor.obtener_temperatura_ambiente() == 18.0

            # Paso 2: Ajustar temperatura deseada
            for _ in range(22):  # Subir a 22
                gestor.aumentar_temperatura_deseada()
            assert gestor.obtener_temperatura_deseada() == 22

            # Paso 3: Mostrar ambas temperaturas
            gestor.mostrar_temperatura_ambiente()
            gestor.mostrar_temperatura_deseada()

            mock_visualizador.mostrar_temperatura_ambiente.assert_called_with(18.0)
            mock_visualizador.mostrar_temperatura_deseada.assert_called_with(22)
