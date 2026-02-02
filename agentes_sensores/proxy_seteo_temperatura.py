"""
Componentes para seteo de temperatura deseada.

Este modulo contiene las implementaciones para obtener comandos
de ajuste de temperatura (aumentar/disminuir) desde consola
o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el control de seteo real/remoto
"""
import logging
import socket
from servicios_aplicacion.abs_seteo_temperatura import AbsSeteoTemperatura

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class SeteoTemperatura(AbsSeteoTemperatura):
    """
    Seteo de temperatura desde consola.

    Solicita al usuario via input() el comando de ajuste
    de temperatura: '1' para aumentar, '2' para disminuir.
    """

    def obtener_seteo(self):
        logger.debug("Esperando entrada de usuario para seteo de temperatura")
        opcion = "0"
        while opcion not in ["1", "2"]:
            opcion = input(">")
        diferencia = "aumentar" if opcion == "1" else "disminuir"
        logger.info("Usuario seleccionó: %s temperatura", diferencia)
        return diferencia


class SeteoTemperaturaSocket(AbsSeteoTemperatura):
    """
    Seteo de temperatura via socket TCP.

    Escucha conexiones TCP para recibir comandos de ajuste
    de temperatura ('aumentar' o 'disminuir').

    Patron de Diseno:
        - DIP: Recibe host y puerto via inyeccion de dependencias

    Args:
        host: Direccion IP para escuchar conexiones.
        puerto: Puerto TCP para escuchar conexiones.
    """

    def __init__(self, host, puerto):
        """
        Inicializa el socket persistente.

        Args:
            host: Direccion IP para escuchar conexiones.
            puerto: Puerto TCP para escuchar conexiones.
        """
        logger.info("Inicializando seteo de temperatura socket en %s:%d", host, puerto)
        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        self._servidor.listen(1)

        self._conexion = None
        self._servidor.settimeout(2.0)  # Timeout para accept
        logger.debug("Socket de seteo listo para recibir comandos")

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
                    logger.info("Cliente de seteo conectado desde: %s", direccion_cliente)
                except socket.timeout:
                    # No hay cliente, retornar None
                    logger.debug("Sin cliente de seteo conectado")
                    return None

            # Leer comando (bloqueante con timeout)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    diferencia = str(datos.decode("utf-8"))
                    logger.info("Comando de seteo recibido: %s", diferencia)
                else:
                    # Cliente cerró conexión
                    logger.debug("Cliente de seteo desconectado")
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # Timeout esperando comando, retornar None
                logger.debug("Timeout esperando comando de seteo")
                return None
            except ConnectionError as e:
                logger.error("Error de conexión en seteo: %s", str(e))
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except (socket.error, OSError) as e:
            logger.error("Error en socket de seteo: %s", str(e))

        return diferencia

    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self._conexion:
            self._conexion.close()
        if self._servidor:
            self._servidor.close()
