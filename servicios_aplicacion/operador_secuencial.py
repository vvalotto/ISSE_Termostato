"""
Es la clase responsable de orquestar de manera ciclica
la lectura de los dispositivos externos y el accionamiento
del climatizador de acuerdo al seteo de la temperatura
ambiente.
Las responsbilidades específicas son delegadas a los gestores
y procesos correspondientes
"""

import time
from os import system
from servicios_aplicacion.selector_entrada import *
from servicios_aplicacion.presentador import *


class OperadorSecuencial:

    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        """
        Arma la dependencia con las clases con las que va
        a trabajar
        """
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador
        self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)

    def ejecutar(self):

        print("Inicio")

        self._gestor_ambiente.ambiente.temperatura_deseada = 24

        'Ciclo infinito que establece la secuencia de acciones' \
        'del termostato'

        while True:
            print("lee_bateria")

            self._gestor_bateria.verificar_nivel_de_carga()
            time.sleep(1)

            print("lee temperatura")
            self._gestor_ambiente.leer_temperatura_ambiente()
            time.sleep(1)

            print("revisa selector de temperatura")
            self._selector.ejecutar()
            time.sleep(1)

            print("acciona climatizador")
            self._gestor_climatizador.accionar_climatizador(self._gestor_ambiente.ambiente)
            time.sleep(1)

            print("Muestra estado del termostato")
            self._presentador.ejecutar()
            time.sleep(5)

            system("clear")
        # FIN DEL BUCLE
