"""
Paquete de agentes sensores del termostato.

Contiene los proxies que comunican con los sensores fisicos
o simulados via socket TCP:
    - proxy_bateria: Proxy del sensor de bateria
    - proxy_sensor_temperatura: Proxy del sensor de temperatura
    - proxy_selector_temperatura: Proxy del selector de modo
    - proxy_seteo_temperatura: Proxy del seteo de temperatura
"""
# pylint: disable=consider-using-f-string,duplicate-code
