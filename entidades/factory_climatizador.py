"""
Creación del tipo especifico del climarizador
"""

from entidades.climatizador import *


class FactoryClimatizador:

    @staticmethod
    def crear(tipo: str) -> AbsClimatizador:

        if tipo == "climatizador":
            return Climatizador()
        elif tipo == "calefactor":
            return Calefactor()
        else:
            return None
