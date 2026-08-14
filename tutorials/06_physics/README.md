# 模块 06：动力学与物理模拟 (Physics Simulation)

## 📌 课程目标 (Duration: ~15 mins)
本模块通过一个**多米诺骨牌级联撞击与丝绸桌布下落碰撞场景 (Domino Cascade & Cloth Collision)**，讲解 Blender 的刚体动力学 (Rigid Body)、布料模拟 (Cloth Simulation) 以及碰撞物理体 (Collision Physics) 的设置与烘焙流程。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/06_physics/06_physics.blend`
- **主要对象结构**：
  - `Physics_Floor_Passive`：被动刚体地面（阻挡下落与承载碰撞）
  - `Trigger_Ball`：主动刚体触发球（较重质量，沿倾斜角度下落撞击第一块骨牌）
  - `Domino_01 ~ 08`：主动刚体多米诺方块（连锁倒塌反应）
  - `Cloth_Collision_Pillar`：带有碰撞属性的圆柱支柱
  - `Simulated_Cloth_Silk`：丝绸材质高密度布料面片（悬空下落包裹柱体）

---

## 🛠 核心功能与技术点拆解

### 1. 刚体动力学 (Rigid Body Dynamics)
- **Active (主动刚体)**：受重力、碰撞力和外力驱动，自由下落与弹跳（如小球与多米诺牌）。
- **Passive (被动刚体)**：不受物理重力影响（固定在空间），但作为障碍物参与物理碰撞运算（如地面与桌面）。
- **碰撞体形状 (Collision Shape)**：
  - `Box` / `Sphere` / `Cylinder`：基元碰撞体，计算速度极快且极度稳定。
  - `Convex Hull` (凸包)：自动包裹物体外沿，适用于不规则外凸物体。
  - `Mesh` (网格)：完全精准匹配凹面几何体，但计算消耗较高。

### 2. 布料模拟 (Cloth Simulation)
- **布料预设 (Cloth Presets)**：Blender 内置了 Cotton (棉布)、Silk (丝绸)、Leather (皮革)、Rubber (橡胶) 等不同阻尼与硬度参数。
- **碰撞与自碰撞 (Self-Collision)**：
  - 勾选 `Self-Collision`（自碰撞）可防止布料在折叠堆叠时发生自身穿模。
  - 配合细分修改器（Subdivision Surface），可获得平滑柔顺的织物褶皱细节。

### 3. 物理烘焙与缓存 (Physics Caching & Baking)
- 物理运算默认是实时单线程推导。对于复杂项目，建议在场景属性的 **Rigid Body World** 或布料修改器的 **Cache** 面板中点击 **Bake (烘焙)**，将结果永久固化在时间线上。

---

## 📝 完整分步实战构建指南 (Step-by-Step Physics Walkthrough)

### 步骤 1：搭建静止物理地面 (Passive Rigid Body Floor)
1. 按 `Shift + A` -> `Mesh` -> `Plane`，放大至 `Size: 14`，命名为 `Physics_Floor_Passive`。
2. 在右侧属性面板进入 **Physics (物理属性 - 蓝色圆环)**。
3. 点击 **Rigid Body (刚体)**，将类型设置为 **Passive (被动/静止碰撞体)**，碰撞形状设为 `Convex Hull` 或 `Box`，摩擦力设为 `0.5`。

### 步骤 2：创建骨牌阵列与主动刚体 (Active Dominos Cascade)
1. 按 `Shift + A` -> `Mesh` -> `Cube`，缩放为细长骨牌形状（`X: 0.5, Y: 0.12, Z: 0.9`），应用缩放（`Ctrl + A` -> `Scale`）。
2. 在物理属性中点击 **Rigid Body**，保持类型为 **Active (主动/受重力与碰撞驱动)**，质量设为 `1.0 kg`。
3. 沿 Y 轴复制 8 块骨牌（`Shift + D`），间距约为 `0.65m`，整齐排列成多米诺骨牌阵列。

### 步骤 3：悬挂触发钢球 (Heavy Trigger Ball)
1. 按 `Shift + A` -> `Mesh` -> `UV Sphere`，放置在第 1 块骨牌后上方（`X: 0, Y: -3.2, Z: 1.2`）。
2. 添加 **Rigid Body (Active)**，将质量加大至 `5.0 kg`。
3. 当按下空格键播放时，重球因重力迅速下落撞击第 1 块骨牌，引发震撼的多米诺连锁倾倒反应！

### 步骤 4：布料桌布与柱子碰撞体 (Cloth & Collision Pillar)
1. 在右侧添加圆柱体 `Cloth_Collision_Pillar`，在物理面板为其添加 **Collision (碰撞体)** 修改器。
2. 在柱子正上方添加网格面片 `Simulated_Cloth_Silk`（细分 24x24 顶点保证布料柔软度）。
3. 为面片添加 **Cloth (布料)** 物理属性：
   - 预设选择 `Silk (丝绸)` 或 `Cotton (棉布)`，质量设为 `0.2 kg`。
   - 展开 **Collisions (碰撞)**：勾选 `Object Collisions (物体碰撞)` 并务必勾选 **Self-Collisions (自碰撞)**（防止布料自身褶皱穿模折叠）。
   - 在修改器列表添加 **Subdivision Surface (表面细分)** 增加平滑度。

### 步骤 5：动力学烘焙与缓存固化 (Physics Cache Baking)
1. 在场景属性或布料缓存面板找到 **Cache (缓存)**。
2. 设置起始帧 `1` 到结束帧 `150`，点击 **Bake All Dynamics (烘焙所有动力学)**。
3. 烘焙完成后，物理计算结果将被永久固化在工程中，拖动时间线即可高速无卡顿前后回放！

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **播放物理模拟** | `Space` (空格键) | 实时计算刚体下落与布料飘落解算 |
| **重置时间线到起始帧** | `Shift + Left Arrow` (左方向键) | 快速让刚体与布料回归初始位置准备重放 |
| **应用变换** | `Ctrl + A` -> `All Transforms` | **物理必做项**：将物体缩放与旋转清零归一化，防止刚体碰撞体积畸变 |
| **快速添加被动/主动刚体** | 顶部菜单 `Object` -> `Rigid Body` -> `Add Active/Passive` | 批量为多选物体赋予刚体属性 |
| **复制刚体到选中项** | `Object` -> `Rigid Body` -> `Copy from Active` | 将选定物体的刚体物理参数一键同步给其他所有骨牌 |

---

## 💡 实践步骤与课后练习
1. 打开 `06_physics.blend`，按下空格键 `Space` 播放 1~150 帧。
2. 观察小球撞击骨牌后的连环倾倒动力学，以及右侧丝绸布料自然飘落在立柱顶端并形成优美垂坠褶皱的全过程。
3. 尝试将 `Trigger_Ball` 的质量从 `5.0 kg` 降为 `0.1 kg`，观察轻球是否还能推动沉重的骨牌阵列。
4. 尝试调节布料的 **Friction (摩擦力)** 与 **Stiffness (刚度/抗拉伸)** 参数，体验牛仔布与丝绸的不同垂坠质感。
