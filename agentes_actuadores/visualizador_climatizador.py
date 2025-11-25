""""
Muestra los valores del estado del climatizador
Clase dummy que simula la visualizacion de los parametros
"""
import socket
import requests
from entidades.abs_visualizador_climatizador import *


class VisualizadorClimatizador(AbsVisualizadorClimatizador):

    @staticmethod
    def mostrar_estado_climatizador(estado_climatizador):
        print(str(estado_climatizador))
        return


class VisualizadorClimatizadorSocket(AbsVisualizadorClimatizador):

    def mostrar_estado_climatizador(self, estado_climatizador):

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14002)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(estado_climatizador).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

class VisualizadorClimatizadorApi(AbsVisualizadorClimatizador):

    def mostrar_estado_climatizador(self, estado_climatizador):
        from configurador.configurador import Configurador
        api_url = Configurador.obtener_api_url()
        try:
            requests.post("{}/termostato/estado_climatizador".format(api_url),
                         json={"climatizador": estado_climatizador},
                         timeout=5)
        except requests.RequestException as e:
            print("Error al enviar estado climatizador: {}".format(e))