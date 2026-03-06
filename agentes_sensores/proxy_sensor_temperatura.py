"""
Proxies para lectura del sensor de temperatura.

Este modulo contiene las implementaciones concretas del proxy de temperatura,
permitiendo leer la temperatura ambiente desde archivo o via socket TCP.

Patron de Diseno:
    - Proxy: Representa el sensor de temperatura real/remoto
"""
# pylint: disable=duplicate-code
# El codigo de socket es similar entre proxies (patron comun aceptable)

import logging
import socket
from entidades.abs_sensor_temperatura import AbsProxySensorTemperatura

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class ProxySensorTemperaturaArchivo(AbsProxySensorTemperatura):
    """
    Proxy para lectura de temperatura desde archivo.

    Implementa la interfaz AbsProxySensorTemperatura leyendo la temperatura
    desde un archivo local llamado 'temperatura'.
    """

    def leer_temperatura(self):
        """Lee la temperatura desde el archivo 'temperatura'."""
        logger.debug("Intentando leer temperatura desde archivo 'temperatura'")
        try:
            with open("temperatura", "r", encoding="utf-8") as archivo:
                temperatura = int(archivo.read())
                logger.info("Temperatura leída exitosamente: %d°C", temperatura)
        except IOError as exc:
            logger.error("Error al leer archivo 'temperatura': %s", str(exc))
            raise IOError("Error de Lectura de Sensor") from exc
        except ValueError as exc:
            logger.error("Valor inválido en archivo 'temperatura': %s", str(exc))
            raise ValueError("Valor de temperatura inválido") from exc
        return temperatura


# pylint: disable=too-few-public-methods
class ProxySensorTemperaturaSocket(AbsProxySensorTemperatura):
    """
    Proxy para lectura de temperatura via socket TCP.

    Implementa la interfaz AbsProxySensorTemperatura escuchando conexiones
    TCP para recibir la temperatura de un cliente remoto.

    Ciclo de vida del socket: EFIMERO — el socket se crea y cierra en cada
    llamada a leer_temperatura(). Esta estrategia es adecuada porque el sensor
    es consultado periodicamente por el sistema y el actor externo actua como
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

    def leer_temperatura(self):
        """Lee la temperatura via socket TCP."""
        logger.debug("Iniciando servidor socket en %s:%d para lectura de temperatura",
                    self._host, self._puerto)
        temperatura = None
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
                temperatura = float(datos.decode("utf-8"))
                logger.info("Temperatura recibida: %.1f°C", temperatura)
        except ValueError as e:
            logger.error("Valor inválido recibido del sensor: %s", str(e))
        except ConnectionError as e:  # FIX: sintaxis correcta
            logger.error("Error de conexión: %s", str(e))
        finally:  # FIX: asegurar cierre
            conexion.close()
            servidor.close()
            logger.debug("Socket cerrado")

        return temperatura
