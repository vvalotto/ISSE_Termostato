"""
Interfaz abstracta para proxies de bateria (Patron Proxy).

Este modulo define el contrato que deben cumplir todos los proxies
que actuan como intermediarios para leer el nivel de carga de la bateria.
El patron Proxy permite simular hardware fisico mediante diferentes
implementaciones (archivo, socket, sensores reales, etc.).

Ejemplo de uso:
    Las implementaciones concretas pueden leer la carga desde:
    - Archivos locales (para simulacion)
    - Sockets de red (para sensores remotos)
    - Hardware real (para produccion)
"""

from abc import ABCMeta, abstractmethod


class AbsProxyBateria(metaclass=ABCMeta):
    """
    Interfaz abstracta para proxies de lectura de bateria.

    Define el contrato que deben implementar todos los proxies
    que actuan como intermediarios para obtener el nivel de carga
    de la bateria del sistema.

    Patron de diseno: Proxy
    Permite separar la logica de dominio de los detalles de
    infraestructura (lectura desde archivo, socket, hardware, etc.).
    """

    @abstractmethod
    def leer_carga(self):
        """
        Lee el nivel de carga actual de la bateria.

        Este metodo debe ser implementado por las clases concretas
        para obtener el nivel de carga desde la fuente correspondiente
        (archivo, socket, sensor fisico, etc.).

        Returns:
            float: Nivel de carga de la bateria (ej: 4.5 voltios).
                   Retorna None si hay error en la lectura.

        Raises:
            Exception: Puede lanzar excepciones especificas segun
                      la implementacion concreta (IOError, ConnectionError, etc.).
        """
        pass
