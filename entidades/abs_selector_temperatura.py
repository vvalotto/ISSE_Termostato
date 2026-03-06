"""
Abstraccion para selector de modo de temperatura.

Define la interfaz para componentes que determinan si mostrar
la temperatura ambiente o la deseada.
"""
from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class AbsSelectorTemperatura(metaclass=ABCMeta):
    """Interfaz abstracta para selector de modo de temperatura."""

    @staticmethod
    @abstractmethod
    def obtener_selector():
        """Obtiene el modo actual: 'ambiente' o 'deseada'."""
