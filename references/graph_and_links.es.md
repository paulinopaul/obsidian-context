# Guía de Interoperabilidad con Obsidian Graph View

## Semántica de Enlaces Bidireccionales
Para que Obsidian construya un Grafo de Conocimiento navegable y coherente entre proyectos y tecnologías:

1. **Notas de Proyecto (`obsidian-context/Projects/`)**:
   - Cada tecnología mencionada en el YAML y en el cuerpo debe enlazarse como `[[NombreTecnologia]]`.
   - Cada estrategia debe enlazarse como `[[NombreEstrategia]]`.
   - Esto convierte a cada tecnología y estrategia en un nodo central (Hub) en el Obsidian Graph View.

2. **Notas de Hub Tecnológico (`obsidian-context/Technologies/`)**:
   - Cada tecnología tiene una nota individual (ej. `Technologies/ChromaDB.md`).
   - Mantiene enlaces de retroceso (*back-links*) automáticos hacia todos los proyectos que la emplearon.
   - Registra atributos como `usage_count`, `category`, `status`.

3. **Interoperabilidad con Modelos de Lenguaje**:
   - Los modelos pueden leer directamente la carpeta `Technologies/` o consultar `tech_analytics.py` para responder de inmediato:
     - "¿Cuál es la base de datos vectorial que más usamos?"
     - "¿Qué herramientas CLI solemos emplear para parsing AST?"
     - "¿Cuáles son las directrices de cierre que acordamos en la sesión anterior?"
