# 🚀 ARQUITECTURA Y DESPLIEGUE - ISSE TERMOSTATO

> Sistema de Control de Climatización para Raspberry Pi con Clean Architecture

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Compatible-red.svg)](https://www.raspberrypi.org/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 📋 TABLA DE CONTENIDOS

- [Resumen Ejecutivo](#-resumen-ejecutivo)
- [Inicio Rápido](#-inicio-rápido)
- [Arquitectura](#-arquitectura)
- [Documentación](#-documentación)
- [Scripts Disponibles](#-scripts-disponibles)
- [Casos de Uso](#-casos-de-uso)

---

## 🎯 RESUMEN EJECUTIVO

### ¿Qué es ISSE_Termostato?

Sistema embebido de control de climatización implementado con **Clean Architecture**, diseñado para ejecutarse en **Raspberry Pi** con separación clara entre:

- **CORE** (~375 KB): Sistema de producción en Raspberry Pi
- **SIMULADORES** (~76 KB): Herramientas de desarrollo en MacBook/PC
- **TESTS + DOCS** (~700 KB): Suite de validación y documentación

### Características Principales

✅ **Sin dependencias externas** - Solo bibliotecas estándar de Python  
✅ **Bajo consumo** - 60 MB RAM, 7% CPU en RPi  
✅ **Arquitectura limpia** - 5 capas concéntricas bien definidas  
✅ **Despliegue automatizado** - Scripts listos para usar  
✅ **Alta calidad** - 8.1/10 en análisis de diseño  

---

## ⚡ INICIO RÁPIDO

### Opción 1: Despliegue Automático (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/vvalotto/ISSE_Termostato.git
cd ISSE_Termostato

# 2. Dar permisos (solo primera vez)
chmod +x scripts/*.sh

# 3. Desplegar a Raspberry Pi
./scripts/deploy_to_rpi.sh 192.168.0.14

# ¡Eso es todo! El sistema ya está corriendo en tu RPi
```

### Opción 2: Construcción Manual

```bash
# Construir paquete distribuible
./scripts/build_distribution.sh

# Ver archivos generados
ls -lh dist/
# - termostato_core-1.0.0-py3-none-any.whl  (~400 KB)
# - termostato-core-1.0.0.tar.gz             (~150 KB)
```

---

## 🏗️ ARQUITECTURA

### Vista de Despliegue

```
┌──────────────────────────────────────────────────────────────────┐
│  MacBook/PC (Desarrollo)                                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  📦 PAQUETE SIMULADORES (~76 KB)                          │  │
│  │  ├── simulador_temperatura.py                             │  │
│  │  ├── simulador_bateria.py                                 │  │
│  │  ├── cartel_temperatura.py                                │  │
│  │  └── [4 simuladores más...]                               │  │
│  │                                                            │  │
│  │  🧪 TESTS (183 tests, ~200 KB)                            │  │
│  │  📚 DOCS (~500 KB)                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                          ↕ TCP/IP Sockets
┌──────────────────────────────────────────────────────────────────┐
│  Raspberry Pi (Producción)                                       │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  📦 PAQUETE CORE (~375 KB código, ~400 KB wheel)          │  │
│  │  ├── entidades/           (Lógica de negocio)             │  │
│  │  ├── servicios_dominio/   (Algoritmos puros)              │  │
│  │  ├── gestores_entidades/  (Coordinación)                  │  │
│  │  ├── servicios_aplicacion/(Orquestación)                  │  │
│  │  ├── agentes_sensores/    (Lectura GPIO/I2C)              │  │
│  │  ├── agentes_actuadores/  (Control Relays/PWM)            │  │
│  │  ├── configurador/        (DI Container)                  │  │
│  │  └── registrador/         (Auditoría)                     │  │
│  └────────────────────────────────────────────────────────────┘  │
│                          ↕                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  🔧 HARDWARE                                               │  │
│  │  ├── Sensor DHT22/DS18B20 (GPIO 4)                        │  │
│  │  ├── ADC MCP3008 (SPI)                                    │  │
│  │  ├── Relays 5V                                            │  │
│  │  └── LEDs + Botones                                       │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Vista de Capas (Clean Architecture)

```
┌─────────────────────────────────────────────────────┐
│  🌐 LAYER 1: Frameworks & Drivers                  │
│     actores_externos/, configurador/                │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  🔌 LAYER 2: Interface Adapters                    │
│     agentes_sensores/, agentes_actuadores/          │
│     registrador/                                    │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  📋 LAYER 3: Use Cases                             │
│     servicios_aplicacion/, gestores_entidades/      │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  💎 LAYER 4: Entities                              │
│     entidades/ (Ambiente, Bateria, Climatizador)    │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  🧠 LAYER 5: Domain Services                       │
│     servicios_dominio/ (Controlador de temp.)       │
└─────────────────────────────────────────────────────┘
```

---

## 📚 DOCUMENTACIÓN

### Documentos Principales

| Documento | Descripción | Tamaño | Enlace |
|-----------|-------------|--------|--------|
| **Estrategia de Despliegue** | Arquitectura completa y planificación | 600+ líneas | [Ver](docs/estrategia_despliegue_raspberry_pi.md) |
| **Guía de Despliegue** | Paso a paso para usuarios | 400+ líneas | [Ver](DEPLOYMENT.md) |
| **Resumen de Despliegue** | Quick reference | 300+ líneas | [Ver](docs/RESUMEN_DESPLIEGUE.md) |
| **Análisis de Calidad** | Evaluación integral de diseño | 700+ líneas | [Ver](docs/Analisis%20de%20Calidad%20de%20Código/analisis_integral_calidad_diseno.md) |

### Documentos de Análisis

- 📊 [Métricas de Acoplamiento](docs/Mediciones/reporte_metricas_acoplamiento.md)
- 📊 [Métricas de Cohesión](docs/Mediciones/reporte_metricas_cohesion.md)
- 📊 [Métricas de Complejidad](docs/Mediciones/reporte_metricas_complejidad.md)
- 📊 [Métricas CK](docs/Mediciones/reporte_metricas_ck.md)
- 📊 [Clean Architecture](docs/Mediciones/reporte_metricas_clean_architecture.md)

---

## 🛠️ SCRIPTS DISPONIBLES

### Scripts de Despliegue

| Script | Descripción | Uso |
|--------|-------------|-----|
| `build_distribution.sh` | Construye paquete wheel | `./scripts/build_distribution.sh` |
| `deploy_to_rpi.sh` | Despliegue completo automático | `./scripts/deploy_to_rpi.sh <IP>` |
| `install_rpi.sh` | Instalación en RPi (local) | `sudo ./scripts/install_rpi.sh` |

### Archivos de Empaquetado

| Archivo | Descripción |
|---------|-------------|
| `setup.py` | Configuración setuptools |
| `pyproject.toml` | Configuración moderna Python |
| `MANIFEST.in` | Define archivos a incluir |

---

## 💡 CASOS DE USO

### Caso 1: Primer Despliegue

```bash
# Preparar Raspberry Pi
# - Instalar Raspberry Pi OS
# - Configurar SSH: sudo raspi-config
# - Conectar a red

# Desde MacBook
./scripts/deploy_to_rpi.sh 192.168.0.14

# Verificar
ssh pi@192.168.0.14 'sudo systemctl status termostato'
```

### Caso 2: Actualización de Software

```bash
# Hacer cambios al código
# ... editar archivos ...

# Re-desplegar (actualización automática)
./scripts/deploy_to_rpi.sh 192.168.0.14
```

### Caso 3: Desarrollo con Simuladores

```bash
# Terminal 1 - RPi ejecutando sistema
ssh pi@192.168.0.14
sudo journalctl -u termostato -f

# Terminal 2 - Simuladores en MacBook
cd actores_externos
./lanzar_simuladores.sh

# Los simuladores se conectan automáticamente al RPi
```

### Caso 4: Modo Standalone (Sin Red)

```bash
# Editar configuración en RPi
ssh pi@192.168.0.14
sudo nano /etc/termostato/termostato.json

# Cambiar proxies a "archivo"
# Guardar y reiniciar
sudo systemctl restart termostato
```

---

## 📊 MÉTRICAS DEL SISTEMA

### Calidad de Diseño

| Dimensión | Calificación | Estado |
|-----------|--------------|--------|
| Complejidad | 9.5/10 | ✅ Excelente |
| Cohesión | 9.0/10 | ✅ Excelente |
| Acoplamiento | 8.8/10 | ✅ Excelente |
| Métricas CK | 10.0/10 | ✅ Perfecto |
| SOLID | 8.5/10 | ✅ Muy bueno |
| **TOTAL** | **8.1/10** | ✅ Muy buena calidad |

### Rendimiento en RPi

| Métrica | Valor | Límite |
|---------|-------|--------|
| RAM | ~60 MB | 100 MB |
| CPU | ~7% | 20% |
| Almacenamiento | ~10 MB | 50 MB |
| Threads | 5 | 10 |

---

## 🔧 CONFIGURACIÓN

### Archivo Principal

`/etc/termostato/termostato.json`:

```json
{
  "proxy_sensor_temperatura": "archivo",  // o "socket"
  "proxy_bateria": "archivo",             // o "socket"
  "climatizador": "climatizador",         // o "calefactor"
  "visualizador_temperatura": "consola",  // o "socket" o "api"
  
  "red": {
    "host_escucha": "0.0.0.0",
    "puertos": {
      "temperatura": 12000,
      "bateria": 11000
    }
  }
}
```

### Servicio Systemd

```bash
# Gestión del servicio
sudo systemctl status termostato    # Ver estado
sudo systemctl restart termostato   # Reiniciar
sudo systemctl stop termostato      # Detener
sudo journalctl -u termostato -f    # Ver logs
```

---

## 🎯 REQUISITOS

### Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Raspberry Pi | Zero W | 3 Model B+ |
| RAM | 512 MB | 1 GB+ |
| Storage | 8 GB | 16 GB+ |

### Software

- Raspberry Pi OS (Lite o Full)
- Python 3.7+
- SSH habilitado
- Red configurada

---

## 📞 SOPORTE

### Recursos

- 📖 [Documentación Completa](docs/)
- 🐛 [Issues](https://github.com/vvalotto/ISSE_Termostato/issues)
- 💬 [Discussions](https://github.com/vvalotto/ISSE_Termostato/discussions)

### Comandos Útiles

```bash
# Ver estado del sistema
ssh pi@<IP> 'sudo systemctl status termostato'

# Ver logs en tiempo real
ssh pi@<IP> 'sudo journalctl -u termostato -f'

# Verificar configuración
ssh pi@<IP> 'cat /etc/termostato/termostato.json'

# Monitorear recursos
ssh pi@<IP> 'top -p $(pgrep -f termostato)'
```

---

## 🚀 PRÓXIMOS PASOS

1. **Leer documentación**:
   - [Estrategia de Despliegue](docs/estrategia_despliegue_raspberry_pi.md)
   - [Guía de Despliegue](DEPLOYMENT.md)

2. **Preparar Raspberry Pi**:
   - Instalar OS
   - Configurar red y SSH

3. **Desplegar**:
   ```bash
   ./scripts/deploy_to_rpi.sh <IP>
   ```

4. **Validar**:
   - Verificar servicio
   - Ver logs
   - Probar funcionalidad

---

## 📄 LICENCIA

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

## 👤 AUTOR

**Victor Valotto**
- GitHub: [@vvalotto](https://github.com/vvalotto)
- Proyecto: ISSE_Termostato

---

**Última actualización**: 2025-12-02  
**Versión**: 1.0.0  
**Estado**: ✅ Producción Ready
