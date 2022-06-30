import unittest
from entidades.ambiente import *


class TestAmbiente(unittest.TestCase):

    def setUp(self) -> None:
        self.__ambiente = Ambiente()

    def test_temperatura_ambiente(self):
        self.__ambiente.temperatura_ambiente = 20
        self.assertEqual(self.__ambiente.temperatura_ambiente, 20)

    def test_temperatura_deseada(self):
        self.__ambiente.temperatura_deseada = 24
        self.assertAlmostEqual(self.__ambiente.temperatura_deseada, 24)

    def test_temperatura_a_mostrar(self):
        self.__ambiente.temperatura_a_mostrar = "ambiente"
        self.assertAlmostEqual(self.__ambiente.temperatura_a_mostrar, "ambiente")
