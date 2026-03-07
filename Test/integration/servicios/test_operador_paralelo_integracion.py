"""
Tests de integracion para servicios_aplicacion/operador_paralelo.py

Casos de prueba:
- OPP-INT-001: Constructor asigna gestores correctamente
- OPP-INT-002: Constructor crea _selector y _presentador con tipos correctos
- OPP-INT-003: ejecutar() crea exactamente 5 threads
- OPP-INT-004: ejecutar() llama start() en cada thread creado
- OPP-INT-005: lee_carga_bateria() llama verificar_nivel_de_carga en una iteracion
- OPP-INT-006: lee_temperatura_ambiente() llama leer_temperatura_ambiente en una iteracion
- OPP-INT-007: acciona_climatizador() llama accionar_climatizador con el ambiente correcto
- OPP-INT-008: muestra_parametros() llama _presentador.ejecutar en una iteracion
"""
import pytest
import threading
from unittest.mock import Mock, patch, call
from servicios_aplicacion.operador_paralelo import OperadorParalelo
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador


@pytest.fixture
def operador():
    """OperadorParalelo con gestores mockeados y Configurador parchado."""
    gestor_bateria = Mock()
    gestor_ambiente = Mock()
    gestor_climatizador = Mock()

    with patch("servicios_aplicacion.selector_entrada.Configurador") as cfg:
        cfg.configurar_seteo_temperatura.return_value = Mock()
        cfg.configurar_selector_temperatura.return_value = Mock()
        op = OperadorParalelo(gestor_bateria, gestor_ambiente, gestor_climatizador)

    return op, gestor_bateria, gestor_ambiente, gestor_climatizador


class TestOperadorParaleloConstructor:

    # OPP-INT-001
    def test_constructor_asigna_gestores(self, operador):
        """Constructor asigna _gestor_bateria, _gestor_ambiente y _gestor_climatizador."""
        op, gestor_bateria, gestor_ambiente, gestor_climatizador = operador
        assert op._gestor_bateria is gestor_bateria
        assert op._gestor_ambiente is gestor_ambiente
        assert op._gestor_climatizador is gestor_climatizador

    # OPP-INT-002
    def test_constructor_crea_selector_y_presentador(self, operador):
        """Constructor crea instancias de SelectorEntradaTemperatura y Presentador."""
        op, _, _, _ = operador
        assert isinstance(op._selector, SelectorEntradaTemperatura)
        assert isinstance(op._presentador, Presentador)


class TestOperadorParaleloEjecutar:

    # OPP-INT-003
    def test_ejecutar_crea_cinco_threads(self, operador):
        """ejecutar() crea exactamente 5 threads."""
        op, _, _, _ = operador
        with patch("threading.Thread") as mock_thread_cls:
            mock_thread_cls.return_value = Mock()
            op.ejecutar()
        assert mock_thread_cls.call_count == 5

    # OPP-INT-004
    def test_ejecutar_inicia_todos_los_threads(self, operador):
        """ejecutar() llama start() en cada uno de los 5 threads."""
        op, _, _, _ = operador
        mock_hilos = [Mock() for _ in range(5)]
        with patch("threading.Thread", side_effect=mock_hilos):
            op.ejecutar()
        for hilo in mock_hilos:
            hilo.start.assert_called_once()


class TestOperadorParaleloMetodosIndividuales:

    # OPP-INT-005
    def test_lee_carga_bateria_llama_verificar_nivel(self, operador):
        """lee_carga_bateria() llama verificar_nivel_de_carga en una iteracion."""
        op, gestor_bateria, _, _ = operador
        with patch("time.sleep", side_effect=StopIteration()):
            with pytest.raises(StopIteration):
                op.lee_carga_bateria()
        gestor_bateria.verificar_nivel_de_carga.assert_called_once()

    # OPP-INT-006
    def test_lee_temperatura_ambiente_llama_gestor(self, operador):
        """lee_temperatura_ambiente() llama leer_temperatura_ambiente en una iteracion."""
        op, _, gestor_ambiente, _ = operador
        with patch("time.sleep", side_effect=StopIteration()):
            with pytest.raises(StopIteration):
                op.lee_temperatura_ambiente()
        gestor_ambiente.leer_temperatura_ambiente.assert_called_once()

    # OPP-INT-007
    def test_acciona_climatizador_llama_gestor(self, operador):
        """acciona_climatizador() llama accionar_climatizador con el ambiente correcto."""
        op, _, gestor_ambiente, gestor_climatizador = operador
        with patch("time.sleep", side_effect=StopIteration()):
            with pytest.raises(StopIteration):
                op.acciona_climatizador()
        gestor_climatizador.accionar_climatizador.assert_called_once_with(
            gestor_ambiente.ambiente
        )

    # OPP-INT-008
    def test_muestra_parametros_llama_presentador(self, operador):
        """muestra_parametros() llama _presentador.ejecutar en una iteracion."""
        op, gestor_bateria, gestor_ambiente, gestor_climatizador = operador
        with patch("time.sleep", side_effect=StopIteration()):
            with pytest.raises(StopIteration):
                op.muestra_parametros()
        # _presentador llama a los 3 gestores internamente
        gestor_bateria.mostrar_nivel_de_carga.assert_called_once()
        gestor_ambiente.mostrar_temperatura.assert_called_once()
        gestor_climatizador.mostrar_estado_climatizador.assert_called_once()
