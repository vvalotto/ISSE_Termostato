"""
Clases abstractas para registro de auditoria y excepciones.

Este modulo define las interfaces base para el sistema de registro,
permitiendo implementaciones concretas para logging de errores y
auditoria de funciones.

Patron de Diseno:
    - Template Method: Define la interfaz que las subclases deben implementar
"""
from abc import abstractmethod


# pylint: disable=too-few-public-methods
class AbsRegistrador:
    """
    Clase abstracta para registro de errores.

    Define la interfaz que deben implementar las clases concretas
    de registro de errores del sistema.
    """

    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        """
        Registra un error en el sistema de logging.

        Args:
            registro (str): Mensaje de error formateado para registrar.

        Note:
            Las implementaciones concretas deben definir el destino
            del registro (archivo, consola, base de datos, etc.).
        """


# pylint: disable=too-few-public-methods
class AbsAuditor:
    """
    Clase abstracta para auditoria de funciones.

    Define la interfaz que deben implementar las clases concretas
    de auditoria del sistema.
    """

    @staticmethod
    @abstractmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        """
        Registra una entrada de auditoria para una funcion.

        Args:
            clase (str): Nombre de la clase que genera el evento.
            mensaje (str): Descripcion del evento auditado.
            fecha_hora (str): Timestamp del evento.

        Note:
            Las implementaciones concretas deben definir el formato
            y destino de los registros de auditoria.
        """
