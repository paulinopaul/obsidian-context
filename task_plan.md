# Task Plan: Obsidian Context Agent Skill Development

## Goal
Desarrollar y empaquetar una Agent Skill modular y robusta (`obsidian-context`) para gestión de memoria persistente, grafos de stack tecnológico e interoperabilidad MCP/CLI, dejándola lista para su publicación en GitHub.

## Next Step
Repositorio local preparado y validado para publicación en GitHub (`git remote add origin <url>`).

## Current Phase
Phase 5: Delivery & GitHub Preparation (Complete)

## Phases

### Phase 1: Requerimientos, Descubrimiento y Auditoría
- [x] Auditar código existente en `obsidian_rag` y bóveda de Obsidian.
- [x] Extraer contexto semántico histórico y auditoría de repositorios GitHub.
- [x] Identificar cuello de botella de dependencias (`sentence-transformers` vs ONNX).
- **Status:** complete

### Phase 2: Diseño Arquitectónico y Modular (SOLID)
- [x] Definir estructura canónica de skill (`SKILL.md`, `scripts/`, `templates/`, `references/`, `tests/`).
- [x] Diseñar semántica de enlaces bidireccionales (`[[wikilinks]]`) para el Obsidian Graph View.
- [x] Diseñar motor de analítica y recomendación de tecnologías (`tech_analytics.py`).
- **Status:** complete

### Phase 3: Implementación Test-Driven (TDD)
- [x] Escribir suite de pruebas unitarias exhaustiva (`tests/test_obsidian_context.py`).
- [x] Implementar `save_knowledge.py` con sanitización defensiva y hubs en `Technologies/`.
- [x] Implementar `tech_analytics.py` con cálculo de frecuencia y recomendador por dominio.
- [x] Implementar `search_context.py` con inferencia local liviana en ONNXRuntime.
- [x] Implementar `sync_vault.py` para sincronización incremental bóveda <-> ChromaDB.
- [x] Implementar `chat_summary_extract.py` para captura de directrices de chat.
- **Status:** complete

### Phase 4: Integración MCP y Regresiones
- [x] Habilitar compatibilidad dual MCP v1 (`FastMCP`) y MCP v2 (`MCPServer`) en `mcp_server.py`.
- [x] Actualizar `search_executor.py` para usar el motor robusto ONNX.
- [x] Ejecutar suite de pruebas completa (17/17 tests pasando sin regresiones).
- [x] Indexar la bóveda real de Obsidian y verificar generación de notas.
- **Status:** complete

### Phase 5: Empaquetado y Preparación para GitHub
- [x] Crear `LICENSE` (MIT).
- [x] Crear `.gitignore` defensivo.
- [x] Crear `pyproject.toml` estándar.
- [x] Documentar `README.md` exhaustivo con guías de instalación para Antigravity, OpenCode y Claude Code.
- [x] Inicializar repositorio Git local con commit inicial.
- **Status:** complete

## Key Questions

1. **¿Cómo evitar la descarga pesada de PyTorch (~2GB) para embeddings locales?**
   - *Respuesta:* Utilizando `DefaultEmbeddingFunction` de ChromaDB, la cual opera nativamente sobre `ONNXRuntime` (`all-MiniLM-L6-v2`) en CPU local con latencia de milisegundos.
2. **¿Cómo hacer que los modelos recuerden tecnologías y directrices sin saturar tokens?**
   - *Respuesta:* Extrayendo un resumen estructurado al cierre con wikilinks `[[tech]]` y notas maestras en `Technologies/`, consultables mediante `tech_analytics.py`.

## Decisions Made

| Decisión | Justificación |
|----------|---------------|
| Migrar a estructura Agent Skill (`~/.agents/skills/obsidian-context`) | Alineación con estándares multiplataforma (Antigravity, OpenCode, Claude Code). |
| Descartar `sentence-transformers` en favor de `DefaultEmbeddingFunction` (ONNX) | Elimina fragilidad de dependencias, CUDA y consumo excesivo de memoria. |
| Wikilinks bidireccionales en Obsidian | Permite visualización orgánica del stack y relaciones en el Obsidian Graph View. |
| Compatibilidad dual MCP v1 / v2 | Garantiza que `mcp_server.py` no falle ante cambios de versión del SDK de FastMCP. |

## Errors Encountered

| Error | Intento | Resolución |
|-------|---------|------------|
| `No module named sentence_transformers` | 1 | Migrado a `DefaultEmbeddingFunction` de ChromaDB que corre sobre `onnxruntime` preinstalado. |
| `FastMCP renamed to MCPServer in mcp 2.x` | 1 | Implementada importación condicional dual `try/except` en `mcp_server.py`. |
| `AssertionError: 'no_results' != 'error'` en test legado | 1 | Ajustado mock en `test_obsidian_rag.py` para simular ausencia real del módulo chromadb. |
