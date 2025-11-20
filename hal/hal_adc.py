"""
Interfaz abstracta para la capa HAL del ADC
Permite intercambiar implementaciones (simulada, GPIO real, mock para tests)
"""
from abc import ABC, abstractmethod


class HAL_ADC(ABC):
    """
    Abstracción del hardware de ADC (Analog-to-Digital Converter)

    Define el contrato que deben cumplir todas las implementaciones
    de HAL para lectura de valores analógicos.
    """

    @abstractmethod
    def inicializar(self) -> None:
        """
        Inicializa el hardware del ADC

        Esta operación debe llamarse antes de usar leer_adc()
        Puede configurar pines, velocidades, modos, etc.

        :raises IOError: Si hay error de inicialización
        """
        pass

    @abstractmethod
    def leer_adc(self, canal: int) -> int:
        """
        Lee el valor del ADC en el canal especificado

        :param canal: Número de canal/pin ADC a leer
        :return: Valor digital del ADC (rango depende de la implementación)
                 Por ejemplo: 0-1023 para 10 bits, 0-4095 para 12 bits
        :raises IOError: Si hay error de lectura o ADC no inicializado
        """
        pass

    @abstractmethod
    def finalizar(self) -> None:
        """
        Libera recursos del hardware

        Debe llamarse al terminar de usar el ADC para liberar recursos
        (cerrar archivos, liberar GPIO, etc.)
        """
        pass

    @abstractmethod
    def obtener_resolucion(self) -> int:
        """
        Obtiene la resolución del ADC en bits

        :return: Número de bits de resolución (ej: 10, 12, 16)
        """
        pass
