import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TUTORIALS_DIR = os.path.join(BASE_DIR, "tutorials")
RENDERS_DIR = os.path.join(BASE_DIR, "renders")

MODULES = [
    "01_modeling",
    "02_sculpting",
    "03_shading",
    "04_geometry_nodes",
    "05_character_animation",
    "06_physics",
    "07_lighting_rendering",
    "08_compositing"
]

class TestCoreHarnessAndStandards(unittest.TestCase):
    """
    Test suite for Issue #2 (Ticket 01: Core Test Harness & Project Standards)
    """

    def test_01_workspace_directory_structure(self):
        """Verify all tutorial modules and renders folders exist."""
        self.assertTrue(os.path.isdir(TUTORIALS_DIR), "Tutorials directory must exist")
        self.assertTrue(os.path.isdir(RENDERS_DIR), "Renders directory must exist")
        for mod in MODULES:
            mod_path = os.path.join(TUTORIALS_DIR, mod)
            self.assertTrue(os.path.isdir(mod_path), f"Module directory {mod} must exist")
            
            blend_file = os.path.join(mod_path, f"{mod}.blend")
            self.assertTrue(os.path.isfile(blend_file), f"Blend file {blend_file} must exist")
            self.assertGreater(os.path.getsize(blend_file), 1024, f"Blend file {blend_file} should not be empty")

            readme_file = os.path.join(mod_path, "README.md")
            self.assertTrue(os.path.isfile(readme_file), f"README file {readme_file} must exist")
            self.assertGreater(os.path.getsize(readme_file), 100, f"README file {readme_file} should have content")

    def test_02_domain_model_and_standards(self):
        """Verify CONTEXT.md and master README.md define domain ubiquitous language."""
        context_path = os.path.join(BASE_DIR, "CONTEXT.md")
        self.assertTrue(os.path.isfile(context_path), "CONTEXT.md must exist")
        with open(context_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Pure Scene Policy", content)
            self.assertIn("Scenario-Driven Pedagogy", content)

        master_readme = os.path.join(BASE_DIR, "README.md")
        self.assertTrue(os.path.isfile(master_readme), "Master README.md must exist")

    def test_03_renders_output_integrity(self):
        """Verify all 8 preview render PNG files exist and are non-empty."""
        for mod in MODULES:
            img_path = os.path.join(RENDERS_DIR, f"{mod}.png")
            self.assertTrue(os.path.isfile(img_path), f"Render output {img_path} must exist")
            self.assertGreater(os.path.getsize(img_path), 10000, f"Render output {img_path} should be a valid image file")

    def test_04_blender_cli_automation_seam(self):
        """Verify generator script runs headlessly via Blender CLI without error."""
        script_path = os.path.join(BASE_DIR, "scripts", "generate_all_projects.py")
        self.assertTrue(os.path.isfile(script_path), "Generator script must exist")
        
        cmd = ["blender", "--background", "--python", script_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender script execution failed with stderr:\n{res.stderr}\nstdout:\n{res.stdout}")
        self.assertNotIn("Traceback (most recent call last)", res.stderr, "Blender execution should not produce Python tracebacks")

if __name__ == "__main__":
    unittest.main()
