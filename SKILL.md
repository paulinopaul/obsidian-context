---
name: obsidian-context
description: "Gestión de memoria persistente, contexto técnico histórico, análisis de stack tecnológico y enlaces bidireccionales en la bóveda de Obsidian. Permite consultar tecnologías más usadas, registrar resúmenes de proyectos con directrices del chat y visualizar conexiones en el grafo de Obsidian."
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep"
metadata:
  version: "1.0.0"
---

# Obsidian Context Skill

Habilidad modular para gobernar el conocimiento técnico persistente de los agentes en Obsidian. Transforma las decisiones de diseño, fragmentos de código, directrices del chat y selecciones tecnológicas en un Grafo de Conocimiento conectado mediante `[[wikilinks]]`.

---

## 🤖 Protocolo Operativo para Agentes de IA (AGY, OpenCode, Claude Code)

Cualquier modelo ejecutándose bajo Antigravity (AGY), OpenCode o Claude Code debe aplicar esta skill siguiendo este ciclo de vida:

### 1. Al Iniciar una Tarea o Proyecto (Fase de Exploración)
Antes de proponer arquitecturas o stacks tecnológicos desde cero:
1. **Ejecutar Búsqueda Semántica**:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "<descripción del problema o tecnologías en cuestión>"
   ```
2. **Consultar Frecuencia y Recomendación de Stack**:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/tech_analytics.py --domain "<dominio-técnico>"
   ```
3. **Preguntar al Usuario**: Si existe un stack histórico probado, presentar al usuario:
   > *"Históricamente para tareas de tipo `<dominio>` se ha utilizado `<stack_top>`. ¿Deseas reutilizar esta pila o explorar una alternativa?"*

### 2. Al Concluir un Proyecto o Hito Mayor (Fase de Cierre)
Una vez finalizada la implementación y superada la suite de pruebas:
1. **Persistir el Conocimiento Estructurado**:
   Invocar `scripts/save_knowledge.py` o la herramienta MCP `tool_save_project_knowledge`:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py \
     --name "<nombre_proyecto>" \
     --domain "<dominio>" \
     --techs "Tecnología1" "Tecnología2" \
     --strategies "Estrategia1" "Estrategia2" \
     --decisions "<decisiones clave y alternativas descartadas>" \
     --instructions "<directrices o indicaciones recibidas en el chat>" \
     --code "<fragmento crítico de código>"
   ```
2. **Sincronizar Vectores**:
   ```bash
   python3 ~/.agents/skills/obsidian-context/scripts/sync_vault.py
   ```

---

## 🛠️ Herramientas y Scripts Disponibles

- `scripts/save_knowledge.py`: Genera notas enriquecidas en `Projects/` y actualiza fichas técnicas en `Technologies/` para el Obsidian Graph View.
- `scripts/tech_analytics.py`: Calcula estadísticas de frecuencias globales y formula recomendaciones contextuales por dominio.
- `scripts/search_context.py`: Ejecuta búsqueda semántica local con `ChromaDB` y `ONNXRuntime` (`DefaultEmbeddingFunction`).
- `scripts/sync_vault.py`: Sincroniza e indexa incrementalmente notas hacia ChromaDB.
- `scripts/chat_summary_extract.py`: Parsea notas crudas de sesión para estructurar el resumen técnico.
