# 🧠 Obsidian Context Agent Skill (`obsidian-context`) v2.0

[ English | [Español](README.es.md) ]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude Code | Any Agent](https://img.shields.io/badge/Platform-Universal%20Agent%20Skill-purple.svg)]()
[![Dependencies: Zero](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Stdlib)-brightgreen.svg)]()

> **Frictionless Agent Skill for persistent engineering memory, Architecture Decision Records (ADRs), tech stack analytics, and Obsidian Graph View visualization using bidirectional wikilinks (`[[wikilinks]]`). 100% self-contained in pure Markdown.**

---

## 📌 Problem Solved

AI coding agents operate with volatile session context that vanishes once a task concludes. `obsidian-context` solves this without bloated runtime overhead:

1. **Architecture Decision Records (ADRs)**: Captures problem statements, considered alternatives, decisions, and trade-offs into `Decisions/` notes.
2. **Project Knowledge Retention**: Saves structured summaries of completed projects, architectural patterns, and critical guidelines into `Projects/`.
3. **Obsidian Graph View Exploration**: Automatically links project notes and ADRs to centralized hub notes in `Technologies/[[Technology]]`, rendering a knowledge graph across all your repositories.
4. **Zero-Friction Agent Protocol**: No intrusive chat confirmations or language selection gates. The agent acts quietly or on-demand, automatically matching the conversation language.
5. **Zero External Dependencies**: Operates entirely with the Python 3 standard library (`os`, `re`, `glob`, `json`, `math`). No ChromaDB, no ONNXRuntime, and no external daemons required.
6. **Clean Vault Isolation**: All generated artifacts reside strictly within the dedicated `obsidian-context/` subfolder in your Obsidian vault.

---

## 📂 Vault Directory Layout

Create an `obsidian-context` folder in your Obsidian vault and specify your vault's path in `config.json`:

```
Your-Obsidian-Vault/
└── obsidian-context/                 <-- Isolated workspace in your Obsidian Vault
    ├── Decisions/                    <-- Architecture Decision Records (ADRs)
    ├── Projects/                     <-- Completed project summaries ([[tech]] links)
    ├── Technologies/                 <-- Technology catalog hubs for Obsidian Graph View
    └── Strategies/                   <-- Architectural patterns and guidelines
```

---

## 🏗️ Repository Architecture

```
obsidian-context/                     <-- Skill directory (~/.agents/skills/obsidian-context)
├── config.json                       <-- Active vault & directory configuration (gitignored)
├── config.example.json               <-- Template configuration
├── SKILL.md                          <-- Standard Agent Skill definition (v2.0 Zero Friction)
├── README.md                         <-- English documentation
├── README.es.md                      <-- Spanish documentation
├── LICENSE                           <-- MIT License
├── pyproject.toml                    <-- Standard Python packaging (zero external deps)
├── schema_knowledge.json             <-- JSON schema for agent tooling
├── scripts/                          <-- Lightweight modular scripts (Python standard library)
│   ├── config.py                     <-- Configuration loader
│   ├── save_knowledge.py             <-- Saves ADRs, project notes, and updates Technologies/ hubs
│   ├── search_context.py             <-- Fast zero-dependency keyword & metadata search (<20ms)
│   ├── tech_analytics.py             <-- Analyzes tech frequencies and recommends stacks
│   ├── sync_vault.py                 <-- Vault note validator and status metrics
│   └── chat_summary_extract.py       <-- Session notes parser
├── templates/                        <-- Markdown templates with frontmatter and wikilinks
│   ├── adr.en.md                     <-- ADR template (English)
│   ├── adr.es.md                     <-- ADR template (Spanish)
│   ├── project_knowledge.en.md       <-- Project summary template (English)
│   ├── project_knowledge.es.md       <-- Project summary template (Spanish)
│   ├── technology_hub.en.md          <-- Technology hub note template (English)
│   ├── technology_hub.es.md          <-- Technology hub note template (Spanish)
│   ├── postmortem.en.md              <-- Post-mortem template (English)
│   └── postmortem.es.md              <-- Post-mortem template (Spanish)
├── references/
│   ├── graph_and_links.md            <-- Obsidian Graph View semantic reference (English)
│   └── graph_and_links.es.md         <-- Obsidian Graph View semantic reference (Spanish)
└── tests/
    └── test_obsidian_context.py       <-- Automated unit test suite (100% passing)
```

---

## 🤖 Universal Agent Directive (System Prompt Snippet)

Add this directive to your agent's system prompt or global rules file (e.g. `AGENTS.md`, `CLAUDE.md`, or rules block):

```markdown
### Memory & Knowledge Governance (obsidian-context)
When the `obsidian-context` skill is available:
- **Zero Friction:** Do NOT interrupt the user with protocol questions or language prompts.
- **On-Demand or Contextual Lookup:** When the user asks about past decisions or stack patterns, query the vault quietly:
  `python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "<keywords>"`
- **Architecture Decisions (ADRs):** When an architectural decision or tradeoff is finalized (or requested by the user), persist it:
  `python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py --type adr --title "<Title>" --context "<Problem>" --decisions "<Outcome>" --consequences "<Tradeoffs>" --techs "Tech1" "Tech2"`
- **Project Summaries:** When concluding a major milestone, persist the project summary using `save_knowledge.py --name "<Name>"`.
```

---

## 🚀 Quick Start

### 1. Configure Vault Path
Copy `config.example.json` to `config.json` and set your Obsidian vault path:

```bash
cp config.example.json config.json
```

```json
{
  "vault_path": "/home/user/Documents/ObsidianVaults/context_ai",
  "context_folder": "obsidian-context",
  "projects_dir": "Projects",
  "decisions_dir": "Decisions",
  "technologies_dir": "Technologies",
  "strategies_dir": "Strategies",
  "default_language": "en"
}
```

### 2. Verify Vault Status
```bash
python3 scripts/sync_vault.py
```

---

## 💻 CLI Commands Reference

### 1. Save an Architecture Decision Record (ADR)
```bash
python3 scripts/save_knowledge.py \
  --type adr \
  --title "Adopt Go for CLI Orchestrator" \
  --status "accepted" \
  --context "TypeScript implementation had concurrency bottlenecks with terminal TUIs." \
  --decisions "Migrate core orchestrator to Go 1.22 with Bubbletea and goroutine event bus." \
  --consequences "Single static binary, sub-second startup, clean concurrent event channels." \
  --techs "Go" "Bubbletea" "Lipgloss" \
  --lang en
```

### 2. Fast Vault Search (Zero Dependencies)
```bash
python3 scripts/search_context.py --query "concurrency bubbletea"
```

### 3. Save Project Knowledge
```bash
python3 scripts/save_knowledge.py \
  --name "Network Analyzer" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "Clean Architecture" "TDD" \
  --decisions "Adopted Scapy for packet crafting over raw sockets" \
  --instructions "Verify sandbox network permissions before sniffing" \
  --code "def capture(): pass" \
  --lang en
```

### 4. Analyze Technology Frequency
```bash
python3 scripts/tech_analytics.py --top 10 --lang en
```

---

## 🧪 Testing

Run the unit test suite (verifies ADR persistence, zero-dependency search, and sanitization):
```bash
python3 -m unittest discover -s tests/
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).
