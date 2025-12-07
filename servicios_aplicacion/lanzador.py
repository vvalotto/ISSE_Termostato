"""
Clase que inicializa el termostato.

Este modulo contiene el Lanzador, punto de entrada principal del sistema.
Aqui se realiza la composicion de dependencias (Composition Root) donde
se crean todas las instancias y se inyectan a los componentes que las necesitan.

Patron de Diseno:
    - Composition Root: Punto unico donde se ensamblan las dependencias
    - Dependency Injection: Las dependencias se inyectan en los constructores
"""
from gestores_entidades.gestor_bateria import GestorBateria
from gestores_entidades.gestor_ambiente import GestorAmbiente
from gestores_entidades.gestor_climatizador import GestorClimatizador
from servicios_aplicacion.operador_paralelo import OperadorParalelo
from servicios_aplicacion.inicializador import Inicializador
from servicios_aplicacion.presentador import Presentador
from configurador.configurador import Configurador
from entidades.ambiente import Ambiente
from entidades.bateria import Bateria


class Lanzador:
    """
    Punto de entrada principal del sistema de termostato.

    Actua como Composition Root donde se ensamblan todas las dependencias
    del sistema. Crea las entidades, proxies, visualizadores y gestores,
    inyectando las dependencias en cada componente.
    """

    def __init__(self):
        """
        Inicializa el sistema creando y ensamblando todos los componentes.

        Obtiene la configuracion desde el Configurador, crea las entidades
        de dominio, los proxies y visualizadores, y los inyecta en los
        gestores correspondientes.
        """
        # Crear dependencias para GestorBateria
        carga_maxima = Configurador.obtener_carga_maxima_bateria()
        umbral = Configurador.obtener_umbral_bateria()
        bateria = Bateria(carga_maxima, umbral)
        proxy_bateria = Configurador().configurar_proxy_bateria()
        visualizador_bateria = Configurador.configurar_visualizador_bateria()

        self._gestor_bateria = GestorBateria(
            bateria=bateria,
            proxy_bateria=proxy_bateria,
            visualizador_bateria=visualizador_bateria
        )

        # Crear dependencias para GestorAmbiente
        temperatura_inicial = Configurador.obtener_temperatura_inicial()
        ambiente = Ambiente(temperatura_deseada_inicial=temperatura_inicial)
        proxy_sensor = Configurador.configurar_proxy_temperatura()
        visualizador_temperatura = Configurador().configurar_visualizador_temperatura()
        incremento = Configurador.obtener_incremento_temperatura()

        self._gestor_ambiente = GestorAmbiente(
            ambiente=ambiente,
            proxy_sensor=proxy_sensor,
            visualizador=visualizador_temperatura,
            incremento_temperatura=incremento
        )

        # Crear dependencias para GestorClimatizador
        climatizador = Configurador.configurar_climatizador()
        actuador = Configurador.configurar_actuador_climatizador()
        visualizador_climatizador = Configurador.configurar_visualizador_climatizador()

        self._gestor_climatizador = GestorClimatizador(
            climatizador=climatizador,
            actuador=actuador,
            visualizador=visualizador_climatizador
        )

        # Crear presentador y operador
        self._presentador = Presentador(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._gestor_climatizador)
        self._operador = OperadorParalelo(self._gestor_bateria,
                                          self._gestor_ambiente,
                                          self._gestor_climatizador)

    def ejecutar(self):

        todo_ok = Inicializador.iniciar(self._gestor_bateria,
                                        self._gestor_ambiente,
                                        self._presentador)

        if todo_ok:
            print("Entra en operacion")
            self._operador.ejecutar()
