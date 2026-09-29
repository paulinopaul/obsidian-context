#!/usr/bin/env python3
"""
config.py - Gestor de configuración centralizado para obsidian-context.
Carga las rutas desde config.json o variables de entorno, asegurando que todo
el contenido se almacene en la subcarpeta dedicada 'obsidian-context' de la bóveda.
"""

import os
import json
from typing import Dict, Any, Optional

SKILL_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_FILE = os.path.join(SKILL_ROOT, "config.json")

def load_config() -> Dict[str, Any]:
    """Carga config.json con valores predeterminados seguros."""
    defaults = {
        "vault_path": os.getenv("OBSIDIAN_VAULT_PATH", "/home/paul/Documents/ObsidianVaults/context_ai"),
        "context_folder": "obsidian-context",
        "projects_dir": "Projects",
        "technologies_dir": "Technologies",
        "strategies_dir": "Strategies",
        "chroma_dir": "chroma_storage"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
                defaults.update(user_conf)
        except Exception:
            pass
    # Variables de entorno tienen precedencia si existen
    if os.getenv("OBSIDIAN_VAULT_PATH"):
        defaults["vault_path"] = os.environ["OBSIDIAN_VAULT_PATH"]
    return defaults

def resolve_context_dir(custom_vault: Optional[str] = None) -> str:
    """
    Resuelve el directorio de almacenamiento aislado 'obsidian-context' dentro de la bóveda.
    Si custom_vault ya termina en 'obsidian-context', se utiliza directamente.
    De lo contrario, apunta a <vault_path>/obsidian-context/.
    """
    conf = load_config()
    base_vault = custom_vault or conf["vault_path"]
    folder_name = conf.get("context_folder", "obsidian-context")
    
    # Override explícito por variable de entorno
    if os.getenv("OBSIDIAN_CONTEXT_DIR"):
        return os.environ["OBSIDIAN_CONTEXT_DIR"]
        
    normalized = os.path.normpath(base_vault)
    if os.path.basename(normalized) == folder_name:
        return normalized
    return os.path.join(normalized, folder_name)

def get_projects_dir(custom_vault: Optional[str] = None) -> str:
    ctx = resolve_context_dir(custom_vault)
    conf = load_config()
    return os.path.join(ctx, conf.get("projects_dir", "Projects"))

def get_technologies_dir(custom_vault: Optional[str] = None) -> str:
    ctx = resolve_context_dir(custom_vault)
    conf = load_config()
    return os.path.join(ctx, conf.get("technologies_dir", "Technologies"))

def get_strategies_dir(custom_vault: Optional[str] = None) -> str:
    ctx = resolve_context_dir(custom_vault)
    conf = load_config()
    return os.path.join(ctx, conf.get("strategies_dir", "Strategies"))

def get_chroma_dir(custom_vault: Optional[str] = None, custom_chroma: Optional[str] = None) -> str:
    if custom_chroma:
        return custom_chroma
    if os.getenv("CHROMA_DB_PATH"):
        return os.environ["CHROMA_DB_PATH"]
    ctx = resolve_context_dir(custom_vault)
    conf = load_config()
    return os.path.join(ctx, conf.get("chroma_dir", "chroma_storage"))
