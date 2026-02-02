# Documento de Diseño: Proyecto ISSE_Simuladores

## Información del Proyecto

**Proyecto:** ISSE_Simuladores - Simuladores HIL para Termostato
**Fecha:** Diciembre 2025
**Autor:** Victor Valotto
**Objetivo:** Crear aplicaciones desktop PyQt6 para simulación Hardware-in-the-Loop (HIL) del sistema de termostato embebido.

---

## 1. Descripción General

### 1.1 Propósito

Desarrollar un conjunto de simuladores desktop que permitan realizar testing HIL (Hardware-in-the-Loop) del sistema ISSE_Termostato ejecutándose en Raspberry Pi, sin necesidad de hardware físico de sensores.

### 1.2 Productos de Software

El proyecto contiene **3 productos independientes**:

| Producto | Descripción | Comunicación |
|----------|-------------|--------------|
| **Simulador Temperatura** | Simula sensor de temperatura | Cliente TCP → Puerto 14001 |
| **Simulador Batería** | Simula sensor de batería | Cliente TCP → Puerto 14002 |
| **UX Termostato** | Interfaz de usuario del termostato | Servidor 14003 / Cliente 14004 |

### 1.3 Arquitectura HIL

```
┌─────────────────────────────────────────────────────────┐
│  ISSE_Simuladores (Mac/PC)                              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Simulador      │  │  Simulador      │              │
│  │  Temperatura    │  │  Batería        │              │
│  │  (PyQt6)        │  │  (PyQt6)        │              │
│  └────────┬────────┘  └────────┬────────┘              │
│           │ :14001             │ :14002                │
│           └──────────┬─────────┘                       │
│                      │                                  │
│  ┌───────────────────┴───────────────────┐             │
│  │       UX Desktop Termostato           │             │
│  │       (PyQt6)                         │             │
│  │       Servidor: 14003 / Cliente: 14004│             │
│  └───────────────────┬───────────────────┘             │
└──────────────────────┼──────────────────────────────────┘
                       │ TCP/IP (Red local)
                       ▼
┌─────────────────────────────────────────────────────────┐
│  RASPBERRY PI - ISSE_Termostato                         │
│                                                         │
│  Servidores (reciben de simuladores):                   │
│  - ProxySensorTemperatura: 14001                        │
│  - ProxyBateria: 14002                                  │
│                                                         │
│  Clientes (envían a UX):                                │
│  - VisualizadorTemperatura: 14003                       │
│  - ActuadorClimatizador: 14004                          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Creación del Proyecto en PyCharm

### 2.1 Pasos para Crear el Proyecto

1. **Abrir PyCharm** → File → New Project

2. **Configurar proyecto:**
   - **Location:** `/Users/victor/PycharmProjects/ISSE_Simuladores`
   - **Python Interpreter:** Python 3.12+
   - **Create a main.py welcome script:** No (desmarcar)

3. **Crear estructura de carpetas** (ver sección 3)

4. **Configurar Virtual Environment:**
   ```bash
   cd /Users/victor/PycharmProjects/ISSE_Simuladores
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configurar PyCharm:**
   - Settings → Project → Python Interpreter → Seleccionar venv
   - Settings → Project → Project Structure → Marcar carpetas como Sources

### 2.2 Configuración de Git

```bash
cd /Users/victor/PycharmProjects/ISSE_Simuladores
git init
git remote add origin https://github.com/vvalotto/ISSE_Simuladores.git
```

---

## 3. Estructura del Proyecto

```
ISSE_Simuladores/
│
├── README.md                           # Documentación principal
├── requirements.txt                    # Dependencias globales
├── config.json                         # Configuración de red compartida
├── .env.example                        # Variables de entorno de ejemplo
├── .gitignore
│
├── docs/                               # Documentación general
│   ├── arquitectura.md
│   ├── protocolo_comunicacion.md
│   └── manual_usuario.md
│
├── simulador_temperatura/              # PRODUCTO 1
│   ├── run.py                          # Punto de entrada
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── configuracion/
│   │   │   ├── __init__.py
│   │   │   ├── config.py               # Configuración del producto
│   │   │   └── configurador.py         # Singleton
│   │   ├── servicios/
│   │   │   ├── __init__.py
│   │   │   └── ui_principal.py         # Ventana PyQt6
│   │   ├── general/
│   │   │   ├── __init__.py
│   │   │   └── generador_temperatura.py # Lógica de simulación
│   │   └── datos/
│   │       ├── __init__.py
│   │       └── socket_client.py        # Cliente TCP
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_generador.py
│   │   └── test_socket.py
│   └── quality/
│       ├── requirements.txt
│       ├── scripts/
│       │   ├── calculate_metrics.py
│       │   ├── validate_gates.py
│       │   └── generate_report.py
│       └── reports/
│
├── simulador_bateria/                  # PRODUCTO 2
│   ├── run.py
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── configuracion/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── configurador.py
│   │   ├── servicios/
│   │   │   ├── __init__.py
│   │   │   └── ui_principal.py
│   │   ├── general/
│   │   │   ├── __init__.py
│   │   │   ├── simulador_descarga.py   # Lógica de descarga
│   │   │   └── simulador_carga.py      # Lógica de carga
│   │   └── datos/
│   │       ├── __init__.py
│   │       └── socket_client.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_simulador.py
│   │   └── test_socket.py
│   └── quality/
│       ├── requirements.txt
│       ├── scripts/
│       │   ├── calculate_metrics.py
│       │   ├── validate_gates.py
│       │   └── generate_report.py
│       └── reports/
│
├── ux_termostato/                      # PRODUCTO 3
│   ├── run.py
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── configuracion/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── configurador.py
│   │   ├── servicios/
│   │   │   ├── __init__.py
│   │   │   └── ui_principal.py         # Ventana principal
│   │   ├── general/
│   │   │   ├── __init__.py
│   │   │   └── estado_termostato.py    # Modelo de estado
│   │   ├── datos/
│   │   │   ├── __init__.py
│   │   │   ├── socket_server.py        # Servidor TCP (recibe)
│   │   │   └── socket_client.py        # Cliente TCP (envía)
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── display_lcd.py
│   │       ├── clima_indicator.py
│   │       ├── led_indicator.py
│   │       └── temperature_chart.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_estado.py
│   │   ├── test_widgets.py
│   │   └── test_networking.py
│   └── quality/
│       ├── requirements.txt
│       ├── scripts/
│       │   ├── calculate_metrics.py
│       │   ├── validate_gates.py
│       │   └── generate_report.py
│       └── reports/
│
├── compartido/                         # Código reutilizable
│   ├── __init__.py
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── led_indicator.py
│   │   ├── config_panel.py
│   │   └── log_viewer.py
│   ├── networking/
│   │   ├── __init__.py
│   │   ├── base_socket_client.py
│   │   └── base_socket_server.py
│   └── estilos/
│       └── dark_theme.qss
│
└── assets/
    └── icons/
        ├── temperatura.png
        ├── bateria.png
        └── termostato.png
```

---

## 4. Dependencias

### 4.1 Dependencias Globales

**Archivo:** `requirements.txt`

```
# UI Framework
PyQt6==6.7.0
PyQt6-Qt6==6.7.0
PyQt6-sip==13.6.0

# Gráficos
pyqtgraph==0.13.3

# Utilidades
python-dotenv==1.0.0

# Testing
pytest==8.0.0
pytest-qt==4.2.0

# Calidad (para quality/)
radon>=6.0.1
pylint>=3.0.0
pytest-cov>=4.1.0
```

### 4.2 Dependencias de Quality (por producto)

**Archivo:** `<producto>/quality/requirements.txt`

```
radon>=6.0.1
pylint>=3.0.0
pytest>=8.0.0
pytest-cov>=4.1.0
```

---

## 5. Configuración Compartida

### 5.1 Configuración de Red

**Archivo:** `config.json`

```json
{
  "version": "1.0.0",
  "raspberry": {
    "ip": "192.168.1.50",
    "puertos": {
      "sensor_temperatura": 14001,
      "sensor_bateria": 14002,
      "visualizador": 14003,
      "control": 14004
    }
  },
  "simulador_temperatura": {
    "intervalo_envio": 2,
    "temperatura_inicial": 22.0,
    "rango_min": -10.0,
    "rango_max": 40.0,
    "ruido_amplitud": 0.3
  },
  "simulador_bateria": {
    "intervalo_envio": 5,
    "voltaje_max": 4.2,
    "voltaje_min": 3.0,
    "voltaje_inicial": 3.7,
    "tasa_descarga": 0.01,
    "tasa_carga": 0.02
  },
  "ux_termostato": {
    "intervalo_actualizacion": 1000,
    "rango_temp_min": 15.0,
    "rango_temp_max": 35.0,
    "step_temperatura": 0.5,
    "historico_minutos": 10
  }
}
```

### 5.2 Variables de Entorno

**Archivo:** `.env.example`

```bash
# Configuración de red
RASPBERRY_IP=192.168.1.50

# Puertos
PUERTO_TEMPERATURA=14001
PUERTO_BATERIA=14002
PUERTO_VISUALIZADOR=14003
PUERTO_CONTROL=14004

# Modo desarrollo
DEBUG=true
```

---

## 6. Agentes de Calidad

### 6.1 Descripción General

Cada producto tiene su propio ambiente de calidad (`quality/`) con:
- Scripts de análisis de métricas
- Validación de puertas de calidad
- Generación de reportes

### 6.2 Quality Gates (Puertas de Calidad)

| Gate | Métrica | Umbral | Descripción |
|------|---------|--------|-------------|
| **Complejidad** | CC Promedio | ≤ 10 | Complejidad ciclomática |
| **Mantenibilidad** | MI Promedio | > 20 | Índice de mantenibilidad |
| **Pylint** | Score | ≥ 8.0 | Puntuación de calidad |

### 6.3 Grados de Calidad

| Grado | Gates Pasados | Descripción |
|-------|---------------|-------------|
| **A** | 3/3 | Excelente - Sin issues bloqueantes |
| **B** | 2/3 | Bueno - 1 issue bloqueante |
| **C** | 1/3 | Regular - 2 issues bloqueantes |
| **F** | 0/3 | Falla - 3 issues bloqueantes |

### 6.4 Scripts de Calidad

#### A. calculate_metrics.py

**Propósito:** Calcular métricas de calidad del código.

**Métricas calculadas:**
- **Tamaño:** LOC, SLOC, comentarios, líneas en blanco
- **Complejidad:** CC promedio, máximo, distribución por grado
- **Mantenibilidad:** MI promedio, mínimo, módulos bajo umbral
- **Pylint:** Score, errores, warnings, refactor, convención

**Uso:**
```bash
cd simulador_temperatura
python quality/scripts/calculate_metrics.py app
```

**Salida:** JSON en `quality/reports/quality_YYYYMMDD_HHMMSS.json`

#### B. validate_gates.py

**Propósito:** Validar que las métricas cumplan los umbrales.

**Uso:**
```bash
python quality/scripts/validate_gates.py quality/reports/quality_YYYYMMDD_HHMMSS.json
```

**Salida:** Estado PASS/FAIL de cada gate + recomendaciones si hay fallas.

#### C. generate_report.py

**Propósito:** Generar reporte Markdown legible.

**Uso:**
```bash
python quality/scripts/generate_report.py quality/reports/quality_YYYYMMDD_HHMMSS.json
```

**Salida:** Markdown en `quality/reports/quality_report_YYYYMMDD_HHMMSS.md`

### 6.5 Flujo de Calidad

```
┌─────────────────────────────────────────────────────────┐
│ FLUJO DE CALIDAD POR PRODUCTO                           │
└─────────────────────────────────────────────────────────┘

1. Desarrollador modifica código en app/

2. Ejecutar análisis de métricas:
   $ python quality/scripts/calculate_metrics.py app

   → Genera: quality/reports/quality_YYYYMMDD_HHMMSS.json
   → Imprime resumen en consola
   → Return code: 0 (OK), 1 (issues), 2 (error)

3. Validar quality gates:
   $ python quality/scripts/validate_gates.py quality/reports/quality_*.json

   → Muestra estado de cada gate
   → Si hay fallas: muestra recomendaciones
   → Return code: 0 (PASS), 1 (FAIL)

4. Generar reporte (opcional):
   $ python quality/scripts/generate_report.py quality/reports/quality_*.json

   → Genera: quality/reports/quality_report_YYYYMMDD_HHMMSS.md

5. Si hay issues bloqueantes:
   → Refactorizar código según recomendaciones
   → Volver al paso 2
```

### 6.6 Configuración de Quality Gates

**Archivo:** `<producto>/.claude/settings.json`

```json
{
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0
  }
}
```

---

## 7. Protocolo de Comunicación

### 7.1 Simuladores → Raspberry (Texto plano)

**Formato:**
```
<valor_float>\n
```

**Ejemplos:**
```
# Temperatura
23.5\n

# Batería (voltaje)
3.85\n

# Valores especiales
ERROR\n      # Simula falla del sensor
-999.0\n     # Sensor desconectado
```

### 7.2 Raspberry → UX Desktop (JSON)

**Formato:**
```json
{
  "timestamp": 1703001234,
  "temp_actual": 22.5,
  "temp_deseada": 24.0,
  "estado_climatizador": "calentando",
  "falla_sensor": false,
  "bateria_baja": false,
  "nivel_bateria": 75,
  "tiempo_en_estado": 120
}
```

### 7.3 UX Desktop → Raspberry (JSON)

**Comandos:**
```json
// Cambiar temperatura deseada
{
  "comando": "set_temp_deseada",
  "valor": 25.0,
  "timestamp": 1703001234
}

// Encender/Apagar
{
  "comando": "power",
  "estado": "on",
  "timestamp": 1703001234
}

// Cambiar modo display
{
  "comando": "set_modo_display",
  "modo": "deseada",
  "timestamp": 1703001234
}
```

---

## 8. Estilo Visual

### 8.1 Tema Oscuro

**Archivo:** `compartido/estilos/dark_theme.qss`

```css
/* Tema oscuro para simular dispositivo embebido */

QMainWindow {
    background-color: #1e293b;
}

QLabel {
    color: #e2e8f0;
    font-size: 14px;
}

QPushButton {
    background-color: #334155;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #475569;
}

QPushButton:pressed {
    background-color: #1e293b;
}

/* Botón subir - rojo */
QPushButton#btnSubir {
    background-color: #dc2626;
}

/* Botón bajar - azul */
QPushButton#btnBajar {
    background-color: #2563eb;
}

/* Display LCD */
QWidget#displayLCD {
    background-color: #065f46;
    border: 2px solid #047857;
    border-radius: 12px;
}

/* Slider */
QSlider::groove:horizontal {
    background: #334155;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #3b82f6;
    width: 20px;
    margin: -6px 0;
    border-radius: 10px;
}

/* Log viewer */
QTextEdit {
    background-color: #0f172a;
    color: #94a3b8;
    border: 1px solid #334155;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}
```

---

## 9. Testing

### 9.1 Estructura de Tests por Producto

```
<producto>/tests/
├── __init__.py
├── test_<modulo>.py          # Tests unitarios
├── test_socket.py            # Tests de comunicación
└── conftest.py               # Fixtures compartidos
```

### 9.2 Ejecutar Tests

```bash
# Tests de un producto
cd simulador_temperatura
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=app --cov-report=html

# Tests de todos los productos
cd ISSE_Simuladores
pytest simulador_temperatura/tests/ simulador_bateria/tests/ ux_termostato/tests/ -v
```

### 9.3 Configuración pytest

**Archivo:** `<producto>/pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## 10. Orden de Implementación

### Fase 1: Infraestructura Base

1. Crear estructura de carpetas del proyecto
2. Configurar `requirements.txt` global
3. Crear `config.json` compartido
4. Implementar `compartido/networking/base_socket_client.py`
5. Implementar `compartido/widgets/` (LED, ConfigPanel, LogViewer)
6. Crear `compartido/estilos/dark_theme.qss`

### Fase 2: Simulador de Temperatura

1. Crear estructura de `simulador_temperatura/`
2. Implementar `app/configuracion/` (Config + Configurador)
3. Implementar `app/general/generador_temperatura.py`
4. Implementar `app/datos/socket_client.py`
5. Implementar `app/servicios/ui_principal.py`
6. Crear tests en `tests/`
7. Configurar `quality/` y ejecutar análisis

### Fase 3: Simulador de Batería

1. Crear estructura de `simulador_bateria/`
2. Implementar lógica de carga/descarga
3. Implementar UI
4. Crear tests
5. Configurar quality

### Fase 4: UX Termostato

1. Crear estructura de `ux_termostato/`
2. Implementar widgets personalizados (DisplayLCD, ClimaIndicator, etc.)
3. Implementar socket server (recepción)
4. Implementar socket client (envío comandos)
5. Implementar UI principal
6. Crear tests
7. Configurar quality

### Fase 5: Integración y Refinamiento

1. Tests de integración entre productos
2. Validar comunicación con Raspberry Pi
3. Aplicar estilos finales
4. Documentación de usuario
5. Ejecutar quality en todos los productos

---

## 11. Checklist de Validación

### Pre-desarrollo
- [ ] Proyecto creado en PyCharm
- [ ] Virtual environment configurado
- [ ] Dependencias instaladas
- [ ] Git inicializado

### Por cada producto
- [ ] Estructura de carpetas creada
- [ ] Config + Configurador implementados
- [ ] Lógica de negocio implementada
- [ ] Socket client/server implementado
- [ ] UI PyQt6 funcional
- [ ] Tests unitarios pasando
- [ ] Quality gates pasando (Grado A o B)
- [ ] Documentación actualizada

### Integración
- [ ] Comunicación entre productos funciona
- [ ] Conexión con Raspberry Pi validada
- [ ] Tema visual aplicado
- [ ] Manual de usuario completo

---

## 12. Referencias

- **Repositorio ISSE_Termostato:** https://github.com/vvalotto/ISSE_Termostato
- **Documentación PyQt6:** https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Python Socket:** https://docs.python.org/3/library/socket.html
- **Radon (métricas):** https://radon.readthedocs.io/
- **Pylint:** https://pylint.pycqa.org/

---

---

## Apéndice A: Scripts de Quality (Plantillas)

Los siguientes scripts deben copiarse a cada producto en `<producto>/quality/scripts/`.

### A.1 calculate_metrics.py

```python
#!/usr/bin/env python3
"""
Calcula metricas esenciales de calidad de codigo para proyectos Python.
Genera salida JSON con datos de metricas.

Metricas medidas:
- LOC/SLOC: Lineas de codigo
- CC: Complejidad Ciclomatica
- MI: Indice de Mantenibilidad
- Pylint Score: Calidad general

Autor: Ambiente Agentico - ISSE_Simuladores
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime


class CalculadorMetricas:
    """Calcula metricas de calidad de codigo usando radon y pylint."""

    def __init__(self, ruta_objetivo="."):
        self.ruta_objetivo = Path(ruta_objetivo)
        self.metricas = {
            "timestamp": datetime.now().isoformat(),
            "objetivo": str(self.ruta_objetivo),
            "tamanio": {},
            "complejidad": {},
            "mantenibilidad": {},
            "pylint": {},
            "resumen": {}
        }

    def calcular_metricas_tamanio(self):
        """Calcula LOC, SLOC usando radon raw."""
        try:
            resultado = subprocess.run(
                ["radon", "raw", str(self.ruta_objetivo), "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )

            datos_raw = json.loads(resultado.stdout)

            total_loc = 0
            total_sloc = 0
            total_comentarios = 0
            total_blancos = 0

            for ruta_archivo, datos in datos_raw.items():
                total_loc += datos.get("loc", 0)
                total_sloc += datos.get("sloc", 0)
                total_comentarios += datos.get("comments", 0)
                total_blancos += datos.get("blank", 0)

            self.metricas["tamanio"] = {
                "loc": total_loc,
                "sloc": total_sloc,
                "comentarios": total_comentarios,
                "lineas_blanco": total_blancos,
                "ratio_comentarios": round(
                    total_comentarios / total_loc * 100, 2
                ) if total_loc > 0 else 0
            }

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error calculando metricas de tamanio: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parseando salida de radon: {e}", file=sys.stderr)
            return False

    def calcular_metricas_complejidad(self):
        """Calcula Complejidad Ciclomatica usando radon cc."""
        try:
            resultado = subprocess.run(
                ["radon", "cc", str(self.ruta_objetivo), "-a", "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )

            datos_cc = json.loads(resultado.stdout)

            todas_complejidades = []
            max_cc = 0
            funcion_max_cc = None

            distribucion = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

            for ruta_archivo, funciones in datos_cc.items():
                for func in funciones:
                    cc = func.get("complexity", 0)
                    todas_complejidades.append(cc)

                    if cc > max_cc:
                        max_cc = cc
                        funcion_max_cc = (
                            f"{ruta_archivo}:{func.get('lineno')} "
                            f"{func.get('name')}"
                        )

                    grado = func.get("rank", "F")
                    if grado in distribucion:
                        distribucion[grado] += 1

            promedio_cc = (
                sum(todas_complejidades) / len(todas_complejidades)
                if todas_complejidades else 0
            )

            self.metricas["complejidad"] = {
                "promedio": round(promedio_cc, 2),
                "maximo": max_cc,
                "ubicacion_maximo": funcion_max_cc,
                "total_funciones": len(todas_complejidades),
                "distribucion": distribucion
            }

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error calculando complejidad: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parseando salida de radon cc: {e}", file=sys.stderr)
            return False

    def calcular_indice_mantenibilidad(self):
        """Calcula Indice de Mantenibilidad usando radon mi."""
        try:
            resultado = subprocess.run(
                ["radon", "mi", str(self.ruta_objetivo), "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )

            datos_mi = json.loads(resultado.stdout)

            todos_mi = []
            min_mi = 100
            archivo_min_mi = None

            for ruta_archivo, datos in datos_mi.items():
                mi = datos.get("mi", 0)
                todos_mi.append(mi)

                if mi < min_mi:
                    min_mi = mi
                    archivo_min_mi = ruta_archivo

            promedio_mi = sum(todos_mi) / len(todos_mi) if todos_mi else 0
            bajo_umbral = sum(1 for mi in todos_mi if mi < 20)

            self.metricas["mantenibilidad"] = {
                "promedio": round(promedio_mi, 2),
                "minimo": round(min_mi, 2),
                "archivo_minimo": archivo_min_mi,
                "cantidad_bajo_umbral": bajo_umbral
            }

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error calculando MI: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parseando salida de radon mi: {e}", file=sys.stderr)
            return False

    def calcular_pylint_score(self):
        """Calcula score de Pylint."""
        try:
            resultado_json = subprocess.run(
                ["pylint", str(self.ruta_objetivo), "--output-format=json"],
                capture_output=True,
                text=True
            )

            mensajes = (
                json.loads(resultado_json.stdout)
                if resultado_json.stdout else []
            )

            resultado_score = subprocess.run(
                ["pylint", str(self.ruta_objetivo), "--score=yes"],
                capture_output=True,
                text=True
            )

            score = 0.0
            for linea in resultado_score.stdout.split('\n'):
                if 'rated at' in linea.lower():
                    match = re.search(r'(\d+\.\d+)/10', linea)
                    if match:
                        score = float(match.group(1))
                    break

            errores = sum(1 for msg in mensajes if msg.get("type") == "error")
            warnings = sum(1 for msg in mensajes if msg.get("type") == "warning")
            refactor = sum(1 for msg in mensajes if msg.get("type") == "refactor")
            convencion = sum(
                1 for msg in mensajes if msg.get("type") == "convention"
            )

            self.metricas["pylint"] = {
                "score": score,
                "errores": errores,
                "warnings": warnings,
                "refactor": refactor,
                "convencion": convencion,
                "total_mensajes": len(mensajes)
            }

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando pylint: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parseando salida de pylint: {e}", file=sys.stderr)
            return False

    def generar_resumen(self):
        """Genera resumen ejecutivo con estado pass/fail."""

        gates = {
            "max_complejidad": 10,
            "min_mantenibilidad": 20,
            "min_pylint_score": 8.0
        }

        settings_path = Path(".claude/settings.json")
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    qg = settings.get("quality_gates", {})
                    gates["max_complejidad"] = qg.get("max_complexity", 10)
                    gates["min_mantenibilidad"] = qg.get("min_maintainability", 20)
                    gates["min_pylint_score"] = qg.get("min_pylint_score", 8.0)
            except (json.JSONDecodeError, IOError):
                pass

        complejidad_ok = (
            self.metricas["complejidad"]["promedio"] <= gates["max_complejidad"]
        )
        mi_ok = (
            self.metricas["mantenibilidad"]["promedio"] > gates["min_mantenibilidad"]
        )
        pylint_ok = (
            self.metricas["pylint"]["score"] >= gates["min_pylint_score"]
        )

        pasados = sum([complejidad_ok, mi_ok, pylint_ok])

        if pasados == 3:
            grado = "A"
        elif pasados == 2:
            grado = "B"
        elif pasados == 1:
            grado = "C"
        else:
            grado = "F"

        self.metricas["resumen"] = {
            "grado": grado,
            "gates_pasados": pasados,
            "gates_totales": 3,
            "issues_bloqueantes": 3 - pasados,
            "quality_gates": {
                "complejidad": {
                    "estado": "PASS" if complejidad_ok else "FAIL",
                    "valor": self.metricas["complejidad"]["promedio"],
                    "umbral": gates["max_complejidad"]
                },
                "mantenibilidad": {
                    "estado": "PASS" if mi_ok else "FAIL",
                    "valor": self.metricas["mantenibilidad"]["promedio"],
                    "umbral": gates["min_mantenibilidad"]
                },
                "pylint": {
                    "estado": "PASS" if pylint_ok else "FAIL",
                    "valor": self.metricas["pylint"]["score"],
                    "umbral": gates["min_pylint_score"]
                }
            }
        }

    def ejecutar_todo(self):
        """Ejecuta todos los calculos de metricas."""
        exito = True

        print("Calculando metricas de calidad de codigo...")
        print(f"Objetivo: {self.ruta_objetivo}\n")

        print("1/4 Calculando metricas de tamanio...", end=" ")
        if self.calcular_metricas_tamanio():
            print("[OK]")
        else:
            print("[ERROR]")
            exito = False

        print("2/4 Calculando complejidad...", end=" ")
        if self.calcular_metricas_complejidad():
            print("[OK]")
        else:
            print("[ERROR]")
            exito = False

        print("3/4 Calculando indice de mantenibilidad...", end=" ")
        if self.calcular_indice_mantenibilidad():
            print("[OK]")
        else:
            print("[ERROR]")
            exito = False

        print("4/4 Ejecutando analisis pylint...", end=" ")
        if self.calcular_pylint_score():
            print("[OK]")
        else:
            print("[ERROR]")
            exito = False

        if exito:
            self.generar_resumen()
            print("\n[OK] Todas las metricas calculadas exitosamente!")
        else:
            print("\n[WARN] Algunas metricas fallaron al calcular")

        return exito

    def guardar_json(self, ruta_salida):
        """Guarda metricas como JSON."""
        Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(self.metricas, f, indent=2, ensure_ascii=False)
        print(f"\nMetricas guardadas en: {ruta_salida}")

    def imprimir_resumen(self):
        """Imprime resumen ejecutivo en consola."""
        resumen = self.metricas["resumen"]

        print("\n" + "="*60)
        print("RESUMEN DE METRICAS DE CALIDAD")
        print("="*60)

        print(f"\nGrado General: {resumen['grado']}")
        print(f"Quality Gates: {resumen['gates_pasados']}/{resumen['gates_totales']} pasaron")
        print(f"Issues Bloqueantes: {resumen['issues_bloqueantes']}")

        print("\nMetricas de Tamanio:")
        print(f"  - Total LOC: {self.metricas['tamanio']['loc']}")
        print(f"  - Source LOC: {self.metricas['tamanio']['sloc']}")
        print(f"  - Comentarios: {self.metricas['tamanio']['ratio_comentarios']}%")

        print("\nComplejidad:")
        print(f"  - CC Promedio: {self.metricas['complejidad']['promedio']}")
        print(f"  - CC Maximo: {self.metricas['complejidad']['maximo']} "
              f"({self.metricas['complejidad']['ubicacion_maximo']})")

        print("\nMantenibilidad:")
        print(f"  - MI Promedio: {self.metricas['mantenibilidad']['promedio']}")
        print(f"  - Modulos bajo umbral: "
              f"{self.metricas['mantenibilidad']['cantidad_bajo_umbral']}")

        print("\nPylint:")
        print(f"  - Score: {self.metricas['pylint']['score']}/10.0")
        print(f"  - Errores: {self.metricas['pylint']['errores']}")
        print(f"  - Warnings: {self.metricas['pylint']['warnings']}")

        print("\nEstado de Quality Gates:")
        for gate, datos in resumen["quality_gates"].items():
            estado_icono = "[PASS]" if datos["estado"] == "PASS" else "[FAIL]"
            print(f"  {estado_icono} {gate.title()}: {datos['valor']} "
                  f"(umbral: {datos['umbral']})")

        print("\n" + "="*60)


if __name__ == "__main__":
    objetivo = sys.argv[1] if len(sys.argv) > 1 else "."

    calculador = CalculadorMetricas(objetivo)

    if calculador.ejecutar_todo():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"quality/reports/quality_{timestamp}.json"
        calculador.guardar_json(archivo_salida)
        calculador.imprimir_resumen()

        bloqueantes = calculador.metricas["resumen"]["issues_bloqueantes"]
        sys.exit(0 if bloqueantes == 0 else 1)
    else:
        print("\n[ERROR] Fallo al calcular metricas")
        sys.exit(2)
```

### A.2 validate_gates.py

```python
#!/usr/bin/env python3
"""
Valida quality gates basado en metricas calculadas.
Retorna codigo de salida 0 si todos los gates pasan, 1 si alguno falla.

Autor: Ambiente Agentico - ISSE_Simuladores
"""

import json
import sys
from pathlib import Path


def cargar_metricas(archivo_metricas):
    """Carga metricas desde archivo JSON."""
    with open(archivo_metricas, 'r', encoding='utf-8') as f:
        return json.load(f)


def validar_gates(metricas):
    """Valida todos los quality gates."""

    resumen = metricas.get("resumen", {})
    gates = resumen.get("quality_gates", {})

    print("Validando Quality Gates...")
    print("="*60)

    todos_pasaron = True

    for nombre_gate, datos_gate in gates.items():
        estado = datos_gate["estado"]
        valor = datos_gate["valor"]
        umbral = datos_gate["umbral"]

        if estado == "PASS":
            print(f"[PASS] {nombre_gate.upper()}")
            print(f"       Valor: {valor}, Umbral: {umbral}")
        else:
            print(f"[FAIL] {nombre_gate.upper()}")
            print(f"       Valor: {valor}, Umbral: {umbral}")
            todos_pasaron = False

        print()

    print("="*60)

    if todos_pasaron:
        print("[OK] TODOS LOS QUALITY GATES PASARON!")
        return 0
    else:
        print("[FAIL] ALGUNOS QUALITY GATES FALLARON!")
        print("\nPor favor corrija los issues antes de hacer commit.")
        return 1


def mostrar_recomendaciones(metricas):
    """Muestra recomendaciones basadas en gates fallidos."""

    resumen = metricas.get("resumen", {})
    gates = resumen.get("quality_gates", {})

    gates_fallidos = [
        nombre for nombre, datos in gates.items()
        if datos["estado"] == "FAIL"
    ]

    if not gates_fallidos:
        return

    print("\nRecomendaciones:")
    print("-"*60)

    for gate in gates_fallidos:
        datos = gates[gate]

        if gate == "complejidad":
            print(f"\n[COMPLEJIDAD] CC promedio ({datos['valor']}) "
                  f"excede umbral ({datos['umbral']})")
            print("  Acciones sugeridas:")
            print(f"  1. Revisar funcion con mayor CC: "
                  f"{metricas['complejidad']['ubicacion_maximo']}")
            print("  2. Extraer condiciones complejas en funciones separadas")
            print("  3. Considerar aplicar patron Strategy para logica de branching")

        elif gate == "mantenibilidad":
            print(f"\n[MANTENIBILIDAD] MI promedio ({datos['valor']}) "
                  f"bajo umbral ({datos['umbral']})")
            print("  Acciones sugeridas:")
            print(f"  1. Revisar modulo: "
                  f"{metricas['mantenibilidad']['archivo_minimo']}")
            print("  2. Dividir modulos grandes en unidades mas pequenias")
            print("  3. Reducir dependencias entre modulos")
            print("  4. Mejorar documentacion y comentarios")

        elif gate == "pylint":
            print(f"\n[PYLINT] Score ({datos['valor']}) "
                  f"bajo umbral ({datos['umbral']})")
            print("  Acciones sugeridas:")
            print(f"  1. Corregir {metricas['pylint']['errores']} error(es)")
            print(f"  2. Atender {metricas['pylint']['warnings']} warning(s)")
            print("  3. Ejecutar: pylint --list-msgs para entender violaciones")
            print("  4. Ejecutar: autopep8 --in-place <archivo> para auto-corregir")

    print("\n" + "-"*60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python validate_gates.py <archivo_metricas.json>")
        print("\nEjemplo:")
        print("  python validate_gates.py quality/reports/quality_20251219_143022.json")
        sys.exit(2)

    archivo_metricas = sys.argv[1]

    if not Path(archivo_metricas).exists():
        print(f"Error: Archivo de metricas no encontrado: {archivo_metricas}")
        sys.exit(2)

    metricas = cargar_metricas(archivo_metricas)
    codigo_salida = validar_gates(metricas)

    if codigo_salida != 0:
        mostrar_recomendaciones(metricas)

    sys.exit(codigo_salida)
```

### A.3 generate_report.py

```python
#!/usr/bin/env python3
"""
Genera reporte Markdown legible a partir de metricas JSON.

Autor: Ambiente Agentico - ISSE_Simuladores
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def generar_reporte_markdown(metricas, nombre_producto="Producto"):
    """Genera reporte detallado en Markdown."""

    resumen = metricas.get("resumen", {})
    gates = resumen.get("quality_gates", {})

    total_funciones = metricas["complejidad"]["total_funciones"]
    distribucion = metricas["complejidad"]["distribucion"]

    def porcentaje(valor):
        return round(valor / total_funciones * 100, 1) if total_funciones > 0 else 0

    reporte = f"""# Reporte de Calidad de Codigo

**Proyecto:** ISSE_Simuladores - {nombre_producto}
**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Objetivo Analizado:** `{metricas['objetivo']}`
**Grado General:** {resumen['grado']}

---

## Resumen Ejecutivo

| Metrica | Valor |
|---------|-------|
| Quality Gates Pasados | {resumen['gates_pasados']}/{resumen['gates_totales']} |
| Issues Bloqueantes | {resumen['issues_bloqueantes']} |
| Grado General | {resumen['grado']} |

---

## Metricas de Tamanio

| Metrica | Valor |
|---------|-------|
| Total LOC | {metricas['tamanio']['loc']} |
| Source LOC | {metricas['tamanio']['sloc']} |
| Comentarios | {metricas['tamanio']['comentarios']} ({metricas['tamanio']['ratio_comentarios']}%) |
| Lineas en Blanco | {metricas['tamanio']['lineas_blanco']} |

---

## Analisis de Complejidad

| Metrica | Valor |
|---------|-------|
| CC Promedio | {metricas['complejidad']['promedio']} |
| CC Maximo | {metricas['complejidad']['maximo']} |
| Ubicacion Maximo | `{metricas['complejidad']['ubicacion_maximo']}` |
| Total Funciones | {total_funciones} |

### Distribucion por Grado

| Grado | Rango CC | Cantidad | Porcentaje |
|-------|----------|----------|------------|
| A | 1-5 | {distribucion['A']} | {porcentaje(distribucion['A'])}% |
| B | 6-10 | {distribucion['B']} | {porcentaje(distribucion['B'])}% |
| C | 11-20 | {distribucion['C']} | {porcentaje(distribucion['C'])}% |
| D | 21-30 | {distribucion['D']} | {porcentaje(distribucion['D'])}% |
| E | 31-40 | {distribucion['E']} | {porcentaje(distribucion['E'])}% |
| F | 41+ | {distribucion['F']} | {porcentaje(distribucion['F'])}% |

---

## Indice de Mantenibilidad

| Metrica | Valor |
|---------|-------|
| MI Promedio | {metricas['mantenibilidad']['promedio']} |
| MI Minimo | {metricas['mantenibilidad']['minimo']} |
| Archivo con MI Minimo | `{metricas['mantenibilidad']['archivo_minimo']}` |
| Modulos bajo umbral (< 20) | {metricas['mantenibilidad']['cantidad_bajo_umbral']} |

---

## Analisis Pylint

| Metrica | Valor |
|---------|-------|
| Score | {metricas['pylint']['score']}/10.0 |
| Errores | {metricas['pylint']['errores']} |
| Warnings | {metricas['pylint']['warnings']} |
| Sugerencias Refactor | {metricas['pylint']['refactor']} |
| Convenciones | {metricas['pylint']['convencion']} |
| Total Mensajes | {metricas['pylint']['total_mensajes']} |

---

## Estado de Quality Gates

| Gate | Estado | Valor | Umbral |
|------|--------|-------|--------|
"""

    for nombre_gate, datos_gate in gates.items():
        estado = datos_gate["estado"]
        valor = datos_gate["valor"]
        umbral = datos_gate["umbral"]
        icono = "[PASS]" if estado == "PASS" else "[FAIL]"
        reporte += f"| {nombre_gate.title()} | {icono} | {valor} | {umbral} |\n"

    reporte += """
---

## Recomendaciones

"""

    bloqueantes = resumen['issues_bloqueantes']

    if bloqueantes == 0:
        reporte += """[OK] **No hay issues bloqueantes.** El codigo cumple con todos los estandares de calidad.

**Sugerencias de mejora continua:**
- Mantener monitoreo de metricas en futuros commits
- Considerar aumentar cobertura de tests
- Documentar algoritmos complejos
"""
    else:
        reporte += f"""[ALERTA] **{bloqueantes} issue(s) bloqueante(s) detectado(s).**

Por favor corregir antes de hacer commit:

"""
        for nombre_gate, datos_gate in gates.items():
            if datos_gate["estado"] == "FAIL":
                if nombre_gate == "complejidad":
                    reporte += f"""### Complejidad Ciclomatica

**Problema:** CC promedio ({datos_gate['valor']}) excede umbral ({datos_gate['umbral']})

**Acciones:**
1. Refactorizar funcion: `{metricas['complejidad']['ubicacion_maximo']}`
2. Extraer condiciones complejas en funciones separadas
3. Aplicar patron Strategy para logica de branching

"""
                elif nombre_gate == "mantenibilidad":
                    reporte += f"""### Indice de Mantenibilidad

**Problema:** MI promedio ({datos_gate['valor']}) bajo umbral ({datos_gate['umbral']})

**Acciones:**
1. Revisar modulo: `{metricas['mantenibilidad']['archivo_minimo']}`
2. Dividir modulos grandes en unidades mas pequenias
3. Reducir dependencias entre modulos
4. Mejorar documentacion y comentarios

"""
                elif nombre_gate == "pylint":
                    reporte += f"""### Pylint Score

**Problema:** Score ({datos_gate['valor']}) bajo umbral ({datos_gate['umbral']})

**Acciones:**
1. Corregir {metricas['pylint']['errores']} error(es)
2. Atender {metricas['pylint']['warnings']} warning(s)
3. Ejecutar: `pylint <archivo> --list-msgs` para detalles
4. Ejecutar: `autopep8 --in-place <archivo>` para auto-corregir estilo

"""

    reporte += f"""---

## Metadata del Reporte

| Campo | Valor |
|-------|-------|
| Timestamp | {metricas['timestamp']} |
| Generado | {datetime.now().isoformat()} |
| Herramienta | quality-agent (ISSE_Simuladores) |

---

*Reporte generado automaticamente por el ambiente agentico de calidad.*
"""

    return reporte


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_report.py <metricas.json> [nombre_producto]")
        print("\nEjemplo:")
        print("  python generate_report.py quality/reports/quality_20251219.json")
        print("  python generate_report.py quality/reports/quality_20251219.json 'Simulador Temperatura'")
        sys.exit(1)

    archivo_metricas = sys.argv[1]
    nombre_producto = sys.argv[2] if len(sys.argv) > 2 else "Producto"

    if not Path(archivo_metricas).exists():
        print(f"Error: Archivo no encontrado: {archivo_metricas}")
        sys.exit(1)

    with open(archivo_metricas, 'r', encoding='utf-8') as f:
        metricas = json.load(f)

    reporte = generar_reporte_markdown(metricas, nombre_producto)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_reporte = f"quality/reports/quality_report_{timestamp}.md"

    Path(archivo_reporte).parent.mkdir(parents=True, exist_ok=True)

    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)

    print(f"Reporte generado: {archivo_reporte}")
    print("\n" + "="*60)
    print(reporte)
```

---

## Apéndice B: Archivos de Configuración Iniciales

### B.1 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# PyQt6
*.ui.bak
*.qrc.bak

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Quality reports (mantener estructura, ignorar contenido)
quality/reports/*.json
quality/reports/*.md
!quality/reports/.gitkeep

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Build
build/
dist/
*.egg-info/
```

### B.2 pytest.ini (por producto)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
qt_api = pyqt6
```

### B.3 .claude/settings.json (por producto)

```json
{
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0
  }
}
```

---

**FIN DEL DOCUMENTO DE DISEÑO**

Versión: 1.0
Fecha: Diciembre 2025
