"""
Presentador del sistema de termostato.

Este modulo contiene la clase responsable de mostrar los parametros
del sistema al usuario (bateria, temperatura, climatizador).

Patron de Diseno:
    - Facade: Simplifica la visualizacion de multiples componentes
"""


# pylint: disable=too-few-public-methods
class Presentador:
    """
    Presentador de parametros del sistema.

    Coordina la visualizacion de los parametros de bateria, temperatura
    y climatizador en la interfaz de usuario.

    Attributes:
        _gestor_bateria: Gestor de bateria para mostrar nivel e indicador.
        _gestor_ambiente: Gestor de ambiente para mostrar temperatura.
        _gestor_climatizador: Gestor de climatizador para mostrar estado.
    """

    def __init__(self, gestor_bateria, gestor_ambiente, gestor_climatizador):
        """
        Inicializa el presentador con los gestores necesarios.

        Args:
            gestor_bateria: Gestor de bateria.
            gestor_ambiente: Gestor de ambiente.
            gestor_climatizador: Gestor de climatizador.
        """
        self._gestor_bateria = gestor_bateria
        self._gestor_ambiente = gestor_ambiente
        self._gestor_climatizador = gestor_climatizador

    def ejecutar(self):
        """Muestra todos los parametros del sistema en consola."""
        print("-------------- BATERIA -------------")
        self._gestor_bateria.mostrar_nivel_de_carga()
        self._gestor_bateria.mostrar_indicador_de_carga()
        print("------------------------------------")
        print("\n")
        print("------------ TEMPERATURA ----------")
        self._gestor_ambiente.mostrar_temperatura()
        print("------------------------------------")
        print("\n")
        print("------------ CLIMATIZADOR ----------")
        self._gestor_climatizador.mostrar_estado_climatizador()
        print("------------------------------------")
        print("\n")
