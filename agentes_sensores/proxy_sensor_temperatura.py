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
        from configurador.configurador import Configurador

        temperatura = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("temperatura")
        direccion_servidor = (host, puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, direccion_cliente = servidor.accept()

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                temperatura = float(datos.decode("utf-8"))
        except ConnectionError as e:  # FIX: sintaxis correcta
            print("Error de conexión: {}".format(e))
        finally:  # FIX: asegurar cierre
            conexion.close()
            servidor.close()

        return temperatura
