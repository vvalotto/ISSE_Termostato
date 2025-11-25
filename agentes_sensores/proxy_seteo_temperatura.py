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

    def __init__(self):
        """Inicializa el socket persistente"""
        from configurador.configurador import Configurador

        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("seteo_temperatura")
        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        self._servidor.listen(1)

        self._conexion = None
        self._servidor.settimeout(2.0)  # Timeout para accept

    def obtener_seteo(self):
        """
        Espera comando de seteo (aumentar/disminuir).
        Mantiene socket abierto para recibir múltiples comandos.
        """
        diferencia = None

        try:
            # Si no hay conexión activa, aceptar una (con timeout)
            if self._conexion is None:
                try:
                    self._conexion, direccion_cliente = self._servidor.accept()
                    self._conexion.settimeout(5.0)  # Timeout para recv
                    print(f"[Seteo] Cliente conectado: {direccion_cliente}")
                except socket.timeout:
                    # No hay cliente, retornar None
                    return None

            # Leer comando (bloqueante con timeout)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    diferencia = str(datos.decode("utf-8"))
                    print(f"[Seteo] Comando recibido: {diferencia}")
                else:
                    # Cliente cerró conexión
                    print("[Seteo] Cliente desconectado")
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # Timeout esperando comando, retornar None
                return None
            except ConnectionError as e:
                print(f"[Seteo] Error de conexión: {e}")
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except Exception as e:
            print(f"[Seteo] Error: {e}")

        return diferencia

    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self._conexion:
            self._conexion.close()
        if self._servidor:
            self._servidor.close()
