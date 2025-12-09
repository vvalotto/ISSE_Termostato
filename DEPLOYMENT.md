# GUÍA DE DESPLIEGUE - TERMOSTATO RASPBERRY PI

## Inicio Rápido

### Opción 1: Despliegue Automático (Recomendado)

```bash
# En tu MacBook/PC
./scripts/deploy_to_rpi.sh 192.168.0.14
```

### Opción 2: Instalación Manual en RPi

```bash
# 1. Construir paquete en MacBook/PC
./scripts/build_distribution.sh

# 2. Transferir a RPi
scp dist/termostato_core-*.whl pi@192.168.0.14:/home/pi/

# 3. Instalar en RPi
ssh pi@192.168.0.14
pip3 install termostato_core-*.whl

# 4. Configurar
sudo mkdir -p /etc/termostato
sudo nano /etc/termostato/termostato.json
```

---

## Métodos de Instalación Detallados

### Método 1: Despliegue Automatizado

**Prerrequisitos**:
- Raspberry Pi con Raspberry Pi OS instalado
- SSH habilitado en RPi
- Conexión de red entre MacBook y RPi
- Usuario `pi` con permisos sudo

**Pasos**:

```bash
# 1. Dar permisos de ejecución (solo primera vez)
chmod +x scripts/*.sh

# 2. Ejecutar despliegue
./scripts/deploy_to_rpi.sh <IP_RASPBERRY_PI>

# Ejemplo:
./scripts/deploy_to_rpi.sh 192.168.0.14
```

**Lo que hace el script**:
1. ✅ Construye el paquete wheel
2. ✅ Transfiere archivos a RPi
3. ✅ Instala el paquete
4. ✅ Copia configuración
5. ✅ Reinicia el servicio

### Método 2: Instalación desde Wheel

```bash
# En MacBook/PC - Construir paquete
cd /path/to/ISSE_Termostato
./scripts/build_distribution.sh

# Transferir a RPi
scp dist/termostato_core-1.0.0-py3-none-any.whl pi@192.168.0.14:/home/pi/

# En RPi - Instalar
ssh pi@192.168.0.14
pip3 install --upgrade termostato_core-1.0.0-py3-none-any.whl
```

### Método 3: Instalación Manual Completa

```bash
# En RPi
ssh pi@192.168.0.14

# Clonar repositorio
git clone https://github.com/vvalotto/ISSE_Termostato.git
cd ISSE_Termostato

# Ejecutar instalación
chmod +x scripts/install_rpi.sh
sudo ./scripts/install_rpi.sh
```

---

## Configuración

### Archivo de Configuración

Ubicación: `/etc/termostato/termostato.json`

```json
{
  "proxy_bateria": "archivo",
  "proxy_sensor_temperatura": "archivo",
  "climatizador": "climatizador",
  "actuador_climatizador": "general",
  "selector_temperatura": "archivo",
  "seteo_temperatura": "archivo",
  "visualizador_bateria": "consola",
  "visualizador_temperatura": "consola",
  "visualizador_climatizador": "consola",

  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": {
      "bateria": 11000,
      "temperatura": 12000,
      "seteo_temperatura": 13000,
      "selector_temperatura": 14000
    }
  },

  "ambiente": {
    "temperatura_inicial": 22.0,
    "histeresis": 2.0,
    "incremento_ajuste": 1.0
  },

  "bateria": {
    "carga_maxima": 5.0,
    "umbral_carga_baja": 0.8
  }
}
```

Para cambiar entre lecturas locales (archivos) y remotas (sockets):

```bash
# Editar configuración
sudo nano /etc/termostato/termostato.json

# Cambiar:
"proxy_sensor_temperatura": "archivo"  →  "socket"
"proxy_bateria": "archivo"  →  "socket"

# Guardar y reiniciar servicio
sudo systemctl restart termostato
```

---

## Gestión del Servicio

### Comandos Básicos

```bash
# Ver estado
sudo systemctl status termostato

# Iniciar servicio
sudo systemctl start termostato

# Detener servicio
sudo systemctl stop termostato

# Reiniciar servicio
sudo systemctl restart termostato

# Habilitar en arranque
sudo systemctl enable termostato

# Deshabilitar en arranque
sudo systemctl disable termostato
```

### Ver Logs

```bash
# Logs en tiempo real
sudo journalctl -u termostato -f

# Últimas 100 líneas
sudo journalctl -u termostato -n 100

# Logs de auditoría
tail -f /tmp/registro_auditoria

# Logs de errores
tail -f /tmp/registro_errores
```

---

## Verificación Post-Instalación

### Checklist de Verificación

```bash
# 1. Verificar que el servicio está corriendo
sudo systemctl status termostato
# Debe mostrar: Active: active (running)

# 2. Verificar logs
sudo journalctl -u termostato --since "5 minutes ago"

# 3. Verificar archivos de configuración
ls -la /etc/termostato/
cat /etc/termostato/termostato.json

# 4. Verificar directorios
ls -la /opt/termostato/
ls -la /var/log/termostato/

# 5. Verificar procesos
ps aux | grep python

# 6. Verificar puertos (si usa sockets)
sudo netstat -tulpn | grep python
```

### Test de Funcionamiento

```bash
# Conectarse desde MacBook/PC (si usa sockets)
nc -v 192.168.0.14 12000  # Puerto de temperatura

# O usar simuladores
cd actores_externos
python3 simulador_temperatura.py
```

---

## Actualización

### Update Rápido

```bash
# En MacBook/PC
./scripts/deploy_to_rpi.sh 192.168.0.14
```

### Update Manual

```bash
# 1. Construir nueva versión
./scripts/build_distribution.sh

# 2. Transferir
scp dist/termostato_core-*.whl pi@192.168.0.14:/home/pi/

# 3. Actualizar en RPi
ssh pi@192.168.0.14
pip3 install --upgrade termostato_core-*.whl
sudo systemctl restart termostato
```

---

## Troubleshooting

### Problema: Servicio no inicia

```bash
# Ver logs de error
sudo journalctl -u termostato -n 50

# Verificar permisos
sudo chown -R termostato:termostato /opt/termostato
sudo chown -R termostato:termostato /var/log/termostato

# Reiniciar
sudo systemctl restart termostato
```

### Problema: No conecta con simuladores

```bash
# Verificar IP y puertos
sudo netstat -tulpn | grep python

# Verificar firewall (si está habilitado)
sudo ufw status
sudo ufw allow 11000:14002/tcp

# Verificar configuración
cat /etc/termostato/termostato.json
```

### Problema: Consumo alto de recursos

```bash
# Monitorear recursos
top  # Ver uso de CPU/RAM
htop  # Versión mejorada

# Ver uso específico
ps aux | grep termostato

# Reducir frecuencia de polling si es necesario
sudo nano /etc/termostato/termostato.json
# Aumentar intervalos en operador_paralelo
```

---

## Desinstalación

```bash
# Detener y deshabilitar servicio
sudo systemctl stop termostato
sudo systemctl disable termostato

# Eliminar servicio
sudo rm /etc/systemd/system/termostato.service
sudo systemctl daemon-reload

# Desinstalar paquete
pip3 uninstall termostato-core

# Eliminar archivos
sudo rm -rf /opt/termostato
sudo rm -rf /etc/termostato
sudo rm -rf /var/log/termostato

# Eliminar usuario (opcional)
sudo userdel termostato
```

---

## Arquitectura de Despliegue

```
MacBook/PC                     Raspberry Pi
┌──────────────────┐          ┌──────────────────┐
│  Simuladores     │  Socket  │  termostato-core │
│  (desarrollo)    │ ←──────→ │  (producción)    │
│                  │          │                  │
│  - simulador_*   │          │  - entidades/    │
│  - cartel_*      │          │  - servicios_*/  │
│  - Test/         │          │  - gestores_*/   │
│  - docs/         │          │  - agentes_*/    │
└──────────────────┘          │  - configurador/ │
                              │  - registrador/  │
                              └──────────────────┘
                                      ↓
                              ┌──────────────────┐
                              │  Hardware        │
                              │  - Sensores      │
                              │  - Relays        │
                              │  - LEDs          │
                              │  - Botones       │
                              └──────────────────┘
```

---

## Recursos y Soporte

### Documentación Adicional

- [Estrategia de Despliegue Completa](docs/Despliegue/estrategia_despliegue_raspberry_pi.md)
- [Análisis de Calidad de Diseño](docs/Analisis de Calidad de Codigo/analisis_integral_calidad_diseno.md)
- [README Principal](README.md)

### Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Raspberry Pi | Pi Zero W | Pi 3 Model B+ |
| RAM | 512 MB | 1 GB+ |
| Almacenamiento | 8 GB | 16 GB+ |
| Python | 3.7+ | 3.9+ |
| Raspberry Pi OS | Lite | Full Desktop |

### Contacto y Soporte

- Issues: https://github.com/vvalotto/ISSE_Termostato/issues
- Documentación: https://github.com/vvalotto/ISSE_Termostato/docs

---

**Última actualización**: 2025-12-02
**Versión**: 1.0.0
