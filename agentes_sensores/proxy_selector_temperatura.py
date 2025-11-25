"""
Clase que simula la lectura de un boton de seleccion
"""

from registrador.registrador import *
from servicios_aplicacion.abs_selector_temperatura import *
import datetime
import socket


class SelectorTemperaturaArchivo(AbsSelectorTemperatura, AbsRegistrador):

    @staticmethod
    def obtener_selector():
        try:
            archivo = open("tipo_temperatura", "r")
            tipo_temperatura = str(archivo.read()).strip()  # FIX: eliminar espacios/saltos de línea
            archivo.close()
        except IOError:
            mensaje_error = "Error al leer el tipo de temperatura"
            registro_error = SelectorTemperaturaArchivo._armar_registro_error(
                                                        SelectorTemperaturaArchivo.__name__,
                                                        SelectorTemperaturaArchivo.obtener_selector.__name__,
                                                        str(datetime.datetime.now()),
                                                        str(IOError),
                                                        mensaje_error)

            SelectorTemperaturaArchivo.registrar_error(registro_error)
            raise mensaje_error
        return tipo_temperatura

    @staticmethod
    def _armar_registro_error(clase, metodo, fecha_hora, tipo_de_error, mensaje):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "metodo: " + metodo + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "tipo_de_error: " + tipo_de_error + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "-------------------------" + "\n" + "\n" + "\n"
        return registro

    @staticmethod
    def registrar_error(registro):
        try:
            with open("registro_errores", "a") as archivo_errores:
                archivo_errores.write(registro)
                archivo_errores.close()
        except IOError:
            raise "Error al escribir el archivo de errores: " + str(IOError.errno)


class SelectorTemperaturaSocket(AbsSelectorTemperatura):

    def __init__(self):
        """Inicializa el socket persistente y el estado"""
        from configurador.configurador import Configurador

        self._estado_actual = "ambiente"  # Estado inicial
        self._servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = Configurador.obtener_host_escucha()
        puerto = Configurador.obtener_puerto("selector_temperatura")
        direccion_servidor = (host, puerto)
        self._servidor.bind(direccion_servidor)
        self._servidor.listen(1)

        self._conexion = None
        self._servidor.settimeout(1.0)  # Timeout para accept

    def obtener_selector(self):
        """
        Consulta no-bloqueante del selector.
        Retorna el estado actual sin bloquearse si no hay cambios.
        """
        try:
            # Si no hay conexión activa, intentar aceptar una (con timeout)
            if self._conexion is None:
                try:
                    self._conexion, _ = self._servidor.accept()
                    self._conexion.settimeout(0.1)  # Timeout corto para recv
                except socket.timeout:
                    # No hay cliente intentando conectar, devolver estado actual
                    return self._estado_actual

            # Intentar leer datos (no bloqueante)
            try:
                datos = self._conexion.recv(4096)
                if datos:
                    nuevo_estado = str(datos.decode("utf-8"))
                    self._estado_actual = nuevo_estado
                    print(f"[Selector] Cambio a modo: {self._estado_actual.upper()}")
                else:
                    # Cliente cerró conexión
                    self._conexion.close()
                    self._conexion = None
            except socket.timeout:
                # No hay datos nuevos, mantener estado actual
                pass
            except ConnectionError as e:
                print(f"[Selector] Error de conexión: {e}")
                if self._conexion:
                    self._conexion.close()
                self._conexion = None

        except Exception as e:
            print(f"[Selector] Error: {e}")

        return self._estado_actual

    def __del__(self):
        """Limpieza al destruir el objeto"""
        if self._conexion:
            self._conexion.close()
        if self._servidor:
            self._servidor.close()
