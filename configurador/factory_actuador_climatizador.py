"""
Creación del tipo especifico del actuador del climatizador
"""

from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral
from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador


class FactoryActuadorClimatizador:

    @staticmethod
    def crear(tipo: str) -> AbsProxyActuadorClimatizador:

        if tipo == "general":
            return ActuadorClimatizadorGeneral()
        else:
            return None