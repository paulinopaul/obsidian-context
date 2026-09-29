#!/usr/bin/env python3
"""
save_knowledge.py - Guarda el conocimiento técnico persistente de proyectos en Obsidian.
Genera notas estructuradas con enlaces bidireccionales [[wikilinks]] y mantiene
las notas de catálogo en Technologies/ para visualización en el Obsidian Graph View.
"""

import os
import re
import json
import argparse
from datetime import datetime
from typing import List, Optional, Dict, Any

DEFAULT_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/home/paul/Documents/ObsidianVaults/context_ai")
PROJECTS_DIR = "Projects"
TECHNOLOGIES_DIR = "Technologies"
STRATEGIES_DIR = "Strategies"

def _sanitize_name(name: str) -> str:
    """Sanitiza nombres de proyectos y archivos eliminando caracteres peligrosos y path traversal."""
    if not isinstance(name, str):
        return "unnamed_project"
    cleaned = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name).strip()
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned if cleaned else "default_project"

def _update_technology_hub(tech_name: str, project_name: str, vault_path: str) -> None:
    """Crea o actualiza la nota de catálogo para una tecnología en Technologies/."""
    safe_tech = _sanitize_name(tech_name)
    tech_dir = os.path.join(vault_path, TECHNOLOGIES_DIR)
    os.makedirs(tech_dir, exist_ok=True)
    tech_file = os.path.join(tech_dir, f"{safe_tech}.md")
    
    today = datetime.now().strftime("%Y-%m-%d")
    project_link = f"- [[{project_name}]]"
    
    if os.path.exists(tech_file):
        try:
            with open(tech_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Actualizar usage_count
            count_match = re.search(r'usage_count:\s*(\d+)', content)
            new_count = (int(count_match.group(1)) + 1) if count_match else 1
            content = re.sub(r'usage_count:\s*\d+', f'usage_count: {new_count}', content)
            content = re.sub(r'last_used:\s*\S+', f'last_used: {today}', content)
            
            # Agregar link del proyecto si no existe ya
            if project_link not in content:
                if "## 🔗 Proyectos Donde se ha Utilizado" in content:
                    content = content.replace(
                        "## 🔗 Proyectos Donde se ha Utilizado",
                        f"## 🔗 Proyectos Donde se ha Utilizado\n{project_link}"
                    )
                else:
                    content += f"\n## 🔗 Proyectos Donde se ha Utilizado\n{project_link}\n"
                    
            with open(tech_file, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass
    else:
        # Crear nota inicial
        initial_content = f"""---
technology: "{tech_name}"
category: "general"
first_used: {today}
last_used: {today}
usage_count: 1
status: "active"
tags:
  - technology-hub
  - tech-catalog
---

# 🔧 Tecnología: {tech_name}

## 📋 Descripción y Propósito
Ficha técnica y registro histórico de uso de la tecnología {tech_name}.

## 🔗 Proyectos Donde se ha Utilizado
{project_link}

## 💡 Mejores Prácticas y Patrones Clave
- Documentar versiones y configuraciones óptimas aquí.

## ⚠️ Errores Conocidos y Advertencias
- Ninguno registrado hasta el momento.
"""
        with open(tech_file, "w", encoding="utf-8") as f:
            f.write(initial_content)

def save_project_knowledge(
    project_name: str,
    domain: str,
    technologies: List[str],
    strategies: List[str],
    decisions: str,
    instructions_learned: str,
    code_snippets: str,
    tags: Optional[List[str]] = None,
    vault_path: Optional[str] = None
) -> str:
    """
    Persiste el conocimiento de un proyecto en Obsidian con formato enriquecido y wikilinks.
    Retorna un JSON serializado con status, file y detalles.
    """
    if not isinstance(project_name, str) or not project_name.strip():
        return json.dumps({"status": "error", "msg": "Nombre de proyecto inválido o vacío."}, separators=(',', ':'))

    vault = vault_path or os.getenv("OBSIDIAN_VAULT_PATH", DEFAULT_VAULT_PATH)
    safe_slug = _sanitize_name(project_name)
    target_dir = os.path.join(vault, PROJECTS_DIR)

    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Fallo al crear directorio Projects: {str(e)}"}, separators=(',', ':'))

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_{safe_slug}.md"
    filepath = os.path.join(target_dir, filename)

    # Formateo de wikilinks y YAML
    formatted_techs_yaml = "\n".join([f'  - "[[{t.strip()}]]"' for t in technologies if t.strip()])
    formatted_strats_yaml = "\n".join([f'  - "[[{s.strip()}]]"' for s in strategies if s.strip()])
    
    all_tags = set(tags or [])
    all_tags.update(["project-knowledge", "tech-stack", f"domain/{_sanitize_name(domain)}"])
    formatted_tags_yaml = "\n".join([f'  - {t}' for t in sorted(all_tags)])

    techs_body = "\n".join([f"- [[{t.strip()}]]: Componente técnico del stack." for t in technologies if t.strip()])
    strats_body = "\n".join([f"- [[{s.strip()}]]: Estrategia o patrón de diseño aplicado." for s in strategies if s.strip()])

    content = f"""---
date: {today}
project: "{project_name}"
domain: "{domain}"
technologies:
{formatted_techs_yaml if formatted_techs_yaml else '  []'}
strategies:
{formatted_strats_yaml if formatted_strats_yaml else '  []'}
status: "completed"
tags:
{formatted_tags_yaml}
---

# 📌 Resumen Técnico: {project_name}

## 🛠️ Stack Tecnológico Utilizado
{techs_body if techs_body else "- Sin tecnologías específicas declaradas."}

## 📐 Estrategias y Patrones Aplicados
{strats_body if strats_body else "- Sin estrategias específicas declaradas."}

## 💡 Decisiones de Diseño y Alternativas Descartadas
{decisions if decisions.strip() else "- Sin decisiones registradas."}

## 📋 Directrices e Indicaciones del Chat Recordadas
{instructions_learned if instructions_learned.strip() else "- Sin directrices adicionales registradas."}

## 💻 Fragmentos Críticos de Código / Patrones
```text
{code_snippets if code_snippets.strip() else "# Sin fragmentos de código guardados"}
```
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # Actualizar fichas de tecnologías en Technologies/
        for tech in technologies:
            if tech.strip():
                _update_technology_hub(tech.strip(), project_name, vault)

        return json.dumps({
            "status": "success",
            "file": filename,
            "project": project_name,
            "path": filepath,
            "msg": "Conocimiento del proyecto persistido exitosamente en Obsidian."
        }, separators=(',', ':'))

    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Fallo al escribir archivo: {str(e)[:150]}"}, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guardar resumen de proyecto y tecnologías en Obsidian.")
    parser.add_argument("--name", required=True, help="Nombre del proyecto")
    parser.add_argument("--domain", default="general", help="Dominio del proyecto (ej: web, cli, ai, networking)")
    parser.add_argument("--techs", nargs="*", default=[], help="Lista de tecnologías utilizadas")
    parser.add_argument("--strategies", nargs="*", default=[], help="Lista de estrategias o patrones utilizados")
    parser.add_argument("--decisions", default="", help="Decisiones técnicas y alternativas descartadas")
    parser.add_argument("--instructions", default="", help="Directrices e indicaciones aprendidas del chat")
    parser.add_argument("--code", default="", help="Fragmentos de código críticos")
    args = parser.parse_args()

    res = save_project_knowledge(
        project_name=args.name,
        domain=args.domain,
        technologies=args.techs,
        strategies=args.strategies,
        decisions=args.decisions,
        instructions_learned=args.instructions,
        code_snippets=args.code
    )
    print(res)
