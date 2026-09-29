# Findings & Research: Obsidian Context Skill

## Descubrimientos Técnicos Clave

### 1. Inferencia Local y Embeddings en ChromaDB
- **Hallazgo:** `sentence-transformers` arrastra PyTorch, Triton y herramientas de compilación CUDA (~2.2 GB de dependencias en Linux).
- **Solución Óptima:** ChromaDB incluye soporte directo para `DefaultEmbeddingFunction` basado en `onnxruntime`, que ejecuta el modelo `all-MiniLM-L6-v2` (384 dimensiones) en CPU local sin GPU ni librerías pesadas.

### 2. Estructura de Bóveda y Grafo en Obsidian
- **Carpetas Estandarizadas:**
  - `Projects/`: Registros de proyectos finalizados con frontmatter YAML y sección de directrices de chat.
  - `Technologies/`: Fichas de catálogo (`[[Python]]`, `[[FastAPI]]`, etc.) con contador de proyectos (`usage_count`) y enlaces retrospectivos.
  - `PostMortems/`: Documentos de análisis post-mortem de hitos de ingeniería.
  - `chroma_storage/`: Almacén persistente local de ChromaDB.
- **Obsidian Graph View:** Al vincular tecnologías mediante `[[NombreTecnologia]]` tanto en el frontmatter como en el cuerpo Markdown, Obsidian genera automáticamente nodos centrales que permiten visualizar la constelación de dependencias entre todos los proyectos del desarrollador.

### 3. Evolución del SDK de MCP
- En `mcp` 2.x, `mcp.server.fastmcp.FastMCP` fue renombrado a `mcp.server.mcpserver.MCPServer`.
- Se requiere encapsulamiento con `try/except` para mantener soporte en sistemas con `mcp<2` y `mcp>=2`.
