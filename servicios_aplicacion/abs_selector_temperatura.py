from abc import ABCMeta, abstractmethod


class AbsSelectorTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def obtener_selector():
        pass
