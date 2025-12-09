"""
Interfaz abstracta para proxies de actuador de climatizador (Patron Proxy).

Este modulo define el contrato que deben cumplir todos los proxies
que se encargan de accionar fisicamente el sistema de climatizacion
(calefaccion, aire acondicionado, ventilacion, etc.).

El patron Proxy permite simular hardware fisico mediante diferentes
implementaciones y facilita el testing sin hardware real.

Ejemplo de uso:
    Las implementaciones concretas pueden accionar el climatizador mediante:
    - Escritura en archivos (para simulacion y testing)
    - GPIO/Relays (para control de hardware real en Raspberry Pi)
    - Protocolos de automatizacion (MQTT, Modbus, etc.)
"""

from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class AbsProxyActuadorClimatizador(metaclass=ABCMeta):
    """
    Interfaz abstracta para proxies de actuador de climatizador.

    Define el contrato que deben implementar todos los proxies
    que se encargan de accionar fisicamente el sistema de climatizacion.

    Patron de diseno: Proxy
    Permite separar la logica de control de la climatizacion de los
    detalles de hardware (GPIO, relays, protocolos de comunicacion, etc.).

    Design Decision:
        Esta interfaz usa metodos de instancia (no @staticmethod) para
        permitir que las implementaciones mantengan estado si lo necesitan
        (ej: conexiones GPIO, contadores de acciones, configuracion, cache).
    """

    @abstractmethod
    def accionar_climatizador(self, accion):
        """
        Acciona el sistema de climatizacion segun la accion especificada.

        Este metodo debe ser implementado por las clases concretas
        para ejecutar la accion de control sobre el hardware real
        o simulado del climatizador.

        Args:
            accion (str): Accion a ejecutar sobre el climatizador.
                         Valores validos: "calentar", "enfriar", "apagar"

        Returns:
            None: Este metodo no retorna valor. Los errores se comunican
                  via excepciones o logging/auditoria.

        Raises:
            IOError: Si hay error al escribir comandos al actuador fisico.
            ConnectionError: Si el actuador remoto no esta disponible.
            ValueError: Si la accion especificada no es valida.

        Note:
            Las implementaciones deben incluir logging/auditoria para
            trazabilidad de las acciones ejecutadas sobre el hardware.
            Como metodo de instancia, puede acceder al estado del objeto
            (self) para mantener configuracion, contadores, etc.
        """


# Alias para compatibilidad con codigo existente
# DEPRECADO: Usar AbsProxyActuadorClimatizador en su lugar
AbsActuadorClimatizador = AbsProxyActuadorClimatizador
