"""
Display de estado del climatizador via socket TCP.

Este script actua como servidor socket que recibe y muestra
en consola el estado actual del climatizador (calentando,
enfriando, apagado).
"""
# pylint: disable=invalid-name,duplicate-code
# Las variables de script (estado, etc.) son mutables, no constantes.
# El codigo duplicado entre carteles es aceptable (scripts independientes).

import socket
import time
from os import system

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar puerto
direccion_servidor = ('localhost', 14002)
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

    except ConnectionError as e:  # FIX: sintaxis correcta
        print(f"Error en la lectura del estado: {e}")
    finally:  # FIX: Asegurar cierre de conexión
        conexion.close()

    time.sleep(1)
    system("clear")
