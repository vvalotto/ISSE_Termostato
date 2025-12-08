"""
Factory para crear proxies de sensor de temperatura.

Patron de Diseno:
    - Factory Method: Crea objetos sin especificar la clase exacta
"""
from agentes_sensores.proxy_sensor_temperatura import (
    AbsProxySensorTemperatura,
    ProxySensorTemperaturaArchivo,
    ProxySensorTemperaturaSocket
)


# pylint: disable=too-few-public-methods
class FactoryProxySensorTemperatura:
    """Factory para crear instancias de proxy de sensor de temperatura."""

    @staticmethod
    def crear(tipo: str, host: str = None, puerto: int = None) -> AbsProxySensorTemperatura:
        """
        Crea un proxy de sensor de temperatura segun el tipo especificado.

        Args:
            tipo (str): Tipo de proxy ("archivo" o "socket").
            host (str): Direccion IP (requerido si tipo es "socket").
            puerto (int): Puerto TCP (requerido si tipo es "socket").

        Returns:
            AbsProxySensorTemperatura: Instancia del proxy o None si tipo invalido.
        """
        if tipo == "archivo":
            return ProxySensorTemperaturaArchivo()
        if tipo == "socket":
            return ProxySensorTemperaturaSocket(host, puerto)
        return None
