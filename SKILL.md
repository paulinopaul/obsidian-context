---
name: obsidian-context
description: "Persistent engineering memory, architecture decision records (ADRs), and bidirectional linking in Obsidian. Generates structured notes with [[wikilinks]] for the Obsidian Graph View using fast, zero-dependency Markdown parsing."
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep"
metadata:
  version: "2.0.0"
---

# Obsidian Context Skill (v2.0 - Zero Friction)

Persists and retrieves technical memory, Architecture Decision Records (ADRs), and stack patterns directly in Obsidian without external database daemons or heavy vector dependencies. All notes are pure Markdown with standard YAML frontmatter and `[[wikilinks]]`, rendering natively in the Obsidian Graph View.

---

## 📂 Vault Directory & Storage Layout

Reads `~/.agents/skills/obsidian-context/config.json` to resolve the vault path. Notes are organized strictly inside `obsidian-context/`:

```
Your-Obsidian-Vault/
└── obsidian-context/
    ├── Decisions/        <-- Architecture Decision Records (ADRs: problem, choices, outcome, tradeoffs)
    ├── Projects/         <-- Milestone & project summaries with [[tech]] links
    ├── Technologies/     <-- Technology catalog hub notes for Obsidian Graph View
    └── Strategies/       <-- Architectural patterns and engineering guidelines
```

---

## ⚡ Operational Protocol (Zero Friction)

### 1. No Bureaucracy (Zero Interruption)
- **DO NOT** block the chat with greetings, confirmation prompts, or language questions (*never* ask "He detectado obsidian-context..." or "¿Prefieres inglés o español?").
- Match the user's active conversation language automatically (`es` or `en`).

### 2. Context Retrieval (On-Demand or Quiet Lookup)
- When the user asks about previous architectural decisions or stack patterns (or when formulating a plan for an established domain), search the vault:
  ```bash
  python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "<keywords>"
  ```
- Alternatively, read notes directly from `Decisions/` or `Projects/` using file tools.
- Incorporate findings directly into your plan or response without ceremonies.

### 3. Persisting Architectural Decisions (ADRs)
When a key architectural decision, technology selection, or significant refactoring tradeoff is made (or when the user requests it):
```bash
python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py \
  --type adr \
  --title "<Title of Decision>" \
  --status "accepted" \
  --context "<Problem statement and forces>" \
  --decisions "<Chosen solution and justification>" \
  --alternatives "<Discarded options and why>" \
  --consequences "<Tradeoffs, positive and negative impacts>" \
  --techs "Tech1" "Tech2" \
  --lang "<es|en>"
```

### 4. Persisting Project / Milestone Summaries
When completing a major project or when requested by the user:
```bash
python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py \
  --name "<ProjectName>" \
  --domain "<domain>" \
  --techs "Tech1" "Tech2" \
  --strategies "Clean Architecture" "TDD" \
  --decisions "<Key tradeoffs>" \
  --instructions "<Critical learned preferences>" \
  --code "<Critical snippet>" \
  --lang "<es|en>"
```

---

## 🛠️ Tooling & Scripts

- `scripts/search_context.py`: Fast, zero-dependency keyword & metadata search across all vault notes.
- `scripts/save_knowledge.py`: Generates structured ADRs in `Decisions/`, summaries in `Projects/`, and maintains hub notes in `Technologies/`.
- `scripts/tech_analytics.py`: Analyzes stack frequency and patterns across existing notes.
- `scripts/sync_vault.py`: Validates note integrity and provides vault statistics.
