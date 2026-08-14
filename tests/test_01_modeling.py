import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "01_modeling")
BLEND_FILE = os.path.join(MODULE_DIR, "01_modeling.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "01_modeling.png")

class TestModule01Modeling(unittest.TestCase):
    """
    TDD Test Suite for Issue #3 (Ticket 02: Module 01 - Hard-Surface Poly-Modeling & Modifiers Slice)
    """

    def test_01_files_exist(self):
        """Verify .blend file and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers all core concepts and shortcuts."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Bevel", content)
            self.assertIn("Subdivision", content)
            self.assertIn("Extrude", content)
            self.assertIn("Inset", content)
            self.assertIn("Loop Cut", content)
            self.assertIn("Camera_Body", content)

    def test_03_blend_scene_structure_and_modifiers(self):
        """Verify 01_modeling.blend object hierarchy and modifier stack via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify objects in Camera_Model collection
expected_objects = [
    "Camera_Body",
    "Lens_Barrel_Base",
    "Lens_Focus_Ring",
    "Lens_Front_Element",
    "Mode_Dial",
    "Shutter_Button",
    "Power_Switch",
    "Viewfinder_Window"
]

for name in expected_objects:
    if name not in bpy.data.objects:
        print(f"ERROR: Missing expected object '{name}'", file=sys.stderr)
        sys.exit(1)

body = bpy.data.objects["Camera_Body"]
mod_types = [m.type for m in body.modifiers]
if "BEVEL" not in mod_types:
    print("ERROR: Camera_Body missing BEVEL modifier", file=sys.stderr)
    sys.exit(2)
if "SUBSURF" not in mod_types:
    print("ERROR: Camera_Body missing SUBSURF modifier", file=sys.stderr)
    sys.exit(3)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(4)

print("Scene inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender scene inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview(self):
        """Verify render preview image exists and is non-empty."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000)

if __name__ == "__main__":
    unittest.main()
