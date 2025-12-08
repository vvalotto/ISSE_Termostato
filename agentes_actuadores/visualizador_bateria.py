""""
Muestra los valores de carga de la Bateria
Clase dummy que simula la visualizacion de los parametros
"""
import socket
import requests

from entidades.abs_visualizador_bateria import AbsVisualizadorBateria


class VisualizadorBateria(AbsVisualizadorBateria):
    """
    Visualizador de bateria que imprime en consola.

    Implementa la interfaz AbsVisualizadorBateria mostrando
    la tension e indicador de bateria por salida estandar.

    Patron de Diseno:
        - Presenter: Presenta datos de bateria al usuario
    """

    @staticmethod
    def mostrar_tension(tension_bateria):
        """
        Muestra la tension de la bateria en consola.

        Args:
            tension_bateria: Valor de tension a mostrar.
        """
        print(str(tension_bateria))

    @staticmethod
    def mostrar_indicador(indicador_bateria):
        """
        Muestra el indicador de bateria en consola.

        Args:
            indicador_bateria: Valor del indicador a mostrar.
        """
        print(str(indicador_bateria))


class VisualizadorBateriaSocket(AbsVisualizadorBateria):
    """
    Visualizador de bateria via socket TCP.

    Implementa la interfaz AbsVisualizadorBateria enviando
    los datos a un servidor remoto via socket.

    Patron de Diseno:
        - Proxy: Envia datos a visualizador remoto
    """

    def mostrar_tension(self, tension_bateria):
        """
        Envia la tension de la bateria via socket TCP.

        Args:
            tension_bateria: Valor de tension a enviar.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14000)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(tension_bateria).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    def mostrar_indicador(self, indicador_bateria):
        """
        Envia el indicador de bateria via socket TCP.

        Args:
            indicador_bateria: Valor del indicador a enviar.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 13005)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(indicador_bateria).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")


class VisualizadorBateriaApi(AbsVisualizadorBateria):
    """
    Visualizador de bateria via API REST.

    Implementa la interfaz AbsVisualizadorBateria enviando
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

    def mostrar_tension(self, tension_bateria):
        """
        Envia la tension de la bateria a la API REST.

        Args:
            tension_bateria: Valor de tension a enviar.
        """
        try:
            requests.post("{}/termostato/bateria".format(self._api_url),
                         json={"bateria": tension_bateria},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar tensión batería: {}".format(e))

    def mostrar_indicador(self, indicador_bateria):
        """
        Envia el indicador de bateria a la API REST.

        Args:
            indicador_bateria: Valor del indicador a enviar.
        """
        try:
            requests.post("{}/termostato/indicador".format(self._api_url),
                         json={"indicador": indicador_bateria},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar indicador batería: {}".format(e))
