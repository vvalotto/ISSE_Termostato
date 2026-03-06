"""
Interfaz abstracta para dispositivos de climatizacion.

Patron de Diseno:
    - Template Method: evaluar_accion() define el flujo comun,
      _definir_accion() es el hook method para variaciones.
"""
from abc import ABCMeta, abstractmethod
from servicios_dominio.controlador_climatizador import ControladorTemperatura


class AbsClimatizador(metaclass=ABCMeta):
    """
    Clase abstracta base para dispositivos de climatizacion.

    Generaliza el comportamiento comun de todos los dispositivos que
    modifican la temperatura del ambiente (climatizadores, calefactores, etc.).

    Implementa una maquina de estados finitos para gestionar transiciones
    validas entre estados (apagado, calentando, enfriando) y aplica el
    patron Template Method para definir el flujo de evaluacion de acciones.

    Attributes:
        estado (str): Estado actual del dispositivo.
                     Valores: "apagado", "calentando", "enfriando".

    Design Patterns:
        - Template Method: evaluar_accion() es el template method.
        - State Machine: Transiciones gestionadas via diccionario.

    Note:
        Las subclases deben implementar:
        - _inicializar_maquina_estado(): Define transiciones validas
        - _definir_accion(): Logica especifica para determinar accion
    """

    @property
    def estado(self):
        """str: Estado actual del climatizador (apagado/calentando/enfriando)."""
        return self._estado

    def __init__(self, histeresis=2):
        """
        Inicializa el climatizador en estado apagado.

        Args:
            histeresis (float): Margen de tolerancia en grados para la
                               comparacion de temperatura. Por defecto 2.
        """
        self._estado = "apagado"
        self._histeresis = histeresis
        self._transiciones = {}
        self._inicializar_maquina_estado()

    def proximo_estado(self, accion):
        """
        Ejecuta una transicion de estado basada en la accion dada.

        Args:
            accion (str): Accion a ejecutar ("calentar", "enfriar", "apagar").

        Returns:
            str: Nuevo estado del climatizador despues de la transicion.

        Raises:
            ValueError: Si la transicion (estado_actual, accion) no es valida.
        """
        clave = (self._estado, accion)
        if clave not in self._transiciones:
            mensaje = "Transicion no valida: estado={}, accion={}"
            raise ValueError(mensaje.format(self._estado, accion))
        self._estado = self._transiciones[clave]
        return self._estado

    @abstractmethod
    def _inicializar_maquina_estado(self):
        """
        Inicializa el diccionario de transiciones de estado.

        El diccionario debe tener la estructura:
            {(estado_origen, accion): estado_destino}
        """

    def evaluar_accion(self, ambiente):
        """
        Evalua que accion tomar basada en el estado del ambiente (Template Method).

        Args:
            ambiente (Ambiente): Estado actual del ambiente con temperaturas.

        Returns:
            str: Accion a ejecutar ("calentar", "enfriar", "apagar", None).
        """
        temperatura = ControladorTemperatura.comparar_temperatura(
            ambiente.temperatura_ambiente,
            ambiente.temperatura_deseada,
            self._histeresis
        )
        return self._definir_accion(temperatura)

    @abstractmethod
    def _definir_accion(self, temperatura):
        """
        Define la accion basada en la comparacion de temperatura (Hook Method).

        Args:
            temperatura (str): Resultado de comparacion ("alta", "baja", "normal").

        Returns:
            str: Accion a ejecutar ("calentar", "enfriar", "apagar", None).
        """
