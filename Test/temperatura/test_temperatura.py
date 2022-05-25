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
