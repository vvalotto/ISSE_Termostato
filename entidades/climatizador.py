"""
Entidades Climatizador - Sistema de control de temperatura.

Este modulo define las entidades de dominio para el control de climatizacion,
incluyendo la clase abstracta AbsClimatizador que generaliza el comportamiento
comun, y sus implementaciones concretas: Climatizador (calefaccion + refrigeracion)
y Calefactor (solo calefaccion).

Patrones de Diseno Aplicados:
    - Template Method: evaluar_accion() define el algoritmo comun,
      _definir_accion() permite variaciones en subclases.
    - State Machine: Gestiona transiciones de estado (apagado/calentando/enfriando)
      usando diccionario para O(1) lookup.

Responsabilidades:
    - Gestionar el estado del climatizador (apagado/calentando/enfriando)
    - Evaluar acciones necesarias basadas en temperatura ambiente vs deseada
    - Validar transiciones de estado segun maquina de estados
    - Definir comportamiento especifico por tipo (climatizador vs calefactor)
"""
from abc import ABCMeta, abstractmethod
from servicios_dominio.controlador_climatizador import ControladorTemperatura


class AbsClimatizador(metaclass=ABCMeta):
    """
    Clase abstracta base para dispositivos de climatizacion.

    Generaliza el comportamiento comun de todos los dispositivos que
    modifican la temperatura del ambiente (climatizadores, calefactores, etc.).

    Implementa una maquina de estados finitos para gestionar transiciones
    validas entre estados (apagado, calentando, enfriando) y aplica el
    patron Template Method para definir el flujo de evaluacion de acciones.

    Attributes:
        estado (str): Estado actual del dispositivo.
                     Valores: "apagado", "calentando", "enfriando".

    Design Patterns:
        - Template Method: evaluar_accion() es el template method.
        - State Machine: Transiciones gestionadas via diccionario.

    Note:
        Las subclases deben implementar:
        - _inicializar_maquina_estado(): Define transiciones validas
        - _definir_accion(): Logica especifica para determinar accion
    """
    @property
    def estado(self):
        """str: Estado actual del climatizador (apagado/calentando/enfriando)."""
        return self._estado

    def __init__(self, histeresis=2):
        """
        Inicializa el climatizador en estado apagado.

        Crea la estructura de la maquina de estados (diccionario vacio)
        y delega a la subclase la definicion de transiciones validas
        via _inicializar_maquina_estado().

        Args:
            histeresis (float): Margen de tolerancia en grados para la
                               comparacion de temperatura. Por defecto 2.
        """
        self._estado = "apagado"
        self._histeresis = histeresis
        self._transiciones = {}
        self._inicializar_maquina_estado()

    def proximo_estado(self, accion):
        """
        Ejecuta una transicion de estado basada en la accion dada.

        Args:
            accion (str): Accion a ejecutar ("calentar", "enfriar", "apagar").

        Returns:
            str: Nuevo estado del climatizador despues de la transicion.

        Raises:
            ValueError: Si la transicion (estado_actual, accion) no es valida.

        Example:
            >>> clima = Climatizador()
            >>> clima.proximo_estado("calentar")
            'calentando'
            >>> clima.proximo_estado("apagar")
            'apagado'
        """
        clave = (self._estado, accion)
        if clave not in self._transiciones:
            mensaje = "Transicion no valida: estado={}, accion={}"
            raise ValueError(mensaje.format(self._estado, accion))
        self._estado = self._transiciones[clave]
        return self._estado

    @abstractmethod
    def _inicializar_maquina_estado(self):
        """
        Inicializa el diccionario de transiciones de estado.

        Este metodo abstracto debe ser implementado por cada subclase
        para definir que transiciones de estado son validas.

        El diccionario debe tener la estructura:
            {(estado_origen, accion): estado_destino}

        Example:
            self._transiciones = {
                ("apagado", "calentar"): "calentando",
                ("calentando", "apagar"): "apagado",
            }
        """

    def evaluar_accion(self, ambiente):
        """
        Evalua que accion tomar basada en el estado del ambiente (Template Method).

        Este metodo implementa el patron Template Method, definiendo el
        algoritmo comun para evaluar acciones:
        1. Comparar temperatura ambiente vs deseada
        2. Delegar a _definir_accion() la decision especifica

        Args:
            ambiente (Ambiente): Estado actual del ambiente con temperaturas.

        Returns:
            str: Accion a ejecutar ("calentar", "enfriar", "apagar", None).

        Note:
            Este es el template method que define el flujo de evaluacion.
            Las subclases customizann via _definir_accion().
        """
        temperatura = ControladorTemperatura.comparar_temperatura(
            ambiente.temperatura_ambiente,
            ambiente.temperatura_deseada,
            self._histeresis
        )
        return self._definir_accion(temperatura)

    @abstractmethod
    def _definir_accion(self, temperatura):
        """
        Define la accion basada en la comparacion de temperatura (Hook Method).

        Este metodo abstracto (hook method del Template Method) debe
        ser implementado por cada subclase para definir su logica
        especifica de decision de acciones.

        Args:
            temperatura (str): Resultado de comparacion de temperatura.
                             Valores: "alta", "baja", "normal".

        Returns:
            str: Accion a ejecutar ("calentar", "enfriar", "apagar", None).

        Note:
            Este es el hook method que permite variacion en el algoritmo
            definido por evaluar_accion() (template method).
        """


class Climatizador(AbsClimatizador):
    """
    Climatizador completo con capacidad de calefaccion y refrigeracion.

    Implementacion concreta de AbsClimatizador que puede tanto calentar
    como enfriar el ambiente. Implementa una maquina de estados con 3 estados
    (apagado, calentando, enfriando) y 4 transiciones validas.

    Este dispositivo es ideal para control total de temperatura en ambientes
    que requieren tanto calefaccion en invierno como refrigeracion en verano.

    Estados posibles:
        - apagado: Dispositivo sin accionar
        - calentando: Modo calefaccion activo
        - enfriando: Modo refrigeracion activo

    Transiciones validas:
        - (apagado, calentar) -> calentando
        - (apagado, enfriar) -> enfriando
        - (calentando, apagar) -> apagado
        - (enfriando, apagar) -> apagado

    Logica de decision:
        - Temperatura alta + apagado -> enfriar
        - Temperatura alta + calentando -> apagar (evitar desperdiciar energia)
        - Temperatura baja + apagado -> calentar
        - Temperatura baja + enfriando -> apagar (evitar desperdiciar energia)
        - Temperatura normal -> None (sin accion)

    Example:
        >>> clima = Climatizador()
        >>> ambiente = Ambiente(temperatura_deseada_inicial=22)
        >>> ambiente.temperatura_ambiente = 25  # Temperatura alta
        >>> accion = clima.evaluar_accion(ambiente)
        >>> accion
        'enfriar'
        >>> clima.proximo_estado(accion)
        'enfriando'
    """
    def _inicializar_maquina_estado(self):
        self._transiciones = {
            ("apagado", "calentar"): "calentando",
            ("apagado", "enfriar"): "enfriando",
            ("calentando", "apagar"): "apagado",
            ("enfriando", "apagar"): "apagado",
        }

    def _definir_accion(self, temperatura):
        """Determina la accion basada en temperatura y estado actual"""
        decisiones = {
            ("alta", "apagado"): "enfriar",
            ("alta", "calentando"): "apagar",
            ("baja", "apagado"): "calentar",
            ("baja", "enfriando"): "apagar",
        }
        return decisiones.get((temperatura, self._estado), None)


class Calefactor(AbsClimatizador):
    """
    Calefactor con capacidad unicamente de calefaccion.

    Implementacion concreta de AbsClimatizador que solo puede calentar
    el ambiente. No tiene capacidad de refrigeracion. Implementa una
    maquina de estados con 2 estados (apagado, calentando) y 3 transiciones.

    Este dispositivo es ideal para ambientes que solo requieren calefaccion
    y no necesitan refrigeracion, optimizando costos y complejidad del sistema.

    Estados posibles:
        - apagado: Dispositivo sin accionar
        - calentando: Modo calefaccion activo

    Transiciones validas:
        - (apagado, calentar) -> calentando
        - (apagado, enfriar) -> apagado (sin efecto, no tiene capacidad de enfriamiento)
        - (calentando, apagar) -> apagado

    Logica de decision:
        - Temperatura baja + apagado -> calentar
        - Temperatura normal + calentando -> apagar (temperatura alcanzada)
        - Temperatura alta + calentando -> apagar (temperatura excedida)
        - Otras combinaciones -> None (sin accion)

    Note:
        A diferencia del Climatizador, este dispositivo ignora solicitudes
        de enfriamiento (accion "enfriar") ya que no tiene esa capacidad.
        La transicion (apagado, enfriar) mantiene el estado apagado.
    """
    def _inicializar_maquina_estado(self):
        self._transiciones = {
            ("apagado", "calentar"): "calentando",
            ("apagado", "enfriar"): "apagado",
            ("calentando", "apagar"): "apagado",
        }

    def _definir_accion(self, temperatura):
        """Determina la accion basada en temperatura y estado actual"""
        decisiones = {
            ("baja", "apagado"): "calentar",
            ("normal", "calentando"): "apagar",
            ("alta", "calentando"): "apagar",
        }
        return decisiones.get((temperatura, self._estado), None)
