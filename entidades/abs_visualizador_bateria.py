"""
Interfaz abstracta para visualizadores de bateria (Patron Presenter/View).

Este modulo define el contrato que deben cumplir todas las implementaciones
de visualizadores de estado de bateria. Separa la logica de presentacion
de datos de bateria de la logica de dominio, siguiendo el patron de diseno
Presenter/View.

Responsabilidades:
    - Definir interfaz para mostrar tension/nivel de carga de bateria
    - Definir interfaz para mostrar indicador de estado (BAJA/NORMAL)
    - Garantizar separacion entre dominio y capa de presentacion

Patron de Diseno:
    - Presenter/View: Separa logica de presentacion de logica de dominio
    - Interface Segregation: Define contrato especifico para visualizacion de bateria

Implementaciones tipicas:
    - Visualizador LCD/Display fisico
    - Visualizador en consola para debugging
    - Visualizador web/GUI
"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorBateria(metaclass=ABCMeta):
    """
    Interfaz abstracta para visualizadores de estado de bateria.

    Define los metodos que deben implementar todos los visualizadores
    que muestran informacion sobre el estado de la bateria del sistema.
    Permite desacoplar la capa de presentacion de la logica de dominio.

    Methods:
        mostrar_tension: Visualiza el nivel de carga actual de la bateria
        mostrar_indicador: Visualiza el indicador de estado (BAJA/NORMAL)

    Note:
        Los metodos son @staticmethod porque los visualizadores tipicamente
        no mantienen estado propio, solo presentan datos que reciben.
    """

    @staticmethod
    @abstractmethod
    def mostrar_tension(tension_bateria):
        """
        Muestra el nivel de carga actual de la bateria.

        Args:
            tension_bateria (float): Nivel de carga de la bateria a mostrar.
                                    Tipicamente en voltios o porcentaje.

        Note:
            Las implementaciones concretas deben definir como presentar
            este valor (display LCD, consola, interfaz grafica, etc.).
        """
        pass

    @staticmethod
    @abstractmethod
    def mostrar_indicador(indicador_bateria):
        """
        Muestra el indicador de estado de la bateria (BAJA/NORMAL).

        Args:
            indicador_bateria (str): Estado de la bateria a mostrar.
                                    Valores esperados: "BAJA", "NORMAL".

        Note:
            Las implementaciones concretas deben definir como presentar
            este indicador (LED, icono, texto, color, etc.).
        """
        pass
