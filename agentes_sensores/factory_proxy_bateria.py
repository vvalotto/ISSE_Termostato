"""
Creación del tipo especifico del proxy para leer la batería
"""

from agentes_sensores.proxy_bateria import *


class FactoryProxyBateria:

    @staticmethod
    def crear(tipo: str) -> AbsProxyBateria:

        if tipo == "archivo":
            return ProxyBateriaArchivo()
        elif tipo == "socket":
            return ProxyBateriaSocket()
        else:
            return None