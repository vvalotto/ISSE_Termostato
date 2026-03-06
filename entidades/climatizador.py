"""
Implementaciones concretas de dispositivos de climatizacion.

Este modulo contiene las clases concretas Climatizador y Calefactor,
que implementan la interfaz AbsClimatizador definida en abs_climatizador.py.

Patrones de Diseno Aplicados:
    - Template Method: _definir_accion() es el hook method especifico.
    - State Machine: Transiciones definidas en _inicializar_maquina_estado().
"""
from entidades.abs_climatizador import AbsClimatizador


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
