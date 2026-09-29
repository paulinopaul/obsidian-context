# 🧠 Obsidian Context Agent Skill (`obsidian-context`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude](https://img.shields.io/badge/Platform-Antigravity%20%7C%20OpenCode%20%7C%20Claude-purple.svg)]()
[![Embeddings: Local ONNX](https://img.shields.io/badge/Embeddings-Local%20ONNX-green.svg)]()

> **Agent Skill para la persistencia del conocimiento de proyectos, análisis de stack tecnológico y visualización en el Grafo de Obsidian mediante enlaces bidireccionales (`[[wikilinks]]`).**

---

## 📌 ¿Qué problema resuelve?

Durante las sesiones de programación en agentes de IA (Antigravity, OpenCode, Claude Code), el contexto volátil se pierde al cerrar el chat. `obsidian-context` permite:

1. **Persistencia Estructurada de Cierre**: Guarda un resumen técnico del proyecto (tecnologías empleadas, estrategias aplicadas, decisiones de arquitectura y directrices dadas en el chat) sin necesidad de inspeccionar logs crudos de ejecución.
2. **Visualización en el Obsidian Graph View**: Al conectar automáticamente cada nota de proyecto con fichas técnicas en `Technologies/[[Tecnología]]`, se genera una red visual que muestra la constelación de herramientas utilizadas en todos tus proyectos.
3. **Analítica de Stack y Recomendación**: Permite a los agentes analizar cuáles son las tecnologías más utilizadas históricamente para un tipo de tarea (`web`, `cli`, `ai`, etc.) y consultar al usuario si desea reutilizar la pila probada o explorar una alternativa.
4. **Inferencia Vectorial Liviana (Cero PyTorch/CUDA)**: Utiliza `DefaultEmbeddingFunction` de ChromaDB sobre `ONNXRuntime` local (`all-MiniLM-L6-v2`, 384 dimensiones), eliminando los ~2GB de dependencias pesadas de `sentence-transformers`.

---

## 🏗️ Arquitectura del Repositorio

```
obsidian-context/
├── SKILL.md                  # Especificación estándar Agent Skill (frontmatter, hooks, roles)
├── README.md                 # Documentación técnica completa y guía de uso
├── LICENSE                   # Licencia MIT
├── pyproject.toml            # Empaquetado estándar Python
├── .gitignore                # Reglas de exclusión de compilados y caches
├── schema_knowledge.json     # Esquema JSON estructurado para herramientas MCP/agentes
├── task_plan.md              # Artefacto de planificación persistente (planning-with-files)
├── findings.md               # Registro de descubrimientos de arquitectura
├── progress.md               # Bitácora de ejecución y resultados de pruebas
├── scripts/                  # Scripts ejecutables modulares (SOLID)
│   ├── save_knowledge.py     # Guarda notas de proyecto y actualiza fichas en Technologies/
│   ├── tech_analytics.py     # Análisis de frecuencias de stack y recomendador por dominio
│   ├── search_context.py     # Búsqueda semántica vectorial local (ChromaDB + ONNX)
│   ├── sync_vault.py         # Sincronizador incremental Bóveda <-> ChromaDB
│   └── chat_summary_extract.py # Extractor estructurado de notas de sesión
├── templates/                # Plantillas Markdown estructuradas
│   ├── project_knowledge.md  # Salida persistente de proyectos (Stack, Decisiones, Código)
│   ├── technology_hub.md     # Ficha técnica de catálogo en Technologies/
│   └── postmortem.md         # Plantilla estándar para notas de Post-Mortem
├── references/
│   └── graph_and_links.md    # Guía de interoperabilidad con Obsidian Graph View
└── tests/
    └── test_obsidian_context.py # Suite de pruebas automatizadas TDD
```

---

## 🚀 Instalación y Configuración

### 1. Clonar en el directorio de Agent Skills
```bash
# Directorio estándar global de Agent Skills
cd ~/.agents/skills
git clone https://github.com/tu-usuario/obsidian-context.git
```

### 2. Instalar Dependencias
```bash
pip install chromadb onnxruntime mcp
```

### 3. Variables de Entorno (Opcionales)
Configura en tu `~/.bashrc` o `~/.zshrc`:
```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/ObsidianVaults/context_ai"
export CHROMA_DB_PATH="$OBSIDIAN_VAULT_PATH/chroma_storage"
```
*(Si no se configuran, el sistema asumirá las rutas por defecto).*

---

## 🛠️ Integración con Plataformas de Agentes

### Antigravity / Gemini CLI
Agrega la skill en `~/.gemini/config/skills.json`:
```json
{
  "entries": [
    { "path": "~/.agents/skills" }
  ]
}
```

Para exponer las herramientas MCP en `~/.gemini/config/mcp_config.json`:
```json
{
  "mcpServers": {
    "obsidian-context": {
      "command": "python3",
      "args": ["-m", "mcp_server"]
    }
  }
}
```

### OpenCode
La skill es descubierta automáticamente al residir en `~/.agents/skills/obsidian-context`.

---

## 💻 Uso por Línea de Comandos (CLI)

### Analizar Tecnologías Más Utilizadas
```bash
python3 scripts/tech_analytics.py --top 10
```

### Recomendar Stack para un Dominio
```bash
python3 scripts/tech_analytics.py --domain agent-skills
```

### Guardar Resumen de Conocimiento de un Proyecto
```bash
python3 scripts/save_knowledge.py \
  --name "Network Analyzer" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "TDD" "Clean-Architecture" \
  --decisions "Adopción de Scapy para parsing de tramas Ethernet" \
  --instructions "Validar permisos en sandbox antes de capturar tráfico" \
  --code "def capture(): pass"
```

### Sincronizar Bóveda hacia ChromaDB
```bash
python3 scripts/sync_vault.py
```

### Búsqueda Semántica Vectorial
```bash
python3 scripts/search_context.py --query "estrategias de persistencia en obsidian"
```

---

## 🧪 Pruebas Automatizadas (TDD)

El proyecto incluye una suite de pruebas rigurosa que cubre sanitización de rutas, extracción de metadatos, concurrencia en ChromaDB e inferencia ONNX:

```bash
python3 -m unittest discover -s tests/
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).
