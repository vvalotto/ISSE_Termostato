"""
Factory para crear selectores de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_sensores.proxy_selector_temperatura import (
    AbsSelectorTemperatura,
    SelectorTemperaturaArchivo,
    SelectorTemperaturaSocket
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactorySelectorTemperatura(RegistryFactory):
    """Factory para crear instancias de selector de temperatura."""

    _registry = {}


FactorySelectorTemperatura.registrar("archivo", lambda **kw: SelectorTemperaturaArchivo())
FactorySelectorTemperatura.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: SelectorTemperaturaSocket(host, puerto)
)
