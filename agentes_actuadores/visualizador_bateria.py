""""
Muestra los valores de carga de la Bateria
Clase dummy que simula la visualizacion de los parametros
"""
import socket
from entidades.abs_visualizador_bateria import *


class VisualizadorBateria(AbsVisualizadorBateria):

    @staticmethod
    def mostrar_tension(tension_bateria):
        print(str(tension_bateria))
        return

    @staticmethod
    def mostrar_indicador(indicador_bateria):
        print(str(indicador_bateria))
        return


class VisualizadorBateriaSocket(AbsVisualizadorBateria):

    def mostrar_tension(self, tension_bateria):

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14000)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(tension_bateria).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    def mostrar_indicador(self, indicador_bateria):

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 13005)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(str(indicador_bateria).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")
