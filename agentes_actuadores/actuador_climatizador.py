"""
Clase que simula el accionamiento del climatizador.
Aqui la acción es escribir en un archivo externo
"""

from registrador.registrador import *
import datetime


class ActuadorClimatizador:

    @staticmethod
    def accionar_climatizador(accion):

        # Simula Actuador
        mensaje_accion = "accionando el climatizador"
        Registrador.auditar_funcion(ActuadorClimatizador.__name__,
                                    mensaje_accion,
                                    str(datetime.datetime.now()))
        try:
            with open("climatizador", "w") as archivo_climatizador:
                archivo_climatizador.write(accion)
                archivo_climatizador.close()
        except IOError:
            mensaje_error = "Error al quierer actuar en el climatizador"
            Registrador.registrar_error(ActuadorClimatizador.__name__,
                                        ActuadorClimatizador.accionar_climatizador.__name__,
                                        str(datetime.datetime.now()),
                                        str(IOError),
                                        mensaje_error)
            raise mensaje_error
        return
