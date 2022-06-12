"""

"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorBateria(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def mostrar_tension(tension_bateria):
        pass

    @staticmethod
    @abstractmethod
    def mostrar_indicador(indicador_bateria):
        pass
