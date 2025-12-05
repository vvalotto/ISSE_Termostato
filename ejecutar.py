from servicios_aplicacion.lanzador import *
from configurador.configurador import *

def main():
    """Punto de entrada principal del sistema de termostato"""
    Configurador().cargar_configuracion()
    Lanzador().ejecutar()

if __name__ == "__main__":
    main()