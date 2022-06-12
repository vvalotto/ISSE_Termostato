from gestores_entidades.gestor_climatizador import *
from gestores_entidades.gestor_ambiente import *

gestor_ambiente = GestorAmbiente()
for t in range(24):
    gestor_ambiente.aumentar_temperatura_deseada()
gestor_ambiente.leer_temperatura_ambiente()
gestor_ambiente.indicar_temperatura_a_mostrar("ambiente")
gestor_ambiente.mostrar_temperatura_ambiente()

gestor_climatizador = GestorClimatizador()
gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

gestor_climatizador.mostrar_estado_climatizador()
