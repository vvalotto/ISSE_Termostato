""""
Muestra los valores del estado del climatizador
Clase dummy que simula la visualizacion de los parametros
"""
import socket
from entidades.abs_visualizador_climatizador import *
import requests


class VisualizadorClimatizador(AbsVisualizadorClimatizador):

    @staticmethod
    def mostrar_estado_climatizador(estado_climatizador):
        print(str(estado_climatizador))
        return


class VisualizadorClimatizadorSocket(AbsVisualizadorClimatizador):

    @staticmethod
    def mostrar_estado_climatizador(self, estado_climatizador):

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14002)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(estado_climatizador).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")


class VisualizadorClimatizadorWebApi(AbsVisualizadorClimatizador):

    @staticmethod
    def mostrar_estado_climatizador(estado_climatizador):
        try:
            url_server = "http://0.0.0.0:5001/termostato/estado_climatizador/"
            dato = {'climatizador' : str(estado_climatizador)}
            respuesta = requests.post(url_server, json=dato)
        except ConnectionError:
            print("Intentar de vuelta")