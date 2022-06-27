"""
Clase responsable de sacar el dato de las temperaturas
a un visualizador
Clase dummy
"""
import socket
from entidades.abs_visualizador_temperatura import *
import requests
import json

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
            direccion_servidor = ("localhost", 14001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("ambiente: " + str(temperatura_ambiente)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")

    @staticmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ("localhost", 14001)
            cliente.connect(direccion_servidor)

            cliente.send(bytes(("deseada: " + str(temperatura_deseada)).encode()))
            cliente.close()
        except ConnectionError:
            print("Intentar de vuelta")


class VisualizadorTemperaturaWebApi(AbsVisualizadorTemperatura):

    @staticmethod
    def mostrar_temperatura_ambiente(temperatura_ambiente):
        try:
            url_server = "http://0.0.0.0:5050/termostato/temperatura_ambiente/"
            dato = {'ambiente' : str(temperatura_ambiente)}
            respuesta = requests.post(url_server, json=dato)
        except ConnectionError:
            print("Intentar de vuelta")

    @staticmethod
    def mostrar_temperatura_deseada(temperatura_deseada):
        try:
            url_server = "http://0.0.0.0:5050/termostato/temperatura_deseada/"
            dato = {'deseada': str(temperatura_deseada)}
            respuesta = requests.post(url_server, json=dato)
        except ConnectionError:
            print("Intentar de vuelta")