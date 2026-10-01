# 🧠 Obsidian Context Agent Skill (`obsidian-context`) v2.0

[ [English](README.md) | Español ]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform: Antigravity | OpenCode | Claude Code | Any Agent](https://img.shields.io/badge/Platform-Universal%20Agent%20Skill-purple.svg)]()
[![Dependencies: Zero](https://img.shields.io/badge/Dependencias-Cero%20(Pure%20Stdlib)-brightgreen.svg)]()

> **Agent Skill sin fricción para la persistencia de memoria técnica, Registros de Decisiones Arquitectónicas (ADRs), analítica de stack y visualización en el Grafo de Obsidian mediante enlaces bidireccionales (`[[wikilinks]]`). 100% autónoma en Markdown puro sin dependencias externas.**

---

## 📌 ¿Qué problema resuelve?

Durante las sesiones con agentes de IA, el contexto volátil se pierde al concluir la tarea. `obsidian-context` resuelve este problema sin sobreingeniería ni consumo innecesario de recursos:

1. **Registros de Decisiones Arquitectónicas (ADRs)**: Documenta el problema, las opciones descartadas, la solución adoptada y los tradeoffs en notas dentro de `Decisions/`.
2. **Retención de Conocimiento por Proyecto**: Guarda resúmenes técnicos estructurados de proyectos finalizados, patrones de diseño y directrices clave en `Projects/`.
3. **Visualización en el Obsidian Graph View**: Conecta automáticamente cada nota de proyecto o ADR con fichas centrales en `Technologies/[[Tecnología]]`, generando un grafo visual de todo tu ecosistema de software.
4. **Protocolo Ágil y sin Fricción**: Erradica las interrupciones burocráticas en el chat (sin preguntas obligatorias de inicio o de confirmación de idioma). El agente actúa en silencio o a demanda del usuario.
5. **Cero Dependencias Externas**: Funciona completamente con la biblioteca estándar de Python 3 (`os`, `re`, `glob`, `json`, `math`). Sin ChromaDB, sin ONNXRuntime y sin daemons externos. Búsqueda instantánea (<20 ms).
6. **Aislamiento Limpio en la Bóveda**: Toda la información generada reside estrictamente en la subcarpeta `obsidian-context/` dentro de tu bóveda de Obsidian, sin contaminar tus notas personales.

---

## 📂 Estructura de la Bóveda

Crea la carpeta `obsidian-context` en tu bóveda de Obsidian y define su ruta en `config.json`:

```
Tu-Boveda-Obsidian/
└── obsidian-context/                 <-- Subcarpeta dedicada dentro de tu Bóveda
    ├── Decisions/                    <-- Registros de Decisiones Arquitectónicas (ADRs)
    ├── Projects/                     <-- Resúmenes de proyectos cerrados (enlaces [[tech]])
    ├── Technologies/                 <-- Fichas de catálogo para el Obsidian Graph View
    └── Strategies/                   <-- Patrones y arquitecturas de ingeniería
```

---

## 🏗️ Arquitectura del Repositorio

```
obsidian-context/                     <-- Directorio de la Skill (~/.agents/skills/obsidian-context)
├── config.json                       <-- Configuración activa de rutas (ignorado por git)
├── config.example.json               <-- Plantilla de configuración de ejemplo
├── SKILL.md                          <-- Especificación de la Skill v2.0 (Zero Friction)
├── README.md                         <-- Documentación en inglés
├── README.es.md                      <-- Documentación en español
├── LICENSE                           <-- Licencia MIT
├── pyproject.toml                    <-- Empaquetado estándar Python (cero dependencias externas)
├── schema_knowledge.json             <-- Esquema JSON para herramientas de agentes
├── scripts/                          <-- Scripts modulares livianos (biblioteca estándar)
│   ├── config.py                     <-- Gestor centralizado de rutas
│   ├── save_knowledge.py             <-- Guarda ADRs, resúmenes de proyectos y actualiza Technologies/
│   ├── search_context.py             <-- Búsqueda rápida por metadatos y palabras clave (<20 ms)
│   ├── tech_analytics.py             <-- Analiza frecuencias de tecnologías y recomienda stacks
│   ├── sync_vault.py                 <-- Validador de notas e inventario de la bóveda
│   └── chat_summary_extract.py       <-- Extractor estructurado de notas de sesión
├── templates/                        <-- Plantillas Markdown con frontmatter YAML y wikilinks
│   ├── adr.en.md                     <-- Plantilla para ADR (Inglés)
│   ├── adr.es.md                     <-- Plantilla para ADR (Español)
│   ├── project_knowledge.en.md       <-- Plantilla para resumen de proyecto (Inglés)
│   ├── project_knowledge.es.md       <-- Plantilla para resumen de proyecto (Español)
│   ├── technology_hub.en.md          <-- Ficha técnica de tecnología (Inglés)
│   ├── technology_hub.es.md          <-- Ficha técnica de tecnología (Español)
│   ├── postmortem.en.md              <-- Plantilla para Post-Mortem (Inglés)
│   └── postmortem.es.md              <-- Plantilla para Post-Mortem (Español)
├── references/
│   ├── graph_and_links.md            <-- Guía para Obsidian Graph View (Inglés)
│   └── graph_and_links.es.md         <-- Guía para Obsidian Graph View (Español)
└── tests/
    └── test_obsidian_context.py       <-- Suite de pruebas unitarias automatizadas (100% pasando)
```

---

## 🤖 Directiva Universal para Agentes (System Prompt Snippet)

Añade este bloque a las instrucciones del sistema de tu agente o a tus reglas globales (como `AGENTS.md`, `CLAUDE.md`, o bloque de reglas):

```markdown
### Memoria y Decisiones Arquitectónicas (obsidian-context)
Cuando la skill `obsidian-context` esté disponible en el entorno:
- **Cero Fricción:** NO interrumpas al usuario con preguntas burocráticas de inicio o selección de idioma.
- **Consulta a Demanda o Contextual:** Cuando el usuario pregunte por decisiones pasadas o patrones de stack, consulta la bóveda en silencio:
  `python3 ~/.agents/skills/obsidian-context/scripts/search_context.py --query "<palabras_clave>"`
- **Decisiones de Arquitectura (ADRs):** Al acordar una decisión de arquitectura o tradeoff técnico relevante (o cuando el usuario lo solicite), guárdala:
  `python3 ~/.agents/skills/obsidian-context/scripts/save_knowledge.py --type adr --title "<Título>" --context "<Problema>" --decisions "<Solución>" --consequences "<Tradeoffs>" --techs "Tech1" "Tech2"`
- **Cierre de Proyectos:** Al concluir un hito importante, guarda el resumen técnico con `save_knowledge.py --name "<Nombre>"`.
```

---

## 🚀 Inicio Rápido

### 1. Configurar la Ruta de la Bóveda
Copia `config.example.json` a `config.json` y especifica tu ruta local:

```bash
cp config.example.json config.json
```

```json
{
  "vault_path": "/home/usuario/Documents/ObsidianVaults/context_ai",
  "context_folder": "obsidian-context",
  "projects_dir": "Projects",
  "decisions_dir": "Decisions",
  "technologies_dir": "Technologies",
  "strategies_dir": "Strategies",
  "default_language": "es"
}
```

### 2. Verificar el Estado de la Bóveda
```bash
python3 scripts/sync_vault.py
```

---

## 💻 Referencia de Comandos CLI

### 1. Guardar un Registro de Decisión Arquitectónica (ADR)
```bash
python3 scripts/save_knowledge.py \
  --type adr \
  --title "Migración de whtexpert a Go" \
  --status "accepted" \
  --context "La implementación previa en TypeScript presentaba cuellos de botella con la TUI de terminal." \
  --decisions "Reescribir el orquestador en Go 1.22 utilizando Bubbletea y un bus de eventos concurrente." \
  --consequences "Binario único estático, arranque instantáneo y aislamiento total de eventos por canales." \
  --techs "Go" "Bubbletea" "Lipgloss" \
  --lang es
```

### 2. Búsqueda Rápida en la Bóveda (Cero Dependencias)
```bash
python3 scripts/search_context.py --query "concurrencia bubbletea"
```

### 3. Guardar Resumen de Conocimiento de Proyecto
```bash
python3 scripts/save_knowledge.py \
  --name "Analizador de Red" \
  --domain "networking" \
  --techs "Python" "Scapy" "FastAPI" \
  --strategies "Clean Architecture" "TDD" \
  --decisions "Adopción de Scapy para captura de tramas frente a raw sockets" \
  --instructions "Validar permisos en sandbox antes de capturar" \
  --code "def capture(): pass" \
  --lang es
```

### 4. Analizar Frecuencia de Tecnologías
```bash
python3 scripts/tech_analytics.py --top 10 --lang es
```

---

## 🧪 Pruebas Unitarias

Ejecuta la suite de pruebas (valida persistencia de ADRs, sanitización y búsqueda sin dependencias externas):
```bash
python3 -m unittest discover -s tests/
```

---

## 📄 Licencia

Distribuido bajo la [Licencia MIT](LICENSE).
