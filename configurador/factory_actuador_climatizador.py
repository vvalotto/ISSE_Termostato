"""
Factory para crear actuadores de climatizador.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral
from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador
from registrador.registrador import RegistradorArchivo, AuditorArchivo
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryActuadorClimatizador(RegistryFactory):
    """Factory para crear instancias de actuador de climatizador."""

    _registry = {}


FactoryActuadorClimatizador.registrar(
    "general",
    lambda **kw: ActuadorClimatizadorGeneral(
        registrador=RegistradorArchivo(),
        auditor=AuditorArchivo()
    )
)
