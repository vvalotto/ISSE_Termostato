"""
Creacion del tipo especifico del climatizador.

Este modulo contiene el factory para crear instancias de climatizadores
(Climatizador o Calefactor) segun la configuracion del sistema.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from entidades.climatizador import Climatizador, Calefactor, AbsClimatizador


# pylint: disable=too-few-public-methods
class FactoryClimatizador:
    """Factory para crear instancias de climatizadores."""

    @staticmethod
    def crear(tipo: str, histeresis: float = 2) -> AbsClimatizador:
        """
        Crea una instancia del climatizador segun el tipo especificado.

        Args:
            tipo (str): Tipo de climatizador ("climatizador" o "calefactor").
            histeresis (float): Margen de tolerancia en grados. Por defecto 2.

        Returns:
            AbsClimatizador: Instancia del climatizador o None si tipo invalido.
        """
        if tipo == "climatizador":
            return Climatizador(histeresis=histeresis)
        if tipo == "calefactor":
            return Calefactor(histeresis=histeresis)
        return None
