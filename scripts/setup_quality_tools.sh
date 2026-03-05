#!/bin/bash
# =============================================================================
# setup_quality_tools.sh
# Instala software_limpio en un virtualenv separado (Python 3.11+)
# Los agentes de calidad requieren Python >= 3.11 y NO deben mezclarse
# con el entorno de runtime del proyecto (Python 3.5+)
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
QUALITY_VENV="$PROJECT_DIR/.venv-quality"

echo "==> Instalando herramientas de calidad en $QUALITY_VENV"

# Verificar Python 3.11+
PYTHON=$(which python3.11 2>/dev/null || which python3.12 2>/dev/null || which python3.13 2>/dev/null)
if [ -z "$PYTHON" ]; then
  echo "ERROR: Se requiere Python 3.11 o superior."
  echo "Instalar con: brew install python@3.11"
  exit 1
fi

echo "  Usando: $($PYTHON --version)"

# Crear virtualenv de calidad
if [ ! -d "$QUALITY_VENV" ]; then
  "$PYTHON" -m venv "$QUALITY_VENV"
  echo "  Virtualenv creado en .venv-quality/"
fi

# Instalar software_limpio
"$QUALITY_VENV/bin/pip" install --quiet --upgrade pip
"$QUALITY_VENV/bin/pip" install --quiet \
  "git+https://github.com/vvalotto/software_limpio.git@v0.3.0"

# Instalar pre-commit (para el hook de codeguard)
"$QUALITY_VENV/bin/pip" install --quiet pre-commit

echo ""
echo "✅ Instalación completada."
echo ""
echo "Comandos disponibles:"
echo "  .venv-quality/bin/codeguard       -- Análisis pre-commit (< 5s)"
echo "  .venv-quality/bin/designreviewer  -- Revisión de diseño (2-5 min)"
echo "  .venv-quality/bin/architectanalyst -- Análisis arquitectónico (10-30 min)"
echo ""
echo "Para activar pre-commit hooks:"
echo "  source .venv-quality/bin/activate"
echo "  pre-commit install"
