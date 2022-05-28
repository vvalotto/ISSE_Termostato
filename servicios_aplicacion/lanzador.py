"""
Clase que inicializa el termostato
"""
from servicios_aplicacion.operador_secuencial import *


class Lanzador:

    def __init__(self):
        self._gestor_bateria = GestorBateria()
        self._gestor_ambiente = GestorAmbiente()
        self._gestor_climatizador = GestorClimatizador()
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)

    def ejecutar(self):

        todo_ok = True
        print("inicio")

        self._gestor_ambiente.ambiente.temperatura_deseada = 24
        print("lee_bateria")
        self._gestor_bateria.verificar_nivel_de_carga()
        if self._gestor_bateria.obtener_indicador_de_carga() != "NORMAL": todo_ok = False

        print("lee temperatura")
        self._gestor_ambiente.leer_temperatura_ambiente()
        if self._gestor_ambiente.obtener_temperatura_ambiente() is None: todo_ok = False

        print("Muestra estado")
        self._presentador.ejecutar()

        if todo_ok:
            print("Entre en operacion")
            OperadorSecuencial().ejecutar()
