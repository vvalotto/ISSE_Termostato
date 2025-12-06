"""
Interfaz abstracta para visualizadores de climatizador (Patron Presenter/View).

Este modulo define el contrato que deben cumplir todas las implementaciones
de visualizadores de estado del climatizador. Separa la logica de presentacion
del estado operacional del climatizador de la logica de dominio, siguiendo
el patron de diseno Presenter/View.

Responsabilidades:
    - Definir interfaz para mostrar estado operacional del climatizador
    - Garantizar separacion entre dominio y capa de presentacion
    - Permitir multiples implementaciones de visualizacion

Patron de Diseno:
    - Presenter/View: Separa logica de presentacion de logica de dominio
    - Interface Segregation: Define contrato especifico para visualizacion de climatizador

Estados tipicos del climatizador:
    - "apagado": Sistema sin accionar
    - "calentando": Modo calefaccion activo
    - "enfriando": Modo refrigeracion activo (solo en Climatizador completo)

Implementaciones tipicas:
    - Visualizador LCD/Display con iconos de llama/copo de nieve
    - Visualizador LED (rojo=calentando, azul=enfriando, apagado=off)
    - Visualizador en consola para debugging
    - Visualizador web/GUI con animaciones
"""

from abc import ABCMeta, abstractmethod


class AbsVisualizadorClimatizador(metaclass=ABCMeta):
    """
    Interfaz abstracta para visualizadores de estado del climatizador.

    Define el metodo que deben implementar todos los visualizadores
    que muestran el estado operacional del sistema de climatizacion.
    Permite desacoplar la capa de presentacion de la logica de dominio.

    Methods:
        mostrar_estado_climatizador: Visualiza el estado actual del climatizador

    Note:
        El metodo es @staticmethod porque los visualizadores tipicamente
        no mantienen estado propio, solo presentan datos que reciben.
    """

    @staticmethod
    @abstractmethod
    def mostrar_estado_climatizador(estado_climatizador):
        """
        Muestra el estado operacional actual del climatizador.

        Args:
            estado_climatizador (str): Estado actual del sistema de climatizacion.
                                      Valores esperados:
                                      - "apagado": Sistema sin accionar
                                      - "calentando": Modo calefaccion activo
                                      - "enfriando": Modo refrigeracion activo

        Note:
            Las implementaciones concretas deben definir como presentar
            cada estado de forma clara y distinguible (iconos, colores,
            texto, LEDs, etc.).
        """
        pass
