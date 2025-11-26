"""
Clase que es la responsable de manejar la entidad Ambiente.
- Obteniendo la temperatura desde el sensor externo
- Aceptando la determinación de la temperatura deseeada
- mostrando las temperaturas en los dispositivos de visualizacion
"""

from entidades.ambiente import *
from configurador.configurador import *


class GestorAmbiente:

    @property
    def ambiente(self):
        return self._ambiente

    def __init__(self):
        # Obtener temperatura inicial desde configuración
        temperatura_inicial = Configurador.obtener_temperatura_inicial()
        self._ambiente = Ambiente(temperatura_deseada_inicial=temperatura_inicial)
        self._proxy_sensor_temperatura = Configurador.configurar_proxy_temperatura()
        self._visualizador_temperatura = Configurador().configurar_visualizador_temperatura()

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
        """Aumenta la temperatura deseada según el incremento configurado"""
        incremento = Configurador.obtener_incremento_temperatura()
        self._ambiente.temperatura_deseada += incremento

    def disminuir_temperatura_deseada(self):
        """Disminuye la temperatura deseada según el incremento configurado"""
        incremento = Configurador.obtener_incremento_temperatura()
        self._ambiente.temperatura_deseada -= incremento

    def obtener_temperatura_deseada(self):
        return self._ambiente.temperatura_deseada

    def mostrar_temperatura_deseada(self):
        self._visualizador_temperatura.mostrar_temperatura_deseada(self._ambiente.temperatura_deseada)

    def mostrar_temperatura(self):
        if self._ambiente.temperatura_a_mostrar == "ambiente":
            self._visualizador_temperatura.mostrar_temperatura_ambiente(self._ambiente.temperatura_ambiente)
        elif self._ambiente.temperatura_a_mostrar == "deseada":
            self._visualizador_temperatura.mostrar_temperatura_deseada(self._ambiente.temperatura_deseada)

    def indicar_temperatura_a_mostrar(self, tipo_temperatura):
        self.ambiente.temperatura_a_mostrar = tipo_temperatura
