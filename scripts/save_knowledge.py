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
    from config import resolve_context_dir, get_projects_dir, get_decisions_dir, get_technologies_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, get_projects_dir, get_decisions_dir, get_technologies_dir, load_config

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

def save_adr(
    title: str,
    status: str = "accepted",
    context: str = "",
    decision: str = "",
    consequences: str = "",
    alternatives: str = "",
    technologies: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    vault_path: Optional[str] = None,
    language: str = "es"
) -> str:
    """
    Persists an Architecture Decision Record (ADR) under 'obsidian-context/Decisions/'.
    Generates rich Markdown with [[wikilinks]]. Supports 'es' and 'en'.
    """
    if not isinstance(title, str) or not title.strip():
        err_msg = "Invalid or empty ADR title." if language == "en" else "Título de ADR inválido o vacío."
        return json.dumps({"status": "error", "msg": err_msg}, separators=(',', ':'))

    context_dir = resolve_context_dir(vault_path)
    safe_slug = _sanitize_name(title)
    target_dir = os.path.join(context_dir, "Decisions")

    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Failed to create Decisions directory: {str(e)}"}, separators=(',', ':'))

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_{safe_slug}.md"
    filepath = os.path.join(target_dir, filename)

    technologies = technologies or []
    formatted_techs_yaml = "\n".join([f'  - "[[{t.strip()}]]"' for t in technologies if t.strip()])

    all_tags = set(tags or [])
    all_tags.update(["adr", "architecture-decision", f"status/{status.lower()}"])
    formatted_tags_yaml = "\n".join([f'  - {t}' for t in sorted(all_tags)])

    techs_body = "\n".join([f"- [[{t.strip()}]]" for t in technologies if t.strip()])

    if language == "en":
        content = f"""---
date: {today}
title: "{title}"
status: "{status}"
technologies:
{formatted_techs_yaml if formatted_techs_yaml else '  []'}
tags:
{formatted_tags_yaml}
---

# 🏛️ Architecture Decision Record: {title}

## 🎯 Context & Problem Statement
{context.strip() if context.strip() else "- Context not specified."}

## ⚖️ Considered Options & Alternatives
{alternatives.strip() if alternatives.strip() else "- No specific alternatives recorded."}

## 🏁 Decision Outcome
{decision.strip() if decision.strip() else "- Decision outcome not recorded."}

## 📈 Consequences & Trade-offs
{consequences.strip() if consequences.strip() else "- Trade-offs not specified."}

## 🛠️ Related Technologies
{techs_body if techs_body else "- None declared."}
"""
    else:
        content = f"""---
date: {today}
title: "{title}"
status: "{status}"
technologies:
{formatted_techs_yaml if formatted_techs_yaml else '  []'}
tags:
{formatted_tags_yaml}
---

# 🏛️ Registro de Decisión Arquitectónica (ADR): {title}

## 🎯 Contexto y Definición del Problema
{context.strip() if context.strip() else "- Contexto no especificado."}

## ⚖️ Opciones Consideradas y Alternativas
{alternatives.strip() if alternatives.strip() else "- No se registraron alternativas específicas."}

## 🏁 Decisión Tomada
{decision.strip() if decision.strip() else "- Decisión tomada no registrada."}

## 📈 Consecuencias y Trade-offs
{consequences.strip() if consequences.strip() else "- Trade-offs no especificados."}

## 🛠️ Tecnologías Relacionadas
{techs_body if techs_body else "- Ninguna declarada."}
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        for tech in technologies:
            if tech.strip():
                _update_technology_hub(tech.strip(), f"ADR: {title}", context_dir, language=language)

        msg = "ADR persisted successfully in obsidian-context." if language == "en" else "ADR persistido exitosamente en obsidian-context."
        return json.dumps({
            "status": "success",
            "file": filename,
            "title": title,
            "language": language,
            "path": filepath,
            "context_dir": context_dir,
            "msg": msg
        }, separators=(',', ':'))
    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Failed to write ADR: {str(e)[:150]}"}, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save project knowledge, ADRs, and technologies to Obsidian.")
    parser.add_argument("--name", default="", help="Project or ADR name")
    parser.add_argument("--title", default="", help="Alias for ADR title")
    parser.add_argument("--type", default="project", choices=["project", "adr"], help="Type of record to save (project or adr)")
    parser.add_argument("--status", default="accepted", help="Status of ADR (proposed, accepted, superseded, deprecated)")
    parser.add_argument("--domain", default="general", help="Project domain (e.g. web, cli, ai, networking)")
    parser.add_argument("--techs", nargs="*", default=[], help="List of technologies used")
    parser.add_argument("--strategies", nargs="*", default=[], help="List of strategies or design patterns applied")
    parser.add_argument("--decisions", default="", help="Technical decisions and discarded alternatives")
    parser.add_argument("--context", default="", help="Context and problem definition for ADR")
    parser.add_argument("--alternatives", default="", help="Considered alternatives for ADR")
    parser.add_argument("--consequences", default="", help="Consequences and trade-offs for ADR")
    parser.add_argument("--instructions", default="", help="Chat guidelines and learned preferences")
    parser.add_argument("--code", default="", help="Critical code snippets")
    parser.add_argument("--vault", default=None, help="Base path to Obsidian vault")
    parser.add_argument("--lang", default="es", choices=["es", "en"], help="Output language for Markdown notes (es/en)")
    args = parser.parse_args()

    record_name = args.title or args.name

    if args.type == "adr":
        res = save_adr(
            title=record_name,
            status=args.status,
            context=args.context or args.decisions,
            decision=args.decisions or args.context,
            consequences=args.consequences or args.instructions,
            alternatives=args.alternatives,
            technologies=args.techs,
            vault_path=args.vault,
            language=args.lang
        )
    else:
        res = save_project_knowledge(
            project_name=record_name,
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
