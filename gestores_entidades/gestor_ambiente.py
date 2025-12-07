"""
Gestor de Ambiente - Orquestador de operaciones sobre el ambiente.

Este modulo contiene el gestor responsable de coordinar las operaciones
relacionadas con el ambiente a climatizar: lectura de temperatura desde
sensores, gestion de temperatura deseada, y visualizacion de temperaturas.

Patron de Diseno:
    - Facade: Simplifica la interaccion con multiples componentes
    - Controller (GRASP): Coordina casos de uso relacionados al ambiente

Responsabilidades:
    - Leer temperatura ambiente desde proxy de sensor
    - Gestionar temperatura deseada (aumentar/disminuir)
    - Coordinar visualizacion de temperaturas
    - Controlar que temperatura se muestra (ambiente vs deseada)
"""

# Las dependencias se inyectan en el constructor (Dependency Injection)


class GestorAmbiente:
    """
    Orquestador de operaciones sobre el ambiente a climatizar.

    Coordina la interaccion entre el sensor de temperatura, la entidad
    Ambiente, y el visualizador de temperatura. Actua como Facade para
    simplificar las operaciones de temperatura para las capas superiores.

    Attributes:
        _ambiente (Ambiente): Entidad de dominio con estado del ambiente.
        _proxy_sensor_temperatura: Proxy para lectura de temperatura.
        _visualizador_temperatura: Componente de visualizacion.
    """

    @property
    def ambiente(self):
        """Ambiente: Entidad de dominio que representa el ambiente."""
        return self._ambiente

    def __init__(self, ambiente, proxy_sensor, visualizador, incremento_temperatura=1):
        """
        Inicializa el gestor de ambiente.

        Args:
            ambiente (Ambiente): Entidad de dominio que representa el ambiente.
            proxy_sensor (AbsProxySensorTemperatura): Proxy para leer temperatura.
            visualizador (AbsVisualizadorTemperatura): Visualizador de temperatura.
            incremento_temperatura (float): Incremento para ajustar temperatura
                                           deseada. Por defecto 1 grado.
        """
        self._ambiente = ambiente
        self._proxy_sensor_temperatura = proxy_sensor
        self._visualizador_temperatura = visualizador
        self._incremento_temperatura = incremento_temperatura

    def leer_temperatura_ambiente(self):
        """
        Lee la temperatura actual del sensor y actualiza el ambiente.

        Obtiene la temperatura desde el proxy del sensor y la almacena
        en la entidad Ambiente. Si ocurre un error de lectura (sensor
        desconectado, timeout, valor invalido), establece la temperatura
        como None para indicar lectura no disponible.

        Excepciones manejadas:
            - OSError: Error de comunicacion con el sensor (I/O, conexion)
            - ValueError: Valor de temperatura invalido o fuera de rango
            - TimeoutError: Timeout en la lectura del sensor
        """
        try:
            temperatura = self._proxy_sensor_temperatura.leer_temperatura()
            self._ambiente.temperatura_ambiente = temperatura
        except (OSError, ValueError, TimeoutError):
            self._ambiente.temperatura_ambiente = None

    def obtener_temperatura_ambiente(self):
        """
        Obtiene la temperatura ambiente actual.

        Returns:
            float: Temperatura ambiente en grados Celsius, o None si no hay lectura.
        """
        return self._ambiente.temperatura_ambiente

    def mostrar_temperatura_ambiente(self):
        """Muestra la temperatura ambiente actual en el visualizador."""
        temperatura = self._ambiente.temperatura_ambiente
        self._visualizador_temperatura.mostrar_temperatura_ambiente(temperatura)

    def aumentar_temperatura_deseada(self):
        """
        Aumenta la temperatura deseada segun el incremento configurado.

        Suma el valor de incremento a la temperatura deseada actual.
        """
        self._ambiente.temperatura_deseada += self._incremento_temperatura

    def disminuir_temperatura_deseada(self):
        """
        Disminuye la temperatura deseada segun el incremento configurado.

        Resta el valor de incremento de la temperatura deseada actual.
        """
        self._ambiente.temperatura_deseada -= self._incremento_temperatura

    def obtener_temperatura_deseada(self):
        """
        Obtiene la temperatura deseada actual.

        Returns:
            float: Temperatura deseada (setpoint) en grados Celsius.
        """
        return self._ambiente.temperatura_deseada

    def mostrar_temperatura_deseada(self):
        """Muestra la temperatura deseada actual en el visualizador."""
        temperatura = self._ambiente.temperatura_deseada
        self._visualizador_temperatura.mostrar_temperatura_deseada(temperatura)

    def mostrar_temperatura(self):
        """
        Muestra la temperatura segun el modo de visualizacion configurado.

        Si el modo es "ambiente", muestra la temperatura ambiente.
        Si el modo es "deseada", muestra la temperatura deseada.
        """
        if self._ambiente.temperatura_a_mostrar == "ambiente":
            temperatura = self._ambiente.temperatura_ambiente
            self._visualizador_temperatura.mostrar_temperatura_ambiente(temperatura)
        elif self._ambiente.temperatura_a_mostrar == "deseada":
            temperatura = self._ambiente.temperatura_deseada
            self._visualizador_temperatura.mostrar_temperatura_deseada(temperatura)

    def indicar_temperatura_a_mostrar(self, tipo_temperatura):
        """
        Configura que temperatura debe mostrarse en el visualizador.

        Args:
            tipo_temperatura (str): Tipo de temperatura a mostrar.
                                   Valores validos: "ambiente", "deseada".
        """
        self.ambiente.temperatura_a_mostrar = tipo_temperatura
