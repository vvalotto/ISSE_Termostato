"""
Selector de entrada de temperatura.

Este modulo contiene la clase responsable de gestionar la entrada
del usuario para establecer la temperatura deseada.

Patron de Diseno:
    - Controller (GRASP): Coordina la interaccion de seteo de temperatura
"""
from configurador.configurador import Configurador


# pylint: disable=too-few-public-methods
class SelectorEntradaTemperatura:
    """
    Selector para establecer la temperatura deseada.

    Gestiona la interaccion con el usuario para ajustar la temperatura
    deseada del sistema, procesando comandos de aumentar/disminuir.

    Attributes:
        _seteo_temperatura: Componente para obtener comandos de seteo.
        _selector_temperatura: Selector de modo de visualizacion.
        _gestor_ambiente: Gestor de ambiente para aplicar cambios.
    """

    def __init__(self, gestor_ambiente):
        """
        Inicializa el selector con el gestor de ambiente.

        Args:
            gestor_ambiente: Gestor de ambiente para aplicar cambios.
        """
        self._seteo_temperatura = Configurador.configurar_seteo_temperatura()
        self._selector_temperatura = Configurador.configurar_selector_temperatura()
        self._gestor_ambiente = gestor_ambiente

    def ejecutar(self):
        """
        Ejecuta el ciclo de seteo de temperatura.

        Mientras el selector este en modo "deseada", muestra la temperatura
        deseada y procesa los comandos del usuario para ajustarla.
        """
        while self._selector_temperatura.obtener_selector() == "deseada":
            self._mostrar_temperatura_deseada()
            self._obtener_seteo_temperatura_deseada()
        self._gestor_ambiente.indicar_temperatura_a_mostrar("ambiente")

    def _mostrar_temperatura_deseada(self):
        """Muestra la temperatura deseada en el visualizador."""
        self._gestor_ambiente.indicar_temperatura_a_mostrar("deseada")
        self._gestor_ambiente.mostrar_temperatura()

    def _obtener_seteo_temperatura_deseada(self):
        """Obtiene y procesa el comando de seteo del usuario."""
        opcion = self._seteo_temperatura.obtener_seteo()

        if opcion is None:
            return

        if opcion == "aumentar":
            self._gestor_ambiente.aumentar_temperatura_deseada()
        elif opcion == "disminuir":
            self._gestor_ambiente.disminuir_temperatura_deseada()
