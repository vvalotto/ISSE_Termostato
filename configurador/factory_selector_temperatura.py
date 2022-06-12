"""
Creación del tipo especifico del selector de temperatura
"""

from agentes_sensores.proxy_selector_temperatura import *


class FactorySelectorTemperatura:

    @staticmethod
    def crear(tipo: str) -> AbsSelectorTemperatura:

        if tipo == "archivo":
            return SelectorTemperaturaArchivo()
        else:
            return None
