"""
Script para calcular métricas de herencia del proyecto ISSE_Termostato.

Métricas calculadas:
- DIT (Depth of Inheritance Tree): Profundidad del árbol de herencia
- NOC (Number of Children): Número de hijos directos
- NOP (Number of Parents): Número de padres directos (herencia múltiple)
- NOM (Number of Methods): Número de métodos totales (heredados + propios)
- MIF (Method Inheritance Factor): Factor de herencia de métodos
- AIF (Attribute Inheritance Factor): Factor de herencia de atributos
- POF (Polymorphism Factor): Factor de polimorfismo
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class InheritanceAnalyzer(ast.NodeVisitor):
    """Analizador de herencia usando AST de Python."""

    def __init__(self):
        self.classes = {}  # Diccionario: nombre_clase -> info_clase
        self.inheritance_map = defaultdict(list)  # padre -> [hijos]
        self.reverse_inheritance_map = defaultdict(list)  # hijo -> [padres]
        self.current_file = ""

    def visit_ClassDef(self, node):
        """Visita una definición de clase."""
        class_name = node.name

        # Obtener bases (padres)
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                # Para casos como module.ClassName
                bases.append(base.attr)

        # Contar métodos propios (excluyendo __init__ y métodos privados para simplicidad)
        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

        # Contar atributos (aproximación: asignaciones en __init__)
        attributes = set()
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                if target.value.id == 'self':
                                    attributes.add(target.attr)

        # Guardar información de la clase
        self.classes[class_name] = {
            'file': self.current_file,
            'bases': bases,
            'methods': methods,
            'attributes': list(attributes),
            'node': node
        }

        # Actualizar mapas de herencia
        for base in bases:
            self.inheritance_map[base].append(class_name)
            self.reverse_inheritance_map[class_name].append(base)

        self.generic_visit(node)


def analyze_project(root_path: str) -> InheritanceAnalyzer:
    """Analiza todos los archivos Python del proyecto."""
    analyzer = InheritanceAnalyzer()

    # Excluir directorios
    exclude_dirs = {'Test', 'tests', '__pycache__', '.git', 'venv', 'env', 'docs',
                   'actores_externos', 'setup.py'}

    for py_file in Path(root_path).rglob('*.py'):
        # Saltar archivos de test y setup
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue
        if py_file.name.startswith('setup_') or py_file.name == 'ejecutar.py':
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(py_file))
                analyzer.current_file = str(py_file.relative_to(root_path))
                analyzer.visit(tree)
        except Exception as e:
            print(f"Error procesando {py_file}: {e}")

    return analyzer


def calculate_dit(class_name: str, analyzer: InheritanceAnalyzer, memo: Dict[str, int] = None) -> int:
    """
    Calcula DIT (Depth of Inheritance Tree) para una clase.
    DIT = profundidad máxima desde la clase hasta la raíz.
    """
    if memo is None:
        memo = {}

    if class_name in memo:
        return memo[class_name]

    if class_name not in analyzer.classes:
        # Clase externa (como ABCMeta, object, etc.)
        memo[class_name] = 0
        return 0

    bases = analyzer.classes[class_name]['bases']

    if not bases:
        # No tiene padres
        memo[class_name] = 0
        return 0

    # DIT = 1 + máximo DIT de los padres
    max_depth = max(calculate_dit(base, analyzer, memo) for base in bases)
    dit = 1 + max_depth
    memo[class_name] = dit
    return dit


def calculate_noc(class_name: str, analyzer: InheritanceAnalyzer) -> int:
    """
    Calcula NOC (Number of Children) para una clase.
    NOC = número de subclases directas.
    """
    return len(analyzer.inheritance_map.get(class_name, []))


def calculate_nop(class_name: str, analyzer: InheritanceAnalyzer) -> int:
    """
    Calcula NOP (Number of Parents) para una clase.
    NOP = número de clases padre directas (herencia múltiple).
    """
    if class_name not in analyzer.classes:
        return 0
    return len(analyzer.classes[class_name]['bases'])


def get_all_inherited_methods(class_name: str, analyzer: InheritanceAnalyzer, visited: Set[str] = None) -> Set[str]:
    """Obtiene todos los métodos heredados (recursivamente)."""
    if visited is None:
        visited = set()

    if class_name in visited or class_name not in analyzer.classes:
        return set()

    visited.add(class_name)
    inherited = set()

    for base in analyzer.classes[class_name]['bases']:
        if base in analyzer.classes:
            # Métodos del padre
            inherited.update(analyzer.classes[base]['methods'])
            # Métodos heredados por el padre (recursivo)
            inherited.update(get_all_inherited_methods(base, analyzer, visited))

    return inherited


def calculate_nom(class_name: str, analyzer: InheritanceAnalyzer) -> Tuple[int, int, int]:
    """
    Calcula NOM (Number of Methods).
    Retorna: (total_methods, own_methods, inherited_methods)
    """
    if class_name not in analyzer.classes:
        return 0, 0, 0

    own_methods = set(analyzer.classes[class_name]['methods'])
    inherited_methods = get_all_inherited_methods(class_name, analyzer)

    # Métodos totales = propios + heredados (sin sobreescrituras duplicadas)
    total_methods = own_methods | inherited_methods

    return len(total_methods), len(own_methods), len(inherited_methods)


def calculate_mif(analyzer: InheritanceAnalyzer) -> float:
    """
    Calcula MIF (Method Inheritance Factor) del proyecto.
    MIF = Σ(métodos_heredados) / Σ(métodos_totales)
    Indica qué proporción de métodos son heredados vs definidos.
    """
    total_inherited = 0
    total_methods = 0

    for class_name in analyzer.classes:
        nom_total, nom_own, nom_inherited = calculate_nom(class_name, analyzer)
        total_methods += nom_total
        total_inherited += nom_inherited

    if total_methods == 0:
        return 0.0

    return total_inherited / total_methods


def calculate_aif(analyzer: InheritanceAnalyzer) -> float:
    """
    Calcula AIF (Attribute Inheritance Factor) del proyecto.
    Similar a MIF pero para atributos.
    """
    total_inherited = 0
    total_attributes = 0

    for class_name in analyzer.classes:
        own_attrs = set(analyzer.classes[class_name]['attributes'])
        inherited_attrs = set()

        # Obtener atributos heredados
        for base in analyzer.classes[class_name]['bases']:
            if base in analyzer.classes:
                inherited_attrs.update(analyzer.classes[base]['attributes'])

        total_attributes += len(own_attrs | inherited_attrs)
        total_inherited += len(inherited_attrs)

    if total_attributes == 0:
        return 0.0

    return total_inherited / total_attributes


def calculate_pof(analyzer: InheritanceAnalyzer) -> float:
    """
    Calcula POF (Polymorphism Factor) del proyecto.
    POF = Σ(métodos_sobreescritos) / (Σ(métodos_totales) * NOC)
    Indica el grado de polimorfismo (sobreescritura de métodos).
    """
    total_overridden = 0
    total_possible = 0

    for class_name in analyzer.classes:
        noc = calculate_noc(class_name, analyzer)
        if noc == 0:
            continue

        # Métodos que podrían ser sobreescritos
        class_methods = set(analyzer.classes[class_name]['methods'])

        # Contar cuántos hijos sobreescriben métodos
        for child in analyzer.inheritance_map[class_name]:
            if child in analyzer.classes:
                child_methods = set(analyzer.classes[child]['methods'])
                # Métodos sobreescritos = intersección
                overridden = class_methods & child_methods
                total_overridden += len(overridden)

        total_possible += len(class_methods) * noc

    if total_possible == 0:
        return 0.0

    return total_overridden / total_possible


def generate_report(analyzer: InheritanceAnalyzer, output_file: str):
    """Genera el reporte de métricas de herencia."""

    # Calcular métricas globales
    mif = calculate_mif(analyzer)
    aif = calculate_aif(analyzer)
    pof = calculate_pof(analyzer)

    # Calcular métricas por clase
    class_metrics = []
    for class_name in sorted(analyzer.classes.keys()):
        dit = calculate_dit(class_name, analyzer)
        noc = calculate_noc(class_name, analyzer)
        nop = calculate_nop(class_name, analyzer)
        nom_total, nom_own, nom_inherited = calculate_nom(class_name, analyzer)

        class_metrics.append({
            'name': class_name,
            'dit': dit,
            'noc': noc,
            'nop': nop,
            'nom_total': nom_total,
            'nom_own': nom_own,
            'nom_inherited': nom_inherited,
            'file': analyzer.classes[class_name]['file'],
            'bases': analyzer.classes[class_name]['bases']
        })

    # Estadísticas
    total_classes = len(class_metrics)
    avg_dit = sum(m['dit'] for m in class_metrics) / total_classes if total_classes > 0 else 0
    avg_noc = sum(m['noc'] for m in class_metrics) / total_classes if total_classes > 0 else 0
    avg_nop = sum(m['nop'] for m in class_metrics) / total_classes if total_classes > 0 else 0
    max_dit = max((m['dit'] for m in class_metrics), default=0)
    max_noc = max((m['noc'] for m in class_metrics), default=0)

    # Contar jerarquías
    classes_with_inheritance = sum(1 for m in class_metrics if m['dit'] > 0 or m['noc'] > 0)
    abstract_classes = sum(1 for m in class_metrics if m['noc'] > 0)
    leaf_classes = sum(1 for m in class_metrics if m['noc'] == 0)
    multiple_inheritance = sum(1 for m in class_metrics if m['nop'] > 1)

    # Generar reporte en Markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# REPORTE DE MÉTRICAS DE HERENCIA\n")
        f.write("**Proyecto**: ISSE_Termostato\n")
        f.write(f"**Fecha**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Herramientas**: Script personalizado basado en AST de Python\n")
        f.write("**Alcance**: Código de producción (excluye tests y actores externos)\n\n")
        f.write("---\n\n")

        # RESUMEN EJECUTIVO
        f.write("## RESUMEN EJECUTIVO\n\n")
        f.write("### Visión General\n\n")
        f.write("Las métricas de herencia evalúan cómo se utiliza la herencia orientada a objetos ")
        f.write("en el diseño del sistema. Un uso adecuado de la herencia mejora la reutilización ")
        f.write("y el polimorfismo, pero el abuso puede aumentar la complejidad y el acoplamiento.\n\n")

        f.write("| Concepto | Valor | Interpretación |\n")
        f.write("|----------|-------|----------------|\n")
        f.write(f"| **Clases analizadas** | {total_classes} | Total de clases del proyecto |\n")
        f.write(f"| **Clases con herencia** | {classes_with_inheritance} | {classes_with_inheritance/total_classes*100:.1f}% del total |\n")
        f.write(f"| **Clases abstractas/base** | {abstract_classes} | Clases con hijos (NOC > 0) |\n")
        f.write(f"| **Clases hoja** | {leaf_classes} | Sin subclases |\n")
        f.write(f"| **Herencia múltiple** | {multiple_inheritance} | Clases con NOP > 1 |\n")
        f.write(f"| **DIT Promedio** | {avg_dit:.2f} | {'✅ Herencia limitada' if avg_dit <= 2 else '⚠️ Jerarquía profunda'} |\n")
        f.write(f"| **NOC Promedio** | {avg_noc:.2f} | {'✅ Jerarquía balanceada' if avg_noc <= 3 else '⚠️ Alta ramificación'} |\n")
        f.write(f"| **DIT Máximo** | {max_dit} | Profundidad máxima de herencia |\n")
        f.write(f"| **NOC Máximo** | {max_noc} | Máximo número de hijos |\n")
        f.write(f"| **MIF (Factor herencia métodos)** | {mif:.3f} | {'✅ Bajo' if mif < 0.3 else '⚠️ Alto'} |\n")
        f.write(f"| **AIF (Factor herencia atributos)** | {aif:.3f} | {'✅ Bajo' if aif < 0.3 else '⚠️ Alto'} |\n")
        f.write(f"| **POF (Factor polimorfismo)** | {pof:.3f} | {'✅ Moderado' if 0.1 <= pof <= 0.5 else '⚠️ Revisar'} |\n\n")

        # Distribuciones
        f.write("### Distribución por Profundidad de Herencia (DIT)\n\n")
        dit_dist = defaultdict(int)
        for m in class_metrics:
            if m['dit'] == 0:
                dit_dist['Sin herencia (0)'] += 1
            elif m['dit'] == 1:
                dit_dist['Herencia directa (1)'] += 1
            elif m['dit'] <= 3:
                dit_dist['Herencia moderada (2-3)'] += 1
            else:
                dit_dist['Herencia profunda (>3)'] += 1

        f.write("| Nivel | Clases | Porcentaje |\n")
        f.write("|-------|--------|------------|\n")
        for level in ['Sin herencia (0)', 'Herencia directa (1)', 'Herencia moderada (2-3)', 'Herencia profunda (>3)']:
            count = dit_dist[level]
            pct = count / total_classes * 100 if total_classes > 0 else 0
            f.write(f"| **{level}** | {count} | {pct:.1f}% |\n")

        f.write("\n---\n\n")

        # EXPLICACIÓN DE MÉTRICAS
        f.write("## 1. MÉTRICAS DE HERENCIA EXPLICADAS\n\n")

        f.write("### 1.1 DIT (Depth of Inheritance Tree)\n\n")
        f.write("**Menor es mejor (generalmente)** - Profundidad máxima desde la clase hasta la raíz del árbol de herencia.\n\n")
        f.write("```\nDIT = Distancia máxima a la raíz de la jerarquía\n```\n\n")
        f.write("- **Rango**: [0, ∞)\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0: Sin herencia\n")
        f.write("  - 1: Herencia directa (un nivel)\n")
        f.write("  - 2-3: Herencia moderada (aceptable)\n")
        f.write("  - 4-5: Herencia profunda (revisar)\n")
        f.write("  - > 5: Jerarquía muy profunda (problemático)\n\n")
        f.write("**Ventajas de DIT alto**:\n")
        f.write("- Mayor reutilización de código\n")
        f.write("- Mayor abstracción\n\n")
        f.write("**Desventajas de DIT alto**:\n")
        f.write("- Mayor complejidad conceptual\n")
        f.write("- Dificulta el entendimiento\n")
        f.write("- Mayor acoplamiento a la jerarquía\n\n")

        f.write("### 1.2 NOC (Number of Children)\n\n")
        f.write("**Moderado es mejor** - Número de subclases directas.\n\n")
        f.write("```\nNOC = número de clases que heredan directamente\n```\n\n")
        f.write("- **Rango**: [0, ∞)\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0: Clase hoja (común)\n")
        f.write("  - 1-3: Reutilización moderada (bien)\n")
        f.write("  - 4-7: Abstracción importante (revisar diseño)\n")
        f.write("  - > 7: Posible sobre-abstracción\n\n")

        f.write("### 1.3 NOP (Number of Parents)\n\n")
        f.write("**Menor es mejor** - Número de clases padre directas (indica herencia múltiple).\n\n")
        f.write("```\nNOP = número de clases padre\n```\n\n")
        f.write("- **Rango**: [0, ∞)\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0: Sin herencia\n")
        f.write("  - 1: Herencia simple (preferido)\n")
        f.write("  - 2-3: Herencia múltiple (usar con cuidado)\n")
        f.write("  - > 3: Herencia múltiple compleja (problemático)\n\n")

        f.write("### 1.4 MIF (Method Inheritance Factor)\n\n")
        f.write("**Moderado es mejor** - Factor de herencia de métodos a nivel de proyecto.\n\n")
        f.write("```\nMIF = Σ(métodos_heredados) / Σ(métodos_totales)\n```\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0-0.2: Baja reutilización (posible duplicación)\n")
        f.write("  - 0.2-0.5: Reutilización moderada (óptimo)\n")
        f.write("  - 0.5-0.8: Alta reutilización (verificar diseño)\n")
        f.write("  - 0.8-1.0: Muy alta reutilización (posible sobre-abstracción)\n\n")

        f.write("### 1.5 AIF (Attribute Inheritance Factor)\n\n")
        f.write("**Moderado es mejor** - Factor de herencia de atributos a nivel de proyecto.\n\n")
        f.write("```\nAIF = Σ(atributos_heredados) / Σ(atributos_totales)\n```\n\n")
        f.write("- Similar a MIF pero para atributos de instancia\n\n")

        f.write("### 1.6 POF (Polymorphism Factor)\n\n")
        f.write("**Moderado es mejor** - Factor de polimorfismo del proyecto.\n\n")
        f.write("```\nPOF = Σ(métodos_sobreescritos) / (Σ(métodos) × NOC)\n```\n\n")
        f.write("- **Rango**: [0, 1]\n")
        f.write("- **Interpretación**:\n")
        f.write("  - 0.0-0.1: Bajo polimorfismo (herencia no aprovechada)\n")
        f.write("  - 0.1-0.5: Polimorfismo moderado (óptimo)\n")
        f.write("  - 0.5-1.0: Alto polimorfismo (posible complejidad)\n\n")

        f.write("---\n\n")

        # JERARQUÍAS DE HERENCIA
        f.write("## 2. JERARQUÍAS DE HERENCIA DEL PROYECTO\n\n")

        # Agrupar por jerarquía
        roots = [c for c in class_metrics if c['nop'] == 0 and c['noc'] > 0]

        if roots:
            f.write("### 2.1 Árboles de Herencia\n\n")
            for root in sorted(roots, key=lambda x: x['noc'], reverse=True):
                f.write(f"#### Jerarquía: `{root['name']}`\n\n")
                f.write(f"- **Archivo**: `{root['file']}`\n")
                f.write(f"- **Hijos directos**: {root['noc']}\n")
                f.write(f"- **Métodos**: {root['nom_own']} propios\n\n")

                # Listar hijos
                children = analyzer.inheritance_map.get(root['name'], [])
                if children:
                    f.write("**Subclases**:\n\n")
                    for child in sorted(children):
                        if child in analyzer.classes:
                            child_info = next(m for m in class_metrics if m['name'] == child)
                            f.write(f"- `{child}` (DIT={child_info['dit']}, métodos={child_info['nom_own']})\n")
                    f.write("\n")

                f.write("```\n")
                f.write(f"{root['name']}\n")
                for i, child in enumerate(sorted(children)):
                    prefix = "└──" if i == len(children) - 1 else "├──"
                    f.write(f"{prefix} {child}\n")
                f.write("```\n\n")

        f.write("---\n\n")

        # TOP CLASES POR DIT
        f.write("## 3. TOP 15 CLASES CON MAYOR DIT (PROFUNDIDAD DE HERENCIA)\n\n")
        top_dit = sorted(class_metrics, key=lambda x: (x['dit'], x['name']), reverse=True)[:15]

        f.write("| # | Clase | DIT | NOC | NOP | Métodos Totales | Métodos Propios | Hereda de | Archivo |\n")
        f.write("|---|-------|-----|-----|-----|----------------|----------------|-----------|----------|\n")
        for i, m in enumerate(top_dit, 1):
            bases_str = ', '.join(m['bases']) if m['bases'] else '-'
            estado = '⚠️' if m['dit'] > 3 else '✅'
            f.write(f"| {i} | `{m['name']}` | {m['dit']} | {m['noc']} | {m['nop']} | "
                   f"{m['nom_total']} | {m['nom_own']} | {bases_str} | `{m['file']}` {estado} |\n")

        f.write("\n**Observaciones**:\n")
        deep_classes = [m for m in class_metrics if m['dit'] > 3]
        if deep_classes:
            f.write(f"- {len(deep_classes)} clases con DIT > 3 (herencia profunda)\n")
            f.write("- **Recomendación**: Revisar si la profundidad es necesaria o puede simplificarse\n\n")
        else:
            f.write("- ✅ No hay clases con herencia profunda (DIT > 3)\n\n")

        f.write("---\n\n")

        # TOP CLASES POR NOC
        f.write("## 4. TOP 15 CLASES CON MAYOR NOC (NÚMERO DE HIJOS)\n\n")
        top_noc = sorted(class_metrics, key=lambda x: (x['noc'], x['name']), reverse=True)[:15]

        f.write("Clases base con mayor número de subclases:\n\n")
        f.write("| # | Clase | NOC | DIT | Métodos | Hijos | Archivo |\n")
        f.write("|---|-------|-----|-----|---------|-------|----------|\n")
        for i, m in enumerate(top_noc, 1):
            children = analyzer.inheritance_map.get(m['name'], [])
            children_str = ', '.join(sorted(children)[:3])
            if len(children) > 3:
                children_str += f" + {len(children)-3} más"
            estado = '⚠️' if m['noc'] > 7 else '✅'
            f.write(f"| {i} | `{m['name']}` | {m['noc']} | {m['dit']} | {m['nom_own']} | "
                   f"{children_str} | `{m['file']}` {estado} |\n")

        f.write("\n**Observaciones**:\n")
        f.write(f"- {abstract_classes} clases tienen subclases (NOC > 0)\n")
        if abstract_classes > 0:
            avg_children = sum(m['noc'] for m in class_metrics if m['noc'] > 0) / abstract_classes
            f.write(f"- Promedio de hijos por clase base: {avg_children:.1f}\n")
        f.write("- **Implicación**: Cambios en clases base afectan a todas sus subclases\n\n")

        f.write("---\n\n")

        # HERENCIA MÚLTIPLE
        f.write("## 5. CLASES CON HERENCIA MÚLTIPLE (NOP > 1)\n\n")
        multi_inherit = [m for m in class_metrics if m['nop'] > 1]

        if multi_inherit:
            f.write(f"Se encontraron **{len(multi_inherit)} clases** con herencia múltiple:\n\n")
            f.write("| # | Clase | NOP | Padres | DIT | Archivo |\n")
            f.write("|---|-------|-----|--------|-----|----------|\n")
            for i, m in enumerate(sorted(multi_inherit, key=lambda x: x['nop'], reverse=True), 1):
                parents_str = ', '.join(m['bases'])
                f.write(f"| {i} | `{m['name']}` | {m['nop']} | {parents_str} | {m['dit']} | `{m['file']}` |\n")

            f.write("\n**Observaciones**:\n")
            f.write("- La herencia múltiple puede aumentar la complejidad\n")
            f.write("- **Recomendación**: Verificar que sea necesaria y esté bien documentada\n")
            f.write("- Considerar composición como alternativa en algunos casos\n\n")
        else:
            f.write("✅ No se encontraron clases con herencia múltiple en el proyecto.\n\n")

        f.write("---\n\n")

        # ANÁLISIS DE MÉTODOS HEREDADOS
        f.write("## 6. ANÁLISIS DE REUTILIZACIÓN DE MÉTODOS\n\n")
        f.write("### 6.1 Top 15 Clases por Métodos Heredados\n\n")

        classes_with_inherited = [m for m in class_metrics if m['nom_inherited'] > 0]
        top_inherited = sorted(classes_with_inherited, key=lambda x: x['nom_inherited'], reverse=True)[:15]

        if top_inherited:
            f.write("| # | Clase | Métodos Heredados | Métodos Propios | Métodos Totales | % Heredados | Archivo |\n")
            f.write("|---|-------|------------------|----------------|----------------|-------------|----------|\n")
            for i, m in enumerate(top_inherited, 1):
                pct = m['nom_inherited'] / m['nom_total'] * 100 if m['nom_total'] > 0 else 0
                f.write(f"| {i} | `{m['name']}` | {m['nom_inherited']} | {m['nom_own']} | "
                       f"{m['nom_total']} | {pct:.1f}% | `{m['file']}` |\n")
        else:
            f.write("No se encontraron clases con métodos heredados.\n")

        f.write("\n### 6.2 Métricas Globales de Reutilización\n\n")
        f.write(f"- **MIF (Method Inheritance Factor)**: {mif:.3f}\n")
        f.write(f"- **AIF (Attribute Inheritance Factor)**: {aif:.3f}\n")
        f.write(f"- **POF (Polymorphism Factor)**: {pof:.3f}\n\n")

        f.write("**Interpretación**:\n")
        if mif < 0.2:
            f.write("- ⚠️ MIF bajo: Poca reutilización de métodos, posible duplicación de código\n")
        elif mif <= 0.5:
            f.write("- ✅ MIF óptimo: Buen balance entre reutilización y especialización\n")
        else:
            f.write("- ⚠️ MIF alto: Alta dependencia de herencia, considerar composición\n")

        if pof < 0.1:
            f.write("- ⚠️ POF bajo: Poco uso de polimorfismo, herencia podría no estar justificada\n")
        elif pof <= 0.5:
            f.write("- ✅ POF óptimo: Buen uso de polimorfismo\n")
        else:
            f.write("- ⚠️ POF alto: Mucha sobreescritura, verificar complejidad\n")

        f.write("\n---\n\n")

        # LISTA COMPLETA
        f.write("## 7. LISTA COMPLETA DE CLASES\n\n")
        f.write("Todas las clases ordenadas por DIT (profundidad) descendente:\n\n")
        f.write("| # | Clase | DIT | NOC | NOP | Métodos (T/P/H) | Padres | Archivo |\n")
        f.write("|---|-------|-----|-----|-----|-----------------|--------|----------|\n")

        for i, m in enumerate(sorted(class_metrics, key=lambda x: (x['dit'], x['name']), reverse=True), 1):
            bases_str = ', '.join(m['bases']) if m['bases'] else '-'
            methods_str = f"{m['nom_total']}/{m['nom_own']}/{m['nom_inherited']}"
            f.write(f"| {i} | `{m['name']}` | {m['dit']} | {m['noc']} | {m['nop']} | "
                   f"{methods_str} | {bases_str} | `{m['file']}` |\n")

        f.write("\n**Leyenda**: T=Total, P=Propios, H=Heredados\n\n")

        f.write("---\n\n")

        # CONCLUSIONES
        f.write("## 8. CONCLUSIONES Y RECOMENDACIONES\n\n")

        f.write("### 8.1 Puntos Fuertes ⭐\n\n")
        if avg_dit <= 2:
            f.write(f"1. **Herencia limitada**: DIT promedio de {avg_dit:.2f} evita complejidad excesiva\n")
        if avg_noc <= 3:
            f.write(f"2. **Jerarquía balanceada**: NOC promedio de {avg_noc:.2f} indica diseño equilibrado\n")
        if 0.2 <= mif <= 0.5:
            f.write(f"3. **Reutilización óptima**: MIF de {mif:.3f} muestra buen balance\n")
        if multiple_inheritance == 0:
            f.write("4. **Sin herencia múltiple compleja**: Diseño simple y fácil de entender\n")

        f.write("\n### 8.2 Áreas de Mejora ⚠️\n\n")
        issues = []
        if deep_classes:
            issues.append(f"1. **Herencia profunda**: {len(deep_classes)} clases con DIT > 3")
        if max_noc > 7:
            issues.append(f"2. **Alta ramificación**: Clase con {max_noc} hijos, considerar refactorizar")
        if mif < 0.2:
            issues.append(f"3. **Baja reutilización**: MIF={mif:.3f}, posible duplicación de código")
        if mif > 0.5:
            issues.append(f"4. **Alta dependencia de herencia**: MIF={mif:.3f}, considerar composición")
        if pof < 0.1:
            issues.append(f"5. **Poco polimorfismo**: POF={pof:.3f}, herencia podría no estar justificada")

        if issues:
            for issue in issues:
                f.write(f"{issue}\n")
            f.write("\n")
        else:
            f.write("✅ No se identificaron áreas críticas de mejora\n\n")

        f.write("### 8.3 Plan de Acción Sugerido\n\n")
        f.write("#### Prioridad Alta\n")
        if deep_classes:
            f.write(f"1. Revisar las {len(deep_classes)} clases con DIT > 3\n")
        if max_noc > 7:
            f.write("2. Evaluar jerarquías con muchos hijos (considerar patrones como Strategy o State)\n")
        if not deep_classes and max_noc <= 7:
            f.write("✅ No se requieren acciones de alta prioridad\n")

        f.write("\n#### Prioridad Media\n")
        if multiple_inheritance > 0:
            f.write(f"1. Documentar las {multiple_inheritance} clases con herencia múltiple\n")
        if mif < 0.2:
            f.write("2. Identificar código duplicado y aplicar Extract Superclass\n")
        if mif > 0.5:
            f.write("2. Considerar composición sobre herencia donde sea apropiado\n")

        f.write("\n#### Prioridad Baja\n")
        f.write("1. Establecer guías de diseño para nuevas jerarquías\n")
        f.write("2. Automatizar medición de métricas de herencia en CI/CD\n")
        f.write("3. Crear diagramas UML de las jerarquías principales\n\n")

        f.write("### 8.4 Calificación General\n\n")

        # Calcular puntuación
        score = 10.0
        if avg_dit > 3:
            score -= 2
        elif avg_dit > 2:
            score -= 1

        if max_noc > 7:
            score -= 1.5

        if mif < 0.2 or mif > 0.5:
            score -= 1

        if pof < 0.1:
            score -= 0.5

        if multiple_inheritance > 3:
            score -= 1

        score = max(0, score)

        f.write(f"**Métricas de Herencia del Proyecto**: **{score:.1f}/10** ")
        if score >= 9:
            f.write("⭐⭐⭐\n\n")
        elif score >= 7:
            f.write("⭐⭐\n\n")
        elif score >= 5:
            f.write("⭐\n\n")
        else:
            f.write("⚠️\n\n")

        f.write("---\n\n")
        f.write("**Fin del Reporte de Métricas de Herencia**\n\n")
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
    analyzer = analyze_project(project_root)
    print(f"Clases encontradas: {len(analyzer.classes)}")

    # Generar reporte
    output_file = os.path.join(project_root, "docs", "reporte_metricas_herencia.md")
    generate_report(analyzer, output_file)
    print(f"Reporte generado: {output_file}")


if __name__ == "__main__":
    main()
