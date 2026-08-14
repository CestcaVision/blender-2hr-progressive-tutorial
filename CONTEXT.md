# Blender 2-Hour Progressive Tutorial Series - Domain Model & Architecture

## Ubiquitous Language & Core Concepts

- **Progressive Project (.blend file)**: A self-contained, clean, production-ready Blender 5.x scene representing a milestone in the 2-hour tutorial.
- **Pure Scene Policy (纯洁性工程原则)**: `.blend` files contain strictly production-quality 3D assets, hierarchies, materials, nodes, and animations without in-viewport 3D text graffiti or clutter.
- **External Markdown Courseware (外部讲义与导学)**: All explanations, step-by-step operations, keyboard shortcuts, node breakdowns, and parameter tips live in companion Markdown documents corresponding 1:1 with each project file.
- **Scenario-Driven Pedagogy (情境式具象教学)**: Introducing features through vivid, meaningful mini-projects (e.g. bird flock for Geometry Nodes, expressive character for Rigging/ShapeKeys, architectural/studio lighting for Cycles/EEVEE) rather than dry abstract UI tool tours.

## Curriculum Modules (8 Progressive Steps, ~120 Minutes)

1. **01_Modeling_HardSurface**: Poly-modeling, modifiers (Subdivision, Bevel, Mirror), mesh topology.
2. **02_Sculpting_Organic**: Sculpt mode, brush dynamics, Voxel Remesh, Dyntopo, multi-resolution.
3. **03_Shading_PBR**: Principled BSDF, procedural texture mapping (Noise, Voronoi, Bump, Roughness), UV mapping.
4. **04_GeometryNodes_Flock**: Procedural scattering, point distribution, flight simulation/boids math, curves/instances.
5. **05_Rigging_Character_Animation**: Character armature, limb IK/FK, Weight Painting, Facial Shape Keys, Dope Sheet & Graph Editor.
6. **06_Physics_Simulation**: Rigid body dynamics, Cloth simulation, collision physics, caching & baking.
7. **07_Lighting_Camera_Rendering**: Three-point studio & cinematic lighting, HDRI, depth of field, EEVEE-Next & Cycles engine comparison.
8. **08_Compositing_PostPipeline**: Compositor node tree, Glare, Color Balance/LUT, Cryptomatte/Render Passes, final output setup.

## File Organization Standard

```
/
├── CONTEXT.md
├── README.md                                  # Master Course Overview & Timeline
├── tutorials/
│   ├── 01_modeling/
│   │   ├── 01_modeling.blend
│   │   └── README.md                          # Step-by-step guide & shortcut index
│   ├── 02_sculpting/
│   │   ├── 02_sculpting.blend
│   │   └── README.md
│   ├── 03_shading/
│   │   ├── 03_shading.blend
│   │   └── README.md
│   ├── 04_geometry_nodes/
│   │   ├── 04_geometry_nodes.blend
│   │   └── README.md
│   ├── 05_character_animation/
│   │   ├── 05_character_animation.blend
│   │   └── README.md
│   ├── 06_physics/
│   │   ├── 06_physics.blend
│   │   └── README.md
│   ├── 07_lighting_rendering/
│   │   ├── 07_lighting_rendering.blend
│   │   └── README.md
│   └── 08_compositing/
│       ├── 08_compositing.blend
│       └── README.md
```
