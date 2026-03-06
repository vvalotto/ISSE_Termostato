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
    def crear(tipo: str, host: str = None, puerto: int = None,
              api_url: str = None) -> AbsVisualizadorClimatizador:
        """
        Crea un visualizador de climatizador segun el tipo especificado.

        Args:
            tipo (str): Tipo de visualizador ("archivo", "socket" o "api").
            host (str): Direccion IP del servidor (requerido si tipo es "socket").
            puerto (int): Puerto TCP del servidor (requerido si tipo es "socket").
            api_url (str): URL de la API REST (requerido si tipo es "api").

        Returns:
            AbsVisualizadorClimatizador: Instancia del visualizador o None si tipo invalido.
        """
        if tipo == "archivo":
            return VisualizadorClimatizador()
        if tipo == "socket":
            return VisualizadorClimatizadorSocket(host, puerto)
        if tipo == "api":
            return VisualizadorClimatizadorApi(api_url)
        return None
