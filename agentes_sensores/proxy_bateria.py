"""
Proxies para lectura del sensor de bateria.

Este modulo contiene las implementaciones concretas del proxy de bateria,
permitiendo leer el nivel de carga desde archivo o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el sensor de bateria real/remoto
"""
import socket
from entidades.abs_bateria import AbsProxyBateria


# pylint: disable=too-few-public-methods
class ProxyBateriaArchivo(AbsProxyBateria):
    """
    Proxy para lectura de bateria desde archivo.

    Implementa la interfaz AbsProxyBateria leyendo el nivel de carga
    desde un archivo local llamado 'bateria'.
    """

    def leer_carga(self):
        """Lee el nivel de carga desde el archivo 'bateria'."""
        try:
            with open("bateria", "r", encoding="utf-8") as archivo:
                carga = float(archivo.read())
        except IOError:
            carga = None
        return carga


# pylint: disable=too-few-public-methods
class ProxyBateriaSocket(AbsProxyBateria):
    """
    Proxy para lectura de bateria via socket TCP.

    Implementa la interfaz AbsProxyBateria escuchando conexiones
    TCP para recibir el nivel de carga de un cliente remoto.
    """

    def leer_carga(self):
        """Lee el nivel de carga via socket TCP."""
        # pylint: disable=import-outside-toplevel
        from configurador.configurador import Configurador

        carga = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("bateria")
        direccion_servidor = (host, puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        conexion, _ = servidor.accept()

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
