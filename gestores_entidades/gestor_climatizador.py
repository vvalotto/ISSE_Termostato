"""
Es el componente responsable de mantener y gestionar el
estado interno de la clase que representa el climatizador real
"""

from configurador.configurador import *


class GestorClimatizador:

    def __init__(self):
        self._climatizador = Configurador.configurar_climatizador()
        self._actuador = Configurador.configurar_actuador_climatizador()
        self._visualizador = Configurador.configurar_visualizador_climatizador()

    def accionar_climatizador(self, ambiente):
        accion = self._climatizador.evaluar_accion(ambiente)
        if accion is not None:
            self._actuador.accionar_climatizador(accion)
            self._climatizador.proximo_estado(accion)

    def obtener_estado_climatizador(self):
        return self._climatizador.estado

    def mostrar_estado_climatizador(self):
        self._visualizador.mostrar_estado_climatizador(self._climatizador.estado)
