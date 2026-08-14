import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "05_character_animation")
BLEND_FILE = os.path.join(MODULE_DIR, "05_character_animation.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "05_character_animation.png")

class TestModule05CharacterAnimation(unittest.TestCase):
    """
    TDD Test Suite for Issue #7 (Ticket 06: Module 05 - Character Armature Rigging & Facial Shape Keys Slice)
    """

    def test_01_files_exist(self):
        """Verify 05_character_animation.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Armature Rigging, Pose Mode, 4 Facial Shape Keys, and Graph Editor."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Char_Armature", content)
            self.assertIn("Shape Keys", content)
            self.assertIn("Blink", content)
            self.assertIn("Smile", content)
            self.assertIn("OpenMouth", content)
            self.assertIn("Surprise", content)
            self.assertIn("Pose Mode", content)

    def test_03_blend_character_rig_and_shape_keys(self):
        """Verify Armature bones, facial shape keys, and timeline keyframes via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify Armature and Head objects
if "Char_Armature" not in bpy.data.objects:
    print("ERROR: Missing 'Char_Armature' object", file=sys.stderr)
    sys.exit(1)

if "Char_Head" not in bpy.data.objects:
    print("ERROR: Missing 'Char_Head' object", file=sys.stderr)
    sys.exit(2)

rig = bpy.data.objects["Char_Armature"]
head = bpy.data.objects["Char_Head"]

# Verify Pose bones
expected_bones = ["Root", "Chest", "Head", "Arm_L", "Arm_R", "Leg_L", "Leg_R"]
for b_name in expected_bones:
    if b_name not in rig.pose.bones:
        print(f"ERROR: Missing pose bone '{b_name}'", file=sys.stderr)
        sys.exit(3)

# Verify 4 Facial Shape Keys
if not head.data.shape_keys:
    print("ERROR: 'Char_Head' missing shape keys block", file=sys.stderr)
    sys.exit(4)

sk_names = [kb.name for kb in head.data.shape_keys.key_blocks]
expected_sks = ["Blink", "Smile", "OpenMouth", "Surprise"]
for sk in expected_sks:
    if sk not in sk_names:
        print(f"ERROR: Missing shape key '{sk}' in Char_Head", file=sys.stderr)
        sys.exit(5)

# Verify Animation Keyframes on Armature and Shape Keys
if not rig.animation_data or not rig.animation_data.action:
    print("ERROR: Char_Armature missing animated action/keyframes", file=sys.stderr)
    sys.exit(6)

if not head.data.shape_keys.animation_data:
    print("ERROR: Facial Shape Keys missing animated keyframes", file=sys.stderr)
    sys.exit(7)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(8)

print("Character animation and rig inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender Character Animation inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_05_dynamic_headless_render(self):
        """Verify 05_character_animation.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_05_char_dynamic.png")
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
