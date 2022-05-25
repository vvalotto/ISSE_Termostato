"""
Clase que representa la bateria que alimenta al dispositivo
"""


class Bateria:

    carga_maxima = 5

    def __init__(self):
        self.__indicador = None
        self.__nivel_de_carga = None

    @property
    def nivel_de_carga(self):
        return self.__nivel_de_carga

    @property
    def indicador(self):
        return self.__indicador

    @nivel_de_carga.setter
    def nivel_de_carga(self, valor):
        if valor <= Bateria.carga_maxima * 0.80:
            self.__indicador = "BAJA"
            self.__nivel_de_carga = valor
        else:
            self.__indicador = "NORMAL"
        self.__nivel_de_carga = valor
