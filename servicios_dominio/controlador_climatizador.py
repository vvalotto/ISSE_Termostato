"""
Servicio del dominio porque es el algoritmo para identificar
que siente el dueño de casa respecto de la temperatura deseada
"""


class ControladorTemperatura:

    @staticmethod
    def comparar_temperatura(temperatura_actual, temperatura_deseada):
        """
        Compara la temperatura actual con la deseada usando histéresis.

        Args:
            temperatura_actual: Temperatura ambiente en grados Celsius
            temperatura_deseada: Temperatura objetivo en grados Celsius

        Returns:
            str: "alta" si está muy caliente, "baja" si está muy fría, "normal" si está dentro del rango
        """
        from configurador.configurador import Configurador

        # Obtener histéresis desde configuración
        histeris = Configurador.obtener_histeresis()

        temperatura = "normal"
        limite_superior = temperatura_deseada + histeris
        limite_inferior = temperatura_deseada - histeris
        if (limite_superior < temperatura_actual): temperatura = "alta"
        if (limite_inferior > temperatura_actual): temperatura = "baja"
        return temperatura
