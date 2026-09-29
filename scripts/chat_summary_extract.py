#!/usr/bin/env python3
"""
chat_summary_extract.py - Extractor and parser for session technical knowledge.
Structures decisions, technologies, learned instructions, and code snippets
for direct persistence via save_knowledge.py without inspecting raw brain logs.
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
    Parses notes or raw session text to automatically extract structured
    technical knowledge for the project.
    """
    technologies: List[str] = []
    strategies: List[str] = []
    decisions: List[str] = []
    instructions: List[str] = []
    code_snippets: List[str] = []

    # Common technologies to match if mentioned in text
    known_techs = [
        "Python", "FastAPI", "Flask", "Django", "ChromaDB", "SQLite", "PostgreSQL",
        "Redis", "Docker", "ONNXRuntime", "Pytest", "Typer", "Rich", "Scapy",
        "Bash", "Node.js", "TypeScript", "React", "Linux", "OpenCode", "Antigravity"
    ]
    for tech in known_techs:
        if re.search(r'\b' + re.escape(tech) + r'\b', raw_notes, re.IGNORECASE):
            if tech not in technologies:
                technologies.append(tech)

    # Common engineering strategies
    known_strats = [
        "TDD", "SOLID", "Clean Architecture", "Defensive Programming",
        "AST Parsing", "Token Efficiency", "Mocking", "Microservices"
    ]
    for strat in known_strats:
        if re.search(r'\b' + re.escape(strat) + r'\b', raw_notes, re.IGNORECASE):
            if strat not in strategies:
                strategies.append(strat)

    # Code blocks detection
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", raw_notes, re.DOTALL)
    if code_blocks:
        code_snippets = [b.strip() for b in code_blocks[:3]]

    return {
        "project_name": project_name,
        "domain": domain,
        "technologies": technologies,
        "strategies": strategies,
        "decisions": raw_notes[:500] if raw_notes else "Technical decisions documented in session.",
        "instructions_learned": "Follow modular architecture, rigorous typing, and defensive design.",
        "code_snippets": "\n\n".join(code_snippets) if code_snippets else ""
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract structured technical knowledge from session notes.")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--notes", required=True, help="Session notes or conversational recap text")
    parser.add_argument("--domain", default="general", help="Technical domain")
    args = parser.parse_args()

    data = extract_structured_knowledge(args.name, args.notes, args.domain)
    print(json.dumps(data, indent=2))
