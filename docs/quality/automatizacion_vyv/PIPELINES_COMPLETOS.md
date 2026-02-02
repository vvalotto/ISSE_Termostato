# Guía Completa: Dos Pipelines de Calidad

## Visión General

Tu proyecto ahora tiene **DOS pipelines complementarios**:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  📋 Historia de Usuario                                 │
│      "Como usuario quiero..."                           │
│                                                         │
└────────────┬────────────────────────────────────────────┘
             │
             ↓
      ┌──────────────┐
      │  1. Feature  │  ← Escribe criterios BDD
      │     (BDD)    │
      └──────┬───────┘
             │
             ↓
      ┌──────────────┐
      │ 2. Implementa│  ← Escribe código
      │    Código    │
      └──────┬───────┘
             │
             ├─────────────────────┬──────────────────────┐
             ↓                     ↓                      ↓
   ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐
   │  VERIFICACIÓN   │   │   VALIDACIÓN    │   │   INTEGRACIÓN    │
   │   (Técnica)     │   │  (Funcional)    │   │    CONTINUA      │
   │                 │   │                 │   │                  │
   │ • Tests         │   │ • Scenarios BDD │   │ • Pull Request   │
   │ • Cobertura     │   │ • Criterios     │   │ • Code Review    │
   │ • Métricas      │   │ • Aceptación    │   │ • Merge          │
   │ • Arquitectura  │   │                 │   │                  │
   └─────────────────┘   └─────────────────┘   └──────────────────┘
```

---

## Los Dos Pipelines

### 🔧 Pipeline de VERIFICACIÓN (Calidad Técnica)

**Archivo**: `verificar_calidad.py`

**Pregunta**: "¿Está bien construido?"

**Verifica**:
- ✅ Tests unitarios pasan
- ✅ Cobertura de código > 70%
- ✅ Código sigue estándares (PEP8)
- ✅ Complejidad < umbrales
- ✅ Métricas de diseño OK

**Cuándo usar**:
- Durante el desarrollo (ciclo corto)
- Antes de cada commit
- En pre-commit hook

**Comando**:
```bash
python verificar_calidad.py         # Verificación completa
python verificar_calidad.py --rapido # Solo tests + estilo
```

---

### 🎯 Pipeline de VALIDACIÓN (Requisitos Funcionales)

**Archivo**: `validar_historia.py`

**Pregunta**: "¿Hace lo que debe hacer?"

**Valida**:
- ✅ Cumple criterios de aceptación
- ✅ Todos los scenarios BDD pasan
- ✅ Comportamiento esperado funciona
- ✅ Historia de usuario completa

**Cuándo usar**:
- Al completar una historia
- Antes de PR/merge
- Para demo/aceptación

**Comando**:
```bash
python validar_historia.py           # Validar todas las features
python validar_historia.py --branch  # Validar historia del branch
```

---

## Comparación Lado a Lado

| Aspecto | 🔧 Verificación | 🎯 Validación |
|---------|----------------|---------------|
| **Enfoque** | Código y diseño | Comportamiento y requisitos |
| **Tests** | Unitarios, integración | Aceptación (BDD) |
| **Lenguaje** | Python (pytest) | Gherkin (behave) |
| **Escritos por** | Desarrolladores | PO + Desarrolladores |
| **Frecuencia** | Muchas veces/día | 1 vez por historia |
| **Duración** | Rápido (5-15s) | Moderado (15-60s) |
| **Fallo** | Código con problemas | Requisito no cumplido |
| **Éxito** | Código técnicamente correcto | Feature funcionalmente completa |

---

## Workflow Completo

### Inicio de Historia

```bash
# 1. Crear branch
git checkout -b feature/control-temperatura

# 2. Escribir feature con criterios de aceptación
# features/control_temperatura.feature
```

```gherkin
Feature: Control Automático de Temperatura
  Como usuario del termostato
  Quiero control automático
  Para mantener confort

  Scenario: Encender cuando hace frío
    Given temperatura ambiente 18°C
    And temperatura deseada 22°C
    When verifico estado
    Then climatizador debe estar "calentando"
```

### Durante Desarrollo

```bash
# 3. Ciclo de desarrollo (repetir)
while [ coding ]; do
    # Escribir código
    vim entidades/climatizador.py

    # Verificar calidad técnica (RÁPIDO)
    python verificar_calidad.py --rapido

    # Si falla, corregir
done
```

### Al Completar Funcionalidad

```bash
# 4. Verificación técnica completa
python verificar_calidad.py
# ✅ Asegurar que el código es de calidad

# 5. Validación funcional
python validar_historia.py --branch
# ✅ Asegurar que cumple requisitos
```

### Antes de Commit

```bash
# 6. Doble check
python verificar_calidad.py && python validar_historia.py --branch
# ✅ Ambos deben pasar

# 7. Commit
git add .
git commit -m "feat: control automático de temperatura"
```

### Pull Request

```bash
# 8. Push
git push origin feature/control-temperatura

# 9. En el PR, mencionar:
# - ✅ Verificación técnica: PASSED
# - ✅ Validación funcional: PASSED
# - 📄 Feature: features/control_temperatura.feature
```

---

## Automatización con Pre-commit Hook

### Hook Completo

Crear `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║         🚀 VERIFICACIÓN AUTOMÁTICA                   ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# 1. VERIFICACIÓN TÉCNICA
echo "🔧 [1/2] Verificación de Calidad Técnica..."
python verificar_calidad.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ VERIFICACIÓN TÉCNICA FALLÓ"
    echo "   Corrige los problemas de calidad antes de commitear"
    exit 1
fi

# 2. VALIDACIÓN FUNCIONAL (solo si hay feature para el branch)
echo ""
echo "🎯 [2/2] Validación de Historia de Usuario..."
python validar_historia.py --branch

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  VALIDACIÓN FUNCIONAL FALLÓ"
    echo "   La historia de usuario no está completa"
    echo ""
    read -p "   ¿Continuar de todas formas? (y/N): " respuesta

    if [ "$respuesta" != "y" ] && [ "$respuesta" != "Y" ]; then
        exit 1
    fi
fi

echo ""
echo "✅ TODAS LAS VERIFICACIONES PASARON"
echo "   Procediendo con commit..."
echo ""
```

Hacer ejecutable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Configuración por Entorno

### Desarrollo Local (Rápido)

```bash
# Solo verificaciones rápidas
alias vc='python verificar_calidad.py --rapido'

# Usar durante desarrollo
vc  # Ejecutar cada pocos minutos
```

### Antes de Commit (Completo)

```bash
# Verificación completa
alias commit-seguro='python verificar_calidad.py && python validar_historia.py --branch && git commit'

# Usar en lugar de git commit
commit-seguro -m "mensaje"
```

### CI/CD (Pipeline completo)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  verificacion:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Instalar dependencias
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8 radon behave

      - name: Verificación Técnica
        run: python verificar_calidad.py

      - name: Validación Funcional
        run: python validar_historia.py

  metricas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Generar Reportes de Métricas
        run: |
          python docs/calcular_metricas_herencia.py
          python docs/calcular_metricas_dsm.py
          python docs/calcular_metricas_clean_architecture.py

      - name: Publicar Reportes
        uses: actions/upload-artifact@v2
        with:
          name: metricas
          path: docs/reporte_*.md
```

---

## Casos de Uso

### Caso 1: Nueva Feature

```bash
# Fase 1: Definir (Product Owner + Dev)
git checkout -b feature/nueva-feature
vim features/nueva_feature.feature  # Escribir criterios BDD

# Fase 2: Desarrollar
# Implementar código con verificaciones continuas
python verificar_calidad.py --rapido  # Cada pocos minutos

# Fase 3: Completar
python verificar_calidad.py           # Verificación completa
python validar_historia.py --branch   # Validación funcional

# Fase 4: Commit y PR
git commit -m "feat: nueva feature"
git push
```

### Caso 2: Bug Fix

```bash
# Fase 1: Reproducir con test
vim features/bug_fix.feature  # Scenario que reproduce el bug
python validar_historia.py bug_fix  # Debe FALLAR

# Fase 2: Corregir
# Implementar fix

# Fase 3: Verificar
python verificar_calidad.py    # No romper nada más
python validar_historia.py bug_fix  # Ahora debe PASAR

# Fase 4: Commit
git commit -m "fix: corregir bug X"
```

### Caso 3: Refactoring

```bash
# Fase 1: Establecer baseline
python validar_historia.py    # Todos pasan (baseline)
python verificar_calidad.py   # Métricas actuales

# Fase 2: Refactorizar
# Mejorar código manteniendo comportamiento

# Fase 3: Validar
python validar_historia.py    # Debe seguir pasando (regresión)
python verificar_calidad.py   # Métricas deben mejorar

# Fase 4: Commit
git commit -m "refactor: mejorar diseño de X"
```

---

## Definition of Done (DoD)

Una historia NO está terminada hasta que:

### ✅ Checklist Obligatorio

- [ ] Feature escrita con scenarios BDD
- [ ] Código implementado
- [ ] Tests unitarios pasan
- [ ] Cobertura >= 70%
- [ ] **Verificación técnica**: `python verificar_calidad.py` ✅
- [ ] **Validación funcional**: `python validar_historia.py --branch` ✅
- [ ] Métricas dentro de umbrales
- [ ] Code review aprobado
- [ ] Documentación actualizada
- [ ] Merged a main

### 📊 Métricas Mínimas

```python
UMBRALES_MINIMOS = {
    # Verificación
    'tests_pasados': '100%',
    'cobertura': '70%',
    'complejidad_ciclomatica': '≤ 10',
    'indice_mantenibilidad': '≥ 20',

    # Validación
    'scenarios_bdd_pasados': '100%',
    'criterios_aceptacion': '100%',
}
```

---

## Comandos Rápidos

```bash
# Durante desarrollo (rápido, ejecutar frecuentemente)
python verificar_calidad.py --rapido

# Antes de commit (completo)
python verificar_calidad.py && python validar_historia.py --branch

# Ver estado del proyecto
python validar_historia.py --resumen

# Listar historias disponibles
python validar_historia.py --listar

# Validar historia específica
python validar_historia.py nombre_feature

# Solo tests
python verificar_calidad.py --solo-tests
```

---

## Troubleshooting

### "No puedo hacer commit"

```bash
# Verificar qué falla
python verificar_calidad.py        # Ver errores técnicos
python validar_historia.py --branch # Ver escenarios que fallan

# Corregir y reintentar
```

### "Los scenarios BDD no se encuentran"

```bash
# Verificar convención de naming
git branch  # Muestra: feature/control-temperatura
ls features # Debe existir: control_temperatura.feature

# El script convierte automáticamente:
# control-temperatura → control_temperatura
```

### "Quiero saltarme las verificaciones"

```bash
# NO RECOMENDADO, pero si es urgente:
git commit --no-verify -m "WIP: trabajo en progreso"

# PERO: Debes arreglarlo después
```

---

## Métricas de Éxito del Proceso

Tras usar ambos pipelines, deberías ver:

### 📈 Mejoras Esperadas

- **Bugs en producción**: ↓ 50-80%
- **Tiempo de debugging**: ↓ 30-50%
- **Tiempo de review**: ↓ 40% (código ya validado)
- **Confianza en deploys**: ↑ Significativa
- **Comunicación PO-Dev**: ↑ (criterios claros)

### 🎯 Indicadores

```bash
# Al final de cada sprint
echo "Features completadas: $(ls features/*.feature | wc -l)"
echo "Scenarios validados: $(behave --dry-run | grep scenarios)"
echo "Cobertura de tests: $(pytest --cov --cov-report=term | grep TOTAL)"
```

---

## Siguiente Paso

1. **Instala behave**:
   ```bash
   pip install behave
   ```

2. **Ejecuta por primera vez**:
   ```bash
   python validar_historia.py
   ```

3. **Personaliza el ejemplo** generado con tu primera historia real

4. **Integra en tu workflow** desde la próxima feature

---

## Resumen Visual

```
          📋 HISTORIA DE USUARIO
                    ↓
        ┌───────────────────────┐
        │  Escribir Feature     │
        │  (Criterios BDD)      │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │  Implementar Código   │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │  🔧 VERIFICACIÓN      │ ← Calidad técnica
        │  verificar_calidad.py │
        └───────────┬───────────┘
                    ↓
              ¿Pasa?
             /      \
           NO        SÍ
            ↓         ↓
      Refactor   ┌───────────────────────┐
                 │  🎯 VALIDACIÓN        │ ← Requisitos
                 │  validar_historia.py  │
                 └───────────┬───────────┘
                             ↓
                       ¿Pasa?
                      /      \
                    NO        SÍ
                     ↓         ↓
               Implementar   ✅ DONE
                 faltante      ↓
                              COMMIT
```

---

**¿Listo para empezar?** 🚀

Ejecuta:
```bash
python validar_historia.py
```

Y sigue el flujo para tu primera historia de usuario con BDD.
