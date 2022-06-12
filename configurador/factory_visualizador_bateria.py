"""
Creación del tipo especifico visualizador de nivel de bateria
"""

from agentes_actuadores.visualizador_bateria import *


class FactoryVisualizadorBateria:

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorBateria:

        if tipo == "archivo":
            return VisualizadorBateria()
        elif tipo == "socket":
            return VisualizadorBateriaSocket()
        else:
            return None
