"""
Es el componente responsable de mantener y gestionar el
estado interno de la clase que representa la bateria real
"""

from agentes_sensores.proxy_bateria import *
from agentes_actuadores.visualizador_bateria import *
from entidades.bateria import *


class GestorBateria:

    def __init__(self, tipo_proxy):
        """
        Inicializa el gestor que esta compuesto de:
        La clase que que obtiene la carga de la bateria desde la interfaz
        la clase que guarda el estado de la bateria
        la clase que expone visualmente el estado de la bateria
        """
        self._bateria = Bateria()

        # Se cambia el constructor!!!!
        if tipo_proxy == "archivo":
            self._proxy_bateria = ProxyBateria()
        elif tipo_proxy == "socket":
            self._proxy_bateria = ProxyBateriaSocket()
        self._visualizador_bateria = VisualizadorBateria()

    def verificar_nivel_de_carga(self):
        self._bateria.nivel_de_carga = self._proxy_bateria.leer_carga()

    def obtener_nivel_de_carga(self):
        return self._bateria.nivel_de_carga

    def obtener_indicador_de_carga(self):
        return self._bateria.indicador

    def mostrar_nivel_de_carga(self):
        self._visualizador_bateria.mostrar_tension(self._bateria.nivel_de_carga)
        pass

    def mostrar_indicador_de_carga(self):
        self._visualizador_bateria.mostrar_indicador(self._bateria.indicador)
        pass