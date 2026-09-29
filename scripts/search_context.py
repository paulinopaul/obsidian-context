#!/usr/bin/env python3
"""
search_context.py - Búsqueda semántica vectorial en la bóveda de Obsidian mediante ChromaDB.
Implementa inferencia local liviana con ONNXRuntime (DefaultEmbeddingFunction) sin
dependencias invasivas de PyTorch o sentence-transformers.
"""

import os
import json
import argparse
from typing import Optional, List, Dict, Any

DEFAULT_CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "/home/paul/Documents/ObsidianVaults/context_ai/chroma_storage")
COLLECTION_NAME = "obsidian_memory"

def search_semantic_context(concept_query: str, n_results: int = 3, db_path: Optional[str] = None) -> str:
    """
    Ejecuta consulta semántica sobre la base vectorial de Obsidian.
    Retorna JSON estandarizado compatible con herramientas MCP y scripts CLI.
    """
    if not isinstance(concept_query, str) or not concept_query.strip():
        return json.dumps({"status": "error", "msg": "Consulta vacía o inválida."}, separators=(',', ':'))

    target_db = db_path or os.getenv("CHROMA_DB_PATH", DEFAULT_CHROMA_PATH)

    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError as e:
        return json.dumps({
            "status": "error",
            "msg": f"Dependencias vectoriales (chromadb) no disponibles: {str(e)}"
        }, separators=(',', ':'))

    try:
        os.makedirs(target_db, exist_ok=True)
        client = chromadb.PersistentClient(path=target_db)
        # DefaultEmbeddingFunction utiliza ONNX nativo (all-MiniLM-L6-v2) sin requerir torch ni sentence-transformers
        ef = embedding_functions.DefaultEmbeddingFunction()
        
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )

        count = collection.count()
        if count == 0:
            return json.dumps({
                "status": "no_results",
                "msg": "La base vectorial está vacía. Ejecute sync_vault.py para indexar la bóveda.",
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

        return json.dumps({"status": "success", "data": formatted_results}, separators=(',', ':'))

    except Exception as e:
        return json.dumps({"status": "error", "msg": f"Fallo en la base vectorial: {str(e)[:150]}"}, separators=(',', ':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Búsqueda semántica en Obsidian ChromaDB.")
    parser.add_argument("--query", required=True, help="Concepto o consulta semántica")
    parser.add_argument("--results", type=int, default=3, help="Número de resultados a recuperar")
    parser.add_argument("--db-path", type=str, default=None, help="Ruta alternativa de ChromaDB")
    args = parser.parse_args()

    print(search_semantic_context(concept_query=args.query, n_results=args.results, db_path=args.db_path))
