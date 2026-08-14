import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "06_physics")
BLEND_FILE = os.path.join(MODULE_DIR, "06_physics.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "06_physics.png")

class TestModule06Physics(unittest.TestCase):
    """
    TDD Test Suite for Issue #8 (Ticket 07: Module 06 - Physics Simulation & Cloth Collision Slice)
    """

    def test_01_files_exist(self):
        """Verify 06_physics.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Rigid Body Active/Passive, Cloth Quality, Self-Collision, and Cache Baking."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Rigid Body", content)
            self.assertIn("Active", content)
            self.assertIn("Passive", content)
            self.assertIn("Cloth", content)
            self.assertIn("Self-Collision", content)
            self.assertIn("Bake", content)

    def test_03_blend_physics_rigid_body_and_cloth(self):
        """Verify Rigid Body dominos, trigger sphere, and cloth collision via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify Floor & Passive Rigid Body
if "Physics_Floor_Passive" not in bpy.data.objects:
    print("ERROR: Missing 'Physics_Floor_Passive' object", file=sys.stderr)
    sys.exit(1)

floor = bpy.data.objects["Physics_Floor_Passive"]
if not floor.rigid_body or floor.rigid_body.type != 'PASSIVE':
    print("ERROR: Floor must have PASSIVE rigid body", file=sys.stderr)
    sys.exit(2)

# Verify Trigger Ball & Active Rigid Body
if "Trigger_Ball" not in bpy.data.objects:
    print("ERROR: Missing 'Trigger_Ball' object", file=sys.stderr)
    sys.exit(3)

ball = bpy.data.objects["Trigger_Ball"]
if not ball.rigid_body or ball.rigid_body.type != 'ACTIVE' or ball.rigid_body.mass < 1.0:
    print("ERROR: Trigger_Ball must have ACTIVE rigid body with mass", file=sys.stderr)
    sys.exit(4)

# Verify Dominos
for i in range(1, 9):
    d_name = f"Domino_{i:02d}"
    if d_name not in bpy.data.objects:
        print(f"ERROR: Missing domino '{d_name}'", file=sys.stderr)
        sys.exit(5)
    domino = bpy.data.objects[d_name]
    if not domino.rigid_body or domino.rigid_body.type != 'ACTIVE':
        print(f"ERROR: Domino '{d_name}' missing ACTIVE rigid body", file=sys.stderr)
        sys.exit(6)

# Verify Pillar & Collision Modifier
if "Cloth_Collision_Pillar" not in bpy.data.objects:
    print("ERROR: Missing 'Cloth_Collision_Pillar' object", file=sys.stderr)
    sys.exit(7)

pillar = bpy.data.objects["Cloth_Collision_Pillar"]
if not any(m.type == 'COLLISION' for m in pillar.modifiers):
    print("ERROR: Pillar missing COLLISION modifier", file=sys.stderr)
    sys.exit(8)

# Verify Cloth & Settings
if "Simulated_Cloth_Silk" not in bpy.data.objects:
    print("ERROR: Missing 'Simulated_Cloth_Silk' object", file=sys.stderr)
    sys.exit(9)

cloth = bpy.data.objects["Simulated_Cloth_Silk"]
cloth_mod = next((m for m in cloth.modifiers if m.type == 'CLOTH'), None)
if not cloth_mod:
    print("ERROR: Cloth object missing CLOTH modifier", file=sys.stderr)
    sys.exit(10)

if not cloth_mod.collision_settings.use_self_collision:
    print("ERROR: Cloth modifier must enable use_self_collision", file=sys.stderr)
    sys.exit(11)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(12)

print("Physics and Cloth simulation scene inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender Physics inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_05_dynamic_headless_render(self):
        """Verify 06_physics.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_06_physics_dynamic.png")
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
