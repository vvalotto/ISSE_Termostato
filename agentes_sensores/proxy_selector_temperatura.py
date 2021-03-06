"""
Clase que simula la lectura de un boton de seleccion
"""

from registrador.registrador import *
from servicios_aplicacion.abs_selector_temperatura import *
import datetime


class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = str(archivo.read())
            archivo.close()
        except IOError:
            mensaje_error = "Error al leer el tipo de temperatura"
            registro_error = SelectorTemperaturaArchivo._armar_registro_error(
                                                        SelectorTemperaturaArchivo.__name__,
                                                        SelectorTemperaturaArchivo.obtener_selector.__name__,
                                                        str(datetime.datetime.now()),
                                                        str(IOError),
                                                        mensaje_error)

            SelectorTemperaturaArchivo.registrar_error(registro_error)
            raise mensaje_error
        return tipo_temperatura

    @staticmethod
    def _armar_registro_error(clase, metodo, fecha_hora, tipo_de_error, mensaje):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "metodo: " + metodo + "\n"
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
