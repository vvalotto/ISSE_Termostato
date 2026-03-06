"""
Creacion del tipo especifico del climatizador.

Este modulo contiene el factory para crear instancias de climatizadores
(Climatizador o Calefactor) segun la configuracion del sistema.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
    - Registry: Permite registrar nuevas implementaciones sin modificar este archivo
"""
from entidades.climatizador import Climatizador, Calefactor
from entidades.abs_climatizador import AbsClimatizador
from configurador.registry_factory import RegistryFactory


# pylint: disable=too-few-public-methods
class FactoryClimatizador(RegistryFactory):
    """Factory para crear instancias de climatizadores."""

    _registry = {}


FactoryClimatizador.registrar(
    "climatizador",
    lambda histeresis=2, **kw: Climatizador(histeresis=histeresis)
)
FactoryClimatizador.registrar(
    "calefactor",
    lambda histeresis=2, **kw: Calefactor(histeresis=histeresis)
)
