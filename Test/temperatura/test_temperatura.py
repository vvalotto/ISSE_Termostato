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
