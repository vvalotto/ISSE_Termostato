import unittest
from entidades.ambiente import *


class TestAmbiente(unittest.TestCase):

    def test_temperatura_ambiente(self):
        Ambiente.temperatura_ambiente = 5
        self.assertEqual(Ambiente.temperatura_ambiente, 5)

    def test_temperatura_deseada(self):
        Ambiente.temperatura_deseada = 5
        self.assertAlmostEqual(Ambiente.temperatura_deseada, 5)

    def test_temperatura_a_mostrar(self):
        Ambiente.temperatura_a_mostrar = "ambiente"
        self.assertAlmostEqual(Ambiente.temperatura_a_mostrar, "ambiente")