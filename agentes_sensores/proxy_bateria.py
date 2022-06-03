"""
Segunda version: Nueva clase que lee de otra manera el dato de la bateria
Se extiende a otra clase sin tocar la primera
"""
import socket


class ProxyBateria:

    @staticmethod
    def leer_carga():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        :return: carga
        """
        carga = None
        archivo = open("bateria", "r")
        carga = float(archivo.read())
        archivo.close()
        return carga


class ProxyBateriaSocket:

    @staticmethod
    def leer_carga():
        """
        Aqui lee desde la GPIO el valor que indica la bateria
        :return: carga
        """
        carga = None

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
