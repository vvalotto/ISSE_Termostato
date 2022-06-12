"""
Creación del tipo especifico del seteo de temperatura
"""

from agentes_sensores.proxy_seteo_temperatura import *


class FactorySeteoTemperatura:

    @staticmethod
    def crear(tipo: str) -> AbsSeteoTemperatura:

        if tipo == "consola":
            return SeteoTemperatura()
        if tipo == "socket":
            return SeteoTemperaturaSocket()
        else:
            return None
