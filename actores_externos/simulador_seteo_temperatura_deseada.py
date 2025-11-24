import socket
import time
import json
import os
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

while True:
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = (HOST, PUERTO)
        cliente.connect(direccion_servidor)

        print("Para Subir la temperatura: S")
        print("Para Bajar la temperatura: B")
        opcion = input("Elección: ").upper()  # Convertir a mayúscula
        if opcion in ["S", "B"]:
            diferencia = "aumentar" if opcion == "S" else "disminuir"
            cliente.send(bytes(diferencia.encode()))

        cliente.close()
    except ConnectionError:
        print(f"No se pudo conectar a {HOST}:{PUERTO}. Intentar de vuelta...")

    time.sleep(1)
    system("clear")
