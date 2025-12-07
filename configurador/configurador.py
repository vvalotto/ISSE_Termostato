"""
Configurador del sistema de termostato.

Este modulo es el punto central de configuracion del sistema. Carga la
configuracion desde termostato.json y proporciona metodos factory para
crear los componentes del sistema segun la configuracion.

Patron de Diseno:
    - Abstract Factory: Crea familias de objetos relacionados
    - Singleton (configuracion): Una sola configuracion global
"""
import json
import os
from configurador.factory_proxy_bateria import FactoryProxyBateria
from configurador.factory_sensor_temperatura import FactoryProxySensorTemperatura
from configurador.factory_actuador_climatizador import FactoryActuadorClimatizador
from configurador.factory_visualizador_bateria import FactoryVisualizadorBateria
from configurador.factory_visualizador_climatizador import FactoryVisualizadorClimatizador
from configurador.factory_climatizador import FactoryClimatizador
from configurador.factory_visualizador_temperatura import FactoryVisualizadorTemperatura
from configurador.factory_selector_temperatura import FactorySelectorTemperatura
from configurador.factory_seteo_temperatura import FactorySeteoTemperatura


# pylint: disable=unsubscriptable-object,unsupported-membership-test
class Configurador:
    """
    Configurador central del sistema de termostato.

    Carga la configuracion desde termostato.json y proporciona metodos
    factory para crear los componentes del sistema. Actua como Abstract
    Factory coordinando la creacion de familias de objetos relacionados.

    Attributes:
        configuracion_termostato (dict): Diccionario con la configuracion
            cargada desde termostato.json. None si no se ha cargado.

    Note:
        Debe llamarse cargar_configuracion() antes de usar otros metodos.
    """

    configuracion_termostato = None

    @staticmethod
    def cargar_configuracion():
        """
        Carga la configuracion desde termostato.json.

        Busca el archivo en multiples ubicaciones y lo carga en memoria.
        Valida que contenga todas las claves requeridas.

        Raises:
            FileNotFoundError: Si no encuentra termostato.json.
            json.JSONDecodeError: Si el archivo tiene formato invalido.
            KeyError: Si faltan claves requeridas en la configuracion.
        """
        config_paths = [
            "termostato.json",
            "/etc/termostato/termostato.json",
            os.path.join(os.path.dirname(__file__), "termostato.json"),
        ]

        config_file = None
        for path in config_paths:
            if os.path.exists(path):
                config_file = path
                break

        if config_file is None:
            raise FileNotFoundError(
                f"ERROR: No se encontro termostato.json en: {config_paths}"
            )

        try:
            with open(config_file, "r", encoding="utf-8") as termostato_config:
                Configurador.configuracion_termostato = json.load(termostato_config)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"ERROR: termostato.json tiene formato invalido: {e}",
                e.doc,
                e.pos
            ) from e

        Configurador._validar_configuracion()

    @staticmethod
    def configurar_proxy_bateria():
        """Crea y retorna el proxy de bateria segun configuracion."""
        tipo = Configurador.configuracion_termostato["proxy_bateria"]
        return FactoryProxyBateria.crear(tipo)

    @staticmethod
    def configurar_proxy_temperatura():
        """Crea y retorna el proxy de sensor de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["proxy_sensor_temperatura"]
        return FactoryProxySensorTemperatura.crear(tipo)

    @staticmethod
    def configurar_actuador_climatizador():
        """Crea y retorna el actuador de climatizador segun configuracion."""
        tipo = Configurador.configuracion_termostato["actuador_climatizador"]
        return FactoryActuadorClimatizador.crear(tipo)

    @staticmethod
    def configurar_visualizador_temperatura():
        """Crea y retorna el visualizador de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_temperatura"]
        return FactoryVisualizadorTemperatura.crear(tipo)

    @staticmethod
    def configurar_visualizador_bateria():
        """Crea y retorna el visualizador de bateria segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_bateria"]
        return FactoryVisualizadorBateria.crear(tipo)

    @staticmethod
    def configurar_visualizador_climatizador():
        """Crea y retorna el visualizador de climatizador segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_climatizador"]
        return FactoryVisualizadorClimatizador.crear(tipo)

    @staticmethod
    def configurar_climatizador():
        """Crea y retorna el climatizador con histeresis segun configuracion."""
        tipo = Configurador.configuracion_termostato["climatizador"]
        histeresis = Configurador.obtener_histeresis()
        return FactoryClimatizador.crear(tipo, histeresis=histeresis)

    @staticmethod
    def configurar_selector_temperatura():
        """Crea y retorna el selector de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["selector_temperatura"]
        return FactorySelectorTemperatura.crear(tipo)

    @staticmethod
    def configurar_seteo_temperatura():
        """Crea y retorna el componente de seteo de temperatura segun config."""
        tipo = Configurador.configuracion_termostato["seteo_temperatura"]
        return FactorySeteoTemperatura.crear(tipo)

    @staticmethod
    def obtener_host_escucha():
        """Retorna el host donde escuchar conexiones socket."""
        config = Configurador.configuracion_termostato
        return config.get("red", {}).get("host_escucha", "localhost")

    @staticmethod
    def obtener_puerto(nombre_sensor):
        """Retorna el puerto para un sensor especifico."""
        puertos_default = {
            "bateria": 11000,
            "temperatura": 12000,
            "seteo_temperatura": 13000
        }
        config = Configurador.configuracion_termostato
        puertos = config.get("red", {}).get("puertos", puertos_default)
        return puertos.get(nombre_sensor, puertos_default.get(nombre_sensor))

    @staticmethod
    def obtener_api_url():
        """Retorna la URL base de la API REST."""
        config = Configurador.configuracion_termostato
        return config.get("red", {}).get("api_url", "http://localhost:5050")

    @staticmethod
    def obtener_carga_maxima_bateria():
        """Retorna la carga maxima de la bateria en voltios."""
        config = Configurador.configuracion_termostato
        return config.get("bateria", {}).get("carga_maxima", 5.0)

    @staticmethod
    def obtener_umbral_bateria():
        """Retorna el umbral para indicador de bateria baja (decimal)."""
        config = Configurador.configuracion_termostato
        return config.get("bateria", {}).get("umbral_carga_baja", 0.95)

    @staticmethod
    def obtener_histeresis():
        """Retorna el valor de histeresis para control de temperatura."""
        config = Configurador.configuracion_termostato
        return config.get("ambiente", {}).get("histeresis", 2.0)

    @staticmethod
    def obtener_temperatura_inicial():
        """Retorna la temperatura deseada inicial en grados Celsius."""
        config = Configurador.configuracion_termostato
        return config.get("ambiente", {}).get("temperatura_inicial", 22.0)

    @staticmethod
    def obtener_incremento_temperatura():
        """Retorna el incremento para ajustar temperatura en grados."""
        config = Configurador.configuracion_termostato
        return config.get("ambiente", {}).get("incremento_ajuste", 1.0)

    @staticmethod
    def _validar_configuracion():
        """
        Valida que la configuracion tenga todas las claves necesarias.

        Raises:
            KeyError: Si falta alguna clave requerida.
        """
        config = Configurador.configuracion_termostato

        claves_requeridas = [
            "proxy_bateria", "proxy_sensor_temperatura", "climatizador",
            "actuador_climatizador", "selector_temperatura", "seteo_temperatura",
            "visualizador_bateria", "visualizador_temperatura",
            "visualizador_climatizador"
        ]

        for clave in claves_requeridas:
            if clave not in config:
                raise KeyError(f"ERROR: Falta la clave '{clave}' en termostato.json")

        if "red" in config:
            red = config["red"]
            if "host_escucha" not in red:
                print("ADVERTENCIA: Falta 'host_escucha', usando 'localhost'")
            if "puertos" not in red:
                print("ADVERTENCIA: Falta 'puertos', usando valores por defecto")
            if "api_url" not in red:
                print("ADVERTENCIA: Falta 'api_url', usando default")
        else:
            print("ADVERTENCIA: No hay seccion 'red' en termostato.json")
            print("  -> Proxies socket usaran 'localhost' y puertos default")
            print("  -> Visualizadores API usaran 'http://localhost:5050'")
