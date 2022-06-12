"""
Clase abstracta sensor de temperatura
"""

import socket
from entidades.abs_sensor_temperatura import *


class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):

    def leer_temperatura(self):
        try:
            archivo = open("temperatura", "r")
            temperatura = int(archivo.read())
            archivo.close()
        except IOError:
            raise Exception("Error de Lectura de Sensor")
        return temperatura


class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):

    def leer_temperatura(self):

        temperatura = None

        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = ('localhost', 12000)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, direccion_cliente = servidor.accept()

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                temperatura = float(datos.decode("utf-8"))
        except ConnectionError("Error en la lectura de la carga"):
            conexion.close()
            print("FIN")

        return temperatura
