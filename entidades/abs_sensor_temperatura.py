from abc import ABCMeta, abstractmethod


class AbsProxySensorTemperatura(metaclass=ABCMeta):

    @abstractmethod
    def leer_temperatura(self):
        pass
