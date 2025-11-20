"""
Hardware Abstraction Layer (HAL)
Capa de abstracción de hardware que aísla el código de aplicación
del hardware específico. Permite cambiar fácilmente entre simulación
y hardware real.
"""

from .hal_adc import HAL_ADC
from .hal_adc_simulado import HAL_ADC_Simulado
from .hal_adc_mock import HAL_ADC_Mock

__all__ = [
    'HAL_ADC',
    'HAL_ADC_Simulado',
    'HAL_ADC_Mock',
]
