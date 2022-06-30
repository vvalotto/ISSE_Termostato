from unittest import TestCase
from entidades.climatizador import *
from entidades.ambiente import *


class TestClimatizador(TestCase):

    def setUp(self) -> None:
        self._climatizador = Climatizador()
        self._ambiente = Ambiente()

    def test__inicializar_maquina_estado(self):
        self.assertEqual(self._climatizador._maquina_estado[0],
                         [["apagado", "calentar"], "calentando"])
        self.assertEqual(self._climatizador._maquina_estado[1],
                         [["apagado", "enfriar"], "enfriando"])
        self.assertEqual(self._climatizador._maquina_estado[2],
                         [["calentando", "apagar"], "apagado"])
        self.assertEqual(self._climatizador._maquina_estado[3],
                         [["enfriando", "apagar"], "apagado"])

    def test_evaluar_accion_temperatura_alta(self):
        self._ambiente.temperatura_ambiente = 28
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         "enfriar")

    def test_evaluar_accion_temperatura_alta_de_frontera(self):
        self._ambiente.temperatura_ambiente = 27
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         "enfriar")

    def test_evaluar_accion_temperatura_alta_de_frontera_dentro_de_histeris(self):
        self._ambiente.temperatura_ambiente = 26
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         None)

    def test_evaluar_accion_temperatura_dentro_de_histeris(self):
        self._ambiente.temperatura_ambiente = 24
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         None)

    def test_evaluar_accion_temperatura_baja_de_frontera_dentro_de_histeris(self):
        self._ambiente.temperatura_ambiente = 22
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         None)

    def test_evaluar_accion_temperatura_baja_de_frontera(self):
        self._ambiente.temperatura_ambiente = 21
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         "calentar")

    def test_evaluar_accion_temperatura_baja(self):
        self._ambiente.temperatura_ambiente = 20
        self._ambiente.temperatura_deseada = 24
        self.assertEqual(self._climatizador.evaluar_accion(self._ambiente),
                         "calentar")

    def test__definir_accion_apagar_porque_es_alta_y_esta_calentando(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("calentar")
        self.assertEqual(self._climatizador._definir_accion("alta"), "apagar")

    def test__definir_accion_apagar_porque_es_baja_y_esta_enfriando(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("enfriar")
        self.assertEqual(self._climatizador._definir_accion("baja"), "apagar")

    def test__definir_accion_enfriar_porque_es_alta(self):
        self._climatizador._inicializar_maquina_estado()
        self.assertEqual(self._climatizador._definir_accion("alta"), "enfriar")

    def test__definir_accion_calentar_porque_es_baja(self):
        self._climatizador._inicializar_maquina_estado()
        self.assertEqual(self._climatizador._definir_accion("baja"), "calentar")

    def test__definir_accion_ninguna_porque_es_baja_y_esta_calentando(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("calentar")
        self.assertEqual(self._climatizador._definir_accion("baja"), None)

    def test__definir_accion_ninguna_porque_es_alta_y_esta_enfriando(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("enfriar")
        self.assertEqual(self._climatizador._definir_accion("alta"), None)
        pass

    def test_proximo_estado_calentado(self):
        self._climatizador._inicializar_maquina_estado()
        self.assertEqual(self._climatizador.proximo_estado("calentar"),
                         "calentando")

    def test_proximo_estado_apagado_desde_calentado(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("calentar")
        self.assertEqual(self._climatizador.proximo_estado("apagar"),
                         "apagado")

    def test_proximo_estado_enfriando(self):
        self.assertEqual(self._climatizador.proximo_estado("enfriar"),
                         "enfriando")

    def test_proximo_estado_apagado_desde_enfriando(self):
        self._climatizador._inicializar_maquina_estado()
        self._climatizador.proximo_estado("enfriar")
        self.assertEqual(self._climatizador.proximo_estado("apagar"),
                         "apagado")

    def test_proximo_estado_ciclo_completo(self):
        self._climatizador._inicializar_maquina_estado()
        self.assertEqual(self._climatizador.proximo_estado("calentar"),
                         "calentando")
        self.assertEqual(self._climatizador.proximo_estado("apagar"),
                         "apagado")
        self.assertEqual(self._climatizador.proximo_estado("enfriar"),
                         "enfriando")
        self.assertEqual(self._climatizador.proximo_estado("apagar"),
                         "apagado")
