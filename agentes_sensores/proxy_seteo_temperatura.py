"""
Clase que simula el cambio de la temperatura deseada
"""
import socket
from  servicios_aplicacion.abs_seteo_temperatura import *


class SeteoTemperatura(AbsSeteoTemperatura):

    @staticmethod
    def obtener_seteo():
        opcion = "0"
        while opcion not in ["1", "2"]:
            opcion = input(">")
        diferencia = "aumentar" if opcion == "1" else "disminuir"
        return diferencia


class SeteoTemperaturaSocket(AbsSeteoTemperatura):

    @staticmethod
    def obtener_seteo():

        diferencia = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = ('localhost', 14000)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, direccion_cliente = servidor.accept()

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                diferencia = str(datos.decode("utf-8"))
        except ConnectionError("Error"):
            conexion.close()
            print("FIN")

        return diferencia
