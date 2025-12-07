"""
Inicializador del sistema de termostato.

Este modulo contiene la clase responsable de inicializar el sistema,
verificando que los sensores esten operativos antes de comenzar.
"""
from os import system


# pylint: disable=too-few-public-methods
class Inicializador:
    """
    Inicializador del sistema de termostato.

    Verifica que la bateria y el sensor de temperatura esten operativos
    antes de permitir que el sistema entre en operacion normal.
    """

    @staticmethod
    def iniciar(gestor_bateria, gestor_ambiente, presentador):
        """
        Inicializa el sistema verificando sensores.

        Args:
            gestor_bateria: Gestor de bateria.
            gestor_ambiente: Gestor de ambiente.
            presentador: Presentador para mostrar estado inicial.

        Returns:
            bool: True si la inicializacion fue exitosa, False si fallo.
        """
        print("INICIO")
        gestor_ambiente.ambiente.temperatura_deseada = 24

        print("lee_bateria")
        gestor_bateria.verificar_nivel_de_carga()
        if gestor_bateria.obtener_indicador_de_carga() != "NORMAL":
            return False

        print("lee temperatura")
        gestor_ambiente.leer_temperatura_ambiente()
        if gestor_ambiente.obtener_temperatura_ambiente() is None:
            return False

        print("Muestra estado Termostato")
        presentador.ejecutar()

        system("clear")
        return True
