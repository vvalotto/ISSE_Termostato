
from gestores_entidades.gestor_bateria import *

gestor = GestorBateria()
gestor.verificar_nivel_de_carga("socket")
print(gestor.obtener_nivel_de_carga())
print(gestor.obtener_indicador_de_carga())
