from gestores_entidades.gestor_ambiente import *

gestor = GestorAmbiente()
gestor.leer_temperatura_ambiente()
gestor.indicar_temperatura_a_mostrar("ambiente")
gestor.mostrar_temperatura_ambiente()

for t in range(17):
    gestor.aumentar_temperatura_deseada()
gestor.indicar_temperatura_a_mostrar("deseada")
gestor.mostrar_temperatura_deseada()

for t in range(6):
    gestor.disminuir_temperatura_deseada()
gestor.indicar_temperatura_a_mostrar("deseada")
gestor.mostrar_temperatura_deseada()
