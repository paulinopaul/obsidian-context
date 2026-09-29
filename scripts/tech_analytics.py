#!/usr/bin/env python3
"""
tech_analytics.py - Analizador de frecuencia de stack tecnológico y recomendador contextual.
Permite a los modelos y usuarios analizar qué tecnologías se han usado más en la bóveda
y formular sugerencias para nuevos proyectos (reutilizar pila probada vs. explorar alternativas).
"""

import os
import re
import glob
import json
import argparse
from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional

DEFAULT_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/home/paul/Documents/ObsidianVaults/context_ai")

def _extract_metadata_from_file(filepath: str) -> Dict[str, Any]:
    """Extrae metadatos básicos y wikilinks de una nota Markdown."""
    meta: Dict[str, Any] = {"technologies": [], "strategies": [], "domain": "general", "tags": []}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parsear bloque YAML frontmatter
        yaml_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if yaml_match:
            yaml_text = yaml_match.group(1)
            # Dominio
            domain_match = re.search(r"domain:\s*[\"']?([^\"'\n]+)[\"']?", yaml_text)
            if domain_match:
                meta["domain"] = domain_match.group(1).strip()

            # Tecnologías en YAML
            tech_block = re.search(r"technologies:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if tech_block:
                for line in tech_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]]', '', line).strip()
                    if clean:
                        meta["technologies"].append(clean)

            # Estrategias en YAML
            strat_block = re.search(r"strategies:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if strat_block:
                for line in strat_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]]', '', line).strip()
                    if clean:
                        meta["strategies"].append(clean)

            # Tags en YAML
            tags_block = re.search(r"tags:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if tags_block:
                for line in tags_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]#]', '', line).strip()
                    if clean:
                        meta["tags"].append(clean)

            # Si no hubo tecnologías explícitas, usar tags técnicos como fallback
            if not meta["technologies"] and meta["tags"]:
                generic_tags = {"configuration", "architecture", "project-knowledge", "tech-stack"}
                for t in meta["tags"]:
                    if t.lower() not in generic_tags:
                        meta["technologies"].append(t)

        # Fallback a extracción de wikilinks en sección de Stack
        tech_section = re.search(r"## 🛠️ Stack Tecnológico Utilizado(.*?)(?:##|\Z)", content, re.DOTALL)
        if tech_section:
            wikilinks = re.findall(r"\[\[([^\]]+)\]\]", tech_section.group(1))
            for wl in wikilinks:
                if wl not in meta["technologies"]:
                    meta["technologies"].append(wl.strip())

    except Exception:
        pass
    return meta

def analyze_technology_stack(vault_path: Optional[str] = None) -> Dict[str, Any]:
    """Analiza la frecuencia global de tecnologías en todas las notas de proyectos de la bóveda."""
    vault = vault_path or os.getenv("OBSIDIAN_VAULT_PATH", DEFAULT_VAULT_PATH)
    project_files = glob.glob(os.path.join(vault, "Projects", "*.md"))
    # Añadimos PostMortems como histórico complementario
    project_files.extend(glob.glob(os.path.join(vault, "PostMortems", "*.md")))

    total_projects = len(project_files)
    tech_counter: Counter = Counter()
    domain_map: Dict[str, List[str]] = defaultdict(list)
    strategy_counter: Counter = Counter()

    for pfile in project_files:
        meta = _extract_metadata_from_file(pfile)
        domain = meta.get("domain", "general")
        for tech in meta["technologies"]:
            tech_counter[tech] += 1
            domain_map[domain].append(tech)
        for strat in meta["strategies"]:
            strategy_counter[strat] += 1

    ranking = [{"tech": tech, "count": count, "frequency": round(count / max(total_projects, 1), 2)} 
               for tech, count in tech_counter.most_common()]

    strategies_ranking = [{"strategy": s, "count": c} for s, c in strategy_counter.most_common()]

    return {
        "status": "success",
        "total_projects": total_projects,
        "technologies": ranking,
        "strategies": strategies_ranking,
        "domains": {dom: dict(Counter(techs).most_common(5)) for dom, techs in domain_map.items()}
    }

def recommend_stack_for_domain(domain: str, vault_path: Optional[str] = None) -> Dict[str, Any]:
    """Recomienda tecnologías basándose en proyectos previos del mismo dominio."""
    stats = analyze_technology_stack(vault_path=vault_path)
    domain_techs = stats.get("domains", {}).get(domain, {})

    if domain_techs:
        sorted_techs = list(domain_techs.keys())
        msg = f"Para el dominio '{domain}', las tecnologías más empleadas históricamente son: {', '.join(sorted_techs[:3])}."
    else:
        # Fallback a tecnologías globales más frecuentes
        sorted_techs = [item["tech"] for item in stats.get("technologies", [])[:5]]
        msg = f"No hay proyectos previos registrados para el dominio '{domain}'. Pila global más utilizada: {', '.join(sorted_techs[:3])}."

    return {
        "domain": domain,
        "top_technologies": sorted_techs,
        "recommendation_prompt": f"{msg} ¿Deseas utilizar esta pila probada o experimentar con una alternativa tecnológica?",
        "alternatives_note": "Si deseas explorar una nueva tecnología, especifícala para añadirla al grafo tras validar compatibilidad."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analítica y recomendación de tecnologías en Obsidian.")
    parser.add_argument("--top", type=int, default=10, help="Número de tecnologías top a mostrar")
    parser.add_argument("--domain", type=str, default=None, help="Consultar recomendación para un dominio específico")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON crudo")
    args = parser.parse_args()

    if args.domain:
        rec = recommend_stack_for_domain(args.domain)
        if args.json:
            print(json.dumps(rec, indent=2))
        else:
            print(f"\n📊 Recomendación de Stack para '{args.domain}':")
            print(f"Top Tecnologías: {', '.join(rec['top_technologies'])}")
            print(f"Propuesta: {rec['recommendation_prompt']}\n")
    else:
        stats = analyze_technology_stack()
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(f"\n📊 Estadísticas de Stack Tecnológico ({stats['total_projects']} proyectos analizados):")
            print("="*60)
            for item in stats["technologies"][:args.top]:
                print(f" - {item['tech']}: {item['count']} usos ({int(item['frequency'] * 100)}%)")
            print("="*60 + "\n")
