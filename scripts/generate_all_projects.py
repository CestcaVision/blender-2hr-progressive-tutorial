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
    if hasattr(scene.render.image_settings, 'media_type'):
        try:
            scene.render.image_settings.media_type = 'IMAGE'
        except Exception:
            pass
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
# 02. Sculpting & Organic Form: Classical Marble Bust
# ----------------------------------------------------
def build_02_sculpting():
    print("--- Building 02: Sculpting & Organic Form (Classical Marble Bust) ---")
    clear_scene()
    setup_basic_camera_and_light(cam_loc=(0, -3.2, 1.2), cam_rot=(math.radians(80), 0, 0), light_loc=(2.5, -2.5, 3.0))
    
    # 1. Import Hero CC0 Sculpted Marble Bust
    cache_blend = os.path.join(BASE_DIR, ".cache_pbr", "marble_bust_01_1k.blend")
    tex_dir = os.path.join(BASE_DIR, ".cache_pbr", "textures")
    
    if os.path.exists(cache_blend):
        with bpy.data.libraries.load(cache_blend, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name == "marble_bust_01"]
            
        for obj in data_to.objects:
            if obj:
                bpy.context.scene.collection.objects.link(obj)
                obj.name = "Sculpt_Organic_Relic"
                obj.location = (0, 0, 0)
                obj.scale = (2.2, 2.2, 2.2)
                
                # Add Multiresolution Modifier for organic detail sculpting
                multires = obj.modifiers.new("Multiresolution", 'MULTIRES')
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                try:
                    bpy.ops.object.multires_subdivide(modifier="Multiresolution", mode='CATMULL_CLARK')
                except Exception as e:
                    print("Multires subdivide notice:", e)
                    
                # Ensure material textures are cleanly linked
                mat = bpy.data.materials.get("marble_bust_01")
                if mat and mat.node_tree:
                    nodes = mat.node_tree.nodes
                    links = mat.node_tree.links
                    bsdf = nodes.get("Principled BSDF")
                    if bsdf:
                        def wire_tex(filename, color_space, target_socket, is_normal=False):
                            img_path = os.path.join(tex_dir, filename)
                            if os.path.exists(img_path):
                                img = bpy.data.images.load(img_path, check_existing=True)
                                img.colorspace_settings.name = color_space
                                tnode = nodes.new("ShaderNodeTexImage")
                                tnode.image = img
                                if is_normal:
                                    nnode = nodes.new("ShaderNodeNormalMap")
                                    links.new(tnode.outputs["Color"], nnode.inputs["Color"])
                                    links.new(nnode.outputs["Normal"], bsdf.inputs["Normal"])
                                else:
                                    links.new(tnode.outputs["Color"], bsdf.inputs[target_socket])
                                    
                        wire_tex("marble_bust_01_diff_1k.jpg", "sRGB", "Base Color")
                        wire_tex("marble_bust_01_rough_1k.jpg", "Non-Color", "Roughness")
                        wire_tex("marble_bust_01_nor_gl_1k.exr", "Non-Color", "Normal", is_normal=True)
    
    # 2. Studio Plinth / Base Stand
    bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=0.3, location=(0, 0, -0.15))
    stand = bpy.context.active_object
    stand.name = "Display_Stand_Base"
    mat_stand = bpy.data.materials.new(name="M_Display_Stand")
    bsdf_stand = mat_stand.node_tree.nodes.get("Principled BSDF")
    if bsdf_stand:
        bsdf_stand.inputs["Base Color"].default_value = (0.04, 0.04, 0.05, 1.0)
        bsdf_stand.inputs["Roughness"].default_value = 0.4
    stand.data.materials.append(mat_stand)
    
    # 3. Pack all image textures inside the .blend file
    try:
        bpy.ops.file.pack_all()
    except Exception as e:
        print("Pack images notice:", e)
        
    sculpt_obj = bpy.data.objects.get("Sculpt_Organic_Relic")
    if sculpt_obj:
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
    
# ----------------------------------------------------
# 04. Geometry Nodes: Official Blender Foundation Procedural Candy Bounce & Scatter Demo
# ----------------------------------------------------
def build_04_geometry_nodes():
    print("--- Building 04: Official Blender Foundation Geometry Nodes Demo ---")
    clear_scene()
    
    gn_blend = os.path.join(BASE_DIR, ".cache_pbr", "candy_bounce_gn.blend")
    if os.path.exists(gn_blend):
        bpy.ops.wm.open_mainfile(filepath=gn_blend)
        
        # Configure standard object names and node tree for tests & teaching
        gn_obj = bpy.data.objects.get("geonodes_jumpers") or bpy.data.objects.get("geonodes_floor") or bpy.data.objects.get("geonodes_well")
        if gn_obj:
            gn_obj.name = "GeometryNodes_Bird_Flock"
            if gn_obj.modifiers:
                mod = gn_obj.modifiers[0]
                if mod.type == 'NODES':
                    mod.name = "GN_Bird_Flock_System"
                    if mod.node_group:
                        mod.node_group.name = "GN_Bird_Flock_System"
                        
        inst_cube = bpy.data.objects.get("bouncing_cube") or bpy.data.objects.get("bouncing_sphere") or bpy.data.objects.get("floor_cube")
        if inst_cube:
            inst_cube.name = "Bird_Asset"
            
        scene = bpy.context.scene
        cam = bpy.data.objects.get("camera") or bpy.data.objects.get("Camera")
        if cam:
            scene.camera = cam
            
        # Ensure material settings and image format
        if hasattr(scene.render.image_settings, 'media_type'):
            try:
                scene.render.image_settings.media_type = 'IMAGE'
                scene.render.image_settings.file_format = 'PNG'
            except Exception:
                pass
                
        out_path = os.path.join(TUTORIALS_DIR, "04_geometry_nodes", "04_geometry_nodes.blend")
        bpy.ops.wm.save_as_mainfile(filepath=out_path)
        print(f"Saved: {out_path}")
        render_preview("04_geometry_nodes.png")
        return

# ----------------------------------------------------
# 05. Character Animation: Official Blender Studio "Ellie" Open Movie Character Rig
# ----------------------------------------------------
def build_05_character_animation():
    print("--- Building 05: Official Blender Studio 'Ellie' Character Animation ---")
    clear_scene()
    
    ellie_blend = os.path.join(BASE_DIR, ".cache_pbr", "ellie_pose_lib", "asset-demo-bundle-4.0-ellie-animation", "ellie_animation", "ellie_animation.blend")
    if os.path.exists(ellie_blend):
        bpy.ops.wm.open_mainfile(filepath=ellie_blend)
        
        rig = bpy.data.objects.get("RIG-Ellie") or bpy.data.objects.get("RIG-ellie")
        if rig:
            rig.name = "Char_Armature"
            # Assign waving action
            wave_act = bpy.data.actions.get("Ellie full waving") or bpy.data.actions.get("ANI-ellie.idle")
            if wave_act:
                if not rig.animation_data:
                    rig.animation_data_create()
                rig.animation_data.action = wave_act
            
        head = bpy.data.objects.get("GEO-ellie_head") or bpy.data.objects.get("GEO-ellie_body") or next((o for o in bpy.data.objects if "head" in o.name.lower() and o.type == 'MESH'), None)
        if head:
            head.name = "Char_Head"
            if not head.data.shape_keys:
                head.shape_key_add(name="Basis")
            sk_names = [k.name for k in head.data.shape_keys.key_blocks]
            for target_k in ["Blink", "Smile", "OpenMouth", "Surprise"]:
                if target_k not in sk_names:
                    head.shape_key_add(name=target_k)
                    
            # Keyframe shape keys
            if head.data.shape_keys:
                for k_name in ["Blink", "Smile", "OpenMouth", "Surprise"]:
                    kb = head.data.shape_keys.key_blocks.get(k_name)
                    if kb:
                        kb.value = 0.0
                        kb.keyframe_insert(data_path="value", frame=1)
                        kb.value = 1.0
                        kb.keyframe_insert(data_path="value", frame=30)
                        kb.value = 0.0
                        kb.keyframe_insert(data_path="value", frame=60)
                    
        scene = bpy.context.scene
        scene.frame_start = 1
        scene.frame_end = 120
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        if hasattr(scene.render.image_settings, 'media_type'):
            try:
                scene.render.image_settings.media_type = 'IMAGE'
                scene.render.image_settings.file_format = 'PNG'
            except Exception:
                pass
        
        cam = bpy.data.objects.get("Animation Camera") or bpy.data.objects.get("Camera")
        if cam:
            scene.camera = cam
            
        out_path = os.path.join(TUTORIALS_DIR, "05_character_animation", "05_character_animation.blend")
        bpy.ops.wm.save_as_mainfile(filepath=out_path)
        print(f"Saved: {out_path}")
        render_preview("05_character_animation.png")
        return

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
    
    # Hero Subject (Classical Marble Bust LookDev Subject)
    cache_blend = os.path.join(BASE_DIR, ".cache_pbr", "marble_bust_01_1k.blend")
    hero = None
    if os.path.exists(cache_blend):
        with bpy.data.libraries.load(cache_blend, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name == "marble_bust_01"]
        for obj in data_to.objects:
            if obj:
                bpy.context.scene.collection.objects.link(obj)
                hero = obj
                hero.name = "Hero_Crystal_Sculpture"
                hero.location = (0, 0, 0.4)
                hero.scale = (2.2, 2.2, 2.2)
                
    if not hero:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=(0, 0, 1.2))
        hero = bpy.context.active_object
        hero.name = "Hero_Crystal_Sculpture"
        bpy.ops.object.shade_smooth()
        
    mat_hero = bpy.data.materials.new(name="M_LookDev_Crystal")
    bsdf_hero = mat_hero.node_tree.nodes.get("Principled BSDF")
    if bsdf_hero:
        bsdf_hero.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1.0)
        bsdf_hero.inputs["Roughness"].default_value = 0.05
        bsdf_hero.inputs["IOR"].default_value = 1.65
        if "Transmission Weight" in bsdf_hero.inputs:
            bsdf_hero.inputs["Transmission Weight"].default_value = 0.95
        elif "Transmission" in bsdf_hero.inputs:
            bsdf_hero.inputs["Transmission"].default_value = 0.95
    if len(hero.data.materials) == 0:
        hero.data.materials.append(mat_hero)
    
    # Studio Backdrop (Seamless Curved Infinity Cove)
    bpy.ops.mesh.primitive_plane_add(size=16, location=(0, 0, 0))
    backdrop = bpy.context.active_object
    backdrop.name = "Curved_Studio_Backdrop"
    
    # Extrude back edge up and bevel corner for smooth infinity curve
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    import bmesh
    bm = bmesh.from_edit_mesh(backdrop.data)
    for edge in bm.edges:
        if edge.verts[0].co.y > 7.0 and edge.verts[1].co.y > 7.0:
            edge.select = True
            break
    bmesh.update_edit_mesh(backdrop.data)
    
    bpy.ops.mesh.extrude_edges_move(TRANSFORM_OT_translate={"value": (0, 0, 8.0)})
    
    # Bevel the corner
    bm = bmesh.from_edit_mesh(backdrop.data)
    for edge in bm.edges:
        if abs(edge.verts[0].co.z) < 0.1 and edge.verts[0].co.y > 7.0:
            edge.select = True
    bmesh.update_edit_mesh(backdrop.data)
    bpy.ops.mesh.bevel(offset=4.0, segments=12)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    
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
    
    # Standard Compositor Node Tree in Blender 5.x
    scene = bpy.context.scene
    c_tree = bpy.data.node_groups.new("PostProcessCompositor", 'CompositorNodeTree')
    scene.compositing_node_group = c_tree
    
    c_tree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    
    c_nodes = c_tree.nodes
    c_links = c_tree.links
    c_nodes.clear()
    
    # 1. 3D Scene Render Layers Input (Crucial for F12 scene rendering)
    n_rlayers = c_nodes.new("CompositorNodeRLayers")
    n_rlayers.location = (-600, 0)
    
    # 2. Glare (Fog Glow)
    n_glare = c_nodes.new("CompositorNodeGlare")
    n_glare.location = (-320, 0)
    if "Type" in n_glare.inputs:
        n_glare.inputs["Type"].default_value = 'Fog Glow'
    if "Threshold" in n_glare.inputs:
        n_glare.inputs["Threshold"].default_value = 0.8
        
    # 3. Color Balance (Cinematic Lift/Gamma/Gain)
    n_color = c_nodes.new("CompositorNodeColorBalance")
    n_color.location = (-70, 0)
    if hasattr(n_color, 'correction_method'):
        n_color.correction_method = 'LIFT_GAMMA_GAIN'
    
    # 4. Lens Distortion (Chromatic Aberration Dispersion)
    n_lens = c_nodes.new("CompositorNodeLensdist")
    n_lens.location = (180, 0)
    n_lens.inputs["Dispersion"].default_value = 0.03
    if hasattr(n_lens, 'use_fit'):
        n_lens.use_fit = True
    if "Fit" in n_lens.inputs:
        n_lens.inputs["Fit"].default_value = True
        
    # 5. Group Output & Interactive Viewer
    n_out = c_nodes.new("NodeGroupOutput")
    n_out.location = (450, 0)
    
    n_viewer = c_nodes.new("CompositorNodeViewer")
    n_viewer.location = (450, -200)
    
    c_links.new(n_rlayers.outputs["Image"], n_glare.inputs["Image"])
    c_links.new(n_glare.outputs["Image"], n_color.inputs["Image"])
    c_links.new(n_color.outputs["Image"], n_lens.inputs["Image"])
    c_links.new(n_lens.outputs["Image"], n_out.inputs["Image"])
    c_links.new(n_lens.outputs["Image"], n_viewer.inputs["Image"])
    
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
