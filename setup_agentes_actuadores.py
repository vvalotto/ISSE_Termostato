from setuptools import setup

setup(
    name='agentes_actuadores',
    version='1.0.0',
    description='Modulos que interfacean actuando sobre el ambiente',
    author='VOV',
    packages=['agentes_actuadores'],
    install_requires=['entidades', 'servicios_aplicacion'],
)
