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
import logging
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

logger = logging.getLogger(__name__)

_CLAVES_REQUERIDAS = [
    "proxy_bateria", "proxy_sensor_temperatura", "climatizador",
    "actuador_climatizador", "selector_temperatura", "seteo_temperatura",
    "visualizador_bateria", "visualizador_temperatura",
    "visualizador_climatizador"
]

_PUERTOS_DEFAULT = {
    "bateria": 11000,
    "temperatura": 12000,
    "seteo_temperatura": 13000,
    "visualizador_bateria": 14000,
    "visualizador_temperatura": 14001,
    "visualizador_climatizador": 14002
}


def _buscar_config(paths):
    """Busca termostato.json en las rutas dadas. Lanza FileNotFoundError si no lo encuentra."""
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("ERROR: No se encontro termostato.json en: {0}".format(paths))


def _cargar_json(config_file):
    """Carga y parsea un archivo JSON. Lanza JSONDecodeError si el formato es invalido."""
    try:
        with open(config_file, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            "ERROR: termostato.json tiene formato invalido: {0}".format(e),
            e.doc,
            e.pos
        ) from e


def _verificar_claves_requeridas(config):
    """Verifica que el diccionario de config tenga todas las claves requeridas."""
    for clave in _CLAVES_REQUERIDAS:
        if clave not in config:
            raise KeyError("ERROR: Falta la clave '{0}' en termostato.json".format(clave))


def _verificar_configuracion_red(red):
    """Valida la seccion 'red' de la configuracion y emite advertencias si faltan claves."""
    if red is None:
        logger.warning(
            "No hay seccion 'red' en termostato.json. "
            "Proxies socket usaran 'localhost' y puertos default. "
            "Visualizadores API usaran 'http://localhost:5050'"
        )
        return
    if "host_escucha" not in red:
        logger.warning("Falta 'host_escucha' en configuracion, usando 'localhost'")
    if "puertos" not in red:
        logger.warning("Falta 'puertos' en configuracion, usando valores por defecto")
    if "api_url" not in red:
        logger.warning("Falta 'api_url' en configuracion, usando default")


def _crear_componente_socket(factory, tipo, nombre_puerto):
    """Crea un componente inyectando host/puerto si el tipo es 'socket'."""
    if tipo == "socket":
        return factory.crear(
            tipo,
            host=Configurador.obtener_host_escucha(),
            puerto=Configurador.obtener_puerto(nombre_puerto)
        )
    return factory.crear(tipo)


def _crear_visualizador(factory, tipo, nombre_puerto):
    """Crea un visualizador con soporte para tipos 'socket', 'api' y 'archivo'."""
    if tipo == "socket":
        return factory.crear(
            tipo,
            host=Configurador.obtener_host_escucha(),
            puerto=Configurador.obtener_puerto(nombre_puerto)
        )
    api_url = Configurador.obtener_api_url() if tipo == "api" else None
    return factory.crear(tipo, api_url=api_url)


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
        Configurador.configuracion_termostato = _cargar_json(_buscar_config(config_paths))
        Configurador._validar_configuracion()

    @staticmethod
    def configurar_proxy_bateria():
        """Crea y retorna el proxy de bateria segun configuracion."""
        tipo = Configurador.configuracion_termostato["proxy_bateria"]
        return _crear_componente_socket(FactoryProxyBateria, tipo, "bateria")

    @staticmethod
    def configurar_proxy_temperatura():
        """Crea y retorna el proxy de sensor de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["proxy_sensor_temperatura"]
        return _crear_componente_socket(FactoryProxySensorTemperatura, tipo, "temperatura")

    @staticmethod
    def configurar_actuador_climatizador():
        """Crea y retorna el actuador de climatizador segun configuracion."""
        tipo = Configurador.configuracion_termostato["actuador_climatizador"]
        return FactoryActuadorClimatizador.crear(tipo)

    @staticmethod
    def configurar_visualizador_temperatura():
        """Crea y retorna el visualizador de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_temperatura"]
        return _crear_visualizador(FactoryVisualizadorTemperatura, tipo, "visualizador_temperatura")

    @staticmethod
    def configurar_visualizador_bateria():
        """Crea y retorna el visualizador de bateria segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_bateria"]
        return _crear_visualizador(FactoryVisualizadorBateria, tipo, "visualizador_bateria")

    @staticmethod
    def configurar_visualizador_climatizador():
        """Crea y retorna el visualizador de climatizador segun configuracion."""
        tipo = Configurador.configuracion_termostato["visualizador_climatizador"]
        return _crear_visualizador(FactoryVisualizadorClimatizador, tipo, "visualizador_climatizador")

    @staticmethod
    def configurar_climatizador():
        """Crea y retorna el climatizador con histeresis segun configuracion."""
        tipo = Configurador.configuracion_termostato["climatizador"]
        return FactoryClimatizador.crear(tipo, histeresis=Configurador.obtener_histeresis())

    @staticmethod
    def configurar_selector_temperatura():
        """Crea y retorna el selector de temperatura segun configuracion."""
        tipo = Configurador.configuracion_termostato["selector_temperatura"]
        return _crear_componente_socket(FactorySelectorTemperatura, tipo, "selector_temperatura")

    @staticmethod
    def configurar_seteo_temperatura():
        """Crea y retorna el componente de seteo de temperatura segun config."""
        tipo = Configurador.configuracion_termostato["seteo_temperatura"]
        return _crear_componente_socket(FactorySeteoTemperatura, tipo, "seteo_temperatura")

    @staticmethod
    def obtener_host_escucha():
        """Retorna el host donde escuchar conexiones socket."""
        config = Configurador.configuracion_termostato
        return config.get("red", {}).get("host_escucha", "localhost")

    @staticmethod
    def obtener_puerto(nombre_sensor):
        """Retorna el puerto para un sensor especifico."""
        config = Configurador.configuracion_termostato
        puertos = config.get("red", {}).get("puertos", _PUERTOS_DEFAULT)
        return puertos.get(nombre_sensor, _PUERTOS_DEFAULT.get(nombre_sensor))

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
        _verificar_claves_requeridas(config)
        _verificar_configuracion_red(config.get("red"))
