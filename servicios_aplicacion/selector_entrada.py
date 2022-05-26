"""
Clase Responsable del establecimiento de la temperatura deseada
"""
from agentes_sensores.proxy_seteo_temperatura import *
from agentes_sensores.proxy_selector_temperatura import *
from gestores_entidades.gestor_ambiente import *


class SelectorEntradaTemperatura:

    def __init__(self, gestor_ambiente):
        """
        Arma la clases con la que necesita colaborar
        """
        self._seteo_temperatura = SeteoTemperatura()
        self._selector_temperatura = SelectorTemperatura()
        self._gestor_ambiente = gestor_ambiente

    def ejecutar(self):

        """
        Ejecucion periodica para observar si el usuario quiere
        setear la temperatura
        En caso que asi sea, se queda ciclando para leer el ingreso
        de las consignas
        :return:
        """
        while self._selector_temperatura.obtener_selector() == "deseada":
            self._mostrar_temperatura_deseada()
            self._obtener_seteo_temperatura_deseada()
        self._gestor_ambiente.indicar_temperatura_a_mostrar("ambiente")

    def _mostrar_temperatura_deseada(self):
        self._gestor_ambiente.indicar_temperatura_a_mostrar("deseada")
        self._gestor_ambiente.mostrar_temperatura()

    def _obtener_seteo_temperatura_deseada(self):
        opcion = self._seteo_temperatura.obtener_seteo()

        if opcion == "aumentar":
            self._gestor_ambiente.aumentar_temperatura_deseada()
        if opcion == "disminuir":
            self._gestor_ambiente.disminuir_temperatura_deseada()
