"""
Clase que simula la lectura de un boton de seleccion
"""


class SelectorTemperatura:

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = archivo.read()
            archivo.close()
        except IOError:
            raise "Error al leer el tipo de temperatura"
        return tipo_temperatura
