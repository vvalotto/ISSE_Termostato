
from gestores_entidades.gestor_bateria import *

gestor = GestorBateria("socket")
gestor.verificar_nivel_de_carga()
print(gestor.obtener_nivel_de_carga())
print(gestor.obtener_indicador_de_carga())
