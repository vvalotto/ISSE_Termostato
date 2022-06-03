"""

"""

import time
import threading


from gestores_entidades.gestor_bateria import *
from gestores_entidades.gestor_ambiente import *
from gestores_entidades.gestor_climatizador import *
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *


class OperadorParalelo:

    def __init__(self):
        self._gestor_bateria = GestorBateria("socket")
        self._gestor_ambiente = GestorAmbiente()
        self._gestor_climatizador = GestorClimatizador()
        self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)

    def lee_carga_bateria(self):
        while True:
            print("lee_bateria")
            self._gestor_bateria.verificar_nivel_de_carga()
            time.sleep(1)

    def lee_temperatura_ambiente(self):
        while True:
            print("lee temperatura")
            self._gestor_ambiente.leer_temperatura_ambiente()
            self._gestor_ambiente.ambiente.temperatura_deseada = 25
            time.sleep(2)

    def acciona_climatizador(self):
        while True:
            print("acciona climatizador")
            self._gestor_climatizador.accionar_climatizador(self._gestor_ambiente.ambiente)
            time.sleep(5)

    def muestra_parametros(self):
        while True:
            self._presentador.ejecutar()
            time.sleep(5)

    def setea_temperatura(self):
        while True:
            print("ve si setea temperatura")
            self._selector.ejecutar()
            time.sleep(5)

    def ejecutar(self):

        print("inicio")

        t1 = threading.Thread(target=self.lee_carga_bateria)

        t2 = threading.Thread(target=self.lee_temperatura_ambiente)

        t3 = threading.Thread(target=self.acciona_climatizador)

        t4 = threading.Thread(target=self.muestra_parametros)

        t5 = threading.Thread(target=self.setea_temperatura)

        t1.start()
        t2.start()
        t3.start()
        time.sleep(1)
        t4.start()
        time.sleep(5)
        t5.start()


