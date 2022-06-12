import socket
import time
from os import system

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
direccion_servidor = ('localhost', 13002)
servidor.bind(direccion_servidor)

servidor.listen(1)
estado = None

while True:
    print("Climatizador")
    print('-> ', estado, "\n")

    conexion, direccion_cliente = servidor.accept()
    try:
        while True:
            datos = conexion.recv(4096)
            if not datos:
                break
            estado = str(datos.decode("utf-8"))

    except ConnectionError("Error en la lectura del estado"):
        conexion.close()
        print("FIN")

    time.sleep(1)
    system("clear")