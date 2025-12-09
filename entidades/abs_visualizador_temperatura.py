"""
Interfaz abstracta para visualizadores de temperatura (Patron Presenter/View).

Este modulo define el contrato que deben cumplir todas las implementaciones
de visualizadores de temperatura del sistema de termostato. Separa la logica
de presentacion de datos de temperatura de la logica de dominio, siguiendo
el patron de diseno Presenter/View.

Responsabilidades:
    - Definir interfaz para mostrar temperatura ambiente (actual)
    - Definir interfaz para mostrar temperatura deseada (setpoint)
    - Garantizar separacion entre dominio y capa de presentacion

Patron de Diseno:
    - Presenter/View: Separa logica de presentacion de logica de dominio
    - Interface Segregation: Define contrato especifico para visualizacion de temperatura

Implementaciones tipicas:
    - Visualizador LCD/Display fisico con 7 segmentos
    - Visualizador en consola para debugging y testing
    - Visualizador web/GUI para interfaces remotas
"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorTemperatura(metaclass=ABCMeta):
    """
    Interfaz abstracta para visualizadores de temperatura.

    Define los metodos que deben implementar todos los visualizadores
    que muestran informacion de temperaturas del sistema (ambiente y deseada).
    Permite desacoplar la capa de presentacion de la logica de dominio.

    Methods:
        mostrar_temperatura_ambiente: Visualiza la temperatura actual medida
        mostrar_temperatura_deseada: Visualiza la temperatura objetivo configurada

    Note:
        Los metodos pueden ser de instancia para permitir que implementaciones
        mantengan estado (ej: URLs de API, conexiones socket).
    """

    @abstractmethod
    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        """
        Muestra la temperatura ambiente actual.

        Args:
            temperatura_ambiente (float): Temperatura actual del ambiente en grados Celsius.
                                         Valor leido desde los sensores de temperatura.

        Note:
            Las implementaciones concretas deben definir como presentar
            este valor (display LCD, consola, interfaz grafica, etc.).
            Tipicamente se muestra con precision de 1 decimal.
        """

    @abstractmethod
    def mostrar_temperatura_deseada(self, temperatura_deseada):
        """
        Muestra la temperatura deseada (setpoint).

        Args:
            temperatura_deseada (float): Temperatura objetivo configurada por el usuario
                                        en grados Celsius.

        Note:
            Las implementaciones concretas deben definir como presentar
            este valor (display LCD, consola, interfaz grafica, etc.).
            Tipicamente se distingue visualmente de la temperatura ambiente
            (diferente linea, color, o indicador).
        """
