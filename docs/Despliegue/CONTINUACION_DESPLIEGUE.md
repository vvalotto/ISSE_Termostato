# CONTINUACIÓN DEL DESPLIEGUE - TERMOSTATO RASPBERRY PI

**Fecha**: 2025-12-02
**Estado**: Paquete construido y listo para instalación en Raspberry Pi
**Próximo paso**: Instalación limpia en producción

---

## 📊 ESTADO ACTUAL

### ✅ Completado

1. **Paquete wheel construido correctamente**:
   - Archivo: `dist/termostato_core-1.0.0-py3-none-any.whl` (35 KB)
   - Compatible con: Python 3.5+ (necesario para RPi con Python 3.5.3)
   - Incluye todos los módulos CORE necesarios
   - Entry point configurado correctamente

2. **Correcciones aplicadas al código**:
   - **setup.py**: Agregado `py_modules=['ejecutar']` para incluir ejecutar.py
   - **setup.py y pyproject.toml**: Cambiado `python_requires='>=3.5'` (era >=3.7)
   - **ejecutar.py**: Agregada función `main()` como entry point
   - **configurador.py**: Modificado para buscar `termostato.json` en múltiples ubicaciones:
     - `./termostato.json` (directorio actual)
     - `/etc/termostato/termostato.json` (ubicación estándar Linux)
     - `{paquete}/configurador/termostato.json` (incluido en el paquete)

3. **Raspberry Pi preparada**:
   - IP: 192.168.0.14
   - Sistema operativo: Raspberry Pi OS (con Python 3.5.3)
   - SSH habilitado
   - Red configurada
   - Instalaciones previas limpiadas completamente

### ⏸️ Pendiente

1. Transferir paquete wheel a Raspberry Pi
2. Instalar paquete en RPi
3. Configurar directorios del sistema
4. Copiar archivo de configuración
5. Crear servicio systemd
6. Iniciar y validar funcionamiento

---

## 🔧 PROBLEMAS RESUELTOS

### Problema 1: Versión de Python incompatible
**Error**: `termostato-core requires Python '>=3.7' but the running Python is 3.5.3`

**Solución aplicada**:
- Modificado `setup.py` y `pyproject.toml` para requerir Python >=3.5
- El código no usa características exclusivas de Python 3.7+ (no hay f-strings)

### Problema 2: Módulo ejecutar.py no se instalaba
**Error**: `ImportError: No module named 'ejecutar'`

**Solución aplicada**:
- Agregado `py_modules=['ejecutar']` en setup.py
- Agregada función `main()` en ejecutar.py para el entry point

### Problema 3: No encontraba termostato.json
**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'termostato.json'`

**Solución aplicada**:
- Modificado `configurador.py` para buscar en múltiples ubicaciones
- Prioridad: directorio actual → /etc/termostato → paquete instalado

---

## 📦 ARCHIVOS LISTOS PARA DESPLIEGUE

### En MacBook (listos para transferir)

```
/Users/victor/PycharmProjects/ISSE_Termostato/
├── dist/
│   ├── termostato_core-1.0.0-py3-none-any.whl  ← ARCHIVO PRINCIPAL
│   ├── termostato_core-1.0.0.tar.gz
│   └── checksums.txt
├── scripts/
│   ├── build_distribution.sh          (construir paquete)
│   ├── deploy_to_rpi.sh               (despliegue automático)
│   └── install_rpi.sh                 (instalación en RPi)
└── configurador/
    └── termostato.json                (configuración de referencia)
```

### Verificar integridad del paquete

```bash
# Desde MacBook, verificar contenido del wheel
cd /Users/victor/PycharmProjects/ISSE_Termostato
unzip -l dist/termostato_core-1.0.0-py3-none-any.whl

# Debe incluir:
# - ejecutar.py
# - entidades/
# - servicios_dominio/
# - gestores_entidades/
# - servicios_aplicacion/
# - agentes_sensores/
# - agentes_actuadores/
# - configurador/ (con termostato.json)
# - registrador/
```

---

## 🚀 PASOS PARA CONTINUAR LA INSTALACIÓN

### FASE 1: TRANSFERENCIA E INSTALACIÓN (5 minutos)

#### Paso 1.1: Transferir paquete wheel

Desde tu **MacBook**, ejecuta:

```bash
scp /Users/victor/PycharmProjects/ISSE_Termostato/dist/termostato_core-1.0.0-py3-none-any.whl pi@192.168.0.14:/home/pi/
```

**Verificación**: Te pedirá la contraseña de la Raspberry Pi.

---

#### Paso 1.2: Conectar a Raspberry Pi

```bash
ssh pi@192.168.0.14
```

**Verificación**: Deberías ver el prompt `pi@raspberrypi:~ $`

---

#### Paso 1.3: Verificar que el archivo se transfirió

En la **Raspberry Pi**:

```bash
ls -lh /home/pi/termostato_core-1.0.0-py3-none-any.whl
```

**Verificación**: Debería mostrar el archivo con ~35 KB

---

#### Paso 1.4: Instalar el paquete

```bash
pip3 install --user termostato_core-1.0.0-py3-none-any.whl
```

**Verificación exitosa**: Debería mostrar:
```
Successfully installed termostato-core-1.0.0
```

---

#### Paso 1.5: Verificar instalación

```bash
pip3 show termostato-core
```

**Verificación exitosa**: Debería mostrar:
```
Name: termostato-core
Version: 1.0.0
Location: /home/pi/.local/lib/python3.5/site-packages
Requires-Python: >=3.5
```

---

#### Paso 1.6: Probar import básico

```bash
python3 -c "from ejecutar import main; print('✓ Import exitoso!')"
```

**Verificación exitosa**: Debe imprimir `✓ Import exitoso!`

---

### FASE 2: CONFIGURACIÓN DEL SISTEMA (5 minutos)

#### Paso 2.1: Crear estructura de directorios

```bash
# Crear directorios necesarios
sudo mkdir -p /etc/termostato
sudo mkdir -p /var/log/termostato
sudo mkdir -p /tmp

# Verificar creación
ls -ld /etc/termostato /var/log/termostato
```

**Verificación exitosa**:
```
drwxr-xr-x 2 root root 4096 ... /etc/termostato
drwxr-xr-x 2 root root 4096 ... /var/log/termostato
```

---

#### Paso 2.2: Encontrar ubicación del paquete instalado

```bash
pip3 show -f termostato-core | grep Location
```

**Resultado esperado**:
```
Location: /home/pi/.local/lib/python3.5/site-packages
```

**Importante**: Anota esta ruta, la necesitarás en el siguiente paso.

---

#### Paso 2.3: Copiar archivo de configuración

Usando la ruta del paso anterior:

```bash
# Copiar termostato.json al directorio del sistema
sudo cp /home/pi/.local/lib/python3.5/site-packages/configurador/termostato.json /etc/termostato/

# Verificar que se copió correctamente
cat /etc/termostato/termostato.json
```

**Verificación exitosa**: Debería mostrar el contenido JSON de la configuración.

---

#### Paso 2.4: Ajustar permisos

```bash
# Dar permisos al usuario pi
sudo chown -R pi:pi /var/log/termostato
sudo chmod 755 /etc/termostato
sudo chmod 644 /etc/termostato/termostato.json

# Verificar permisos
ls -la /etc/termostato/
ls -la /var/log/termostato/
```

**Verificación exitosa**:
```
-rw-r--r-- 1 root root ... termostato.json
drwxr-xr-x 2 pi   pi   ... /var/log/termostato/
```

---

#### Paso 2.5: Probar ejecución manual

```bash
# Ejecutar manualmente (presiona Ctrl+C después de unos segundos)
python3 -c "from ejecutar import main; main()"
```

**Verificación exitosa**: Debería iniciar el sistema y mostrar mensajes como:
- Carga de configuración
- Inicialización de componentes
- Inicio de threads (batería, temperatura, climatizador)

**Presiona Ctrl+C para detener** después de verificar que arranca.

---

### FASE 3: SERVICIO SYSTEMD (10 minutos)

#### Paso 3.1: Crear archivo del servicio

```bash
sudo nano /etc/systemd/system/termostato.service
```

**Copia y pega este contenido**:

```ini
[Unit]
Description=Termostato ISSE - Sistema de Control de Climatización
After=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 -m ejecutar
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Límites de recursos
MemoryLimit=100M
CPUQuota=20%

# Variables de entorno
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

**Guardar**: `Ctrl+O`, `Enter`, `Ctrl+X`

---

#### Paso 3.2: Recargar systemd

```bash
sudo systemctl daemon-reload
```

---

#### Paso 3.3: Habilitar servicio en arranque

```bash
sudo systemctl enable termostato
```

**Verificación exitosa**: `Created symlink ...`

---

#### Paso 3.4: Iniciar servicio

```bash
sudo systemctl start termostato
```

---

#### Paso 3.5: Verificar estado del servicio

```bash
sudo systemctl status termostato
```

**Verificación exitosa**: Debería mostrar:
```
● termostato.service - Termostato ISSE - Sistema de Control de Climatización
   Loaded: loaded (/etc/systemd/system/termostato.service; enabled)
   Active: active (running) since ...
   ...
```

Si ves `Active: active (running)`, ¡el servicio está funcionando! ✅

---

### FASE 4: VALIDACIÓN Y MONITOREO (Continuo)

#### Paso 4.1: Ver logs en tiempo real

```bash
sudo journalctl -u termostato -f
```

**Presiona Ctrl+C** para salir de los logs.

---

#### Paso 4.2: Ver últimas 50 líneas de logs

```bash
sudo journalctl -u termostato -n 50
```

---

#### Paso 4.3: Verificar archivos de auditoría

```bash
# Ver registro de auditoría
tail -20 /tmp/registro_auditoria

# Ver registro de errores (si existe)
tail -20 /tmp/registro_errores 2>/dev/null || echo "Sin errores registrados"
```

---

#### Paso 4.4: Verificar puertos abiertos (si usa sockets)

```bash
sudo netstat -tulpn | grep python
```

**Esperado** (si usa configuración con sockets):
```
tcp  0.0.0.0:11000  ... LISTEN  ... python3
tcp  0.0.0.0:12000  ... LISTEN  ... python3
...
```

---

#### Paso 4.5: Monitorear uso de recursos

```bash
# Ver procesos Python
ps aux | grep python

# Ver uso de recursos del proceso termostato
top -p $(pgrep -f termostato)
```

**Presiona `q`** para salir de `top`.

---

## 📋 COMANDOS ÚTILES DE GESTIÓN

### Gestión del Servicio

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

# Últimas N líneas
sudo journalctl -u termostato -n 100

# Logs desde hace X minutos
sudo journalctl -u termostato --since "5 minutes ago"

# Logs de hoy
sudo journalctl -u termostato --since today

# Logs con nivel de error
sudo journalctl -u termostato -p err
```

### Monitoreo de Recursos

```bash
# Ver uso de CPU y RAM
top -p $(pgrep -f termostato)

# Memoria total usada
ps aux | grep termostato | awk '{print $6}'

# Procesos y threads
ps -eLf | grep termostato
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### Editar Configuración

```bash
# Editar configuración principal
sudo nano /etc/termostato/termostato.json

# Después de editar, reiniciar servicio
sudo systemctl restart termostato
```

### Configuración para Hardware Real

Si tienes sensores y actuadores reales, modifica:

```json
{
  "proxy_bateria": "archivo",              // Cambiar a "socket" si es remoto
  "proxy_sensor_temperatura": "archivo",   // Cambiar a "socket" si es remoto
  "climatizador": "climatizador",
  "actuador_climatizador": "general",

  "rpi": {
    "gpio_enabled": true,
    "sensor_type": "DHT22",
    "sensor_pin": 4,
    "relay_heat_pin": 17,
    "relay_cool_pin": 27
  }
}
```

### Configuración para Modo Simulación

Para probar con simuladores en tu MacBook:

```json
{
  "proxy_bateria": "socket",
  "proxy_sensor_temperatura": "socket",

  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": {
      "bateria": 11000,
      "temperatura": 12000
    }
  }
}
```

---

## 🔍 TROUBLESHOOTING

### Problema: Servicio no inicia

**Síntomas**: `systemctl status termostato` muestra `failed`

**Diagnóstico**:
```bash
# Ver logs de error
sudo journalctl -u termostato -n 50 --no-pager

# Probar ejecución manual
python3 -c "from ejecutar import main; main()"
```

**Soluciones comunes**:
1. Verificar que `/etc/termostato/termostato.json` existe
2. Verificar permisos de `/var/log/termostato`
3. Verificar que el paquete está instalado: `pip3 show termostato-core`

---

### Problema: No encuentra termostato.json

**Error**: `FileNotFoundError: ERROR: No se encontró el archivo termostato.json`

**Solución**:
```bash
# Verificar que existe
ls -la /etc/termostato/termostato.json

# Si no existe, copiarlo
sudo cp /home/pi/.local/lib/python3.5/site-packages/configurador/termostato.json /etc/termostato/

# Verificar permisos
sudo chmod 644 /etc/termostato/termostato.json
```

---

### Problema: Error de importación

**Error**: `ImportError: No module named 'XXX'`

**Solución**:
```bash
# Reinstalar paquete
pip3 uninstall -y termostato-core
pip3 install --user /home/pi/termostato_core-1.0.0-py3-none-any.whl

# Verificar instalación
pip3 show termostato-core
python3 -c "from ejecutar import main; print('OK')"
```

---

### Problema: Consumo alto de recursos

**Síntomas**: CPU > 20% o RAM > 100 MB

**Diagnóstico**:
```bash
# Ver uso actual
top -p $(pgrep -f termostato)
```

**Solución**: Editar `/etc/termostato/termostato.json` y aumentar intervalos:
```json
{
  "intervalos": {
    "bateria": 2,
    "temperatura": 5,
    "climatizador": 10
  }
}
```

---

### Problema: Puertos ya en uso

**Error**: `Address already in use`

**Solución**:
```bash
# Ver qué proceso usa el puerto
sudo netstat -tulpn | grep :12000

# Matar proceso (si es necesario)
sudo kill <PID>

# O cambiar puerto en configuración
sudo nano /etc/termostato/termostato.json
```

---

## 📊 MÉTRICAS ESPERADAS

### Recursos del Sistema (Raspberry Pi 3 Model B)

| Métrica | Valor Normal | Umbral Crítico | Acción si excede |
|---------|--------------|----------------|------------------|
| RAM | 50-80 MB | 100 MB | Revisar memory leaks |
| CPU | 5-10% | 20% | Aumentar intervalos |
| Threads | 5-6 | 10 | Revisar deadlocks |
| Almacenamiento | ~10 MB | 50 MB | Limpiar logs antiguos |

### Indicadores de Funcionamiento Correcto

✅ Servicio en estado `active (running)`
✅ Logs sin errores críticos
✅ Archivos de auditoría creciendo (`/tmp/registro_auditoria`)
✅ CPU < 20%
✅ RAM < 100 MB
✅ Threads activos (5-6 threads normalmente)

---

## 🔄 ACTUALIZACIÓN DEL SISTEMA

### Actualizar a Nueva Versión

```bash
# 1. Desde MacBook - Reconstruir paquete
cd /Users/victor/PycharmProjects/ISSE_Termostato
./scripts/build_distribution.sh

# 2. Transferir nueva versión
scp dist/termostato_core-1.0.0-py3-none-any.whl pi@192.168.0.14:/home/pi/termostato_nuevo.whl

# 3. En RPi - Actualizar
ssh pi@192.168.0.14
pip3 install --user --upgrade termostato_nuevo.whl
sudo systemctl restart termostato

# 4. Verificar
sudo systemctl status termostato
```

---

## 📞 CHECKLIST FINAL DE VALIDACIÓN

Una vez completada la instalación, verifica:

- [ ] **Instalación**: `pip3 show termostato-core` muestra versión 1.0.0
- [ ] **Configuración**: `/etc/termostato/termostato.json` existe y es válido
- [ ] **Directorios**: `/var/log/termostato` existe con permisos correctos
- [ ] **Import**: `python3 -c "from ejecutar import main; print('OK')"` funciona
- [ ] **Servicio habilitado**: `systemctl is-enabled termostato` → `enabled`
- [ ] **Servicio corriendo**: `systemctl is-active termostato` → `active`
- [ ] **Sin errores**: `journalctl -u termostato -p err -n 10` sin errores críticos
- [ ] **Auditoría**: `/tmp/registro_auditoria` existe y crece
- [ ] **Recursos**: CPU < 20%, RAM < 100 MB

---

## 📚 REFERENCIAS RÁPIDAS

### Estructura de Archivos en Raspberry Pi

```
/home/pi/
├── termostato_core-1.0.0-py3-none-any.whl (instalador)
└── .local/lib/python3.5/site-packages/   (código instalado)
    ├── entidades/
    ├── servicios_dominio/
    ├── gestores_entidades/
    ├── servicios_aplicacion/
    ├── agentes_sensores/
    ├── agentes_actuadores/
    ├── configurador/
    │   └── termostato.json (backup)
    ├── registrador/
    └── ejecutar.py

/etc/termostato/
└── termostato.json          (configuración activa)

/var/log/termostato/         (logs del sistema)

/tmp/
├── registro_auditoria       (eventos del sistema)
└── registro_errores         (errores capturados)

/etc/systemd/system/
└── termostato.service       (definición del servicio)
```

### Puertos por Defecto

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 11000 | Batería | Lectura de nivel de batería |
| 12000 | Temperatura | Lectura de temperatura |
| 13000 | Seteo Temperatura | Establecer temperatura deseada |
| 14000 | Selector Temperatura | Selector de modo |
| 14001 | Display Temperatura | Visualización remota |
| 13005 | Display Batería | Visualización remota |
| 14002 | Display Climatizador | Visualización remota |

---

## ✅ INSTALACIÓN EXITOSA

Cuando veas esto, la instalación está completa:

```bash
pi@raspberrypi:~ $ sudo systemctl status termostato
● termostato.service - Termostato ISSE - Sistema de Control de Climatización
   Loaded: loaded (/etc/systemd/system/termostato.service; enabled)
   Active: active (running) since Mon 2025-12-02 16:30:00 UTC; 5min ago
 Main PID: 1234 (python3)
   CGroup: /system.slice/termostato.service
           └─1234 /usr/bin/python3 -m ejecutar

Dec 02 16:30:00 raspberrypi systemd[1]: Started Termostato ISSE...
Dec 02 16:30:01 raspberrypi python3[1234]: Configuración cargada desde /etc/termostato/termostato.json
Dec 02 16:30:01 raspberrypi python3[1234]: Sistema inicializado correctamente
```

---

**Documento creado**: 2025-12-02
**Última actualización**: 2025-12-02
**Versión del paquete**: 1.0.0
**Raspberry Pi**: 192.168.0.14

---

**¡Listo para continuar el despliegue!** 🚀
