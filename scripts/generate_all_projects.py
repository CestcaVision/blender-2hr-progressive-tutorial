import bpy
import math
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TUTORIALS_DIR = os.path.join(BASE_DIR, "tutorials")
RENDERS_DIR = os.path.join(BASE_DIR, "renders")
os.makedirs(RENDERS_DIR, exist_ok=True)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not bpy.data.scenes:
        bpy.data.scenes.new("Scene")

def setup_basic_camera_and_light(cam_loc=(0, -6, 3), cam_rot=(math.radians(65), 0, 0), light_loc=(4, -4, 5)):
    scene = bpy.context.scene
    # Camera
    cam_data = bpy.data.cameras.new("Main_Camera")
    cam_obj = bpy.data.objects.new("Main_Camera", cam_data)
    cam_obj.location = cam_loc
    cam_obj.rotation_euler = cam_rot
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Key Light
    light_data = bpy.data.lights.new("Key_Light", type='AREA')
    light_data.energy = 400
    light_data.size = 2.5
    light_obj = bpy.data.objects.new("Key_Light", light_data)
    light_obj.location = light_loc
    light_obj.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))
    scene.collection.objects.link(light_obj)

    # Fill Light
    fill_data = bpy.data.lights.new("Fill_Light", type='POINT')
    fill_data.energy = 100
    fill_data.color = (0.7, 0.85, 1.0)
    fill_obj = bpy.data.objects.new("Fill_Light", fill_data)
    fill_obj.location = (-4, -3, 2)
    scene.collection.objects.link(fill_obj)

def render_preview(filename):
    scene = bpy.context.scene
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    out_img = os.path.join(RENDERS_DIR, filename)
    scene.render.filepath = out_img
    bpy.ops.render.render(write_still=True)
    print(f"Rendered Preview: {out_img}")

# ----------------------------------------------------
# 01. Hard Surface Modeling: Vintage Camera
# ----------------------------------------------------
def build_01_modeling():
    print("--- Building 01: Hard Surface Modeling ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -3.5, 1.8), cam_rot=(math.radians(70), 0, 0), light_loc=(2, -3, 3))
    
    # Camera Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.6))
    body = bpy.context.active_object
    body.name = "Camera_Body"
    body.scale = (1.6, 0.6, 0.9)
    bpy.ops.object.transform_apply(scale=True)
    
    # Bevel Modifier
    bevel = body.modifiers.new("Bevel", 'BEVEL')
    bevel.width = 0.05
    bevel.segments = 4
    
    # Subdiv Modifier
    subdiv = body.modifiers.new("Subdivision", 'SUBSURF')
    subdiv.levels = 1
    subdiv.render_levels = 2
    
    # Camera Lens Mount & Barrel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.5, location=(0, -0.45, 0.6), rotation=(math.radians(90), 0, 0))
    lens_base = bpy.context.active_object
    lens_base.name = "Lens_Barrel_Base"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.4, location=(0, -0.75, 0.6), rotation=(math.radians(90), 0, 0))
    lens_ring = bpy.context.active_object
    lens_ring.name = "Lens_Focus_Ring"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.1, location=(0, -0.92, 0.6), rotation=(math.radians(90), 0, 0))
    lens_glass = bpy.context.active_object
    lens_glass.name = "Lens_Front_Element"
    
    # Dials & Shutter
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.15, location=(-0.5, 0, 1.12))
    dial_left = bpy.context.active_object
    dial_left.name = "Mode_Dial"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.2, location=(0.4, 0, 1.15))
    shutter = bpy.context.active_object
    shutter.name = "Shutter_Button"
    
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.6, -0.1, 1.1))
    power_switch = bpy.context.active_object
    power_switch.name = "Power_Switch"
    power_switch.scale = (0.6, 0.8, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Viewfinder
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(-0.45, -0.32, 0.95))
    viewfinder = bpy.context.active_object
    viewfinder.name = "Viewfinder_Window"
    viewfinder.scale = (1.2, 0.3, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Materials
    mat_metal = bpy.data.materials.new(name="M_Camera_Metal")
    bsdf_m = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs["Base Color"].default_value = (0.7, 0.7, 0.72, 1.0)
        bsdf_m.inputs["Metallic"].default_value = 0.9
        bsdf_m.inputs["Roughness"].default_value = 0.25
    body.data.materials.append(mat_metal)
    dial_left.data.materials.append(mat_metal)
    shutter.data.materials.append(mat_metal)
    power_switch.data.materials.append(mat_metal)
    lens_base.data.materials.append(mat_metal)
    
    mat_grip = bpy.data.materials.new(name="M_Leather_Grip")
    bsdf_g = mat_grip.node_tree.nodes.get("Principled BSDF")
    if bsdf_g:
        bsdf_g.inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf_g.inputs["Roughness"].default_value = 0.7
    lens_ring.data.materials.append(mat_grip)
    
    col = bpy.data.collections.new("Camera_Model")
    bpy.context.scene.collection.children.link(col)
    for obj in [body, lens_base, lens_ring, lens_glass, dial_left, shutter, power_switch, viewfinder]:
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        col.objects.link(obj)
        
    out_path = os.path.join(TUTORIALS_DIR, "01_modeling", "01_modeling.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("01_modeling.png")

# ----------------------------------------------------
# 02. Sculpting: Fantasy Medallion / Relic
# ----------------------------------------------------
def build_02_sculpting():
    print("--- Building 02: Sculpting & Organic Form ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -3.2, 1.5), cam_rot=(math.radians(72), 0, 0), light_loc=(2.5, -3, 3.5))
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0, 0, 0.8))
    sculpt_obj = bpy.context.active_object
    sculpt_obj.name = "Sculpt_Organic_Relic"
    sculpt_obj.scale = (1.1, 0.35, 1.4)
    bpy.ops.object.transform_apply(scale=True)
    
    multires = sculpt_obj.modifiers.new("Multiresolution", 'MULTIRES')
    bpy.ops.object.multires_subdivide(modifier="Multiresolution", mode='CATMULL_CLARK')
    bpy.ops.object.multires_subdivide(modifier="Multiresolution", mode='CATMULL_CLARK')
    bpy.ops.object.multires_subdivide(modifier="Multiresolution", mode='CATMULL_CLARK')
    
    # Stand
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=0.2, location=(0, 0, 0.1))
    stand_base = bpy.context.active_object
    stand_base.name = "Display_Stand_Base"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.7, location=(0, 0, 0.45))
    stand_pole = bpy.context.active_object
    stand_pole.name = "Display_Stand_Pillar"
    
    mat_relic = bpy.data.materials.new(name="M_Ancient_Stone")
    bsdf_r = mat_relic.node_tree.nodes.get("Principled BSDF")
    if bsdf_r:
        bsdf_r.inputs["Base Color"].default_value = (0.45, 0.42, 0.38, 1.0)
        bsdf_r.inputs["Roughness"].default_value = 0.8
    sculpt_obj.data.materials.append(mat_relic)
    
    bpy.context.view_layer.objects.active = sculpt_obj
    sculpt_obj.select_set(True)
    try:
        bpy.ops.object.mode_set(mode='SCULPT')
    except Exception as e:
        print("Set sculpt mode notice:", e)
    
    out_path = os.path.join(TUTORIALS_DIR, "02_sculpting", "02_sculpting.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("02_sculpting.png")

# ----------------------------------------------------
# 03. Shading & PBR Materials: Image-Based PBR & Procedural Showcase
# ----------------------------------------------------
def build_03_shading():
    print("--- Building 03: Shading & PBR Materials (Image PBR + Procedural) ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -6.5, 2.5), cam_rot=(math.radians(70), 0, 0), light_loc=(3, -4, 4))
    
    # 1. Import Hero CC0 Image-Based PBR Model: Vintage Lantern
    cache_blend = os.path.join(BASE_DIR, ".cache_pbr", "Lantern_01_1k.blend")
    tex_dir = os.path.join(BASE_DIR, ".cache_pbr", "textures")
    
    if os.path.exists(cache_blend):
        with bpy.data.libraries.load(cache_blend, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name in ["Lantern_01", "Lantern_01_glass"]]
            
        for obj in data_to.objects:
            if obj:
                bpy.context.scene.collection.objects.link(obj)
                obj.location = (-1.6, 0, 0.1)
                obj.scale = (1.5, 1.5, 1.5)
                
        # Configure Brass Material Image Textures explicitly for crystal clear teaching
        mat_brass = bpy.data.materials.get("Lantern_01_brass")
        if mat_brass and mat_brass.node_tree:
            nodes = mat_brass.node_tree.nodes
            links = mat_brass.node_tree.links
            bsdf = nodes.get("Principled BSDF")
            
            # Helper to load and wire image
            def wire_image_tex(img_filename, color_space, target_socket, is_normal=False):
                img_path = os.path.join(tex_dir, img_filename)
                if os.path.exists(img_path):
                    img = bpy.data.images.load(img_path, check_existing=True)
                    img.colorspace_settings.name = color_space
                    tex_node = nodes.new("ShaderNodeTexImage")
                    tex_node.image = img
                    if is_normal:
                        norm_node = nodes.new("ShaderNodeNormalMap")
                        links.new(tex_node.outputs["Color"], norm_node.inputs["Color"])
                        links.new(norm_node.outputs["Normal"], bsdf.inputs["Normal"])
                    else:
                        links.new(tex_node.outputs["Color"], bsdf.inputs[target_socket])
                        
            wire_image_tex("Lantern_01_brass_diff_1k.png", "sRGB", "Base Color")
            wire_image_tex("Lantern_01_brass_roughness_1k.png", "Non-Color", "Roughness")
            wire_image_tex("Lantern_01_brass_metallic_1k.png", "Non-Color", "Metallic")
            wire_image_tex("Lantern_01_brass_opacity_1k.png", "Non-Color", "Alpha")
            wire_image_tex("Lantern_01_brass_nor_gl_1k.png", "Non-Color", "Normal", is_normal=True)
    
    # 2. Side-by-Side Procedural Comparison Shader Balls
    mat_configs = [
        {"name": "M_Procedural_Gold", "loc": (0.8, 0, 0.8), "type": "gold"},
        {"name": "M_Procedural_Jade", "loc": (2.2, 0, 0.8), "type": "jade"},
        {"name": "M_Procedural_Glass", "loc": (3.6, 0, 0.8), "type": "glass"}
    ]
    
    # Floor Studio Backdrop
    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Studio_Backdrop"
    floor_mat = bpy.data.materials.new(name="M_Studio_Backdrop")
    bsdf_floor = floor_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = (0.08, 0.08, 0.09, 1.0)
        bsdf_floor.inputs["Roughness"].default_value = 0.4
    floor.data.materials.append(floor_mat)
    
    for cfg in mat_configs:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.6, location=cfg["loc"])
        orb = bpy.context.active_object
        orb.name = f"ShaderBall_{cfg['name']}"
        bpy.ops.object.shade_smooth()
        
        mat = bpy.data.materials.new(name=cfg["name"])
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        node_out = nodes.new(type="ShaderNodeOutputMaterial")
        node_out.location = (400, 0)
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)
        links.new(bsdf.outputs["BSDF"], node_out.inputs["Surface"])
        
        tex_noise = nodes.new(type="ShaderNodeTexNoise")
        tex_noise.location = (-500, 100)
        tex_noise.inputs["Scale"].default_value = 15.0
        tex_noise.inputs["Detail"].default_value = 6.0
        
        bump = nodes.new(type="ShaderNodeBump")
        bump.location = (-200, -100)
        bump.inputs["Strength"].default_value = 0.15
        links.new(tex_noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
        
        if cfg["type"] == "gold":
            bsdf.inputs["Base Color"].default_value = (1.0, 0.78, 0.28, 1.0)
            bsdf.inputs["Metallic"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.25
        elif cfg["type"] == "jade":
            bsdf.inputs["Base Color"].default_value = (0.1, 0.85, 0.4, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.2
            if "Subsurface Weight" in bsdf.inputs:
                bsdf.inputs["Subsurface Weight"].default_value = 0.8
                bsdf.inputs["Subsurface Radius"].default_value = (0.2, 0.5, 0.1)
            elif "Subsurface" in bsdf.inputs:
                bsdf.inputs["Subsurface"].default_value = 0.8
        elif cfg["type"] == "glass":
            bsdf.inputs["Base Color"].default_value = (0.95, 0.98, 1.0, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.05
            bsdf.inputs["IOR"].default_value = 1.52
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = 1.0
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = 1.0
                
        orb.data.materials.append(mat)
        
    # 3. Pack all image textures inside the .blend file (Zero Missing Texture Guarantee)
    try:
        bpy.ops.file.pack_all()
        print("All PBR image textures packed into .blend!")
    except Exception as e:
        print("Pack images notice:", e)
        
    out_path = os.path.join(TUTORIALS_DIR, "03_shading", "03_shading.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("03_shading.png")

# ----------------------------------------------------
# 04. Geometry Nodes: Bird Flock Simulation
# ----------------------------------------------------
def build_04_geometry_nodes():
    print("--- Building 04: Geometry Nodes Bird Flock (4D Volume Flight) ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -14, 6), cam_rot=(math.radians(72), 0, 0), light_loc=(6, -10, 10))
    
    # 1. Base Bird Model
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.2, radius2=0.02, depth=0.8, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    bird_body = bpy.context.active_object
    bird_body.name = "Bird_Instance_Template"
    
    bpy.ops.mesh.primitive_plane_add(size=0.8, location=(0, 0, 0.05))
    bird_wings = bpy.context.active_object
    bird_wings.name = "Bird_Wings"
    bird_wings.scale = (2.2, 0.4, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.context.view_layer.objects.active = bird_body
    bird_wings.select_set(True)
    bird_body.select_set(True)
    bpy.ops.object.join()
    bird_model = bpy.context.active_object
    bird_model.name = "Bird_Asset"
    bird_model.location = (0, 0, -50)
    
    mat_bird = bpy.data.materials.new(name="M_Bird_Feathers")
    bsdf = mat_bird.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.05, 0.06, 0.08, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.6
    bird_model.data.materials.append(mat_bird)
    
    # 2. Flock Generator Object
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2))
    flock_obj = bpy.context.active_object
    flock_obj.name = "GeometryNodes_Bird_Flock"
    
    gn_mod = flock_obj.modifiers.new("GeometryNodes", 'NODES')
    node_group = bpy.data.node_groups.new("GN_Bird_Flock_System", 'GeometryNodeTree')
    gn_mod.node_group = node_group
    
    node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    
    nodes = node_group.nodes
    links = node_group.links
    nodes.clear()
    
    n_in = nodes.new("NodeGroupInput")
    n_in.location = (-800, 0)
    
    n_out = nodes.new("NodeGroupOutput")
    n_out.location = (700, 0)
    
    # Volume Generation & Point Distribution in 3D Space
    n_cube = nodes.new("GeometryNodeMeshCube")
    n_cube.location = (-600, 150)
    n_cube.inputs["Size"].default_value = (14.0, 10.0, 5.0)
    
    n_dist = nodes.new("GeometryNodeDistributePointsOnFaces")
    n_dist.location = (-350, 150)
    n_dist.inputs["Density"].default_value = 1.5
    
    # Set Position & 4D Fluid Flight Turbulence Field
    n_time = nodes.new("GeometryNodeInputSceneTime")
    n_time.location = (-600, -150)
    
    n_math_time = nodes.new("ShaderNodeMath")
    n_math_time.location = (-400, -150)
    n_math_time.operation = 'MULTIPLY'
    n_math_time.inputs[1].default_value = 0.5  # Time speed control
    
    n_noise = nodes.new("ShaderNodeTexNoise")
    n_noise.location = (-200, -150)
    n_noise.noise_dimensions = '4D'
    n_noise.inputs["Scale"].default_value = 0.35
    n_noise.inputs["Detail"].default_value = 2.0
    
    # Vector Math to center and scale displacement
    n_vmath = nodes.new("ShaderNodeVectorMath")
    n_vmath.location = (50, -150)
    n_vmath.operation = 'SCALE'
    n_vmath.inputs["Scale"].default_value = 1.8
    
    n_pos = nodes.new("GeometryNodeSetPosition")
    n_pos.location = (50, 150)
    
    # Instance on Points
    n_inst = nodes.new("GeometryNodeInstanceOnPoints")
    n_inst.location = (280, 150)
    
    n_obj_info = nodes.new("GeometryNodeObjectInfo")
    n_obj_info.location = (50, 0)
    n_obj_info.inputs["Object"].default_value = bird_model
    if "As Instance" in n_obj_info.inputs:
        n_obj_info.inputs["As Instance"].default_value = True
        
    n_scale = nodes.new("GeometryNodeScaleInstances")
    n_scale.location = (480, 150)
    n_scale.inputs["Scale"].default_value = (0.5, 0.5, 0.5)
    
    # Node Links
    links.new(n_cube.outputs["Mesh"], n_dist.inputs["Mesh"])
    links.new(n_dist.outputs["Points"], n_pos.inputs["Geometry"])
    
    # 4D Noise Time Link (Scene Time -> Math Speed -> Noise W -> Vector Scale -> Set Position Offset)
    links.new(n_time.outputs["Seconds"], n_math_time.inputs[0])
    links.new(n_math_time.outputs["Value"], n_noise.inputs["W"])
    links.new(n_noise.outputs["Color"], n_vmath.inputs["Vector"])
    links.new(n_vmath.outputs["Vector"], n_pos.inputs["Offset"])
    
    # Instancing links
    links.new(n_pos.outputs["Geometry"], n_inst.inputs["Points"])
    links.new(n_obj_info.outputs["Geometry"], n_inst.inputs["Instance"])
    links.new(n_inst.outputs["Instances"], n_scale.inputs["Instances"])
    links.new(n_scale.outputs["Instances"], n_out.inputs["Geometry"])
    
    out_path = os.path.join(TUTORIALS_DIR, "04_geometry_nodes", "04_geometry_nodes.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("04_geometry_nodes.png")

# ----------------------------------------------------
# 05. Character Animation: Rigging & Facial Shape Keys
# ----------------------------------------------------
def build_05_character_animation():
    print("--- Building 05: Character Animation & Rigging ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -4.5, 1.6), cam_rot=(math.radians(78), 0, 0), light_loc=(2.5, -3, 3))
    
    # Head with Facial Shape Keys
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.45, location=(0, 0, 1.7))
    head = bpy.context.active_object
    head.name = "Char_Head"
    bpy.ops.object.shade_smooth()
    
    head.shape_key_add(name="Basis")
    sk_blink = head.shape_key_add(name="Blink")
    sk_smile = head.shape_key_add(name="Smile")
    sk_mouth_open = head.shape_key_add(name="OpenMouth")
    sk_surprise = head.shape_key_add(name="Surprise")
    
    for v in sk_blink.data:
        if v.co.y < 0 and abs(v.co.z - 1.7) < 0.15:
            v.co.z = 1.7 + (v.co.z - 1.7) * 0.1
            
    for v in sk_smile.data:
        if v.co.y < -0.1 and v.co.z < 1.6:
            v.co.z += 0.08 * (1.0 - abs(v.co.x))
            v.co.x *= 1.2
            
    for v in sk_mouth_open.data:
        if v.co.y < -0.1 and v.co.z < 1.65:
            v.co.z -= 0.12
            v.co.y -= 0.05
            
    for v in sk_surprise.data:
        if v.co.z > 1.7:
            v.co.z += 0.1
        if v.co.y < -0.1 and v.co.z < 1.6:
            v.co.z -= 0.08
            
    # Eyes
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(-0.16, -0.4, 1.75))
    eye_l = bpy.context.active_object
    eye_l.name = "Char_Eye_L"
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(0.16, -0.4, 1.75))
    eye_r = bpy.context.active_object
    eye_r.name = "Char_Eye_R"
    
    # Torso
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 0, 1.05))
    torso = bpy.context.active_object
    torso.name = "Char_Torso"
    torso.scale = (0.7, 0.5, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Arms
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.65, location=(-0.45, 0, 1.0), rotation=(0, math.radians(20), 0))
    arm_l = bpy.context.active_object
    arm_l.name = "Char_Arm_L"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.65, location=(0.45, 0, 1.0), rotation=(0, math.radians(-20), 0))
    arm_r = bpy.context.active_object
    arm_r.name = "Char_Arm_R"
    
    # Legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.75, location=(-0.2, 0, 0.4))
    leg_l = bpy.context.active_object
    leg_l.name = "Char_Leg_L"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.75, location=(0.2, 0, 0.4))
    leg_r = bpy.context.active_object
    leg_r.name = "Char_Leg_R"
    
    # Materials
    mat_skin = bpy.data.materials.new(name="M_Char_Skin")
    bsdf_skin = mat_skin.node_tree.nodes.get("Principled BSDF")
    if bsdf_skin:
        bsdf_skin.inputs["Base Color"].default_value = (0.96, 0.76, 0.65, 1.0)
        bsdf_skin.inputs["Roughness"].default_value = 0.4
    head.data.materials.append(mat_skin)
    
    mat_suit = bpy.data.materials.new(name="M_Char_Suit")
    bsdf_suit = mat_suit.node_tree.nodes.get("Principled BSDF")
    if bsdf_suit:
        bsdf_suit.inputs["Base Color"].default_value = (0.1, 0.4, 0.8, 1.0)
        bsdf_suit.inputs["Roughness"].default_value = 0.3
    torso.data.materials.append(mat_suit)
    arm_l.data.materials.append(mat_suit)
    arm_r.data.materials.append(mat_suit)
    leg_l.data.materials.append(mat_suit)
    leg_r.data.materials.append(mat_suit)
    
    mat_eye = bpy.data.materials.new(name="M_Char_Eye")
    bsdf_eye = mat_eye.node_tree.nodes.get("Principled BSDF")
    if bsdf_eye:
        bsdf_eye.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
        bsdf_eye.inputs["Roughness"].default_value = 0.1
    eye_l.data.materials.append(mat_eye)
    eye_r.data.materials.append(mat_eye)

    # Armature Rig
    bpy.ops.object.armature_add(location=(0, 0, 0))
    rig = bpy.context.active_object
    rig.name = "Char_Armature"
    rig.show_in_front = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    eb = rig.data.edit_bones
    
    b_root = eb[0]
    b_root.name = "Root"
    b_root.head = (0, 0, 0.75)
    b_root.tail = (0, 0, 1.05)
    
    b_chest = eb.new("Chest")
    b_chest.head = (0, 0, 1.05)
    b_chest.tail = (0, 0, 1.4)
    b_chest.parent = b_root
    
    b_head = eb.new("Head")
    b_head.head = (0, 0, 1.4)
    b_head.tail = (0, 0, 2.1)
    b_head.parent = b_chest
    
    b_arm_l = eb.new("Arm_L")
    b_arm_l.head = (-0.25, 0, 1.35)
    b_arm_l.tail = (-0.55, 0, 0.75)
    b_arm_l.parent = b_chest
    
    b_arm_r = eb.new("Arm_R")
    b_arm_r.head = (0.25, 0, 1.35)
    b_arm_r.tail = (0.55, 0, 0.75)
    b_arm_r.parent = b_chest
    
    b_leg_l = eb.new("Leg_L")
    b_leg_l.head = (-0.2, 0, 0.75)
    b_leg_l.tail = (-0.2, 0, 0.0)
    b_leg_l.parent = b_root
    
    b_leg_r = eb.new("Leg_R")
    b_leg_r.head = (0.2, 0, 0.75)
    b_leg_r.tail = (0.2, 0, 0.0)
    b_leg_r.parent = b_root
    
    # Bone Parenting for articulated character hierarchy
    head.parent = rig
    head.parent_type = 'BONE'
    head.parent_bone = 'Head'
    
    eye_l.parent = head
    eye_r.parent = head
    
    torso.parent = rig
    torso.parent_type = 'BONE'
    torso.parent_bone = 'Chest'
    
    arm_l.parent = rig
    arm_l.parent_type = 'BONE'
    arm_l.parent_bone = 'Arm_L'
    
    arm_r.parent = rig
    arm_r.parent_type = 'BONE'
    arm_r.parent_bone = 'Arm_R'
    
    leg_l.parent = rig
    leg_l.parent_type = 'BONE'
    leg_l.parent_bone = 'Leg_L'
    
    leg_r.parent = rig
    leg_r.parent_type = 'BONE'
    leg_r.parent_bone = 'Leg_R'
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Keyframes: Facial Shape Keys (Frames 1-120)
    sk_blink.value = 0.0
    sk_blink.keyframe_insert(data_path="value", frame=1)
    sk_blink.value = 1.0
    sk_blink.keyframe_insert(data_path="value", frame=25)
    sk_blink.value = 0.0
    sk_blink.keyframe_insert(data_path="value", frame=35)
    
    sk_smile.value = 0.0
    sk_smile.keyframe_insert(data_path="value", frame=1)
    sk_smile.value = 1.0
    sk_smile.keyframe_insert(data_path="value", frame=45)
    sk_smile.value = 0.0
    sk_smile.keyframe_insert(data_path="value", frame=75)
    
    sk_mouth_open.value = 0.0
    sk_mouth_open.keyframe_insert(data_path="value", frame=40)
    sk_mouth_open.value = 0.8
    sk_mouth_open.keyframe_insert(data_path="value", frame=55)
    sk_mouth_open.value = 0.0
    sk_mouth_open.keyframe_insert(data_path="value", frame=70)
    
    sk_surprise.value = 0.0
    sk_surprise.keyframe_insert(data_path="value", frame=75)
    sk_surprise.value = 1.0
    sk_surprise.keyframe_insert(data_path="value", frame=95)
    sk_surprise.value = 0.0
    sk_surprise.keyframe_insert(data_path="value", frame=120)
    
    # Armature Wave Keyframes (Frames 1-120)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')
    pb_arm_r = rig.pose.bones.get("Arm_R")
    if pb_arm_r:
        pb_arm_r.rotation_mode = 'XYZ'
        pb_arm_r.rotation_euler = (0, 0, 0)
        pb_arm_r.keyframe_insert(data_path="rotation_euler", frame=1)
        pb_arm_r.rotation_euler = (0, 0, math.radians(110))
        pb_arm_r.keyframe_insert(data_path="rotation_euler", frame=30)
        pb_arm_r.rotation_euler = (0, math.radians(30), math.radians(130))
        pb_arm_r.keyframe_insert(data_path="rotation_euler", frame=50)
        pb_arm_r.rotation_euler = (0, math.radians(-30), math.radians(100))
        pb_arm_r.keyframe_insert(data_path="rotation_euler", frame=70)
        pb_arm_r.rotation_euler = (0, 0, 0)
        pb_arm_r.keyframe_insert(data_path="rotation_euler", frame=120)
        
    bpy.context.scene.frame_end = 120
    out_path = os.path.join(TUTORIALS_DIR, "05_character_animation", "05_character_animation.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("05_character_animation.png")

# ----------------------------------------------------
# 06. Physics Simulation
# ----------------------------------------------------
def build_06_physics():
    print("--- Building 06: Physics Simulation ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -6.5, 3.5), cam_rot=(math.radians(65), 0, 0), light_loc=(4, -5, 6))
    
    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Physics_Floor_Passive"
    bpy.ops.rigidbody.object_add()
    floor.rigid_body.type = 'PASSIVE'
    
    # Materials for Physics Scene
    mat_floor = bpy.data.materials.new(name="M_Physics_Floor")
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = (0.08, 0.09, 0.11, 1.0)
        bsdf_floor.inputs["Roughness"].default_value = 0.5
    floor.data.materials.append(mat_floor)
    
    mat_domino = bpy.data.materials.new(name="M_Domino_Active")
    bsdf_domino = mat_domino.node_tree.nodes.get("Principled BSDF")
    if bsdf_domino:
        bsdf_domino.inputs["Base Color"].default_value = (0.85, 0.15, 0.15, 1.0)
        bsdf_domino.inputs["Roughness"].default_value = 0.25
        
    for i in range(8):
        y_pos = -2.5 + i * 0.65
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y_pos, 0.45))
        domino = bpy.context.active_object
        domino.name = f"Domino_{i+1:02d}"
        domino.scale = (0.5, 0.12, 0.9)
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.rigidbody.object_add()
        domino.rigid_body.type = 'ACTIVE'
        domino.rigid_body.mass = 1.0
        domino.rigid_body.friction = 0.5
        domino.data.materials.append(mat_domino)
        
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, -3.2, 1.2))
    ball = bpy.context.active_object
    ball.name = "Trigger_Ball"
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.type = 'ACTIVE'
    ball.rigid_body.mass = 5.0
    mat_ball = bpy.data.materials.new(name="M_Trigger_Ball")
    bsdf_ball = mat_ball.node_tree.nodes.get("Principled BSDF")
    if bsdf_ball:
        bsdf_ball.inputs["Base Color"].default_value = (0.9, 0.6, 0.2, 1.0)
        bsdf_ball.inputs["Metallic"].default_value = 1.0
        bsdf_ball.inputs["Roughness"].default_value = 0.2
    ball.data.materials.append(mat_ball)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1.2, location=(2.8, 0, 0.6))
    pillar = bpy.context.active_object
    pillar.name = "Cloth_Collision_Pillar"
    bpy.ops.object.modifier_add(type='COLLISION')
    mat_pillar = bpy.data.materials.new(name="M_Collision_Pillar")
    bsdf_pillar = mat_pillar.node_tree.nodes.get("Principled BSDF")
    if bsdf_pillar:
        bsdf_pillar.inputs["Base Color"].default_value = (0.7, 0.72, 0.75, 1.0)
        bsdf_pillar.inputs["Roughness"].default_value = 0.3
    pillar.data.materials.append(mat_pillar)
    
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=24, y_subdivisions=24, size=1.5, location=(2.8, 0, 1.5))
    cloth = bpy.context.active_object
    cloth.name = "Simulated_Cloth_Silk"
    cloth_mod = cloth.modifiers.new("Cloth", 'CLOTH')
    cloth_mod.settings.quality = 5
    cloth_mod.settings.mass = 0.2
    cloth_mod.collision_settings.use_collision = True
    cloth_mod.collision_settings.use_self_collision = True
    cloth_mod.point_cache.frame_start = 1
    cloth_mod.point_cache.frame_end = 150
    
    subdiv = cloth.modifiers.new("Subdivision", 'SUBSURF')
    subdiv.levels = 1
    
    mat_cloth = bpy.data.materials.new(name="M_Simulated_Cloth")
    bsdf_cloth = mat_cloth.node_tree.nodes.get("Principled BSDF")
    if bsdf_cloth:
        bsdf_cloth.inputs["Base Color"].default_value = (0.1, 0.6, 0.8, 1.0)
        bsdf_cloth.inputs["Roughness"].default_value = 0.4
        if "Sheen Weight" in bsdf_cloth.inputs:
            bsdf_cloth.inputs["Sheen Weight"].default_value = 1.0
        elif "Sheen" in bsdf_cloth.inputs:
            bsdf_cloth.inputs["Sheen"].default_value = 1.0
    cloth.data.materials.append(mat_cloth)
    
    bpy.context.scene.frame_end = 150
    out_path = os.path.join(TUTORIALS_DIR, "06_physics", "06_physics.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("06_physics.png")

# ----------------------------------------------------
# 07. Lighting, Camera & Rendering
# ----------------------------------------------------
def build_07_lighting_rendering():
    print("--- Building 07: Lighting, Camera & Rendering ---")
    clear_scene()
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.film_transparent = False
    
    # Hero Object: Crystal Sculpture
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=(0, 0, 1.2))
    hero = bpy.context.active_object
    hero.name = "Hero_Crystal_Sculpture"
    bpy.ops.object.shade_flat()
    
    mat_hero = bpy.data.materials.new(name="M_Hero_Crystal")
    bsdf_hero = mat_hero.node_tree.nodes.get("Principled BSDF")
    if bsdf_hero:
        bsdf_hero.inputs["Base Color"].default_value = (0.1, 0.6, 0.95, 1.0)
        bsdf_hero.inputs["Roughness"].default_value = 0.05
        bsdf_hero.inputs["IOR"].default_value = 1.65
        if "Transmission Weight" in bsdf_hero.inputs:
            bsdf_hero.inputs["Transmission Weight"].default_value = 0.95
        elif "Transmission" in bsdf_hero.inputs:
            bsdf_hero.inputs["Transmission"].default_value = 0.95
    hero.data.materials.append(mat_hero)
    
    # Studio Backdrop
    bpy.ops.mesh.primitive_plane_add(size=16, location=(0, 0, 0))
    backdrop = bpy.context.active_object
    backdrop.name = "Curved_Studio_Backdrop"
    mat_back = bpy.data.materials.new(name="M_Dark_Studio_Floor")
    bsdf_back = mat_back.node_tree.nodes.get("Principled BSDF")
    if bsdf_back:
        bsdf_back.inputs["Base Color"].default_value = (0.03, 0.03, 0.04, 1.0)
        bsdf_back.inputs["Roughness"].default_value = 0.2
    backdrop.data.materials.append(mat_back)
    
    # Three-Point Lighting Setup
    key_data = bpy.data.lights.new("Key_Light_Warm", type='AREA')
    key_data.energy = 500
    key_data.size = 2.5
    key_data.color = (1.0, 0.9, 0.75)
    key_obj = bpy.data.objects.new("Key_Light_Warm", key_data)
    key_obj.location = (3.5, -3.5, 4.0)
    key_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))
    scene.collection.objects.link(key_obj)
    
    fill_data = bpy.data.lights.new("Fill_Light_Cool", type='AREA')
    fill_data.energy = 150
    fill_data.size = 4.0
    fill_data.color = (0.65, 0.8, 1.0)
    fill_obj = bpy.data.objects.new("Fill_Light_Cool", fill_data)
    fill_obj.location = (-4.0, -2.5, 2.5)
    fill_obj.rotation_euler = (math.radians(60), math.radians(-15), math.radians(45))
    scene.collection.objects.link(fill_obj)
    
    rim_data = bpy.data.lights.new("Rim_Light_Cyan", type='SPOT')
    rim_data.energy = 800
    rim_data.spot_size = math.radians(50)
    rim_data.spot_blend = 0.4
    rim_data.color = (0.2, 0.9, 1.0)
    rim_obj = bpy.data.objects.new("Rim_Light_Cyan", rim_data)
    rim_obj.location = (-2.0, 3.5, 3.5)
    rim_obj.rotation_euler = (math.radians(-45), math.radians(-20), math.radians(160))
    scene.collection.objects.link(rim_obj)
    
    # Cinematic Camera with DoF
    cam_data = bpy.data.cameras.new("Cinematic_Camera_85mm")
    cam_data.lens = 85.0
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = hero
    cam_data.dof.aperture_fstop = 2.0
    cam_obj = bpy.data.objects.new("Cinematic_Camera_85mm", cam_data)
    cam_obj.location = (0, -4.8, 1.5)
    cam_obj.rotation_euler = (math.radians(82), 0, 0)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Color Management (AgX / Medium High Contrast)
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium High Contrast'
    except Exception as e:
        print("Set look notice:", e)
        
    out_path = os.path.join(TUTORIALS_DIR, "07_lighting_rendering", "07_lighting_rendering.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("07_lighting_rendering.png")

# ----------------------------------------------------
# 08. Compositing Pipeline
# ----------------------------------------------------
def build_08_compositing():
    print("--- Building 08: Compositing Pipeline ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -4.5, 2.0), cam_rot=(math.radians(72), 0, 0), light_loc=(3, -3, 4))
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.15, location=(0, 0, 1.2))
    ring = bpy.context.active_object
    ring.name = "Cyber_Emission_Ring"
    
    mat_ring = bpy.data.materials.new(name="M_Emission_Neon_Cyan")
    nodes = mat_ring.node_tree.nodes
    links = mat_ring.node_tree.links
    nodes.clear()
    n_out = nodes.new("ShaderNodeOutputMaterial")
    n_emit = nodes.new("ShaderNodeEmission")
    n_emit.inputs["Color"].default_value = (0.0, 0.8, 1.0, 1.0)
    n_emit.inputs["Strength"].default_value = 8.0
    links.new(n_emit.outputs["Emission"], n_out.inputs["Surface"])
    ring.data.materials.append(mat_ring)
    
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 0, 1.2), rotation=(math.radians(45), math.radians(35), math.radians(20)))
    cube = bpy.context.active_object
    cube.name = "Core_Metallic_Cube"
    mat_cube = bpy.data.materials.new(name="M_Dark_Chrome")
    bsdf_cube = mat_cube.node_tree.nodes.get("Principled BSDF")
    if bsdf_cube:
        bsdf_cube.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1.0)
        bsdf_cube.inputs["Metallic"].default_value = 1.0
        bsdf_cube.inputs["Roughness"].default_value = 0.1
    cube.data.materials.append(mat_cube)
    
    # Compositor Node Tree
    scene = bpy.context.scene
    c_tree = bpy.data.node_groups.new("PostProcessCompositor", 'CompositorNodeTree')
    scene.compositing_node_group = c_tree
    
    c_tree.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    c_tree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    
    c_nodes = c_tree.nodes
    c_links = c_tree.links
    c_nodes.clear()
    
    n_in = c_nodes.new("NodeGroupInput")
    n_in.location = (-400, 0)
    
    n_glare = c_nodes.new("CompositorNodeGlare")
    n_glare.location = (-150, 0)
    if "Type" in n_glare.inputs:
        n_glare.inputs["Type"].default_value = 'Fog Glow'
    if "Threshold" in n_glare.inputs:
        n_glare.inputs["Threshold"].default_value = 1.2
    
    n_lens = c_nodes.new("CompositorNodeLensdist")
    n_lens.location = (100, 0)
    n_lens.inputs["Dispersion"].default_value = 0.02
    if "Fit" in n_lens.inputs:
        n_lens.inputs["Fit"].default_value = True
        
    n_out = c_nodes.new("NodeGroupOutput")
    n_out.location = (350, 0)
    
    c_links.new(n_in.outputs["Image"], n_glare.inputs["Image"])
    c_links.new(n_glare.outputs["Image"], n_lens.inputs["Image"])
    c_links.new(n_lens.outputs["Image"], n_out.inputs["Image"])
    
    out_path = os.path.join(TUTORIALS_DIR, "08_compositing", "08_compositing.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"Saved: {out_path}")
    render_preview("08_compositing.png")

if __name__ == "__main__":
    print("=== Generating all 8 Blender Tutorial Projects ===")
    build_01_modeling()
    build_02_sculpting()
    build_03_shading()
    build_04_geometry_nodes()
    build_05_character_animation()
    build_06_physics()
    build_07_lighting_rendering()
    build_08_compositing()
    print("=== All 8 Projects & Previews Generated Successfully! ===")
