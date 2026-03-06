"""
Factory para crear visualizadores de estado del climatizador.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_actuadores.visualizador_climatizador import (
    AbsVisualizadorClimatizador,
    VisualizadorClimatizador,
    VisualizadorClimatizadorSocket,
    VisualizadorClimatizadorApi
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryVisualizadorClimatizador(RegistryFactory):
    """Factory para crear instancias de visualizador de climatizador."""

    _registry = {}


FactoryVisualizadorClimatizador.registrar("archivo", lambda **kw: VisualizadorClimatizador())
FactoryVisualizadorClimatizador.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: VisualizadorClimatizadorSocket(host, puerto)
)
FactoryVisualizadorClimatizador.registrar(
    "api",
    lambda api_url=None, **kw: VisualizadorClimatizadorApi(api_url)
)
