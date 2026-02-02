"""
Visualizador de estado consolidado del termostato.

Envía el estado completo del sistema (temperatura, climatizador, batería, etc.)
en un único mensaje JSON al puerto 14001 para consumo por aplicaciones UX externas.

Este visualizador es compatible con el formato esperado por ux_termostato.
"""
import json
import socket
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class VisualizadorEstadoConsolidadoSocket:
    """
    Visualizador que envía el estado completo del termostato como JSON vía TCP.

    Recopila información de los tres gestores (ambiente, climatizador, batería)
    y la envía consolidada en un único mensaje JSON al puerto 14001.

    Formato JSON enviado:
        {
            "temperatura_actual": float,
            "temperatura_deseada": float,
            "modo_climatizador": str,  # "calentando" | "enfriando" | "reposo" | "apagado"
            "falla_sensor": bool,
            "bateria_baja": bool,
            "encendido": bool,
            "modo_display": str,  # "ambiente" | "deseada"
            "timestamp": str  # ISO 8601
        }

    Patron de Diseno:
        - Facade: Simplifica el envío de estado completo consolidado
        - Adapter: Adapta el formato interno a JSON esperado por UX externa
    """

    def __init__(self, host="localhost", port=14001):
        """
        Inicializa el visualizador consolidado.

        Args:
            host: Dirección IP del servidor UX (default: localhost).
            port: Puerto TCP del servidor UX (default: 14001).
        """
        self._host = host
        self._port = port
        logger.info("VisualizadorEstadoConsolidadoSocket inicializado: %s:%d", host, port)

    def mostrar_estado_completo(
        self,
        gestor_ambiente,
        gestor_climatizador,
        gestor_bateria
    ):
        """
        Envía el estado completo del termostato vía socket TCP.

        Recopila el estado de los tres gestores, lo serializa a JSON
        y lo envía al servidor UX en el puerto configurado.

        Args:
            gestor_ambiente: GestorAmbiente con temperatura y configuración.
            gestor_climatizador: GestorClimatizador con estado del climatizador.
            gestor_bateria: GestorBateria con nivel de carga.
        """
        logger.info("→ Enviando estado consolidado JSON a UX...")
        try:
            # Recopilar estado de cada gestor
            logger.debug("Construyendo estado desde gestores...")
            estado = self._construir_estado(
                gestor_ambiente,
                gestor_climatizador,
                gestor_bateria
            )
            logger.info("Estado construido: temp=%.1f°C, modo=%s",
                       estado['temperatura_actual'],
                       estado['modo_climatizador'])

            # Serializar a JSON con terminador de línea (mejor práctica para TCP)
            mensaje_json = json.dumps(estado) + "\n"
            logger.info("JSON generado (%d bytes): %s", len(mensaje_json), mensaje_json.strip())

            # Enviar vía TCP (patrón efímero: conectar -> enviar -> cerrar)
            logger.debug("Creando socket TCP...")
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = (self._host, self._port)

            logger.info("Conectando a UX en %s:%d...", self._host, self._port)
            cliente.connect(direccion_servidor)
            logger.info("✓ Conectado exitosamente")

            logger.debug("Enviando %d bytes...", len(mensaje_json))
            bytes_enviados = cliente.send(mensaje_json.encode('utf-8'))
            logger.info("✓ Enviados %d bytes", bytes_enviados)

            # Shutdown para señalar "no más escrituras" pero permitir que el servidor lea
            logger.debug("Haciendo shutdown del socket (SHUT_WR)...")
            try:
                cliente.shutdown(socket.SHUT_WR)
            except OSError:
                pass  # Socket ya cerrado, no es crítico

            # Esperar un momento para que el servidor procese los datos
            logger.debug("Esperando que servidor procese datos...")
            time.sleep(0.5)  # 500ms de gracia para asegurar procesamiento

            logger.debug("Cerrando socket...")
            cliente.close()
            logger.info("✓ Estado consolidado enviado exitosamente")

        except ConnectionError as e:
            logger.error("❌ Error de conexión con UX en %s:%d - %s", self._host, self._port, e)
        except socket.error as e:
            logger.error("❌ Error de socket: %s", e, exc_info=True)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("❌ Error inesperado al enviar estado consolidado: %s", e, exc_info=True)

    def _construir_estado(
        self,
        gestor_ambiente,
        gestor_climatizador,
        gestor_bateria
    ):
        """
        Construye el diccionario con el estado completo del sistema.

        Args:
            gestor_ambiente: GestorAmbiente.
            gestor_climatizador: GestorClimatizador.
            gestor_bateria: GestorBateria.

        Returns:
            dict: Estado completo en formato compatible con ux_termostato.
        """
        # Obtener temperaturas
        temp_actual = gestor_ambiente.obtener_temperatura_ambiente()
        temp_deseada = gestor_ambiente.obtener_temperatura_deseada()
        logger.debug("Temperaturas: actual=%s, deseada=%s", temp_actual, temp_deseada)

        # Mapear estado del climatizador
        # ISSE_Termostato: "apagado", "calentando", "enfriando"
        # ux_termostato espera: "apagado", "calentando", "enfriando", "reposo"
        estado_climatizador = gestor_climatizador.obtener_estado_climatizador()
        modo_climatizador = self._mapear_modo_climatizador(estado_climatizador)
        logger.debug("Climatizador: estado_raw='%s' -> modo_mapeado='%s'",
                    estado_climatizador, modo_climatizador)

        # Detectar falla de sensor (temperatura None)
        falla_sensor = temp_actual is None

        # Si hay falla, usar valor seguro para evitar errores en UX
        if falla_sensor:
            logger.warning("⚠️  Falla de sensor detectada (temp_actual=None), usando 0.0")
            temp_actual = 0.0

        # Detectar batería baja
        indicador_bateria = gestor_bateria.obtener_indicador_de_carga()
        bateria_baja = indicador_bateria == "BAJA"
        logger.debug("Batería: indicador='%s', baja=%s", indicador_bateria, bateria_baja)

        # Modo display (qué temperatura muestra la UI)
        modo_display = gestor_ambiente.ambiente.temperatura_a_mostrar
        logger.debug("Modo display: '%s'", modo_display)

        # Timestamp ISO 8601
        timestamp = datetime.now().isoformat()

        estado = {
            "temperatura_actual": float(temp_actual),
            "temperatura_deseada": float(temp_deseada),
            "modo_climatizador": modo_climatizador,
            "falla_sensor": falla_sensor,
            "bateria_baja": bateria_baja,
            "encendido": True,  # Siempre True si el sistema está ejecutándose
            "modo_display": modo_display,
            "timestamp": timestamp
        }

        logger.debug("Estado construido completo: %s", estado)
        return estado

    @staticmethod
    def _mapear_modo_climatizador(estado):
        """
        Mapea el estado del climatizador de ISSE_Termostato a formato UX.

        Args:
            estado: Estado del climatizador ("apagado", "calentando", "enfriando").

        Returns:
            str: Modo climatizador para UX ("apagado", "calentando", "enfriando", "reposo").
        """
        # En ISSE_Termostato, "apagado" puede significar dos cosas:
        # - Sistema completamente apagado
        # - Sistema en reposo (temperatura alcanzada)
        # Para simplificar, mapeamos "apagado" a "reposo"
        mapeo = {
            "apagado": "reposo",
            "calentando": "calentando",
            "enfriando": "enfriando"
        }
        return mapeo.get(estado, "reposo")
