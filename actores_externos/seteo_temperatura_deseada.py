import socket
import time
from os import system
"""
Objeto que hace de botones o selectores para el
seteo de la temperatura deseada
"""

while True:
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direccion_servidor = ("localhost", 14000)
        cliente.connect(direccion_servidor)

        print("Para aumentar la temperatura >")
        print("Para disminuir la temperatura <")
        opcion = input("Elección: ")
        if opcion in [">", "<"]:
            diferencia = "aumentar" if opcion == ">" else "disminuir"
            cliente.send(bytes(diferencia.encode()))

        cliente.close()
    except ConnectionError:
        print("Intentar de vuelta")

    time.sleep(1)
    system("clear")
