"""
Clase que representa el ambiente a climatizar
"""


class Ambiente:

    @property
    def temperatura_ambiente(self):
        return self.__temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        self.__temperatura_ambiente = valor
        return

    @property
    def temperatura_deseada(self):
        return self.__temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        self.__temperatura_deseada = valor
        return

    @property
    def temperatura_a_mostrar(self):
        return self.__temperatura_a_mostrar

    @temperatura_a_mostrar.setter
    def temperatura_a_mostrar(self, valor):
        self.__temperatura_a_mostrar = valor
        return

    def __init__(self):
        self.__temperatura_ambiente = 0
        self.__temperatura_deseada = 0
        self.__temperatura_a_mostrar = "ambiente"
        return
