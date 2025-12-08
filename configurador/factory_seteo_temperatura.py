"""
Factory para crear componentes de seteo de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_sensores.proxy_seteo_temperatura import (
    AbsSeteoTemperatura,
    SeteoTemperatura,
    SeteoTemperaturaSocket
)


# pylint: disable=too-few-public-methods
class FactorySeteoTemperatura:
    """Factory para crear instancias de seteo de temperatura."""

    @staticmethod
    def crear(tipo: str, host: str = None, puerto: int = None) -> AbsSeteoTemperatura:
        """
        Crea un componente de seteo de temperatura segun el tipo especificado.

        Args:
            tipo (str): Tipo de seteo ("consola" o "socket").
            host (str): Direccion IP (requerido si tipo es "socket").
            puerto (int): Puerto TCP (requerido si tipo es "socket").

        Returns:
            AbsSeteoTemperatura: Instancia del componente o None si tipo invalido.
        """
        if tipo == "consola":
            return SeteoTemperatura()
        if tipo == "socket":
            return SeteoTemperaturaSocket(host, puerto)
        return None
