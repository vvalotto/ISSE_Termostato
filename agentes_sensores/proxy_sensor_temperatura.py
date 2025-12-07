"""
Proxies para lectura del sensor de temperatura.

Este modulo contiene las implementaciones concretas del proxy de temperatura,
permitiendo leer la temperatura ambiente desde archivo o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el sensor de temperatura real/remoto
"""
import socket
from entidades.abs_sensor_temperatura import AbsProxySensorTemperatura


# pylint: disable=too-few-public-methods
class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):
    """
    Proxy para lectura de temperatura desde archivo.

    Implementa la interfaz AbsProxySensorTemperatura leyendo la temperatura
    desde un archivo local llamado 'temperatura'.
    """

    def leer_temperatura(self):
        """Lee la temperatura desde el archivo 'temperatura'."""
        try:
            with open("temperatura", "r", encoding="utf-8") as archivo:
                temperatura = int(archivo.read())
        except IOError as exc:
            raise IOError("Error de Lectura de Sensor") from exc
        return temperatura


# pylint: disable=too-few-public-methods
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):
    """
    Proxy para lectura de temperatura via socket TCP.

    Implementa la interfaz AbsProxySensorTemperatura escuchando conexiones
    TCP para recibir la temperatura de un cliente remoto.
    """

    def leer_temperatura(self):
        """Lee la temperatura via socket TCP."""
        # pylint: disable=import-outside-toplevel
        from configurador.configurador import Configurador

        temperatura = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("temperatura")
        direccion_servidor = (host, puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, _ = servidor.accept()

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
