#!/bin/bash
# Script de instalación para Raspberry Pi
# Debe ejecutarse en la Raspberry Pi con sudo
# Uso: sudo ./install_rpi.sh

set -e

echo "======================================"
echo "  INSTALACIÓN TERMOSTATO EN RPi"
echo "======================================"
echo ""

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Este script debe ejecutarse como root (use sudo)"
    exit 1
fi

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1/10]${NC} Actualizando sistema..."
apt-get update -qq
apt-get upgrade -y -qq
echo -e "${GREEN}✓${NC} Sistema actualizado"
echo ""

echo -e "${YELLOW}[2/10]${NC} Instalando Python 3 y pip..."
apt-get install -y python3 python3-pip python3-dev -qq
echo -e "${GREEN}✓${NC} Python instalado: $(python3 --version)"
echo ""

echo -e "${YELLOW}[3/10]${NC} Creando directorios del sistema..."
mkdir -p /opt/termostato
mkdir -p /etc/termostato
mkdir -p /var/log/termostato
echo -e "${GREEN}✓${NC} Directorios creados"
echo ""

echo -e "${YELLOW}[4/10]${NC} Creando usuario del sistema..."
if ! id -u termostato > /dev/null 2>&1; then
    useradd -r -s /bin/false -d /opt/termostato termostato
    echo -e "${GREEN}✓${NC} Usuario termostato creado"
else
    echo -e "${GREEN}✓${NC} Usuario termostato ya existe"
fi
echo ""

echo -e "${YELLOW}[5/10]${NC} Copiando archivos del proyecto..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Copiar código fuente
cp -r "$SCRIPT_DIR/entidades" /opt/termostato/
cp -r "$SCRIPT_DIR/servicios_dominio" /opt/termostato/
cp -r "$SCRIPT_DIR/gestores_entidades" /opt/termostato/
cp -r "$SCRIPT_DIR/servicios_aplicacion" /opt/termostato/
cp -r "$SCRIPT_DIR/agentes_sensores" /opt/termostato/
cp -r "$SCRIPT_DIR/agentes_actuadores" /opt/termostato/
cp -r "$SCRIPT_DIR/configurador" /opt/termostato/
cp -r "$SCRIPT_DIR/registrador" /opt/termostato/
cp "$SCRIPT_DIR/ejecutar.py" /opt/termostato/

# Copiar configuración
cp "$SCRIPT_DIR/configurador/termostato.json" /etc/termostato/
echo -e "${GREEN}✓${NC} Archivos copiados"
echo ""

echo -e "${YELLOW}[6/10]${NC} Configurando permisos..."
chown -R termostato:termostato /opt/termostato
chown -R termostato:termostato /var/log/termostato
chown -R termostato:termostato /etc/termostato
chmod 755 /opt/termostato/ejecutar.py
echo -e "${GREEN}✓${NC} Permisos configurados"
echo ""

echo -e "${YELLOW}[7/10]${NC} Creando servicio systemd..."
cat > /etc/systemd/system/termostato.service <<EOF
[Unit]
Description=Termostato ISSE - Sistema de Control de Climatización
After=network.target

[Service]
Type=simple
User=termostato
Group=termostato
WorkingDirectory=/opt/termostato
ExecStart=/usr/bin/python3 /opt/termostato/ejecutar.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Límites de recursos
MemoryLimit=100M
CPUQuota=20%

# Seguridad
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
echo -e "${GREEN}✓${NC} Servicio systemd creado"
echo ""

echo -e "${YELLOW}[8/10]${NC} Recargando systemd..."
systemctl daemon-reload
echo -e "${GREEN}✓${NC} Systemd recargado"
echo ""

echo -e "${YELLOW}[9/10]${NC} Habilitando servicio en arranque..."
systemctl enable termostato
echo -e "${GREEN}✓${NC} Servicio habilitado"
echo ""

echo -e "${YELLOW}[10/10]${NC} Iniciando servicio..."
systemctl start termostato
sleep 2
echo -e "${GREEN}✓${NC} Servicio iniciado"
echo ""

echo "======================================"
echo -e "${GREEN}  INSTALACIÓN COMPLETADA${NC}"
echo "======================================"
echo ""
echo "Estado del servicio:"
systemctl status termostato --no-pager
echo ""
echo "Comandos útiles:"
echo "  sudo systemctl status termostato    # Ver estado"
echo "  sudo systemctl restart termostato   # Reiniciar"
echo "  sudo systemctl stop termostato      # Detener"
echo "  sudo journalctl -u termostato -f    # Ver logs en tiempo real"
echo "  sudo nano /etc/termostato/termostato.json  # Editar configuración"
echo ""
