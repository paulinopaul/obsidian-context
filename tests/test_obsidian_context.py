import unittest
import os
import sys
import json
import tempfile
import shutil
from typing import List, Dict, Any

# Añadimos scripts al path para imports limpios
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

class TestObsidianContext(unittest.TestCase):
    def setUp(self):
        self.temp_vault = tempfile.mkdtemp()
        self.chroma_path = os.path.join(self.temp_vault, "chroma_storage")
        os.environ["OBSIDIAN_VAULT_PATH"] = self.temp_vault
        os.environ["CHROMA_DB_PATH"] = self.chroma_path

    def tearDown(self):
        shutil.rmtree(self.temp_vault, ignore_errors=True)

    def test_save_knowledge_success(self):
        from save_knowledge import save_project_knowledge
        
        result = save_project_knowledge(
            project_name="Network Analyzer",
            domain="networking",
            technologies=["Python", "Scapy", "FastAPI"],
            strategies=["TDD", "Clean Architecture"],
            decisions="Descartado socket raw por complejidad de permisos; adoptado Scapy.",
            instructions_learned="Asegurar permisos sudo en sandbox antes de sniffing.",
            code_snippets="def sniff_packets(): pass",
            vault_path=self.temp_vault
        )
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertTrue("file" in data)
        
        # Verificar creación del archivo del proyecto dentro de la subcarpeta obsidian-context
        proj_file = os.path.join(self.temp_vault, "obsidian-context", "Projects", data["file"])
        self.assertTrue(os.path.exists(proj_file))
        
        with open(proj_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("[[Python]]", content)
            self.assertIn("[[Scapy]]", content)
            self.assertIn("[[FastAPI]]", content)
            self.assertIn("[[TDD]]", content)
            self.assertIn("Asegurar permisos sudo", content)
            self.assertIn("def sniff_packets()", content)

        # Verificar creación/actualización de notas en Technologies/ dentro de obsidian-context
        tech_file = os.path.join(self.temp_vault, "obsidian-context", "Technologies", "Scapy.md")
        self.assertTrue(os.path.exists(tech_file))
        with open(tech_file, "r", encoding="utf-8") as f:
            t_content = f.read()
            self.assertIn("usage_count: 1", t_content)
            self.assertIn("[[Network Analyzer]]", t_content)

    def test_save_knowledge_sanitization(self):
        from save_knowledge import save_project_knowledge
        
        result = save_project_knowledge(
            project_name="../../malicious_path_test",
            domain="security",
            technologies=["Python"],
            strategies=["Defensive"],
            decisions="Testing path sanitization",
            instructions_learned="None",
            code_snippets="",
            vault_path=self.temp_vault
        )
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertNotIn("..", data["file"])
        self.assertNotIn("/", data["file"])

    def test_save_knowledge_invalid_inputs(self):
        from save_knowledge import save_project_knowledge
        
        # Nombre de proyecto vacío
        result = save_project_knowledge(
            project_name="",
            domain="test",
            technologies=[],
            strategies=[],
            decisions="",
            instructions_learned="",
            code_snippets="",
            vault_path=self.temp_vault
        )
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIn("inválido", data["msg"].lower())

    def test_tech_analytics_frequency(self):
        from save_knowledge import save_project_knowledge
        from tech_analytics import analyze_technology_stack
        
        # Guardar 2 proyectos con overlap tecnológico
        save_project_knowledge(
            project_name="Project Alpha",
            domain="web",
            technologies=["Python", "FastAPI", "PostgreSQL"],
            strategies=["TDD"],
            decisions="Dec 1",
            instructions_learned="Inst 1",
            code_snippets="",
            vault_path=self.temp_vault
        )
        save_project_knowledge(
            project_name="Project Beta",
            domain="web",
            technologies=["Python", "FastAPI", "Redis"],
            strategies=["TDD"],
            decisions="Dec 2",
            instructions_learned="Inst 2",
            code_snippets="",
            vault_path=self.temp_vault
        )
        
        stats = analyze_technology_stack(vault_path=self.temp_vault)
        self.assertEqual(stats["total_projects"], 2)
        # Python y FastAPI deben tener conteo 2
        tech_counts = {item["tech"]: item["count"] for item in stats["technologies"]}
        self.assertEqual(tech_counts.get("Python"), 2)
        self.assertEqual(tech_counts.get("FastAPI"), 2)
        self.assertEqual(tech_counts.get("PostgreSQL"), 1)
        self.assertEqual(tech_counts.get("Redis"), 1)

    def test_tech_analytics_domain_recommendation(self):
        from save_knowledge import save_project_knowledge
        from tech_analytics import recommend_stack_for_domain
        
        save_project_knowledge(
            project_name="CLI Parser",
            domain="cli-tools",
            technologies=["Python", "Typer", "Rich"],
            strategies=["Modular"],
            decisions="",
            instructions_learned="",
            code_snippets="",
            vault_path=self.temp_vault
        )
        
        rec = recommend_stack_for_domain("cli-tools", vault_path=self.temp_vault)
        self.assertIn("Typer", rec["top_technologies"])
        self.assertIn("Rich", rec["top_technologies"])

    def test_search_context_fallback(self):
        from search_context import search_semantic_context
        
        # Búsqueda sobre bóveda sin índice inicial debe retornar resultado seguro sin excepciones
        result = search_semantic_context("redes y sockets", n_results=2, db_path=self.chroma_path)
        data = json.loads(result)
        self.assertIn("status", data)
        self.assertIn(data["status"], ["success", "no_results", "error"])

    def test_sync_vault_indexing(self):
        from save_knowledge import save_project_knowledge
        from sync_vault import sync_obsidian_vault_to_chroma
        from search_context import search_semantic_context
        
        # Crear un proyecto
        save_project_knowledge(
            project_name="AI Memory Engine",
            domain="ai",
            technologies=["Python", "ChromaDB", "ONNXRuntime"],
            strategies=["SOLID", "TDD"],
            decisions="Adopción de embeddings locales",
            instructions_learned="Evitar llamadas de red",
            code_snippets="def get_embeddings(): pass",
            vault_path=self.temp_vault
        )
        
        # Sincronizar hacia ChromaDB
        sync_result = sync_obsidian_vault_to_chroma(vault_path=self.temp_vault, db_path=self.chroma_path)
        self.assertEqual(sync_result["status"], "success")
        self.assertGreaterEqual(sync_result["indexed_count"], 1)
        
        # Ahora buscar semánticamente
        search_res = json.loads(search_semantic_context("embeddings locales y vector", n_results=1, db_path=self.chroma_path))
        self.assertEqual(search_res["status"], "success")
        self.assertGreaterEqual(len(search_res["data"]), 1)

if __name__ == "__main__":
    unittest.main()
