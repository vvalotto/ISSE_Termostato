"""
Clase que define que componentes se usaran
"""

from agentes_sensores.proxy_bateria import *


class Configurador:

    def configurar_proxy_bateria(self):
        return ProxyBateriaSocket()
