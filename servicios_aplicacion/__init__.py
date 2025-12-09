"""
Paquete de servicios de aplicacion del termostato.

Contiene los casos de uso y la logica de orquestacion del sistema:
    - inicializador: Inicializacion del sistema
    - lanzador: Punto de entrada principal
    - operador_paralelo: Ejecucion concurrente de tareas
    - operador_secuencial: Ejecucion secuencial de tareas
    - presentador: Presentacion de datos al usuario
    - selector_entrada: Seleccion de modo de temperatura
    - abs_selector_temperatura: Abstraccion del selector
    - abs_seteo_temperatura: Abstraccion del seteo
"""
# pylint: disable=consider-using-f-string
