"""
Proxy del sensor de temperatura
Usa la capa HAL para abstraer el acceso al hardware
Convierte valores ADC a temperatura en °C
"""
from hal.hal_adc import HAL_ADC
from hal.hal_adc_simulado import HAL_ADC_Simulado


class ProxySensorTemperatura:
    """
    Proxy para lectura de sensor de temperatura

    Responsabilidades:
    - Abstraer la lectura del sensor mediante HAL
    - Convertir valores ADC a temperatura en °C
    - Validar rangos de temperatura
    - Lanzar excepciones en caso de error
    """

    # Configuración del sensor
    PIN_SENSOR_TEMPERATURA = 0  # Canal ADC donde está conectado el sensor

    # Parámetros de conversión ADC → Temperatura
    # Mapeo lineal: ADC 150 = 0°C, ADC 400 = 50°C
    ADC_OFFSET = 150
    ADC_ESCALA = 5.0  # unidades ADC por °C

    # Rango válido de temperatura
    TEMP_MIN = -10  # °C
    TEMP_MAX = 50   # °C

    def __init__(self, hal: HAL_ADC = None):
        """
        Inicializa el proxy del sensor

        :param hal: Implementación del HAL ADC
                    Si es None, usa HAL_ADC_Simulado por defecto
        """
        self._hal = hal if hal is not None else HAL_ADC_Simulado()
        self._hal.inicializar()

    def leer_temperatura(self) -> int:
        """
        Lee temperatura desde el sensor mediante HAL

        Proceso:
        1. Lee valor ADC mediante HAL
        2. Convierte ADC a temperatura usando fórmula de calibración
        3. Valida que esté en rango físicamente posible
        4. Retorna temperatura en °C

        :return: Temperatura en °C (int)
        :raises Exception: Si hay error de lectura o valor fuera de rango
        """
        try:
            # 1. Lee valor del ADC mediante HAL
            valor_adc = self._hal.leer_adc(self.PIN_SENSOR_TEMPERATURA)

            # 2. Convierte ADC a temperatura
            # Fórmula: temp = (adc - offset) / escala
            temperatura = (valor_adc - self.ADC_OFFSET) / self.ADC_ESCALA
            temperatura = int(temperatura)

            # 3. Valida rango
            if temperatura < self.TEMP_MIN or temperatura > self.TEMP_MAX:
                raise Exception(
                    f"Temperatura fuera de rango válido: {temperatura}°C "
                    f"(válido: {self.TEMP_MIN}-{self.TEMP_MAX}°C)"
                )

            return temperatura

        except IOError as e:
            # Error de hardware (sensor no responde)
            raise Exception("Error de Lectura de Sensor") from e

    def __del__(self):
        """Destructor: libera recursos del HAL"""
        if hasattr(self, '_hal'):
            self._hal.finalizar()
