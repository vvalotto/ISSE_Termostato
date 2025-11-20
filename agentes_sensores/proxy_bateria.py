"""
Proxy del sensor de batería
Usa la capa HAL para abstraer el acceso al hardware
Convierte valores ADC a nivel de carga
"""
from hal.hal_adc import HAL_ADC
from hal.hal_adc_simulado import HAL_ADC_Simulado


class ProxyBateria:
    """
    Proxy para lectura del nivel de carga de la batería

    Responsabilidades:
    - Abstraer la lectura del sensor mediante HAL
    - Convertir valores ADC a nivel de carga
    - Validar rangos de carga
    - Lanzar excepciones en caso de error
    """

    # Configuración del sensor
    PIN_SENSOR_BATERIA = 1  # Canal ADC donde está conectado el sensor de batería

    # Parámetros de conversión ADC → Carga
    # Mapeo lineal: ADC 0 = 0V (batería vacía), ADC 1023 = 5V (batería llena)
    # Asumiendo batería con rango 0-5V
    CARGA_MAXIMA = 5.0

    def __init__(self, hal: HAL_ADC = None):
        """
        Inicializa el proxy del sensor de batería

        :param hal: Implementación del HAL ADC
                    Si es None, usa HAL_ADC_Simulado por defecto
        """
        self._hal = hal if hal is not None else HAL_ADC_Simulado()
        self._hal.inicializar()

    def leer_carga(self) -> float:
        """
        Lee el nivel de carga de la batería mediante HAL

        Proceso:
        1. Lee valor ADC mediante HAL
        2. Convierte ADC a voltaje/carga
        3. Valida que esté en rango válido
        4. Retorna nivel de carga

        :return: Nivel de carga (0.0 - 5.0)
        :raises IOError: Si hay error de lectura
        """
        try:
            # 1. Lee valor del ADC mediante HAL
            valor_adc = self._hal.leer_adc(self.PIN_SENSOR_BATERIA)

            # 2. Convierte ADC a carga
            # Fórmula: carga = (adc / adc_max) * carga_maxima
            adc_max = (1 << self._hal.obtener_resolucion()) - 1  # 2^bits - 1
            carga = (valor_adc / adc_max) * self.CARGA_MAXIMA

            # 3. Limita a rango válido
            carga = max(0.0, min(self.CARGA_MAXIMA, carga))

            return carga

        except IOError as e:
            # Error de hardware
            raise IOError("Error de lectura de batería") from e

    def __del__(self):
        """Destructor: libera recursos del HAL"""
        if hasattr(self, '_hal'):
            self._hal.finalizar()
