#!/usr/bin/env python3
"""
search_context.py - Fast, zero-dependency search across Obsidian vault notes.
Performs keyword & metadata scoring over Markdown frontmatter, wikilinks,
tags, and body content without external vector/database dependencies.
"""

import os
import re
import glob
import json
import argparse
from typing import Optional, List, Dict, Any

try:
    from config import resolve_context_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, load_config

def _extract_note_data(filepath: str) -> Dict[str, Any]:
    """Extracts frontmatter, title, tags, and body from a markdown file."""
    data = {
        "path": filepath,
        "filename": os.path.basename(filepath),
        "title": os.path.splitext(os.path.basename(filepath))[0],
        "tags": [],
        "technologies": [],
        "strategies": [],
        "domain": "general",
        "body": ""
    }
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        yaml_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if yaml_match:
            yaml_text = yaml_match.group(1)
            body = content[yaml_match.end():]

            m_title = re.search(r'^(?:title|project):\s*["\']?([^"\'\n\r]+)["\']?', yaml_text, re.MULTILINE)
            if m_title:
                data["title"] = m_title.group(1).strip()

            m_domain = re.search(r'^(?:domain):\s*["\']?([^"\'\n\r]+)["\']?', yaml_text, re.MULTILINE)
            if m_domain:
                data["domain"] = m_domain.group(1).strip()

            m_tags = re.search(r'tags:\s*\n((?:\s*-\s*[^\n]+\n?)+)', yaml_text)
            if m_tags:
                for line in m_tags.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|["\'\[\]#]', '', line).strip()
                    if clean:
                        data["tags"].append(clean)

            m_tech = re.search(r'technologies:\s*\n((?:\s*-\s*[^\n]+\n?)+)', yaml_text)
            if m_tech:
                for line in m_tech.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|["\'\[\]]', '', line).strip()
                    if clean:
                        data["technologies"].append(clean)

            m_strat = re.search(r'strategies:\s*\n((?:\s*-\s*[^\n]+\n?)+)', yaml_text)
            if m_strat:
                for line in m_strat.group(1).splitlines():
                    clean = re.sub(r'^\s*-\s*|["\'\[\]]', '', line).strip()
                    if clean:
                        data["strategies"].append(clean)
        else:
            body = content

        h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        if h1_match and data["title"] == os.path.splitext(os.path.basename(filepath))[0]:
            data["title"] = h1_match.group(1).strip()

        data["body"] = body
    except Exception:
        pass
    return data

def search_semantic_context(
    concept_query: str,
    n_results: int = 5,
    db_path: Optional[str] = None,
    vault_path: Optional[str] = None
) -> str:
    """
    Executes a fast search across Markdown notes in obsidian-context and base vault.
    Returns standardized JSON response.
    """
    if not isinstance(concept_query, str) or not concept_query.strip():
        return json.dumps({"status": "error", "msg": "Empty or invalid query."}, separators=(',', ':'))

    context_dir = resolve_context_dir(vault_path)
    base_vault = vault_path or load_config()["vault_path"]

    query_tokens = [tok.lower() for tok in re.findall(r'\w+', concept_query) if len(tok) > 1]
    if not query_tokens:
        return json.dumps({"status": "error", "msg": "Query does not contain searchable terms."}, separators=(',', ':'))

    target_folders = ["Projects", "Decisions", "Technologies", "Strategies"]
    all_files: List[str] = []

    for fld in target_folders:
        fld_path = os.path.join(context_dir, fld)
        if os.path.exists(fld_path):
            all_files.extend(glob.glob(os.path.join(fld_path, "*.md")))

    if os.path.exists(os.path.join(base_vault, "PostMortems")):
        all_files.extend(glob.glob(os.path.join(base_vault, "PostMortems", "*.md")))

    all_files = list(set(all_files))

    if not all_files:
        return json.dumps({
            "status": "no_results",
            "msg": f"No notes found in {context_dir}",
            "data": []
        }, separators=(',', ':'))

    scored_notes = []

    for fpath in all_files:
        note = _extract_note_data(fpath)
        score = 0.0

        title_lower = note["title"].lower()
        filename_lower = note["filename"].lower()
        tags_lower = [t.lower() for t in note["tags"]]
        techs_lower = [t.lower() for t in note["technologies"]]
        strats_lower = [s.lower() for s in note["strategies"]]
        domain_lower = note["domain"].lower()
        body_lower = note["body"].lower()

        matched_tokens = 0
        for tok in query_tokens:
            tok_score = 0.0
            if tok in title_lower:
                tok_score += 10.0
            if tok in filename_lower:
                tok_score += 6.0
            if any(tok in t for t in tags_lower):
                tok_score += 8.0
            if any(tok in tc for tc in techs_lower):
                tok_score += 8.0
            if any(tok in st for st in strats_lower):
                tok_score += 6.0
            if tok in domain_lower:
                tok_score += 5.0
            
            body_count = body_lower.count(tok)
            if body_count > 0:
                tok_score += min(body_count * 1.5, 9.0)

            if tok_score > 0:
                matched_tokens += 1
                score += tok_score

        if score > 0:
            coverage_multiplier = matched_tokens / len(query_tokens)
            final_score = score * (1.0 + coverage_multiplier)

            excerpt = ""
            for tok in query_tokens:
                pos = body_lower.find(tok)
                if pos != -1:
                    start = max(0, pos - 60)
                    end = min(len(note["body"]), pos + 120)
                    excerpt = "..." + note["body"][start:end].replace("\n", " ").strip() + "..."
                    break
            if not excerpt:
                excerpt = note["body"][:150].replace("\n", " ").strip() + "..."

            scored_notes.append({
                "source": note["filename"],
                "title": note["title"],
                "path": fpath,
                "domain": note["domain"],
                "tags": note["tags"],
                "technologies": note["technologies"],
                "context": excerpt,
                "score": round(final_score, 2),
                "distance": round(1.0 / (1.0 + final_score), 4)
            })

    scored_notes.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored_notes[:n_results]

    if not top_results:
        return json.dumps({"status": "no_results", "data": []}, separators=(',', ':'))

    return json.dumps({
        "status": "success",
        "count": len(top_results),
        "data": top_results
    }, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-dependency fast search in Obsidian vault notes.")
    parser.add_argument("--query", required=True, help="Concept or search query text")
    parser.add_argument("--results", type=int, default=5, help="Number of results to retrieve")
    parser.add_argument("--db-path", type=str, default=None, help="Ignored (kept for backwards compatibility)")
    parser.add_argument("--vault", type=str, default=None, help="Custom path to Obsidian vault")
    args = parser.parse_args()

    print(search_semantic_context(
        concept_query=args.query,
        n_results=args.results,
        db_path=args.db_path,
        vault_path=args.vault
    ))
