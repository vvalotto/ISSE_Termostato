import socket
import time
import json
import os

"""
Simula el sensor físico de temperatura, mediante socket
"""

# Cargar configuración (buscar en directorio actual o padre)
config_file = "simuladores_config.json"
if not os.path.exists(config_file):
    config_file = os.path.join("..", "simuladores_config.json")

with open(config_file, "r") as f:
    config = json.load(f)

HOST = config["raspberry_pi"]["host"]
PUERTO = config["raspberry_pi"]["puertos"]["temperatura"]

while True:
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = (HOST, PUERTO)
        cliente.connect(direccion_servidor)

        temperatura = input("Temperatura (°C) > ")
        cliente.send(bytes(temperatura.encode()))
        cliente.close()

    except ConnectionError:
        print(f"No se pudo conectar a {HOST}:{PUERTO}. Intentar de vuelta...")

    time.sleep(2)
