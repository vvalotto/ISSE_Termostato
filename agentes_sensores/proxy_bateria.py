"""
Proxies para lectura del sensor de bateria.

Este modulo contiene las implementaciones concretas del proxy de bateria,
permitiendo leer el nivel de carga desde archivo o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el sensor de bateria real/remoto
"""
# pylint: disable=duplicate-code
# El codigo de socket es similar entre proxies (patron comun aceptable)

import logging
import socket
from entidades.abs_bateria import AbsProxyBateria

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class ProxyBateriaArchivo(AbsProxyBateria):
    """
    Proxy para lectura de bateria desde archivo.

    Implementa la interfaz AbsProxyBateria leyendo el nivel de carga
    desde un archivo local llamado 'bateria'.
    """

    def leer_carga(self):
        """Lee el nivel de carga desde el archivo 'bateria'."""
        logger.debug("Intentando leer nivel de carga desde archivo 'bateria'")
        try:
            with open("bateria", "r", encoding="utf-8") as archivo:
                carga = float(archivo.read())
                logger.info("Nivel de carga leído exitosamente: %.2f%%", carga)
        except IOError as e:
            logger.error("Error al leer archivo 'bateria': %s", str(e))
            carga = None
        except ValueError as e:
            logger.error("Valor inválido en archivo 'bateria': %s", str(e))
            carga = None
        return carga


# pylint: disable=too-few-public-methods
class ProxyBateriaSocket(AbsProxyBateria):
    """
    Proxy para lectura de bateria via socket TCP.

    Implementa la interfaz AbsProxyBateria escuchando conexiones
    TCP para recibir el nivel de carga de un cliente remoto.

    Ciclo de vida del socket: EFIMERO — el socket se crea y cierra en cada
    llamada a leer_carga(). Esta estrategia es adecuada porque el sensor es
    consultado periodicamente por el sistema y el actor externo actua como
    cliente que siempre esta disponible. Si el cliente se reinicia, la proxima
    lectura se reconecta automaticamente sin logica adicional.
    Ver: docs/decisions/ADR-001-ciclo-vida-sockets.md

    Patron de Diseno:
        - DIP: Recibe host y puerto via inyeccion de dependencias

    Args:
        host: Direccion IP para escuchar conexiones.
        puerto: Puerto TCP para escuchar conexiones.
    """

    def __init__(self, host, puerto):
        """
        Inicializa el proxy con la configuracion de red.

        Args:
            host: Direccion IP para escuchar conexiones.
            puerto: Puerto TCP para escuchar conexiones.
        """
        self._host = host
        self._puerto = puerto

    def leer_carga(self):
        """Lee el nivel de carga via socket TCP."""
        logger.debug("Iniciando servidor socket en %s:%d para lectura de carga",
                    self._host, self._puerto)
        carga = None
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto

        direccion_servidor = (self._host, self._puerto)
        servidor.bind(direccion_servidor)

        servidor.listen(1)
        logger.info("Esperando conexión en %s:%d...", self._host, self._puerto)
        conexion, direccion_cliente = servidor.accept()
        logger.info("Cliente conectado desde: %s", direccion_cliente)

        try:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    logger.debug("Cliente cerró la conexión")
                    break
                carga = float(datos.decode("utf-8"))
                logger.info("Nivel de carga recibido: %.2f%%", carga)
        except ValueError as e:
            logger.error("Valor inválido recibido del sensor: %s", str(e))
        except ConnectionError as e:  # FIX: sintaxis correcta
            logger.error("Error de conexión: %s", str(e))
        finally:  # FIX: asegurar cierre
            conexion.close()
            servidor.close()
            logger.debug("Socket cerrado")

        return carga
