"""
Servicio de dominio para control de temperatura.

Este modulo contiene la logica de negocio para comparar temperaturas
y determinar el estado termico del ambiente (alta, baja, normal).

Patron de Diseno:
    - Service: Encapsula logica de dominio sin estado
    - Strategy: El algoritmo de comparacion puede variar
    - DIP: Recibe histeresis como parametro (inyeccion de dependencias)
"""


# pylint: disable=too-few-public-methods
class ControladorTemperatura:
    """
    Servicio de dominio para comparacion de temperaturas.

    Implementa el algoritmo de histeresis para determinar si la
    temperatura actual esta por encima, por debajo o dentro del
    rango aceptable respecto a la temperatura deseada.

    La histeresis evita oscilaciones frecuentes del climatizador
    al crear una "zona muerta" alrededor de la temperatura deseada.

    Example:
        >>> ControladorTemperatura.comparar_temperatura(25, 22, histeresis=2)
        'alta'  # 25 > 22+2=24
        >>> ControladorTemperatura.comparar_temperatura(22, 22, histeresis=2)
        'normal'  # 20 <= 22 <= 24
    """

    @staticmethod
    def comparar_temperatura(temperatura_actual, temperatura_deseada, histeresis=2):
        """
        Compara la temperatura actual con la deseada usando histeresis.

        Args:
            temperatura_actual (float): Temperatura ambiente en grados Celsius.
            temperatura_deseada (float): Temperatura objetivo en grados Celsius.
            histeresis (float): Margen de tolerancia en grados. Por defecto 2.

        Returns:
            str: "alta", "baja" o "normal" segun la comparacion.
        """
        limite_superior = temperatura_deseada + histeresis
        limite_inferior = temperatura_deseada - histeresis

        if temperatura_actual > limite_superior:
            return "alta"
        if temperatura_actual < limite_inferior:
            return "baja"
        return "normal"
