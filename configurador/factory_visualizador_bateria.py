"""
Factory para crear visualizadores de nivel de bateria.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_actuadores.visualizador_bateria import (
    AbsVisualizadorBateria,
    VisualizadorBateria,
    VisualizadorBateriaSocket,
    VisualizadorBateriaApi
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryVisualizadorBateria(RegistryFactory):
    """Factory para crear instancias de visualizador de bateria."""

    _registry = {}


FactoryVisualizadorBateria.registrar("archivo", lambda **kw: VisualizadorBateria())
FactoryVisualizadorBateria.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: VisualizadorBateriaSocket(host, puerto)
)
FactoryVisualizadorBateria.registrar(
    "api",
    lambda api_url=None, **kw: VisualizadorBateriaApi(api_url)
)
