"""
Clase que inicializa el termostato
"""
from gestores_entidades.gestor_bateria import *
from gestores_entidades.gestor_ambiente import *
from gestores_entidades.gestor_climatizador import *
from servicios_aplicacion.operador_paralelo import *
from servicios_aplicacion.inicializador import *
from os import system


class Lanzador:

    def __init__(self):
        self._gestor_bateria = GestorBateria()
        self._gestor_ambiente = GestorAmbiente()
        self._gestor_climatizador = GestorClimatizador()
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)
        self._operador = OperadorParalelo()

    def ejecutar(self):

        todo_ok = Inicializador.iniciar(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._presentador)

        if todo_ok:
            print("Entra en operacion")
            self._operador.ejecutar()
