"""
Simulador de selector de modo de temperatura via socket TCP.

Este script simula el boton selector que alterna entre mostrar
la temperatura ambiente o la temperatura deseada en el display.
Funciona como un boton toggle de dos estados.
"""
# pylint: disable=invalid-name,duplicate-code
# Las variables de script (contador, conectado, etc.) son mutables,
# no constantes, por lo que no requieren UPPER_CASE.
# El codigo duplicado entre simuladores es aceptable (scripts independientes).

import socket
import time
import json
import os
from datetime import datetime
from os import system

# Cargar configuración (buscar en directorio actual o padre)
config_file = "simuladores_config.json"
if not os.path.exists(config_file):
    config_file = os.path.join("..", "simuladores_config.json")

with open(config_file, "r", encoding="utf-8") as f:
    config = json.load(f)

HOST = config["raspberry_pi"]["host"]
PUERTO = config["raspberry_pi"]["puertos"]["selector_temperatura"]

# Estado interno del selector (comienza en "ambiente")
estado_actual = "ambiente"
historial = []
contador = 0
conectado = False

while True:
    system("clear")

    print("╔" + "═" * 54 + "╗")
    print("║" + " " * 10 + "SELECTOR DE MODO DEL DISPLAY" + " " * 16 + "║")
    print("╚" + "═" * 54 + "╝")
    print()

    # Estado de conexión
    hora = datetime.now().strftime("%H:%M:%S")
    estado_icono = "✓" if conectado else "✗"
    print(f"Conexión: {HOST}:{PUERTO} {estado_icono}")
    print(f"Hora: {hora}")
    print(f"Cambios realizados: {contador}")
    print()

    # Estado actual resaltado
    print("┌─────────────────────────────────────────────────────┐")
    if estado_actual == "ambiente":
        print("│ MODO ACTUAL: AMBIENTE                               │")
        print("│ • Muestra temperatura del sensor (solo lectura)    │")
        print("│ • Seteo de temperatura: DESHABILITADO              │")
    else:
        print("│ MODO ACTUAL: DESEADA                                │")
        print("│ • Muestra temperatura objetivo                     │")
        print("│ • Seteo de temperatura: HABILITADO                 │")
    print("└─────────────────────────────────────────────────────┘")
    print()

    # Historial
    if historial:
        print("┌─────────────────────────────────────────────────────┐")
        print("│ Historial (últimas 5 acciones):                     │")
        for registro in historial[-5:]:
            print(f"│  {registro}" + " " * (52 - len(registro)) + "│")
        print("└─────────────────────────────────────────────────────┘")
        print()

    # Determinar próximo estado
    proximo_estado = "deseada" if estado_actual == "ambiente" else "ambiente"
    proximo_modo = "DESEADA" if proximo_estado == "deseada" else "AMBIENTE"

    print("┌─────────────────────────────────────────────────────┐")
    print(f"│ [Enter] Cambiar a modo {proximo_modo}" + " " * (27 - len(proximo_modo)) + "│")
    print("│ [Ctrl+C] Salir                                      │")
    print("└─────────────────────────────────────────────────────┘")
    print()

    try:
        input()  # Esperar Enter

        # Alternar estado
        estado_actual = proximo_estado

        # Conectar y enviar
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = (HOST, PUERTO)
        cliente.connect(direccion_servidor)
        conectado = True

        cliente.send(bytes(estado_actual.encode()))
        cliente.close()

        contador += 1
        registro = f"{hora} → {estado_actual.upper()}"
        historial.append(registro)

        print(f"\n✓ Cambiado a modo {estado_actual.upper()}")

    except ConnectionError:
        conectado = False
        print(f"\n✗ Error: No se pudo conectar a {HOST}:{PUERTO}")
        print("  Verifique que el termostato esté ejecutándose.")
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        break
    except (OSError, socket.error) as e:
        conectado = False
        print(f"\n✗ Error de conexion: {e}")

    time.sleep(2)
