#!/usr/bin/env python3
"""
save_knowledge.py - Persists engineering project knowledge notes into Obsidian.
Generates structured Markdown notes with bidirectional [[wikilinks]] and maintains
catalog hub notes in Technologies/ within the dedicated 'obsidian-context' folder
for visual rendering in Obsidian Graph View. Supports English and Spanish output.
"""

import os
import re
import json
import argparse
from datetime import datetime
from typing import List, Optional, Dict, Any

try:
    from config import resolve_context_dir, get_projects_dir, get_technologies_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, get_projects_dir, get_technologies_dir, load_config

def _sanitize_name(name: str) -> str:
    """Sanitizes project and file names by stripping unsafe characters and preventing path traversal."""
    if not isinstance(name, str):
        return "unnamed_project"
    cleaned = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name).strip()
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned if cleaned else "default_project"

def _update_technology_hub(tech_name: str, project_name: str, context_dir: str, language: str = "es") -> None:
    """Creates or updates the technology hub note in Technologies/ inside obsidian-context."""
    safe_tech = _sanitize_name(tech_name)
    tech_dir = os.path.join(context_dir, "Technologies")
    os.makedirs(tech_dir, exist_ok=True)
    tech_file = os.path.join(tech_dir, f"{safe_tech}.md")
    
    today = datetime.now().strftime("%Y-%m-%d")
    project_link = f"- [[{project_name}]]"
    
    if os.path.exists(tech_file):
        try:
            with open(tech_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Increment usage_count
            count_match = re.search(r'usage_count:\s*(\d+)', content)
            new_count = (int(count_match.group(1)) + 1) if count_match else 1
            content = re.sub(r'usage_count:\s*\d+', f'usage_count: {new_count}', content)
            content = re.sub(r'last_used:\s*\S+', f'last_used: {today}', content)
            
            # Append project back-link under the relevant section
            if project_link not in content:
                if "## 🔗 Projects Where Used" in content:
                    content = content.replace(
                        "## 🔗 Projects Where Used",
                        f"## 🔗 Projects Where Used\n{project_link}"
                    )
                elif "## 🔗 Proyectos Donde se ha Utilizado" in content:
                    content = content.replace(
                        "## 🔗 Proyectos Donde se ha Utilizado",
                        f"## 🔗 Proyectos Donde se ha Utilizado\n{project_link}"
                    )
                else:
                    heading = "## 🔗 Projects Where Used" if language == "en" else "## 🔗 Proyectos Donde se ha Utilizado"
                    content += f"\n{heading}\n{project_link}\n"
                    
            with open(tech_file, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass
    else:
        # Create initial technology note according to chosen language
        if language == "en":
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

# 🔧 Technology: {tech_name}

## 📋 Purpose & Description
Technical catalog sheet and usage history for {tech_name}.

## 🔗 Projects Where Used
{project_link}

## 💡 Best Practices & Key Patterns
- Document optimal versions and configurations here.

## ⚠️ Known Issues & Pitfalls
- None reported yet.
"""
        else:
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
    vault_path: Optional[str] = None,
    language: str = "es"
) -> str:
    """
    Persists project knowledge into Obsidian under 'obsidian-context/Projects/'.
    Generates rich Markdown with [[wikilinks]]. Supports 'es' (Spanish) and 'en' (English).
    Returns a serialized JSON response with status, file, and path.
    """
    if not isinstance(project_name, str) or not project_name.strip():
        err_msg = "Invalid or empty project name." if language == "en" else "Nombre de proyecto inválido o vacío."
        return json.dumps({"status": "error", "msg": err_msg}, separators=(',', ':'))

    context_dir = resolve_context_dir(vault_path)
    safe_slug = _sanitize_name(project_name)
    target_dir = os.path.join(context_dir, "Projects")

    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Failed to create Projects directory: {str(e)}"}, separators=(',', ':'))

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_{safe_slug}.md"
    filepath = os.path.join(target_dir, filename)

    # Format wikilinks and YAML tags
    formatted_techs_yaml = "\n".join([f'  - "[[{t.strip()}]]"' for t in technologies if t.strip()])
    formatted_strats_yaml = "\n".join([f'  - "[[{s.strip()}]]"' for s in strategies if s.strip()])
    
    all_tags = set(tags or [])
    all_tags.update(["project-knowledge", "tech-stack", f"domain/{_sanitize_name(domain)}"])
    formatted_tags_yaml = "\n".join([f'  - {t}' for t in sorted(all_tags)])

    # Language-aware body formatting
    if language == "en":
        techs_body = "\n".join([f"- [[{t.strip()}]]: Technology stack component." for t in technologies if t.strip()])
        strats_body = "\n".join([f"- [[{s.strip()}]]: Applied architectural strategy or design pattern." for s in strategies if s.strip()])
        
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

# 📌 Technical Summary: {project_name}

## 🛠️ Technology Stack Used
{techs_body if techs_body else "- No specific technologies declared."}

## 📐 Strategies & Design Patterns Applied
{strats_body if strats_body else "- No specific strategies declared."}

## 💡 Design Decisions & Trade-offs
{decisions if decisions.strip() else "- No decisions recorded."}

## 📋 Key Chat Instructions & Learned Guidelines
{instructions_learned if instructions_learned.strip() else "- No additional guidelines recorded."}

## 💻 Critical Code Snippets
```text
{code_snippets if code_snippets.strip() else "# No code snippets saved"}
```
"""
    else:
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

        # Update or create technology hubs in Technologies/
        for tech in technologies:
            if tech.strip():
                _update_technology_hub(tech.strip(), project_name, context_dir, language=language)

        success_msg = "Project knowledge persisted successfully in obsidian-context." if language == "en" else "Conocimiento del proyecto persistido exitosamente en obsidian-context."
        return json.dumps({
            "status": "success",
            "file": filename,
            "project": project_name,
            "language": language,
            "path": filepath,
            "context_dir": context_dir,
            "msg": success_msg
        }, separators=(',', ':'))

    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Failed to write file: {str(e)[:150]}"}, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save project knowledge and technologies to Obsidian.")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--domain", default="general", help="Project domain (e.g. web, cli, ai, networking)")
    parser.add_argument("--techs", nargs="*", default=[], help="List of technologies used")
    parser.add_argument("--strategies", nargs="*", default=[], help="List of strategies or design patterns applied")
    parser.add_argument("--decisions", default="", help="Technical decisions and discarded alternatives")
    parser.add_argument("--instructions", default="", help="Chat guidelines and learned preferences")
    parser.add_argument("--code", default="", help="Critical code snippets")
    parser.add_argument("--vault", default=None, help="Base path to Obsidian vault")
    parser.add_argument("--lang", default="es", choices=["es", "en"], help="Output language for Markdown notes (es/en)")
    args = parser.parse_args()

    res = save_project_knowledge(
        project_name=args.name,
        domain=args.domain,
        technologies=args.techs,
        strategies=args.strategies,
        decisions=args.decisions,
        instructions_learned=args.instructions,
        code_snippets=args.code,
        vault_path=args.vault,
        language=args.lang
    )
    print(res)
