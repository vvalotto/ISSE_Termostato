"""
Clase para realizar el registro de auditoria y excepciones
"""


class Registrador:

    @staticmethod
    def registrar_error(clase, metodo, fecha_hora,
                        tipo_de_error, mensaje):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "metodo: " + metodo + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "tipo_de_error: " + tipo_de_error + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "-------------------------" + "\n" + "\n" + "\n"

        try:
            with open("registro_errores", "a") as archivo_errores:
                archivo_errores.write(registro)
                archivo_errores.close()
        except IOError:
            raise "Error al escribir el archivo de errores: " + str(IOError.errno)

    @staticmethod
    def auditar_funcion(clase, mensaje, fecha_hora):
        registro = ""
        registro += "clase: " + clase + "\n"
        registro += "fecha_hora: " + fecha_hora + "\n"
        registro += "mensaje: " + mensaje + "\n"
        registro += "*************" + "\n" + "\n" + "\n"

        try:
            with open("registro_auditoria", "a") as archivo_auditoria:
                archivo_auditoria.write(registro)
                archivo_auditoria.close()
        except IOError:
            raise "Error al escribir el archivo de auditoria: " + str(IOError.errno)
