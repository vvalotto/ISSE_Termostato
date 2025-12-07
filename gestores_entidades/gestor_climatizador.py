"""
Gestor de Climatizador - Orquestador de operaciones sobre el climatizador.

Este modulo contiene el gestor responsable de coordinar las operaciones
relacionadas con el climatizador: evaluacion de acciones de control,
accionamiento del dispositivo fisico, y visualizacion del estado.

Patron de Diseno:
    - Facade: Simplifica la interaccion con multiples componentes
    - Controller (GRASP): Coordina casos de uso relacionados al climatizador

Responsabilidades:
    - Evaluar acciones necesarias basadas en temperatura ambiente vs deseada
    - Accionar el climatizador fisico mediante el actuador
    - Gestionar transiciones de estado del climatizador
    - Coordinar visualizacion del estado del climatizador
"""

class GestorClimatizador:
    """
    Orquestador de operaciones sobre el climatizador del sistema.

    Coordina la interaccion entre el climatizador (entidad de dominio),
    el actuador (proxy de hardware), y el visualizador. Actua como Facade
    para simplificar las operaciones de climatizacion para las capas superiores.

    Attributes:
        _climatizador (AbsClimatizador): Entidad climatizador o calefactor.
        _actuador: Proxy para accionar el climatizador fisico.
        _visualizador: Componente de visualizacion de estado.
    """

    def __init__(self, climatizador, actuador, visualizador):
        """
        Inicializa el gestor de climatizador.

        Args:
            climatizador (AbsClimatizador): Entidad climatizador o calefactor.
            actuador (AbsProxyActuadorClimatizador): Actuador para accionar
                                                     el climatizador fisico.
            visualizador (AbsVisualizadorClimatizador): Visualizador de estado.
        """
        self._climatizador = climatizador
        self._actuador = actuador
        self._visualizador = visualizador

    def accionar_climatizador(self, ambiente):
        """
        Evalua y ejecuta la accion necesaria sobre el climatizador.

        Compara la temperatura ambiente con la deseada, determina si
        se requiere alguna accion (calentar, enfriar, apagar), y si es
        necesario, acciona el dispositivo fisico y actualiza el estado.

        Args:
            ambiente (Ambiente): Entidad con temperaturas ambiente y deseada.
        """
        accion = self._climatizador.evaluar_accion(ambiente)
        if accion is not None:
            self._actuador.accionar_climatizador(accion)
            self._climatizador.proximo_estado(accion)

    def obtener_estado_climatizador(self):
        """
        Obtiene el estado actual del climatizador.

        Returns:
            str: Estado actual ("apagado", "calentando", "enfriando").
        """
        return self._climatizador.estado

    def mostrar_estado_climatizador(self):
        """Muestra el estado actual del climatizador en el visualizador."""
        self._visualizador.mostrar_estado_climatizador(self._climatizador.estado)
