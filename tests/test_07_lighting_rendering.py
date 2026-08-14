import os
import unittest
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE_DIR = os.path.join(BASE_DIR, "tutorials", "07_lighting_rendering")
BLEND_FILE = os.path.join(MODULE_DIR, "07_lighting_rendering.blend")
README_FILE = os.path.join(MODULE_DIR, "README.md")
RENDER_PNG = os.path.join(BASE_DIR, "renders", "07_lighting_rendering.png")

class TestModule07LightingRendering(unittest.TestCase):
    """
    TDD Test Suite for Issue #9 (Ticket 08: Module 07 - Studio Three-Point Lighting & Cinematic Camera Slice)
    """

    def test_01_files_exist(self):
        """Verify 07_lighting_rendering.blend and README.md exist and have non-zero size."""
        self.assertTrue(os.path.isfile(BLEND_FILE), f"Blend file {BLEND_FILE} must exist")
        self.assertGreater(os.path.getsize(BLEND_FILE), 1024)
        
        self.assertTrue(os.path.isfile(README_FILE), f"README file {README_FILE} must exist")
        self.assertGreater(os.path.getsize(README_FILE), 200)

    def test_02_readme_curriculum_completeness(self):
        """Verify README covers Three-Point Lighting (Key, Fill, Rim), 85mm DoF, AgX, and Cycles vs EEVEE."""
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Key Light", content)
            self.assertIn("Fill Light", content)
            self.assertIn("Rim Light", content)
            self.assertIn("85mm", content)
            self.assertIn("AgX", content)
            self.assertIn("Cycles", content)
            self.assertIn("EEVEE", content)

    def test_03_blend_three_point_lights_and_cinematic_camera(self):
        """Verify Three-Point Lights, 85mm Camera with DoF, and AgX Color Management via Blender headless script."""
        check_script = """
import bpy
import sys

# Verify Three-Point Lights
expected_lights = ["Key_Light_Warm", "Fill_Light_Cool", "Rim_Light_Cyan"]
for l_name in expected_lights:
    if l_name not in bpy.data.objects:
        print(f"ERROR: Missing light object '{l_name}'", file=sys.stderr)
        sys.exit(1)

# Verify Hero Sculpture
if "Hero_Crystal_Sculpture" not in bpy.data.objects:
    print("ERROR: Missing 'Hero_Crystal_Sculpture' object", file=sys.stderr)
    sys.exit(2)

# Verify 85mm Camera with DoF
if "Cinematic_Camera_85mm" not in bpy.data.objects:
    print("ERROR: Missing 'Cinematic_Camera_85mm' object", file=sys.stderr)
    sys.exit(3)

cam_obj = bpy.data.objects["Cinematic_Camera_85mm"]
cam = cam_obj.data
if cam.lens != 85.0:
    print(f"ERROR: Expected camera focal length 85mm, got {cam.lens}", file=sys.stderr)
    sys.exit(4)

if not cam.dof.use_dof:
    print("ERROR: Camera must have Depth of Field (DoF) enabled", file=sys.stderr)
    sys.exit(5)

if cam.dof.aperture_fstop > 2.8:
    print(f"ERROR: Camera fstop {cam.dof.aperture_fstop} should be <= 2.8 for cinematic bokeh", file=sys.stderr)
    sys.exit(6)

# Verify Color Management
if bpy.context.scene.view_settings.view_transform not in ['AgX', 'Filmic']:
    print(f"ERROR: Unexpected view_transform {bpy.context.scene.view_settings.view_transform}", file=sys.stderr)
    sys.exit(7)

# Pure Scene Policy check: no 3D Text objects in scene
text_objects = [obj.name for obj in bpy.data.objects if obj.type == 'FONT']
if text_objects:
    print(f"ERROR: Violates Pure Scene Policy with text objects: {text_objects}", file=sys.stderr)
    sys.exit(8)

print("Lighting, Camera, and Color Management inspection passed!")
sys.exit(0)
"""
        cmd = ["blender", BLEND_FILE, "--background", "--python-expr", check_script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Blender Lighting & Camera inspection failed:\n{res.stderr}\n{res.stdout}")

    def test_04_render_preview_integrity(self):
        """Verify committed render preview exists and has valid image size."""
        self.assertTrue(os.path.isfile(RENDER_PNG), f"Render output {RENDER_PNG} must exist")
        self.assertGreater(os.path.getsize(RENDER_PNG), 10000, "Render output should be a valid PNG image")

    def test_05_dynamic_headless_render(self):
        """Verify 07_lighting_rendering.blend renders dynamically without errors via Blender CLI."""
        test_out = os.path.join(BASE_DIR, "renders", "test_07_lighting_dynamic.png")
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
