"""
Entidad Bateria - Representa la bateria que alimenta el sistema de termostato.

Este modulo define la entidad de dominio Bateria, que modela el estado
de la bateria que alimenta el dispositivo termostato. Mantiene el nivel
de carga actual y calcula automaticamente el indicador de estado
(BAJA/NORMAL) basado en un umbral configurable.

Responsabilidades:
    - Almacenar el nivel de carga actual de la bateria
    - Calcular automaticamente el indicador de estado (BAJA/NORMAL)
    - Validar parametros de configuracion (carga maxima, umbral)

Invariantes:
    - carga_maxima debe ser > 0
    - umbral_del_carga debe estar en el rango [0, 1]
    - nivel_de_carga siempre tiene un indicador correspondiente
"""


class Bateria:
    """
    Entidad que representa la bateria del sistema de termostato.

    Modela el estado de la bateria que alimenta el dispositivo,
    incluyendo su nivel de carga actual y un indicador de estado
    calculado automaticamente (BAJA/NORMAL).

    El indicador se actualiza automaticamente cada vez que se
    modifica el nivel de carga, comparando contra un umbral
    configurable.

    Attributes:
        nivel_de_carga (float): Nivel actual de carga de la bateria.
        indicador (str): Estado de la bateria ("BAJA" o "NORMAL").
    """

    @property
    def nivel_de_carga(self):
        """
        float: Nivel actual de carga de la bateria.

        Representa el nivel de carga medido en la unidad definida
        por el sistema (tipicamente voltios o porcentaje).
        """
        return self.__nivel_de_carga

    @property
    def indicador(self):
        """
        str: Indicador de estado de la bateria ("BAJA" o "NORMAL").

        Este valor se calcula automaticamente al modificar nivel_de_carga.
        - "BAJA": nivel <= carga_maxima * umbral_de_carga
        - "NORMAL": nivel > carga_maxima * umbral_de_carga
        """
        return self.__indicador

    @nivel_de_carga.setter
    def nivel_de_carga(self, valor):
        """
        Establece el nivel de carga y actualiza el indicador automaticamente.

        Args:
            valor (float): Nuevo nivel de carga de la bateria.

        Note:
            El indicador se actualiza automaticamente basado en el umbral:
            - Si valor <= carga_maxima * umbral -> indicador = "BAJA"
            - Si valor > carga_maxima * umbral -> indicador = "NORMAL"
        """
        self.__nivel_de_carga = valor
        if valor <= self.__carga_maxima * self.__umbral_de_carga:
            self.__indicador = "BAJA"
        else:
            self.__indicador = "NORMAL"

    def __init__(self, carga_maxima, umbral_del_carga):
        """
        Inicializa una nueva instancia de Bateria.

        Args:
            carga_maxima (float): Capacidad maxima de la bateria (debe ser > 0).
                                 Tipicamente en voltios o Ah.
            umbral_del_carga (float): Umbral para determinar bateria baja.
                                     Debe estar en el rango [0, 1].
                                     Ej: 0.8 = 80% de la carga maxima.

        Raises:
            ValueError: Si carga_maxima <= 0 o umbral_del_carga no esta en [0,1].
        """
        if carga_maxima <= 0:
            mensaje = "carga_maxima debe ser > 0, recibido: {}"
            raise ValueError(mensaje.format(carga_maxima))
        if not 0 <= umbral_del_carga <= 1:
            mensaje = "umbral_del_carga debe estar en [0,1], recibido: {}"
            raise ValueError(mensaje.format(umbral_del_carga))

        self.__carga_maxima = carga_maxima
        self.__umbral_de_carga = umbral_del_carga
        self.__nivel_de_carga = 0
        self.__indicador = None
