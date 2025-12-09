"""
Simulador de sensor de temperatura via socket TCP.

Este script simula un sensor de temperatura que envia lecturas
en grados Celsius al termostato a traves de conexion socket.
Se conecta al puerto configurado y permite ingresar valores
manualmente para pruebas del sistema.
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
PUERTO = config["raspberry_pi"]["puertos"]["temperatura"]

# Historial de acciones
historial = []
contador = 0
conectado = False

while True:
    system("clear")

    print("╔" + "═" * 54 + "╗")
    print("║" + " " * 10 + "SIMULADOR DE SENSOR DE TEMPERATURA" + " " * 10 + "║")
    print("╚" + "═" * 54 + "╝")
    print()

    # Estado de conexión
    hora = datetime.now().strftime("%H:%M:%S")
    estado_icono = "✓" if conectado else "✗"
    print(f"Conexión: {HOST}:{PUERTO} {estado_icono}")
    print(f"Hora: {hora}")
    print(f"Lecturas enviadas: {contador}")
    print()

    # Historial
    if historial:
        print("┌─────────────────────────────────────────────────────┐")
        print("│ Historial (últimas 5 lecturas):                     │")
        for registro in historial[-5:]:
            print(f"│  {registro}" + " " * (52 - len(registro)) + "│")
        print("└─────────────────────────────────────────────────────┘")
        print()

    print("┌─────────────────────────────────────────────────────┐")
    print("│ Ingrese la temperatura ambiente (°C)                 │")
    print("│ Ejemplos: 22, 18.5, 25                              │")
    print("└─────────────────────────────────────────────────────┘")
    print()

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = (HOST, PUERTO)
        cliente.connect(direccion_servidor)
        conectado = True

        temperatura = input("Temperatura (°C) → ")

        if temperatura.strip():  # Solo enviar si hay contenido
            cliente.send(bytes(temperatura.encode()))
            contador += 1
            registro = f"{hora} → {temperatura}°C"
            historial.append(registro)
            print(f"\n✓ Enviado: {temperatura}°C")

        cliente.close()

    except ConnectionError:
        conectado = False
        print(f"\n✗ Error: No se pudo conectar a {HOST}:{PUERTO}")
        print("  Verifique que el termostato esté ejecutándose.")
    except ValueError:
        print("\n✗ Error: Ingrese un valor numérico válido")
    except (OSError, socket.error) as e:
        conectado = False
        print(f"\n✗ Error de conexion: {e}")

    time.sleep(2)
