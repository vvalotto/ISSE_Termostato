"""
Factory para crear selectores de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_sensores.proxy_selector_temperatura import (
    AbsSelectorTemperatura,
    SelectorTemperaturaArchivo,
    SelectorTemperaturaSocket
)


# pylint: disable=too-few-public-methods
class FactorySelectorTemperatura:
    """Factory para crear instancias de selector de temperatura."""

    @staticmethod
    def crear(tipo: str, host: str = None, puerto: int = None) -> AbsSelectorTemperatura:
        """
        Crea un selector de temperatura segun el tipo especificado.

        Args:
            tipo (str): Tipo de selector ("archivo" o "socket").
            host (str): Direccion IP (requerido si tipo es "socket").
            puerto (int): Puerto TCP (requerido si tipo es "socket").

        Returns:
            AbsSelectorTemperatura: Instancia del selector o None si tipo invalido.
        """
        if tipo == "archivo":
            return SelectorTemperaturaArchivo()
        if tipo == "socket":
            return SelectorTemperaturaSocket(host, puerto)
        return None
