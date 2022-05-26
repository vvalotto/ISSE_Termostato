"""
Es el componente responsable de mantener y gestionar el
estado interno de la clase que representa el climatizador real
"""

from entidades.climatizador import *
# from agentes_actuadores.visualizador_climatizador import *
from agentes_actuadores.actuador_climatizador import *
from servicios_dominio.controlador_climatizador import *


class GestorClimatizador:

    def __init__(self):
        self._climatizador = Climatizador()
        self._actuador = ActuadorClimatizador()
        # self._visualizador = VisualizadorClimatizador()

    def accionar_climatizador(self, ambiente):
        accion = self._definir_accion(ambiente)
        if accion is not None:
            self._actuador.accionar_climatizador(accion)
            self._climatizador.proximo_estado(accion)

    def obtener_estado_climatizador(self):
        return self._climatizador.estado

    def mostrar_estado_climatizador(self):
        # self._visualizador.mostrar_estado_climatizador(self._climatizador.estado)
        pass

    def _definir_accion(self, ambiente):
        accion = None
        temperatura = ControladorTemperatura.comparar_temperatura(ambiente.temperatura_ambiente, ambiente.temperatura_deseada)
        if temperatura == "alta":
            if self._climatizador.estado == "apagado":
                accion = "enfriar"
            elif self._climatizador.estado == "calentando":
                accion = "apagar"
            else:
                accion = None
        if temperatura == "baja":
            if self._climatizador.estado == "apagado":
                accion = "calentar"
            elif self._climatizador.estado == "enfriando":
                accion = "apagar"
            else:
                accion = None
        print('accion:', accion)
        return accion
