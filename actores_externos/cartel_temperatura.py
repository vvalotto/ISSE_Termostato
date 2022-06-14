import socket
import time
from os import system


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
direccion_servidor = ('localhost', 14001)
servidor.bind(direccion_servidor)

servidor.listen(1)
temperatura = None

while True:
    print("Temperatura")
    print('-> ', temperatura, "\n")

    conexion, direccion_cliente = servidor.accept()
    try:
        while True:
            datos = conexion.recv(4096)
            if not datos:
                break
            temperatura = str(datos.decode("utf-8"))

    except ConnectionError("Error en la lectura de la temperatura"):
        conexion.close()
        print("FIN")

    time.sleep(1)
    system("clear")
