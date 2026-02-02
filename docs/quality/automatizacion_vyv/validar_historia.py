#!/usr/bin/env python3
"""
Pipeline de Validación de Historias de Usuario (BDD)

Valida que la implementación cumple con los requisitos funcionales
especificados en las historias de usuario usando BDD (Behavior-Driven Development).

Estructura:
    Historia de Usuario → Escenarios BDD → Tests de Aceptación → Validación

Uso:
    python validar_historia.py                    # Validar todas las features
    python validar_historia.py control_temp       # Validar feature específica
    python validar_historia.py --branch actual    # Validar branch actual
    python validar_historia.py --resumen          # Solo mostrar resumen
"""

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime
import re


class Color:
    """Códigos ANSI para colores en terminal."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class PipelineValidacion:
    """Pipeline de validación de historias de usuario con BDD."""

    def __init__(self):
        self.inicio = datetime.now()
        self.features_path = Path('features')
        self.resultados = {
            'features': [],
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'scenarios_skipped': 0,
            'steps_passed': 0,
            'steps_failed': 0
        }

    def verificar_estructura_bdd(self):
        """Verifica que exista la estructura necesaria para BDD."""
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}🔍 Verificando Estructura BDD{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        errores = []

        # Verificar directorio features
        if not self.features_path.exists():
            errores.append("❌ Directorio 'features/' no existe")
            print(f"{Color.FAIL}❌ Directorio 'features/' no encontrado{Color.ENDC}")
            print(f"{Color.WARNING}   Creando estructura básica...{Color.ENDC}\n")
            self.crear_estructura_bdd()
            return True

        # Verificar archivos .feature
        feature_files = list(self.features_path.glob('*.feature'))
        if not feature_files:
            errores.append("⚠️  No hay archivos .feature en features/")
            print(f"{Color.WARNING}⚠️  No se encontraron archivos .feature{Color.ENDC}")
            print(f"   Ubicación: {self.features_path.absolute()}\n")
            print(f"{Color.OKCYAN}💡 Ejemplo de archivo .feature:{Color.ENDC}")
            self.mostrar_ejemplo_feature()
            return False

        # Verificar directorio steps
        steps_dir = self.features_path / 'steps'
        if not steps_dir.exists():
            errores.append("⚠️  Directorio 'features/steps/' no existe")
            print(f"{Color.WARNING}⚠️  Directorio 'features/steps/' no encontrado{Color.ENDC}")
            print(f"   Creando...{Color.ENDC}\n")
            steps_dir.mkdir(parents=True, exist_ok=True)
            (steps_dir / '__init__.py').touch()

        if errores:
            print(f"{Color.WARNING}Estructura BDD necesita ajustes:{Color.ENDC}")
            for error in errores:
                print(f"  {error}")
            print()
            return False

        print(f"{Color.OKGREEN}✅ Estructura BDD correcta{Color.ENDC}")
        print(f"   • {len(feature_files)} archivo(s) .feature encontrado(s)")
        print(f"   • Directorio steps/ presente\n")
        return True

    def crear_estructura_bdd(self):
        """Crea la estructura básica de directorios para BDD."""
        # Crear directorios
        self.features_path.mkdir(exist_ok=True)
        steps_dir = self.features_path / 'steps'
        steps_dir.mkdir(exist_ok=True)

        # Crear __init__.py en steps
        (steps_dir / '__init__.py').touch()

        # Crear feature de ejemplo
        feature_ejemplo = self.features_path / 'ejemplo.feature'
        feature_ejemplo.write_text("""# Ejemplo de Feature con BDD

Feature: Control de Temperatura (EJEMPLO)
  Como usuario del termostato
  Quiero controlar la temperatura del ambiente
  Para mantenerlo confortable

  Scenario: Temperatura más baja que la deseada
    Given un ambiente con temperatura de 18°C
    And la temperatura deseada es 22°C
    When consulto el estado del climatizador
    Then el climatizador debe estar en modo "calentando"
""")

        # Crear step de ejemplo
        step_ejemplo = steps_dir / 'ejemplo_steps.py'
        step_ejemplo.write_text("""# Implementación de steps de ejemplo
from behave import given, when, then

@given('un ambiente con temperatura de {temp}°C')
def step_ambiente_temperatura(context, temp):
    context.temp_ambiente = float(temp)

@given('la temperatura deseada es {temp}°C')
def step_temperatura_deseada(context, temp):
    context.temp_deseada = float(temp)

@when('consulto el estado del climatizador')
def step_consultar_estado(context):
    # Lógica para determinar estado
    if context.temp_ambiente < context.temp_deseada:
        context.estado = "calentando"
    else:
        context.estado = "apagado"

@then('el climatizador debe estar en modo "{modo}"')
def step_verificar_modo(context, modo):
    assert context.estado == modo, \\
        f"Esperaba {modo}, obtuve {context.estado}"
""")

        print(f"{Color.OKGREEN}✅ Estructura BDD creada:{Color.ENDC}")
        print(f"   • features/ejemplo.feature")
        print(f"   • features/steps/ejemplo_steps.py")
        print(f"\n{Color.OKCYAN}💡 Personaliza estos archivos con tus historias de usuario{Color.ENDC}\n")

    def mostrar_ejemplo_feature(self):
        """Muestra un ejemplo de archivo .feature."""
        print("""
# features/control_temperatura.feature

Feature: Control de Temperatura del Ambiente
  Como usuario del termostato
  Quiero que el sistema controle automáticamente la temperatura
  Para mantener el ambiente confortable

  Scenario: Encender climatizador cuando hace frío
    Given un ambiente con temperatura de 18°C
    And la temperatura deseada es 22°C
    When verifico el estado del climatizador
    Then debe estar encendido en modo "calentando"

  Scenario: Apagar cuando se alcanza temperatura
    Given un ambiente con temperatura de 22°C
    And la temperatura deseada es 22°C
    When verifico el estado del climatizador
    Then debe estar "apagado"
        """)

    def ejecutar_behave(self, feature=None):
        """Ejecuta behave para validar features."""
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}🧪 Ejecutando Tests de Aceptación BDD{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        # Verificar que behave esté instalado
        try:
            subprocess.run(['behave', '--version'],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Color.FAIL}❌ behave no está instalado{Color.ENDC}")
            print(f"\n{Color.OKCYAN}Instalar con:{Color.ENDC}")
            print(f"  pip install behave\n")
            return False

        # Construir comando
        comando = ['behave']

        if feature:
            # Ejecutar feature específica
            feature_path = self.features_path / f"{feature}.feature"
            if not feature_path.exists():
                print(f"{Color.FAIL}❌ Feature no encontrada: {feature_path}{Color.ENDC}\n")
                return False
            comando.append(str(feature_path))

        comando.extend([
            '--no-capture',  # Mostrar prints
            '--no-capture-stderr',
            '--format', 'pretty',
            '--tags', '~@skip'  # Ignorar scenarios con @skip
        ])

        # Ejecutar
        resultado = subprocess.run(
            comando,
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )

        return resultado.returncode == 0

    def obtener_branch_actual(self):
        """Obtiene el nombre del branch actual."""
        try:
            resultado = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            return resultado.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def obtener_historia_desde_branch(self):
        """
        Extrae el nombre de la historia desde el nombre del branch.
        Convención: feature/nombre-historia o historia/nombre-historia
        """
        branch = self.obtener_branch_actual()
        if not branch:
            return None

        # Extraer nombre de historia del branch
        # Ejemplo: feature/control-temperatura -> control_temperatura
        if '/' in branch:
            _, historia = branch.split('/', 1)
            # Reemplazar guiones por guiones bajos
            historia = historia.replace('-', '_')
            return historia

        return None

    def listar_features_disponibles(self):
        """Lista todas las features disponibles."""
        print(f"\n{Color.OKCYAN}📋 Features Disponibles:{Color.ENDC}\n")

        if not self.features_path.exists():
            print(f"{Color.WARNING}   No hay features definidas todavía{Color.ENDC}\n")
            return

        features = list(self.features_path.glob('*.feature'))

        if not features:
            print(f"{Color.WARNING}   No hay archivos .feature en features/{Color.ENDC}\n")
            return

        for i, feature_file in enumerate(features, 1):
            # Leer primera línea (Feature: ...)
            with open(feature_file) as f:
                primera_linea = f.readline().strip()
                if primera_linea.startswith('#'):
                    primera_linea = f.readline().strip()

            print(f"   {i}. {feature_file.stem}")
            if 'Feature:' in primera_linea:
                titulo = primera_linea.split('Feature:', 1)[1].strip()
                print(f"      {Color.HEADER}{titulo}{Color.ENDC}")
            print()

    def mostrar_resumen_bdd(self):
        """Muestra un resumen del estado de BDD en el proyecto."""
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}📊 Resumen BDD del Proyecto{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        if not self.features_path.exists():
            print(f"{Color.WARNING}⚠️  No hay estructura BDD configurada{Color.ENDC}")
            print(f"\n{Color.OKCYAN}Para empezar:{Color.ENDC}")
            print(f"  1. Ejecuta: python validar_historia.py")
            print(f"  2. Se creará estructura automáticamente")
            print(f"  3. Personaliza los ejemplos con tus historias\n")
            return

        features = list(self.features_path.glob('*.feature'))
        steps = list((self.features_path / 'steps').glob('*_steps.py')) if (self.features_path / 'steps').exists() else []

        print(f"📁 Estructura:")
        print(f"   • Features: {len(features)}")
        print(f"   • Steps implementados: {len(steps)}")

        if features:
            print(f"\n📝 Features:")
            for feature in features:
                print(f"   • {feature.name}")

        if steps:
            print(f"\n🔧 Steps:")
            for step in steps:
                print(f"   • {step.name}")

        print(f"\n{Color.OKCYAN}💡 Comandos útiles:{Color.ENDC}")
        print(f"   • Validar todo: python validar_historia.py")
        print(f"   • Validar feature: python validar_historia.py nombre_feature")
        print(f"   • Ver este resumen: python validar_historia.py --resumen\n")

    def validar_branch_actual(self):
        """Valida la historia asociada al branch actual."""
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}🌿 Validación de Branch Actual{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        branch = self.obtener_branch_actual()
        if not branch:
            print(f"{Color.FAIL}❌ No se pudo determinar el branch actual{Color.ENDC}\n")
            return False

        print(f"{Color.OKCYAN}Branch actual: {branch}{Color.ENDC}\n")

        historia = self.obtener_historia_desde_branch()
        if not historia:
            print(f"{Color.WARNING}⚠️  No se pudo extraer nombre de historia del branch{Color.ENDC}")
            print(f"   Convención esperada: feature/nombre-historia\n")
            return False

        print(f"Historia detectada: {Color.BOLD}{historia}{Color.ENDC}\n")

        # Buscar feature correspondiente
        feature_path = self.features_path / f"{historia}.feature"

        if not feature_path.exists():
            print(f"{Color.FAIL}❌ Feature no encontrada: {historia}.feature{Color.ENDC}")
            print(f"\n{Color.OKCYAN}💡 Debes crear:{Color.ENDC}")
            print(f"   features/{historia}.feature\n")
            return False

        # Validar feature
        return self.ejecutar_behave(historia)

    def ejecutar_pipeline_completo(self):
        """Ejecuta el pipeline completo de validación."""
        print(f"\n{Color.BOLD}{Color.HEADER}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                                                                   ║")
        print("║          🎯 PIPELINE DE VALIDACIÓN (BDD)                         ║")
        print("║              Historias de Usuario                                ║")
        print("║                                                                   ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Color.ENDC}\n")

        # 1. Verificar estructura
        if not self.verificar_estructura_bdd():
            print(f"{Color.WARNING}⚠️  Estructura BDD no está lista{Color.ENDC}")
            print(f"   Configura tus features y vuelve a ejecutar\n")
            sys.exit(1)

        # 2. Listar features
        self.listar_features_disponibles()

        # 3. Ejecutar behave
        exito = self.ejecutar_behave()

        # 4. Resumen
        duracion = (datetime.now() - self.inicio).total_seconds()

        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}📋 RESULTADO DE VALIDACIÓN{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        if exito:
            print(f"{Color.OKGREEN}✅ VALIDACIÓN EXITOSA{Color.ENDC}")
            print(f"   Todos los escenarios pasaron")
            print(f"   La historia de usuario está implementada correctamente")
        else:
            print(f"{Color.FAIL}❌ VALIDACIÓN FALLÓ{Color.ENDC}")
            print(f"   Algunos escenarios no pasaron")
            print(f"   La implementación NO cumple con los requisitos")

        print(f"\n⏱️  Duración: {duracion:.2f}s\n")

        return exito


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Pipeline de validación de historias de usuario (BDD)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python validar_historia.py                    # Validar todas las features
  python validar_historia.py control_temp       # Validar feature específica
  python validar_historia.py --branch           # Validar branch actual
  python validar_historia.py --resumen          # Ver resumen del proyecto
  python validar_historia.py --listar           # Listar features disponibles

Convención de branches:
  feature/control-temperatura  →  Busca features/control_temperatura.feature
  historia/gestion-bateria     →  Busca features/gestion_bateria.feature
        """
    )

    parser.add_argument(
        'feature',
        nargs='?',
        help='Nombre de la feature a validar (sin extensión .feature)'
    )

    parser.add_argument(
        '--branch',
        action='store_true',
        help='Validar historia asociada al branch actual'
    )

    parser.add_argument(
        '--resumen',
        action='store_true',
        help='Mostrar resumen del estado BDD del proyecto'
    )

    parser.add_argument(
        '--listar',
        action='store_true',
        help='Listar features disponibles'
    )

    args = parser.parse_args()

    pipeline = PipelineValidacion()

    # Modos de ejecución
    if args.resumen:
        pipeline.mostrar_resumen_bdd()
        sys.exit(0)

    if args.listar:
        pipeline.listar_features_disponibles()
        sys.exit(0)

    if args.branch:
        exito = pipeline.validar_branch_actual()
        sys.exit(0 if exito else 1)

    if args.feature:
        # Validar feature específica
        if pipeline.verificar_estructura_bdd():
            exito = pipeline.ejecutar_behave(args.feature)
            sys.exit(0 if exito else 1)
        else:
            sys.exit(1)

    # Por defecto: pipeline completo
    exito = pipeline.ejecutar_pipeline_completo()
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
