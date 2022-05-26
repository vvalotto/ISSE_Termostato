from servicios_aplicacion.presentador import *
from gestores_entidades.gestor_ambiente import *
from gestores_entidades.gestor_bateria import *
from gestores_entidades.gestor_climatizador import *

gestor_bateria = GestorBateria()
gestor_ambiente = GestorAmbiente()
gestor_climatizador = GestorClimatizador()

gestor_bateria.verificar_nivel_de_carga()
gestor_ambiente.leer_temperatura_ambiente()

for t in range(24):
    gestor_ambiente.aumentar_temperatura_deseada()
gestor_ambiente.leer_temperatura_ambiente()

presentador = Presentador(gestor_bateria, gestor_ambiente, gestor_climatizador)
presentador.ejecutar()

gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)
presentador.ejecutar()