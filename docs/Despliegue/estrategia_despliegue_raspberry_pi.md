# ESTRATEGIA DE DESPLIEGUE EN RASPBERRY PI
**Proyecto**: ISSE_Termostato
**Fecha**: 2025-12-02
**Objetivo**: Despliegue optimizado del sistema de control de climatización en dispositivos embebidos

---

## ÍNDICE
1. [Análisis de Componentes](#1-análisis-de-componentes)
2. [Arquitectura de Despliegue](#2-arquitectura-de-despliegue)
3. [Paquetes de Distribución](#3-paquetes-de-distribución)
4. [Estrategia de Instalación](#4-estrategia-de-instalación)
5. [Configuración y Optimización](#5-configuración-y-optimización)
6. [Plan de Despliegue](#6-plan-de-despliegue)

---

## 1. ANÁLISIS DE COMPONENTES

### 1.1 Clasificación de Componentes

#### Componentes CORE (Obligatorios en Raspberry Pi)

| Componente | Tamaño | Dependencias | Función | Prioridad |
|------------|--------|--------------|---------|-----------|
| **entidades/** | 76 KB | Ninguna | Lógica de negocio pura | CRÍTICO |
| **servicios_dominio/** | 8 KB | entidades | Algoritmos de control | CRÍTICO |
| **gestores_entidades/** | 28 KB | entidades | Coordinación de casos de uso | CRÍTICO |
| **servicios_aplicacion/** | 68 KB | gestores | Orquestación del sistema | CRÍTICO |
| **agentes_sensores/** | 48 KB | entidades | Lectura de sensores (I2C/GPIO/Socket) | CRÍTICO |
| **agentes_actuadores/** | 40 KB | entidades | Control de actuadores | CRÍTICO |
| **configurador/** | 96 KB | Todas | Inyección de dependencias | CRÍTICO |
| **registrador/** | 8 KB | Ninguna | Auditoría del sistema | CRÍTICO |
| **ejecutar.py** | 1 KB | servicios_aplicacion | Punto de entrada | CRÍTICO |
| **termostato.json** | 2 KB | - | Configuración del sistema | CRÍTICO |

**Total CORE**: ~375 KB (código Python puro)

#### Componentes EXTERNOS (Opcionales - Máquina de Desarrollo)

| Componente | Tamaño | Función | Ubicación |
|------------|--------|---------|-----------|
| **actores_externos/** | 76 KB | Simuladores y displays externos | MacBook/PC |
| **Test/** | ~200 KB | Tests unitarios e integración | MacBook/PC |
| **docs/** | ~500 KB | Documentación | MacBook/PC |

**Total EXTERNOS**: ~776 KB (no necesarios en RPi)

### 1.2 Dependencias del Sistema

#### Python y Librerías

```python
# requirements_rpi.txt (optimizado para Raspberry Pi)
# Ninguna librería externa requerida para CORE
# Solo bibliotecas estándar de Python 3.7+
```

**Ventaja**: El sistema CORE usa **solo bibliotecas estándar de Python** (socket, threading, abc, json, os, time, datetime)

#### Hardware Soportado

| Modelo Raspberry Pi | RAM | CPU | Soporte | Recomendación |
|---------------------|-----|-----|---------|---------------|
| Pi Zero W | 512 MB | 1 GHz | ✅ Sí | Mínimo aceptable |
| Pi 3 Model B | 1 GB | 1.2 GHz | ✅ Sí | Recomendado |
| Pi 4 Model B | 2-8 GB | 1.5 GHz | ✅ Sí | Óptimo |
| Pi 5 | 4-8 GB | 2.4 GHz | ✅ Sí | Futuro |

**Consumo de recursos estimado**:
- RAM: ~50-80 MB (5 threads concurrentes)
- CPU: ~5-10% en operación normal
- Almacenamiento: ~10 MB (código + logs)

---

## 2. ARQUITECTURA DE DESPLIEGUE

### 2.1 Modelo de Despliegue Distribuido

```
┌─────────────────────────────────────────────────────────────┐
│  MÁQUINA DE DESARROLLO (MacBook/PC)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  actores_externos/                                    │  │
│  │  ├── simulador_temperatura.py                         │  │
│  │  ├── simulador_bateria.py                             │  │
│  │  ├── simulador_selector_temperatura.py                │  │
│  │  ├── simulador_seteo_temperatura_deseada.py           │  │
│  │  ├── cartel_temperatura.py                            │  │
│  │  ├── cartel_bateria.py                                │  │
│  │  └── cartel_climatizador.py                           │  │
│  │                                                         │  │
│  │  Test/ (183 tests unitarios e integración)            │  │
│  │  docs/ (Documentación y análisis)                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↕ TCP/IP (Socket)                 │
│                      LAN (192.168.x.x)                       │
└─────────────────────────────────────────────────────────────┘
                             ↕
┌─────────────────────────────────────────────────────────────┐
│  RASPBERRY PI (Sistema Embebido)                            │
│  IP: 192.168.0.14 (ejemplo)                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PAQUETE CORE (~375 KB)                               │  │
│  │  ├── entidades/                                       │  │
│  │  ├── servicios_dominio/                               │  │
│  │  ├── gestores_entidades/                              │  │
│  │  ├── servicios_aplicacion/                            │  │
│  │  ├── agentes_sensores/  ← GPIO/I2C real              │  │
│  │  ├── agentes_actuadores/ ← Relays/PWM real           │  │
│  │  ├── configurador/                                    │  │
│  │  ├── registrador/                                     │  │
│  │  ├── ejecutar.py                                      │  │
│  │  └── termostato.json                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  HARDWARE REAL                                        │  │
│  │  ├── Sensor DHT22/DS18B20 (GPIO 4)                   │  │
│  │  ├── ADC MCP3008 para batería (SPI)                  │  │
│  │  ├── Relays 5V para calefacción/refrigeración        │  │
│  │  ├── LEDs indicadores (GPIO 17, 27, 22)              │  │
│  │  └── Botones físicos (GPIO 23, 24)                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Ventajas de esta Arquitectura

✅ **Separación clara**:
- RPi ejecuta solo el código CORE (~375 KB)
- Simuladores y tests en máquina de desarrollo
- Comunicación transparente vía TCP/IP

✅ **Escalabilidad**:
- Múltiples RPi controlando diferentes zonas
- Centralización de monitoreo en PC

✅ **Mantenibilidad**:
- Desarrollo y debugging en PC potente
- Despliegue de updates sin recompilar

✅ **Recursos optimizados**:
- RAM: Solo ~50-80 MB en RPi
- CPU: <10% de uso en operación normal
- Almacenamiento: Solo 10 MB en SD

---

## 3. PAQUETES DE DISTRIBUCIÓN

### 3.1 Estructura de Paquetes

#### Paquete 1: `termostato-core` (para Raspberry Pi)

```
termostato-core/
├── setup.py                    # Script de instalación
├── requirements.txt            # Vacío (solo stdlib)
├── README.md                   # Instrucciones de instalación
├── termostato/                 # Código fuente
│   ├── __init__.py
│   ├── entidades/
│   ├── servicios_dominio/
│   ├── gestores_entidades/
│   ├── servicios_aplicacion/
│   ├── agentes_sensores/
│   ├── agentes_actuadores/
│   ├── configurador/
│   └── registrador/
├── config/
│   └── termostato.json         # Configuración por defecto
├── bin/
│   ├── termostato              # Ejecutable (wrapper de ejecutar.py)
│   └── termostato-daemon       # Servicio systemd
└── scripts/
    ├── install.sh              # Instalación automática
    ├── post-install.sh         # Configuración post-instalación
    └── uninstall.sh            # Desinstalación
```

#### Paquete 2: `termostato-simulators` (para MacBook/PC)

```
termostato-simulators/
├── setup.py
├── requirements.txt            # Vacío
├── README.md
├── simulators/
│   ├── __init__.py
│   ├── simulador_temperatura.py
│   ├── simulador_bateria.py
│   ├── simulador_selector_temperatura.py
│   ├── simulador_seteo_temperatura_deseada.py
│   ├── cartel_temperatura.py
│   ├── cartel_bateria.py
│   └── cartel_climatizador.py
├── config/
│   └── simuladores_config.json
└── scripts/
    └── lanzar_simuladores.sh
```

#### Paquete 3: `termostato-dev` (para desarrollo)

```
termostato-dev/
├── Test/                       # 183 tests
├── docs/                       # Documentación
├── tools/                      # Herramientas de análisis
│   ├── metricas/
│   └── analisis/
└── requirements-dev.txt        # pytest, radon, pylint, etc.
```

### 3.2 Formato de Distribución

#### Opción A: Wheel Package (Recomendado)

```bash
# Construcción
python setup.py bdist_wheel

# Genera:
dist/termostato_core-1.0.0-py3-none-any.whl  (~400 KB)

# Instalación en RPi
pip install termostato_core-1.0.0-py3-none-any.whl
```

#### Opción B: Tar.gz Comprimido

```bash
# Construcción
python setup.py sdist

# Genera:
dist/termostato-core-1.0.0.tar.gz  (~150 KB comprimido)

# Instalación en RPi
pip install termostato-core-1.0.0.tar.gz
```

#### Opción C: Imagen Docker (Avanzado)

```dockerfile
# Dockerfile.rpi
FROM python:3.9-slim-buster

WORKDIR /app
COPY termostato/ ./termostato/
COPY config/ ./config/
COPY ejecutar.py .

CMD ["python", "ejecutar.py"]
```

```bash
# Construcción para ARM (RPi)
docker buildx build --platform linux/arm/v7 -t termostato-rpi:1.0.0 .
```

---

## 4. ESTRATEGIA DE INSTALACIÓN

### 4.1 Requisitos Previos en Raspberry Pi

```bash
# Sistema operativo
# Raspberry Pi OS Lite (32-bit) - Recomendado
# Raspberry Pi OS with desktop - Alternativa

# Python 3.7+ (viene preinstalado)
python3 --version

# pip (gestor de paquetes)
sudo apt update
sudo apt install python3-pip

# Git (opcional, para clonar repositorio)
sudo apt install git
```

### 4.2 Método 1: Instalación desde Wheel (Recomendado)

```bash
# 1. Transferir wheel a RPi
scp dist/termostato_core-1.0.0-py3-none-any.whl pi@192.168.0.14:/home/pi/

# 2. Conectarse a RPi
ssh pi@192.168.0.14

# 3. Instalar paquete
pip3 install termostato_core-1.0.0-py3-none-any.whl

# 4. Verificar instalación
termostato --version

# 5. Configurar
sudo nano /etc/termostato/termostato.json
```

### 4.3 Método 2: Instalación desde Repositorio Git

```bash
# 1. Clonar repositorio (solo core)
git clone --depth 1 https://github.com/usuario/ISSE_Termostato.git
cd ISSE_Termostato

# 2. Ejecutar script de instalación
chmod +x scripts/install_rpi.sh
sudo ./scripts/install_rpi.sh

# 3. Activar servicio
sudo systemctl enable termostato
sudo systemctl start termostato
```

### 4.4 Método 3: Instalación Manual (Desarrollo/Debug)

```bash
# 1. Crear directorio
sudo mkdir -p /opt/termostato

# 2. Copiar archivos CORE
sudo cp -r entidades servicios_dominio gestores_entidades \
          servicios_aplicacion agentes_sensores agentes_actuadores \
          configurador registrador ejecutar.py \
          /opt/termostato/

# 3. Copiar configuración
sudo mkdir -p /etc/termostato
sudo cp configurador/termostato.json /etc/termostato/

# 4. Crear logs
sudo mkdir -p /var/log/termostato

# 5. Crear usuario de sistema
sudo useradd -r -s /bin/false termostato

# 6. Permisos
sudo chown -R termostato:termostato /opt/termostato
sudo chown -R termostato:termostato /var/log/termostato
```

---

## 5. CONFIGURACIÓN Y OPTIMIZACIÓN

### 5.1 Configuración para Raspberry Pi

**`/etc/termostato/termostato.json`** (optimizado para RPi):

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
      "selector_temperatura": 14000,
      "display_temperatura": 14001,
      "display_bateria": 13005,
      "display_climatizador": 14002
    },
    "api_url": null
  },

  "ambiente": {
    "temperatura_inicial": 22.0,
    "histeresis": 2.0,
    "incremento_ajuste": 1.0
  },

  "bateria": {
    "carga_maxima": 5.0,
    "umbral_carga_baja": 0.8
  },

  "rpi": {
    "gpio_enabled": true,
    "sensor_type": "DHT22",
    "sensor_pin": 4,
    "relay_heat_pin": 17,
    "relay_cool_pin": 27,
    "led_status_pin": 22,
    "button_up_pin": 23,
    "button_down_pin": 24
  },

  "logging": {
    "level": "INFO",
    "file": "/var/log/termostato/termostato.log",
    "max_size_mb": 10,
    "backup_count": 5
  }
}
```

### 5.2 Servicio Systemd

**`/etc/systemd/system/termostato.service`**:

```ini
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
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/termostato /tmp

[Install]
WantedBy=multi-user.target
```

### 5.3 Optimizaciones para Raspberry Pi

#### CPU y Memoria

```python
# operador_paralelo.py - Ajustar intervalos para RPi
INTERVALO_BATERIA = 2          # Cada 2s (era 1s)
INTERVALO_TEMPERATURA = 5      # Cada 5s (era 2s)
INTERVALO_CLIMATIZADOR = 10    # Cada 10s (era 5s)
INTERVALO_VISUALIZACION = 10   # Cada 10s (era 5s)
```

#### Logging Optimizado

```python
# registrador.py - Rotación de logs
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    '/var/log/termostato/termostato.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
```

#### Reducir Threads en RPi Zero

```python
# Para RPi Zero (512 MB RAM), usar operador_secuencial.py
# en vez de operador_paralelo.py
```

---

## 6. PLAN DE DESPLIEGUE

### 6.1 Fase 1: Preparación (Semana 1)

#### Día 1-2: Creación de Paquetes

- [ ] Crear estructura de `termostato-core`
- [ ] Escribir `setup.py` para empaquetado
- [ ] Generar `requirements.txt` (vacío)
- [ ] Documentar `README.md`

#### Día 3-4: Scripts de Instalación

- [ ] Crear `install_rpi.sh`
- [ ] Crear servicio systemd
- [ ] Crear script de configuración GPIO
- [ ] Testear instalación en RPi limpio

#### Día 5: Testing

- [ ] Probar instalación desde wheel
- [ ] Probar instalación desde git
- [ ] Verificar servicio systemd
- [ ] Validar logs y auditoría

### 6.2 Fase 2: Construcción (Semana 2)

```bash
# 1. En máquina de desarrollo
cd /Users/victor/PycharmProjects/ISSE_Termostato

# 2. Crear estructura de distribución
python scripts/build_distribution.py

# 3. Construir wheel
python setup.py bdist_wheel

# 4. Verificar empaquetado
ls -lh dist/
# termostato_core-1.0.0-py3-none-any.whl  (~400 KB)

# 5. Opcional: Construir simuladores
cd simulators-package
python setup.py bdist_wheel
```

### 6.3 Fase 3: Despliegue (Semana 3)

#### Despliegue en Raspberry Pi de Prueba

```bash
# 1. Preparar RPi
ssh pi@192.168.0.14
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev

# 2. Transferir wheel
# Desde MacBook:
scp dist/termostato_core-1.0.0-py3-none-any.whl pi@192.168.0.14:/home/pi/

# 3. Instalar en RPi
ssh pi@192.168.0.14
pip3 install termostato_core-1.0.0-py3-none-any.whl

# 4. Configurar GPIO (si es necesario)
sudo raspi-config
# Interfaces > GPIO > Enable

# 5. Configurar sistema
sudo nano /etc/termostato/termostato.json

# 6. Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable termostato
sudo systemctl start termostato

# 7. Verificar funcionamiento
sudo systemctl status termostato
sudo journalctl -u termostato -f
```

#### Despliegue en Máquina de Desarrollo (Simuladores)

```bash
# 1. Instalar paquete de simuladores
pip install dist/termostato_simulators-1.0.0-py3-none-any.whl

# 2. Configurar IP de RPi
nano ~/.termostato/simuladores_config.json
{
  "raspberry_pi": {
    "host": "192.168.0.14",
    "puertos": {...}
  }
}

# 3. Lanzar simuladores
termostato-simulators start

# 4. Verificar conexión
# Los simuladores deben conectarse al RPi vía TCP
```

### 6.4 Fase 4: Validación (Semana 4)

#### Tests de Integración

- [ ] Comunicación RPi ↔ Simuladores
- [ ] Lectura de sensores reales (si disponible)
- [ ] Control de relays
- [ ] Logs y auditoría
- [ ] Consumo de recursos (top, htop)
- [ ] Estabilidad 24h continuas

#### Métricas de Rendimiento

```bash
# En RPi, monitorear recursos
watch -n 5 'ps aux | grep python'
watch -n 5 'free -h'
watch -n 5 'df -h'

# Logs
tail -f /var/log/termostato/termostato.log
tail -f /tmp/registro_auditoria
```

---

## 7. DISTRIBUCIÓN DE ARCHIVOS

### 7.1 Archivos Obligatorios en RPi

```
/opt/termostato/              # Código fuente
/etc/termostato/              # Configuración
/var/log/termostato/          # Logs
/tmp/registro_auditoria       # Auditoría temporal
/tmp/registro_errores         # Errores
```

### 7.2 Archivos Opcionales en MacBook/PC

```
~/termostato-dev/
├── actores_externos/         # Simuladores
├── Test/                     # Tests
├── docs/                     # Documentación
└── tools/                    # Herramientas de análisis
```

---

## 8. ESTRATEGIA DE ACTUALIZACIÓN

### 8.1 Update sin Downtime

```bash
# 1. Construir nueva versión
python setup.py bdist_wheel

# 2. Transferir a RPi
scp dist/termostato_core-1.1.0-py3-none-any.whl pi@192.168.0.14:/home/pi/

# 3. Actualizar con reinicio automático
ssh pi@192.168.0.14
pip3 install --upgrade termostato_core-1.1.0-py3-none-any.whl
sudo systemctl restart termostato

# 4. Verificar
sudo systemctl status termostato
```

### 8.2 Rollback

```bash
# Guardar versión anterior
pip3 install termostato_core==1.0.0 --force-reinstall
sudo systemctl restart termostato
```

---

## 9. CONCLUSIONES

### 9.1 Ventajas de esta Estrategia

✅ **Optimización de recursos**:
- Solo 375 KB de código en RPi
- Sin dependencias externas
- Consumo mínimo de RAM/CPU

✅ **Separación clara**:
- Core en RPi (producción)
- Simuladores en PC (desarrollo)
- Tests en PC (validación)

✅ **Fácil despliegue**:
- Wheel de ~400 KB
- Instalación con pip
- Servicio systemd automático

✅ **Mantenibilidad**:
- Updates rápidos
- Rollback sencillo
- Logs centralizados

### 9.2 Próximos Pasos Recomendados

1. **Crear scripts de empaquetado** (Día 1-2)
2. **Testear en RPi de prueba** (Día 3-5)
3. **Documentar proceso completo** (Día 6-7)
4. **Desplegar en producción** (Semana 2)

---

**Fin de la Estrategia de Despliegue**

*Documento creado: 2025-12-02*
*Versión: 1.0*
