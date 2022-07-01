""""
Clase que respresenta el climatizador
"""
from abc import ABCMeta, abstractmethod
from servicios_dominio.controlador_climatizador import *


class AbsClimatizador(metaclass=ABCMeta):
    """
    Clase Abstracta Climatizador que generaliza el comportamiento
    de los posibles dispositivo que sirven para cambiar la temperatura
    de un ambiente
    """
    @property
    def estado(self):
        return self._estado

    def __init__(self):
        self._estado = "apagado"
        self._maquina_estado = []
        self._inicializar_maquina_estado()

    def proximo_estado(self, accion):
        estado_actual = [self._estado, accion]

        for transicion in self._maquina_estado:
            if estado_actual == transicion[0]:
                self._estado = transicion[1]
                return self._estado
        raise 'No existe proximo estado'

    @abstractmethod
    def _inicializar_maquina_estado(self):
        pass

    @abstractmethod
    def evaluar_accion(self, ambiente):
        pass

    @abstractmethod
    def _definir_accion(self, temperatura):
        pass


class Climatizador(AbsClimatizador):
    """
    Clase climatizador: calienta y enfria el ambiente
    """
    def _inicializar_maquina_estado(self):
        self._maquina_estado.append([["apagado", "calentar"], "calentando"])
        self._maquina_estado.append([["apagado", "enfriar"], "enfriando"])
        self._maquina_estado.append([["calentando", "apagar"], "apagado"])
        self._maquina_estado.append([["enfriando", "apagar"], "apagado"])

    def evaluar_accion(self, ambiente):
        temperatura = ControladorTemperatura.comparar_temperatura(ambiente.temperatura_ambiente,
                                                                  ambiente.temperatura_deseada)
        accion = self._definir_accion(temperatura)
        return accion

    def _definir_accion(self, temperatura):
        accion = None
        if temperatura == "alta":
            if self._estado == "apagado":
                accion = "enfriar"
            elif self._estado == "calentando":
                accion = "apagar"

        if temperatura == "baja":
            if self._estado == "apagado":
                accion = "calentar"
            elif self._estado == "enfriando":
                accion = "apagar"

        print('accion:', accion)
        return accion


class Calefactor(AbsClimatizador):
    """
    Calefactor
    """
    def evaluar_accion(self, ambiente):
        temperatura = ControladorTemperatura.comparar_temperatura(ambiente.temperatura_ambiente,
                                                                  ambiente.temperatura_deseada)
        accion = self._definir_accion(temperatura)
        return accion

    def _inicializar_maquina_estado(self):
        self._maquina_estado.append([["apagado", "calentar"], "calentando"])
        self._maquina_estado.append([["apagado", "enfriar"], "apagado"])
        self._maquina_estado.append([["calentando", "apagar"], "apagado"])

    def _definir_accion(self, temperatura):
        accion = None
        if temperatura == "baja":
            if self._estado == "apagado":
                accion = "calentar"
        else:
            if self._estado == "calentando":
                accion = "apagar"
        print('accion:', accion)
        return accion
