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

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **播放物理演算** | `Space` (空格键) | 从第 1 帧开始实时解算动力学动画 |
| **跳转至第 1 帧** | `Shift + 左方向键` | 重置物理世界到初始态 |
| **快速添加刚体** | 顶部菜单 `Object` -> `Rigid Body` -> `Add Active/Passive` | 批量为选中物体赋予刚体属性 |
| **复制刚体设置** | 选中多个物体 -> `Object` -> `Rigid Body` -> `Copy from Active` | 将活动物体的物理参数一键同步给全部选定物体 |

---

## 💡 实践步骤与练习建议
1. 打开 `06_physics.blend`，按 `Shift + 左箭头` 确保处于第 1 帧，然后按空格键播放。
2. 观察小球撞倒骨牌的连锁物理链，以及右侧丝绸布料自然下落包裹圆柱的真实褶皱。
3. 尝试选中 `Trigger_Ball`，在物理属性面板中将其 **Mass (质量)** 从 5kg 增加到 20kg，观察骨牌被撞飞的剧烈程度差异。
