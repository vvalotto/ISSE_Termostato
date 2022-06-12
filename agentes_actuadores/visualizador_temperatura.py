"""
Clase responsable de sacar el dato de las temperaturas
a un visualizador
Clase dummy
"""
import socket
from entidades.abs_visualizador_temperatura import *


class VisualizadorTemperatura(AbsVisualizadorTemperatura):

    @staticmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        print(str(temperatura_ambiente))
        return

    @staticmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        print(str(temperatura_deseada))
        return


class VisualizadorTemperaturaSocket(AbsVisualizadorTemperatura):

    @staticmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 13001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("ambiente: " + str(temperatura_ambiente)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    @staticmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 13001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("deseada: " + str(temperatura_deseada)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")
