"""
Primera version: simula una lectura
"""


class ProxyBateria:

    @staticmethod
    def leer_carga():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        :return:
        """
        archivo = open("bateria", "r")
        carga = float(archivo.read())
        archivo.close()
        return carga
