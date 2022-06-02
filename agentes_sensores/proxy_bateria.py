"""
Segunda version: lee desde otra fuente de datos
"""
import socket


class ProxyBateria:

    # Se cambia el contrato!!!!
    @staticmethod
    def leer_carga(tipo_proxy):
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        :return: carga
        """
        carga = None

        # Lee la simulacion desde un archivo
        if tipo_proxy == "archivo":
            archivo = open("bateria", "r")
            carga = float(archivo.read())
            archivo.close()

        # Lee la simulación desde un ingreso de datos cliente
        elif tipo_proxy == "socket":
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            direccion_servidor = ('localhost', 11000)
            servidor.bind(direccion_servidor)

            servidor.listen(1)
            conexion, direccion_cliente = servidor.accept()

            try:
                while True:
                    datos = conexion.recv(4096)
                    if not datos:
                        break
                    carga = float(datos.decode("utf-8"))
            except ConnectionError("Error en la lectura de la carga"):
                conexion.close()
                print("FIN")

        return carga
