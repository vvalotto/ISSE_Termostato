#!/bin/bash
# Script para desplegar termostato en Raspberry Pi de forma remota
# Uso: ./scripts/deploy_to_rpi.sh <IP_RASPBERRY>
# Ejemplo: ./scripts/deploy_to_rpi.sh 192.168.0.14

set -e

if [ -z "$1" ]; then
    echo "Error: Debe proporcionar la IP de la Raspberry Pi"
    echo "Uso: $0 <IP_RASPBERRY>"
    echo "Ejemplo: $0 192.168.0.14"
    exit 1
fi

RPI_IP="$1"
RPI_USER="pi"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "======================================"
echo "  DESPLIEGUE A RASPBERRY PI"
echo "  IP: $RPI_IP"
echo "======================================"
echo ""

# Verificar conexión
echo -e "${YELLOW}[1/6]${NC} Verificando conexión con RPi..."
if ! ssh -o ConnectTimeout=5 "$RPI_USER@$RPI_IP" "echo 'Conexión OK'" > /dev/null 2>&1; then
    echo -e "${RED}✗${NC} Error: No se puede conectar a $RPI_IP"
    echo "Verifique que:"
    echo "  1. La Raspberry Pi está encendida y conectada a la red"
    echo "  2. La IP es correcta"
    echo "  3. SSH está habilitado en la Raspberry Pi"
    echo "  4. Tiene permisos de acceso (pruebe: ssh $RPI_USER@$RPI_IP)"
    exit 1
fi
echo -e "${GREEN}✓${NC} Conexión exitosa"
echo ""

# Construir paquete
echo -e "${YELLOW}[2/6]${NC} Construyendo paquete..."
./scripts/build_distribution.sh
echo -e "${GREEN}✓${NC} Paquete construido"
echo ""

# Transferir wheel
echo -e "${YELLOW}[3/6]${NC} Transfiriendo archivos a RPi..."
WHEEL_FILE=$(ls dist/termostato_core-*.whl | head -1)
if [ -z "$WHEEL_FILE" ]; then
    echo -e "${RED}✗${NC} Error: No se encontró archivo wheel"
    exit 1
fi

scp "$WHEEL_FILE" "$RPI_USER@$RPI_IP:/home/$RPI_USER/"
echo -e "${GREEN}✓${NC} Archivo transferido: $(basename $WHEEL_FILE)"
echo ""

# Instalar en RPi
echo -e "${YELLOW}[4/6]${NC} Instalando en Raspberry Pi..."
ssh "$RPI_USER@$RPI_IP" "sudo pip3 install --upgrade /home/$RPI_USER/$(basename $WHEEL_FILE)"
echo -e "${GREEN}✓${NC} Instalación completada"
echo ""

# Transferir configuración
echo -e "${YELLOW}[5/6]${NC} Configurando sistema..."
scp configurador/termostato.json "$RPI_USER@$RPI_IP:/tmp/"
ssh "$RPI_USER@$RPI_IP" "sudo mkdir -p /etc/termostato && sudo mv /tmp/termostato.json /etc/termostato/"
echo -e "${GREEN}✓${NC} Configuración actualizada"
echo ""

# Reiniciar servicio
echo -e "${YELLOW}[6/6]${NC} Reiniciando servicio..."
ssh "$RPI_USER@$RPI_IP" "sudo systemctl daemon-reload && sudo systemctl restart termostato" || true
sleep 2
echo -e "${GREEN}✓${NC} Servicio reiniciado"
echo ""

echo "======================================"
echo -e "${GREEN}  DESPLIEGUE COMPLETADO${NC}"
echo "======================================"
echo ""
echo "Para verificar el estado:"
echo "  ssh $RPI_USER@$RPI_IP 'sudo systemctl status termostato'"
echo ""
echo "Para ver logs en tiempo real:"
echo "  ssh $RPI_USER@$RPI_IP 'sudo journalctl -u termostato -f'"
echo ""
