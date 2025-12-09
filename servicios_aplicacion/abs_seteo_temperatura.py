"""
Abstraccion para seteo de temperatura.

Define la interfaz para componentes que obtienen comandos del usuario
para ajustar la temperatura deseada.
"""
from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class AbsSeteoTemperatura(metaclass=ABCMeta):
    """Interfaz abstracta para obtener comandos de seteo de temperatura."""

    @abstractmethod
    def obtener_seteo(self):
        """Obtiene comando: 'aumentar', 'disminuir' o None."""
