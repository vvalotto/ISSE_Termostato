"""
Interfaces y clases concretas para registro de auditoria y excepciones.

Este modulo define las interfaces base para el sistema de registro
y sus implementaciones concretas de archivo.

Patron de Diseno:
    - Strategy: Las implementaciones concretas son intercambiables
    - DIP: Los consumidores dependen de las interfaces, no de las concretas
"""
from abc import abstractmethod


# pylint: disable=too-few-public-methods
class AbsRegistrador:
    """
    Interfaz abstracta para registro de errores.

    Define el contrato que deben cumplir las implementaciones
    concretas de registro de errores del sistema.
    """

    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        """
        Registra un error en el sistema de logging.

        Args:
            registro (str): Mensaje de error formateado para registrar.
        """


# pylint: disable=too-few-public-methods
class AbsAuditor:
    """
    Interfaz abstracta para auditoria de funciones.

    Define el contrato que deben cumplir las implementaciones
    concretas de auditoria del sistema.
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
        """


class RegistradorArchivo(AbsRegistrador):
    """
    Registrador concreto que persiste errores en archivo.

    Escribe los registros de error en el archivo 'registro_errores'.
    """

    @staticmethod
    def registrar_error(registro):
        """
        Persiste el registro de error en el archivo 'registro_errores'.

        Args:
            registro (str): Texto del registro a persistir.

        Raises:
            IOError: Si no se puede escribir el archivo.
        """
        try:
            with open("registro_errores", "a", encoding="utf-8") as archivo:
                archivo.write(registro)
        except IOError as exc:
            raise IOError("Error al escribir el archivo de errores") from exc


class AuditorArchivo(AbsAuditor):
    """
    Auditor concreto que persiste eventos de auditoria en archivo.

    Escribe los registros de auditoria en el archivo 'registro_auditoria'.
    """

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        """
        Persiste el evento de auditoria en el archivo 'registro_auditoria'.

        Args:
            clase (str): Nombre de la clase que genera el evento.
            mensaje (str): Descripcion del evento auditado.
            fecha_hora (str): Timestamp del evento.

        Raises:
            IOError: Si no se puede escribir el archivo.
        """
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "*************" + "\n" + "\n" + "\n"
        try:
            with open("registro_auditoria", "a", encoding="utf-8") as archivo:
                archivo.write(registro)
        except IOError as exc:
            raise IOError("Error al escribir el archivo de auditoria") from exc
