from setuptools import setup

setup(
    name='configurador',
    version='1.0.0',
    description='Inicializador de la componentes de la aplicacion',
    author='VOV',
    packages=['configurador'],
    install_requires=['entidades', 'servicios_aplicacion'],
)
