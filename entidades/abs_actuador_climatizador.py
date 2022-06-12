"""

"""

from abc import ABCMeta, abstractmethod


class AbsActuadorClimatizador(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def accionar_climatizador(accion):
        pass