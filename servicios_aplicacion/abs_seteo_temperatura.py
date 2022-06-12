from abc import ABCMeta, abstractmethod


class AbsSeteoTemperatura(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def obtener_seteo():
        pass
