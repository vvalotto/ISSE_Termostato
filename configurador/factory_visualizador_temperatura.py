"""
Factory para crear visualizadores de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_actuadores.visualizador_temperatura import (
    AbsVisualizadorTemperatura,
    VisualizadorTemperatura,
    VisualizadorTemperaturaSocket,
    VisualizadorTemperaturaApi
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryVisualizadorTemperatura(RegistryFactory):
    """Factory para crear instancias de visualizador de temperatura."""

    _registry = {}


FactoryVisualizadorTemperatura.registrar("archivo", lambda **kw: VisualizadorTemperatura())
FactoryVisualizadorTemperatura.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: VisualizadorTemperaturaSocket(host, puerto)
)
FactoryVisualizadorTemperatura.registrar(
    "api",
    lambda api_url=None, **kw: VisualizadorTemperaturaApi(api_url)
)
