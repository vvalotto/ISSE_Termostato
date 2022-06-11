"""
Clase para realizar el registro de auditoria y excepciones
"""

from abc import abstractmethod


class AbsRegistrador:

    @staticmethod
    @abstractmethod
    def registrar_error(registro):
        pass


class AbsAuditor:
    @staticmethod
    @abstractmethod
    def auditar_funcion(registro):
        pass
