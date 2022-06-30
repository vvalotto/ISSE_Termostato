import unittest
from entidades.ambiente import *


class TestAmbiente(unittest.TestCase):

    def setUp(self) -> None:
        self._ambiente = Ambiente()
        self._ambiente.temperatura_deseada = 24
        self._ambiente.temperatura_ambiente = 19
        self._ambiente.temperatura_a_mostrar = "deseada"

    def test_temperatura_ambiente(self):
        self.assertEqual(self._ambiente.temperatura_ambiente, 19)

    def test_temperatura_deseada(self):
        self.assertEqual(self._ambiente.temperatura_deseada, 24)

    def test_temperatura_a_mostrar_deseada(self):
        self.assertEqual(self._ambiente.temperatura_a_mostrar, "deseada")

    def test_temperatura_a_mostrar_ambiente(self):
        self._ambiente.temperatura_a_mostrar = "ambiente"
        self.assertEqual(self._ambiente.temperatura_a_mostrar, "ambiente")

    def test_temperatura_a_mostrar_deseada_incorrecta(self):
        self._ambiente.temperatura_a_mostrar = "ambiente"
        self.assertNotEqual(self._ambiente.temperatura_a_mostrar, "deseada")

    def test_ambiente_repr(self):
        repr_ambiente = 'Ambiente: ' + str(19) + ' - ' + \
                        'Deseada: ' + str(24) + ' - ' + \
                        'a mostrar: ' + 'ambiente'

    def test_ambiente_inicializado(self):
        ambiente_inicial = Ambiente()
        self.assertEqual(ambiente_inicial.temperatura_ambiente, 0)
        self.assertEqual(ambiente_inicial.temperatura_deseada, 0)
        self.assertEqual(ambiente_inicial.temperatura_a_mostrar, "ambiente")




