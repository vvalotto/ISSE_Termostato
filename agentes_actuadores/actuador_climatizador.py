"""
Clase que simula el accionamiento del climatizador.
Aqui la acción es escribir en un archivo externo
"""

from registrador.registrador import *
import datetime


class ActuadorClimatizador(AbsRegistrador, AbsAuditor):

    @staticmethod
    def accionar_climatizador(accion):

        # Simula Actuador
        mensaje_accion = "accionando el climatizador"
        ActuadorClimatizador.auditar_funcion(ActuadorClimatizador.__name__,
                                             mensaje_accion,
                                             str(datetime.datetime.now()))
        try:
            with open("climatizador", "w") as archivo_climatizador:
                archivo_climatizador.write(accion)
                archivo_climatizador.close()
        except IOError:
            mensaje_error = "Error al quierer actuar en el climatizador"
            registro_error = ActuadorClimatizador._armar_registro_error(
                str(datetime.datetime.now()),
                str(IOError),
                mensaje_error)

            ActuadorClimatizador.registrar_error(registro_error)

    @staticmethod
    def _armar_registro_error(fecha_hora, tipo_de_error, mensaje):
        registro = ""
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "tipo_de_error: " + tipo_de_error + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "-------------------------" + "\n" + "\n" + "\n"
        return registro

    @staticmethod
    def registrar_error(registro):
        try:
            with open("registro_errores", "a") as archivo_errores:
                archivo_errores.write(registro)
                archivo_errores.close()
        except IOError:
            raise "Error al escribir el archivo de errores: " + str(IOError.errno)

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "*************" + "\n" + "\n" + "\n"

        try:
            with open("registro_auditoria", "a") as archivo_auditoria:
                archivo_auditoria.write(registro)
                archivo_auditoria.close()
        except IOError:
            raise "Error al escribir el archivo de auditoria: " + str(IOError.errno)
