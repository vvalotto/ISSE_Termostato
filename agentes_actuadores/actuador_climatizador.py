"""
Clase que simula el accionamiento del climatizador.
Aqui la accion es escribir en un archivo externo.
"""
import datetime

from registrador.registrador import AbsRegistrador, AbsAuditor
from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador


class ActuadorClimatizadorGeneral(AbsProxyActuadorClimatizador, AbsRegistrador, AbsAuditor):
    """
    Actuador que controla el climatizador mediante escritura en archivo.

    Implementa las interfaces AbsProxyActuadorClimatizador, AbsRegistrador
    y AbsAuditor para accionar el climatizador y registrar eventos.

    Patron de Diseno:
        - Proxy: Representa el actuador real del climatizador
        - Observer: Registra eventos de auditoria y errores
    """

    def accionar_climatizador(self, accion):
        """
        Acciona el climatizador escribiendo la accion en archivo.

        Args:
            accion: Accion a ejecutar en el climatizador (str).
        """
        # Simula Actuador
        mensaje_accion = "accionando el climatizador"
        ActuadorClimatizadorGeneral.auditar_funcion(ActuadorClimatizadorGeneral.__name__,
                                                    mensaje_accion,
                                                    str(datetime.datetime.now()))
        try:
            with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
                archivo_climatizador.write(accion)
        except IOError:
            mensaje_error = "Error al quierer actuar en el climatizador"
            registro_error = ActuadorClimatizadorGeneral._armar_registro_error(
                str(datetime.datetime.now()),
                str(IOError),
                mensaje_error)

            ActuadorClimatizadorGeneral.registrar_error(registro_error)

    @staticmethod
    def _armar_registro_error(fecha_hora, tipo_de_error, mensaje):
        """
        Arma el registro de error con formato estandar.

        Args:
            fecha_hora: Timestamp del error.
            tipo_de_error: Tipo de excepcion ocurrida.
            mensaje: Descripcion del error.

        Returns:
            str: Registro formateado listo para persistir.
        """
        registro = ""
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "tipo_de_error: " + tipo_de_error + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "-------------------------" + "\n" + "\n" + "\n"
        return registro

    @staticmethod
    def registrar_error(registro):
        """
        Persiste el registro de error en archivo.

        Args:
            registro: Texto del registro a persistir.

        Raises:
            IOError: Si no se puede escribir el archivo de errores.
        """
        try:
            with open("registro_errores", "a", encoding="utf-8") as archivo_errores:
                archivo_errores.write(registro)
        except IOError as exc:
            raise IOError("Error al escribir el archivo de errores") from exc

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        """
        Registra una entrada de auditoria en archivo.

        Args:
            clase: Nombre de la clase que genera el evento.
            mensaje: Descripcion del evento auditado.
            fecha_hora: Timestamp del evento.

        Raises:
            IOError: Si no se puede escribir el archivo de auditoria.
        """
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "*************" + "\n" + "\n" + "\n"

        try:
            with open("registro_auditoria", "a", encoding="utf-8") as archivo_auditoria:
                archivo_auditoria.write(registro)
        except IOError as exc:
            raise IOError("Error al escribir el archivo de auditoria") from exc
