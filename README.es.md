# 🧠 Obsidian Context Agent Skill (`obsidian-context`)

[ [English](README.md) | Español ]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude](https://img.shields.io/badge/Platform-Antigravity%20%7C%20OpenCode%20%7C%20Claude-purple.svg)]()
[![Embeddings: Local ONNX](https://img.shields.io/badge/Embeddings-Local%20ONNX-green.svg)]()

> **Agent Skill para la persistencia del conocimiento de proyectos, análisis de stack tecnológico y visualización en el Grafo de Obsidian mediante enlaces bidireccionales (`[[wikilinks]]`).**

---

## 📌 ¿Qué problema resuelve?

Durante las sesiones de programación en agentes de IA (Antigravity, OpenCode, Claude Code), el contexto volátil se pierde al finalizar una tarea. `obsidian-context` permite:

1. **Persistencia Estructurada de Cierre**: Guarda un resumen técnico del proyecto (tecnologías empleadas, estrategias aplicadas, decisiones de arquitectura y directrices dadas en el chat) sin necesidad de inspeccionar logs crudos de ejecución.
2. **Visualización en el Obsidian Graph View**: Al conectar automáticamente cada nota de proyecto con fichas técnicas en `Technologies/[[Tecnología]]`, se genera una red visual que muestra la constelación de herramientas utilizadas en todos tus proyectos.
3. **Analítica de Stack y Recomendación**: Permite a los agentes analizar cuáles son las tecnologías más utilizadas históricamente para un tipo de tarea (`web`, `cli`, `ai`, `networking`) y consultar al usuario si desea reutilizar la pila probada o explorar una alternativa.
4. **Inferencia Vectorial Liviana (Cero PyTorch/CUDA)**: Utiliza `DefaultEmbeddingFunction` de ChromaDB sobre `ONNXRuntime` local (`all-MiniLM-L6-v2`, 384 dimensiones), eliminando los ~2GB de dependencias pesadas de `sentence-transformers`.
5. **Aislamiento Limpio en la Bóveda**: Todas las notas, tecnologías y bases vectoriales residen en una subcarpeta dedicada `obsidian-context/` dentro de tu bóveda, evitando saturar o mezclar tus notas personales.

---

## 📂 Configuración de la Bóveda y Estructura de Directorios

> [!IMPORTANT]
> **Subcarpeta Dedicada en la Bóveda Obligatoria:**
> Debes crear una carpeta llamada `obsidian-context` dentro de tu bóveda de Obsidian y especificar la ruta en el archivo `config.json` dentro de la skill. Esto garantiza que todos los proyectos, tecnologías y vectores generados por los agentes se almacenen de forma limpia y autónoma.

```
Tu-Boveda-Obsidian/
└── obsidian-context/                 <-- Subcarpeta dedicada dentro de tu Bóveda
    ├── Projects/                     <-- Resúmenes de proyectos cerrados (enlaces [[tech]])
    ├── Technologies/                 <-- Fichas de catálogo para el Obsidian Graph View
    ├── Strategies/                   <-- Patrones y arquitecturas aplicadas
    └── chroma_storage/               <-- Base vectorial ChromaDB local (ONNX)
```

---

## 🏗️ Arquitectura del Repositorio

```
obsidian-context/                     <-- Directorio de la Skill (~/.agents/skills/obsidian-context)
├── config.json                       <-- Configuración activa de rutas y carpetas
├── config.example.json               <-- Plantilla de configuración de ejemplo
├── SKILL.md                          <-- Especificación Agent Skill y protocolo para modelos
├── README.md                         <-- Documentación en inglés
├── README.es.md                      <-- Documentación en español
├── LICENSE                           <-- Licencia MIT
├── pyproject.toml                    <-- Empaquetado estándar Python
├── .gitignore                        <-- Exclusiones de Git
├── schema_knowledge.json             <-- Esquema JSON para herramientas MCP y agentes
├── task_plan.md                      <-- Plan persistente (planning-with-files)
├── findings.md                       <-- Registro de descubrimientos de arquitectura
├── progress.md                       <-- Bitácora de ejecución y validación TDD
├── scripts/                          <-- Scripts ejecutables modulares (SOLID)
│   ├── config.py                     <-- Gestor centralizado de configuración
│   ├── save_knowledge.py             <-- Guarda notas de proyecto y actualiza Technologies/
│   ├── tech_analytics.py             <-- Analiza frecuencias de stack y formula recomendaciones
│   ├── search_context.py             <-- Búsqueda semántica vectorial local (ChromaDB + ONNX)
│   ├── sync_vault.py                 <-- Sincronizador incremental Bóveda <-> ChromaDB
│   └── chat_summary_extract.py       <-- Extractor estructurado de notas de sesión
├── templates/                        <-- Plantillas Markdown estructuradas
│   ├── project_knowledge.md          <-- Plantilla para resúmenes de proyectos
│   ├── technology_hub.md             <-- Ficha técnica para catálogo de tecnologías
│   └── postmortem.md                 <-- Plantilla estándar para Post-Mortems
├── references/
│   └── graph_and_links.md            <-- Guía de semántica para el Obsidian Graph View
└── tests/
    └── test_obsidian_context.py       <-- Suite de pruebas unitarias automatizadas (TDD)
```

---

## 🚀 Instalación y Puesta en Marcha Rápida

### 1. Clonar en el Directorio de Agent Skills
```bash
# Directorio estándar global de Agent Skills
cd ~/.agents/skills
git clone https://github.com/<tu-usuario>/obsidian-context.git
cd obsidian-context
```

### 2. Configurar la Ruta de tu Bóveda en la Skill
Edita o crea el archivo `config.json` dentro de `~/.agents/skills/obsidian-context/config.json`:

```json
{
  "vault_path": "/ruta/a/tu/BovedaObsidian",
  "context_folder": "obsidian-context",
  "projects_dir": "Projects",
  "technologies_dir": "Technologies",
  "strategies_dir": "Strategies",
  "chroma_dir": "chroma_storage"
}
```

> [!TIP]
> También puedes definir la variable de entorno en tu `~/.bashrc` o `~/.zshrc`:
> ```bash
> export OBSIDIAN_VAULT_PATH="/ruta/a/tu/BovedaObsidian"
> ```

### 3. Instalar Dependencias
```bash
pip install chromadb onnxruntime mcp
```

### 4. Crear la Carpeta en tu Bóveda y Sincronización Inicial
```bash
# Crear la carpeta aislada en tu bóveda
mkdir -p "/ruta/a/tu/BovedaObsidian/obsidian-context"

# Sincronización inicial de notas existentes
python3 scripts/sync_vault.py
```

---

## 🤖 Cómo los Agentes de Código Utilizan Esta Skill

### 1. Antigravity (AGY)
- **Descubrimiento**: Registrada globalmente en `~/.gemini/config/skills.json` (apuntando a `~/.agents/skills`).
- **Integración MCP**: Expone 4 herramientas nativas en `~/.gemini/config/mcp_config.json`:
  - `tool_query_tech_stack`: Estadísticas de frecuencia y recomendaciones.
  - `tool_save_project_knowledge`: Guarda resúmenes con wikilinks en `obsidian-context/`.
  - `tool_semantic_search_obsidian`: Recupera contexto técnico histórico desde ChromaDB local.
  - `tool_sync_obsidian_vault`: Sincroniza notas nuevas hacia ChromaDB.
- **Ciclo de Vida**: El modelo activa búsquedas semánticas durante la planificación inicial (Regla 20) y persiste el conocimiento al concluir el hito.

### 2. OpenCode
- **Descubrimiento**: Descubierta automáticamente de forma nativa en `~/.agents/skills/obsidian-context` según la especificación de Agent Skills.
- **Flujo de Trabajo**: Guiado por directrices globales en `~/.agents/AGENTS.md`. Al inicio, OpenCode ejecuta `tech_analytics.py --domain <dominio>` para evaluar stacks probados; al cierre, invoca `save_knowledge.py`.

### 3. Claude Code
- **Descubrimiento**: Vinculada simbólicamente en `~/.claude/skills/obsidian-context`:
  ```bash
  mkdir -p ~/.claude/skills
  ln -s ~/.agents/skills/obsidian-context ~/.claude/skills/obsidian-context
  ```
- **Ejecución**: Puede invocarse interactivamente mediante `/obsidian-context` o de forma automática cuando el agente investiga proyectos anteriores o concluye una tarea compleja.

---

## 💻 Uso por Línea de Comandos (CLI)

### Analizar Tecnologías Más Utilizadas
```bash
python3 scripts/tech_analytics.py --top 10
```

### Recomendar Stack para un Dominio Específico
```bash
python3 scripts/tech_analytics.py --domain backend-rag
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

### Sincronizar Bóveda hacia ChromaDB Local
```bash
python3 scripts/sync_vault.py
```

### Búsqueda Semántica Vectorial
```bash
python3 scripts/search_context.py --query "estrategias de persistencia en obsidian"
```

---

## 🧪 Pruebas Automatizadas (TDD)

Ejecuta la suite de pruebas unitarias:
```bash
python3 -m unittest discover -s tests/
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).
