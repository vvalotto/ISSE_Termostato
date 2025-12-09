""""
Muestra los valores del estado del climatizador
Clase dummy que simula la visualizacion de los parametros
"""
import socket
import requests
from entidades.abs_visualizador_climatizador import AbsVisualizadorClimatizador


# pylint: disable=too-few-public-methods
class VisualizadorClimatizador(AbsVisualizadorClimatizador):
    """
    Visualizador de climatizador que imprime en consola.

    Implementa la interfaz AbsVisualizadorClimatizador mostrando
    el estado del climatizador por salida estandar.

    Patron de Diseno:
        - Presenter: Presenta estado del climatizador al usuario
    """

    def mostrar_estado_climatizador(self, estado_climatizador):
        """
        Muestra el estado del climatizador en consola.

        Args:
            estado_climatizador: Estado actual del climatizador.
        """
        print(str(estado_climatizador))


# pylint: disable=too-few-public-methods
class VisualizadorClimatizadorSocket(AbsVisualizadorClimatizador):
    """
    Visualizador de climatizador via socket TCP.

    Implementa la interfaz AbsVisualizadorClimatizador enviando
    el estado a un servidor remoto via socket.

    Patron de Diseno:
        - Proxy: Envia datos a visualizador remoto
    """

    def mostrar_estado_climatizador(self, estado_climatizador):
        """
        Envia el estado del climatizador via socket TCP.

        Args:
            estado_climatizador: Estado actual del climatizador.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14002)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(estado_climatizador).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")


# pylint: disable=too-few-public-methods
class VisualizadorClimatizadorApi(AbsVisualizadorClimatizador):
    """
    Visualizador de climatizador via API REST.

    Implementa la interfaz AbsVisualizadorClimatizador enviando
    el estado a una API REST mediante peticiones HTTP POST.

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

    def mostrar_estado_climatizador(self, estado_climatizador):
        """
        Envia el estado del climatizador a la API REST.

        Args:
            estado_climatizador: Estado actual del climatizador.
        """
        try:
            requests.post("{}/termostato/estado_climatizador".format(self._api_url),
                         json={"climatizador": estado_climatizador},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar estado climatizador: {}".format(e))
