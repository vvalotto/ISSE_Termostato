import socket
import time

"""
Simula la bateria fisica, mediante socket
"""

while True:
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = ("localhost", 11000)
        cliente.connect(direccion_servidor)

        carga = input("Carga > ")
        cliente.send(bytes(carga.encode()))
        cliente.close()

    except ConnectionError:
        print("Intentar de vuelta")

    time.sleep(2)
