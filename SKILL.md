---
name: obsidian-context
description: "Persistent engineering memory, tech stack analytics, and bidirectional linking in Obsidian. Generates structured project summaries and technology hubs with [[wikilinks]] for the Obsidian Graph View, featuring local ONNX vector embeddings and bilingual support (EN/ES)."
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep"
metadata:
  version: "1.1.0"
---

# Obsidian Context Skill

Modular skill to govern persistent engineering knowledge in Obsidian for AI coding agents. Transforms architectural decisions, code patterns, chat directives, and technology choices into an interconnected Knowledge Graph using `[[wikilinks]]`.

---

## 📂 Vault Directory & Storage Layout

The skill reads `config.json` at its root directory (`~/.agents/skills/obsidian-context/config.json`) to resolve the vault path.
All generated artifacts are strictly stored in the dedicated `obsidian-context/` subfolder inside the user's Obsidian vault:

```
Your-Obsidian-Vault/
└── obsidian-context/
    ├── Projects/         <-- Completed project summaries ([[tech]], [[strategy]])
    ├── Technologies/     <-- Technology catalog hub notes for Obsidian Graph View
    ├── Strategies/       <-- Architectural patterns and guidelines
    └── chroma_storage/   <-- Local ChromaDB vector database (ONNX)
```

---

## 🤖 AI Agent Operational Protocol (Antigravity, OpenCode, Claude Code)

Any AI model operating in an agentic coding environment must follow this lifecycle when `obsidian-context` is present:

### 1. Task Initiation & Review Confirmation
When the agent starts a new task or recognizes the presence of `obsidian-context`, **it must proactively ask the user whether to perform a historical context review or skip it**:
- **Spanish Interaction**:
  > *"He detectado la skill `obsidian-context`. ¿Deseas hacer una revisión del contexto histórico y stack tecnológico recomendado para este trabajo, o prefieres omitir la revisión?"*
- **English Interaction**:
  > *"I detected the `obsidian-context` skill. Would you like to review historical context and recommended tech stack for this task, or would you prefer to skip this review?"*

**If the user approves the review:**
1. Run semantic search:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "<task description>"
   ```
2. Run stack recommendation for the domain:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/tech_analytics.py --domain "<domain>" --lang "<es|en>"
   ```
3. Present the historical stack to the user and confirm whether to reuse it or test an alternative.

---

### 2. Task Closure & Language Confirmation
Upon completing implementation and passing all unit tests, **the agent must prompt the user to confirm the language for the saved Markdown notes**:
- **Spanish Interaction**:
  > *"¿Deseas que el resumen técnico y las notas del proyecto se guarden en español o prefieres en inglés?"*
- **English Interaction**:
  > *"Would you like the technical summary and project notes saved in English or Spanish?"*

**After confirmation:**
1. Execute `save_knowledge.py` with the selected language flag (`--lang es` or `--lang en`):
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py \
     --name "<ProjectName>" \
     --domain "<domain>" \
     --techs "Tech1" "Tech2" \
     --strategies "Strategy1" "Strategy2" \
     --decisions "<tradeoffs and discarded alternatives>" \
     --instructions "<chat instructions and preferences learned>" \
     --code "<critical code snippet>" \
     --lang "<es|en>"
   ```
2. Trigger incremental vector synchronization:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/sync_vault.py
   ```

---

## 🛠️ Available Scripts & Tools

- `scripts/config.py`: Centralized configuration manager (`config.json` and environment variables).
- `scripts/save_knowledge.py`: Generates structured project notes in `Projects/` and updates hub notes in `Technologies/` in Spanish or English.
- `scripts/tech_analytics.py`: Computes tech frequency metrics and produces bilingual domain recommendations.
- `scripts/search_context.py`: Performs local semantic queries using ChromaDB and ONNXRuntime (`DefaultEmbeddingFunction`).
- `scripts/sync_vault.py`: Incrementally indexes vault notes into ChromaDB.
- `scripts/chat_summary_extract.py`: Parses raw chat recaps into structured JSON for storage.
