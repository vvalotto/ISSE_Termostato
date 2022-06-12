"""
Clase que define que componentes se usaran
"""

from agentes_sensores.factory_proxy_bateria import *
from agentes_sensores.factory_sensor_temperatura import *
from agentes_sensores.factory_selector_temperatura import *
from agentes_actuadores.factory_actuador_climatizador import *
from agentes_actuadores.visualizador_bateria import *
from agentes_actuadores.visualizador_temperatura import *
from agentes_actuadores.visualizador_climatizador import *
from entidades.factory_climatizador import *


class Configurador:

    @staticmethod
    def configurar_proxy_bateria():
        return FactoryProxyBateria.crear("archivo")

    @staticmethod
    def configurar_proxy_temperatura():
        return FactoryProxySensorTemperatura.crear("archivo")

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
