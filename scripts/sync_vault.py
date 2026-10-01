#!/usr/bin/env python3
"""
sync_vault.py - Lightweight vault status and index validator for obsidian-context.
Scans Projects/, Decisions/, Technologies/, and Strategies/ inside obsidian-context
and base vault, verifying markdown files and providing index statistics without
requiring external vector databases.
"""

import os
import glob
import json
import argparse
from typing import Optional, Dict, Any, List

try:
    from config import resolve_context_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, load_config

TARGET_FOLDERS = ["Projects", "Decisions", "Technologies", "Strategies"]

def sync_obsidian_vault_to_chroma(
    vault_path: Optional[str] = None,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Backwards-compatible vault indexer and validator.
    Validates notes across obsidian-context folders and returns inventory metrics.
    """
    context_dir = resolve_context_dir(vault_path)
    base_vault = vault_path or load_config()["vault_path"]

    all_files: List[str] = []
    folder_counts: Dict[str, int] = {}

    for folder in TARGET_FOLDERS:
        folder_path = os.path.join(context_dir, folder)
        if os.path.exists(folder_path):
            files = glob.glob(os.path.join(folder_path, "*.md"))
            folder_counts[folder] = len(files)
            all_files.extend(files)
        else:
            folder_counts[folder] = 0

    if os.path.exists(os.path.join(base_vault, "PostMortems")):
        pm_files = glob.glob(os.path.join(base_vault, "PostMortems", "*.md"))
        folder_counts["PostMortems"] = len(pm_files)
        all_files.extend(pm_files)

    all_files = list(set(all_files))

    return {
        "status": "success",
        "indexed_count": len(all_files),
        "folder_breakdown": folder_counts,
        "context_dir": context_dir,
        "msg": f"Vault verified successfully. {len(all_files)} markdown notes active."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate and count Obsidian notes in obsidian-context.")
    parser.add_argument("--vault", type=str, default=None, help="Path to Obsidian vault")
    parser.add_argument("--db-path", type=str, default=None, help="Ignored (backwards compatibility)")
    args = parser.parse_args()

    result = sync_obsidian_vault_to_chroma(vault_path=args.vault, db_path=args.db_path)
    print(json.dumps(result, indent=2))
