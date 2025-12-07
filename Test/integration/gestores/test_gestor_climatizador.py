"""
Tests de integracion para GestorClimatizador

Casos de prueba del Plan de Pruebas:
- GCL-001: Activar calefaccion -> estado="calentando"
- GCL-002: Activar enfriamiento -> estado="enfriando"
- GCL-003: Mantener estado normal -> estado="apagado"
- GCL-004: Actuador invocado -> accionar_climatizador() llamado
"""
import pytest
from unittest.mock import Mock
from gestores_entidades.gestor_climatizador import GestorClimatizador
from entidades.ambiente import Ambiente
from entidades.climatizador import Climatizador, Calefactor


class TestGestorClimatizadorIntegracion:
    """Tests de integracion para GestorClimatizador"""

    def _crear_ambiente(self, temp_ambiente, temp_deseada):
        """Helper para crear ambiente con temperaturas especificas"""
        ambiente = Ambiente()
        ambiente.temperatura_ambiente = temp_ambiente
        ambiente.temperatura_deseada = temp_deseada
        return ambiente

    def _crear_gestor(self, climatizador=None, actuador=None, visualizador=None):
        """Helper para crear gestor con dependencias inyectadas"""
        return GestorClimatizador(
            climatizador=climatizador or Climatizador(),
            actuador=actuador or Mock(),
            visualizador=visualizador or Mock()
        )

    # GCL-001: Activar calefaccion (temperatura baja)
    def test_activar_calefaccion_cuando_temperatura_baja(self):
        """Con temperatura baja, debe activar calefaccion"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        ambiente = self._crear_ambiente(temp_ambiente=18, temp_deseada=22)

        gestor.accionar_climatizador(ambiente)

        assert gestor.obtener_estado_climatizador() == "calentando"
        mock_actuador.accionar_climatizador.assert_called_once_with("calentar")

    # GCL-002: Activar enfriamiento (temperatura alta)
    def test_activar_enfriamiento_cuando_temperatura_alta(self):
        """Con temperatura alta, debe activar enfriamiento"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        ambiente = self._crear_ambiente(temp_ambiente=28, temp_deseada=22)

        gestor.accionar_climatizador(ambiente)

        assert gestor.obtener_estado_climatizador() == "enfriando"
        mock_actuador.accionar_climatizador.assert_called_once_with("enfriar")

    # GCL-003: Mantener estado cuando temperatura normal
    def test_mantener_apagado_cuando_temperatura_normal(self):
        """Con temperatura normal, debe mantener apagado"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        ambiente = self._crear_ambiente(temp_ambiente=22, temp_deseada=22)

        gestor.accionar_climatizador(ambiente)

        assert gestor.obtener_estado_climatizador() == "apagado"
        mock_actuador.accionar_climatizador.assert_not_called()

    # GCL-004: Visualizador invocado
    def test_mostrar_estado_invoca_visualizador(self):
        """mostrar_estado_climatizador debe invocar al visualizador"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        gestor.mostrar_estado_climatizador()

        mock_visualizador.mostrar_estado_climatizador.assert_called_once_with("apagado")


class TestGestorClimatizadorConCalefactor:
    """Tests con Calefactor (solo calienta)"""

    def _crear_ambiente(self, temp_ambiente, temp_deseada):
        ambiente = Ambiente()
        ambiente.temperatura_ambiente = temp_ambiente
        ambiente.temperatura_deseada = temp_deseada
        return ambiente

    def _crear_gestor(self, climatizador=None, actuador=None, visualizador=None):
        """Helper para crear gestor con dependencias inyectadas"""
        return GestorClimatizador(
            climatizador=climatizador or Calefactor(),
            actuador=actuador or Mock(),
            visualizador=visualizador or Mock()
        )

    def test_calefactor_calienta_cuando_temperatura_baja(self):
        """Calefactor debe calentar cuando temperatura es baja"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Calefactor(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        ambiente = self._crear_ambiente(temp_ambiente=18, temp_deseada=22)

        gestor.accionar_climatizador(ambiente)

        assert gestor.obtener_estado_climatizador() == "calentando"

    def test_calefactor_no_enfria_cuando_temperatura_alta(self):
        """Calefactor NO debe enfriar cuando temperatura es alta"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Calefactor(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )
        ambiente = self._crear_ambiente(temp_ambiente=28, temp_deseada=22)

        gestor.accionar_climatizador(ambiente)

        # Calefactor no puede enfriar, debe permanecer apagado
        assert gestor.obtener_estado_climatizador() == "apagado"
        mock_actuador.accionar_climatizador.assert_not_called()


class TestGestorClimatizadorCicloCompleto:
    """Tests de ciclo completo de climatizacion

    Nota: El climatizador solo se apaga cuando la temperatura pasa al extremo opuesto.
    - Calentando -> se apaga cuando temperatura es "alta"
    - Enfriando -> se apaga cuando temperatura es "baja"
    """

    def _crear_ambiente(self, temp_ambiente, temp_deseada):
        ambiente = Ambiente()
        ambiente.temperatura_ambiente = temp_ambiente
        ambiente.temperatura_deseada = temp_deseada
        return ambiente

    def _crear_gestor(self, climatizador=None, actuador=None, visualizador=None):
        """Helper para crear gestor con dependencias inyectadas"""
        return GestorClimatizador(
            climatizador=climatizador or Climatizador(),
            actuador=actuador or Mock(),
            visualizador=visualizador or Mock()
        )

    def test_ciclo_calentar_y_apagar_por_temperatura_alta(self):
        """Ciclo: frio -> calentar -> caliente -> apagar"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )

        # Paso 1: Temperatura baja, debe calentar
        ambiente_frio = self._crear_ambiente(temp_ambiente=18, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_frio)
        assert gestor.obtener_estado_climatizador() == "calentando"

        # Paso 2: Temperatura alta (sobrecalentado), debe apagar
        ambiente_alta = self._crear_ambiente(temp_ambiente=26, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_alta)
        assert gestor.obtener_estado_climatizador() == "apagado"

    def test_ciclo_enfriar_y_apagar_por_temperatura_baja(self):
        """Ciclo: caliente -> enfriar -> frio -> apagar"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )

        # Paso 1: Temperatura alta, debe enfriar
        ambiente_caliente = self._crear_ambiente(temp_ambiente=28, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_caliente)
        assert gestor.obtener_estado_climatizador() == "enfriando"

        # Paso 2: Temperatura baja (sobreenfriado), debe apagar
        ambiente_fria = self._crear_ambiente(temp_ambiente=18, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_fria)
        assert gestor.obtener_estado_climatizador() == "apagado"

    def test_calentando_mantiene_estado_en_temperatura_normal(self):
        """Calentando con temperatura normal, mantiene estado (no se apaga)"""
        mock_actuador = Mock()
        mock_visualizador = Mock()

        gestor = self._crear_gestor(
            climatizador=Climatizador(),
            actuador=mock_actuador,
            visualizador=mock_visualizador
        )

        # Paso 1: Activar calefaccion
        ambiente_frio = self._crear_ambiente(temp_ambiente=18, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_frio)
        assert gestor.obtener_estado_climatizador() == "calentando"

        # Paso 2: Temperatura normal, sigue calentando (comportamiento actual)
        ambiente_normal = self._crear_ambiente(temp_ambiente=22, temp_deseada=22)
        gestor.accionar_climatizador(ambiente_normal)
        assert gestor.obtener_estado_climatizador() == "calentando"
