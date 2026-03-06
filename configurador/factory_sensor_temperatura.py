"""
Factory para crear proxies de sensor de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_sensores.proxy_sensor_temperatura import (
    AbsProxySensorTemperatura,
    ProxySensorTemperaturaArchivo,
    ProxySensorTemperaturaSocket
)
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryProxySensorTemperatura(RegistryFactory):
    """Factory para crear instancias de proxy de sensor de temperatura."""

    _registry = {}


FactoryProxySensorTemperatura.registrar("archivo", lambda **kw: ProxySensorTemperaturaArchivo())
FactoryProxySensorTemperatura.registrar(
    "socket",
    lambda host=None, puerto=None, **kw: ProxySensorTemperaturaSocket(host, puerto)
)
