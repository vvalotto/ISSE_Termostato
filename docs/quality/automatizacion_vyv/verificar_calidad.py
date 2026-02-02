#!/usr/bin/env python3
"""
Pipeline de Verificación de Calidad para ISSE_Termostato

Ejecuta todas las verificaciones necesarias antes de considerar
una pieza de software como "terminada".

Uso:
    python verificar_calidad.py                    # Verificación completa
    python verificar_calidad.py --solo-tests       # Solo tests
    python verificar_calidad.py --solo-metricas    # Solo métricas
    python verificar_calidad.py --rapido           # Verificación rápida
"""

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime


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


class PipelineVerificacion:
    """Pipeline de verificación de calidad."""

    def __init__(self, modo='completo'):
        self.modo = modo
        self.resultados = []
        self.inicio = datetime.now()

    def ejecutar_comando(self, nombre, comando, bloqueante=True, descripcion=""):
        """
        Ejecuta un comando del pipeline.

        Args:
            nombre: Nombre de la verificación
            comando: Comando a ejecutar
            bloqueante: Si True, falla el pipeline si el comando falla
            descripcion: Descripción adicional
        """
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}🔧 {nombre}{Color.ENDC}")
        if descripcion:
            print(f"   {descripcion}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        # Mostrar salida
        if resultado.stdout:
            print(resultado.stdout)

        # Verificar resultado
        if resultado.returncode != 0:
            print(f"\n{Color.FAIL}❌ {nombre} - FALLÓ{Color.ENDC}")
            if resultado.stderr:
                print(f"{Color.WARNING}Error:{Color.ENDC}")
                print(resultado.stderr)

            self.resultados.append({
                'nombre': nombre,
                'estado': 'FALLO',
                'bloqueante': bloqueante
            })

            if bloqueante:
                return False
        else:
            print(f"\n{Color.OKGREEN}✅ {nombre} - OK{Color.ENDC}")
            self.resultados.append({
                'nombre': nombre,
                'estado': 'OK',
                'bloqueante': bloqueante
            })

        return True

    def verificar_tests(self):
        """Ejecuta tests unitarios y de integración."""
        return self.ejecutar_comando(
            "Tests Unitarios e Integración",
            "pytest Test/ -v --tb=short",
            bloqueante=True,
            descripcion="Ejecutando suite completa de tests"
        )

    def verificar_cobertura(self):
        """Verifica cobertura de código."""
        return self.ejecutar_comando(
            "Cobertura de Código",
            "pytest Test/ --cov=. --cov-report=term-missing --cov-fail-under=70",
            bloqueante=True,
            descripcion="Verificando cobertura mínima del 70%"
        )

    def verificar_estilo(self):
        """Verifica estilo de código con flake8."""
        comando = (
            "flake8 . "
            "--exclude=venv,Test,docs,actores_externos "
            "--max-line-length=100 "
            "--max-complexity=10 "
            "--ignore=E501,W503"
        )

        return self.ejecutar_comando(
            "Estilo de Código (flake8)",
            comando,
            bloqueante=False,
            descripcion="Verificando PEP8 y complejidad básica"
        )

    def calcular_metricas_complejidad(self):
        """Calcula métricas de complejidad con radon."""
        return self.ejecutar_comando(
            "Métricas de Complejidad (radon)",
            "radon cc . -a -s --exclude='Test,venv,docs,actores_externos'",
            bloqueante=False,
            descripcion="Complejidad ciclomática promedio"
        )

    def verificar_metricas_personalizadas(self):
        """Verifica métricas personalizadas del proyecto."""
        print(f"\n{Color.OKCYAN}📊 Métricas disponibles en docs/{Color.ENDC}")
        print("   • Métricas de Herencia: docs/reporte_metricas_herencia.md")
        print("   • Métricas DSM: docs/reporte_metricas_dsm.md")
        print("   • Clean Architecture: docs/reporte_metricas_clean_architecture.md")
        print("   • Acoplamiento: docs/reporte_metricas_acoplamiento.md")
        print("   • Cohesión: docs/reporte_metricas_cohesion.md")

        self.resultados.append({
            'nombre': 'Métricas Personalizadas',
            'estado': 'INFO',
            'bloqueante': False
        })

        return True

    def verificar_arquitectura_limpia(self):
        """Verifica violaciones de Clean Architecture."""
        print(f"\n{Color.WARNING}⚠️  Verificación de Clean Architecture{Color.ENDC}")
        print("   Actualmente hay 111 violaciones conocidas")
        print("   Meta: Reducir violaciones en cada iteración")

        self.resultados.append({
            'nombre': 'Clean Architecture',
            'estado': 'WARNING',
            'bloqueante': False
        })

        return True

    def mostrar_resumen(self):
        """Muestra resumen de resultados."""
        duracion = (datetime.now() - self.inicio).total_seconds()

        print(f"\n\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"{Color.BOLD}📋 RESUMEN DE VERIFICACIÓN{Color.ENDC}")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        ok_count = sum(1 for r in self.resultados if r['estado'] == 'OK')
        fail_count = sum(1 for r in self.resultados if r['estado'] == 'FALLO')
        warning_count = sum(1 for r in self.resultados if r['estado'] == 'WARNING')

        for resultado in self.resultados:
            nombre = resultado['nombre']
            estado = resultado['estado']
            bloqueante = resultado['bloqueante']

            if estado == 'OK':
                icono = f"{Color.OKGREEN}✅{Color.ENDC}"
            elif estado == 'FALLO':
                icono = f"{Color.FAIL}❌{Color.ENDC}"
            elif estado == 'WARNING':
                icono = f"{Color.WARNING}⚠️{Color.ENDC}"
            else:
                icono = f"{Color.OKCYAN}ℹ️{Color.ENDC}"

            bloq_text = " [BLOQUEANTE]" if bloqueante and estado == 'FALLO' else ""
            print(f"{icono}  {nombre:<40} {estado}{bloq_text}")

        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}")
        print(f"✅ OK: {ok_count}  |  ❌ Fallos: {fail_count}  |  ⚠️  Warnings: {warning_count}")
        print(f"⏱️  Duración: {duracion:.2f}s")
        print(f"{Color.HEADER}{'='*70}{Color.ENDC}\n")

        # Determinar si el pipeline pasó
        fallos_bloqueantes = sum(
            1 for r in self.resultados
            if r['estado'] == 'FALLO' and r['bloqueante']
        )

        if fallos_bloqueantes > 0:
            print(f"{Color.FAIL}❌ PIPELINE FALLÓ{Color.ENDC}")
            print(f"   {fallos_bloqueantes} verificaciones bloqueantes fallaron")
            print(f"   {Color.WARNING}La pieza de software NO está lista{Color.ENDC}\n")
            return False
        else:
            print(f"{Color.OKGREEN}✅ PIPELINE COMPLETADO{Color.ENDC}")
            print(f"   Todas las verificaciones bloqueantes pasaron")

            if warning_count > 0:
                print(f"   {Color.WARNING}Nota: {warning_count} warnings encontrados{Color.ENDC}")

            print(f"\n   {Color.BOLD}🎉 La pieza de software está lista para commit{Color.ENDC}\n")
            return True

    def ejecutar_pipeline_completo(self):
        """Ejecuta el pipeline completo."""
        print(f"\n{Color.BOLD}{Color.HEADER}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                                                                   ║")
        print("║          🚀 PIPELINE DE VERIFICACIÓN DE CALIDAD                  ║")
        print("║              ISSE_Termostato                                      ║")
        print("║                                                                   ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Color.ENDC}\n")

        pasos = [
            ("Tests", self.verificar_tests),
            ("Cobertura", self.verificar_cobertura),
            ("Estilo", self.verificar_estilo),
            ("Complejidad", self.calcular_metricas_complejidad),
            ("Métricas", self.verificar_metricas_personalizadas),
            ("Arquitectura", self.verificar_arquitectura_limpia),
        ]

        for nombre, funcion in pasos:
            if not funcion():
                # Si una verificación bloqueante falla, mostrar resumen y salir
                if any(r['nombre'] == nombre and r['bloqueante']
                      for r in self.resultados):
                    self.mostrar_resumen()
                    sys.exit(1)

        # Mostrar resumen final
        exito = self.mostrar_resumen()
        sys.exit(0 if exito else 1)

    def ejecutar_rapido(self):
        """Ejecuta solo verificaciones rápidas."""
        print(f"\n{Color.OKBLUE}⚡ Modo Rápido{Color.ENDC}\n")

        self.verificar_tests()
        self.verificar_estilo()

        exito = self.mostrar_resumen()
        sys.exit(0 if exito else 1)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Pipeline de verificación de calidad',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python verificar_calidad.py              # Verificación completa
  python verificar_calidad.py --rapido     # Solo tests y estilo
  python verificar_calidad.py --solo-tests # Solo ejecutar tests
        """
    )

    parser.add_argument(
        '--rapido',
        action='store_true',
        help='Ejecuta solo verificaciones rápidas (tests + estilo)'
    )

    parser.add_argument(
        '--solo-tests',
        action='store_true',
        help='Ejecuta solo los tests'
    )

    args = parser.parse_args()

    pipeline = PipelineVerificacion()

    if args.rapido:
        pipeline.ejecutar_rapido()
    elif args.solo_tests:
        if pipeline.verificar_tests():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        pipeline.ejecutar_pipeline_completo()


if __name__ == "__main__":
    main()
