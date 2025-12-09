"""
Selectores de modo de temperatura.

Este modulo contiene las implementaciones para seleccionar el modo
de visualizacion de temperatura (ambiente o deseada), desde archivo
o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el boton de seleccion real/remoto
"""
# pylint: disable=duplicate-code
# El codigo de socket y registro es similar entre proxies (patron comun aceptable)

import datetime
import socket

from registrador.registrador import AbsRegistrador
from servicios_aplicacion.abs_selector_temperatura import AbsSelectorTemperatura


class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):
    """
    Selector de modo de temperatura desde archivo.

    Lee el modo de temperatura ('ambiente' o 'deseada') desde un archivo
    local llamado 'tipo_temperatura'. Incluye registro de errores.
    """

    @staticmethod
    def obtener_selector():
        """Obtiene el modo de temperatura desde archivo."""
        try:
            with open("tipo_temperatura", "r", encoding="utf-8") as archivo:
                tipo_temperatura = archivo.read().strip()
        except IOError as exc:
            mensaje_error = "Error al leer el tipo de temperatura"
            registro_error = SelectorTemperaturaArchivo._armar_registro_error(
                SelectorTemperaturaArchivo.__name__,
                SelectorTemperaturaArchivo.obtener_selector.__name__,
                str(datetime.datetime.now()),
                str(IOError),
                mensaje_error)

            SelectorTemperaturaArchivo.registrar_error(registro_error)
            raise IOError(mensaje_error) from exc
        return tipo_temperatura

    @staticmethod
    def _armar_registro_error(clase, metodo, fecha_hora, tipo_de_error, mensaje):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "metodo: " + metodo + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "tipo_de_error: " + tipo_de_error + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "-------------------------" + "\n" + "\n" + "\n"
        return registro

    @staticmethod
    def registrar_error(registro):
        """Registra un error en el archivo de log."""
        try:
            with open("registro_errores", "a", encoding="utf-8") as archivo_errores:
                archivo_errores.write(registro)
        except IOError as exc:
            raise IOError("Error al escribir el archivo de errores") from exc


class SelectorTemperaturaSocket(AbsSelectorTemperatura):
    """
    Selector de modo de temperatura via socket TCP.

    Escucha conexiones TCP para recibir cambios de modo de temperatura.
    Mantiene el estado actual y responde de forma no-bloqueante.

    Patron de Diseno:
        - DIP: Recibe host y puerto via inyeccion de dependencias

    Args:
        host: Direccion IP para escuchar conexiones.
        puerto: Puerto TCP para escuchar conexiones.
    """

    def __init__(self, host, puerto):
        """
        Inicializa el socket persistente y el estado.

        Args:
            host: Direccion IP para escuchar conexiones.
            puerto: Puerto TCP para escuchar conexiones.
        """
        self._estado_actual = "ambiente"  # Estado inicial
        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        self._servidor.listen(1)

        self._conexion = None
        self._servidor.settimeout(1.0)  # Timeout para accept

    # pylint: disable=arguments-differ
    def obtener_selector(self):
        """
        Consulta no-bloqueante del selector.
        Retorna el estado actual sin bloquearse si no hay cambios.
        """
        try:
            # Si no hay conexión activa, intentar aceptar una (con timeout)
            if self._conexion is None:
                try:
                    self._conexion, _ = self._servidor.accept()
                    self._conexion.settimeout(0.1)  # Timeout corto para recv
                except socket.timeout:
                    # No hay cliente intentando conectar, devolver estado actual
                    return self._estado_actual

            # Intentar leer datos (no bloqueante)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    nuevo_estado = str(datos.decode("utf-8"))
                    self._estado_actual = nuevo_estado
                    print("[Selector] Cambio a modo: {}".format(self._estado_actual.upper()))
                else:
                    # Cliente cerró conexión
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # No hay datos nuevos, mantener estado actual
                pass
            except ConnectionError as e:
                print("[Selector] Error de conexión: {}".format(e))
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except (socket.error, OSError) as e:
            print("[Selector] Error: {}".format(e))

        return self._estado_actual

    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self._conexion:
            self._conexion.close()
        if self._servidor:
            self._servidor.close()
