# Pipeline de Validación (BDD) - Historias de Usuario

## ¿Qué es esto?

Un **pipeline de validación** que verifica automáticamente que tu implementación **cumple con los requisitos funcionales** especificados en las historias de usuario usando **BDD (Behavior-Driven Development)**.

## Diferencia con Pipeline de Verificación

| Aspecto | Pipeline Verificación | Pipeline Validación |
|---------|----------------------|---------------------|
| **Pregunta** | ¿Está bien construido? | ¿Hace lo que debe hacer? |
| **Enfoca en** | Calidad técnica | Requisitos de negocio |
| **Usa** | Tests unitarios, métricas | Tests de aceptación BDD |
| **Cuando** | Durante desarrollo | Al completar historia |
| **Valida** | Código, diseño | Comportamiento, funcionalidad |

---

## Flujo de Trabajo con BDD

```
1. Historia de Usuario
   ↓
2. Criterios de Aceptación
   ↓
3. Escenarios BDD (Given-When-Then)
   ↓
4. Implementar Steps
   ↓
5. Implementar Código
   ↓
6. Ejecutar Pipeline Validación
   ↓
7. ¿Todos los escenarios pasan? → ✅ Historia COMPLETADA
```

---

## Instalación

### 1. Instalar behave (framework BDD para Python)

```bash
pip install behave
```

### 2. Hacer script ejecutable

```bash
chmod +x validar_historia.py
```

### 3. Crear estructura BDD

```bash
python validar_historia.py
```

Esto creará automáticamente:
```
features/
├── ejemplo.feature           # Feature de ejemplo
└── steps/
    ├── __init__.py
    └── ejemplo_steps.py      # Steps de ejemplo
```

---

## Sintaxis BDD (Gherkin)

### Estructura de un Feature

```gherkin
Feature: Nombre de la Feature
  Como [rol]
  Quiero [funcionalidad]
  Para [beneficio]

  Background:                  # Setup común (opcional)
    Given [contexto inicial]

  Scenario: Descripción del escenario
    Given [contexto/precondición]
    When [acción]
    Then [resultado esperado]
    And [resultado adicional]
```

### Palabras Clave

- **Feature**: Agrupa escenarios relacionados (una historia de usuario)
- **Scenario**: Un caso de prueba específico
- **Background**: Setup común para todos los scenarios
- **Given**: Establece el contexto inicial (precondiciones)
- **When**: La acción que se ejecuta
- **Then**: El resultado esperado (aserciones)
- **And/But**: Continúa el paso anterior

---

## Ejemplo Completo: Control de Temperatura

### 1. Historia de Usuario

```
Como usuario del termostato
Quiero que el sistema controle automáticamente la temperatura
Para mantener el ambiente confortable
```

### 2. Feature File

```gherkin
# features/control_temperatura.feature

Feature: Control Automático de Temperatura
  Como usuario del termostato
  Quiero que el sistema controle automáticamente la temperatura
  Para mantener el ambiente confortable

  Background:
    Given un sistema de termostato inicializado
    And un ambiente con temperatura inicial

  Scenario: Encender climatizador cuando hace frío
    Given la temperatura ambiente es 18°C
    And la temperatura deseada es 22°C
    And el climatizador está apagado
    When el sistema verifica la temperatura
    Then el climatizador debe encenderse
    And el modo debe ser "calentando"

  Scenario: Mantener temperatura alcanzada
    Given la temperatura ambiente es 22°C
    And la temperatura deseada es 22°C
    And el climatizador está encendido
    When el sistema verifica la temperatura
    Then el climatizador debe apagarse

  Scenario: Cambiar de modo calefacción a refrigeración
    Given la temperatura ambiente es 26°C
    And la temperatura deseada es 22°C
    And el climatizador está en modo "calentando"
    When el sistema actualiza el modo
    Then el climatizador debe cambiar a modo "enfriando"
```

### 3. Implementación de Steps

```python
# features/steps/temperatura_steps.py

from behave import given, when, then, step
from entidades.ambiente import Ambiente
from entidades.climatizador import Climatizador
from gestores_entidades.gestor_climatizador import GestorClimatizador

@given('un sistema de termostato inicializado')
def step_sistema_inicializado(context):
    context.ambiente = Ambiente()
    context.climatizador = Climatizador()
    context.gestor = GestorClimatizador(context.ambiente, context.climatizador)

@given('un ambiente con temperatura inicial')
def step_ambiente_inicial(context):
    # Configuración inicial del ambiente
    context.ambiente.actualizar_temperatura(20.0)

@given('la temperatura ambiente es {temp}°C')
def step_temperatura_ambiente(context, temp):
    context.ambiente.actualizar_temperatura(float(temp))

@given('la temperatura deseada es {temp}°C')
def step_temperatura_deseada(context, temp):
    context.ambiente.establecer_temperatura_deseada(float(temp))

@given('el climatizador está {estado}')
def step_climatizador_estado(context, estado):
    if estado == "apagado":
        context.climatizador.apagar()
    elif estado == "encendido":
        context.climatizador.encender()

@when('el sistema verifica la temperatura')
def step_verificar_temperatura(context):
    context.gestor.controlar_temperatura()

@then('el climatizador debe encenderse')
def step_climatizador_encendido(context):
    assert context.climatizador.esta_encendido(), \
        "El climatizador debería estar encendido"

@then('el modo debe ser "{modo}"')
def step_verificar_modo(context, modo):
    modo_actual = context.climatizador.obtener_modo()
    assert modo_actual == modo, \
        f"Esperaba modo {modo}, pero está en {modo_actual}"

@then('el climatizador debe apagarse')
def step_climatizador_apagado(context):
    assert not context.climatizador.esta_encendido(), \
        "El climatizador debería estar apagado"
```

---

## Uso del Pipeline

### Validar Todas las Historias

```bash
python validar_historia.py
```

### Validar Historia Específica

```bash
python validar_historia.py control_temperatura
```

### Validar Historia del Branch Actual

```bash
# Estando en branch: feature/control-temperatura
python validar_historia.py --branch
```

### Ver Resumen del Proyecto

```bash
python validar_historia.py --resumen
```

### Listar Features Disponibles

```bash
python validar_historia.py --listar
```

---

## Convención de Branches

Para que funcione `--branch`, usa esta convención:

```
feature/nombre-historia  →  features/nombre_historia.feature
historia/gestion-bateria →  features/gestion_bateria.feature
us/control-temp          →  features/control_temp.feature
```

El script convierte automáticamente:
- Guiones (`-`) → Guiones bajos (`_`)
- Extrae el nombre después del `/`

---

## Ejemplo de Salida

### Ejecución Exitosa

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🎯 PIPELINE DE VALIDACIÓN (BDD)                         ║
║              Historias de Usuario                                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

======================================================================
🔍 Verificando Estructura BDD
======================================================================

✅ Estructura BDD correcta
   • 3 archivo(s) .feature encontrado(s)
   • Directorio steps/ presente

📋 Features Disponibles:

   1. control_temperatura
      Control Automático de Temperatura

   2. gestion_bateria
      Gestión de Batería del Sistema

   3. seleccion_modo
      Selección de Modo de Operación

======================================================================
🧪 Ejecutando Tests de Aceptación BDD
======================================================================

Feature: Control Automático de Temperatura

  Scenario: Encender climatizador cuando hace frío
    Given un sistema de termostato inicializado ... passed
    And un ambiente con temperatura inicial ... passed
    Given la temperatura ambiente es 18°C ... passed
    And la temperatura deseada es 22°C ... passed
    And el climatizador está apagado ... passed
    When el sistema verifica la temperatura ... passed
    Then el climatizador debe encenderse ... passed
    And el modo debe ser "calentando" ... passed

  Scenario: Mantener temperatura alcanzada
    Given un sistema de termostato inicializado ... passed
    ...

3 features passed, 0 failed, 0 skipped
12 scenarios passed, 0 failed, 0 skipped
48 steps passed, 0 failed, 0 skipped

======================================================================
📋 RESULTADO DE VALIDACIÓN
======================================================================

✅ VALIDACIÓN EXITOSA
   Todos los escenarios pasaron
   La historia de usuario está implementada correctamente

⏱️  Duración: 2.34s
```

### Ejecución con Fallos

```
Feature: Control Automático de Temperatura

  Scenario: Encender climatizador cuando hace frío
    Given un sistema de termostato inicializado ... passed
    ...
    Then el climatizador debe encenderse ... failed

Assertion Failed: El climatizador debería estar encendido
  Expected: encendido
  Got: apagado

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 1 failed, 0 skipped
15 steps passed, 1 failed, 0 skipped

======================================================================
📋 RESULTADO DE VALIDACIÓN
======================================================================

❌ VALIDACIÓN FALLÓ
   Algunos escenarios no pasaron
   La implementación NO cumple con los requisitos

⏱️  Duración: 1.87s
```

---

## Workflow Completo: De Historia a Código

### 1. Crear Branch para Historia

```bash
git checkout -b feature/control-temperatura
```

### 2. Escribir Feature (Criterios de Aceptación)

```bash
# Crear features/control_temperatura.feature
```

```gherkin
Feature: Control Automático de Temperatura
  ...

  Scenario: Encender cuando hace frío
    Given temperatura ambiente 18°C
    When se verifica
    Then debe encender en modo calentando
```

### 3. Ejecutar Validación (Fallará - TDD)

```bash
python validar_historia.py control_temperatura
```

❌ Falla porque los steps no existen

### 4. Implementar Steps

```bash
# Crear features/steps/temperatura_steps.py
```

```python
from behave import given, when, then

@given('temperatura ambiente {temp}°C')
def step_impl(context, temp):
    context.temp = float(temp)
    # TODO: Implementar

@when('se verifica')
def step_impl(context):
    # TODO: Implementar
    pass

@then('debe encender en modo calentando')
def step_impl(context):
    # TODO: Implementar
    assert False, "Not implemented yet"
```

### 5. Ejecutar de Nuevo

```bash
python validar_historia.py control_temperatura
```

❌ Falla en aserciones

### 6. Implementar Código Real

```python
# En entidades/climatizador.py, gestores, etc.
# Implementar la lógica de negocio
```

### 7. Completar Steps

```python
@given('temperatura ambiente {temp}°C')
def step_impl(context, temp):
    context.ambiente = Ambiente()
    context.ambiente.temperatura = float(temp)

@when('se verifica')
def step_impl(context):
    context.gestor = GestorClimatizador(context.ambiente)
    context.gestor.controlar()

@then('debe encender en modo calentando')
def step_impl(context):
    assert context.ambiente.climatizador.estado == "calentando"
```

### 8. Validar Historia

```bash
python validar_historia.py --branch
```

✅ Todos los scenarios pasan

### 9. Validar Calidad Técnica

```bash
python verificar_calidad.py
```

✅ Tests unitarios y métricas OK

### 10. Commit y PR

```bash
git add .
git commit -m "feat: implementar control automático de temperatura"
git push origin feature/control-temperatura
# Crear Pull Request
```

---

## Combinando Ambos Pipelines

### En Desarrollo

```bash
# Ciclo corto durante desarrollo
while [ coding ]; do
    python verificar_calidad.py --rapido  # Verificación técnica rápida
done
```

### Al Completar Historia

```bash
# 1. Verificación técnica completa
python verificar_calidad.py
# ✅ Calidad técnica OK

# 2. Validación de requisitos
python validar_historia.py --branch
# ✅ Requisitos funcionales cumplidos

# 3. Commit
git commit -m "feat: historia completada"
```

### En Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Verificación Técnica..."
python verificar_calidad.py || exit 1

echo "🎯 Validación de Historia..."
python validar_historia.py --branch || exit 1

echo "✅ Todo listo para commit"
```

---

## Ventajas del Approach BDD

### 1. **Comunicación**
- Product Owner escribe criterios en lenguaje natural
- Desarrolladores implementan exactamente lo que se necesita
- Tests son documentación viva

### 2. **Detección Temprana**
- Escribes scenarios ANTES de implementar
- Sabes exactamente qué construir
- Evitas malentendidos

### 3. **Validación Automática**
- Un comando valida toda la historia
- No hay interpretaciones: o pasa o no pasa
- Regression testing automático

### 4. **Trazabilidad**
```
Historia → Feature → Scenarios → Steps → Código
```
Todo está conectado y validado

---

## Tips y Best Practices

### 1. Un Feature = Una Historia de Usuario

```
✅ BIEN:
features/control_temperatura.feature  → Historia completa

❌ MAL:
features/tests.feature  → Demasiado genérico
```

### 2. Scenarios Independientes

Cada scenario debe poder ejecutarse solo:

```gherkin
✅ BIEN:
Scenario: Test A
  Given setup específico para A
  ...

Scenario: Test B
  Given setup específico para B
  ...

❌ MAL:
Scenario: Test A
  Given setup
  ...

Scenario: Test B (depende de A)
  When continúo desde A
  ...
```

### 3. Background para Setup Común

```gherkin
Background:
  Given un sistema inicializado
  And un ambiente de prueba

Scenario: Test 1
  Given condición específica 1
  ...

Scenario: Test 2
  Given condición específica 2
  ...
```

### 4. Steps Reutilizables

```python
# ✅ BIEN: Step reutilizable
@given('la temperatura es {temp}°C')
def step_impl(context, temp):
    context.temperatura = float(temp)

# ❌ MAL: Step demasiado específico
@given('la temperatura es exactamente 22 grados celsius')
def step_impl(context):
    context.temperatura = 22.0
```

### 5. Tags para Organización

```gherkin
@critico @smoke
Scenario: Funcionalidad crítica
  ...

@lento
Scenario: Test que tarda mucho
  ...

@skip @wip
Scenario: Trabajo en progreso
  ...
```

Ejecutar:
```bash
behave --tags=critico        # Solo críticos
behave --tags=~lento         # Excluir lentos
behave --tags=smoke          # Solo smoke tests
```

---

## Troubleshooting

### behave no encuentra los steps

**Problema**: `Undefined steps`

**Solución**:
```bash
# Verificar estructura
features/
├── mi_feature.feature
└── steps/
    ├── __init__.py          ← Debe existir
    └── mi_steps.py
```

### Steps no coinciden

**Problema**: `No matching step definition`

**Solución**: El texto debe coincidir EXACTAMENTE

```gherkin
# Feature
Given la temperatura es 22°C

# Step (debe coincidir)
@given('la temperatura es {temp}°C')  # ✅
@given('temperatura es {temp}°C')     # ❌ Falta "la"
```

### Imports fallan en steps

**Solución**: Agregar path del proyecto

```python
# features/steps/mi_steps.py
import sys
from pathlib import Path

# Agregar raíz del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Ahora puedes importar
from entidades.bateria import Bateria
```

---

## Recursos

### Documentación
- [Behave Docs](https://behave.readthedocs.io/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
- [BDD by Example](https://cucumber.io/docs/bdd/)

### Ejemplos
- `features/ejemplo.feature` (generado automáticamente)
- `features/steps/ejemplo_steps.py`

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Feature** | Una historia de usuario completa |
| **Scenario** | Un caso de prueba específico |
| **Given** | Establece contexto (precondiciones) |
| **When** | Ejecuta acción |
| **Then** | Verifica resultado |
| **Steps** | Implementación en Python de Given/When/Then |
| **Pipeline** | Ejecuta todos los scenarios automáticamente |

**Regla de Oro**:
```
Si todos los scenarios pasan → Historia COMPLETADA ✅
Si algún scenario falla → Sigue trabajando ⚠️
```
