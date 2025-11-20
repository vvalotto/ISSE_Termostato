"""
Clase que es la responsable de manejar la entidad Ambiente.
- Obteniendo la temperatura desde el sensor externo
- Aceptando la determinación de la temperatura deseeada
- mostrando las temperaturas en los dispositivos de visualizacion
"""

from agentes_sensores.proxy_sensor_temperatura import *
from entidades.ambiente import *
from agentes_actuadores.visualizador_temperatura import *


class GestorAmbiente:

    @property
    def ambiente(self):
        return self._ambiente

    def __init__(self, hal_adc=None):
        """
        Inicializa el gestor de ambiente

        :param hal_adc: Opcional, permite inyectar implementación HAL específica
                        Si es None, ProxySensorTemperatura usará HAL simulado por defecto
        """
        self._ambiente = Ambiente()

        # Permite inyectar HAL desde fuera (útil para testing y producción)
        if hal_adc is not None:
            self._proxy_sensor_temperatura = ProxySensorTemperatura(hal_adc)
        else:
            # Usa HAL simulado por defecto
            self._proxy_sensor_temperatura = ProxySensorTemperatura()

        self._visualizador_temperatura = VisualizadorTemperaturas()

    def leer_temperatura_ambiente(self):
        try:
            self._ambiente.temperatura_ambiente = self._proxy_sensor_temperatura.leer_temperatura()
        except Exception:
            self._ambiente.temperatura_ambiente = None

    def obtener_temperatura_ambiente(self):
        return self._ambiente.temperatura_ambiente

    def mostrar_temperatura_ambiente(self):
        self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_ambiente)

    def aumentar_temperatura_deseada(self):
        self._ambiente.temperatura_deseada += 1

    def disminuir_temperatura_deseada(self):
        self._ambiente.temperatura_deseada -= 1

    def obtener_temperatura_deseada(self):
        return self._ambiente.temperatura_deseada

    def mostrar_temperatura_deseada(self):
        self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_deseada)

    def mostrar_temperatura(self):
        if self._ambiente.temperatura_a_mostrar == "ambiente":
            self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_ambiente)
        elif self._ambiente.temperatura_a_mostrar == "deseada":
            self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_deseada)

    def indicar_temperatura_a_mostrar(self, tipo_temperatura):
        self.ambiente.temperatura_a_mostrar = tipo_temperatura
