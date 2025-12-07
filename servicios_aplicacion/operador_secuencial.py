"""
Operador secuencial del termostato.

Este modulo contiene el orquestador que ejecuta las operaciones del
termostato de manera secuencial en un ciclo infinito.

Patron de Diseno:
    - Controller (GRASP): Coordina el flujo de operaciones del sistema
"""
import time
from os import system
from servicios_aplicacion.selector_entrada import SelectorEntradaTemperatura
from servicios_aplicacion.presentador import Presentador


# pylint: disable=too-few-public-methods
class OperadorSecuencial:
    """
    Orquestador secuencial de operaciones del termostato.

    Ejecuta las operaciones de lectura de sensores, ajuste de temperatura
    y accionamiento del climatizador en un ciclo secuencial.

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

    def ejecutar(self):
        """
        Ejecuta el ciclo principal del termostato.

        Ciclo infinito que lee sensores, procesa entradas del usuario,
        acciona el climatizador y muestra el estado del sistema.
        """
        print("Inicio")
        self._gestor_ambiente.ambiente.temperatura_deseada = 24

        # Ciclo infinito de operaciones del termostato
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
