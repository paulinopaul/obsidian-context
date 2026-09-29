#!/usr/bin/env python3
"""
search_context.py - Semantic vector search across Obsidian vault notes via ChromaDB.
Implements lightweight local inference with ONNXRuntime (DefaultEmbeddingFunction)
without heavy PyTorch/CUDA dependencies, operating over obsidian-context/chroma_storage.
"""

import os
import json
import argparse
from typing import Optional, List, Dict, Any

try:
    from config import get_chroma_dir, resolve_context_dir
except ImportError:
    from obsidian_context.scripts.config import get_chroma_dir, resolve_context_dir

COLLECTION_NAME = "obsidian_memory"

def search_semantic_context(
    concept_query: str,
    n_results: int = 3,
    db_path: Optional[str] = None,
    vault_path: Optional[str] = None
) -> str:
    """
    Executes a semantic query against ChromaDB in obsidian-context.
    Returns a standardized JSON response compatible with MCP tools and CLI scripts.
    """
    if not isinstance(concept_query, str) or not concept_query.strip():
        return json.dumps({"status": "error", "msg": "Empty or invalid query."}, separators=(',', ':'))

    target_db = get_chroma_dir(custom_vault=vault_path, custom_chroma=db_path)

    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError as e:
        return json.dumps({
            "status": "error",
            "msg": f"Vector dependencies (chromadb) unavailable: {str(e)}"
        }, separators=(',', ':'))

    try:
        os.makedirs(target_db, exist_ok=True)
        client = chromadb.PersistentClient(path=target_db)
        ef = embedding_functions.DefaultEmbeddingFunction()
        
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )

        count = collection.count()
        if count == 0:
            return json.dumps({
                "status": "no_results",
                "msg": f"Vector storage at {target_db} is empty. Run sync_vault.py to index.",
                "data": []
            }, separators=(',', ':'))

        effective_n = min(n_results, count)
        results = collection.query(
            query_texts=[concept_query],
            n_results=effective_n
        )

        if not results or not results.get('documents') or not results['documents'][0]:
            return json.dumps({"status": "no_results", "data": []}, separators=(',', ':'))

        formatted_results = []
        docs = results['documents'][0]
        metas = results['metadatas'][0] if results.get('metadatas') else [{}] * len(docs)
        distances = results['distances'][0] if results.get('distances') else [0.0] * len(docs)

        for doc, meta, distance in zip(docs, metas, distances):
            formatted_results.append({
                "source": meta.get('source', 'Unknown') if meta else 'Unknown',
                "context": doc,
                "distance": round(distance, 4)
            })

        return json.dumps({
            "status": "success",
            "chroma_dir": target_db,
            "data": formatted_results
        }, separators=(',', ':'))

    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Vector database error: {str(e)[:150]}"}, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic search in Obsidian ChromaDB.")
    parser.add_argument("--query", required=True, help="Concept or semantic query text")
    parser.add_argument("--results", type=int, default=3, help="Number of results to retrieve")
    parser.add_argument("--db-path", type=str, default=None, help="Custom path to ChromaDB storage")
    parser.add_argument("--vault", type=str, default=None, help="Custom path to Obsidian vault")
    args = parser.parse_args()

    print(search_semantic_context(
        concept_query=args.query,
        n_results=args.results,
        db_path=args.db_path,
        vault_path=args.vault
    ))
