"""
Factory para crear visualizadores de nivel de bateria.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_actuadores.visualizador_bateria import (
    AbsVisualizadorBateria,
    VisualizadorBateria,
    VisualizadorBateriaSocket,
    VisualizadorBateriaApi
)


# pylint: disable=too-few-public-methods
class FactoryVisualizadorBateria:
    """Factory para crear instancias de visualizador de bateria."""

    @staticmethod
    def crear(tipo: str) -> AbsVisualizadorBateria:
        """
        Crea un visualizador de bateria segun el tipo especificado.

        Args:
            tipo (str): Tipo de visualizador ("archivo", "socket" o "api").

        Returns:
            AbsVisualizadorBateria: Instancia del visualizador o None si tipo invalido.
        """
        if tipo == "archivo":
            return VisualizadorBateria()
        if tipo == "socket":
            return VisualizadorBateriaSocket()
        if tipo == "api":
            return VisualizadorBateriaApi()
        return None
