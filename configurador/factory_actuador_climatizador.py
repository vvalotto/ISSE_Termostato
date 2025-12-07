"""
Factory para crear actuadores de climatizador.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral
from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador


# pylint: disable=too-few-public-methods
class FactoryActuadorClimatizador:
    """Factory para crear instancias de actuador de climatizador."""

    @staticmethod
    def crear(tipo: str) -> AbsProxyActuadorClimatizador:
        """
        Crea un actuador de climatizador segun el tipo especificado.

        Args:
            tipo (str): Tipo de actuador ("general").

        Returns:
            AbsProxyActuadorClimatizador: Instancia del actuador o None si tipo invalido.
        """
        if tipo == "general":
            return ActuadorClimatizadorGeneral()
        return None
