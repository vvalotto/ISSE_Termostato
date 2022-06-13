
from gestores_entidades.gestor_bateria import *
from configurador.configurador import *

Configurador().cargar_configuracion()
gestor = GestorBateria()
gestor.verificar_nivel_de_carga()
gestor.mostrar_nivel_de_carga()
gestor.mostrar_indicador_de_carga()
