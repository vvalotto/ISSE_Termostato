"""
Entidad Ambiente - Representa el entorno fisico a climatizar.

Este modulo define la entidad de dominio Ambiente, que modela el espacio
fisico que el sistema de termostato debe controlar. Mantiene la temperatura
actual del ambiente, la temperatura objetivo deseada por el usuario, y
controla que temperatura debe mostrarse en la interfaz de usuario.

Responsabilidades:
    - Almacenar la temperatura ambiente actual (leida de sensores)
    - Mantener la temperatura deseada configurada por el usuario
    - Gestionar que temperatura mostrar en UI (ambiente o deseada)

Invariantes:
    - temperatura_a_mostrar debe ser "ambiente" o "deseada"
    - temperatura_deseada tiene valor por defecto de 22C si no se especifica
"""


class Ambiente:
    """
    Entidad que representa el ambiente a climatizar.

    Modela el espacio fisico controlado por el termostato, incluyendo
    su temperatura actual, la temperatura objetivo deseada, y la
    configuracion de que temperatura mostrar en la interfaz de usuario.

    Esta entidad es el Value Object central del dominio, encapsulando
    todo el estado necesario para las decisiones de control de clima.

    Attributes:
        temperatura_ambiente (float): Temperatura actual medida en el ambiente (C).
        temperatura_deseada (float): Temperatura objetivo configurada por usuario (C).
        temperatura_a_mostrar (str): Modo de visualizacion ("ambiente" o "deseada").
    """

    @property
    def temperatura_ambiente(self):
        """
        float: Temperatura actual del ambiente en grados Celsius.

        Este valor es leido periodicamente desde los sensores de temperatura
        y representa la medicion real del entorno fisico.
        """
        return self.__temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        """
        Establece la temperatura ambiente actual.

        Args:
            valor (float): Nueva temperatura medida del ambiente en C.
        """
        self.__temperatura_ambiente = valor

    @property
    def temperatura_deseada(self):
        """
        float: Temperatura objetivo configurada por el usuario en grados Celsius.

        Este es el setpoint que el sistema de control intentara alcanzar
        mediante el accionamiento del climatizador.
        """
        return self.__temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        """
        Establece la temperatura deseada/objetivo.

        Args:
            valor (float): Nueva temperatura objetivo en C.
        """
        self.__temperatura_deseada = valor

    @property
    def temperatura_a_mostrar(self):
        """
        str: Modo de visualizacion en la interfaz ("ambiente" o "deseada").

        Controla que temperatura se muestra en el display:
        - "ambiente": Muestra la temperatura actual medida
        - "deseada": Muestra la temperatura objetivo configurada
        """
        return self.__temperatura_a_mostrar

    @temperatura_a_mostrar.setter
    def temperatura_a_mostrar(self, valor):
        """
        Establece el modo de visualizacion de temperatura.

        Args:
            valor (str): Modo a mostrar ("ambiente" o "deseada").
        """
        self.__temperatura_a_mostrar = valor

    def __init__(self, temperatura_deseada_inicial=None):
        """
        Inicializa el ambiente.

        Args:
            temperatura_deseada_inicial: Temperatura deseada inicial en °C.
                                        Si es None, se usa 22°C por defecto.
        """
        self.__temperatura_ambiente = None  # Aún no leída del sensor
        self.__temperatura_deseada = temperatura_deseada_inicial if temperatura_deseada_inicial is not None else 22
        self.__temperatura_a_mostrar = "ambiente"

    def __repr__(self):
        """
        Retorna una representacion en string del Ambiente.

        Returns:
            str: Representacion legible del estado del ambiente en formato:
                 "Ambiente(temperatura_ambiente=X, temperatura_deseada=Y, ...)"

        Note:
            Util para debugging y logging. Muestra todos los atributos
            relevantes del estado actual del ambiente.
        """
        return (
            "Ambiente(temperatura_ambiente={}, "
            "temperatura_deseada={}, "
            "temperatura_a_mostrar='{}')".format(
                self.__temperatura_ambiente,
                self.__temperatura_deseada,
                self.__temperatura_a_mostrar
            )
        )