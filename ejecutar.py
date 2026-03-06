import logging
from servicios_aplicacion.lanzador import Lanzador
from configurador.configurador import Configurador

def main():
    """Punto de entrada principal del sistema de termostato"""
    # Configurar logging para toda la aplicación
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('termostato.log'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("=== Iniciando sistema de termostato ===")

    Configurador.cargar_configuracion()
    Lanzador().ejecutar()

if __name__ == "__main__":
    main()