"""
Tests de integracion para servicios_aplicacion/lanzador.py

Casos de prueba:
- LNZ-INT-001: __init__ crea los tres gestores con tipos correctos
- LNZ-INT-002: __init__ crea _presentador (Presentador) y _operador (OperadorParalelo)
- LNZ-INT-003: ejecutar() llama Inicializador.iniciar con gestor_bateria, gestor_ambiente y presentador
- LNZ-INT-004: ejecutar() llama _operador.ejecutar() si Inicializador retorna True
"""
import pytest
from unittest.mock import Mock, patch, call
from servicios_aplicacion.lanzador import Lanzador
from servicios_aplicacion.presentador import Presentador
from servicios_aplicacion.operador_paralelo import OperadorParalelo
from gestores_entidades.gestor_bateria import GestorBateria
from gestores_entidades.gestor_ambiente import GestorAmbiente
from gestores_entidades.gestor_climatizador import GestorClimatizador


_CFG_PATH = "servicios_aplicacion.lanzador.Configurador"
_SEL_CFG_PATH = "servicios_aplicacion.selector_entrada.Configurador"
_VEC_PATH = "servicios_aplicacion.lanzador.VisualizadorEstadoConsolidadoSocket"


@pytest.fixture
def lanzador():
    """Lanzador con Configurador y visualizador consolidado mockeados."""
    with patch.multiple(
        _CFG_PATH,
        obtener_carga_maxima_bateria=Mock(return_value=5.0),
        obtener_umbral_bateria=Mock(return_value=0.95),
        configurar_proxy_bateria=Mock(return_value=Mock()),
        configurar_visualizador_bateria=Mock(return_value=Mock()),
        obtener_temperatura_inicial=Mock(return_value=24.0),
        configurar_proxy_temperatura=Mock(return_value=Mock()),
        configurar_visualizador_temperatura=Mock(return_value=Mock()),
        obtener_incremento_temperatura=Mock(return_value=1.0),
        configurar_climatizador=Mock(return_value=Mock()),
        configurar_actuador_climatizador=Mock(return_value=Mock()),
        configurar_visualizador_climatizador=Mock(return_value=Mock()),
    ):
        with patch(_VEC_PATH):
            with patch(_SEL_CFG_PATH) as cfg_sel:
                cfg_sel.configurar_seteo_temperatura.return_value = Mock()
                cfg_sel.configurar_selector_temperatura.return_value = Mock()
                lnz = Lanzador()

    return lnz


class TestLanzadorConstructor:

    # LNZ-INT-001
    def test_constructor_crea_tres_gestores(self, lanzador):
        """__init__ crea _gestor_bateria, _gestor_ambiente y _gestor_climatizador con tipos correctos."""
        assert isinstance(lanzador._gestor_bateria, GestorBateria)
        assert isinstance(lanzador._gestor_ambiente, GestorAmbiente)
        assert isinstance(lanzador._gestor_climatizador, GestorClimatizador)

    # LNZ-INT-002
    def test_constructor_crea_presentador_y_operador(self, lanzador):
        """__init__ crea _presentador (Presentador) y _operador (OperadorParalelo)."""
        assert isinstance(lanzador._presentador, Presentador)
        assert isinstance(lanzador._operador, OperadorParalelo)


class TestLanzadorEjecutar:

    # LNZ-INT-003
    def test_ejecutar_llama_inicializador_iniciar(self, lanzador):
        """ejecutar() llama Inicializador.iniciar con los gestores y el presentador."""
        with patch("servicios_aplicacion.lanzador.Inicializador.iniciar", return_value=False) as mock_iniciar:
            lanzador.ejecutar()
        mock_iniciar.assert_called_once_with(
            lanzador._gestor_bateria,
            lanzador._gestor_ambiente,
            lanzador._presentador
        )

    # LNZ-INT-004
    def test_ejecutar_llama_operador_si_inicializacion_exitosa(self, lanzador):
        """ejecutar() llama _operador.ejecutar() cuando Inicializador retorna True."""
        with patch("servicios_aplicacion.lanzador.Inicializador.iniciar", return_value=True):
            with patch.object(lanzador._operador, "ejecutar") as mock_ejecutar:
                lanzador.ejecutar()
        mock_ejecutar.assert_called_once()
