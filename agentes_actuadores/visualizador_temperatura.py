"""
Clase responsable de sacar el dato de las temperaturas a un visualizador.

Clase dummy que simula la visualizacion de los parametros.
"""
# pylint: disable=duplicate-code
# El codigo de socket es similar entre visualizadores (patron comun aceptable)

import socket
import requests
from entidades.abs_visualizador_temperatura import AbsVisualizadorTemperatura


class VisualizadorTemperatura(AbsVisualizadorTemperatura):
    """
    Visualizador de temperatura que imprime en consola.

    Implementa la interfaz AbsVisualizadorTemperatura mostrando
    las temperaturas ambiente y deseada por salida estandar.

    Patron de Diseno:
        - Presenter: Presenta datos de temperatura al usuario
    """

    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        """
        Muestra la temperatura ambiente en consola.

        Args:
            temperatura_ambiente: Valor de temperatura ambiente.
        """
        print(str(temperatura_ambiente))

    def mostrar_temperatura_deseada(self, temperatura_deseada):
        """
        Muestra la temperatura deseada en consola.

        Args:
            temperatura_deseada: Valor de temperatura deseada.
        """
        print(str(temperatura_deseada))


class VisualizadorTemperaturaSocket(AbsVisualizadorTemperatura):
    """
    Visualizador de temperatura via socket TCP.

    Implementa la interfaz AbsVisualizadorTemperatura enviando
    los datos a un servidor remoto via socket.

    Patron de Diseno:
        - Proxy: Envia datos a visualizador remoto
    """

    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        """
        Envia la temperatura ambiente via socket TCP.

        Args:
            temperatura_ambiente: Valor de temperatura ambiente.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("ambiente: " + str(temperatura_ambiente)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    def mostrar_temperatura_deseada(self, temperatura_deseada):
        """
        Envia la temperatura deseada via socket TCP.

        Args:
            temperatura_deseada: Valor de temperatura deseada.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("deseada: " + str(temperatura_deseada)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")


class VisualizadorTemperaturaApi(AbsVisualizadorTemperatura):
    """
    Visualizador de temperatura via API REST.

    Implementa la interfaz AbsVisualizadorTemperatura enviando
    los datos a una API REST mediante peticiones HTTP POST.

    Patron de Diseno:
        - Adapter: Adapta la visualizacion a protocolo HTTP
        - DIP: Recibe api_url via inyeccion de dependencias

    Args:
        api_url: URL base de la API REST.
    """

    def __init__(self, api_url):
        """
        Inicializa el visualizador con la URL de la API.

        Args:
            api_url: URL base de la API REST.
        """
        self._api_url = api_url

    def mostrar_temperatura_ambiente(self, temperatura_ambiente):
        """
        Envia la temperatura ambiente a la API REST.

        Args:
            temperatura_ambiente: Valor de temperatura ambiente.
        """
        try:
            requests.post("{}/termostato/temperatura_ambiente".format(self._api_url),
                         json={"ambiente": int(temperatura_ambiente)},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar temperatura ambiente: {}".format(e))

    def mostrar_temperatura_deseada(self, temperatura_deseada):
        """
        Envia la temperatura deseada a la API REST.

        Args:
            temperatura_deseada: Valor de temperatura deseada.
        """
        try:
            requests.post("{}/termostato/temperatura_deseada".format(self._api_url),
                         json={"deseada": int(temperatura_deseada)},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar temperatura deseada: {}".format(e))
