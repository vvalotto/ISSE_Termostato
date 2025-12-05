"""
Setup script para empaquetar ISSE_Termostato como paquete distribuible
Genera wheel para instalación en Raspberry Pi
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else "Sistema de Control de Climatización para Raspberry Pi"

# Versión del proyecto
VERSION = "1.0.0"

setup(
    name="termostato-core",
    version=VERSION,
    author="Victor Valotto",
    author_email="vvalotto@example.com",
    description="Sistema de Control de Climatización embebido para Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vvalotto/ISSE_Termostato",

    # Paquetes a incluir (solo CORE, sin actores_externos ni Test)
    packages=find_packages(
        where='.',
        include=[
            'entidades*',
            'servicios_dominio*',
            'gestores_entidades*',
            'servicios_aplicacion*',
            'agentes_sensores*',
            'agentes_actuadores*',
            'configurador*',
            'registrador*'
        ],
        exclude=['Test*', 'actores_externos*', 'docs*']
    ),

    # Módulos Python individuales (no en paquetes)
    py_modules=['ejecutar'],

    # Archivos de datos
    package_data={
        'configurador': ['termostato.json'],
    },

    # Scripts ejecutables
    entry_points={
        'console_scripts': [
            'termostato=ejecutar:main',
        ],
    },

    # Dependencias (solo stdlib, sin dependencias externas)
    install_requires=[
        # Ninguna! Solo usa bibliotecas estándar de Python
    ],

    # Dependencias opcionales para desarrollo
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'radon>=5.1.0',
            'pylint>=2.15.0',
        ],
        'rpi': [
            # Librerías específicas de Raspberry Pi (opcionales)
            # 'RPi.GPIO>=0.7.1',  # Solo si usas GPIO
            # 'adafruit-circuitpython-dht',  # Para sensor DHT22
        ],
    },

    # Clasificadores
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],

    # Versión mínima de Python
    python_requires='>=3.5',

    # Metadata adicional
    keywords="termostato raspberry-pi control climatizacion embebido iot",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/ISSE_Termostato/issues",
        "Source": "https://github.com/vvalotto/ISSE_Termostato",
        "Documentation": "https://github.com/vvalotto/ISSE_Termostato/docs",
    },

    # Licencia
    license="MIT",
)
