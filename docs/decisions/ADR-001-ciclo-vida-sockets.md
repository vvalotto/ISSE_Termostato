# ADR-001: Ciclo de vida de conexiones socket en proxies de sensores

**Estado:** Aceptado
**Fecha:** 2026-03-06
**Autores:** Equipo ISSE Termostato

---

## Contexto

El sistema utiliza sockets TCP para comunicarse con actores externos (sensores y controles de usuario). Existen dos familias de proxies con comportamiento diferente en cuanto al ciclo de vida de la conexión socket:

- **Proxies de sensores periódicos** (`ProxyBateriaSocket`, `ProxySensorTemperaturaSocket`): son consultados en un loop continuo por los gestores del sistema.
- **Proxies de comandos de usuario** (`SeteoTemperaturaSocket`, `SelectorTemperaturaSocket`): reciben comandos esporádicos del usuario (aumentar/disminuir temperatura, cambiar modo de visualización).

Durante la revisión de calidad (TKT-06) se detectó que ambas familias implementan estrategias distintas de ciclo de vida del socket sin documentación explícita de la razón.

---

## Decisión

Se mantienen **dos estrategias diferenciadas** según el patrón de uso de cada proxy:

### Estrategia A — Socket efímero (proxies de sensores periódicos)

**Aplica a:** `ProxyBateriaSocket`, `ProxySensorTemperaturaSocket`

El socket TCP se crea, usa y cierra en cada llamada al método de lectura.

**Justificación:**
- Los sensores son consultados periódicamente por el sistema (loop continuo).
- El actor externo (simulador) actúa como servidor persistente que siempre está disponible.
- Crear una nueva conexión en cada ciclo es simple, predecible y no genera estado que gestionar entre llamadas.
- Si el servidor externo se reinicia, la próxima lectura se reconecta automáticamente sin lógica adicional de reconexión.

### Estrategia B — Socket persistente (proxies de comandos de usuario)

**Aplica a:** `SeteoTemperaturaSocket`, `SelectorTemperaturaSocket`

El socket TCP se crea al inicializar el proxy y se mantiene abierto entre llamadas.

**Justificación:**
- Los comandos de usuario son esporádicos e impredecibles en el tiempo.
- Mantener la conexión abierta permite recibir un comando en cualquier momento sin latencia de handshake.
- El proxy actúa como servidor (bind/listen/accept), lo que requiere que el socket esté activo permanentemente para no perder comandos que lleguen entre ciclos de consulta.
- Cerrar y reabrir el socket en cada ciclo implicaría una ventana de tiempo donde los comandos podrían perderse.

---

## Opciones consideradas

| Opción | Descripción | Motivo de descarte |
|--------|-------------|-------------------|
| Unificar en efímero | Todos los sockets se crean/destruyen por llamada | No aplica a comandos: el servidor de seteo/selector está del lado del proxy, no del actor externo |
| Unificar en persistente | Todos los sockets mantienen conexión permanente | Agrega complejidad de reconexión innecesaria en sensores periódicos |
| **Mantener diferencia documentada** | Cada familia usa la estrategia adecuada a su patrón de uso | **Seleccionada** |

---

## Consecuencias

- El código de ambas familias es intencionalmente diferente: no es inconsistencia sino una decisión de diseño.
- Los docstrings de cada clase socket hacen referencia explícita a este ADR y a la estrategia que implementan.
- TKT-07 aborda el manejo determinista de recursos en los sockets persistentes (`__enter__`/`__exit__`).
