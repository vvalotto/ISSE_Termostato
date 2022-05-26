"""
Clase que simula el accionamiento del climatizador.
Aqui la acción es escribir en un archivo externo
"""


class ActuadorClimatizador:

    @staticmethod
    def accionar_climatizador(accion):

        # Simula Actuador
        archivo_climatizador = open("climatizador", "w")
        archivo_climatizador.write(accion)
        archivo_climatizador.close()
        return
