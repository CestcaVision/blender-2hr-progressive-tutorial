# Feature Specification: Blender 2-Hour Progressive Tutorial Series & Project Suite

## Problem Statement

Learners attempting to master Blender face an overwhelming learning curve. Most existing tutorials are either exhaustive UI reference manuals that lack creative context, or disjointed single-project videos that fail to systematically introduce the full modern 3D production pipeline in a structured, time-bounded manner (~2 hours). Furthermore, learners often struggle with cluttered sample files where explanatory notes obscure 3D viewports, or suffer from broken external textures and incompatible version workflows.

## Solution

A structured, 8-stage progressive masterclass suite built upon 8 production-grade, self-contained Blender project scenes. Each module introduces core Blender features through vivid, scenario-driven projects (such as bird flock simulation for Geometry Nodes, expressive character rigging with facial shape keys for animation, and studio three-point setups for lighting & camera). 

All project files strictly adhere to a **Pure Scene Policy** (zero in-viewport text graffiti or clutter), while comprehensive step-by-step explanations, shortcut cheat sheets, node architecture breakdowns, and troubleshooting tips are externalized into dedicated Markdown courseware. The entire suite is 100% reproducible and verifiable via headless automated CLI testing.

## User Stories

1. As a 3D beginner, I want to open a clean hard-surface modeling scene, so that I can learn polygon extrusion, insetting, beveling, and subdivision surface workflows without getting lost in UI clutter.
2. As a 3D modeler, I want to explore organic sculpting on a prepared medallion mesh, so that I can master clay strips, crease, inflate, grab brushes, and multiresolution subdivision levels.
3. As a surfacing artist, I want to inspect a multi-material shader ball scene, so that I can understand Principled BSDF metallic, roughness, transmission, subsurface scattering (SSS), and procedural noise bump networks.
4. As a procedural designer, I want to open a flocking flight simulation project, so that I can understand Geometry Nodes point distribution, instance on points, and vector noise field displacement.
5. As a character animator, I want to manipulate an articulated stylized character rig, so that I can practice keyframing limb motion alongside facial expression Shape Keys (blink, smile, open mouth, surprise).
6. As a technical director, I want to play a pre-configured physics simulation scene, so that I can observe active/passive rigid body cascades and cloth collision drape behaviors.
7. As a lighting & lookdev artist, I want to study a three-point studio lighting setup, so that I can learn key/fill/rim light balance, 85mm camera depth-of-field (DoF), and modern AgX / Filmic color transforms.
8. As a post-production artist, I want to inspect a compositor node tree, so that I can learn how to apply Fog Glow glare, chromatic aberration lens distortion, and cinematic color balancing directly inside Blender.
9. As an educator, I want companion Markdown courseware alongside each project file, so that I have immediate access to timestamped curricula, keyboard shortcut tables, and hands-on exercises.
10. As a developer/contributor, I want an automated generation and validation test suite, so that I can rebuild and verify all 8 scenes and render preview images headlessly in continuous integration.

## Implementation Decisions

- **8 Modular Milestones**: The curriculum is decoupled into 8 isolated, self-contained project directories under `tutorials/01_...` through `tutorials/08_...`.
- **Pure Scene Policy**: Project scenes contain exclusively clean, production-grade 3D assets, hierarchies, and shader/node trees. Explanatory text, shortcut maps, and exercise prompts reside strictly in external Markdown files.
- **Embedded Procedural Textures**: All materials rely on mathematical procedural shaders (Noise, Voronoi, Principled BSDF, Bump) and native geometry to guarantee zero external texture link breakages across platforms.
- **Facial Shape Keys Integration**: The character animation module explicitly provides 4 core expressive Shape Keys (`Blink`, `Smile`, `OpenMouth`, `Surprise`) combined with an armature pose keyframed wave animation.
- **Headless Reproducibility**: All project scenes and preview renders are generated and validated programmatically via Blender Python API scripts to ensure 100% testability.

## Testing Decisions

- **Single High-Level Seam (CLI Verification Seam)**: All tests are executed at the highest possible architectural seam — running headless Blender invocations (`blender --background --python <script>`) to verify scene creation, modifier integrity, node tree compilation, and still-frame rendering without errors.
- **Render Output Validation**: Automated verification confirms that each module exports a non-empty, high-fidelity PNG preview into the `renders/` output artifact directory.
- **Regression Guard**: All script execution terminates with exit code 0; any deprecated API warnings or broken enum parameters fail the build immediately.

## Out of Scope

- Video/audio voiceover recording (courseware provides full lecture notes and step-by-step guidance scripts for presenters or self-study).
- Third-party commercial add-on dependencies (all assets utilize vanilla Blender LTS features).
- Complex multi-character combat choreography or full feature-film length simulations.

## Further Notes

- Target runtime compatibility: Blender 5.x LTS.
- Public GitHub repository: `https://github.com/CestcaVision/blender-2hr-progressive-tutorial`
