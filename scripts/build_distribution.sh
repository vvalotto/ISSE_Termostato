#!/bin/bash
# Script para construir paquete distribuible de termostato-core
# Uso: ./scripts/build_distribution.sh

set -e  # Salir si hay errores

echo "======================================"
echo "  CONSTRUCCIÓN DE PAQUETE TERMOSTATO"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${YELLOW}[1/6]${NC} Limpiando builds anteriores..."
rm -rf build/ dist/ *.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Limpieza completada"
echo ""

echo -e "${YELLOW}[2/6]${NC} Verificando estructura del proyecto..."
REQUIRED_DIRS="entidades servicios_dominio gestores_entidades servicios_aplicacion agentes_sensores agentes_actuadores configurador registrador"
for dir in $REQUIRED_DIRS; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}✗${NC} Error: Directorio $dir no encontrado"
        exit 1
    fi
done
echo -e "${GREEN}✓${NC} Todos los directorios requeridos existen"
echo ""

echo -e "${YELLOW}[3/6]${NC} Verificando ejecutar.py..."
if [ ! -f "ejecutar.py" ]; then
    echo -e "${RED}✗${NC} Error: ejecutar.py no encontrado"
    exit 1
fi
echo -e "${GREEN}✓${NC} Punto de entrada verificado"
echo ""

echo -e "${YELLOW}[4/6]${NC} Construyendo wheel..."
python3 setup.py bdist_wheel

if [ ! -d "dist" ] || [ -z "$(ls -A dist/*.whl 2>/dev/null)" ]; then
    echo -e "${RED}✗${NC} Error: No se generó el archivo wheel"
    exit 1
fi
echo -e "${GREEN}✓${NC} Wheel construido exitosamente"
echo ""

echo -e "${YELLOW}[5/6]${NC} Construyendo source distribution..."
python3 setup.py sdist
echo -e "${GREEN}✓${NC} Source distribution creado"
echo ""

echo -e "${YELLOW}[6/6]${NC} Generando checksums..."
cd dist
sha256sum * > checksums.txt 2>/dev/null || shasum -a 256 * > checksums.txt
cd ..
echo -e "${GREEN}✓${NC} Checksums generados"
echo ""

echo "======================================"
echo -e "${GREEN}  CONSTRUCCIÓN COMPLETADA${NC}"
echo "======================================"
echo ""
echo "Archivos generados en dist/:"
ls -lh dist/
echo ""
echo "Para instalar en Raspberry Pi:"
echo "  scp dist/termostato_core-*.whl pi@<IP>:/home/pi/"
echo "  ssh pi@<IP>"
echo "  pip3 install termostato_core-*.whl"
echo ""
