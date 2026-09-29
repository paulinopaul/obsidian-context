#!/usr/bin/env python3
"""
sync_vault.py - Sincronizador de la bóveda de Obsidian hacia ChromaDB.
Indexa de forma diferencial e incremental las notas de Projects/, PostMortems/ y Technologies/
utilizando embeddings locales ONNX sin requerir librerías pesadas ni GPUs.
"""

import os
import glob
import json
import argparse
from typing import Optional, Dict, Any, List

DEFAULT_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/home/paul/Documents/ObsidianVaults/context_ai")
DEFAULT_CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "/home/paul/Documents/ObsidianVaults/context_ai/chroma_storage")
COLLECTION_NAME = "obsidian_memory"
TARGET_FOLDERS = ["Projects", "PostMortems", "Technologies"]

def sync_obsidian_vault_to_chroma(
    vault_path: Optional[str] = None,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Escanea las carpetas principales de la bóveda y sincroniza/indexa
    todas las notas hacia ChromaDB.
    """
    vault = vault_path or os.getenv("OBSIDIAN_VAULT_PATH", DEFAULT_VAULT_PATH)
    chroma_dir = db_path or os.getenv("CHROMA_DB_PATH", DEFAULT_CHROMA_PATH)

    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError as e:
        return {
            "status": "error",
            "msg": f"Dependencias vectoriales (chromadb) no disponibles: {str(e)}",
            "indexed_count": 0
        }

    if not os.path.exists(vault):
        return {
            "status": "error",
            "msg": f"La ruta de la bóveda no existe: {vault}",
            "indexed_count": 0
        }

    try:
        os.makedirs(chroma_dir, exist_ok=True)
        client = chromadb.PersistentClient(path=chroma_dir)
        ef = embedding_functions.DefaultEmbeddingFunction()
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )

        all_files: List[str] = []
        for folder in TARGET_FOLDERS:
            folder_path = os.path.join(vault, folder)
            if os.path.exists(folder_path):
                all_files.extend(glob.glob(os.path.join(folder_path, "*.md")))

        if not all_files:
            return {
                "status": "success",
                "msg": "No se encontraron notas en las carpetas objetivo para indexar.",
                "indexed_count": 0
            }

        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Dict[str, Any]] = []

        for fpath in all_files:
            fname = os.path.basename(fpath)
            parent_folder = os.path.basename(os.path.dirname(fpath))
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                if content.strip():
                    ids.append(f"{parent_folder}_{fname}")
                    documents.append(content)
                    metadatas.append({
                        "source": fname,
                        "folder": parent_folder,
                        "path": fpath
                    })
            except Exception:
                continue

        if ids:
            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

        return {
            "status": "success",
            "indexed_count": len(ids),
            "collection_total": collection.count(),
            "msg": f"Sincronización completada. {len(ids)} notas indexadas en ChromaDB."
        }

    except Exception as e:
        return {
            "status": "error",
            "msg": f"Error durante la sincronización: {str(e)[:150]}",
            "indexed_count": 0
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincronizar notas de Obsidian hacia ChromaDB.")
    parser.add_argument("--vault", type=str, default=None, help="Ruta a la bóveda de Obsidian")
    parser.add_argument("--db-path", type=str, default=None, help="Ruta al almacenamiento ChromaDB")
    args = parser.parse_args()

    result = sync_obsidian_vault_to_chroma(vault_path=args.vault, db_path=args.db_path)
    print(json.dumps(result, indent=2))
