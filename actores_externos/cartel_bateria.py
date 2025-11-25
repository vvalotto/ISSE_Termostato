import socket
import time
from os import system


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto
direccion_servidor = ('localhost', 14000)
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

    except ConnectionError as e:  # FIX: sintaxis correcta
        print(f"Error en la lectura de la carga: {e}")
    finally:  # FIX: Asegurar cierre de conexión
        conexion.close()

    time.sleep(1)
    system('clear')
