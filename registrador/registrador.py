"""
Clase Abstract para realizar el registro de auditoria y excepciones
Cada uno especializa la manera de regisrar
"""

from abc import abstractmethod


class AbsRegistrador:

    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        pass

    @staticmethod
    @abstractmethod
    def auditar_funcion(registro):
        pass
