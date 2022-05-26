from servicios_aplicacion.selector_entrada import *
from gestores_entidades.gestor_ambiente import *

gestor = GestorAmbiente()
selector = SelectorEntradaTemperatura(gestor)
selector.ejecutar()
print(gestor.ambiente)
