import unittest
import os
import sys
import json
import tempfile
import shutil
from typing import List, Dict, Any

# Ensure scripts directory is on python path for clean imports
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

class TestObsidianContext(unittest.TestCase):
    def setUp(self):
        """Sets up an isolated temporary vault for every test execution."""
        self.temp_vault = tempfile.mkdtemp()
        self.chroma_path = os.path.join(self.temp_vault, "obsidian-context", "chroma_storage")
        os.environ["OBSIDIAN_VAULT_PATH"] = self.temp_vault
        os.environ["CHROMA_DB_PATH"] = self.chroma_path

    def tearDown(self):
        """Cleans up the temporary vault directory after test completion."""
        shutil.rmtree(self.temp_vault, ignore_errors=True)

    def test_save_knowledge_spanish_success(self):
        """Validates successful persistence of project knowledge in Spanish."""
        from save_knowledge import save_project_knowledge
        
        result = save_project_knowledge(
            project_name="Network Analyzer",
            domain="networking",
            technologies=["Python", "Scapy", "FastAPI"],
            strategies=["TDD", "Clean Architecture"],
            decisions="Descartado socket raw; adoptado Scapy.",
            instructions_learned="Asegurar permisos sudo en sandbox antes de sniffing.",
            code_snippets="def sniff_packets(): pass",
            vault_path=self.temp_vault,
            language="es"
        )
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertTrue("file" in data)
        self.assertEqual(data.get("language"), "es")
        
        # Verify creation of project file inside obsidian-context/Projects
        proj_file = os.path.join(self.temp_vault, "obsidian-context", "Projects", data["file"])
        self.assertTrue(os.path.exists(proj_file))
        
        with open(proj_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# 📌 Resumen Técnico: Network Analyzer", content)
            self.assertIn("## 🛠️ Stack Tecnológico Utilizado", content)
            self.assertIn("[[Python]]", content)
            self.assertIn("[[Scapy]]", content)
            self.assertIn("[[FastAPI]]", content)
            self.assertIn("[[TDD]]", content)

        # Verify creation of technology hub in obsidian-context/Technologies/
        tech_file = os.path.join(self.temp_vault, "obsidian-context", "Technologies", "Scapy.md")
        self.assertTrue(os.path.exists(tech_file))
        with open(tech_file, "r", encoding="utf-8") as f:
            t_content = f.read()
            self.assertIn("usage_count: 1", t_content)
            self.assertIn("# 🔧 Tecnología: Scapy", t_content)
            self.assertIn("[[Network Analyzer]]", t_content)

    def test_save_knowledge_english_success(self):
        """Validates successful persistence of project knowledge in English."""
        from save_knowledge import save_project_knowledge
        
        result = save_project_knowledge(
            project_name="Cloud Synchronizer",
            domain="cloud",
            technologies=["Go", "gRPC", "Docker"],
            strategies=["SOLID", "Microservices"],
            decisions="Selected gRPC over REST for lower serialization latency.",
            instructions_learned="Enable TLS verification on external endpoints.",
            code_snippets="func main() {}",
            vault_path=self.temp_vault,
            language="en"
        )
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data.get("language"), "en")
        
        # Verify creation of project file with English headers
        proj_file = os.path.join(self.temp_vault, "obsidian-context", "Projects", data["file"])
        self.assertTrue(os.path.exists(proj_file))
        
        with open(proj_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# 📌 Technical Summary: Cloud Synchronizer", content)
            self.assertIn("## 🛠️ Technology Stack Used", content)
            self.assertIn("## 📐 Strategies & Design Patterns Applied", content)
            self.assertIn("[[Go]]", content)
            self.assertIn("[[gRPC]]", content)

        # Verify English technology hub note
        tech_file = os.path.join(self.temp_vault, "obsidian-context", "Technologies", "gRPC.md")
        self.assertTrue(os.path.exists(tech_file))
        with open(tech_file, "r", encoding="utf-8") as f:
            t_content = f.read()
            self.assertIn("# 🔧 Technology: gRPC", t_content)
            self.assertIn("## 🔗 Projects Where Used", t_content)
            self.assertIn("[[Cloud Synchronizer]]", t_content)

    def test_save_knowledge_sanitization(self):
        """Ensures directory traversal attacks in project names are properly sanitized."""
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
        """Verifies error handling when empty or invalid project names are provided."""
        from save_knowledge import save_project_knowledge
        
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

    def test_tech_analytics_frequency(self):
        """Verifies technology usage counting and frequency aggregation across notes."""
        from save_knowledge import save_project_knowledge
        from tech_analytics import analyze_technology_stack
        
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
        tech_counts = {item["tech"]: item["count"] for item in stats["technologies"]}
        self.assertEqual(tech_counts.get("Python"), 2)
        self.assertEqual(tech_counts.get("FastAPI"), 2)
        self.assertEqual(tech_counts.get("PostgreSQL"), 1)
        self.assertEqual(tech_counts.get("Redis"), 1)

    def test_tech_analytics_domain_recommendation_bilingual(self):
        """Verifies domain recommendation generation in both Spanish and English."""
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
        
        # Test Spanish recommendation
        rec_es = recommend_stack_for_domain("cli-tools", vault_path=self.temp_vault, language="es")
        self.assertIn("Typer", rec_es["top_technologies"])
        self.assertIn("¿Deseas utilizar esta pila probada", rec_es["recommendation_prompt"])

        # Test English recommendation
        rec_en = recommend_stack_for_domain("cli-tools", vault_path=self.temp_vault, language="en")
        self.assertIn("Typer", rec_en["top_technologies"])
        self.assertIn("Would you like to use this proven stack", rec_en["recommendation_prompt"])

    def test_search_context_fallback(self):
        """Ensures semantic search handles uninitialized empty databases safely."""
        from search_context import search_semantic_context
        
        result = search_semantic_context("networking and sockets", n_results=2, db_path=self.chroma_path)
        data = json.loads(result)
        self.assertIn("status", data)
        self.assertIn(data["status"], ["success", "no_results", "error"])

    def test_sync_vault_indexing(self):
        """Validates that sync_vault reads markdown notes and indexes them."""
        from save_knowledge import save_project_knowledge
        from sync_vault import sync_obsidian_vault_to_chroma
        from search_context import search_semantic_context
        
        save_project_knowledge(
            project_name="AI Memory Engine",
            domain="ai",
            technologies=["Python", "ChromaDB", "ONNXRuntime"],
            strategies=["SOLID", "TDD"],
            decisions="Local embeddings adoption",
            instructions_learned="Prevent remote network calls",
            code_snippets="def get_embeddings(): pass",
            vault_path=self.temp_vault
        )
        
        sync_result = sync_obsidian_vault_to_chroma(vault_path=self.temp_vault, db_path=self.chroma_path)
        self.assertEqual(sync_result["status"], "success")
        self.assertGreaterEqual(sync_result["indexed_count"], 1)
        
        search_res = json.loads(search_semantic_context("embeddings and vector", n_results=1, vault_path=self.temp_vault))
        self.assertEqual(search_res["status"], "success")
        self.assertGreaterEqual(len(search_res["data"]), 1)

    def test_save_adr_success(self):
        """Validates ADR creation with wikilinks and decisions folder."""
        from save_knowledge import save_adr
        from search_context import search_semantic_context

        res = save_adr(
            title="Adopt SQLite over VectorDB",
            status="accepted",
            context="Need zero-latency, local search without external dependencies.",
            decision="Adopt standard library and direct markdown parsing.",
            consequences="Fast search, zero crashes, zero external deps.",
            technologies=["Python", "Markdown"],
            vault_path=self.temp_vault,
            language="es"
        )
        data = json.loads(res)
        self.assertEqual(data["status"], "success")
        self.assertTrue(os.path.exists(data["path"]))

        # Verify search finds the ADR
        search_res = json.loads(search_semantic_context("Adopt SQLite", n_results=1, vault_path=self.temp_vault))
        self.assertEqual(search_res["status"], "success")
        self.assertEqual(search_res["data"][0]["source"], data["file"])

if __name__ == "__main__":
    unittest.main()
