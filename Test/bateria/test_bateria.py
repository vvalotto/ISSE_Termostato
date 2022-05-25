
from gestor_bateria import *

gestor = GestorBateria()
gestor.obtener_nivel_de_carga()
gestor.verificar_nivel_de_carga()
print(gestor.obtener_nivel_de_carga())
print(gestor.obtener_indicador_de_carga())