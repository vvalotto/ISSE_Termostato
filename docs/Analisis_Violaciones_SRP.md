# Análisis de Violaciones del Principio SRP (Single Responsibility Principle)

**Proyecto:** ISSE_Termostato
**Fecha:** Noviembre 2025
**Análisis realizado por:** Claude Code

---

## 🔴 VIOLACIONES CRÍTICAS

### 1. **ActuadorClimatizadorGeneral** (`agentes_actuadores/actuador_climatizador.py:11`)

**Responsabilidades identificadas:**
- ✗ Actuación del climatizador (escritura a archivo)
- ✗ Registro de errores
- ✗ Auditoría de operaciones

**Impacto:** Clase tiene 3 responsabilidades distintas. Cambios en el formato de auditoría o en el manejo de errores requieren modificar esta clase.

**Recomendación:** Extraer `registrar_error()` y `auditar_funcion()` a clases separadas (`RegistradorErrores`, `Auditor`).

---

### 2. **OperadorParalelo** (`servicios_aplicacion/operador_paralelo.py:12`)

**Responsabilidades identificadas:**
- ✗ Lectura de batería (línea 23)
- ✗ Lectura de temperatura ambiente (línea 30)
- ✗ Accionamiento del climatizador (línea 37)
- ✗ Presentación de parámetros (línea 44)
- ✗ Seteo de temperatura (línea 50)
- ✗ Gestión de threads (línea 57)

**Impacto:** God Class con 6 responsabilidades. Cualquier cambio en la lógica de ejecución, intervalos o coordinación afecta esta clase.

**Recomendación:** Usar patrón Command para encapsular cada operación. Extraer orquestación de threads a un `OrquestadorTareas`.

---

### 3. **SelectorTemperaturaArchivo** (`agentes_sensores/proxy_selector_temperatura.py:11`)

**Responsabilidades identificadas:**
- ✗ Lectura del archivo (línea 15)
- ✗ Construcción del mensaje de error (línea 33)
- ✗ Registro de errores (línea 44)

**Impacto:** Mezcla lógica de I/O con manejo de errores y registro.

**Recomendación:** Extraer registro a clase `RegistradorErrores` dedicada.

---

### 4. **Configurador** (`configurador/configurador.py:16`)

**Responsabilidades identificadas:**
- ✗ Carga del archivo JSON (línea 21)
- ✗ Validación de configuración (línea 116)
- ✗ Creación de objetos vía factories (líneas 35-68)
- ✗ Acceso a propiedades de configuración (líneas 71-113)

**Impacto:** God Object con 4 responsabilidades. Tiene 13 métodos diferentes, demasiada superficie de cambio.

**Recomendación:** Separar en:
- `CargadorConfiguracion`: solo carga y parseo JSON
- `ValidadorConfiguracion`: validación
- `ProveedorConfiguracion`: acceso a propiedades
- Mantener factories separadas (ya lo están)

---

## 🟠 VIOLACIONES MODERADAS

### 5. **Bateria** (`entidades/bateria.py:6`)

**Responsabilidades identificadas:**
- ✗ Almacenamiento de nivel de carga
- ✗ Cálculo del indicador BAJA/NORMAL (línea 18-23)

**Impacto:** La entidad tiene lógica de negocio (comparación con umbral) que debería estar en un servicio de dominio.

**Recomendación:** Extraer cálculo del indicador a `CalculadorIndicadorBateria` en `servicios_dominio/`.

---

### 6. **Climatizador** (`entidades/climatizador.py:45,82`)

**Responsabilidades identificadas:**
- ✗ Lógica de máquina de estados
- ✗ Evaluación de acciones
- ✗ **I/O de consola** (líneas 78, 106: `print('accion:', accion)`)

**Impacto:** Entidad de dominio mezclada con logging/debug. Viola la regla de que las entidades no deberían conocer infraestructura.

**Recomendación:** Eliminar prints o usar un logger inyectado.

---

### 7. **GestorAmbiente** (`gestores_entidades/gestor_ambiente.py:12`)

**Responsabilidades identificadas:**
- ✗ Gestión de la entidad Ambiente
- ✗ Coordinación con proxy de temperatura
- ✗ Coordinación con visualizador
- ✗ Acceso directo al Configurador (líneas 20, 23, 39, 44)

**Impacto:** Mezcla coordinación con acceso a configuración. El gestor no debería conocer al Configurador.

**Recomendación:** Inyectar configuración en el constructor en lugar de acceder al Configurador directamente.

---

### 8. **Inicializador** (`servicios_aplicacion/inicializador.py:4`)

**Responsabilidades identificadas:**
- ✗ Inicialización del sistema
- ✗ Validación de batería (línea 14-16)
- ✗ Validación de temperatura (línea 18-21)
- ✗ Limpieza de pantalla (línea 26: `system("clear")`)

**Impacto:** Mezcla lógica de aplicación con comandos del sistema operativo.

**Recomendación:** Extraer limpieza de pantalla a un servicio de UI separado.

---

### 9. **Presentador** (`servicios_aplicacion/presentador.py:6`)

**Responsabilidades identificadas:**
- ✗ Orquestación de visualización
- ✗ Formato de consola (líneas 28, 31-40: múltiples `print()`)

**Impacto:** Mezcla coordinación con formato de salida específico.

**Recomendación:** Extraer formato a un `FormateadorConsola` o usar un sistema de templates.

---

## 🟡 VIOLACIONES MENORES

### 10. **ProxySensorTemperaturaSocket / ProxyBateriaSocket**

**Responsabilidades identificadas:**
- ✗ Configuración de socket (líneas 27-33)
- ✗ Gestión de conexión
- ✗ Conversión de datos

**Impacto:** Manejo de socket mezclado con lógica de proxy.

**Recomendación:** Extraer configuración y gestión de sockets a una clase `GestorSockets` reutilizable.

---

### 11. **SelectorEntradaTemperatura** (`servicios_aplicacion/selector_entrada.py:8`)

**Responsabilidades identificadas:**
- ✗ Coordinación del seteo de temperatura
- ✗ Control del modo de visualización (línea 27-30)

**Impacto:** Mezcla lógica de seteo con visualización.

**Recomendación:** Separar lógica de visualización a otra clase.

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Clases Afectadas |
|-----------|----------|------------------|
| 🔴 Crítica | 4 | ActuadorClimatizadorGeneral, OperadorParalelo, SelectorTemperaturaArchivo, Configurador |
| 🟠 Moderada | 5 | Bateria, Climatizador, GestorAmbiente, Inicializador, Presentador |
| 🟡 Menor | 2 | Proxies Socket, SelectorEntradaTemperatura |
| **TOTAL** | **11** | |

---

## 💡 Recomendaciones Generales

1. **Separar Concerns de Logging/Auditoría**: Crear `RegistradorErrores` y `Auditor` como servicios transversales
2. **Extraer I/O del Dominio**: Las entidades (`Climatizador`, `Bateria`) no deben tener `print()` statements
3. **Reducir God Objects**: `Configurador` y `OperadorParalelo` necesitan refactoring urgente
4. **Dependency Injection**: Evitar acceso directo a `Configurador` desde gestores
5. **Principio de Composición**: Usar Command Pattern para tareas del `OperadorParalelo`

---

## 📋 Plan de Acción Sugerido

### Prioridad Alta (Críticas)

1. **Refactorizar OperadorParalelo**
   - Crear clases Command para cada tarea
   - Extraer `OrquestadorTareas` para manejo de threads
   - Estimar esfuerzo: 4-6 horas

2. **Dividir Configurador**
   - Crear `CargadorConfiguracion`, `ValidadorConfiguracion`, `ProveedorConfiguracion`
   - Actualizar referencias en todo el proyecto
   - Estimar esfuerzo: 3-4 horas

3. **Refactorizar ActuadorClimatizadorGeneral**
   - Extraer `RegistradorErrores` y `Auditor`
   - Usar inyección de dependencias
   - Estimar esfuerzo: 2-3 horas

4. **Limpiar SelectorTemperaturaArchivo**
   - Usar `RegistradorErrores` centralizado
   - Estimar esfuerzo: 1-2 horas

### Prioridad Media (Moderadas)

5. **Limpiar Entidades de Dominio**
   - Eliminar `print()` de `Climatizador`
   - Extraer cálculo de indicador de `Bateria` a servicio de dominio
   - Estimar esfuerzo: 2-3 horas

6. **Mejorar Gestores**
   - Inyectar configuración en constructores en lugar de acceso directo
   - Estimar esfuerzo: 2-3 horas

7. **Refactorizar Inicializador y Presentador**
   - Extraer UI concerns
   - Estimar esfuerzo: 2 horas

### Prioridad Baja (Menores)

8. **Crear GestorSockets reutilizable**
   - Centralizar configuración de sockets
   - Estimar esfuerzo: 2-3 horas

9. **Separar concerns en SelectorEntradaTemperatura**
   - Estimar esfuerzo: 1-2 horas

**Esfuerzo total estimado:** 19-29 horas

---

## 🎯 Conclusión

El proyecto muestra un buen uso de Clean Architecture y patrones de diseño, pero presenta **11 violaciones del principio SRP** que afectan la mantenibilidad del código. Las violaciones críticas se concentran principalmente en:

1. **Configurador**: God Object que necesita dividirse urgentemente
2. **OperadorParalelo**: God Class con demasiadas responsabilidades
3. **ActuadorClimatizadorGeneral**: Mezcla actuación con logging y auditoría
4. **Entidades de Dominio**: Contienen I/O que no deberían tener

La refactorización de estos componentes mejorará significativamente:
- **Testabilidad**: Clases más pequeñas son más fáciles de probar
- **Mantenibilidad**: Cambios localizados en una sola responsabilidad
- **Extensibilidad**: Más fácil agregar nuevas funcionalidades
- **Legibilidad**: Código más claro y fácil de entender

---

**Documento generado automáticamente mediante análisis estático del código.**
