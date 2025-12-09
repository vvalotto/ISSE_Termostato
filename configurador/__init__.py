"""
Paquete de configuracion y fabricas del termostato.

Contiene las fabricas (factories) para crear instancias
de los componentes del sistema segun la configuracion:
    - configurador: Configurador principal del sistema
    - factory_climatizador: Fabrica de climatizadores
    - factory_actuador_climatizador: Fabrica de actuadores
    - factory_proxy_bateria: Fabrica de proxies de bateria
    - factory_selector_temperatura: Fabrica de selectores
    - factory_sensor_temperatura: Fabrica de sensores
    - factory_seteo_temperatura: Fabrica de seteo
    - factory_visualizador_bateria: Fabrica de visualizadores de bateria
    - factory_visualizador_climatizador: Fabrica de visualizadores de climatizador
    - factory_visualizador_temperatura: Fabrica de visualizadores de temperatura
"""
# pylint: disable=consider-using-f-string
