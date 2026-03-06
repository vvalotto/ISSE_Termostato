"""
Clase que simula el accionamiento del climatizador.
Aqui la accion es escribir en un archivo externo.

Patron de Diseno:
    - Proxy: Representa el actuador real del climatizador
    - DIP: Recibe registrador y auditor como dependencias inyectadas
"""
import datetime

from entidades.abs_actuador_climatizador import AbsProxyActuadorClimatizador


class ActuadorClimatizadorGeneral(AbsProxyActuadorClimatizador):
    """
    Actuador que controla el climatizador mediante escritura en archivo.

    Recibe un registrador y un auditor por inyeccion de dependencias,
    eliminando la herencia multiple de AbsRegistrador y AbsAuditor.
    Esto cumple SRP (una sola razon de cambio: la logica de actuacion)
    e ISP (no implementa interfaces de responsabilidades ortogonales).

    Args:
        registrador (AbsRegistrador): Servicio para registro de errores.
        auditor (AbsAuditor): Servicio para auditoria de eventos.
    """

    def __init__(self, registrador, auditor):
        """
        Inicializa el actuador con sus dependencias de logging.

        Args:
            registrador (AbsRegistrador): Implementacion de registro de errores.
            auditor (AbsAuditor): Implementacion de auditoria de eventos.
        """
        self._registrador = registrador
        self._auditor = auditor

    def accionar_climatizador(self, accion):
        """
        Acciona el climatizador escribiendo la accion en archivo.

        Args:
            accion: Accion a ejecutar en el climatizador (str).
        """
        mensaje_accion = "accionando el climatizador"
        self._auditor.auditar_funcion(self.__class__.__name__,
                                      mensaje_accion,
                                      str(datetime.datetime.now()))
        try:
            with open("climatizador", "w", encoding="utf-8") as archivo_climatizador:
                archivo_climatizador.write(accion)
        except IOError:
            mensaje_error = "Error al quierer actuar en el climatizador"
            registro_error = self._armar_registro_error(
                str(datetime.datetime.now()),
                str(IOError),
                mensaje_error)
            self._registrador.registrar_error(registro_error)

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
