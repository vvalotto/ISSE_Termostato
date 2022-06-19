from servicios_aplicacion.lanzador import *
from configurador.configurador import *

if __name__ == "__main__":
    Configurador().cargar_configuracion()
    Lanzador().ejecutar()