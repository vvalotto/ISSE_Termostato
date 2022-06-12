"""
Clase que define que componentes se usaran
"""

from factory_proxy_bateria import *
from factory_sensor_temperatura import *
from factory_selector_temperatura import *
from factory_actuador_climatizador import *
from agentes_actuadores.visualizador_bateria import *
from agentes_actuadores.visualizador_temperatura import *
from agentes_actuadores.visualizador_climatizador import *
from factory_climatizador import *


class Configurador:

    @staticmethod
    def configurar_proxy_bateria():
        return FactoryProxyBateria.crear("archivo")

    @staticmethod
    def configurar_proxy_temperatura():
        return FactoryProxySensorTemperatura.crear("archivo")

    @staticmethod
    def configurar_selector_temperatura():
        return FactorySelectorTemperatura.crear("archivo")

    @staticmethod
    def configurar_actuador_climatizador():
        return FactoryActuadorClimatizador.crear("general")

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
        return FactoryClimatizador.crear("climatizador")
