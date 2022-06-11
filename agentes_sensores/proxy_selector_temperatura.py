"""
Clase que simula la lectura de un boton de seleccion
"""
from registrador.registrador import *
import datetime


class SelectorTemperatura:

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = archivo.read()
            archivo.close()
        except IOError:
            mensaje_error = "Error al leer el tipo de temperatura"
            Registrador.registrar_error(SelectorTemperatura.__name__,
                                        SelectorTemperatura.obtener_selector.__name__,
                                        str(datetime.datetime.now()),
                                        str(IOError),
                                        mensaje_error)
            raise mensaje_error
        return tipo_temperatura
