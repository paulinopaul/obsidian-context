#!/usr/bin/env python3
"""
chat_summary_extract.py - Extractor y formateador de conocimiento técnico de sesiones.
Estructura decisiones, tecnologías, directrices aprendidas y fragmentos de código
para su persistencia directa a través de save_knowledge.py sin requerir acceso al brain crudo.
"""

import re
import json
import argparse
from typing import Dict, List, Any

def extract_structured_knowledge(
    project_name: str,
    raw_notes: str,
    domain: str = "general"
) -> Dict[str, Any]:
    """
    Parsea notas o texto libre de la sesión para estructurar automáticamente
    el conocimiento técnico del proyecto.
    """
    technologies: List[str] = []
    strategies: List[str] = []
    decisions: List[str] = []
    instructions: List[str] = []
    code_snippets: List[str] = []

    # Detección de tecnologías comunes si aparecen en el texto
    known_techs = [
        "Python", "FastAPI", "Flask", "Django", "ChromaDB", "SQLite", "PostgreSQL",
        "Redis", "Docker", "ONNXRuntime", "Pytest", "Typer", "Rich", "Scapy",
        "Bash", "Node.js", "TypeScript", "React", "Linux", "OpenCode", "Antigravity"
    ]
    for tech in known_techs:
        if re.search(r'\b' + re.escape(tech) + r'\b', raw_notes, re.IGNORECASE):
            if tech not in technologies:
                technologies.append(tech)

    # Detección de estrategias de ingeniería
    known_strats = [
        "TDD", "SOLID", "Clean Architecture", "Defensive Programming",
        "AST Parsing", "Token Efficiency", "Mocking", "Microservices"
    ]
    for strat in known_strats:
        if re.search(r'\b' + re.escape(strat) + r'\b', raw_notes, re.IGNORECASE):
            if strat not in strategies:
                strategies.append(strat)

    # Detección de bloques de código
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", raw_notes, re.DOTALL)
    if code_blocks:
        code_snippets = [b.strip() for b in code_blocks[:3]]

    return {
        "project_name": project_name,
        "domain": domain,
        "technologies": technologies,
        "strategies": strategies,
        "decisions": raw_notes[:500] if raw_notes else "Decisiones técnicas documentadas en sesión.",
        "instructions_learned": "Seguimiento de directrices rigurosas y arquitectura modular.",
        "code_snippets": "\n\n".join(code_snippets) if code_snippets else ""
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraer conocimiento técnico estructurado de notas de sesión.")
    parser.add_argument("--name", required=True, help="Nombre del proyecto")
    parser.add_argument("--notes", required=True, help="Texto o notas de la sesión de trabajo")
    parser.add_argument("--domain", default="general", help="Dominio técnico")
    args = parser.parse_args()

    data = extract_structured_knowledge(args.name, args.notes, args.domain)
    print(json.dumps(data, indent=2))
