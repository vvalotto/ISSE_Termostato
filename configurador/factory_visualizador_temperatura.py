"""
Creación del tipo especifico visualizador de estado del climatizador
"""

from agentes_actuadores.visualizador_temperatura import *


class FactoryVisualizadorTemperatura:

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorTemperatura:

        if tipo == "archivo":
            return VisualizadorTemperatura()
        elif tipo == "socket":
            return VisualizadorTemperaturaSocket()
        elif tipo == "webapi":
            return VisualizadorTemperaturaWebApi()
        else:
            return None
