from servicios_aplicacion.presentador import *
from gestores_entidades.gestor_ambiente import *
from gestores_entidades.gestor_bateria import *

gestor_bateria = GestorBateria()
gestor_amiente = GestorAmbiente()

gestor_bateria.verificar_nivel_de_carga()
gestor_amiente.leer_temperatura_ambiente()

presentador = Presentador(gestor_bateria, gestor_amiente)
presentador.ejecutar()
