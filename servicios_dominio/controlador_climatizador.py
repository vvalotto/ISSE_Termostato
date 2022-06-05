"""
Servicio del dominio porque es el algoritmo para identificar
que siente el dueño de casa respecto de la temperatura deseada
"""


class ControladorTemperatura:

    histeris = 2

    @staticmethod
    def comparar_temperatura(temperatura_actual, temperatura_deseada):
        temperatura = "normal"
        limite_superior = temperatura_deseada + ControladorTemperatura.histeris
        limite_inferior = temperatura_deseada - ControladorTemperatura.histeris
        if (limite_superior < temperatura_actual): temperatura = "alta"
        if (limite_inferior > temperatura_actual): temperatura = "baja"
        return temperatura
