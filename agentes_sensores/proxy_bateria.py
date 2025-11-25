"""
Tercera version: refactorizacion:
Se crea un clase abstracta y se derivan sus implementaciones
con las clases concretas que se corresponden
"""
import socket
from entidades.abs_bateria import *


class ProxyBateriaArchivo(AbsProxyBateria):

    def leer_carga(self):

        try:
            archivo = open("bateria", "r")
            carga = float(archivo.read())
            archivo.close()
        except IOError:
            carga = None
        return carga


class ProxyBateriaSocket(AbsProxyBateria):

    def leer_carga(self):
        from configurador.configurador import Configurador

        carga = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("bateria")
        direccion_servidor = (host, puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, direccion_cliente = servidor.accept()

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                carga = float(datos.decode("utf-8"))
        except ConnectionError as e:  # FIX: sintaxis correcta
            print("Error de conexión: {}".format(e))
        finally:  # FIX: asegurar cierre
            conexion.close()
            servidor.close()

        return carga
