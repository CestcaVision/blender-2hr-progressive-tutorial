import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "04_geometry_nodes")
BLEND_FILE = os.path.join(MODULE_DIR, "04_geometry_nodes.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "04_geometry_nodes.png")

class TestModule04GeometryNodes(unittest.TestCase):
    """
    TDD Test Suite for Issue #6 (Ticket 05: Module 04 - Geometry Nodes Procedural Flight System Slice)
    """

    def test_01_files_exist(self):
        """Verify 04_geometry_nodes.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Geometry Nodes fields, point distribution, instancing, and noise motion."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Distribute Points", content)
            self.assertIn("Instance on Points", content)
            self.assertIn("Scene Time", content)
            self.assertIn("Noise Texture", content)
            self.assertIn("Set Position", content)
            self.assertIn("GN_Bird_Flock_System", content)

    def test_03_blend_geometry_nodes_tree_structure(self):
        """Verify GeometryNodes modifier, node tree connections, and objects via Blender headless script."""
        check_script = """
import bpy
import sys

expected_objects = [
    "GeometryNodes_Bird_Flock",
    "Bird_Asset"
]

for name in expected_objects:
    if name not in bpy.data.objects:
        print(f"ERROR: Missing expected object '{name}'", file=sys.stderr)
        sys.exit(1)

flock_obj = bpy.data.objects["GeometryNodes_Bird_Flock"]
gn_mods = [m for m in flock_obj.modifiers if m.type == 'NODES']
if not gn_mods:
    print("ERROR: GeometryNodes_Bird_Flock missing NODES modifier", file=sys.stderr)
    sys.exit(2)

node_group = gn_mods[0].node_group
if not node_group or node_group.name != "GN_Bird_Flock_System":
    print("ERROR: Expected node group 'GN_Bird_Flock_System'", file=sys.stderr)
    sys.exit(3)

# Verify key nodes in the tree
node_types = [n.type for n in node_group.nodes]
required_types = [
    "GROUP_INPUT",
    "GROUP_OUTPUT",
    "OBJECT_INFO",
    "MAP_RANGE"
]

for req in required_types:
    if req not in node_types:
        print(f"ERROR: Missing required geometry node type '{req}' in tree", file=sys.stderr)
        sys.exit(4)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(5)

print("Geometry Nodes inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender Geometry Nodes inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_05_dynamic_headless_render(self):
        """Verify 04_geometry_nodes.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_04_gn_dynamic.png")
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
