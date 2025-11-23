# Documento de Migración: Incorporación de Capa HAL al Proyecto Termostato

**Proyecto:** ISSE_Termostato
**Versión:** 1.0
**Fecha:** 2025-11-12
**Autor:** Equipo de Desarrollo
**Sprint:** Post Sprint 1

---

## 1. Objetivo

Incorporar una **capa HAL (Hardware Abstraction Layer)** al proyecto termostato para:

1. **Alinear la arquitectura con el modelo tridimensional** propuesto en la "Guía de Diseño Detallado"
2. **Mejorar la portabilidad** del software entre diferentes plataformas hardware
3. **Facilitar el testing** mediante inyección de dependencias
4. **Separar claramente** el acceso al hardware de la lógica de negocio
5. **Preparar el proyecto** para migración futura a hardware real (Raspberry Pi, ESP32, etc.)

---

## 2. Justificación

### 2.1 Problema Actual

La implementación actual mezcla responsabilidades:

```python
# proxy_sensor_temperatura.py (ACTUAL)
class ProxySensorTemperatura:
    @staticmethod
    def leer_temperatura():
        archivo = open("temperatura", "r")  # ← Acceso directo a "hardware"
        temperatura = int(archivo.read())    # ← Conversión mezclada
        archivo.close()
        return temperatura
```

**Problemas:**
- ❌ El proxy accede directamente al "hardware" (archivo)
- ❌ Difícil cambiar de simulación a hardware real
- ❌ No sigue el modelo de 5 capas del documento

### 2.2 Solución Propuesta

Separar en dos capas:

```python
# hal/hal_adc.py (NUEVO)
class HAL_ADC:
    def leer_adc(self, pin: int) -> int:
        # Solo accede al hardware
        pass

# agentes_sensores/proxy_sensor_temperatura.py (MODIFICADO)
class ProxySensorTemperatura:
    def __init__(self, hal: HAL_ADC):
        self._hal = hal

    def leer_temperatura(self) -> int:
        valor_adc = self._hal.leer_adc(0)    # ← Usa HAL
        temperatura = (valor_adc - 150) / 5  # ← Solo conversión
        return int(temperatura)
```

**Beneficios:**
- ✅ Separación clara de responsabilidades
- ✅ Fácil cambio entre simulación y hardware real
- ✅ Sigue el modelo de 5 capas del documento
- ✅ Testeable con mocks

---

## 3. Estructura Actual vs. Propuesta

### 3.1 Estructura Actual

```
ISSE_Termostato/
├── agentes_actuadores/
│   ├── visualizador_bateria.py
│   └── visualizador_temperatura.py
├── agentes_sensores/
│   ├── proxy_bateria.py
│   └── proxy_sensor_temperatura.py
├── entidades/
│   ├── ambiente.py
│   └── bateria.py
├── gestores_entidades/
│   ├── gestor_ambiente.py
│   └── gestor_bateria.py
├── servicios_aplicacion/
│   └── presentador.py
├── Test/
│   ├── bateria/
│   ├── presentador/
│   └── temperatura/
├── bateria                    # ← Archivo de datos
├── temperatura                # ← Archivo de datos
└── ...
```

### 3.2 Estructura Propuesta

```
ISSE_Termostato/
├── hal/                       ⭐ NUEVO
│   ├── __init__.py           ⭐ NUEVO
│   ├── hal_adc.py            ⭐ NUEVO - Interfaz abstracta
│   ├── hal_adc_simulado.py   ⭐ NUEVO - Implementación simulada
│   └── hal_adc_mock.py       ⭐ NUEVO - Mock para testing
│
├── agentes_actuadores/
│   ├── visualizador_bateria.py
│   └── visualizador_temperatura.py
│
├── agentes_sensores/
│   ├── proxy_bateria.py      🔄 MODIFICAR
│   └── proxy_sensor_temperatura.py  🔄 MODIFICAR
│
├── entidades/
│   ├── ambiente.py
│   └── bateria.py
│
├── gestores_entidades/
│   ├── gestor_ambiente.py    🔄 MODIFICAR
│   └── gestor_bateria.py     🔄 MODIFICAR
│
├── servicios_aplicacion/
│   └── presentador.py
│
├── Test/
│   ├── hal/                  ⭐ NUEVO
│   │   ├── __init__.py      ⭐ NUEVO
│   │   └── test_hal_adc.py  ⭐ NUEVO
│   ├── bateria/
│   │   ├── test_bateria.py  🔄 MODIFICAR
│   │   └── bateria
│   ├── presentador/
│   │   ├── test_presentador.py
│   │   └── bateria
│   └── temperatura/
│       └── test_temperatura.py  🔄 MODIFICAR
│
├── datos_simulacion/         ⭐ NUEVO - Directorio para archivos de datos
│   ├── temperatura           🔄 MOVER
│   └── bateria               🔄 MOVER
│
└── ...
```

**Leyenda:**
- ⭐ NUEVO: Archivo/directorio a crear
- 🔄 MODIFICAR: Archivo existente a modificar
- 📦 MOVER: Archivo a mover de ubicación

---

## 4. Archivos Nuevos a Crear

### 4.1 `hal/__init__.py`

**Propósito:** Inicializar el paquete HAL y exponer interfaces públicas

```python
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
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/hal/__init__.py`

---

### 4.2 `hal/hal_adc.py`

**Propósito:** Interfaz abstracta para ADC (Abstract Base Class)

```python
"""
Interfaz abstracta para la capa HAL del ADC
Permite intercambiar implementaciones (simulada, GPIO real, mock para tests)
"""
from abc import ABC, abstractmethod


class HAL_ADC(ABC):
    """
    Abstracción del hardware de ADC (Analog-to-Digital Converter)

    Define el contrato que deben cumplir todas las implementaciones
    de HAL para lectura de valores analógicos.
    """

    @abstractmethod
    def inicializar(self) -> None:
        """
        Inicializa el hardware del ADC

        Esta operación debe llamarse antes de usar leer_adc()
        Puede configurar pines, velocidades, modos, etc.

        :raises IOError: Si hay error de inicialización
        """
        pass

    @abstractmethod
    def leer_adc(self, canal: int) -> int:
        """
        Lee el valor del ADC en el canal especificado

        :param canal: Número de canal/pin ADC a leer
        :return: Valor digital del ADC (rango depende de la implementación)
                 Por ejemplo: 0-1023 para 10 bits, 0-4095 para 12 bits
        :raises IOError: Si hay error de lectura o ADC no inicializado
        """
        pass

    @abstractmethod
    def finalizar(self) -> None:
        """
        Libera recursos del hardware

        Debe llamarse al terminar de usar el ADC para liberar recursos
        (cerrar archivos, liberar GPIO, etc.)
        """
        pass

    @abstractmethod
    def obtener_resolucion(self) -> int:
        """
        Obtiene la resolución del ADC en bits

        :return: Número de bits de resolución (ej: 10, 12, 16)
        """
        pass
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/hal/hal_adc.py`

---

### 4.3 `hal/hal_adc_simulado.py`

**Propósito:** Implementación simulada del HAL para desarrollo

```python
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
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/hal/hal_adc_simulado.py`

---

### 4.4 `hal/hal_adc_mock.py`

**Propósito:** Mock para testing con valores predefinidos

```python
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
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/hal/hal_adc_mock.py`

---

### 4.5 `Test/hal/__init__.py`

**Propósito:** Inicializar paquete de tests HAL

```python
"""
Tests de la capa HAL (Hardware Abstraction Layer)
"""
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/Test/hal/__init__.py`

---

### 4.6 `Test/hal/test_hal_adc.py`

**Propósito:** Tests unitarios del HAL

```python
"""
Tests unitarios de las implementaciones del HAL ADC
"""
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from hal.hal_adc_simulado import HAL_ADC_Simulado
from hal.hal_adc_mock import HAL_ADC_Mock


def test_hal_adc_simulado_inicializacion():
    """Test: HAL simulado se inicializa correctamente"""
    hal = HAL_ADC_Simulado()
    hal.inicializar()

    # Debería poder leer sin errores
    valor = hal.leer_adc(0)
    assert 0 <= valor <= 1023, f"Valor ADC fuera de rango: {valor}"

    hal.finalizar()
    print("✅ Test HAL simulado inicialización: OK")


def test_hal_adc_simulado_lectura():
    """Test: HAL simulado genera valores dentro del rango esperado"""
    hal = HAL_ADC_Simulado(temperatura_base=22.0, ruido_std=0.5)
    hal.inicializar()

    # Realiza múltiples lecturas
    valores = [hal.leer_adc(0) for _ in range(10)]

    # Verifica que todos estén en rango válido
    for valor in valores:
        assert 0 <= valor <= 1023, f"Valor fuera de rango: {valor}"

    # Verifica que haya variación (no todos iguales)
    assert len(set(valores)) > 1, "Los valores no varían (sin ruido)"

    hal.finalizar()
    print(f"✅ Test HAL simulado lectura: OK (valores: {min(valores)}-{max(valores)})")


def test_hal_adc_simulado_error_sin_inicializar():
    """Test: HAL lanza error si se lee sin inicializar"""
    hal = HAL_ADC_Simulado()

    try:
        hal.leer_adc(0)
        assert False, "Debería haber lanzado IOError"
    except IOError as e:
        assert "no inicializado" in str(e).lower()
        print("✅ Test HAL error sin inicializar: OK")


def test_hal_adc_mock_valores_predefinidos():
    """Test: Mock retorna valores predefinidos correctamente"""
    valores_esperados = [200, 250, 300]
    hal = HAL_ADC_Mock(valores_adc=valores_esperados)
    hal.inicializar()

    # Lee los valores
    valores_leidos = [hal.leer_adc(0) for _ in range(3)]

    assert valores_leidos == valores_esperados, \
        f"Valores leídos {valores_leidos} != esperados {valores_esperados}"

    # Verifica que es circular (vuelve al principio)
    valor_circular = hal.leer_adc(0)
    assert valor_circular == valores_esperados[0], "No es circular"

    hal.finalizar()
    print("✅ Test Mock valores predefinidos: OK")


def test_hal_adc_mock_contador_llamadas():
    """Test: Mock cuenta correctamente las llamadas"""
    hal = HAL_ADC_Mock([100])
    hal.inicializar()

    # Realiza varias lecturas
    for _ in range(5):
        hal.leer_adc(0)

    assert hal.obtener_llamadas_leer() == 5, "Contador de llamadas incorrecto"

    hal.finalizar()
    print("✅ Test Mock contador llamadas: OK")


if __name__ == "__main__":
    print("=== Tests HAL ADC ===\n")

    test_hal_adc_simulado_inicializacion()
    test_hal_adc_simulado_lectura()
    test_hal_adc_simulado_error_sin_inicializar()
    test_hal_adc_mock_valores_predefinidos()
    test_hal_adc_mock_contador_llamadas()

    print("\n✅ Todos los tests HAL pasaron correctamente")
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/Test/hal/test_hal_adc.py`

---

## 5. Archivos Existentes a Modificar

### 5.1 `agentes_sensores/proxy_sensor_temperatura.py`

**Cambios:**
1. Agregar dependencia del HAL
2. Modificar `leer_temperatura()` para usar HAL
3. Agregar conversión ADC → °C
4. Mantener manejo de excepciones

**Código ACTUAL:**

```python
"""
Clase que llamaria a la lectura de la interfaz de lectura
del sensor de temperatura
"""


class ProxySensorTemperatura:

    @staticmethod
    def leer_temperatura():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        """
        try:
            archivo = open("temperatura", "r")
            temperatura = int(archivo.read())
            archivo.close()
        except IOError:
            raise Exception("Error de Lectura de Sensor")
        return temperatura
```

**Código NUEVO (propuesto):**

```python
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
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/agentes_sensores/proxy_sensor_temperatura.py`

**Líneas modificadas:**
- Línea 1-8: Docstring y imports nuevos
- Línea 10-80: Toda la clase (refactorizada)

---

### 5.2 `agentes_sensores/proxy_bateria.py`

**Cambios similares a proxy_sensor_temperatura.py**

**Código ACTUAL:**

```python
"""
Primera version: simula una lectura
"""


class ProxyBateria:

    @staticmethod
    def leer_carga():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        :return:
        """
        archivo = open("bateria", "r")
        carga = float(archivo.read())
        archivo.close()
        return carga
```

**Código NUEVO (propuesto):**

```python
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
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/agentes_sensores/proxy_bateria.py`

---

### 5.3 `gestores_entidades/gestor_ambiente.py`

**Cambios:**
1. Permitir inyección de HAL en constructor
2. Pasar HAL al ProxySensorTemperatura
3. Mantener comportamiento por defecto

**Código ACTUAL (líneas relevantes):**

```python
# Línea 19-22
def __init__(self):
    self._ambiente = Ambiente()
    self._proxy_sensor_temperatura = ProxySensorTemperatura()
    self._visualizador_temperatura = VisualizadorTemperaturas()
```

**Código MODIFICADO:**

```python
# Línea 19-30 (aproximado)
def __init__(self, hal_adc=None):
    """
    Inicializa el gestor de ambiente

    :param hal_adc: Opcional, permite inyectar implementación HAL específica
                    Si es None, ProxySensorTemperatura usará HAL simulado por defecto
    """
    self._ambiente = Ambiente()

    # Permite inyectar HAL desde fuera (útil para testing y producción)
    if hal_adc is not None:
        self._proxy_sensor_temperatura = ProxySensorTemperatura(hal_adc)
    else:
        # Usa HAL simulado por defecto
        self._proxy_sensor_temperatura = ProxySensorTemperatura()

    self._visualizador_temperatura = VisualizadorTemperaturas()
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/gestores_entidades/gestor_ambiente.py`

**Líneas modificadas:** 19-30 (aproximado)

---

### 5.4 `gestores_entidades/gestor_bateria.py`

**Cambios similares a gestor_ambiente.py**

**Código ACTUAL (líneas relevantes):**

```python
# Línea 13-22
def __init__(self):
    """
    Inicializa el gestor que esta compuesto de:
    La clase que que obtiene la carga de la bateria desde la interfaz
    la clase que guarda el estado de la bateria
    la clase que expone visualmente el estado de la bateria
    """
    self._bateria = Bateria()
    self._proxy_bateria = ProxyBateria()
    self._visualizador_bateria = VisualizadorBateria()
```

**Código MODIFICADO:**

```python
# Línea 13-28 (aproximado)
def __init__(self, hal_adc=None):
    """
    Inicializa el gestor de batería

    :param hal_adc: Opcional, permite inyectar implementación HAL específica
                    Si es None, ProxyBateria usará HAL simulado por defecto

    Composición:
    - Bateria: entidad de dominio que guarda el estado
    - ProxyBateria: boundary que obtiene la carga desde el sensor vía HAL
    - VisualizadorBateria: boundary que expone visualmente el estado
    """
    self._bateria = Bateria()

    # Permite inyectar HAL desde fuera (útil para testing y producción)
    if hal_adc is not None:
        self._proxy_bateria = ProxyBateria(hal_adc)
    else:
        # Usa HAL simulado por defecto
        self._proxy_bateria = ProxyBateria()

    self._visualizador_bateria = VisualizadorBateria()
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/gestores_entidades/gestor_bateria.py`

**Líneas modificadas:** 13-28 (aproximado)

---

### 5.5 `Test/temperatura/test_temperatura.py`

**Cambios:**
1. Agregar import del HAL_ADC_Mock
2. Inyectar mock con valores específicos para testing determinista

**Código ACTUAL:**

```python
from gestores_entidades.gestor_ambiente import *

gestor = GestorAmbiente()
gestor.leer_temperatura_ambiente()
print(gestor.obtener_temperatura_ambiente())

for t in range(17):
    gestor.aumentar_temperatura_deseada()

print(gestor.obtener_temperatura_deseada())

for t in range(6):
    gestor.disminuir_temperatura_deseada()
print(gestor.obtener_temperatura_deseada())
```

**Código MODIFICADO:**

```python
"""
Test del gestor de ambiente con HAL mock
Permite testing determinista con valores predefinidos
"""
from gestores_entidades.gestor_ambiente import GestorAmbiente
from hal.hal_adc_mock import HAL_ADC_Mock

# Test 1: Lectura de temperatura con valor predefinido
print("=== Test 1: Lectura de temperatura ===")

# Crea mock con valor ADC = 250 (corresponde a ~20°C)
# Fórmula: temp = (250 - 150) / 5 = 20°C
hal_mock = HAL_ADC_Mock(valores_adc=[250])

# Inyecta mock en el gestor
gestor = GestorAmbiente(hal_adc=hal_mock)

# Lee temperatura
gestor.leer_temperatura_ambiente()
temp_leida = gestor.obtener_temperatura_ambiente()

print(f"Temperatura leída: {temp_leida}°C")
assert temp_leida == 20, f"Esperaba 20°C, obtuvo {temp_leida}°C"

print("✅ Test 1 OK\n")

# Test 2: Incremento de temperatura deseada
print("=== Test 2: Temperatura deseada ===")

for t in range(17):
    gestor.aumentar_temperatura_deseada()

temp_deseada = gestor.obtener_temperatura_deseada()
print(f"Temperatura deseada tras 17 incrementos: {temp_deseada}°C")

for t in range(6):
    gestor.disminuir_temperatura_deseada()

temp_deseada_final = gestor.obtener_temperatura_deseada()
print(f"Temperatura deseada tras 6 decrementos: {temp_deseada_final}°C")

print("✅ Test 2 OK\n")

# Test 3: Múltiples lecturas
print("=== Test 3: Múltiples lecturas ===")

# Mock con secuencia de valores
valores_secuencia = [250, 260, 255, 245]  # Simula variación de temperatura
hal_mock_secuencia = HAL_ADC_Mock(valores_adc=valores_secuencia)
gestor2 = GestorAmbiente(hal_adc=hal_mock_secuencia)

temperaturas_leidas = []
for i in range(4):
    gestor2.leer_temperatura_ambiente()
    temp = gestor2.obtener_temperatura_ambiente()
    temperaturas_leidas.append(temp)
    print(f"Lectura {i+1}: {temp}°C")

print(f"Secuencia de temperaturas: {temperaturas_leidas}")
print("✅ Test 3 OK\n")

print("✅ Todos los tests pasaron correctamente")
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/Test/temperatura/test_temperatura.py`

---

### 5.6 `Test/bateria/test_bateria.py`

**Cambios similares a test_temperatura.py**

**Código ACTUAL:**

```python
from gestores_entidades.gestor_bateria import *

gestor = GestorBateria()
gestor.obtener_nivel_de_carga()
gestor.verificar_nivel_de_carga()
print(gestor.obtener_nivel_de_carga())
print(gestor.obtener_indicador_de_carga())
```

**Código MODIFICADO:**

```python
"""
Test del gestor de batería con HAL mock
"""
from gestores_entidades.gestor_bateria import GestorBateria
from hal.hal_adc_mock import HAL_ADC_Mock

print("=== Test Gestor Batería con HAL ===\n")

# Test con diferentes niveles de carga
niveles_test = [
    (1023, 5.0, "NORMAL"),   # 100% carga → NORMAL
    (819, 4.0, "BAJA"),      # 80% carga → BAJA
    (512, 2.5, "BAJA"),      # 50% carga → BAJA
    (205, 1.0, "BAJA"),      # 20% carga → BAJA
]

for adc, carga_esperada, indicador_esperado in niveles_test:
    hal_mock = HAL_ADC_Mock(valores_adc=[adc])
    gestor = GestorBateria(hal_adc=hal_mock)

    gestor.verificar_nivel_de_carga()
    nivel = gestor.obtener_nivel_de_carga()
    indicador = gestor.obtener_indicador_de_carga()

    print(f"ADC={adc} → Carga={nivel:.2f}V, Indicador={indicador}")

    # Verifica valores aproximados
    assert abs(nivel - carga_esperada) < 0.1, f"Carga incorrecta: {nivel} vs {carga_esperada}"
    assert indicador == indicador_esperado, f"Indicador incorrecto: {indicador} vs {indicador_esperado}"

print("\n✅ Todos los tests de batería pasaron correctamente")
```

**Ubicación:** `/Users/victor/PycharmProjects/ISSE_Termostato/Test/bateria/test_bateria.py`

---

## 6. Plan de Implementación

### Fase 1: Crear Infraestructura HAL (30 min)

**Objetivo:** Crear la capa HAL completa

**Tareas:**
1. ✅ Crear directorio `hal/`
2. ✅ Crear `hal/__init__.py`
3. ✅ Crear `hal/hal_adc.py` (interfaz)
4. ✅ Crear `hal/hal_adc_simulado.py` (implementación)
5. ✅ Crear `hal/hal_adc_mock.py` (para testing)

**Comandos:**
```bash
cd /Users/victor/PycharmProjects/ISSE_Termostato
mkdir -p hal
touch hal/__init__.py
touch hal/hal_adc.py
touch hal/hal_adc_simulado.py
touch hal/hal_adc_mock.py
```

**Verificación:**
```bash
ls -la hal/
# Debe mostrar 4 archivos: __init__.py, hal_adc.py, hal_adc_simulado.py, hal_adc_mock.py
```

---

### Fase 2: Implementar Tests HAL (20 min)

**Objetivo:** Crear tests antes de refactorizar (TDD)

**Tareas:**
1. ✅ Crear directorio `Test/hal/`
2. ✅ Crear `Test/hal/__init__.py`
3. ✅ Crear `Test/hal/test_hal_adc.py`
4. ✅ Ejecutar tests y verificar que pasen

**Comandos:**
```bash
mkdir -p Test/hal
touch Test/hal/__init__.py
touch Test/hal/test_hal_adc.py
```

**Verificación:**
```bash
cd /Users/victor/PycharmProjects/ISSE_Termostato
python Test/hal/test_hal_adc.py
# Debe mostrar: ✅ Todos los tests HAL pasaron correctamente
```

---

### Fase 3: Refactorizar Proxies (20 min)

**Objetivo:** Actualizar proxies para usar HAL

**Tareas:**
1. ✅ Respaldar `proxy_sensor_temperatura.py` original
2. ✅ Modificar `proxy_sensor_temperatura.py` para usar HAL
3. ✅ Respaldar `proxy_bateria.py` original
4. ✅ Modificar `proxy_bateria.py` para usar HAL

**Comandos:**
```bash
# Respaldos
cp agentes_sensores/proxy_sensor_temperatura.py agentes_sensores/proxy_sensor_temperatura.py.backup
cp agentes_sensores/proxy_bateria.py agentes_sensores/proxy_bateria.py.backup

# Luego editar los archivos con el código propuesto
```

**Verificación:**
```bash
# Verificar imports
grep "from hal" agentes_sensores/proxy_sensor_temperatura.py
grep "from hal" agentes_sensores/proxy_bateria.py
```

---

### Fase 4: Actualizar Gestores (15 min)

**Objetivo:** Permitir inyección de HAL en gestores

**Tareas:**
1. ✅ Modificar constructor de `GestorAmbiente`
2. ✅ Modificar constructor de `GestorBateria`
3. ✅ Verificar compatibilidad hacia atrás (sin parámetros)

**Comandos:**
```bash
# Respaldos
cp gestores_entidades/gestor_ambiente.py gestores_entidades/gestor_ambiente.py.backup
cp gestores_entidades/gestor_bateria.py gestores_entidades/gestor_bateria.py.backup
```

---

### Fase 5: Actualizar Tests (20 min)

**Objetivo:** Adaptar tests existentes para usar HAL mock

**Tareas:**
1. ✅ Modificar `Test/temperatura/test_temperatura.py`
2. ✅ Modificar `Test/bateria/test_bateria.py`
3. ✅ Ejecutar y verificar que pasen

**Verificación:**
```bash
PYTHONPATH=/Users/victor/PycharmProjects/ISSE_Termostato python Test/temperatura/test_temperatura.py
PYTHONPATH=/Users/victor/PycharmProjects/ISSE_Termostato python Test/bateria/test_bateria.py
```

---

### Fase 6: Mover Archivos de Datos (10 min)

**Objetivo:** Organizar archivos de simulación (opcional)

**Tareas:**
1. ✅ Crear directorio `datos_simulacion/`
2. ✅ Mover archivos `temperatura` y `bateria`
3. ⚠️ **NOTA:** Con HAL, estos archivos ya no se usan, pero se conservan por compatibilidad

**Comandos:**
```bash
mkdir -p datos_simulacion
mv temperatura datos_simulacion/ 2>/dev/null || true
mv bateria datos_simulacion/ 2>/dev/null || true
```

---

### Fase 7: Validación Completa (15 min)

**Objetivo:** Verificar que todo funciona

**Tareas:**
1. ✅ Ejecutar todos los tests
2. ✅ Ejecutar test del presentador
3. ✅ Verificar salida esperada

**Comandos:**
```bash
cd /Users/victor/PycharmProjects/ISSE_Termostato

# Tests HAL
python Test/hal/test_hal_adc.py

# Tests de sensores
PYTHONPATH=$(pwd) python Test/temperatura/test_temperatura.py
PYTHONPATH=$(pwd) python Test/bateria/test_bateria.py

# Test integración
PYTHONPATH=$(pwd) python Test/presentador/test_presentador.py
```

**Salida esperada del presentador:**
```
-------------- BATERIA -------------
[HAL_ADC_Simulado] Canal 1: ADC=xxx (~xx.x°C, deriva=x.xx°C)
4.5
NORMAL
------------------------------------


------------ TEMPERATURA ----------
[HAL_ADC_Simulado] Canal 0: ADC=xxx (~xx.x°C, deriva=x.xx°C)
22
------------------------------------
```

---

## 7. Checklist de Verificación

Antes de dar por completada la migración, verificar:

### 7.1 Estructura de Directorios

- [ ] Existe directorio `hal/` con 4 archivos
- [ ] Existe directorio `Test/hal/` con tests
- [ ] Archivos de respaldo creados (`.backup`)

### 7.2 Compilación/Imports

- [ ] No hay errores de import al ejecutar tests
- [ ] `from hal.hal_adc import HAL_ADC` funciona
- [ ] `from hal.hal_adc_simulado import HAL_ADC_Simulado` funciona

### 7.3 Tests

- [ ] `Test/hal/test_hal_adc.py` pasa (5 tests)
- [ ] `Test/temperatura/test_temperatura.py` pasa (3 tests)
- [ ] `Test/bateria/test_bateria.py` pasa
- [ ] `Test/presentador/test_presentador.py` pasa

### 7.4 Funcionalidad

- [ ] Las temperaturas simuladas varían (hay ruido)
- [ ] Los valores de batería son coherentes
- [ ] No se rompe compatibilidad hacia atrás (tests antiguos funcionan)
- [ ] Los gestores pueden usarse sin pasar HAL (comportamiento por defecto)

### 7.5 Arquitectura

- [ ] La capa HAL está completamente aislada
- [ ] Los proxies NO acceden directamente a archivos
- [ ] Los gestores permiten inyección de dependencias
- [ ] Las entidades NO tienen dependencias de HAL

---

## 8. Rollback (Plan B)

Si algo falla, revertir cambios:

```bash
cd /Users/victor/PycharmProjects/ISSE_Termostato

# Restaurar proxies
cp agentes_sensores/proxy_sensor_temperatura.py.backup agentes_sensores/proxy_sensor_temperatura.py
cp agentes_sensores/proxy_bateria.py.backup agentes_sensores/proxy_bateria.py

# Restaurar gestores
cp gestores_entidades/gestor_ambiente.py.backup gestores_entidades/gestor_ambiente.py
cp gestores_entidades/gestor_bateria.py.backup gestores_entidades/gestor_bateria.py

# Eliminar HAL
rm -rf hal/
rm -rf Test/hal/
```

---

## 9. Impacto en Documentación de Diseño

### 9.1 Actualización del Paso 2 (Análisis Tridimensional)

**Dimensión Estructural - Tabla de Capas:**

| Capa | ¿Involucrada? | Responsabilidad Específica |
|------|---------------|---------------------------|
| **Presentación** | ❌ No | No hay UI en esta funcionalidad |
| **Aplicación** | ✅ Sí | **GestorAmbiente**: Coordina la lectura y actualización |
| **Dominio** | ✅ Sí | **Ambiente**: Almacena temperatura como concepto de negocio |
| **Infraestructura** | ✅ Sí | **ProxySensorTemperatura**: Convierte valor ADC a temperatura |
| **Dispositivos (HAL)** | ✅ Sí | **HAL_ADC_Simulado**: Lee pin ADC simulado |

### 9.2 Actualización del Paso 3 (Diagrama de Robustez)

**Nuevos elementos:**

| Elemento | Tipo | Descripción |
|----------|------|-------------|
| **HAL_ADC_Simulado** | Boundary | Nueva capa de abstracción hardware |
| **Sensor ADC** | Actor | Actor hardware (simulado) |

**Flujo actualizado:**
```
[Ciclo Control] → [GestorAmbiente] → [ProxySensorTemperatura] → [HAL_ADC] → [Sensor ADC]
                         ↓
                    [Ambiente]
```

### 9.3 Actualización del Paso 4 (Diagrama de Secuencia)

**Agregar mensajes:**
- `ProxySensorTemperatura → HAL_ADC: leer_adc(0)`
- `HAL_ADC → Sensor: open/read/close`
- `HAL_ADC → ProxySensorTemperatura: valor_adc`

### 9.4 Actualización del Paso 5 (Modelo de Clases)

**Agregar clases:**
- `HAL_ADC` (interfaz)
- `HAL_ADC_Simulado` (implementación)
- `HAL_ADC_Mock` (para testing)

**Relaciones:**
- `ProxySensorTemperatura` → `HAL_ADC` (dependencia)
- `HAL_ADC_Simulado` → `HAL_ADC` (implementa)

---

## 10. Beneficios Post-Migración

### 10.1 Inmediatos

✅ Arquitectura alineada con documento de diseño
✅ Código más limpio y organizado
✅ Tests más robustos y deterministas
✅ Simulación más realista (ruido, deriva)

### 10.2 Futuros

✅ Fácil migración a hardware real
✅ Soporte para múltiples plataformas
✅ Reutilización de HAL en otros proyectos
✅ Base sólida para agregar más sensores

---

## 11. Próximos Pasos (Opcional)

Después de completar la migración, considerar:

1. **Agregar HAL para GPIO digital** (botones, LEDs)
2. **Agregar HAL para EEPROM** (persistencia)
3. **Crear implementación HAL_ADC_GPIO** para Raspberry Pi
4. **Documentar protocolo de calibración** de sensores
5. **Agregar logging estructurado** en capa HAL

---

## 12. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Archivos nuevos** | 6 archivos (5 en `hal/`, 1 test) |
| **Archivos modificados** | 6 archivos (2 proxies, 2 gestores, 2 tests) |
| **Líneas de código nuevas** | ~350 líneas |
| **Líneas de código modificadas** | ~100 líneas |
| **Tiempo estimado** | 2-3 horas |
| **Riesgo** | Bajo (rollback disponible) |
| **Beneficio** | Alto (arquitectura profesional) |

---

**Documento preparado por:** Claude Code
**Revisado por:** Equipo de desarrollo
**Estado:** Listo para implementación
**Fecha de creación:** 2025-11-12
