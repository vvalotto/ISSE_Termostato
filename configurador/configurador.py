"""
Clase que define que componentes se usaran
"""

from agentes_sensores.proxy_bateria import *
from agentes_sensores.proxy_sensor_temperatura import *


class Configurador:

    @staticmethod
    def configurar_proxy_bateria():
        return ProxyBateriaSocket()

    @staticmethod
    def configurar_proxy_temperatura():
        return ProxySensorTemperaturaSocket()
