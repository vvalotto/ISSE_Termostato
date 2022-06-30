from unittest import TestCase
from servicios_dominio.controlador_climatizador import *


class TestControladorTemperatura(TestCase):

    def setUp(self) -> None:
        self._controlador = ControladorTemperatura()

    def test_comparar_temperatura_alta(self):
        self.assertEqual(self._controlador.comparar_temperatura(28, 24), "alta")

    def test_comparar_temperatura_alta_de_frontera(self):
        self.assertEqual(self._controlador.comparar_temperatura(27, 24), "alta")

    def test_comparar_temperatura_alta_de_frontera_dentro_de_histeris(self):
        self.assertEqual(self._controlador.comparar_temperatura(26, 24), "normal")

    def test_comparar_temperatura_dentro_de_histersis(self):
        self.assertEqual(self._controlador.comparar_temperatura(25, 24), "normal")

    def test_comparar_temperatura_baja_de_frontera_dentro_de_histeris(self):
        self.assertEqual(self._controlador.comparar_temperatura(22, 24), "normal")

    def test_comparar_temperatura_baja_de_frontera(self):
        self.assertEqual(self._controlador.comparar_temperatura(21, 24), "baja")

    def test_comparar_temperatura_baja(self):
        self.assertEqual(self._controlador.comparar_temperatura(20, 24), "baja")
