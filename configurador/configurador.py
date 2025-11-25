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
        try:
            with open("termostato.json", "r") as termostato_config:
                Configurador.configuracion_termostato = json.load(termostato_config)
        except FileNotFoundError:
            raise Exception("ERROR: No se encontró el archivo termostato.json")
        except json.JSONDecodeError as e:
            raise Exception("ERROR: termostato.json tiene formato inválido: {}".format(e))

        # Validar configuración
        Configurador._validar_configuracion()
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

    @staticmethod
    def obtener_host_escucha():
        """Retorna el host donde escuchar conexiones socket"""
        return Configurador.configuracion_termostato.get("red", {}).get("host_escucha", "localhost")

    @staticmethod
    def obtener_puerto(nombre_sensor):
        """Retorna el puerto para un sensor específico"""
        puertos_default = {
            "bateria": 11000,
            "temperatura": 12000,
            "seteo_temperatura": 13000
        }
        return Configurador.configuracion_termostato.get("red", {}).get("puertos", puertos_default).get(nombre_sensor, puertos_default.get(nombre_sensor))

    @staticmethod
    def obtener_api_url():
        """Retorna la URL base de la API REST"""
        return Configurador.configuracion_termostato.get("red", {}).get("api_url", "http://localhost:5050")

    @staticmethod
    def _validar_configuracion():
        """Valida que la configuración tenga todas las claves necesarias"""
        config = Configurador.configuracion_termostato

        # Validar claves principales
        claves_requeridas = [
            "proxy_bateria", "proxy_sensor_temperatura", "climatizador",
            "actuador_climatizador", "selector_temperatura", "seteo_temperatura",
            "visualizador_bateria", "visualizador_temperatura", "visualizador_climatizador"
        ]

        for clave in claves_requeridas:
            if clave not in config:
                raise Exception("ERROR: Falta la clave '{}' en termostato.json".format(clave))

        # Validar sección de red (opcional pero recomendada)
        if "red" in config:
            red = config["red"]
            if "host_escucha" not in red:
                print("ADVERTENCIA: Falta 'host_escucha' en config de red, usando 'localhost'")
            if "puertos" not in red:
                print("ADVERTENCIA: Falta 'puertos' en config de red, usando valores por defecto")
            if "api_url" not in red:
                print("ADVERTENCIA: Falta 'api_url' en config de red, usando 'http://localhost:5050'")
        else:
            print("ADVERTENCIA: No se encontró sección 'red' en termostato.json")
            print("  -> Los proxies socket usarán 'localhost' y puertos por defecto")
            print("  -> Los visualizadores API usarán 'http://localhost:5050'")
