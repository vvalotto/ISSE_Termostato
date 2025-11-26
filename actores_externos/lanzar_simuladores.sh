#!/bin/bash
# Script para lanzar los 4 simuladores en terminales separadas

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Lanzar simulador de batería
osascript -e "tell application \"Terminal\"
    do script \"cd '$PROJECT_DIR' && python3 simulador_bateria.py\"
    activate
end tell"

sleep 0.5

# Lanzar simulador de temperatura
osascript -e "tell application \"Terminal\"
    do script \"cd '$PROJECT_DIR' && python3 simulador_temperatura.py\"
end tell"

sleep 0.5

# Lanzar simulador de seteo temperatura
osascript -e "tell application \"Terminal\"
    do script \"cd '$PROJECT_DIR' && python3 simulador_seteo_temperatura_deseada.py\"
end tell"

sleep 0.5

# Lanzar simulador de selector temperatura
osascript -e "tell application \"Terminal\"
    do script \"cd '$PROJECT_DIR' && python3 simulador_selector_temperatura.py\"
end tell"

echo "✓ Simuladores lanzados en 4 terminales"
