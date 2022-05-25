"""
Clase que llamaria a la lectura de la interfaz de lectura
del sensor de temperatura
"""


class ProxySensorTemperatura:

    @staticmethod
    def leer_temperatura():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        """
        try:
            archivo = open("temperatura", "r")
            temperatura = int(archivo.read())
            archivo.close()
        except IOError:
            raise Exception("Error de Lectura de Sensor")
        return temperatura
