"""
Implementación simulada del HAL ADC
Simula lecturas de sensores con valores realistas y ruido
Reemplaza el uso de archivos por generación dinámica de valores
"""
import random
from .hal_adc import HAL_ADC


class HAL_ADC_Simulado(HAL_ADC):
    """
    Simula un ADC con ruido y variación realista

    Características:
    - Resolución: 10 bits (0-1023)
    - Simula sensor de temperatura: rango aproximado 15-30°C
    - Agrega ruido gaussiano para simular condiciones reales
    - Puede simular fallos de lectura (configurable)
    """

    # Constantes de simulación
    RESOLUCION_BITS = 10
    VALOR_MAX = (1 << RESOLUCION_BITS) - 1  # 2^10 - 1 = 1023

    def __init__(self,
                 temperatura_base: float = 22.0,
                 ruido_std: float = 0.5,
                 probabilidad_fallo: float = 0.0):
        """
        Inicializa el HAL simulado

        :param temperatura_base: Temperatura base en °C para simulación
        :param ruido_std: Desviación estándar del ruido en °C
        :param probabilidad_fallo: Probabilidad de fallo (0.0-1.0)
        """
        self._temperatura_base = temperatura_base
        self._ruido_std = ruido_std
        self._probabilidad_fallo = probabilidad_fallo
        self._inicializado = False

        # Simula deriva lenta de temperatura (ciclos térmicos)
        self._deriva = 0.0

    def inicializar(self) -> None:
        """Simula inicialización del ADC"""
        if self._inicializado:
            return

        print("[HAL_ADC_Simulado] Inicializando ADC simulado...")
        print(f"[HAL_ADC_Simulado] Resolución: {self.RESOLUCION_BITS} bits (0-{self.VALOR_MAX})")
        print(f"[HAL_ADC_Simulado] Temperatura base: {self._temperatura_base}°C")

        self._inicializado = True

    def leer_adc(self, canal: int) -> int:
        """
        Simula lectura del ADC con ruido realista

        Fórmula de conversión asumida:
        - Temperatura 0°C  → ADC = 150
        - Temperatura 50°C → ADC = 400
        - Aproximadamente 5 unidades ADC por °C

        :param canal: Canal a leer (0-7, según típico MCP3008)
        :return: Valor ADC (0-1023)
        :raises IOError: Si ADC no inicializado o fallo simulado
        """
        # Validaciones
        if not self._inicializado:
            raise IOError("ADC no inicializado. Llamar inicializar() primero.")

        if canal < 0 or canal > 7:
            raise IOError(f"Canal {canal} inválido. Debe estar entre 0-7.")

        # Simula fallo ocasional
        if random.random() < self._probabilidad_fallo:
            raise IOError(f"Fallo de lectura simulado en canal {canal}")

        # Simula deriva térmica lenta
        self._deriva += random.gauss(0, 0.01)
        self._deriva = max(-2.0, min(2.0, self._deriva))  # Limita deriva

        # Calcula temperatura simulada
        temp_actual = self._temperatura_base + self._deriva
        temp_con_ruido = temp_actual + random.gauss(0, self._ruido_std)

        # Convierte temperatura a valor ADC
        # Mapeo lineal: temp (°C) → adc
        # 0°C = 150, 50°C = 400
        valor_adc = 150 + int(temp_con_ruido * 5.0)

        # Limita a rango válido del ADC
        valor_adc = max(0, min(self.VALOR_MAX, valor_adc))

        print(f"[HAL_ADC_Simulado] Canal {canal}: ADC={valor_adc} "
              f"(~{temp_con_ruido:.1f}°C, deriva={self._deriva:.2f}°C)")

        return valor_adc

    def finalizar(self) -> None:
        """Simula limpieza de recursos"""
        if not self._inicializado:
            return

        print("[HAL_ADC_Simulado] Finalizando ADC simulado...")
        self._inicializado = False
        self._deriva = 0.0

    def obtener_resolucion(self) -> int:
        """Retorna la resolución del ADC simulado"""
        return self.RESOLUCION_BITS
