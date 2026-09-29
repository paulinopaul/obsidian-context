# 🧠 Obsidian Context Agent Skill (`obsidian-context`)

[ [English](README.md) | Español ]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude Code](https://img.shields.io/badge/Platform-Antigravity%20%7C%20OpenCode%20%7C%20Claude%20Code-purple.svg)]()
[![Embeddings: Local ONNX](https://img.shields.io/badge/Embeddings-Local%20ONNX-green.svg)]()

> **Agent Skill para la persistencia del conocimiento de proyectos, análisis de stack tecnológico y visualización en el Grafo de Obsidian mediante enlaces bidireccionales (`[[wikilinks]]`). Soporta generación bilingüe de notas Markdown (Español e Inglés).**

---

## 📌 ¿Qué problema resuelve?

Durante las sesiones de programación en agentes de IA (Antigravity, OpenCode, Claude Code, etc.), el contexto volátil se pierde al finalizar una tarea. `obsidian-context` permite:

1. **Persistencia Estructurada de Cierre**: Guarda un resumen técnico del proyecto (tecnologías empleadas, estrategias aplicadas, decisiones de arquitectura y directrices dadas en el chat) sin necesidad de inspeccionar logs crudos de ejecución.
2. **Visualización en el Obsidian Graph View**: Al conectar automáticamente cada nota de proyecto con fichas técnicas en `Technologies/[[Tecnología]]`, se genera una red visual que muestra la constelación de herramientas utilizadas en todos tus proyectos.
3. **Analítica de Stack y Recomendación**: Permite a los agentes analizar cuáles son las tecnologías más utilizadas históricamente para un tipo de tarea (`web`, `cli`, `ai`, `networking`) y consultar al usuario si desea reutilizar la pila probada o explorar una alternativa.
4. **Inferencia Vectorial Liviana (Cero PyTorch/CUDA)**: Utiliza `DefaultEmbeddingFunction` de ChromaDB sobre `ONNXRuntime` local (`all-MiniLM-L6-v2`, 384 dimensiones), eliminando los ~2GB de dependencias pesadas de `sentence-transformers`.
5. **Aislamiento Limpio en la Bóveda**: Todas las notas, tecnologías y bases vectoriales residen en una subcarpeta dedicada `obsidian-context/` dentro de tu bóveda, evitando saturar o mezclar tus notas personales.
6. **Generación Bilingüe de Notas (ES/EN)**: Genera notas automáticamente en español o inglés según la interacción y confirmación con el usuario.

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
├── config.json                       <-- Configuración activa de rutas (ignorado por git)
├── config.example.json               <-- Plantilla de configuración de ejemplo
├── SKILL.md                          <-- Especificación Agent Skill y protocolo para modelos
├── README.md                         <-- Documentación en inglés
├── README.es.md                      <-- Documentación en español
├── LICENSE                           <-- Licencia MIT
├── pyproject.toml                    <-- Empaquetado estándar Python
├── .gitignore                        <-- Exclusiones de Git (excluye planes locales y config)
├── schema_knowledge.json             <-- Esquema JSON para herramientas MCP y agentes
├── scripts/                          <-- Scripts ejecutables modulares (SOLID)
│   ├── config.py                     <-- Gestor centralizado de configuración
│   ├── save_knowledge.py             <-- Guarda notas de proyecto y actualiza Technologies/ (ES/EN)
│   ├── tech_analytics.py             <-- Analiza frecuencias de stack y formula recomendaciones (ES/EN)
│   ├── search_context.py             <-- Búsqueda semántica vectorial local (ChromaDB + ONNX)
│   ├── sync_vault.py                 <-- Sincronizador incremental Bóveda <-> ChromaDB
│   └── chat_summary_extract.py       <-- Extractor estructurado de notas de sesión
├── templates/                        <-- Plantillas Markdown bilingües
│   ├── project_knowledge.en.md       <-- Plantilla de resumen de proyecto (Inglés)
│   ├── project_knowledge.es.md       <-- Plantilla de resumen de proyecto (Español)
│   ├── technology_hub.en.md          <-- Ficha técnica para catálogo de tecnologías (Inglés)
│   ├── technology_hub.es.md          <-- Ficha técnica para catálogo de tecnologías (Español)
│   ├── postmortem.en.md              <-- Plantilla para Post-Mortem (Inglés)
│   └── postmortem.es.md              <-- Plantilla para Post-Mortem (Español)
├── references/
│   ├── graph_and_links.md            <-- Guía de semántica para Obsidian Graph View (Inglés)
│   └── graph_and_links.es.md         <-- Guía de semántica para Obsidian Graph View (Español)
└── tests/
    └── test_obsidian_context.py       <-- Suite de pruebas unitarias automatizadas (TDD)
```

---

## 🤖 Directiva Universal para Agentes (System Prompt Snippet)

No necesitas reglas complejas ni entornos propietarios. Solo añade este bloque a las instrucciones del sistema de tu agente o a su archivo de reglas globales (como `AGENTS.md`, `CLAUDE.md`, o `GEMINI.md`):

```markdown
### Gobernanza de Memoria y Conocimiento (obsidian-context)
Cuando la skill `obsidian-context` esté disponible en el entorno:
1. **Al Iniciar una Tarea:**
   Pregunta de forma proactiva al usuario si desea realizar una revisión del contexto:
   - Español: "He detectado la skill `obsidian-context`. ¿Deseas hacer una revisión del contexto histórico y stack tecnológico recomendado para este trabajo, o prefieres omitir la revisión?"
   - Inglés: "I detected the `obsidian-context` skill. Would you like to review historical context and recommended tech stack for this task, or would you prefer to skip this review?"
   Si el usuario aprueba, ejecuta `scripts/tech_analytics.py --domain <dominio>` o `scripts/search_context.py`.
2. **Al Finalizar una Tarea:**
   Antes de guardar, consulta al usuario el idioma en el que prefiere registrar las notas:
   - Español: "¿Deseas que el resumen técnico y las notas del proyecto se guarden en español o prefieres en inglés?"
   - Inglés: "Would you like the technical summary and project notes saved in English or Spanish?"
   Luego ejecuta `scripts/save_knowledge.py --lang <es|en>` seguido de `scripts/sync_vault.py`.
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
Copia `config.example.json` a `config.json` y ajusta la ruta de tu bóveda:

```bash
cp config.example.json config.json
```

```json
{
  "vault_path": "/ruta/a/tu/BovedaObsidian",
  "context_folder": "obsidian-context",
  "projects_dir": "Projects",
  "technologies_dir": "Technologies",
  "strategies_dir": "Strategies",
  "chroma_dir": "chroma_storage",
  "default_language": "es"
}
```

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

## 💻 Uso por Línea de Comandos (CLI)

### Analizar Tecnologías Más Utilizadas
```bash
python3 scripts/tech_analytics.py --top 10 --lang es
```

### Recomendar Stack para un Dominio Específico
```bash
python3 scripts/tech_analytics.py --domain backend-rag --lang es
```

### Guardar Resumen de Conocimiento de un Proyecto (Bilingüe)
```bash
# Guardar en Español
python3 scripts/save_knowledge.py \
  --name "Analizador de Red" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "TDD" "Clean-Architecture" \
  --decisions "Adopción de Scapy para parsing de tramas Ethernet" \
  --instructions "Validar permisos en sandbox antes de capturar tráfico" \
  --code "def capture(): pass" \
  --lang es

# Guardar en Inglés
python3 scripts/save_knowledge.py \
  --name "Network Analyzer" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "TDD" "Clean-Architecture" \
  --decisions "Adopted Scapy for packet crafting" \
  --instructions "Verify sandbox network permissions" \
  --code "def capture(): pass" \
  --lang en
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
