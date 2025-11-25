import socket
import time
import json
import os
from datetime import datetime
from os import system

"""
Objeto que hace de botones o selectores para el
seteo de la temperatura deseada
"""

# Cargar configuración (buscar en directorio actual o padre)
config_file = "simuladores_config.json"
if not os.path.exists(config_file):
    config_file = os.path.join("..", "simuladores_config.json")

with open(config_file, "r") as f:
    config = json.load(f)

HOST = config["raspberry_pi"]["host"]
PUERTO = config["raspberry_pi"]["puertos"]["seteo_temperatura"]

# Historial de acciones
historial = []
contador = 0
conectado = False
ultima_accion = None

while True:
    system("clear")

    print("╔" + "═" * 54 + "╗")
    print("║" + " " * 8 + "CONTROL DE TEMPERATURA DESEADA" + " " * 16 + "║")
    print("╚" + "═" * 54 + "╝")
    print()

    # Estado de conexión
    hora = datetime.now().strftime("%H:%M:%S")
    estado_icono = "✓" if conectado else "✗"
    print(f"Conexión: {HOST}:{PUERTO} {estado_icono}")
    print(f"Hora: {hora}")
    print(f"Comandos enviados: {contador}")
    print()

    # Última acción
    if ultima_accion:
        print(f"Última acción: {ultima_accion}")
        print()

    # Historial
    if historial:
        print("┌─────────────────────────────────────────────────────┐")
        print("│ Historial (últimas 5 acciones):                     │")
        for registro in historial[-5:]:
            print(f"│  {registro}" + " " * (52 - len(registro)) + "│")
        print("└─────────────────────────────────────────────────────┘")
        print()

    print("┌─────────────────────────────────────────────────────┐")
    print("│ [S] Subir temperatura (+1°C)                        │")
    print("│ [B] Bajar temperatura (-1°C)                        │")
    print("│ [Ctrl+C] Salir                                      │")
    print("└─────────────────────────────────────────────────────┘")
    print()

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = (HOST, PUERTO)
        cliente.connect(direccion_servidor)
        conectado = True

        opcion = input("Opción [S/B] → ").upper()

        if opcion in ["S", "B"]:
            diferencia = "aumentar" if opcion == "S" else "disminuir"
            accion_texto = "SUBIR" if opcion == "S" else "BAJAR"

            cliente.send(bytes(diferencia.encode()))
            contador += 1
            registro = f"{hora} → {accion_texto}"
            historial.append(registro)
            ultima_accion = f"{accion_texto} ({hora})"
            print(f"\n✓ Comando enviado: {accion_texto}")
        elif opcion:
            print("\n✗ Opción inválida. Use S o B.")

        cliente.close()

    except ConnectionError:
        conectado = False
        print(f"\n✗ Error: No se pudo conectar a {HOST}:{PUERTO}")
        print("  Verifique que el termostato esté en modo DESEADA.")
    except Exception as e:
        conectado = False
        print(f"\n✗ Error inesperado: {e}")

    time.sleep(1)
