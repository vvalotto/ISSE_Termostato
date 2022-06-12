"""
Creación del tipo especifico visualizador de estado del climatizador
"""

from agentes_actuadores.visualizador_climatizador import *


class FactoryVisualizadorClimatizador:

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorClimatizador:

        if tipo == "archivo":
            return VisualizadorClimatizador()
        elif tipo == "socket":
            return VisualizadorClimatizadorSocket()
        else:
            return None