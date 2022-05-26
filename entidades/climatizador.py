""""
Clase que respresenta el climatizador
"""


class Climatizador:

    @property
    def estado(self):
        return self.__estado

    def __init__(self):
        self.__estado = "apagado"
        self.__maquina_estado = []
        self.__inicializar_maquina_estado()

    def proximo_estado(self, accion):
        estado_actual = [self.__estado, accion]

        for transicion in self.__maquina_estado:
            if estado_actual == transicion[0]:
                self.__estado = transicion[1]
                return self.__estado
        raise "No existe proximo estado"

    def __inicializar_maquina_estado(self):
        self.__maquina_estado.append([["apagado", "calentar"], "calentando"])
        self.__maquina_estado.append([["apagado", "enfriar"], "enfriando"])
        self.__maquina_estado.append([["calentando", "apagar"], "apagado"])
        self.__maquina_estado.append([["enfriando", "apagar"], "apagado"])
