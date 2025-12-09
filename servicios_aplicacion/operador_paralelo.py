"""
Operador paralelo del termostato.

Este modulo contiene el orquestador que ejecuta las operaciones del
termostato de manera concurrente usando hilos (threads).

Patron de Diseno:
    - Controller (GRASP): Coordina el flujo de operaciones del sistema
    - Active Object: Cada operacion corre en su propio hilo
"""
# pylint: disable=duplicate-code
# La inicializacion es similar a operador_secuencial (patron comun aceptable)

import time
import threading

from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador


class OperadorParalelo:
    """
    Orquestador paralelo de operaciones del termostato.

    Ejecuta las operaciones de lectura de sensores, ajuste de temperatura
    y accionamiento del climatizador en hilos separados para operacion
    concurrente.

    Attributes:
        _gestor_bateria: Gestor de operaciones de bateria.
        _gestor_ambiente: Gestor de operaciones de ambiente.
        _gestor_climatizador: Gestor de operaciones de climatizador.
    """

    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        """
        Inicializa el operador con los gestores necesarios.

        Args:
            gestor_bateria: Gestor de bateria.
            gestor_ambiente: Gestor de ambiente.
            gestor_climatizador: Gestor de climatizador.
        """
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador
        self._selector = SelectorEntradaTemperatura(self._gestor_ambiente)
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)

    def lee_carga_bateria(self):
        """Lee periodicamente la carga de bateria (cada 1 segundo)."""
        while True:
            print("lee_bateria")
            self._gestor_bateria.verificar_nivel_de_carga()
            time.sleep(1)

    def lee_temperatura_ambiente(self):
        """Lee periodicamente la temperatura ambiente (cada 2 segundos)."""
        while True:
            print("lee temperatura")
            self._gestor_ambiente.leer_temperatura_ambiente()
            time.sleep(2)

    def acciona_climatizador(self):
        """Acciona periodicamente el climatizador (cada 5 segundos)."""
        while True:
            print("acciona climatizador")
            self._gestor_climatizador.accionar_climatizador(
                self._gestor_ambiente.ambiente
            )
            time.sleep(5)

    def muestra_parametros(self):
        """Muestra periodicamente los parametros del sistema (cada 5 segundos)."""
        while True:
            self._presentador.ejecutar()
            time.sleep(5)

    def setea_temperatura(self):
        """Procesa periodicamente el seteo de temperatura (cada 5 segundos)."""
        while True:
            print("ve si setea temperatura")
            self._selector.ejecutar()
            time.sleep(5)

    def ejecutar(self):
        """
        Inicia todos los hilos de operacion del termostato.

        Crea e inicia 5 hilos para: lectura de bateria, lectura de
        temperatura, accionamiento de climatizador, visualizacion
        y seteo de temperatura.
        """
        print("inicio")

        hilos = [
            threading.Thread(target=self.lee_carga_bateria),
            threading.Thread(target=self.lee_temperatura_ambiente),
            threading.Thread(target=self.acciona_climatizador),
            threading.Thread(target=self.muestra_parametros),
            threading.Thread(target=self.setea_temperatura),
        ]

        for hilo in hilos:
            hilo.start()
