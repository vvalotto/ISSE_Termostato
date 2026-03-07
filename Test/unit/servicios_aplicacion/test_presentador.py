"""
Tests unitarios para servicios_aplicacion/presentador.py

Casos de prueba:
- PRE-001: ejecutar invoca mostrar_nivel_de_carga y mostrar_indicador en gestor_bateria
- PRE-002: ejecutar invoca mostrar_temperatura en gestor_ambiente
- PRE-003: ejecutar invoca mostrar_estado_climatizador en gestor_climatizador
- PRE-004: ejecutar invoca mostrar_estado_completo en visualizador_consolidado (si esta configurado)
- PRE-005: ejecutar no invoca visualizador_consolidado si es None
"""
import pytest
from unittest.mock import Mock
from servicios_aplicacion.presentador import Presentador


@pytest.fixture
def presentador():
    gestor_bateria = Mock()
    gestor_ambiente = Mock()
    gestor_climatizador = Mock()
    p = Presentador(gestor_bateria, gestor_ambiente, gestor_climatizador)
    return p, gestor_bateria, gestor_ambiente, gestor_climatizador


class TestPresentador:

    # PRE-001
    def test_ejecutar_llama_mostrar_bateria(self, presentador):
        """ejecutar invoca mostrar_nivel_de_carga y mostrar_indicador_de_carga en gestor_bateria"""
        p, gestor_bateria, gestor_ambiente, gestor_climatizador = presentador
        p.ejecutar()
        gestor_bateria.mostrar_nivel_de_carga.assert_called_once()
        gestor_bateria.mostrar_indicador_de_carga.assert_called_once()

    # PRE-002
    def test_ejecutar_llama_mostrar_temperatura(self, presentador):
        """ejecutar invoca mostrar_temperatura en gestor_ambiente"""
        p, gestor_bateria, gestor_ambiente, gestor_climatizador = presentador
        p.ejecutar()
        gestor_ambiente.mostrar_temperatura.assert_called_once()

    # PRE-003
    def test_ejecutar_llama_mostrar_estado_climatizador(self, presentador):
        """ejecutar invoca mostrar_estado_climatizador en gestor_climatizador"""
        p, gestor_bateria, gestor_ambiente, gestor_climatizador = presentador
        p.ejecutar()
        gestor_climatizador.mostrar_estado_climatizador.assert_called_once()

    # PRE-004
    def test_ejecutar_llama_visualizador_consolidado_si_configurado(self):
        """ejecutar invoca mostrar_estado_completo si visualizador_consolidado esta configurado"""
        gestor_bateria = Mock()
        gestor_ambiente = Mock()
        gestor_climatizador = Mock()
        visualizador_consolidado = Mock()
        p = Presentador(gestor_bateria, gestor_ambiente, gestor_climatizador,
                        visualizador_consolidado)
        p.ejecutar()
        visualizador_consolidado.mostrar_estado_completo.assert_called_once_with(
            gestor_ambiente, gestor_climatizador, gestor_bateria
        )

    # PRE-005
    def test_ejecutar_no_llama_visualizador_si_es_none(self, presentador):
        """ejecutar no invoca visualizador_consolidado si es None"""
        p, gestor_bateria, gestor_ambiente, gestor_climatizador = presentador
        assert p._visualizador_consolidado is None
        p.ejecutar()  # No debe lanzar excepcion
