"""
Creación del tipo especifico del sensor de temperatura
"""

from agentes_sensores.proxy_sensor_temperatura import *


class FactoryProxySensorTemperatura:

    @staticmethod
    def crear(tipo: str) -> AbsProxySensorTemperatura:

        if tipo == "archivo":
            return ProxySensorTemperaturaArchivo()
        elif tipo == "socket":
            return ProxySensorTemperaturaSocket()
        else:
            return None