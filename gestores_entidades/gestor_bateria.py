"""
Es el componente responsable de mantener y gestionar el
estado interno de la clase que representa la bateria real
"""

from agentes_sensores.proxy_bateria import *
from agentes_actuadores.visualizador_bateria import *
from entidades.bateria import *


class GestorBateria:

    def __init__(self, hal_adc=None):
        """
        Inicializa el gestor de batería

        :param hal_adc: Opcional, permite inyectar implementación HAL específica
                        Si es None, ProxyBateria usará HAL simulado por defecto

        Composición:
        - Bateria: entidad de dominio que guarda el estado
        - ProxyBateria: boundary que obtiene la carga desde el sensor vía HAL
        - VisualizadorBateria: boundary que expone visualmente el estado
        """
        self._bateria = Bateria()

        # Permite inyectar HAL desde fuera (útil para testing y producción)
        if hal_adc is not None:
            self._proxy_bateria = ProxyBateria(hal_adc)
        else:
            # Usa HAL simulado por defecto
            self._proxy_bateria = ProxyBateria()

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