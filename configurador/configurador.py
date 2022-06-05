"""
Clase que define que componentes se usaran
"""

from agentes_sensores.proxy_bateria import *
from agentes_sensores.proxy_sensor_temperatura import *
from agentes_actuadores.actuador_climatizador import *
from agentes_actuadores.visualizador_bateria import *
from agentes_actuadores.visualizador_temperatura import *
from agentes_actuadores.visualizador_climatizador import *
from entidades.climatizador import *


class Configurador:

    @staticmethod
    def configurar_proxy_bateria():
        return ProxyBateriaArchivo()

    @staticmethod
    def configurar_proxy_temperatura():
        return ProxySensorTemperaturaSocket()

    @staticmethod
    def configurar_actuador_climatizador():
        return ActuadorClimatizador()

    @staticmethod
    def configurar_visualizador_bateria():
        return VisualizadorBateria()

    @staticmethod
    def configurar_visualizador_temperaturas():
        return VisualizadorTemperaturas()

    @staticmethod
    def configurar_visualizador_climatizador():
        return VisualizadorClimatizador()

    @staticmethod
    def configurar_climatizador():
        return Climatizador()
