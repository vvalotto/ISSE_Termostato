"""
Clase que define que componentes se usaran
"""
import json
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

    configuracion_termostato = None

    @staticmethod
    def cargar_configuracion():
        with open("termostato.json", "r") as termostato_config:
            Configurador.configuracion_termostato = json.load(termostato_config)
        return

    @staticmethod
    def configurar_proxy_bateria():
        return FactoryProxyBateria.crear(Configurador.configuracion_termostato["proxy_bateria"])

    @staticmethod
    def configurar_proxy_temperatura():
        return FactoryProxySensorTemperatura.crear(Configurador.configuracion_termostato["proxy_sensor_temperatura"])

    @staticmethod
    def configurar_actuador_climatizador():
        return FactoryActuadorClimatizador.crear(Configurador.configuracion_termostato["actuador_climatizador"])

    @staticmethod
    def configurar_visualizador_temperatura():
        return FactoryVisualizadorTemperatura.crear(Configurador.configuracion_termostato["visualizador_temperatura"])

    @staticmethod
    def configurar_visualizador_bateria():
        return FactoryVisualizadorBateria.crear(Configurador.configuracion_termostato["visualizador_bateria"])

    @staticmethod
    def configurar_visualizador_climatizador():
        return FactoryVisualizadorClimatizador.crear(Configurador.configuracion_termostato["visualizador_climatizador"])

    @staticmethod
    def configurar_climatizador():
        return FactoryClimatizador.crear(Configurador.configuracion_termostato["climatizador"])

    @staticmethod
    def configurar_selector_temperatura():
        return FactorySelectorTemperatura.crear(Configurador.configuracion_termostato["selector_temperatura"])

    @staticmethod
    def configurar_seteo_temperatura():
        return FactorySeteoTemperatura.crear(Configurador.configuracion_termostato["seteo_temperatura"])
