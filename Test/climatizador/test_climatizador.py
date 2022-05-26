import gestor_climatizador
from servicios_dominio.controlador_climatizador import *
from gestores_entidades.gestor_climatizador import *
from gestores_entidades.gestor_ambiente import *

gestor_ambiente = GestorAmbiente()
for t in range(24):
    gestor_ambiente.aumentar_temperatura_deseada()
gestor_ambiente.leer_temperatura_ambiente()

gestor_climatizador = GestorClimatizador()
gestor_climatizador.accionar_climatizador(gestor_ambiente.ambiente)

print(gestor_climatizador.obtener_estado_climatizador())