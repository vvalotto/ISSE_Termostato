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
        from configurador.configurador import Configurador

        diferencia = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("seteo_temperatura")
        direccion_servidor = (host, puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, direccion_cliente = servidor.accept()

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                diferencia = str(datos.decode("utf-8"))
        except ConnectionError as e:  # FIX: sintaxis correcta
            print(f"Error de conexión: {e}")
        finally:  # FIX: asegurar cierre
            conexion.close()
            servidor.close()

        return diferencia
