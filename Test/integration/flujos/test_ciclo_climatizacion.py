"""
Tests de integracion para flujos completos de climatizacion

Segun el Plan de Pruebas:

Ciclo Completo de Calefaccion:
- Precondiciones: temp_ambiente=18, temp_deseada=22, estado=apagado
- Flujo: leer_temp -> comparar -> evaluar -> accionar -> estado=calentando

Ciclo Completo de Enfriamiento:
- Precondiciones: temp_ambiente=28, temp_deseada=22, estado=apagado
- Flujo: leer_temp -> comparar -> evaluar -> accionar -> estado=enfriando
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from entidades.ambiente import Ambiente
from entidades.climatizador import Climatizador, Calefactor
from gestores_entidades.gestor_ambiente import GestorAmbiente
from gestores_entidades.gestor_climatizador import GestorClimatizador
from servicios_dominio.controlador_climatizador import ControladorTemperatura


class TestCicloCompletoCalefaccion:
    """Tests del ciclo completo de calefaccion"""

    def test_ciclo_calefaccion_desde_temperatura_baja(self):
        """
        Ciclo completo de calefaccion:
        1. GestorAmbiente lee temperatura (18°C)
        2. ControladorTemperatura compara (18 vs 22) -> "baja"
        3. Climatizador evalua accion -> "calentar"
        4. GestorClimatizador acciona -> estado="calentando"
        """
        # Setup mocks
        mock_proxy_temp = Mock()
        mock_proxy_temp.leer_temperatura.return_value = 18.0
        mock_visualizador_temp = Mock()
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        # Crear GestorAmbiente con mocks
        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config_amb:
            mock_config_amb.configurar_proxy_temperatura.return_value = mock_proxy_temp
            mock_config_amb.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador_temp

            gestor_ambiente = GestorAmbiente()

            # Paso 1: Leer temperatura ambiente
            gestor_ambiente.leer_temperatura_ambiente()
            assert gestor_ambiente.obtener_temperatura_ambiente() == 18.0

            # Paso 2: Configurar temperatura deseada (22°C)
            for _ in range(22):
                gestor_ambiente.aumentar_temperatura_deseada()
            assert gestor_ambiente.obtener_temperatura_deseada() == 22

            # Paso 3: Verificar comparacion de temperatura
            resultado = ControladorTemperatura.comparar_temperatura(18, 22)
            assert resultado == "baja"

        # Crear GestorClimatizador con mocks
        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config_clima:
            mock_config_clima.configurar_climatizador.return_value = Climatizador()
            mock_config_clima.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config_clima.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor_climatizador = GestorClimatizador()

            # Paso 4: Accionar climatizador con el ambiente
            gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

            # Verificaciones finales
            assert gestor_climatizador.obtener_estado_climatizador() == "calentando"
            mock_actuador.accionar_climatizador.assert_called_once_with("calentar")


class TestCicloCompletoEnfriamiento:
    """Tests del ciclo completo de enfriamiento"""

    def test_ciclo_enfriamiento_desde_temperatura_alta(self):
        """
        Ciclo completo de enfriamiento:
        1. GestorAmbiente lee temperatura (28°C)
        2. ControladorTemperatura compara (28 vs 22) -> "alta"
        3. Climatizador evalua accion -> "enfriar"
        4. GestorClimatizador acciona -> estado="enfriando"
        """
        # Setup mocks
        mock_proxy_temp = Mock()
        mock_proxy_temp.leer_temperatura.return_value = 28.0
        mock_visualizador_temp = Mock()
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        # Crear GestorAmbiente con mocks
        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config_amb:
            mock_config_amb.configurar_proxy_temperatura.return_value = mock_proxy_temp
            mock_config_amb.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador_temp

            gestor_ambiente = GestorAmbiente()

            # Paso 1: Leer temperatura ambiente
            gestor_ambiente.leer_temperatura_ambiente()
            assert gestor_ambiente.obtener_temperatura_ambiente() == 28.0

            # Paso 2: Configurar temperatura deseada (22°C)
            for _ in range(22):
                gestor_ambiente.aumentar_temperatura_deseada()
            assert gestor_ambiente.obtener_temperatura_deseada() == 22

            # Paso 3: Verificar comparacion de temperatura
            resultado = ControladorTemperatura.comparar_temperatura(28, 22)
            assert resultado == "alta"

        # Crear GestorClimatizador con mocks
        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config_clima:
            mock_config_clima.configurar_climatizador.return_value = Climatizador()
            mock_config_clima.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config_clima.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor_climatizador = GestorClimatizador()

            # Paso 4: Accionar climatizador con el ambiente
            gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

            # Verificaciones finales
            assert gestor_climatizador.obtener_estado_climatizador() == "enfriando"
            mock_actuador.accionar_climatizador.assert_called_once_with("enfriar")


class TestCicloTemperaturaNormal:
    """Tests cuando la temperatura esta en rango normal"""

    def test_ciclo_sin_accion_temperatura_normal(self):
        """
        Cuando la temperatura esta en rango normal:
        1. GestorAmbiente lee temperatura (22°C)
        2. ControladorTemperatura compara (22 vs 22) -> "normal"
        3. Climatizador evalua accion -> None
        4. GestorClimatizador no acciona -> estado="apagado"
        """
        mock_proxy_temp = Mock()
        mock_proxy_temp.leer_temperatura.return_value = 22.0
        mock_visualizador_temp = Mock()
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config_amb:
            mock_config_amb.configurar_proxy_temperatura.return_value = mock_proxy_temp
            mock_config_amb.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador_temp

            gestor_ambiente = GestorAmbiente()
            gestor_ambiente.leer_temperatura_ambiente()

            for _ in range(22):
                gestor_ambiente.aumentar_temperatura_deseada()

            resultado = ControladorTemperatura.comparar_temperatura(22, 22)
            assert resultado == "normal"

        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config_clima:
            mock_config_clima.configurar_climatizador.return_value = Climatizador()
            mock_config_clima.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config_clima.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor_climatizador = GestorClimatizador()
            gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

            assert gestor_climatizador.obtener_estado_climatizador() == "apagado"
            mock_actuador.accionar_climatizador.assert_not_called()


class TestCicloConCalefactor:
    """Tests de ciclo con Calefactor (solo calienta)"""

    def test_calefactor_calienta_temperatura_baja(self):
        """Calefactor debe calentar cuando temperatura es baja"""
        mock_proxy_temp = Mock()
        mock_proxy_temp.leer_temperatura.return_value = 18.0
        mock_visualizador_temp = Mock()
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config_amb:
            mock_config_amb.configurar_proxy_temperatura.return_value = mock_proxy_temp
            mock_config_amb.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador_temp

            gestor_ambiente = GestorAmbiente()
            gestor_ambiente.leer_temperatura_ambiente()
            for _ in range(22):
                gestor_ambiente.aumentar_temperatura_deseada()

        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config_clima:
            mock_config_clima.configurar_climatizador.return_value = Calefactor()
            mock_config_clima.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config_clima.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor_climatizador = GestorClimatizador()
            gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

            assert gestor_climatizador.obtener_estado_climatizador() == "calentando"

    def test_calefactor_no_enfria_temperatura_alta(self):
        """Calefactor NO debe enfriar cuando temperatura es alta"""
        mock_proxy_temp = Mock()
        mock_proxy_temp.leer_temperatura.return_value = 28.0
        mock_visualizador_temp = Mock()
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        with patch('gestores_entidades.gestor_ambiente.Configurador') as mock_config_amb:
            mock_config_amb.configurar_proxy_temperatura.return_value = mock_proxy_temp
            mock_config_amb.return_value.configurar_visualizador_temperatura.return_value = mock_visualizador_temp

            gestor_ambiente = GestorAmbiente()
            gestor_ambiente.leer_temperatura_ambiente()
            for _ in range(22):
                gestor_ambiente.aumentar_temperatura_deseada()

        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config_clima:
            mock_config_clima.configurar_climatizador.return_value = Calefactor()
            mock_config_clima.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config_clima.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor_climatizador = GestorClimatizador()
            gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

            # Calefactor no puede enfriar
            assert gestor_climatizador.obtener_estado_climatizador() == "apagado"
            mock_actuador.accionar_climatizador.assert_not_called()


class TestCicloMultiplesIteraciones:
    """Tests de ciclos con multiples iteraciones"""

    def test_ciclo_completo_frio_a_caliente(self):
        """
        Ciclo completo: frio -> calentar -> sobrecalentar -> apagar
        """
        mock_actuador = Mock()
        mock_visualizador_clima = Mock()

        with patch('gestores_entidades.gestor_climatizador.Configurador') as mock_config:
            mock_config.configurar_climatizador.return_value = Climatizador()
            mock_config.configurar_actuador_climatizador.return_value = mock_actuador
            mock_config.configurar_visualizador_climatizador.return_value = mock_visualizador_clima

            gestor = GestorClimatizador()

            # Iteracion 1: Frio -> Calentar
            ambiente_frio = Ambiente()
            ambiente_frio.temperatura_ambiente = 18
            ambiente_frio.temperatura_deseada = 22
            gestor.accionar_climatizador(ambiente_frio)
            assert gestor.obtener_estado_climatizador() == "calentando"

            # Iteracion 2: Sobrecalentado -> Apagar
            ambiente_caliente = Ambiente()
            ambiente_caliente.temperatura_ambiente = 26
            ambiente_caliente.temperatura_deseada = 22
            gestor.accionar_climatizador(ambiente_caliente)
            assert gestor.obtener_estado_climatizador() == "apagado"

            # Iteracion 3: Sigue caliente -> Enfriar
            gestor.accionar_climatizador(ambiente_caliente)
            assert gestor.obtener_estado_climatizador() == "enfriando"
