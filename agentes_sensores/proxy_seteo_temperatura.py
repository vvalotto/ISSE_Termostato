"""
Componentes para seteo de temperatura deseada.

Este modulo contiene las implementaciones para obtener comandos
de ajuste de temperatura (aumentar/disminuir) desde consola
o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el control de seteo real/remoto
"""
import socket
from servicios_aplicacion.abs_seteo_temperatura import AbsSeteoTemperatura


# pylint: disable=too-few-public-methods
class SeteoTemperatura(AbsSeteoTemperatura):
    """
    Seteo de temperatura desde consola.

    Solicita al usuario via input() el comando de ajuste
    de temperatura: '1' para aumentar, '2' para disminuir.
    """

    @staticmethod
    def obtener_seteo():
        opcion = "0"
        while opcion not in ["1", "2"]:
            opcion = input(">")
        diferencia = "aumentar" if opcion == "1" else "disminuir"
        return diferencia


class SeteoTemperaturaSocket(AbsSeteoTemperatura):
    """
    Seteo de temperatura via socket TCP.

    Escucha conexiones TCP para recibir comandos de ajuste
    de temperatura ('aumentar' o 'disminuir').
    """

    def __init__(self):
        """Inicializa el socket persistente."""
        # pylint: disable=import-outside-toplevel
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
                    print("[Seteo] Cliente conectado: {}".format(direccion_cliente))
                except socket.timeout:
                    # No hay cliente, retornar None
                    return None

            # Leer comando (bloqueante con timeout)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    diferencia = str(datos.decode("utf-8"))
                    print("[Seteo] Comando recibido: {}".format(diferencia))
                else:
                    # Cliente cerró conexión
                    print("[Seteo] Cliente desconectado")
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # Timeout esperando comando, retornar None
                return None
            except ConnectionError as e:
                print("[Seteo] Error de conexión: {}".format(e))
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except (socket.error, OSError) as e:
            print("[Seteo] Error: {}".format(e))

        return diferencia

    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self._conexion:
            self._conexion.close()
        if self._servidor:
            self._servidor.close()
