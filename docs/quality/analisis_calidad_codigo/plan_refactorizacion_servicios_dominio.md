and# PLAN DE REFACTORIZACION: servicios_dominio

**Proyecto**: ISSE_Termostato
**Paquete**: servicios_dominio
**Fecha**: 2025-12-07
**Estado**: Planificado

---

## 1. ESTADO ACTUAL (PRE-REFACTORIZACION)

### 1.1 Archivos del Paquete

| Archivo | LOC | SLOC | Clases | Metodos |
|---------|-----|------|--------|---------|
| controlador_climatizador.py | 31 | 11 | 1 | 1 |
| **TOTAL** | **31** | **11** | **1** | **1** |

**Nota**: Este es un paquete muy pequeno con un solo archivo y una sola clase.

### 1.2 Metricas Actuales

| Metrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| CC Promedio | 3.5 | <= 5 | ✅ Bueno |
| MI | 85.45 | >= 65 | ✅ Excelente |
| Documentacion | 42% | >= 70% | ⚠️ Mejorable |
| Pylint Score | 0.00/10 | >= 8.0 | ❌ Critico |
| Issues Pylint | 9 | <= 5 | ❌ Alto |

### 1.3 Distribucion de Issues Pylint

| Tipo | Cantidad | Issues Principales |
|------|----------|-------------------|
| Convention (C) | 7 | line-too-long (1), superfluous-parens (2), missing-class-docstring (1), import-outside-toplevel (1), multiple-statements (2) |
| Error (E) | 1 | import-error (1) |
| Refactor (R) | 1 | too-few-public-methods (1 - aceptable para clase utilitaria) |
| **TOTAL** | **9** | - |

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Violacion DIP (Dependency Inversion Principle)

**Problema**: Import interno de `Configurador` dentro del metodo.

```python
# ACTUAL - Viola DIP
@staticmethod
def comparar_temperatura(temperatura_actual, temperatura_deseada):
    from configurador.configurador import Configurador  # Import interno!
    histeris = Configurador.obtener_histeresis()
    ...
```

**Impacto**:
- Acoplamiento oculto a Configurador
- Dificil de testear sin la configuracion real
- Import fuera del toplevel (mala practica)

### 2.2 Problemas de Estilo

| Problema | Linea | Descripcion |
|----------|-------|-------------|
| Line too long | 19 | Linea > 100 caracteres |
| Superfluous parens | 29, 30 | Parentesis innecesarios en `if` |
| Multiple statements | 29, 30 | Multiples sentencias en una linea |
| Missing class docstring | 7 | Clase sin docstring |

### 2.3 Codigo No Pythonico

```python
# ACTUAL - No pythonico
if (limite_superior < temperatura_actual): temperatura = "alta"
if (limite_inferior > temperatura_actual): temperatura = "baja"

# MEJOR - Pythonico
if limite_superior < temperatura_actual:
    temperatura = "alta"
elif limite_inferior > temperatura_actual:
    temperatura = "baja"
```

---

## 3. PLAN DE MEJORAS

### 3.1 Resumen de Cambios

| # | Cambio | Prioridad | Complejidad |
|---|--------|-----------|-------------|
| 1 | Inyeccion de histeresis como parametro | ALTA | Baja |
| 2 | Documentacion completa (docstrings) | ALTA | Baja |
| 3 | Formateo pythonico (if statements) | MEDIA | Baja |
| 4 | Eliminar parentesis innecesarios | BAJA | Baja |

---

### 3.2 Cambio 1: Inyeccion de Histeresis

**Objetivo**: Aplicar DIP - Recibir histeresis como parametro en lugar de obtenerla internamente.

```python
# ANTES
@staticmethod
def comparar_temperatura(temperatura_actual, temperatura_deseada):
    from configurador.configurador import Configurador
    histeris = Configurador.obtener_histeresis()
    ...

# DESPUES
@staticmethod
def comparar_temperatura(temperatura_actual, temperatura_deseada, histeresis=2):
    """
    Compara la temperatura actual con la deseada usando histeresis.

    Args:
        temperatura_actual (float): Temperatura ambiente en grados Celsius.
        temperatura_deseada (float): Temperatura objetivo en grados Celsius.
        histeresis (float): Margen de tolerancia en grados. Por defecto 2.

    Returns:
        str: "alta", "baja" o "normal" segun la comparacion.
    """
    limite_superior = temperatura_deseada + histeresis
    limite_inferior = temperatura_deseada - histeresis

    if temperatura_actual > limite_superior:
        return "alta"
    elif temperatura_actual < limite_inferior:
        return "baja"
    return "normal"
```

**Nota**: Este cambio requiere actualizar los llamadores para pasar la histeresis.

---

### 3.3 Cambio 2: Documentacion Completa

**Objetivo**: Agregar docstrings a clase y metodos.

```python
"""
Servicio de dominio para control de temperatura.

Este modulo contiene la logica de negocio para comparar temperaturas
y determinar el estado termico del ambiente (alta, baja, normal).

Patron de Diseno:
    - Service: Encapsula logica de dominio sin estado
    - Strategy: El algoritmo de comparacion puede variar
"""


class ControladorTemperatura:
    """
    Servicio de dominio para comparacion de temperaturas.

    Implementa el algoritmo de histeresis para determinar si la
    temperatura actual esta por encima, por debajo o dentro del
    rango aceptable respecto a la temperatura deseada.

    La histeresis evita oscilaciones frecuentes del climatizador
    al crear una "zona muerta" alrededor de la temperatura deseada.

    Example:
        >>> ControladorTemperatura.comparar_temperatura(25, 22, histeresis=2)
        'alta'  # 25 > 22+2=24
        >>> ControladorTemperatura.comparar_temperatura(22, 22, histeresis=2)
        'normal'  # 20 <= 22 <= 24
    """
```

---

### 3.4 Cambio 3: Formateo Pythonico

**Objetivo**: Usar estilo Pythonico en condicionales.

```python
# ANTES
temperatura = "normal"
if (limite_superior < temperatura_actual): temperatura = "alta"
if (limite_inferior > temperatura_actual): temperatura = "baja"
return temperatura

# DESPUES
if temperatura_actual > limite_superior:
    return "alta"
elif temperatura_actual < limite_inferior:
    return "baja"
return "normal"
```

---

## 4. IMPACTO EN OTROS PAQUETES

### 4.1 Archivos que Usan ControladorTemperatura

El metodo `comparar_temperatura` es usado por:

| Paquete | Archivo | Cambio Requerido |
|---------|---------|------------------|
| entidades | climatizador.py | Pasar histeresis al llamar |
| Test | test_controlador_temperatura.py | Ya pasan histeresis (no requiere cambio) |

**Nota**: Los tests unitarios ya funcionan sin Configurador porque prueban valores especificos.

---

## 5. ORDEN DE EJECUCION

### Fase 1: Documentacion y Formateo (sin romper funcionalidad)
1. [ ] Agregar docstrings a modulo y clase
2. [ ] Formatear condicionales (estilo pythonico)
3. [ ] Eliminar parentesis innecesarios
4. [ ] Verificar que tests pasan

### Fase 2: Inyeccion de Dependencias
5. [ ] Agregar parametro `histeresis` con valor por defecto
6. [ ] Eliminar import interno de Configurador
7. [ ] Actualizar llamadores en `climatizador.py`
8. [ ] Verificar que tests pasan

---

## 6. METRICAS OBJETIVO (POST-REFACTORIZACION)

| Metrica | Actual | Objetivo |
|---------|--------|----------|
| CC Promedio | 3.5 | <= 3 (reducir con early return) |
| MI | 85.45 | >= 80 (mantener) |
| Documentacion | 42% | >= 70% |
| Pylint Score | 0.00 | >= 9.0 |
| Issues Pylint | 9 | <= 2 |

---

## 7. RIESGOS Y MITIGACION

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Romper climatizador.py | Media | Alto | Actualizar llamada junto con el cambio |
| Tests fallen | Baja | Medio | Tests ya usan valores explicitos |

---

## 8. VERIFICACION

### Checklist Post-Refactorizacion

- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integracion pasan
- [ ] CC Promedio <= 3
- [ ] MI >= 80
- [ ] Documentacion >= 70%
- [ ] Pylint Score >= 9.0
- [ ] Sin import interno de Configurador

---

*Documento generado: 2025-12-07*
