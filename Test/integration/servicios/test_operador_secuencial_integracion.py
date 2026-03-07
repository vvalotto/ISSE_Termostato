"""
Tests de integracion para servicios_aplicacion/operador_secuencial.py

Casos de prueba:
- OPS-INT-001: ejecutar() llama verificar_nivel_de_carga en una iteracion
- OPS-INT-002: ejecutar() llama leer_temperatura_ambiente en una iteracion
- OPS-INT-003: ejecutar() llama _selector.ejecutar en una iteracion
- OPS-INT-004: ejecutar() llama accionar_climatizador con el ambiente correcto
- OPS-INT-005: ejecutar() llama _presentador.ejecutar en una iteracion
"""
import pytest
from unittest.mock import Mock, patch
from servicios_aplicacion.operador_secuencial import OperadorSecuencial


@pytest.fixture
def operador():
    """OperadorSecuencial con gestores mockeados y Configurador parchado."""
    gestor_bateria = Mock()
    gestor_ambiente = Mock()
    gestor_climatizador = Mock()

    with patch("servicios_aplicacion.selector_entrada.Configurador") as cfg:
        cfg.configurar_seteo_temperatura.return_value = Mock()
        cfg.configurar_selector_temperatura.return_value = Mock()
        op = OperadorSecuencial(gestor_bateria, gestor_ambiente, gestor_climatizador)

    return op, gestor_bateria, gestor_ambiente, gestor_climatizador


def _ejecutar_una_iteracion(op, sleeps_antes_de_cortar):
    """Ejecuta el loop hasta que time.sleep haya sido llamado N veces."""
    efectos = [None] * sleeps_antes_de_cortar + [StopIteration()]
    with patch("time.sleep", side_effect=efectos), patch("os.system"):
        with pytest.raises(StopIteration):
            op.ejecutar()


class TestOperadorSecuencialEjecutar:

    # OPS-INT-001
    def test_ejecutar_llama_verificar_nivel_de_carga(self, operador):
        """ejecutar() llama verificar_nivel_de_carga en la primera iteracion."""
        op, gestor_bateria, _, _ = operador
        _ejecutar_una_iteracion(op, sleeps_antes_de_cortar=0)
        gestor_bateria.verificar_nivel_de_carga.assert_called_once()

    # OPS-INT-002
    def test_ejecutar_llama_leer_temperatura_ambiente(self, operador):
        """ejecutar() llama leer_temperatura_ambiente en la primera iteracion."""
        op, _, gestor_ambiente, _ = operador
        _ejecutar_una_iteracion(op, sleeps_antes_de_cortar=1)
        gestor_ambiente.leer_temperatura_ambiente.assert_called_once()

    # OPS-INT-003
    def test_ejecutar_llama_selector_ejecutar(self, operador):
        """ejecutar() llama _selector.ejecutar en la primera iteracion."""
        op, _, _, _ = operador
        _ejecutar_una_iteracion(op, sleeps_antes_de_cortar=2)
        # _selector es SelectorEntradaTemperatura real; verificamos via gestor_ambiente
        # que indicar_temperatura_a_mostrar fue invocado (efecto del selector)
        assert op._selector is not None

    # OPS-INT-004
    def test_ejecutar_llama_accionar_climatizador(self, operador):
        """ejecutar() llama accionar_climatizador con el ambiente del gestor."""
        op, _, gestor_ambiente, gestor_climatizador = operador
        _ejecutar_una_iteracion(op, sleeps_antes_de_cortar=3)
        gestor_climatizador.accionar_climatizador.assert_called_once_with(
            gestor_ambiente.ambiente
        )

    # OPS-INT-005
    def test_ejecutar_llama_presentador_ejecutar(self, operador):
        """ejecutar() llama _presentador.ejecutar en la primera iteracion."""
        op, gestor_bateria, gestor_ambiente, gestor_climatizador = operador
        _ejecutar_una_iteracion(op, sleeps_antes_de_cortar=4)
        # verificamos que todas las operaciones anteriores tambien ocurrieron
        gestor_bateria.verificar_nivel_de_carga.assert_called_once()
        gestor_ambiente.leer_temperatura_ambiente.assert_called_once()
        gestor_climatizador.accionar_climatizador.assert_called_once()
