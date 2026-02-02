"""
Script para calcular métricas DSM (Design Structure Matrix) del proyecto ISSE_Termostato.

Métricas calculadas:
- DSM (Design Structure Matrix): Matriz de dependencias
- Propagation Cost: Costo de propagación de cambios
- Visibility: Visibilidad entre módulos
- Clustering Coefficient: Coeficiente de agrupamiento
- Cyclomatic Complexity DSM: Detección de ciclos
- Modularity: Modularidad del sistema
- VDM (Visibility Design Matrix): Matriz de visibilidad de diseño
"""

import ast
import os
from pathlib import Path
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple
import re


class DependencyAnalyzer(ast.NodeVisitor):
    """Analizador de dependencias usando AST de Python."""

    def __init__(self):
        self.current_module = ""
        self.dependencies = defaultdict(set)  # módulo -> {módulos de los que depende}
        self.classes_per_module = defaultdict(set)  # módulo -> {clases}
        self.current_class = None

    def visit_Import(self, node):
        """Visita sentencias import."""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            self.dependencies[self.current_module].add(module_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visita sentencias from...import."""
        if node.module:
            module_name = node.module.split('.')[0]
            self.dependencies[self.current_module].add(module_name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visita definiciones de clases."""
        self.classes_per_module[self.current_module].add(node.name)
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class


def analyze_project(root_path: str) -> Tuple[DependencyAnalyzer, Dict[str, str]]:
    """Analiza todos los archivos Python del proyecto."""
    analyzer = DependencyAnalyzer()
    module_to_path = {}  # módulo -> path completo

    # Excluir directorios
    exclude_dirs = {'Test', 'tests', '__pycache__', '.git', 'venv', 'env',
                   'actores_externos'}

    for py_file in Path(root_path).rglob('*.py'):
        # Saltar archivos de test, setup y docs
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue
        if py_file.name.startswith('setup_') or py_file.name == 'ejecutar.py':
            continue
        if 'docs' in py_file.parts:
            continue

        try:
            # Convertir path a nombre de módulo
            rel_path = py_file.relative_to(root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')

            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(py_file))
                analyzer.current_module = module_name
                module_to_path[module_name] = str(rel_path)
                analyzer.visit(tree)
        except Exception as e:
            print(f"Error procesando {py_file}: {e}")

    return analyzer, module_to_path


def build_internal_dsm(analyzer: DependencyAnalyzer, module_to_path: Dict[str, str]) -> Tuple[List[str], Dict[Tuple[str, str], int]]:
    """
    Construye la DSM (Design Structure Matrix) interna del proyecto.
    Retorna: (lista_módulos, matriz_dependencias)
    """
    # Obtener solo módulos internos
    internal_modules = sorted(module_to_path.keys())

    # Construir matriz de dependencias
    dsm_matrix = {}
    for module in internal_modules:
        for dep in analyzer.dependencies.get(module, set()):
            # Solo dependencias internas
            matching = [m for m in internal_modules if m.startswith(dep) or dep in m]
            for target in matching:
                if target != module:
                    dsm_matrix[(module, target)] = dsm_matrix.get((module, target), 0) + 1

    return internal_modules, dsm_matrix


def calculate_propagation_cost(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int]) -> Dict[str, float]:
    """
    Calcula el costo de propagación de cambios para cada módulo.
    PC(i) = número de módulos alcanzables desde i (transitividad)
    """
    propagation_cost = {}

    for module in modules:
        # BFS para encontrar todos los módulos alcanzables
        visited = set()
        queue = deque([module])
        visited.add(module)

        while queue:
            current = queue.popleft()
            # Encontrar dependientes (quiénes dependen de current)
            for (src, dst) in dsm_matrix:
                if dst == current and src not in visited:
                    visited.add(src)
                    queue.append(src)

        # Costo = número de módulos afectados (excluyendo el propio)
        propagation_cost[module] = len(visited) - 1

    return propagation_cost


def calculate_visibility(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int]) -> Dict[Tuple[str, str], int]:
    """
    Calcula la matriz de visibilidad (alcance transitivo).
    Visibility(i,j) = 1 si j es alcanzable desde i (directa o indirectamente)
    """
    visibility_matrix = {}

    for src_module in modules:
        # BFS para encontrar todos los módulos visibles desde src_module
        visited = set()
        queue = deque([src_module])
        visited.add(src_module)

        while queue:
            current = queue.popleft()
            # Encontrar módulos a los que current depende
            for (s, d) in dsm_matrix:
                if s == current and d not in visited:
                    visited.add(d)
                    queue.append(d)

        # Marcar visibilidad
        for dst_module in visited:
            if dst_module != src_module:
                visibility_matrix[(src_module, dst_module)] = 1

    return visibility_matrix


def calculate_clustering_coefficient(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int]) -> Dict[str, float]:
    """
    Calcula el coeficiente de agrupamiento para cada módulo.
    CC(i) = (aristas entre vecinos de i) / (aristas posibles entre vecinos)
    """
    clustering = {}

    for module in modules:
        # Encontrar vecinos (módulos con los que hay dependencia mutua)
        neighbors = set()
        for (src, dst) in dsm_matrix:
            if src == module:
                neighbors.add(dst)
            if dst == module:
                neighbors.add(src)

        if len(neighbors) < 2:
            clustering[module] = 0.0
            continue

        # Contar aristas entre vecinos
        edges_between_neighbors = 0
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 != n2 and (n1, n2) in dsm_matrix:
                    edges_between_neighbors += 1

        # Aristas posibles
        max_edges = len(neighbors) * (len(neighbors) - 1)

        clustering[module] = edges_between_neighbors / max_edges if max_edges > 0 else 0.0

    return clustering


def detect_cycles(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int]) -> List[List[str]]:
    """
    Detecta ciclos de dependencias usando DFS.
    Retorna lista de ciclos encontrados.
    """
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        # Explorar vecinos
        neighbors = [dst for (src, dst) in dsm_matrix if src == node]
        for neighbor in neighbors:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                # Ciclo detectado
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
                return True

        path.pop()
        rec_stack.remove(node)
        return False

    for module in modules:
        if module not in visited:
            dfs(module)

    return cycles


def calculate_modularity(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int],
                         module_to_path: Dict[str, str]) -> Dict[str, float]:
    """
    Calcula la modularidad por paquete/directorio.
    Modularity = (dependencias internas) / (dependencias totales)
    """
    # Agrupar módulos por paquete (primer nivel de directorio)
    packages = defaultdict(set)
    for module, path in module_to_path.items():
        package = path.split(os.sep)[0] if os.sep in path else 'root'
        packages[package].add(module)

    modularity = {}

    for package, pkg_modules in packages.items():
        internal_deps = 0
        external_deps = 0

        for (src, dst) in dsm_matrix:
            if src in pkg_modules:
                if dst in pkg_modules:
                    internal_deps += 1
                else:
                    external_deps += 1

        total_deps = internal_deps + external_deps
        modularity[package] = internal_deps / total_deps if total_deps > 0 else 0.0

    return modularity


def calculate_fan_metrics(modules: List[str], dsm_matrix: Dict[Tuple[str, str], int]) -> Dict[str, Tuple[int, int, float]]:
    """
    Calcula Fan-In, Fan-Out e Instability para cada módulo.
    Retorna: {módulo: (fan_in, fan_out, instability)}
    """
    fan_metrics = {}

    for module in modules:
        # Fan-In: cuántos módulos dependen de este
        fan_in = len([src for (src, dst) in dsm_matrix if dst == module])

        # Fan-Out: de cuántos módulos depende este
        fan_out = len([dst for (src, dst) in dsm_matrix if src == module])

        # Instability: I = Fan-Out / (Fan-In + Fan-Out)
        instability = fan_out / (fan_in + fan_out) if (fan_in + fan_out) > 0 else 0.0

        fan_metrics[module] = (fan_in, fan_out, instability)

    return fan_metrics


def generate_report(analyzer: DependencyAnalyzer, module_to_path: Dict[str, str], output_file: str):
    """Genera el reporte de métricas DSM."""

    # Construir DSM interna
    modules, dsm_matrix = build_internal_dsm(analyzer, module_to_path)

    # Calcular métricas
    propagation_cost = calculate_propagation_cost(modules, dsm_matrix)
    visibility_matrix = calculate_visibility(modules, dsm_matrix)
    clustering = calculate_clustering_coefficient(modules, dsm_matrix)
    cycles = detect_cycles(modules, dsm_matrix)
    modularity = calculate_modularity(modules, dsm_matrix, module_to_path)
    fan_metrics = calculate_fan_metrics(modules, dsm_matrix)

    # Estadísticas
    total_modules = len(modules)
    total_dependencies = len(dsm_matrix)
    avg_propagation = sum(propagation_cost.values()) / total_modules if total_modules > 0 else 0
    avg_clustering = sum(clustering.values()) / total_modules if total_modules > 0 else 0
    avg_fan_in = sum(fm[0] for fm in fan_metrics.values()) / total_modules if total_modules > 0 else 0
    avg_fan_out = sum(fm[1] for fm in fan_metrics.values()) / total_modules if total_modules > 0 else 0
    avg_instability = sum(fm[2] for fm in fan_metrics.values()) / total_modules if total_modules > 0 else 0

    # Calcular densidad de la DSM
    max_possible_deps = total_modules * (total_modules - 1)
    density = total_dependencies / max_possible_deps if max_possible_deps > 0 else 0

    # Generar reporte en Markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# REPORTE DE MÉTRICAS DSM (DESIGN STRUCTURE MATRIX)\n")
        f.write("**Proyecto**: ISSE_Termostato\n")
        f.write(f"**Fecha**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Herramientas**: Script personalizado basado en AST de Python\n")
        f.write("**Alcance**: Código de producción (excluye tests y actores externos)\n\n")
        f.write("---\n\n")

        # RESUMEN EJECUTIVO
        f.write("## RESUMEN EJECUTIVO\n\n")
        f.write("### Visión General\n\n")
        f.write("La DSM (Design Structure Matrix) es una representación matricial de las dependencias ")
        f.write("entre componentes del sistema. Permite visualizar acoplamiento, detectar ciclos, ")
        f.write("y analizar el impacto de cambios en el diseño.\n\n")

        f.write("| Concepto | Valor | Interpretación |\n")
        f.write("|----------|-------|----------------|\n")
        f.write(f"| **Módulos analizados** | {total_modules} | Total de módulos del proyecto |\n")
        f.write(f"| **Dependencias internas** | {total_dependencies} | Enlaces entre módulos |\n")
        f.write(f"| **Densidad DSM** | {density:.3f} | {'✅ Baja' if density < 0.3 else '⚠️ Alta'} densidad de dependencias |\n")
        f.write(f"| **Costo propagación promedio** | {avg_propagation:.2f} | {'✅ Bajo' if avg_propagation < 5 else '⚠️ Alto'} impacto de cambios |\n")
        f.write(f"| **Clustering promedio** | {avg_clustering:.3f} | {'✅ Alto' if avg_clustering > 0.3 else '⚠️ Bajo'} agrupamiento |\n")
        f.write(f"| **Fan-In promedio** | {avg_fan_in:.2f} | Módulos que dependen de cada uno |\n")
        f.write(f"| **Fan-Out promedio** | {avg_fan_out:.2f} | Módulos de los que depende cada uno |\n")
        f.write(f"| **Instabilidad promedio** | {avg_instability:.3f} | {'✅ Estable' if avg_instability < 0.5 else '⚠️ Inestable'} |\n")
        f.write(f"| **Ciclos detectados** | {len(cycles)} | {'✅ Sin ciclos' if len(cycles) == 0 else '❌ Ciclos presentes'} |\n\n")

        # Distribuciones
        f.write("### Distribución por Costo de Propagación\n\n")
        low_pc = sum(1 for pc in propagation_cost.values() if pc <= 3)
        med_pc = sum(1 for pc in propagation_cost.values() if 3 < pc <= 7)
        high_pc = sum(1 for pc in propagation_cost.values() if pc > 7)

        f.write("| Nivel | Módulos | Porcentaje | Criterio |\n")
        f.write("|-------|---------|------------|----------|\n")
        f.write(f"| **Bajo impacto** | {low_pc} | {low_pc/total_modules*100:.1f}% | PC ≤ 3 |\n")
        f.write(f"| **Impacto medio** | {med_pc} | {med_pc/total_modules*100:.1f}% | 3 < PC ≤ 7 |\n")
        f.write(f"| **Alto impacto** | {high_pc} | {high_pc/total_modules*100:.1f}% | PC > 7 |\n\n")

        f.write("---\n\n")

        # EXPLICACIÓN DE MÉTRICAS
        f.write("## 1. MÉTRICAS DSM EXPLICADAS\n\n")

        f.write("### 1.1 Design Structure Matrix (DSM)\n\n")
        f.write("Matriz cuadrada donde:\n")
        f.write("- Filas y columnas representan módulos\n")
        f.write("- DSM[i,j] = 1 si módulo i depende de módulo j\n")
        f.write("- Diagonal principal = dependencias circulares\n")
        f.write("- Triángulo inferior = feedback (ciclos)\n")
        f.write("- Triángulo superior = feedforward (flujo normal)\n\n")

        f.write("### 1.2 Propagation Cost (Costo de Propagación)\n\n")
        f.write("**Menor es mejor** - Número de módulos afectados por cambios en este módulo.\n\n")
        f.write("```\nPC(i) = |módulos alcanzables desde i|\n```\n\n")
        f.write("- **Rango**: [0, n-1] donde n = total de módulos\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0-3: Bajo impacto (cambios localizados)\n")
        f.write("  - 4-7: Impacto medio (cambios propagables)\n")
        f.write("  - > 7: Alto impacto (cambios sistémicos)\n\n")

        f.write("### 1.3 Visibility (Visibilidad)\n\n")
        f.write("**Matriz de alcance transitivo** - Muestra qué módulos son visibles desde cada módulo.\n\n")
        f.write("```\nV[i,j] = 1 si j es alcanzable desde i (directa o indirectamente)\n```\n\n")

        f.write("### 1.4 Clustering Coefficient (Coeficiente de Agrupamiento)\n\n")
        f.write("**Mayor es mejor** - Mide qué tan agrupados están los módulos relacionados.\n\n")
        f.write("```\nCC(i) = (aristas entre vecinos) / (aristas posibles)\n```\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0-0.3: Bajo agrupamiento (módulo aislado)\n")
        f.write("  - 0.3-0.7: Agrupamiento moderado\n")
        f.write("  - 0.7-1.0: Alto agrupamiento (subsistema cohesivo)\n\n")

        f.write("### 1.5 Modularity (Modularidad)\n\n")
        f.write("**Mayor es mejor** - Proporción de dependencias internas vs externas por paquete.\n\n")
        f.write("```\nM = (deps internas) / (deps totales)\n```\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0-0.3: Baja modularidad\n")
        f.write("  - 0.3-0.7: Modularidad moderada\n")
        f.write("  - 0.7-1.0: Alta modularidad (paquete independiente)\n\n")

        f.write("---\n\n")

        # TOP MÓDULOS POR PROPAGATION COST
        f.write("## 2. TOP 20 MÓDULOS POR COSTO DE PROPAGACIÓN\n\n")
        f.write("Módulos con mayor impacto sistémico (cambios afectan a más módulos):\n\n")

        top_propagation = sorted(propagation_cost.items(), key=lambda x: (x[1], x[0]), reverse=True)[:20]

        f.write("| # | Módulo | PC | Fan-In | Fan-Out | Instability | Clustering | Archivo |\n")
        f.write("|---|--------|----|----|---------|-------------|------------|----------|\n")

        for i, (module, pc) in enumerate(top_propagation, 1):
            fan_in, fan_out, inst = fan_metrics[module]
            clust = clustering[module]
            path = module_to_path[module]
            estado = '⚠️' if pc > 7 else '✅'
            f.write(f"| {i} | `{module}` | {pc:.0f} | {fan_in} | {fan_out} | "
                   f"{inst:.3f} | {clust:.3f} | `{path}` {estado} |\n")

        f.write("\n**Observaciones**:\n")
        high_impact = [m for m, pc in propagation_cost.items() if pc > 7]
        if high_impact:
            f.write(f"- {len(high_impact)} módulos con alto impacto (PC > 7)\n")
            f.write("- **Recomendación**: Estos módulos requieren mayor cuidado al modificarlos\n")
            f.write("- Considerar aislar funcionalidades críticas\n\n")
        else:
            f.write("- ✅ No hay módulos con impacto excesivamente alto\n\n")

        f.write("---\n\n")

        # ANÁLISIS DE CLUSTERING
        f.write("## 3. ANÁLISIS DE CLUSTERING (AGRUPAMIENTO)\n\n")
        f.write("### 3.1 Top 15 Módulos por Coeficiente de Agrupamiento\n\n")

        top_clustering = sorted(clustering.items(), key=lambda x: (x[1], x[0]), reverse=True)[:15]

        f.write("| # | Módulo | Clustering | Fan-In | Fan-Out | PC | Archivo |\n")
        f.write("|---|--------|------------|--------|---------|----|---------|\n")

        for i, (module, clust) in enumerate(top_clustering, 1):
            fan_in, fan_out, _ = fan_metrics[module]
            pc = propagation_cost[module]
            path = module_to_path[module]
            estado = '✅' if clust > 0.3 else '⚠️'
            f.write(f"| {i} | `{module}` | {clust:.3f} | {fan_in} | {fan_out} | "
                   f"{pc:.0f} | `{path}` {estado} |\n")

        f.write("\n**Interpretación**:\n")
        high_clust = sum(1 for c in clustering.values() if c > 0.3)
        f.write(f"- {high_clust} módulos ({high_clust/total_modules*100:.1f}%) con alto agrupamiento\n")
        f.write("- Alto clustering indica subsistemas bien cohesionados\n")
        f.write("- Bajo clustering puede indicar módulos puente o de coordinación\n\n")

        f.write("---\n\n")

        # CICLOS DE DEPENDENCIAS
        f.write("## 4. CICLOS DE DEPENDENCIAS\n\n")

        if cycles:
            f.write(f"Se detectaron **{len(cycles)} ciclos** de dependencias en el proyecto:\n\n")

            for i, cycle in enumerate(cycles, 1):
                f.write(f"### 4.{i} Ciclo {i}\n\n")
                f.write("```\n")
                for j, module in enumerate(cycle):
                    if j < len(cycle) - 1:
                        f.write(f"{module}\n  ↓\n")
                    else:
                        f.write(f"{module}\n")
                f.write("```\n\n")

                f.write("**Módulos involucrados**:\n")
                for module in set(cycle):
                    if module in module_to_path:
                        f.write(f"- `{module}` → `{module_to_path[module]}`\n")
                f.write("\n")

            f.write("**Recomendaciones**:\n")
            f.write("1. Eliminar ciclos mediante Dependency Inversion Principle\n")
            f.write("2. Usar interfaces/abstracciones para romper dependencias circulares\n")
            f.write("3. Reestructurar módulos para establecer jerarquía clara\n\n")
        else:
            f.write("✅ **No se detectaron ciclos de dependencias** en el proyecto.\n\n")
            f.write("Esto indica una arquitectura bien estructurada con jerarquía clara de dependencias.\n\n")

        f.write("---\n\n")

        # MODULARIDAD POR PAQUETE
        f.write("## 5. MODULARIDAD POR PAQUETE\n\n")

        f.write("Análisis de cohesión interna de cada paquete:\n\n")
        f.write("| # | Paquete | Modularidad | Módulos | Deps Internas | Deps Externas | Estado |\n")
        f.write("|---|---------|-------------|---------|---------------|---------------|--------|\n")

        for i, (package, mod) in enumerate(sorted(modularity.items(), key=lambda x: x[1], reverse=True), 1):
            pkg_modules = [m for m, p in module_to_path.items()
                          if (p.split(os.sep)[0] if os.sep in p else 'root') == package]
            num_modules = len(pkg_modules)

            # Contar dependencias
            internal = sum(1 for (s, d) in dsm_matrix if s in pkg_modules and d in pkg_modules)
            external = sum(1 for (s, d) in dsm_matrix if s in pkg_modules and d not in pkg_modules)

            estado = '✅' if mod > 0.5 else ('⚠️' if mod > 0.3 else '❌')
            f.write(f"| {i} | `{package}` | {mod:.3f} | {num_modules} | {internal} | {external} | {estado} |\n")

        f.write("\n**Interpretación**:\n")
        f.write("- Modularidad > 0.7: Paquete muy cohesivo e independiente\n")
        f.write("- Modularidad 0.3-0.7: Balance aceptable\n")
        f.write("- Modularidad < 0.3: Alta dependencia externa\n\n")

        f.write("---\n\n")

        # MÉTRICAS FAN-IN/FAN-OUT
        f.write("## 6. ANÁLISIS FAN-IN / FAN-OUT\n\n")

        f.write("### 6.1 Top 15 Módulos por Fan-In (Más Usados)\n\n")
        top_fanin = sorted(fan_metrics.items(), key=lambda x: (x[1][0], x[0]), reverse=True)[:15]

        f.write("| # | Módulo | Fan-In | Fan-Out | Instability | PC | Archivo |\n")
        f.write("|---|--------|--------|---------|-------------|----|---------|\n")

        for i, (module, (fi, fo, inst)) in enumerate(top_fanin, 1):
            pc = propagation_cost[module]
            path = module_to_path[module]
            f.write(f"| {i} | `{module}` | {fi} | {fo} | {inst:.3f} | {pc:.0f} | `{path}` |\n")

        f.write("\n### 6.2 Top 15 Módulos por Fan-Out (Más Dependientes)\n\n")
        top_fanout = sorted(fan_metrics.items(), key=lambda x: (x[1][1], x[0]), reverse=True)[:15]

        f.write("| # | Módulo | Fan-Out | Fan-In | Instability | PC | Archivo |\n")
        f.write("|---|--------|---------|--------|-------------|----|---------|\n")

        for i, (module, (fi, fo, inst)) in enumerate(top_fanout, 1):
            pc = propagation_cost[module]
            path = module_to_path[module]
            f.write(f"| {i} | `{module}` | {fo} | {fi} | {inst:.3f} | {pc:.0f} | `{path}` |\n")

        f.write("\n---\n\n")

        # MATRIZ DSM (muestra simplificada)
        f.write("## 7. MATRIZ DSM SIMPLIFICADA\n\n")
        f.write("Mostrando solo dependencias principales (módulos con más conexiones):\n\n")

        # Seleccionar top 10 módulos por número de conexiones
        connections = defaultdict(int)
        for (src, dst) in dsm_matrix:
            connections[src] += 1
            connections[dst] += 1

        top_connected = sorted(connections.items(), key=lambda x: x[1], reverse=True)[:10]
        top_modules = [m for m, _ in top_connected]

        # Imprimir matriz
        f.write("| Módulo | " + " | ".join([m.split('.')[-1][:8] for m in top_modules]) + " |\n")
        f.write("|--------|" + "|".join(["--------"] * len(top_modules)) + "|\n")

        for src in top_modules:
            row = f"| `{src.split('.')[-1][:20]}` |"
            for dst in top_modules:
                if (src, dst) in dsm_matrix:
                    row += " X |"
                elif src == dst:
                    row += " - |"
                else:
                    row += "   |"
            f.write(row + "\n")

        f.write("\n**Leyenda**: X = dependencia, - = mismo módulo\n\n")

        f.write("---\n\n")

        # CONCLUSIONES
        f.write("## 8. CONCLUSIONES Y RECOMENDACIONES\n\n")

        f.write("### 8.1 Puntos Fuertes ⭐\n\n")
        if density < 0.3:
            f.write(f"1. **Baja densidad DSM**: {density:.3f} indica bajo acoplamiento global\n")
        if avg_propagation < 5:
            f.write(f"2. **Bajo costo de propagación**: {avg_propagation:.2f} facilita el mantenimiento\n")
        if len(cycles) == 0:
            f.write("3. **Sin ciclos de dependencias**: Arquitectura bien estructurada\n")
        if avg_clustering > 0.3:
            f.write(f"4. **Buen agrupamiento**: {avg_clustering:.3f} indica subsistemas cohesivos\n")

        f.write("\n### 8.2 Áreas de Mejora ⚠️\n\n")
        issues = []
        if len(cycles) > 0:
            issues.append(f"1. **Ciclos de dependencias**: {len(cycles)} ciclos detectados")
        if high_impact:
            issues.append(f"2. **Módulos de alto impacto**: {len(high_impact)} módulos con PC > 7")
        if density > 0.5:
            issues.append(f"3. **Alta densidad**: {density:.3f} indica posible sobre-acoplamiento")
        if avg_clustering < 0.3:
            issues.append(f"4. **Bajo clustering**: {avg_clustering:.3f} puede indicar falta de cohesión")

        if issues:
            for issue in issues:
                f.write(f"{issue}\n")
            f.write("\n")
        else:
            f.write("✅ No se identificaron áreas críticas de mejora\n\n")

        f.write("### 8.3 Recomendaciones Específicas\n\n")

        f.write("#### Para reducir costo de propagación:\n")
        f.write("1. Aplicar Dependency Inversion Principle (DIP)\n")
        f.write("2. Usar abstracciones/interfaces en módulos centrales\n")
        f.write("3. Reducir dependencias transitivas\n\n")

        f.write("#### Para mejorar modularidad:\n")
        f.write("1. Agrupar funcionalidades relacionadas\n")
        f.write("2. Minimizar dependencias entre paquetes\n")
        f.write("3. Establecer APIs claras entre subsistemas\n\n")

        if cycles:
            f.write("#### Para eliminar ciclos:\n")
            f.write("1. Identificar la dependencia más débil del ciclo\n")
            f.write("2. Introducir abstracción o evento para romper el ciclo\n")
            f.write("3. Reestructurar responsabilidades entre módulos\n\n")

        f.write("### 8.4 Calificación General\n\n")

        # Calcular puntuación
        score = 10.0
        if density > 0.5:
            score -= 2
        elif density > 0.3:
            score -= 1

        if len(cycles) > 0:
            score -= 2

        if avg_propagation > 10:
            score -= 2
        elif avg_propagation > 7:
            score -= 1

        if avg_clustering < 0.2:
            score -= 1

        score = max(0, score)

        f.write(f"**Métricas DSM del Proyecto**: **{score:.1f}/10** ")
        if score >= 9:
            f.write("⭐⭐⭐\n\n")
        elif score >= 7:
            f.write("⭐⭐\n\n")
        elif score >= 5:
            f.write("⭐\n\n")
        else:
            f.write("⚠️\n\n")

        # Resumen de indicadores
        f.write("| Indicador | Valor | Umbral | Estado |\n")
        f.write("|-----------|-------|--------|--------|\n")
        f.write(f"| Densidad DSM | {density:.3f} | ≤ 0.3 | {'✅' if density <= 0.3 else '❌'} |\n")
        f.write(f"| Propagation Cost | {avg_propagation:.2f} | ≤ 5 | {'✅' if avg_propagation <= 5 else '❌'} |\n")
        f.write(f"| Clustering | {avg_clustering:.3f} | ≥ 0.3 | {'✅' if avg_clustering >= 0.3 else '❌'} |\n")
        f.write(f"| Ciclos | {len(cycles)} | 0 | {'✅' if len(cycles) == 0 else '❌'} |\n")
        f.write(f"| Instabilidad | {avg_instability:.3f} | ≤ 0.5 | {'✅' if avg_instability <= 0.5 else '❌'} |\n")

        f.write("\n---\n\n")
        f.write("**Fin del Reporte de Métricas DSM**\n\n")
        f.write("*Generado con: Script personalizado basado en AST de Python*\n")
        f.write(f"*Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


def main():
    """Función principal."""
    import sys

    # Obtener directorio raíz del proyecto
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(f"Analizando proyecto en: {project_root}")

    # Analizar proyecto
    analyzer, module_to_path = analyze_project(project_root)
    print(f"Módulos encontrados: {len(module_to_path)}")

    # Generar reporte
    output_file = os.path.join(project_root, "docs", "reporte_metricas_dsm.md")
    generate_report(analyzer, module_to_path, output_file)
    print(f"Reporte generado: {output_file}")


if __name__ == "__main__":
    main()
