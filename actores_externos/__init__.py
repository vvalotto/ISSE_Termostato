"""
Paquete de actores externos del termostato.

Contiene simuladores de sensores y displays para pruebas
del sistema de termostato.

Simuladores (clientes socket):
    - simulador_bateria: Envia lecturas de voltaje
    - simulador_temperatura: Envia lecturas de temperatura
    - simulador_selector_temperatura: Alterna modo ambiente/deseada
    - simulador_seteo_temperatura_deseada: Ajusta temperatura objetivo

Displays (servidores socket):
    - cartel_bateria: Muestra tension de bateria
    - cartel_temperatura: Muestra temperatura
    - cartel_climatizador: Muestra estado del climatizador

Note:
    Los simuladores comparten codigo comun (carga de config,
    interfaz de usuario, manejo de socket). Esto es aceptable
    ya que son scripts independientes de prueba.
"""
# pylint: disable=duplicate-code
