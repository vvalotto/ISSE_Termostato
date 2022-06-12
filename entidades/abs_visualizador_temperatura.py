"""

"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        pass

    @staticmethod
    @abstractmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        pass
