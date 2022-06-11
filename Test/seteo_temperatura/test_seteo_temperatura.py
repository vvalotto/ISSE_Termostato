from servicios_aplicacion.selector_entrada import *
from gestores_entidades.gestor_ambiente import *

gestor = GestorAmbiente()

gestor.leer_temperatura_ambiente()
print(gestor.obtener_temperatura_ambiente())

for t in range(17):
    gestor.aumentar_temperatura_deseada()

selector = SelectorEntradaTemperatura(gestor)
selector.ejecutar()
print(gestor.ambiente)
