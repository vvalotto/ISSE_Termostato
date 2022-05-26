"""
Clase que simula el cambio de la temperatura deseada
"""


class SeteoTemperatura:

    @staticmethod
    def obtener_seteo():
        opcion = "0"
        while opcion not in ["1", "2"]:
            opcion = input(">")
        diferencia = "aumentar" if opcion == "1" else "disminuir"
        return diferencia

