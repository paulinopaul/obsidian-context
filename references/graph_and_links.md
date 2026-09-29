# Obsidian Graph View Interoperability Reference

## Bidirectional Linking Semantics
To allow Obsidian to build an interconnected and navigable Knowledge Graph across projects and technologies:

1. **Project Notes (`obsidian-context/Projects/`)**:
   - Each technology listed in YAML metadata and markdown body must be wrapped as `[[TechnologyName]]`.
   - Each architectural pattern must be wrapped as `[[StrategyName]]`.
   - This turns every technology and pattern into a central hub node in Obsidian Graph View.

2. **Technology Hub Notes (`obsidian-context/Technologies/`)**:
   - Every technology receives a standalone note (e.g., `Technologies/ChromaDB.md`).
   - Maintains automatic back-links to all project summaries that utilized it.
   - Tracks metadata attributes such as `usage_count`, `category`, and `status`.

3. **AI Coding Agent Interoperability**:
   - Models can inspect `Technologies/` or execute `tech_analytics.py` to answer immediately:
     - "Which vector database do we use most frequently?"
     - "What CLI libraries do we prefer for parsing or terminal output?"
     - "What closing guidelines did we agree on in the previous session?"
