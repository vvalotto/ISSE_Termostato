"""

"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorClimatizador(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def mostrar_estado_climatizador(tension_bateria):
        pass
