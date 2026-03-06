"""
Factory para crear componentes de seteo de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_sensores.proxy_seteo_temperatura import (
    AbsSeteoTemperatura,
    SeteoTemperatura,
    SeteoTemperaturaSocket
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactorySeteoTemperatura(RegistryFactory):
    """Factory para crear instancias de seteo de temperatura."""

    _registry = {}


FactorySeteoTemperatura.registrar("consola", lambda **kw: SeteoTemperatura())
FactorySeteoTemperatura.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: SeteoTemperaturaSocket(host, puerto)
)
