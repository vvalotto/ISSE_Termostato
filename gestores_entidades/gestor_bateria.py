"""
Gestor de Bateria - Orquestador de operaciones sobre la bateria.

Este modulo contiene el gestor responsable de coordinar las operaciones
relacionadas con la bateria del sistema: lectura de nivel de carga,
calculo de indicador de estado, y visualizacion del estado de bateria.

Patron de Diseno:
    - Facade: Simplifica la interaccion con multiples componentes
    - Controller (GRASP): Coordina casos de uso relacionados a la bateria

Responsabilidades:
    - Leer nivel de carga desde proxy de bateria
    - Gestionar el estado de la entidad Bateria
    - Coordinar visualizacion del nivel e indicador de bateria
"""

# Las dependencias se inyectan en el constructor (Dependency Injection)


class GestorBateria:
    """
    Orquestador de operaciones sobre la bateria del sistema.

    Coordina la interaccion entre el proxy de bateria, la entidad
    Bateria, y el visualizador de bateria. Actua como Facade para
    simplificar las operaciones de bateria para las capas superiores.

    Attributes:
        _bateria (Bateria): Entidad de dominio con estado de la bateria.
        _proxy_bateria: Proxy para lectura de carga de bateria.
        _visualizador_bateria: Componente de visualizacion de bateria.
    """

    def __init__(self, bateria, proxy_bateria, visualizador_bateria):
        """
        Inicializa el gestor de bateria.

        Args:
            bateria (Bateria): Entidad de dominio que representa la bateria.
            proxy_bateria (AbsProxyBateria): Proxy para leer carga de bateria.
            visualizador_bateria (AbsVisualizadorBateria): Visualizador de bateria.
        """
        self._bateria = bateria
        self._proxy_bateria = proxy_bateria
        self._visualizador_bateria = visualizador_bateria

    def verificar_nivel_de_carga(self):
        """
        Lee el nivel de carga actual y actualiza la entidad Bateria.

        Obtiene la carga desde el proxy de bateria y la almacena
        en la entidad, lo que automaticamente actualiza el indicador.
        """
        self._bateria.nivel_de_carga = self._proxy_bateria.leer_carga()

    def obtener_nivel_de_carga(self):
        """
        Obtiene el nivel de carga actual de la bateria.

        Returns:
            float: Nivel de carga de la bateria.
        """
        return self._bateria.nivel_de_carga

    def obtener_indicador_de_carga(self):
        """
        Obtiene el indicador de estado de la bateria.

        Returns:
            str: Indicador de estado ("BAJA" o "NORMAL").
        """
        return self._bateria.indicador

    def mostrar_nivel_de_carga(self):
        """Muestra el nivel de carga actual en el visualizador."""
        self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)

    def mostrar_indicador_de_carga(self):
        """Muestra el indicador de estado de bateria en el visualizador."""
        self._visualizador_bateria.mostrar_indicador(self._bateria.indicador)
