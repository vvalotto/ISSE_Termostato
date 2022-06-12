"""
Clase que define que componentes se usaran
"""

from configurador.factory_proxy_bateria import *
from configurador.factory_sensor_temperatura import *
from configurador.factory_actuador_climatizador import *
from configurador.factory_visualizador_bateria import *
from configurador.factory_visualizador_climatizador import *
from configurador.factory_climatizador import *
from configurador.factory_visualizador_temperatura import *
from configurador.factory_selector_temperatura import *
from configurador.factory_seteo_temperatura import *


class Configurador:

    @staticmethod
    def configurar_proxy_bateria():
        return FactoryProxyBateria.crear("socket")

    @staticmethod
    def configurar_proxy_temperatura():
        return FactoryProxySensorTemperatura.crear("socket")

    @staticmethod
    def configurar_actuador_climatizador():
        return FactoryActuadorClimatizador.crear("general")

    @staticmethod
    def configurar_visualizador_temperatura():
        return FactoryVisualizadorTemperatura.crear("socket")

    @staticmethod
    def configurar_visualizador_bateria():
        return FactoryVisualizadorBateria.crear("socket")

    @staticmethod
    def configurar_visualizador_climatizador():
        return FactoryVisualizadorClimatizador.crear("socket")

    @staticmethod
    def configurar_climatizador():
        return FactoryClimatizador.crear("calefactor")

    @staticmethod
    def configurar_selector_temperatura():
        return FactorySelectorTemperatura.crear("archivo")

    @staticmethod
    def configurar_seteo_temperatura():
        return FactorySeteoTemperatura.crear("socket")
