"""
Factory para crear proxies de lectura de bateria.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_sensores.proxy_bateria import (
    AbsProxyBateria,
    ProxyBateriaArchivo,
    ProxyBateriaSocket
)


# pylint: disable=too-few-public-methods
class FactoryProxyBateria:
    """Factory para crear instancias de proxy de bateria."""

    @staticmethod
    def crear(tipo: str, host: str = None, puerto: int = None) -> AbsProxyBateria:
        """
        Crea un proxy de bateria segun el tipo especificado.

        Args:
            tipo (str): Tipo de proxy ("archivo" o "socket").
            host (str): Direccion IP (requerido si tipo es "socket").
            puerto (int): Puerto TCP (requerido si tipo es "socket").

        Returns:
            AbsProxyBateria: Instancia del proxy o None si tipo invalido.
        """
        if tipo == "archivo":
            return ProxyBateriaArchivo()
        if tipo == "socket":
            return ProxyBateriaSocket(host, puerto)
        return None
