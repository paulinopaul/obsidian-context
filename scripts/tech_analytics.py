#!/usr/bin/env python3
"""
tech_analytics.py - Technology stack frequency analyzer and contextual recommender.
Enables AI models and developers to analyze which technologies have been used most
frequently inside the 'obsidian-context' folder and suggests stacks for upcoming tasks.
"""

import os
import re
import glob
import json
import argparse
from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional

try:
    from config import resolve_context_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, load_config

def _extract_metadata_from_file(filepath: str) -> Dict[str, Any]:
    """Extracts frontmatter metadata and wikilinks from a Markdown note."""
    meta: Dict[str, Any] = {"technologies": [], "strategies": [], "domain": "general", "tags": []}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse YAML frontmatter block
        yaml_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if yaml_match:
            yaml_text = yaml_match.group(1)
            # Extract domain
            domain_match = re.search(r"domain:\s*[\"']?([^\"'\n]+)[\"']?", yaml_text)
            if domain_match:
                meta["domain"] = domain_match.group(1).strip()

            # Extract technologies from YAML
            tech_block = re.search(r"technologies:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if tech_block:
                for line in tech_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]]', '', line).strip()
                    if clean:
                        meta["technologies"].append(clean)

            # Extract strategies from YAML
            strat_block = re.search(r"strategies:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if strat_block:
                for line in strat_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]]', '', line).strip()
                    if clean:
                        meta["strategies"].append(clean)

            # Extract tags from YAML
            tags_block = re.search(r"tags:\s*\n((?:\s*-\s*[^\n]+\n?)+)", yaml_text)
            if tags_block:
                for line in tags_block.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|[\"\'\[\]#]', '', line).strip()
                    if clean:
                        meta["tags"].append(clean)

            # Fallback to technical tags if explicit technologies are absent
            if not meta["technologies"] and meta["tags"]:
                generic_tags = {"configuration", "architecture", "project-knowledge", "tech-stack"}
                for t in meta["tags"]:
                    if t.lower() not in generic_tags:
                        meta["technologies"].append(t)

        # Fallback to extracting wikilinks under Technology Stack heading (supports EN & ES)
        tech_section = re.search(r"## 🛠️ (?:Stack Tecnológico Utilizado|Technology Stack Used)(.*?)(?:##|\Z)", content, re.DOTALL)
        if tech_section:
            wikilinks = re.findall(r"\[\[([^\]]+)\]\]", tech_section.group(1))
            for wl in wikilinks:
                if wl not in meta["technologies"]:
                    meta["technologies"].append(wl.strip())

    except Exception:
        pass
    return meta

def analyze_technology_stack(vault_path: Optional[str] = None) -> Dict[str, Any]:
    """Analyzes the global frequency of technologies across obsidian-context project notes."""
    context_dir = resolve_context_dir(vault_path)
    base_vault = vault_path or load_config()["vault_path"]

    project_files = glob.glob(os.path.join(context_dir, "Projects", "*.md"))
    # Include base vault notes if they exist
    if os.path.exists(os.path.join(base_vault, "Projects")):
        project_files.extend(glob.glob(os.path.join(base_vault, "Projects", "*.md")))
    if os.path.exists(os.path.join(base_vault, "PostMortems")):
        project_files.extend(glob.glob(os.path.join(base_vault, "PostMortems", "*.md")))

    project_files = list(set(project_files))
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
        "context_dir": context_dir,
        "technologies": ranking,
        "strategies": strategies_ranking,
        "domains": {dom: dict(Counter(techs).most_common(5)) for dom, techs in domain_map.items()}
    }

def recommend_stack_for_domain(domain: str, vault_path: Optional[str] = None, language: str = "es") -> Dict[str, Any]:
    """Recommends technologies based on historical usage in the same domain. Supports EN & ES."""
    stats = analyze_technology_stack(vault_path=vault_path)
    domain_techs = stats.get("domains", {}).get(domain, {})

    if domain_techs:
        sorted_techs = list(domain_techs.keys())
        if language == "en":
            msg = f"For the '{domain}' domain, the most frequently used technologies are: {', '.join(sorted_techs[:3])}."
            prompt = f"{msg} Would you like to use this proven stack or explore an alternative technology?"
            alt = "If you wish to explore a new technology, specify it so we can evaluate it and record it in the graph."
        else:
            msg = f"Para el dominio '{domain}', las tecnologías más empleadas históricamente son: {', '.join(sorted_techs[:3])}."
            prompt = f"{msg} ¿Deseas utilizar esta pila probada o experimentar con una alternativa tecnológica?"
            alt = "Si deseas explorar una nueva tecnología, especifícala para añadirla al grafo tras validar compatibilidad."
    else:
        # Fallback to global ranking
        sorted_techs = [item["tech"] for item in stats.get("technologies", [])[:5]]
        if language == "en":
            msg = f"No previous projects recorded specifically for '{domain}'. Global top technologies: {', '.join(sorted_techs[:3])}."
            prompt = f"{msg} Would you like to use this proven stack or explore an alternative technology?"
            alt = "Specify any preferred new library to adopt."
        else:
            msg = f"No hay proyectos previos registrados para el dominio '{domain}'. Pila global más utilizada: {', '.join(sorted_techs[:3])}."
            prompt = f"{msg} ¿Deseas utilizar esta pila probada o experimentar con una alternativa tecnológica?"
            alt = "Especifica cualquier librería preferida para adoptarla."

    return {
        "domain": domain,
        "language": language,
        "top_technologies": sorted_techs,
        "recommendation_prompt": prompt,
        "alternatives_note": alt
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze technology stack and generate recommendations in Obsidian.")
    parser.add_argument("--top", type=int, default=10, help="Number of top technologies to display")
    parser.add_argument("--domain", type=str, default=None, help="Query recommendation for a specific domain")
    parser.add_argument("--vault", type=str, default=None, help="Path to Obsidian vault")
    parser.add_argument("--lang", default="es", choices=["es", "en"], help="Output language for recommendations (es/en)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if args.domain:
        rec = recommend_stack_for_domain(args.domain, vault_path=args.vault, language=args.lang)
        if args.json:
            print(json.dumps(rec, indent=2))
        else:
            header = f"Stack Recommendation for '{args.domain}':" if args.lang == "en" else f"Recomendación de Stack para '{args.domain}':"
            tech_label = "Top Technologies:" if args.lang == "en" else "Top Tecnologías:"
            prop_label = "Proposal:" if args.lang == "en" else "Propuesta:"
            print(f"\n📊 {header}")
            print(f"{tech_label} {', '.join(rec['top_technologies'])}")
            print(f"{prop_label} {rec['recommendation_prompt']}\n")
    else:
        stats = analyze_technology_stack(vault_path=args.vault)
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            header = f"Technology Stack Statistics ({stats['total_projects']} projects analyzed):" if args.lang == "en" else f"Estadísticas de Stack Tecnológico ({stats['total_projects']} proyectos analizados):"
            uses_label = "uses" if args.lang == "en" else "usos"
            print(f"\n📊 {header}")
            print("="*60)
            for item in stats["technologies"][:args.top]:
                print(f" - {item['tech']}: {item['count']} {uses_label} ({int(item['frequency'] * 100)}%)")
            print("="*60 + "\n")
