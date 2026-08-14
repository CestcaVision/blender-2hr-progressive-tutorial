import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "02_sculpting")
BLEND_FILE = os.path.join(MODULE_DIR, "02_sculpting.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "02_sculpting.png")

class TestModule02Sculpting(unittest.TestCase):
    """
    TDD Test Suite for Issue #4 (Ticket 03: Module 02 - Organic Sculpting & Multiresolution Slice)
    """

    def test_01_files_exist(self):
        """Verify 02_sculpting.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Sculpt brushes, Multiresolution, Remesh, and Symmetry."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Multiresolution", content)
            self.assertIn("Clay Strips", content)
            self.assertIn("Crease", content)
            self.assertIn("Inflate", content)
            self.assertIn("Grab", content)
            self.assertIn("Symmetry", content)

    def test_03_blend_sculpt_object_and_multires(self):
        """Verify Sculpt_Organic_Relic object and Multiresolution modifier via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify sculpt object and stand
expected_objects = [
    "Sculpt_Organic_Relic",
    "Display_Stand_Base",
    "Display_Stand_Pillar"
]

for name in expected_objects:
    if name not in bpy.data.objects:
        print(f"ERROR: Missing expected object '{name}'", file=sys.stderr)
        sys.exit(1)

sculpt_obj = bpy.data.objects["Sculpt_Organic_Relic"]
mod_types = [m.type for m in sculpt_obj.modifiers]
if "MULTIRES" not in mod_types:
    print("ERROR: Sculpt_Organic_Relic missing MULTIRES modifier", file=sys.stderr)
    sys.exit(2)

multires_mod = next(m for m in sculpt_obj.modifiers if m.type == 'MULTIRES')
if multires_mod.total_levels < 1:
    print(f"ERROR: Multires total levels {multires_mod.total_levels} should be >= 1", file=sys.stderr)
    sys.exit(3)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(4)

print("Sculpt scene inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender scene inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_05_dynamic_headless_render(self):
        """Verify 02_sculpting.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_02_sculpting_dynamic.png")
        if os.path.exists(test_out):
            os.remove(test_out)
            
        render_cmd = [
            "blender",
            BLEND_FILE,
            "--background",
            "--render-output", test_out,
            "--render-frame", "1"
        ]
        res = subprocess.run(render_cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Dynamic render failed:\n{res.stderr}\n{res.stdout}")
        
        possible_files = [test_out, test_out + "0001.png", test_out.replace(".png", "0001.png")]
        found = any(os.path.isfile(f) and os.path.getsize(f) > 5000 for f in possible_files)
        self.assertTrue(found, "Dynamic rendered output image must exist and have content")
        
        for f in possible_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    unittest.main()
