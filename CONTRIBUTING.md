# Guía de Contribución - ISSE_Termostato

Gracias por tu interés en contribuir al proyecto ISSE_Termostato! Esta guía te ayudará a comenzar.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Ejecución de Tests](#ejecución-de-tests)
- [Construcción del Proyecto](#construcción-del-proyecto)

## 🤝 Código de Conducta

Este proyecto es educativo y busca demostrar buenas prácticas de arquitectura de software. Se espera:

- Respeto y profesionalismo en las interacciones
- Enfoque en soluciones técnicas basadas en principios SOLID
- Retroalimentación constructiva en code reviews
- Compromiso con la calidad y mantenibilidad del código

## 🚀 Cómo Contribuir

### Tipos de Contribuciones

**Bienvenidas:**
- 🐛 Corrección de bugs
- 📝 Mejoras en documentación
- ✨ Nuevas features (previa discusión en Issues)
- 🧪 Mejoras en tests y cobertura
- ♻️ Refactorización que mejore calidad

**Requieren discusión previa:**
- Cambios arquitectónicos significativos
- Nuevas dependencias externas
- Modificación de principios de diseño establecidos

## 🛠️ Configuración del Entorno

### Requisitos

- Python 3.5+ (para compatibilidad con Raspberry Pi)
- Git
- Conocimiento de Clean Architecture y principios SOLID

### Setup Inicial

```bash
# 1. Fork del repositorio
# (Usa el botón Fork en GitHub)

# 2. Clonar tu fork
git clone https://github.com/TU_USUARIO/ISSE_Termostato.git
cd ISSE_Termostato

# 3. Agregar upstream
git remote add upstream https://github.com/vvalotto/ISSE_Termostato.git

# 4. Crear entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 5. Instalar dependencias de desarrollo
pip install -e ".[dev]"
```

### Instalación desde Código Fuente

```bash
# Instalar el proyecto en modo desarrollo
pip install -e .

# O usando setup.py
python setup.py develop
```

## 📐 Estándares de Código

### Compatibilidad Python 3.5

**IMPORTANTE:** El código debe ser compatible con Python 3.5 para Raspberry Pi OS Lite.

❌ **NO usar:**
```python
# F-strings (Python 3.6+)
mensaje = f"Temperatura: {temp}°C"

# Type hints avanzados (Python 3.6+)
def foo(x: List[str]) -> Dict[str, int]:
```

✅ **SÍ usar:**
```python
# .format() para strings
mensaje = "Temperatura: {}°C".format(temp)

# Type hints básicos o comentarios
def foo(x, y):
    """
    Args:
        x: Lista de strings
        y: Diccionario
    """
```

### Convenciones de Nomenclatura

```python
# Variables y funciones: snake_case
temperatura_actual = 25.0
def leer_temperatura():
    pass

# Clases: PascalCase
class GestorAmbiente:
    pass

# Constantes: UPPER_SNAKE_CASE
DELTA_TEMP = 2.0
```

### Docstrings

Todos los módulos, clases y funciones públicas deben tener docstrings en español:

```python
def comparar_temperatura(actual, deseada):
    """
    Compara temperatura actual con deseada aplicando histeresis.

    Args:
        actual (float): Temperatura actual en grados Celsius.
        deseada (float): Temperatura deseada en grados Celsius.

    Returns:
        str: "alta", "baja" o "normal"
    """
    pass
```

### Arquitectura en Capas

**Respetar la regla de dependencias:** Solo apuntan hacia el centro.

```
Frameworks → Adapters → Use Cases → Entities
```

- **Entities:** NO pueden importar nada de capas externas
- **Use Cases:** Solo pueden importar de Entities
- **Adapters:** Pueden importar de Use Cases y Entities
- **Frameworks:** Pueden importar de cualquier capa

### Linting

El proyecto usa `pylint` con configuración personalizada:

```bash
# Verificar un archivo
pylint archivo.py

# Verificar todo el proyecto
pylint entidades/ servicios_dominio/ gestores_entidades/
```

## 🔄 Proceso de Pull Request

### 1. Crear Branch

Usa nombres descriptivos siguiendo el patrón:

```bash
# Features
git checkout -b feature/descripcion-corta

# Bug fixes
git checkout -b fix/descripcion-del-bug

# Documentación
git checkout -b docs/que-se-documenta

# Refactorización
git checkout -b refactor/que-se-refactoriza
```

### 2. Hacer Commits

Usa **Conventional Commits**:

```bash
# Formato
tipo(scope): descripción corta

# Tipos válidos:
# - feat: Nueva funcionalidad
# - fix: Corrección de bug
# - refactor: Refactorización sin cambio funcional
# - docs: Solo cambios en documentación
# - test: Agregar o modificar tests
# - chore: Tareas de mantenimiento

# Ejemplos
git commit -m "feat(visualizador): Agregar visualizador WebSocket"
git commit -m "fix(climatizador): Corregir transición de estados"
git commit -m "docs(readme): Actualizar instrucciones de instalación"
git commit -m "refactor(gestor): Aplicar principio SRP en GestorAmbiente"
```

### 3. Mantener Actualizado

```bash
# Antes de abrir PR, sincronizar con upstream
git fetch upstream
git rebase upstream/main
```

### 4. Abrir Pull Request

**Checklist antes de abrir PR:**

- [ ] Los tests pasan: `pytest Test/ -v`
- [ ] El código sigue los estándares de estilo
- [ ] Se agregaron tests para código nuevo
- [ ] La documentación está actualizada
- [ ] Los commits siguen Conventional Commits
- [ ] El código es compatible con Python 3.5

**Template de PR:**

```markdown
## Descripción
[Descripción clara de los cambios]

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva feature
- [ ] Refactorización
- [ ] Documentación

## ¿Cómo se probó?
[Describe cómo probaste los cambios]

## Checklist
- [ ] Tests agregados/actualizados
- [ ] Documentación actualizada
- [ ] Compatible con Python 3.5
- [ ] Sigue principios SOLID
- [ ] Respeta Clean Architecture
```

## 🧪 Ejecución de Tests

### Tests Unitarios

```bash
# Todos los tests unitarios
pytest Test/unit/ -v

# Un módulo específico
pytest Test/unit/entidades/ -v

# Un test específico
pytest Test/unit/entidades/test_ambiente.py::TestAmbiente::test_constructor -v
```

### Tests de Integración

```bash
# Todos los tests de integración
pytest Test/integration/ -v
```

### Cobertura

```bash
# Ejecutar con reporte de cobertura
pytest Test/ --cov=. --cov-report=html

# Ver reporte en navegador
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Meta de cobertura:** Mantener >80%

## 🏗️ Construcción del Proyecto

### Generar Distribución

```bash
# Generar wheel para distribución
python setup.py bdist_wheel

# O usando build moderno
pip install build
python -m build
```

Los archivos generados estarán en `dist/`:
- `termostato_core-1.0.0-py3-none-any.whl`
- `termostato_core-1.0.0.tar.gz`

### Instalación en Raspberry Pi

```bash
# En Raspberry Pi (desde archivo wheel)
pip3 install termostato_core-1.0.0-py3-none-any.whl

# Ejecutar
termostato
```

## 📚 Recursos Adicionales

### Arquitectura y Patrones

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Principios SOLID](https://en.wikipedia.org/wiki/SOLID)
- [Patrones GRASP](https://en.wikipedia.org/wiki/GRASP_(object-oriented_design))

### Documentación del Proyecto

- `CLAUDE.md` - Guía específica para trabajar con Claude Code
- `README.md` - Documentación completa del proyecto
- `DEPLOYMENT.md` - Guía de despliegue
- `docs/quality/` - Análisis de calidad y métricas

## ❓ Preguntas Frecuentes

### ¿Por qué Python 3.5?

Para garantizar compatibilidad con Raspberry Pi OS Lite, que incluye Python 3.5 por defecto.

### ¿Por qué tantas interfaces abstractas?

Implementamos **Dependency Inversion Principle** (DIP) de SOLID. Las interfaces permiten intercambiar implementaciones sin modificar las capas superiores.

### ¿Puedo agregar una nueva dependencia?

Solo si es absolutamente necesaria y compatible con Python 3.5. Preferimos mantener dependencias mínimas.

### ¿Cómo propongo cambios arquitectónicos?

Abre un Issue para discutir antes de implementar. Los cambios arquitectónicos requieren consenso.

## 📞 Contacto

- **Issues:** [GitHub Issues](https://github.com/vvalotto/ISSE_Termostato/issues)
- **Autor:** Victor Valotto [@vvalotto](https://github.com/vvalotto)

---

**Gracias por contribuir a ISSE_Termostato! 🎉**
