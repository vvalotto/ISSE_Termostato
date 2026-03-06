"""
Factory para crear proxies de lectura de bateria.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_sensores.proxy_bateria import (
    AbsProxyBateria,
    ProxyBateriaArchivo,
    ProxyBateriaSocket
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryProxyBateria(RegistryFactory):
    """Factory para crear instancias de proxy de bateria."""

    _registry = {}


FactoryProxyBateria.registrar("archivo", lambda **kw: ProxyBateriaArchivo())
FactoryProxyBateria.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: ProxyBateriaSocket(host, puerto)
)
