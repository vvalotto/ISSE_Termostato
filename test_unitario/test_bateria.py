from unittest import TestCase
from entidades.bateria import *


class TestBateria(TestCase):

    def setUp(self) -> None:
        self._bateria = Bateria(5, 0.8)
        self._bateria.nivel_de_carga = 5

    def test_nivel_de_carga(self):
        self.assertEqual(self._bateria.nivel_de_carga, 5)

    def test_indicador_normal(self):
        self.assertEqual(self._bateria.indicador, "NORMAL")

    def test_indicador_baja(self):
        self._bateria.nivel_de_carga = 3
        self.assertEqual(self._bateria.indicador, "BAJA")

    def test_indicador_normal_frontera(self):
        self._bateria.nivel_de_carga = 4.1
        self.assertEqual(self._bateria.indicador, "NORMAL")

    def test_indicador_baja_frontera(self):
        self._bateria.nivel_de_carga = 4
        self.assertEqual(self._bateria.indicador, "BAJA")


