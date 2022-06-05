"""
Clase que representa la bateria que alimenta al dispositivo
"""


class Bateria:

    @property
    def nivel_de_carga(self):
        return self.__nivel_de_carga

    @property
    def indicador(self):
        return self.__indicador

    @nivel_de_carga.setter
    def nivel_de_carga(self, valor):
        if valor <= self.__carga_maxima * self.__umbral_de_carga:
            self.__indicador = "BAJA"
            self.__nivel_de_carga = valor
        else:
            self.__indicador = "NORMAL"
        self.__nivel_de_carga = valor

    def __init__(self, carga_maxima, umbral_del_carga):
        self.__carga_maxima = carga_maxima
        self.__umbral_de_carga = umbral_del_carga
        self.__nivel_de_carga = 0
        self.__indicador = None
