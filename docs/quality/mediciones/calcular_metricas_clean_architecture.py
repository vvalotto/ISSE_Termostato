"""
Script para calcular métricas de Clean Architecture del proyecto ISSE_Termostato.

Métricas calculadas basadas en los principios de Robert C. Martin:
- Abstractness (A): Nivel de abstracción por paquete
- Instability (I): Inestabilidad por paquete
- Distance from Main Sequence (D): Distancia a la secuencia principal
- Zone Analysis: Análisis de zonas (Zone of Pain, Zone of Uselessness)
- Dependency Direction: Dirección de dependencias (hacia dentro)
- Layer Violations: Violaciones de capas arquitectónicas
- Acyclic Dependencies Principle (ADP): Detección de ciclos
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import math


class CleanArchitectureAnalyzer(ast.NodeVisitor):
    """Analizador de Clean Architecture usando AST."""

    def __init__(self):
        self.current_module = ""
        self.current_package = ""
        self.dependencies = defaultdict(set)  # módulo -> {módulos que importa}
        self.abstractions = defaultdict(int)  # paquete -> número de clases abstractas
        self.concretes = defaultdict(int)  # paquete -> número de clases concretas
        self.is_abstract = False

    def visit_ClassDef(self, node):
        """Detecta si una clase es abstracta."""
        # Clase abstracta si hereda de ABCMeta o tiene @abstractmethod
        is_abstract = False

        # Verificar si usa metaclass=ABCMeta
        for keyword in node.keywords:
            if keyword.arg == 'metaclass':
                if isinstance(keyword.value, ast.Name) and keyword.value.id == 'ABCMeta':
                    is_abstract = True

        # Verificar si tiene métodos abstractos
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod':
                        is_abstract = True
                    elif isinstance(decorator, ast.Attribute) and decorator.attr == 'abstractmethod':
                        is_abstract = True

        if is_abstract:
            self.abstractions[self.current_package] += 1
        else:
            self.concretes[self.current_package] += 1

        self.generic_visit(node)

    def visit_Import(self, node):
        """Registra imports."""
        for alias in node.names:
            module_name = alias.name
            self.dependencies[self.current_module].add(module_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Registra from...import."""
        if node.module:
            self.dependencies[self.current_module].add(node.module)
        self.generic_visit(node)


def classify_layer(module_path: str) -> str:
    """
    Clasifica un módulo en una capa de Clean Architecture.

    Capas (de dentro hacia fuera):
    1. Entities (entidades)
    2. Use Cases (servicios_dominio, gestores_entidades)
    3. Interface Adapters (agentes_*, servicios_aplicacion)
    4. Frameworks & Drivers (configurador, actores_externos)
    """
    parts = module_path.split(os.sep)
    if not parts:
        return "Unknown"

    package = parts[0]

    layer_mapping = {
        'entidades': 'Layer 1: Entities',
        'servicios_dominio': 'Layer 2: Use Cases',
        'gestores_entidades': 'Layer 2: Use Cases',
        'servicios_aplicacion': 'Layer 3: Interface Adapters',
        'agentes_sensores': 'Layer 3: Interface Adapters',
        'agentes_actuadores': 'Layer 3: Interface Adapters',
        'registrador': 'Layer 3: Interface Adapters',
        'configurador': 'Layer 4: Frameworks & Drivers',
        'actores_externos': 'Layer 4: Frameworks & Drivers',
    }

    return layer_mapping.get(package, 'Unknown')


def get_layer_number(layer_name: str) -> int:
    """Extrae el número de capa."""
    if 'Layer 1' in layer_name:
        return 1
    elif 'Layer 2' in layer_name:
        return 2
    elif 'Layer 3' in layer_name:
        return 3
    elif 'Layer 4' in layer_name:
        return 4
    return 0


def analyze_project(root_path: str) -> Tuple[CleanArchitectureAnalyzer, Dict[str, str]]:
    """Analiza el proyecto."""
    analyzer = CleanArchitectureAnalyzer()
    module_to_path = {}

    exclude_dirs = {'Test', 'tests', '__pycache__', '.git', 'venv', 'env', 'build', 'dist'}

    for py_file in Path(root_path).rglob('*.py'):
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue
        if py_file.name.startswith('setup') or py_file.name == 'ejecutar.py':
            continue
        if 'docs' in py_file.parts:
            continue

        try:
            rel_path = py_file.relative_to(root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            package = str(rel_path.parts[0]) if len(rel_path.parts) > 0 else 'root'

            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(py_file))
                analyzer.current_module = module_name
                analyzer.current_package = package
                module_to_path[module_name] = str(rel_path)
                analyzer.visit(tree)
        except Exception as e:
            print(f"Error procesando {py_file}: {e}")

    return analyzer, module_to_path


def calculate_abstractness(analyzer: CleanArchitectureAnalyzer, package: str) -> float:
    """
    Calcula Abstractness (A) de un paquete.
    A = Na / Nc
    Donde:
    - Na = número de clases/interfaces abstractas
    - Nc = número total de clases

    Rango: [0, 1]
    - 0 = completamente concreto
    - 1 = completamente abstracto
    """
    na = analyzer.abstractions.get(package, 0)
    nc = na + analyzer.concretes.get(package, 0)

    if nc == 0:
        return 0.0

    return na / nc


def calculate_instability(package: str, analyzer: CleanArchitectureAnalyzer,
                         module_to_path: Dict[str, str]) -> Tuple[float, int, int]:
    """
    Calcula Instability (I) de un paquete.
    I = Ce / (Ca + Ce)
    Donde:
    - Ce = Efferent Coupling (dependencias salientes)
    - Ca = Afferent Coupling (dependencias entrantes)

    Rango: [0, 1]
    - 0 = máxima estabilidad (solo dependencias entrantes)
    - 1 = máxima inestabilidad (solo dependencias salientes)
    """
    # Módulos del paquete
    package_modules = [m for m, p in module_to_path.items()
                      if p.split(os.sep)[0] == package]

    # Ce: Dependencias salientes (módulos externos que este paquete importa)
    ce_set = set()
    for module in package_modules:
        for dep in analyzer.dependencies.get(module, set()):
            # Extraer paquete de la dependencia
            dep_package = dep.split('.')[0]
            if dep_package != package and dep_package in [p.split(os.sep)[0]
                                                          for p in module_to_path.values()]:
                ce_set.add(dep_package)

    ce = len(ce_set)

    # Ca: Dependencias entrantes (otros paquetes que dependen de este)
    ca_set = set()
    for module, deps in analyzer.dependencies.items():
        module_package = module_to_path.get(module, '').split(os.sep)[0]
        if module_package != package:
            for dep in deps:
                dep_package = dep.split('.')[0]
                if dep_package == package:
                    ca_set.add(module_package)

    ca = len(ca_set)

    if ca + ce == 0:
        return 0.0, ca, ce

    return ce / (ca + ce), ca, ce


def calculate_distance(abstractness: float, instability: float) -> float:
    """
    Calcula Distance from Main Sequence (D).
    D = |A + I - 1|

    La "Main Sequence" es la línea ideal donde A + I = 1

    Rango: [0, 1]
    - 0 = en la secuencia principal (ideal)
    - 1 = máxima distancia (problemático)

    Zonas:
    - Zone of Pain: I ≈ 0, A ≈ 0 (concreto y estable, difícil de cambiar)
    - Zone of Uselessness: I ≈ 1, A ≈ 1 (abstracto e inestable, innecesario)
    - Main Sequence: A + I ≈ 1 (balance ideal)
    """
    return abs(abstractness + instability - 1)


def classify_zone(abstractness: float, instability: float, distance: float) -> str:
    """Clasifica un paquete en una zona arquitectónica."""
    if distance <= 0.2:
        return "Main Sequence (Ideal)"
    elif abstractness < 0.3 and instability < 0.3:
        return "Zone of Pain (Rigid)"
    elif abstractness > 0.7 and instability > 0.7:
        return "Zone of Uselessness (Abstract)"
    else:
        return "Suboptimal (Needs adjustment)"


def detect_layer_violations(analyzer: CleanArchitectureAnalyzer,
                            module_to_path: Dict[str, str]) -> List[Dict]:
    """
    Detecta violaciones de la Regla de Dependencia de Clean Architecture.

    Regla: Las dependencias deben apuntar hacia adentro (capas internas).
    - Capa 4 puede depender de 3, 2, 1
    - Capa 3 puede depender de 2, 1
    - Capa 2 puede depender de 1
    - Capa 1 NO debe depender de nadie (entidades puras)
    """
    violations = []

    for module, deps in analyzer.dependencies.items():
        if module not in module_to_path:
            continue

        src_path = module_to_path[module]
        src_layer = classify_layer(src_path)
        src_layer_num = get_layer_number(src_layer)

        for dep in deps:
            # Encontrar módulo de destino
            matching_modules = [m for m in module_to_path.keys()
                               if m.startswith(dep) or dep.startswith(m.split('.')[0])]

            for target_module in matching_modules:
                if target_module == module:
                    continue

                dst_path = module_to_path[target_module]
                dst_layer = classify_layer(dst_path)
                dst_layer_num = get_layer_number(dst_layer)

                # Violación: depende de una capa más externa
                if src_layer_num < dst_layer_num and src_layer_num > 0 and dst_layer_num > 0:
                    violations.append({
                        'source': module,
                        'source_layer': src_layer,
                        'target': target_module,
                        'target_layer': dst_layer,
                        'severity': dst_layer_num - src_layer_num
                    })

    return violations


def detect_package_cycles(analyzer: CleanArchitectureAnalyzer,
                         module_to_path: Dict[str, str]) -> List[List[str]]:
    """Detecta ciclos entre paquetes (Acyclic Dependencies Principle)."""
    # Construir grafo de dependencias entre paquetes
    package_deps = defaultdict(set)

    for module, deps in analyzer.dependencies.items():
        if module not in module_to_path:
            continue
        src_package = module_to_path[module].split(os.sep)[0]

        for dep in deps:
            dep_package = dep.split('.')[0]
            # Solo dependencias internas
            if dep_package in [p.split(os.sep)[0] for p in module_to_path.values()]:
                if src_package != dep_package:
                    package_deps[src_package].add(dep_package)

    # DFS para detectar ciclos
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in package_deps.get(node, set()):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                if cycle not in cycles:
                    cycles.append(cycle)
                return True

        path.pop()
        rec_stack.remove(node)
        return False

    packages = set(p.split(os.sep)[0] for p in module_to_path.values())
    for package in packages:
        if package not in visited:
            dfs(package)

    return cycles


def calculate_stability_vs_abstractness_score(abstractness: float, instability: float) -> float:
    """
    Calcula un score de calidad basado en la posición en el gráfico A vs I.

    Ideal: A + I ≈ 1 (Main Sequence)
    Score: 10 - (D * 10)
    """
    distance = calculate_distance(abstractness, instability)
    return max(0, 10 - (distance * 10))


def generate_report(analyzer: CleanArchitectureAnalyzer, module_to_path: Dict[str, str],
                   output_file: str):
    """Genera el reporte de Clean Architecture."""

    # Obtener paquetes
    packages = sorted(set(p.split(os.sep)[0] for p in module_to_path.values()))

    # Calcular métricas por paquete
    package_metrics = []
    for package in packages:
        abstractness = calculate_abstractness(analyzer, package)
        instability, ca, ce = calculate_instability(package, analyzer, module_to_path)
        distance = calculate_distance(abstractness, instability)
        zone = classify_zone(abstractness, instability, distance)
        score = calculate_stability_vs_abstractness_score(abstractness, instability)

        # Contar módulos
        modules = [m for m, p in module_to_path.items() if p.split(os.sep)[0] == package]

        package_metrics.append({
            'name': package,
            'abstractness': abstractness,
            'instability': instability,
            'distance': distance,
            'zone': zone,
            'score': score,
            'ca': ca,
            'ce': ce,
            'modules': len(modules),
            'abstractions': analyzer.abstractions.get(package, 0),
            'concretes': analyzer.concretes.get(package, 0)
        })

    # Detectar violaciones y ciclos
    violations = detect_layer_violations(analyzer, module_to_path)
    cycles = detect_package_cycles(analyzer, module_to_path)

    # Estadísticas globales
    total_packages = len(package_metrics)
    avg_abstractness = sum(p['abstractness'] for p in package_metrics) / total_packages if total_packages > 0 else 0
    avg_instability = sum(p['instability'] for p in package_metrics) / total_packages if total_packages > 0 else 0
    avg_distance = sum(p['distance'] for p in package_metrics) / total_packages if total_packages > 0 else 0
    avg_score = sum(p['score'] for p in package_metrics) / total_packages if total_packages > 0 else 0

    ideal_packages = sum(1 for p in package_metrics if p['distance'] <= 0.2)
    pain_zone = sum(1 for p in package_metrics if 'Pain' in p['zone'])
    useless_zone = sum(1 for p in package_metrics if 'Uselessness' in p['zone'])

    # Generar reporte
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# REPORTE DE MÉTRICAS DE CLEAN ARCHITECTURE\n")
        f.write("**Proyecto**: ISSE_Termostato\n")
        f.write(f"**Fecha**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Herramientas**: Script personalizado basado en AST de Python\n")
        f.write("**Alcance**: Código de producción (excluye tests y actores externos)\n\n")
        f.write("---\n\n")

        # RESUMEN EJECUTIVO
        f.write("## RESUMEN EJECUTIVO\n\n")
        f.write("### Visión General\n\n")
        f.write("Las métricas de Clean Architecture evalúan qué tan bien el proyecto sigue ")
        f.write("los principios arquitectónicos de Robert C. Martin. Se enfoca en la dirección ")
        f.write("de dependencias, abstracción, estabilidad y la Regla de Dependencia.\n\n")

        f.write("| Concepto | Valor | Interpretación |\n")
        f.write("|----------|-------|----------------|\n")
        f.write(f"| **Paquetes analizados** | {total_packages} | Total de paquetes del proyecto |\n")
        f.write(f"| **Abstractness promedio** | {avg_abstractness:.3f} | {'✅ Adecuado' if 0.3 <= avg_abstractness <= 0.7 else '⚠️ Revisar'} nivel de abstracción |\n")
        f.write(f"| **Instability promedio** | {avg_instability:.3f} | {'✅ Estable' if avg_instability < 0.5 else '⚠️ Inestable'} |\n")
        f.write(f"| **Distance promedio** | {avg_distance:.3f} | {'✅ Cerca' if avg_distance < 0.3 else '⚠️ Lejos'} de secuencia principal |\n")
        f.write(f"| **Score promedio** | {avg_score:.1f}/10 | Calidad arquitectónica |\n")
        f.write(f"| **Paquetes en Main Sequence** | {ideal_packages} | {ideal_packages/total_packages*100:.1f}% en posición ideal |\n")
        f.write(f"| **Paquetes en Zone of Pain** | {pain_zone} | {'❌' if pain_zone > 0 else '✅'} Rígidos y difíciles de cambiar |\n")
        f.write(f"| **Paquetes en Zone of Uselessness** | {useless_zone} | {'❌' if useless_zone > 0 else '✅'} Abstractos pero inútiles |\n")
        f.write(f"| **Violaciones de capas** | {len(violations)} | {'❌' if len(violations) > 0 else '✅'} Dependencias incorrectas |\n")
        f.write(f"| **Ciclos entre paquetes** | {len(cycles)} | {'❌' if len(cycles) > 0 else '✅'} Viola ADP |\n\n")

        # Distribuciones
        f.write("### Distribución por Zona Arquitectónica\n\n")
        zones_count = defaultdict(int)
        for p in package_metrics:
            zones_count[p['zone']] += 1

        f.write("| Zona | Paquetes | Porcentaje | Interpretación |\n")
        f.write("|------|----------|------------|----------------|\n")
        for zone, count in sorted(zones_count.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_packages * 100 if total_packages > 0 else 0
            estado = '✅' if 'Main' in zone or 'Ideal' in zone else '⚠️'
            f.write(f"| {zone} | {count} | {pct:.1f}% | {estado} |\n")

        f.write("\n---\n\n")

        # EXPLICACIÓN DE MÉTRICAS
        f.write("## 1. MÉTRICAS DE CLEAN ARCHITECTURE EXPLICADAS\n\n")

        f.write("### 1.1 Abstractness (A)\n\n")
        f.write("**Proporción de abstracción en un paquete**\n\n")
        f.write("```\nA = Na / Nc\n```\n\n")
        f.write("Donde:\n")
        f.write("- **Na** = Número de clases/interfaces abstractas\n")
        f.write("- **Nc** = Número total de clases\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0 = Completamente concreto\n")
        f.write("  - 1.0 = Completamente abstracto\n")
        f.write("  - 0.3-0.7 = Balance ideal\n\n")

        f.write("### 1.2 Instability (I)\n\n")
        f.write("**Resistencia al cambio de un paquete**\n\n")
        f.write("```\nI = Ce / (Ca + Ce)\n```\n\n")
        f.write("Donde:\n")
        f.write("- **Ce** = Efferent Coupling (dependencias salientes)\n")
        f.write("- **Ca** = Afferent Coupling (dependencias entrantes)\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0 = Máxima estabilidad (muchos dependen de él)\n")
        f.write("  - 1.0 = Máxima inestabilidad (depende de muchos)\n\n")

        f.write("### 1.3 Distance from Main Sequence (D)\n\n")
        f.write("**Distancia a la secuencia principal ideal**\n\n")
        f.write("```\nD = |A + I - 1|\n```\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0 = En la secuencia principal (ideal)\n")
        f.write("  - < 0.2 = Muy cerca (excelente)\n")
        f.write("  - 0.2-0.5 = Distancia aceptable\n")
        f.write("  - > 0.5 = Muy lejos (problemático)\n\n")

        f.write("### 1.4 Main Sequence (Secuencia Principal)\n\n")
        f.write("La línea ideal donde **A + I = 1**\n\n")
        f.write("**Principio**: Paquetes estables (I bajo) deben ser abstractos (A alto).\n")
        f.write("Paquetes inestables (I alto) deben ser concretos (A bajo).\n\n")

        f.write("### 1.5 Zonas Arquitectónicas\n\n")
        f.write("#### Zone of Pain (Zona de Dolor)\n")
        f.write("- **Características**: A ≈ 0, I ≈ 0\n")
        f.write("- **Problema**: Concreto y estable = rígido, difícil de cambiar\n")
        f.write("- **Solución**: Introducir abstracciones\n\n")

        f.write("#### Zone of Uselessness (Zona de Inutilidad)\n")
        f.write("- **Características**: A ≈ 1, I ≈ 1\n")
        f.write("- **Problema**: Abstracto e inestable = sin uso real\n")
        f.write("- **Solución**: Eliminar o hacer más estable\n\n")

        f.write("---\n\n")

        # MÉTRICAS POR PAQUETE
        f.write("## 2. MÉTRICAS POR PAQUETE\n\n")

        sorted_packages = sorted(package_metrics, key=lambda x: x['score'], reverse=True)

        f.write("| # | Paquete | A | I | D | Ca | Ce | Score | Zona | Estado |\n")
        f.write("|---|---------|---|---|---|----|----|-|------|--------|\n")

        for i, p in enumerate(sorted_packages, 1):
            estado = '✅' if p['score'] >= 7 else ('⚠️' if p['score'] >= 5 else '❌')
            f.write(f"| {i} | `{p['name']}` | {p['abstractness']:.3f} | {p['instability']:.3f} | "
                   f"{p['distance']:.3f} | {p['ca']} | {p['ce']} | {p['score']:.1f} | "
                   f"{p['zone']} | {estado} |\n")

        f.write("\n**Leyenda**:\n")
        f.write("- **A** = Abstractness (abstracción)\n")
        f.write("- **I** = Instability (inestabilidad)\n")
        f.write("- **D** = Distance (distancia a secuencia principal)\n")
        f.write("- **Ca** = Afferent Coupling (dependencias entrantes)\n")
        f.write("- **Ce** = Efferent Coupling (dependencias salientes)\n\n")

        f.write("---\n\n")

        # ANÁLISIS POR CAPA
        f.write("## 3. ANÁLISIS POR CAPA ARQUITECTÓNICA\n\n")

        # Agrupar módulos por capa
        layers = defaultdict(list)
        for module, path in module_to_path.items():
            layer = classify_layer(path)
            layers[layer].append(module)

        f.write("Distribución de módulos por capa de Clean Architecture:\n\n")
        f.write("| Capa | Módulos | Paquetes | Descripción |\n")
        f.write("|------|---------|----------|-------------|\n")

        for layer in sorted(layers.keys(), key=lambda x: get_layer_number(x)):
            modules = layers[layer]
            pkgs = set(module_to_path[m].split(os.sep)[0] for m in modules)

            if 'Layer 1' in layer:
                desc = "Entidades de negocio (núcleo)"
            elif 'Layer 2' in layer:
                desc = "Casos de uso y lógica de negocio"
            elif 'Layer 3' in layer:
                desc = "Adaptadores de interfaz"
            elif 'Layer 4' in layer:
                desc = "Frameworks y drivers externos"
            else:
                desc = "No clasificado"

            f.write(f"| {layer} | {len(modules)} | {', '.join(pkgs)} | {desc} |\n")

        f.write("\n---\n\n")

        # VIOLACIONES DE CAPAS
        f.write("## 4. VIOLACIONES DE LA REGLA DE DEPENDENCIA\n\n")

        if violations:
            f.write(f"Se detectaron **{len(violations)} violaciones** de la Regla de Dependencia.\n\n")
            f.write("**Regla**: Las dependencias deben apuntar hacia adentro (capas internas).\n\n")

            # Agrupar por severidad
            critical = [v for v in violations if v['severity'] >= 2]
            moderate = [v for v in violations if v['severity'] == 1]

            if critical:
                f.write(f"### 4.1 Violaciones Críticas ({len(critical)})\n\n")
                f.write("Dependencias que saltan múltiples capas:\n\n")
                f.write("| # | Origen | Capa Origen | Destino | Capa Destino | Severidad |\n")
                f.write("|---|--------|-------------|---------|--------------|-----------|\ n")

                for i, v in enumerate(critical[:20], 1):  # Top 20
                    f.write(f"| {i} | `{v['source']}` | {v['source_layer']} | "
                           f"`{v['target']}` | {v['target_layer']} | {v['severity']} ❌ |\n")

                if len(critical) > 20:
                    f.write(f"\n*...y {len(critical)-20} violaciones críticas más*\n")
                f.write("\n")

            if moderate:
                f.write(f"### 4.2 Violaciones Moderadas ({len(moderate)})\n\n")
                f.write("Dependencias de una capa interna a una externa:\n\n")
                f.write("| # | Origen | Capa Origen | Destino | Capa Destino |\n")
                f.write("|---|--------|-------------|---------|--------------|\ n")

                for i, v in enumerate(moderate[:15], 1):  # Top 15
                    f.write(f"| {i} | `{v['source']}` | {v['source_layer']} | "
                           f"`{v['target']}` | {v['target_layer']} ⚠️ |\n")

                if len(moderate) > 15:
                    f.write(f"\n*...y {len(moderate)-15} violaciones moderadas más*\n")
                f.write("\n")

            f.write("**Recomendaciones**:\n")
            f.write("1. Aplicar Dependency Inversion Principle (DIP)\n")
            f.write("2. Crear abstracciones en capas internas\n")
            f.write("3. Inyectar dependencias desde capas externas\n")
            f.write("4. Usar eventos/mensajes para desacoplar capas\n\n")
        else:
            f.write("✅ **No se detectaron violaciones** de la Regla de Dependencia.\n\n")
            f.write("Las dependencias fluyen correctamente hacia las capas internas.\n\n")

        f.write("---\n\n")

        # CICLOS ENTRE PAQUETES
        f.write("## 5. ACYCLIC DEPENDENCIES PRINCIPLE (ADP)\n\n")

        if cycles:
            f.write(f"Se detectaron **{len(cycles)} ciclos** entre paquetes.\n\n")
            f.write("**Principio violado**: Los paquetes no deben formar ciclos de dependencias.\n\n")

            for i, cycle in enumerate(cycles, 1):
                f.write(f"### 5.{i} Ciclo {i}\n\n")
                f.write("```\n")
                for j, pkg in enumerate(cycle):
                    if j < len(cycle) - 1:
                        f.write(f"{pkg}\n  ↓\n")
                    else:
                        f.write(f"{pkg}\n")
                f.write("```\n\n")

            f.write("**Impacto**: Los ciclos hacen difícil:\n")
            f.write("- Compilar/probar paquetes de forma independiente\n")
            f.write("- Entender el orden de construcción\n")
            f.write("- Reutilizar paquetes en otros proyectos\n\n")

            f.write("**Soluciones**:\n")
            f.write("1. Aplicar Dependency Inversion Principle\n")
            f.write("2. Crear nuevo paquete con abstracciones comunes\n")
            f.write("3. Mover clases entre paquetes\n")
            f.write("4. Usar patrón Observer/Mediator\n\n")
        else:
            f.write("✅ **No se detectaron ciclos** entre paquetes.\n\n")
            f.write("El proyecto cumple con el Acyclic Dependencies Principle.\n\n")

        f.write("---\n\n")

        # DIAGRAMA A vs I
        f.write("## 6. DIAGRAMA ABSTRACTNESS vs INSTABILITY\n\n")
        f.write("Posición de cada paquete en el gráfico A vs I:\n\n")
        f.write("```\nA (Abstractness)\n1.0 │                    Zone of\n    │                   Uselessness\n    │                  ╱\n    │                ╱\n0.5 │              ╱  Main Sequence\n    │            ╱\n    │          ╱\n    │  Zone  ╱\n    │  of   ╱\n    │ Pain ╱\n0.0 └────────────────────────────────\n    0.0    0.5                    1.0\n           I (Instability)\n```\n\n")

        f.write("| Paquete | A | I | Posición |\n")
        f.write("|---------|---|---|----------|\n")
        for p in sorted_packages:
            f.write(f"| `{p['name']}` | {p['abstractness']:.3f} | {p['instability']:.3f} | {p['zone']} |\n")

        f.write("\n---\n\n")

        # CONCLUSIONES
        f.write("## 7. CONCLUSIONES Y RECOMENDACIONES\n\n")

        f.write("### 7.1 Puntos Fuertes ⭐\n\n")
        strengths = []
        if ideal_packages / total_packages >= 0.5:
            strengths.append(f"1. **{ideal_packages} paquetes** ({ideal_packages/total_packages*100:.1f}%) en Main Sequence")
        if avg_distance < 0.3:
            strengths.append(f"2. **Distance promedio bajo**: {avg_distance:.3f}")
        if pain_zone == 0:
            strengths.append("3. **Sin paquetes en Zone of Pain**: No hay rigidez arquitectónica")
        if useless_zone == 0:
            strengths.append("4. **Sin paquetes en Zone of Uselessness**: No hay abstracciones innecesarias")
        if len(cycles) == 0:
            strengths.append("5. **Sin ciclos entre paquetes**: Cumple ADP")
        if len(violations) == 0:
            strengths.append("6. **Sin violaciones de capas**: Respeta Regla de Dependencia")

        if strengths:
            for s in strengths:
                f.write(f"{s}\n")
        else:
            f.write("*Se requiere mejora en múltiples áreas*\n")

        f.write("\n### 7.2 Áreas de Mejora ⚠️\n\n")
        issues = []
        if pain_zone > 0:
            issues.append(f"1. **{pain_zone} paquetes en Zone of Pain**: Introducir abstracciones")
        if useless_zone > 0:
            issues.append(f"2. **{useless_zone} paquetes en Zone of Uselessness**: Eliminar o estabilizar")
        if len(violations) > 0:
            issues.append(f"3. **{len(violations)} violaciones de capas**: Invertir dependencias")
        if len(cycles) > 0:
            issues.append(f"4. **{len(cycles)} ciclos entre paquetes**: Romper ciclos")
        if avg_distance > 0.5:
            issues.append(f"5. **Distance promedio alto**: {avg_distance:.3f}")

        if issues:
            for issue in issues:
                f.write(f"{issue}\n")
            f.write("\n")
        else:
            f.write("✅ No se identificaron áreas críticas de mejora\n\n")

        f.write("### 7.3 Plan de Acción\n\n")
        f.write("#### Prioridad Alta\n")
        if len(violations) > 0:
            f.write("1. Resolver violaciones críticas de la Regla de Dependencia\n")
        if len(cycles) > 0:
            f.write("2. Eliminar ciclos entre paquetes\n")
        if pain_zone > 0:
            f.write("3. Extraer interfaces de paquetes en Zone of Pain\n")
        if not (len(violations) > 0 or len(cycles) > 0 or pain_zone > 0):
            f.write("✅ No se requieren acciones de alta prioridad\n")

        f.write("\n#### Prioridad Media\n")
        if useless_zone > 0:
            f.write("1. Revisar utilidad de paquetes en Zone of Uselessness\n")
        f.write("2. Mejorar balance A/I en paquetes con D > 0.3\n")
        f.write("3. Documentar decisiones arquitectónicas\n")

        f.write("\n#### Prioridad Baja\n")
        f.write("1. Crear diagramas de arquitectura por capas\n")
        f.write("2. Establecer métricas objetivo para nuevos paquetes\n")
        f.write("3. Automatizar verificación de métricas en CI/CD\n\n")

        f.write("### 7.4 Calificación General\n\n")

        # Calcular score global
        score = 10.0
        if len(violations) > 10:
            score -= 3
        elif len(violations) > 0:
            score -= 1.5

        if len(cycles) > 0:
            score -= 2

        if pain_zone > 0:
            score -= 1.5

        if useless_zone > 0:
            score -= 1

        if avg_distance > 0.5:
            score -= 1.5
        elif avg_distance > 0.3:
            score -= 0.5

        score = max(0, score)

        f.write(f"**Clean Architecture del Proyecto**: **{score:.1f}/10** ")
        if score >= 9:
            f.write("⭐⭐⭐\n\n")
        elif score >= 7:
            f.write("⭐⭐\n\n")
        elif score >= 5:
            f.write("⭐\n\n")
        else:
            f.write("⚠️\n\n")

        f.write("| Indicador | Valor | Umbral | Estado |\n")
        f.write("|-----------|-------|--------|--------|\n")
        f.write(f"| Distance promedio | {avg_distance:.3f} | ≤ 0.3 | {'✅' if avg_distance <= 0.3 else '❌'} |\n")
        f.write(f"| Paquetes en Main Seq. | {ideal_packages}/{total_packages} | ≥ 50% | {'✅' if ideal_packages/total_packages >= 0.5 else '❌'} |\n")
        f.write(f"| Zone of Pain | {pain_zone} | 0 | {'✅' if pain_zone == 0 else '❌'} |\n")
        f.write(f"| Violaciones de capas | {len(violations)} | 0 | {'✅' if len(violations) == 0 else '❌'} |\n")
        f.write(f"| Ciclos entre paquetes | {len(cycles)} | 0 | {'✅' if len(cycles) == 0 else '❌'} |\n")

        f.write("\n---\n\n")
        f.write("**Fin del Reporte de Clean Architecture**\n\n")
        f.write("*Generado con: Script personalizado basado en AST de Python*\n")
        f.write(f"*Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


def main():
    """Función principal."""
    import sys

    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(f"Analizando proyecto en: {project_root}")

    analyzer, module_to_path = analyze_project(project_root)
    print(f"Módulos encontrados: {len(module_to_path)}")

    output_file = os.path.join(project_root, "docs", "reporte_metricas_clean_architecture.md")
    generate_report(analyzer, module_to_path, output_file)
    print(f"Reporte generado: {output_file}")


if __name__ == "__main__":
    main()
