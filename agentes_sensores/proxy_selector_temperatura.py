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
import logging
import socket

from registrador.registrador import AbsRegistrador
from entidades.abs_selector_temperatura import AbsSelectorTemperatura

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):
    """
    Selector de modo de temperatura desde archivo.

    Lee el modo de temperatura ('ambiente' o 'deseada') desde un archivo
    local llamado 'tipo_temperatura'. Incluye registro de errores.
    """

    @staticmethod
    def obtener_selector():
        """Obtiene el modo de temperatura desde archivo."""
        logger.debug("Intentando leer tipo de temperatura desde archivo 'tipo_temperatura'")
        try:
            with open("tipo_temperatura", "r", encoding="utf-8") as archivo:
                tipo_temperatura = archivo.read().strip()
                logger.info("Tipo de temperatura leído: %s", tipo_temperatura)
        except IOError as exc:
            mensaje_error = "Error al leer el tipo de temperatura"
            logger.error("Error al leer archivo 'tipo_temperatura': %s", str(exc))
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

    Ciclo de vida del socket: PERSISTENTE — el socket se crea al inicializar
    el proxy y se mantiene abierto entre llamadas. Esta estrategia es adecuada
    porque los comandos de usuario son esporadicos e impredecibles en el tiempo.
    El proxy actua como servidor (bind/listen/accept), por lo que debe mantenerse
    activo permanentemente: cerrar y reabrir el socket en cada ciclo crearía una
    ventana donde los comandos podrian perderse.
    Ver: docs/decisions/ADR-001-ciclo-vida-sockets.md

    Soporta uso como context manager para garantizar cierre determinista
    del socket: usar con bloque `with` en el Lanzador o OperadorParalelo.

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
        logger.info("Inicializando selector de temperatura socket en %s:%d", host, puerto)
        self._estado_actual = "ambiente"  # Estado inicial
        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        self._servidor.listen(1)

        self._conexion = None
        self._servidor.settimeout(1.0)  # Timeout para accept
        logger.debug("Selector socket listo, modo inicial: %s", self._estado_actual)

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
                    self._conexion, direccion_cliente = self._servidor.accept()
                    self._conexion.settimeout(0.1)  # Timeout corto para recv
                    logger.info("Cliente selector conectado desde: %s", direccion_cliente)
                except socket.timeout:
                    # No hay cliente intentando conectar, devolver estado actual
                    logger.debug("Sin nuevas conexiones, modo actual: %s", self._estado_actual)
                    return self._estado_actual

            # Intentar leer datos (no bloqueante)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    nuevo_estado = str(datos.decode("utf-8"))
                    self._estado_actual = nuevo_estado
                    logger.info("Cambio a modo: %s", self._estado_actual.upper())
                else:
                    # Cliente cerró conexión
                    logger.debug("Cliente selector cerró la conexión")
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # No hay datos nuevos, mantener estado actual
                logger.debug("Sin nuevos datos, manteniendo modo: %s", self._estado_actual)
            except ConnectionError as e:
                logger.error("Error de conexión en selector: %s", str(e))
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except (socket.error, OSError) as e:
            logger.error("Error en selector socket: %s", str(e))

        return self._estado_actual

    def __enter__(self):
        """Soporte para uso como context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el socket al salir del contexto."""
        if self._conexion:
            self._conexion.close()
            self._conexion = None
        if self._servidor:
            self._servidor.close()
            self._servidor = None
        logger.debug("Socket de selector cerrado por context manager")
        return False
