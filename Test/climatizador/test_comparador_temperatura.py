from servicios_dominio.controlador_climatizador import *

comparador = ControladorTemperatura()

print(comparador.comparar_temperatura(20, 24))
print(comparador.comparar_temperatura(22, 24))
print(comparador.comparar_temperatura(24, 24))
print(comparador.comparar_temperatura(26, 24))
print(comparador.comparar_temperatura(28, 24))
