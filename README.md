# 🧠 Obsidian Context Agent Skill (`obsidian-context`)

[ English | [Español](README.es.md) ]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude](https://img.shields.io/badge/Platform-Antigravity%20%7C%20OpenCode%20%7C%20Claude-purple.svg)]()
[![Embeddings: Local ONNX](https://img.shields.io/badge/Embeddings-Local%20ONNX-green.svg)]()

> **Agent Skill for persistent engineering memory, tech stack analytics, and Obsidian Graph View visualization using bidirectional wikilinks (`[[wikilinks]]`).**

---

## 📌 Problem Solved

AI coding agents (Antigravity, OpenCode, Claude Code) operate with volatile memory that is lost once a session terminates. `obsidian-context` enables:

1. **Structured Project Knowledge Retention**: Captures technical decisions, libraries used, architectural trade-offs, and critical chat instructions upon completing tasks.
2. **Obsidian Graph View Exploration**: Automatically links project notes to centralized hub notes in `Technologies/[[Technology]]`, generating a visual knowledge graph across all your repositories.
3. **Tech Stack Analytics & Recommendations**: Analyzes historical usage to determine which libraries are most frequently used for specific domains (`web`, `cli`, `ai`, `networking`) and queries the user whether to reuse the proven stack or adopt a new one.
4. **Lightweight Local Embeddings (Zero PyTorch/CUDA)**: Powered by ChromaDB's `DefaultEmbeddingFunction` via native `ONNXRuntime` (`all-MiniLM-L6-v2`, 384 dimensions), eliminating the heavy ~2 GB footprint of `sentence-transformers`.

---

## 🏗️ Repository Architecture

```
obsidian-context/
├── SKILL.md                  # Standard Agent Skill definition (frontmatter, agent protocols)
├── README.md                 # English documentation and usage guide
├── README.es.md              # Spanish documentation
├── LICENSE                   # MIT License
├── pyproject.toml            # Python packaging and entry points
├── .gitignore                # Git exclusions
├── schema_knowledge.json     # JSON schema for MCP tools and agents
├── task_plan.md              # Persistent plan artifact (planning-with-files)
├── findings.md               # Architecture discoveries and research
├── progress.md               # TDD verification and session log
├── scripts/                  # Modular executable scripts (SOLID)
│   ├── save_knowledge.py     # Saves project notes and updates Technologies/ hubs
│   ├── tech_analytics.py     # Analyzes tech frequencies and recommends stacks
│   ├── search_context.py     # Local semantic search (ChromaDB + ONNXRuntime)
│   ├── sync_vault.py         # Incremental Vault <-> ChromaDB synchronizer
│   └── chat_summary_extract.py # Session notes parser
├── templates/                # Standardized Markdown templates
│   ├── project_knowledge.md  # Project summary note template
│   ├── technology_hub.md     # Technology catalog note template
│   └── postmortem.md         # Post-mortem template
├── references/
│   └── graph_and_links.md    # Obsidian Graph View semantic reference
└── tests/
    └── test_obsidian_context.py # Automated unit test suite (TDD)
```

---

## 🤖 How Coding Agents Use This Skill

### 1. Antigravity (AGY)
- **Discovery**: Registered globally via `~/.gemini/config/skills.json` (pointing to `~/.agents/skills`).
- **MCP Integration**: Exposes 4 native MCP tools in `~/.gemini/config/mcp_config.json`:
  - `tool_query_tech_stack`: Queries frequency stats and recommendations.
  - `tool_save_project_knowledge`: Saves project summaries with wikilinks.
  - `tool_semantic_search_obsidian`: Retrieves historical technical context.
  - `tool_sync_obsidian_vault`: Syncs new notes into ChromaDB.
- **Agent Lifecycle**: The agent automatically triggers semantic search during the architectural planning phase (Rule 20) and records structured summaries upon task completion.

### 2. OpenCode
- **Discovery**: Natively auto-discovered in `~/.agents/skills/obsidian-context` following the Agent Skills specification.
- **Workflow**: Guided by global directives in `~/.agents/AGENTS.md`. At project initiation, OpenCode runs `tech_analytics.py --domain <domain>` to evaluate tested stacks; at project closure, it invokes `save_knowledge.py` to persist technical assets.

### 3. Claude Code
- **Discovery**: Symlinked to `~/.claude/skills/obsidian-context`:
  ```bash
  mkdir -p ~/.claude/skills
  ln -s ~/.agents/skills/obsidian-context ~/.claude/skills/obsidian-context
  ```
- **Execution**: Can be invoked interactively via `/obsidian-context` or triggered automatically by Claude Code when analyzing historical project architecture or closing a complex task.

---

## 🚀 Installation & Setup

### 1. Clone into Agent Skills Directory
```bash
cd ~/.agents/skills
git clone https://github.com/<your-username>/obsidian-context.git
```

### 2. Install Dependencies
```bash
pip install chromadb onnxruntime mcp
```

### 3. Environment Variables (Optional)
```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/ObsidianVaults/context_ai"
export CHROMA_DB_PATH="$OBSIDIAN_VAULT_PATH/chroma_storage"
```

---

## 💻 CLI Commands

### Analyze Most Used Technologies
```bash
python3 scripts/tech_analytics.py --top 10
```

### Get Recommendations for a Domain
```bash
python3 scripts/tech_analytics.py --domain backend-rag
```

### Save Project Knowledge
```bash
python3 scripts/save_knowledge.py \
  --name "Network Analyzer" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "TDD" "Clean-Architecture" \
  --decisions "Adopted Scapy for packet crafting over raw sockets" \
  --instructions "Verify sandbox network permissions before sniffing" \
  --code "def capture(): pass"
```

### Sync Vault to ChromaDB
```bash
python3 scripts/sync_vault.py
```

### Semantic Search
```bash
python3 scripts/search_context.py --query "persistence strategies in obsidian"
```

---

## 🧪 Testing

Run the automated test suite:
```bash
python3 -m unittest discover -s tests/
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).
