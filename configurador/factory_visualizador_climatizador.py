"""
Factory para crear visualizadores de estado del climatizador.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_actuadores.visualizador_climatizador import (
    AbsVisualizadorClimatizador,
    VisualizadorClimatizador,
    VisualizadorClimatizadorSocket,
    VisualizadorClimatizadorApi
)


# pylint: disable=too-few-public-methods
class FactoryVisualizadorClimatizador:
    """Factory para crear instancias de visualizador de climatizador."""

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorClimatizador:
        """
        Crea un visualizador de climatizador segun el tipo especificado.

        Args:
            tipo (str): Tipo de visualizador ("archivo", "socket" o "api").

        Returns:
            AbsVisualizadorClimatizador: Instancia del visualizador o None si tipo invalido.
        """
        if tipo == "archivo":
            return VisualizadorClimatizador()
        if tipo == "socket":
            return VisualizadorClimatizadorSocket()
        if tipo == "api":
            return VisualizadorClimatizadorApi()
        return None
