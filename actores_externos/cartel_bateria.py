import socket
import time
from os import system


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
direccion_servidor = ('localhost', 13005)
servidor.bind(direccion_servidor)

servidor.listen(1)

tension = None
while True:
    print("Tension de la batería")
    print('-> ', tension, "\n")

    conexion, direccion_cliente = servidor.accept()

    try:
        while True:
            datos = conexion.recv(4096)
            if not datos:
                break
            tension = str(datos.decode("utf-8"))

    except ConnectionError("Error en la lectura de la carga"):
        conexion.close()
        print("FIN")

    time.sleep(1)
    system('clear')
