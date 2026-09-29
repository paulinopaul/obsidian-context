#!/usr/bin/env python3
"""
sync_vault.py - Sincronizador de la bóveda de Obsidian hacia ChromaDB.
Indexa de forma diferencial e incremental las notas de Projects/, Technologies/ y PostMortems/
almacenadas en la carpeta 'obsidian-context' de la bóveda utilizando embeddings locales ONNX.
"""

import os
import glob
import json
import argparse
from typing import Optional, Dict, Any, List

try:
    from config import resolve_context_dir, get_chroma_dir, load_config
except ImportError:
    from obsidian_context.scripts.config import resolve_context_dir, get_chroma_dir, load_config

COLLECTION_NAME = "obsidian_memory"
TARGET_FOLDERS = ["Projects", "Technologies", "Strategies"]

def sync_obsidian_vault_to_chroma(
    vault_path: Optional[str] = None,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Escanea las carpetas principales de obsidian-context y sincroniza/indexa
    todas las notas hacia ChromaDB.
    """
    context_dir = resolve_context_dir(vault_path)
    base_vault = vault_path or load_config()["vault_path"]
    chroma_dir = get_chroma_dir(vault_path, db_path)

    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError as e:
        return {
            "status": "error",
            "msg": f"Dependencias vectoriales (chromadb) no disponibles: {str(e)}",
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
        # 1. Carpetas dentro de obsidian-context
        for folder in TARGET_FOLDERS:
            folder_path = os.path.join(context_dir, folder)
            if os.path.exists(folder_path):
                all_files.extend(glob.glob(os.path.join(folder_path, "*.md")))

        # 2. Carpetas históricas del vault base si existen
        if os.path.exists(os.path.join(base_vault, "PostMortems")):
            all_files.extend(glob.glob(os.path.join(base_vault, "PostMortems", "*.md")))

        all_files = list(set(all_files))

        if not all_files:
            return {
                "status": "success",
                "msg": f"No se encontraron notas en {context_dir} para indexar.",
                "indexed_count": 0,
                "context_dir": context_dir
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
            "context_dir": context_dir,
            "chroma_dir": chroma_dir,
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
