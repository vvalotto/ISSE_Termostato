"""
Creación del tipo especifico del actuador del climatizador
"""

from agentes_actuadores.actuador_climatizador import *


class FactoryActuadorClimatizador:

    @staticmethod
    def crear(tipo: str) -> AbsActuadorClimatizador:

        if tipo == "general":
            return ActuadorClimatizadorGeneral()
        else:
            return None