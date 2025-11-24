"""
Tests unitarios para las entidades Climatizador y Calefactor

Casos de prueba del Plan de Pruebas - Maquina de Estados Climatizador:
- CLI-001: apagado + calentar -> calentando
- CLI-002: apagado + enfriar -> enfriando
- CLI-003: calentando + apagar -> apagado
- CLI-004: enfriando + apagar -> apagado
- CLI-005: calentando + enfriar -> (no definido en maquina)
- CLI-006: enfriando + calentar -> (no definido en maquina)
- CLI-007: apagado + None -> apagado (sin cambio)

Casos de prueba - Maquina de Estados Calefactor:
- CAL-001: apagado + calentar -> calentando
- CAL-002: calentando + apagar -> apagado
- CAL-003: apagado + enfriar -> apagado (transicion definida)
- CAL-004: calentando + enfriar -> (no definido, lanza excepcion)
"""
import pytest
from entidades.climatizador import Climatizador, Calefactor
from entidades.ambiente import Ambiente


class TestClimatizadorMaquinaEstados:
    """Tests para la maquina de estados del Climatizador"""

    # CLI-001: apagado -> calentar -> calentando
    def test_transicion_apagado_a_calentando(self, climatizador):
        """Desde apagado, al calentar debe pasar a calentando"""
        assert climatizador.estado == "apagado"
        climatizador.proximo_estado("calentar")
        assert climatizador.estado == "calentando"

    # CLI-002: apagado -> enfriar -> enfriando
    def test_transicion_apagado_a_enfriando(self, climatizador):
        """Desde apagado, al enfriar debe pasar a enfriando"""
        assert climatizador.estado == "apagado"
        climatizador.proximo_estado("enfriar")
        assert climatizador.estado == "enfriando"

    # CLI-003: calentando -> apagar -> apagado
    def test_transicion_calentando_a_apagado(self, climatizador):
        """Desde calentando, al apagar debe pasar a apagado"""
        climatizador.proximo_estado("calentar")
        assert climatizador.estado == "calentando"
        climatizador.proximo_estado("apagar")
        assert climatizador.estado == "apagado"

    # CLI-004: enfriando -> apagar -> apagado
    def test_transicion_enfriando_a_apagado(self, climatizador):
        """Desde enfriando, al apagar debe pasar a apagado"""
        climatizador.proximo_estado("enfriar")
        assert climatizador.estado == "enfriando"
        climatizador.proximo_estado("apagar")
        assert climatizador.estado == "apagado"

    # CLI-005: calentando -> enfriar -> excepcion (no definida)
    def test_transicion_calentando_enfriar_lanza_excepcion(self, climatizador):
        """Desde calentando, al enfriar debe lanzar excepcion (transicion no definida)"""
        climatizador.proximo_estado("calentar")
        with pytest.raises(Exception):
            climatizador.proximo_estado("enfriar")

    # CLI-006: enfriando -> calentar -> excepcion (no definida)
    def test_transicion_enfriando_calentar_lanza_excepcion(self, climatizador):
        """Desde enfriando, al calentar debe lanzar excepcion (transicion no definida)"""
        climatizador.proximo_estado("enfriar")
        with pytest.raises(Exception):
            climatizador.proximo_estado("calentar")

    def test_estado_inicial_es_apagado(self, climatizador):
        """El estado inicial debe ser apagado"""
        assert climatizador.estado == "apagado"


class TestCalefactorMaquinaEstados:
    """Tests para la maquina de estados del Calefactor"""

    # CAL-001: apagado -> calentar -> calentando
    def test_transicion_apagado_a_calentando(self, calefactor):
        """Desde apagado, al calentar debe pasar a calentando"""
        assert calefactor.estado == "apagado"
        calefactor.proximo_estado("calentar")
        assert calefactor.estado == "calentando"

    # CAL-002: calentando -> apagar -> apagado
    def test_transicion_calentando_a_apagado(self, calefactor):
        """Desde calentando, al apagar debe pasar a apagado"""
        calefactor.proximo_estado("calentar")
        assert calefactor.estado == "calentando"
        calefactor.proximo_estado("apagar")
        assert calefactor.estado == "apagado"

    # CAL-003: apagado -> enfriar -> apagado (transicion definida en calefactor)
    def test_transicion_apagado_enfriar_permanece_apagado(self, calefactor):
        """Desde apagado, al enfriar debe permanecer apagado (calefactor no enfria)"""
        assert calefactor.estado == "apagado"
        calefactor.proximo_estado("enfriar")
        assert calefactor.estado == "apagado"

    # CAL-004: calentando -> enfriar -> excepcion (no definida)
    def test_transicion_calentando_enfriar_lanza_excepcion(self, calefactor):
        """Desde calentando, al enfriar debe lanzar excepcion"""
        calefactor.proximo_estado("calentar")
        with pytest.raises(Exception):
            calefactor.proximo_estado("enfriar")

    def test_estado_inicial_es_apagado(self, calefactor):
        """El estado inicial debe ser apagado"""
        assert calefactor.estado == "apagado"


class TestClimatizadorEvaluarAccion:
    """Tests para evaluar_accion del Climatizador"""

    def test_evaluar_accion_temperatura_baja_retorna_calentar(self, climatizador, ambiente_frio):
        """Con temperatura baja, debe retornar 'calentar'"""
        accion = climatizador.evaluar_accion(ambiente_frio)
        assert accion == "calentar"

    def test_evaluar_accion_temperatura_alta_retorna_enfriar(self, climatizador, ambiente_caliente):
        """Con temperatura alta, debe retornar 'enfriar'"""
        accion = climatizador.evaluar_accion(ambiente_caliente)
        assert accion == "enfriar"

    def test_evaluar_accion_temperatura_normal_retorna_none(self, climatizador, ambiente_normal):
        """Con temperatura normal, debe retornar None"""
        accion = climatizador.evaluar_accion(ambiente_normal)
        assert accion is None

    def test_evaluar_accion_calentando_temperatura_alta_retorna_apagar(self, climatizador, ambiente_caliente):
        """Calentando con temperatura alta, debe retornar 'apagar'"""
        climatizador.proximo_estado("calentar")
        accion = climatizador.evaluar_accion(ambiente_caliente)
        assert accion == "apagar"

    def test_evaluar_accion_enfriando_temperatura_baja_retorna_apagar(self, climatizador, ambiente_frio):
        """Enfriando con temperatura baja, debe retornar 'apagar'"""
        climatizador.proximo_estado("enfriar")
        accion = climatizador.evaluar_accion(ambiente_frio)
        assert accion == "apagar"


class TestCalefactorEvaluarAccion:
    """Tests para evaluar_accion del Calefactor"""

    def test_evaluar_accion_temperatura_baja_retorna_calentar(self, calefactor, ambiente_frio):
        """Con temperatura baja, debe retornar 'calentar'"""
        accion = calefactor.evaluar_accion(ambiente_frio)
        assert accion == "calentar"

    def test_evaluar_accion_temperatura_alta_retorna_none(self, calefactor, ambiente_caliente):
        """Con temperatura alta, calefactor no puede enfriar, retorna None o apagar"""
        accion = calefactor.evaluar_accion(ambiente_caliente)
        # Calefactor apagado con temp alta no hace nada
        assert accion is None

    def test_evaluar_accion_calentando_temperatura_normal_retorna_apagar(self, calefactor, ambiente_normal):
        """Calentando con temperatura normal, debe retornar 'apagar'"""
        calefactor.proximo_estado("calentar")
        accion = calefactor.evaluar_accion(ambiente_normal)
        assert accion == "apagar"
