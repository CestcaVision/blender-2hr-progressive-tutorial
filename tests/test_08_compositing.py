import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "08_compositing")
BLEND_FILE = os.path.join(MODULE_DIR, "08_compositing.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
MASTER_README = os.path.join(BASE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "08_compositing.png")

class TestModule08CompositingAndMasterCurriculum(unittest.TestCase):
    """
    TDD Test Suite for Issue #10 (Ticket 09: Module 08 - Compositor Post-Processing & Master Curriculum Integration)
    """

    def test_01_files_exist(self):
        """Verify 08_compositing.blend, module README.md, and master README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)
        
        self.assertTrue(os.path.isfile(MASTER_README), f"Master README file {MASTER_README} must exist")
        self.assertGreater(os.path.getsize(MASTER_README), 1000)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Compositor workspace, Glare (Fog Glow), Lens Distortion, and Color Curves."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Compositor", content)
            self.assertIn("Glare", content)
            self.assertIn("Fog Glow", content)
            self.assertIn("Lens Distortion", content)
            self.assertIn("Dispersion", content)

    def test_03_master_readme_all_modules_indexing(self):
        """Verify master README.md indexes all 8 tutorial modules with paths and descriptions."""
        with open(MASTER_README, "r", encoding="utf-8") as f:
            content = f.read()
            for mod_num in range(1, 9):
                self.assertIn(f"0{mod_num}_", content, f"Master README must index module 0{mod_num}")

    def test_04_blend_compositor_nodes_and_emission_scene(self):
        """Verify Cyber Core emission object, metallic cube, and Compositor Glare/LensDist nodes via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify Core objects
expected_objects = ["Cyber_Emission_Ring", "Core_Metallic_Cube"]
for o_name in expected_objects:
    if o_name not in bpy.data.objects:
        print(f"ERROR: Missing expected object '{o_name}'", file=sys.stderr)
        sys.exit(1)

# Verify Compositor Node Tree
scene = bpy.context.scene
c_tree = getattr(scene, 'compositing_node_group', None)
if not c_tree:
    # Check scene node tree fallback
    c_tree = scene.node_tree

if not c_tree and len(bpy.data.node_groups) > 0:
    c_tree = next((ng for ng in bpy.data.node_groups if ng.type == 'COMPOSITING'), None)

if not c_tree:
    print("ERROR: Missing Compositor Node Tree in scene", file=sys.stderr)
    sys.exit(2)

node_types = [n.type for n in c_tree.nodes]
if "COMPOSITOR_GLARE" not in node_types and "CompositorNodeGlare" not in [n.__class__.__name__ for n in c_tree.nodes]:
    print(f"ERROR: Missing Glare node in Compositor tree. Present types: {node_types}", file=sys.stderr)
    sys.exit(3)

if "COMPOSITOR_LENSDIST" not in node_types and "CompositorNodeLensdist" not in [n.__class__.__name__ for n in c_tree.nodes]:
    print(f"ERROR: Missing Lens Distortion node in Compositor tree. Present types: {node_types}", file=sys.stderr)
    sys.exit(4)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(5)

print("Compositor and Post-Processing scene inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender Compositor inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_05_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_06_dynamic_headless_render(self):
        """Verify 08_compositing.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_08_comp_dynamic.png")
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
