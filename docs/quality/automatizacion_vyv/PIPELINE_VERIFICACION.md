# Pipeline de Verificación de Calidad

## ¿Qué es esto?

Un **sistema automatizado** que verifica la calidad de tu código antes de considerar una pieza de software como "terminada".

## ¿Cómo funciona?

```
┌─────────────────┐
│  1. Escribes    │
│     código      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  2. Ejecutas    │
│  verificación   │
└────────┬────────┘
         │
         ↓
    python verificar_calidad.py
         │
         ↓
┌─────────────────────────────────┐
│  Se ejecutan automáticamente:   │
│                                  │
│  ✓ Tests unitarios               │
│  ✓ Tests de integración          │
│  ✓ Cobertura de código           │
│  ✓ Estilo (PEP8)                 │
│  ✓ Complejidad ciclomática       │
│  ✓ Métricas de calidad           │
│  ✓ Arquitectura limpia           │
└─────────────────────────────────┘
         │
         ↓
    ¿Todas pasan?
         │
    ┌────┴────┐
   NO          SÍ
    │           │
    ↓           ↓
  FALLA     ✅ LISTO
    │         para
    │        commit
    ↓
Refactoriza
```

## Instalación

### 1. Hacer el script ejecutable

```bash
chmod +x verificar_calidad.py
```

### 2. Instalar dependencias (si no las tienes)

```bash
pip install pytest pytest-cov flake8 radon
```

## Uso

### Verificación Completa

Ejecuta todas las verificaciones:

```bash
python verificar_calidad.py
```

### Verificación Rápida

Solo tests y estilo (más rápido):

```bash
python verificar_calidad.py --rapido
```

### Solo Tests

```bash
python verificar_calidad.py --solo-tests
```

## ¿Qué verifica?

### ✅ Verificaciones Bloqueantes

Estas **DEBEN pasar** para considerar el código listo:

1. **Tests Unitarios e Integración**
   - Todos los tests deben pasar
   - Si falla alguno → PIPELINE FALLA

2. **Cobertura de Código**
   - Mínimo 70% de cobertura
   - Si es menor → PIPELINE FALLA

### ⚠️ Verificaciones No Bloqueantes (Warnings)

Estas se reportan pero NO fallan el pipeline:

3. **Estilo de Código (flake8)**
   - Verifica PEP8
   - Detecta líneas muy largas
   - Complejidad ciclomática básica

4. **Métricas de Complejidad (radon)**
   - Complejidad ciclomática por función
   - Promedio del proyecto

5. **Métricas Personalizadas**
   - Herencia
   - DSM
   - Clean Architecture
   - Acoplamiento
   - Cohesión

6. **Clean Architecture**
   - Violaciones de capas
   - Ciclos de dependencias

## Ejemplo de Salida

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🚀 PIPELINE DE VERIFICACIÓN DE CALIDAD                  ║
║              ISSE_Termostato                                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

======================================================================
🔧 Tests Unitarios e Integración
======================================================================

Test session starts...
collected 183 items

Test/unit/entidades/test_bateria.py ........         [  4%]
Test/unit/entidades/test_climatizador.py ..........  [ 10%]
...

✅ Tests Unitarios e Integración - OK

======================================================================
🔧 Cobertura de Código
======================================================================

---------- coverage: platform darwin, python 3.x -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
entidades/ambiente.py                      25      2    92%
entidades/bateria.py                       18      1    94%
...
-----------------------------------------------------------
TOTAL                                     856     98    89%

✅ Cobertura de Código - OK

...

======================================================================
📋 RESUMEN DE VERIFICACIÓN
======================================================================

✅  Tests Unitarios e Integración          OK
✅  Cobertura de Código                    OK
⚠️   Estilo de Código (flake8)             WARNING
✅  Métricas de Complejidad (radon)        OK
ℹ️   Métricas Personalizadas               INFO
⚠️   Clean Architecture                    WARNING

======================================================================
✅ OK: 4  |  ❌ Fallos: 0  |  ⚠️  Warnings: 2
⏱️  Duración: 12.34s
======================================================================

✅ PIPELINE COMPLETADO
   Todas las verificaciones bloqueantes pasaron
   Nota: 2 warnings encontrados

   🎉 La pieza de software está lista para commit
```

## Ejemplo de Fallo

```
======================================================================
🔧 Tests Unitarios e Integración
======================================================================

Test session starts...
collected 183 items

Test/unit/entidades/test_bateria.py .....F..     [  4%]

FAILED Test/unit/entidades/test_bateria.py::test_carga_invalida

❌ Tests Unitarios e Integración - FALLÓ

======================================================================
📋 RESUMEN DE VERIFICACIÓN
======================================================================

❌  Tests Unitarios e Integración          FALLO [BLOQUEANTE]

======================================================================
✅ OK: 0  |  ❌ Fallos: 1  |  ⚠️  Warnings: 0
⏱️  Duración: 2.15s
======================================================================

❌ PIPELINE FALLÓ
   1 verificaciones bloqueantes fallaron
   ⚠️  La pieza de software NO está lista
```

## Integración con Git

### Opción 1: Manual

Ejecutar antes de cada commit:

```bash
python verificar_calidad.py
git add .
git commit -m "mensaje"
```

### Opción 2: Pre-commit Hook (Automático)

Crear archivo `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🔍 Ejecutando verificación de calidad..."
python verificar_calidad.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Verificación falló. Commit cancelado."
    echo "   Corrige los errores y vuelve a intentar."
    exit 1
fi

echo ""
echo "✅ Verificación exitosa. Procediendo con commit..."
```

Hacer ejecutable:

```bash
chmod +x .git/hooks/pre-commit
```

Ahora cada vez que hagas `git commit`, se ejecutará automáticamente el pipeline.

## Configuración de Umbrales

Puedes ajustar los umbrales editando `verificar_calidad.py`:

```python
# En la función verificar_cobertura():
"--cov-fail-under=70"  # Cambiar a 80, 90, etc.

# En la función verificar_estilo():
"--max-complexity=10"  # Cambiar a 15, 20, etc.
"--max-line-length=100"  # Cambiar a 120, 150, etc.
```

## Workflow Recomendado

### Para una Nueva Feature

```bash
# 1. Crear rama
git checkout -b feature/nueva-funcionalidad

# 2. Escribir tests
# Crear test_nueva_funcionalidad.py

# 3. Implementar código
# Crear nueva_funcionalidad.py

# 4. Verificar calidad
python verificar_calidad.py

# 5. Si pasa, commit
git add .
git commit -m "feat: nueva funcionalidad"

# 6. Si falla, refactorizar y volver al paso 4
```

### Para un Bug Fix

```bash
# 1. Reproducir bug con test
# Agregar test que falla

# 2. Verificar que test falla
pytest Test/test_bug.py

# 3. Corregir bug

# 4. Verificar calidad completa
python verificar_calidad.py

# 5. Commit si pasa
git commit -m "fix: corrección de bug X"
```

## Preguntas Frecuentes

### ¿Puedo saltarme las verificaciones?

Técnicamente sí, pero **NO es recomendable**. Si necesitas hacer un commit urgente:

```bash
git commit --no-verify -m "WIP: trabajo en progreso"
```

Pero deberías corregirlo después.

### ¿Puedo personalizar qué verificaciones se ejecutan?

Sí, edita el método `ejecutar_pipeline_completo()` en `verificar_calidad.py`.

### ¿Qué hago si tengo muchos warnings?

Los warnings no bloquean el commit, pero deberías:
1. Crear tickets/issues para corregirlos
2. Mejorarlos progresivamente
3. Eventualmente convertirlos en bloqueantes

### ¿Cuánto tiempo tarda?

- **Verificación rápida**: 5-15 segundos
- **Verificación completa**: 15-60 segundos

Depende del tamaño del proyecto y número de tests.

## Próximos Pasos

1. **Ejecuta el pipeline** en tu código actual
2. **Corrige los errores** bloqueantes
3. **Documenta los warnings** para corregirlos después
4. **Establece una regla**: No hacer commit sin pasar el pipeline
5. **Opcional**: Configura pre-commit hooks para automatizar

## Soporte

Si tienes problemas:
1. Revisa que las dependencias estén instaladas
2. Verifica que estás en el directorio correcto
3. Revisa los mensajes de error específicos
4. Ajusta umbrales si son demasiado estrictos inicialmente
