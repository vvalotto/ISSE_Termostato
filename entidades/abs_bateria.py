from abc import ABCMeta, abstractmethod


class AbsProxyBateria(metaclass=ABCMeta):

    @abstractmethod
    def leer_carga(self):
        pass
