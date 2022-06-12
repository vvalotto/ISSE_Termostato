import socket
import time

"""
Simula el sensor físico, mediante socket
"""

while True:
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = ("localhost", 12000)
        cliente.connect(direccion_servidor)

        temperatura = input("Temperatura > ")
        cliente.send(bytes(temperatura.encode()))
        cliente.close()

    except ConnectionError:
        print("Intentar de vuelta")

    time.sleep(2)
