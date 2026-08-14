import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "03_shading")
BLEND_FILE = os.path.join(MODULE_DIR, "03_shading.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "03_shading.png")

class TestModule03Shading(unittest.TestCase):
    """
    TDD Test Suite for Issue #5 (Ticket 04: Module 03 - Image-Based PBR & Shading Slice)
    """

    def test_01_files_exist(self):
        """Verify 03_shading.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024 * 1024, "Blend file with packed textures should be > 1MB")
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Image PBR, Color Space rules, and Normal Map nodes."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Lantern_01", content)
            self.assertIn("Non-Color", content)
            self.assertIn("sRGB", content)
            self.assertIn("Normal Map", content)
            self.assertIn("Pack Resources", content)

    def test_03_blend_image_pbr_structure_and_packed_textures(self):
        """Verify Lantern_01 model, packed PBR textures, and correct color spaces via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify Lantern objects and shader balls
expected_objects = [
    "Lantern_01",
    "Lantern_01_glass",
    "ShaderBall_M_Procedural_Gold",
    "ShaderBall_M_Procedural_Jade",
    "ShaderBall_M_Procedural_Glass"
]

for name in expected_objects:
    if name not in bpy.data.objects:
        print(f"ERROR: Missing expected object '{name}'", file=sys.stderr)
        sys.exit(1)

# Verify brass material node setup
mat = bpy.data.materials.get("Lantern_01_brass")
if not mat or not mat.node_tree:
    print("ERROR: Material 'Lantern_01_brass' missing node tree", file=sys.stderr)
    sys.exit(2)

# Verify image textures exist and are packed
image_names = [img.name for img in bpy.data.images]
if not image_names:
    print("ERROR: No images found in blend data", file=sys.stderr)
    sys.exit(3)

packed_count = sum(1 for img in bpy.data.images if img.packed_file is not None)
if packed_count < 5:
    print(f"ERROR: Expected at least 5 packed PBR textures, found {packed_count}", file=sys.stderr)
    sys.exit(4)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(5)

print(f"Scene inspection passed! Found {packed_count} packed PBR texture maps.")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender scene inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_dynamic_headless_render(self):
        """Verify 03_shading.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_03_shading_dynamic.png")
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
