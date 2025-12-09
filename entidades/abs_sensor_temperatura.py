"""
Interfaz abstracta para proxies de sensor de temperatura (Patron Proxy).

Este modulo define el contrato que deben cumplir todos los proxies
que actuan como intermediarios para leer la temperatura ambiente.
El patron Proxy permite simular hardware fisico mediante diferentes
implementaciones (archivo, socket, sensores reales, etc.).

Ejemplo de uso:
    Las implementaciones concretas pueden leer temperatura desde:
    - Archivos locales (para simulacion y testing)
    - Sockets de red (para sensores remotos distribuidos)
    - Sensores fisicos (DHT22, DS18B20, etc. en produccion)
"""

from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class AbsProxySensorTemperatura(metaclass=ABCMeta):
    """
    Interfaz abstracta para proxies de lectura de temperatura.

    Define el contrato que deben implementar todos los proxies
    que actuan como intermediarios para obtener la temperatura
    ambiente del entorno a climatizar.

    Patron de diseno: Proxy
    Permite separar la logica de dominio del sistema de termostato
    de los detalles de infraestructura (lectura desde archivo, socket,
    hardware real, etc.).
    """

    @abstractmethod
    def leer_temperatura(self):
        """
        Lee la temperatura ambiente actual.

        Este metodo debe ser implementado por las clases concretas
        para obtener la temperatura desde la fuente correspondiente
        (archivo, socket, sensor fisico DHT22/DS18B20, etc.).

        Returns:
            float: Temperatura ambiente en grados Celsius (ej: 23.5).
                   Puede retornar int segun la precision del sensor.

        Raises:
            Exception: Puede lanzar excepciones especificas segun
                      la implementacion concreta (IOError, ConnectionError,
                      timeout, sensor disconnected, etc.).

        Note:
            Las implementaciones deben manejar errores de lectura
            apropiadamente y lanzar excepciones descriptivas para
            facilitar el diagnostico de problemas de hardware.
        """
