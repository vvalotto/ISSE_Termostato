"""
Factory para crear visualizadores de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_actuadores.visualizador_temperatura import (
    AbsVisualizadorTemperatura,
    VisualizadorTemperatura,
    VisualizadorTemperaturaSocket,
    VisualizadorTemperaturaApi
)


# pylint: disable=too-few-public-methods
class FactoryVisualizadorTemperatura:
    """Factory para crear instancias de visualizador de temperatura."""

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorTemperatura:
        """
        Crea un visualizador de temperatura segun el tipo especificado.

        Args:
            tipo (str): Tipo de visualizador ("archivo", "socket" o "api").

        Returns:
            AbsVisualizadorTemperatura: Instancia del visualizador o None si tipo invalido.
        """
        if tipo == "archivo":
            return VisualizadorTemperatura()
        if tipo == "socket":
            return VisualizadorTemperaturaSocket()
        if tipo == "api":
            return VisualizadorTemperaturaApi()
        return None
