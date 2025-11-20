"""
Mock del HAL ADC para testing
Permite inyectar valores predefinidos para pruebas deterministas
"""
from typing import List, Optional
from .hal_adc import HAL_ADC


class HAL_ADC_Mock(HAL_ADC):
    """
    Mock del HAL ADC que retorna valores predefinidos

    Útil para testing donde se necesitan valores específicos
    y comportamiento determinista.
    """

    def __init__(self, valores_adc: Optional[List[int]] = None):
        """
        :param valores_adc: Lista de valores a retornar en cada llamada
                            Si None, retorna siempre 200 (aprox 10°C)
        """
        self._valores_adc = valores_adc if valores_adc else [200]
        self._indice_lectura = 0
        self._inicializado = False
        self._llamadas_leer = 0

    def inicializar(self) -> None:
        """Mock de inicialización"""
        self._inicializado = True
        self._indice_lectura = 0
        self._llamadas_leer = 0

    def leer_adc(self, canal: int) -> int:
        """
        Retorna el siguiente valor de la lista predefinida

        :param canal: Canal a leer (ignorado en mock)
        :return: Siguiente valor de la lista
        :raises IOError: Si no está inicializado
        """
        if not self._inicializado:
            raise IOError("ADC no inicializado")

        # Obtiene valor actual y avanza índice (circular)
        valor = self._valores_adc[self._indice_lectura % len(self._valores_adc)]
        self._indice_lectura += 1
        self._llamadas_leer += 1

        return valor

    def finalizar(self) -> None:
        """Mock de finalización"""
        self._inicializado = False

    def obtener_resolucion(self) -> int:
        """Retorna resolución simulada de 10 bits"""
        return 10

    # Métodos adicionales para testing

    def obtener_llamadas_leer(self) -> int:
        """Retorna el número de veces que se llamó leer_adc()"""
        return self._llamadas_leer

    def configurar_valores(self, valores: List[int]) -> None:
        """Permite reconfigurar los valores durante el test"""
        self._valores_adc = valores
        self._indice_lectura = 0

    def simular_fallo(self) -> None:
        """Configura el mock para lanzar IOError en próxima lectura"""
        self._valores_adc = []  # Lista vacía causará IndexError → IOError
