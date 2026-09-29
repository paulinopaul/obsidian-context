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

## Funcionalidades Principales

1. **Recomendación y Análisis de Stack (`scripts/tech_analytics.py`)**:
   - Analiza el historial de proyectos para identificar las tecnologías más utilizadas por dominio.
   - Permite al modelo y al usuario decidir si continuar con la pila probada o experimentar con nuevas alternativas.
2. **Registro de Conocimiento de Proyecto (`scripts/save_knowledge.py`)**:
   - Guarda un resumen estructurado similar al cierre de planning-with-files: tecnologías empleadas, estrategias aplicadas, decisiones descartadas y directrices clave dadas en el chat.
   - Genera/actualiza automáticamente los hubs de tecnologías (`Technologies/[[Tecnología]]`) para visibilidad inmediata en el Obsidian Graph View.
3. **Búsqueda Semántica Vectorial Robusta (`scripts/search_context.py`)**:
   - Inferencia local mediante `ChromaDB` con soporte nativo de `ONNXRuntime` (modelo `all-MiniLM-L6-v2`), tolerante a fallos y sin dependencias pesadas de GPU/PyTorch.
4. **Sincronizador de Bóveda (`scripts/sync_vault.py`)**:
   - Sincroniza e indexa incrementalmente archivos Markdown de la bóveda hacia el almacenamiento vectorial.

## Uso Rápido por Línea de Comandos

```bash
# Analizar las tecnologías más utilizadas
python3 ~/.agents/skills/obsidian-context/scripts/tech_analytics.py --top 5

# Recomendar stack para un dominio específico
python3 ~/.agents/skills/obsidian-context/scripts/tech_analytics.py --domain backend-rag

# Búsqueda semántica en la memoria histórica
python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "estrategias de persistencia en obsidian"

# Sincronizar la bóveda completa con ChromaDB
python3 ~/.agents/skills/obsidian-context/scripts/sync_vault.py
```
