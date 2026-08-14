# 🎬 Blender 2小时极速通关实战教程 (2-Hour Progressive Blender Masterclass)

> **循序渐进 · 具象案例 · 纯净工程 · 开箱即用**  
> 本教程专为希望在 **2 小时内快速掌握 Blender 核心功能管线** 的学习者设计。摒弃枯燥的手册式罗列，全套课程由 **8 个高度聚焦、独立可运行、视觉出彩的实战工程案例** 组成。

---

## 🗺️ 课程时间线与案例全景图 (~120 分钟)

```mermaid
graph TD
    M1["01. 建模基础 (15min)\n复古旁轴相机\n硬表面/倒角/细分"] --> M2["02. 雕刻有机形态 (15min)\n古代遗迹徽章\n笔刷/Multires/体素"]
    M2 --> M3["03. PBR真实着色 (15min)\n四态材质测试球\n金属/车漆/玉石/玻璃"]
    M3 --> M4["04. 几何节点 (20min)\n群鸟飞行模拟系统\n点分发/噪波场/实例化"]
    M4 --> M5["05. 角色与表情动画 (20min)\n卡通角色与动作表情\n骨骼装配/IK/形态键"]
    M5 --> M6["06. 动力学模拟 (15min)\n多米诺与丝绸下落\n刚体物理/布料碰撞"]
    M6 --> M7["07. 灯光与摄影机 (15min)\n水晶雕塑摄影棚\n三点布光/长焦景深/AgX"]
    M7 --> M8["08. 后期合成管线 (10min)\n赛博霓虹发光核心\nFog Glow辉光/色散/输出"]
```

---

## 📂 教程模块索引与资产目录

| 序号 | 模块名称 | 具象实战案例 | 核心功能点 | 对应工程与讲义 |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **多边形建模** | 复古旁轴相机 (Vintage Camera) | 顶点/边/面编辑、挤出、内插、倒角与细分修改器 | [01_modeling](tutorials/01_modeling/README.md) · [工程](tutorials/01_modeling/01_modeling.blend) |
| **02** | **雕刻有机形态** | 遗迹浮雕勋章 (Organic Relic) | 粘土条/折痕笔刷、多级精度 (Multiresolution)、对称控制 | [02_sculpting](tutorials/02_sculpting/README.md) · [工程](tutorials/02_sculpting/02_sculpting.blend) |
| **03** | **PBR 真实着色** | 材质测试球阵列 (Shader Balls) | Principled BSDF、金属度/粗糙度、透射、次表面散射 (SSS)、噪波凹凸 | [03_shading](tutorials/03_shading/README.md) · [工程](tutorials/03_shading/03_shading.blend) |
| **04** | **几何节点生成** | 飞鸟群模拟 (Bird Flock Simulation) | 点分发 (Distribute Points)、实例复制 (Instance on Points)、时间噪波流体 | [04_geometry_nodes](tutorials/04_geometry_nodes/README.md) · [工程](tutorials/04_geometry_nodes/04_geometry_nodes.blend) |
| **05** | **人物骨骼与表情** | 挥手卡通角色 (Character & Facial Rig) | 骨骼装配 (Armature)、姿态关键帧 (Pose)、面部表情形态键 (Shape Keys) | [05_character_animation](tutorials/05_character_animation/README.md) · [工程](tutorials/05_character_animation/05_character_animation.blend) |
| **06** | **物理动力学模拟** | 多米诺倒塌与丝绸垂落 (Physics Simulation) | 主动/被动刚体 (Rigid Body)、布料碰撞 (Cloth & Collision)、物理缓存 | [06_physics](tutorials/06_physics/README.md) · [工程](tutorials/06_physics/06_physics.blend) |
| **07** | **灯光与摄影机** | 暗调水晶雕塑棚拍 (Cinematic Studio) | 经典三点布光法、85mm 电影长焦景深 (DoF)、Cycles/EEVEE、AgX 色彩 | [07_lighting_rendering](tutorials/07_lighting_rendering/README.md) · [工程](tutorials/07_lighting_rendering/07_lighting_rendering.blend) |
| **08** | **后期合成与输出** | 赛博霓虹核心 (Cyber Glow Core) | 合成节点树 (Compositor)、Fog Glow 辉光、色散畸变 (Lens Distortion) | [08_compositing](tutorials/08_compositing/README.md) · [工程](tutorials/08_compositing/08_compositing.blend) |

---

## 🌟 工程纯洁性与使用规范 (Pure Scene Policy)

1. **零杂质视口**：所有 `.blend` 文件遵循工业化交付标准，场景内无冗余 3D 浮动文字或干扰注记。
2. **外部独立讲义**：全部操作步骤、设计原理、快捷键汇总及参数对照表均位于同级目录下的 `README.md` 中。
3. **零外部路径依赖**：全部材质与程序化逻辑均内嵌生成，跨平台打开 100% 免除 Missing Texture 困扰。

---

## ⚡ 极速自动化验证与一键重建

如需一键重新生成全套 8 个 `.blend` 工程并输出预览渲染图，可在终端执行：

```bash
blender --background --python scripts/generate_all_projects.py
```

渲染产物将自动保存在 `renders/` 目录下（`01_modeling.png` ~ `08_compositing.png`）。

---

## ⌨️ 全课程核心高频快捷键速查总表 (Master Shortcut Cheat Sheet)

| 阶段 / 模块 | 核心操作 | 快捷键 | 功能说明与应用场景 |
| :--- | :--- | :--- | :--- |
| **基础与视口** | 模式切换饼菜单 | `Ctrl + Tab` | 快速在 Object / Edit / Sculpt / Pose 模式间切换 |
| | 视口着色方式 | `Z` | 呼出 Wireframe / Solid / Material / Rendered 饼菜单 |
| | 聚焦所选物体 | `小键盘 .` (Period) | 视口立即将选定物体居中放大 |
| **01. 硬表面建模** | 挤出 / 内插面 / 倒角 | `E` / `I` / `Ctrl + B` | 多边形建模核心三板斧 |
| | 环切与滑移 | `Ctrl + R` | 在网格上添加等分环形边 |
| | 衰减编辑模式 | `O` | 开启软选择与有机平滑拉拽变形 |
| **02. 数字雕刻** | 调整笔刷大小 / 强度 | `F` / `Shift + F` | 动态缩放雕刻笔刷半径与深度 |
| | 平滑 / 反向凹陷 | 按住 `Shift` / 按住 `Ctrl` | 任何笔刷下随时进行表面平滑或反向雕刻 |
| **03. PBR 材质** | 材质着色器节点添加 | `Shift + A` | 搜索并添加 Principled BSDF、Image Texture 节点 |
| | 快速预览单个节点 | `Ctrl + Shift + 左键` | (Node Wrangler) 直接连至材质临时输出 |
| **04. 几何节点** | 几何节点组编辑器 | 切换 `Geometry Nodes` | 搭建程序化点分发、4D 噪波场与实例化 |
| | 激光切断连线 | `Ctrl + 右键划线` | 快速斩断多条节点连线 |
| **05. 角色与动画** | 插入关键帧 | `I` (视口或滑块上) | 为选中骨骼或形态键打上变换关键帧 |
| | 清除骨骼变换 | `Alt + R` / `Alt + G` | 姿态模式下一键恢复骨骼到静止姿态 (Rest Pose) |
| | 曲线编辑器 | `Shift + F6` (Graph Editor) | 调整缓入缓出曲线控制杆 |
| **06. 物理动力学** | 播放 / 重置模拟 | `Space` / `Shift + 左箭头` | 实时计算刚体与布料碰撞，一键复位 |
| | 应用全部变换 | `Ctrl + A` -> `All Transforms` | **物理必做**：归一化缩放与旋转，避免碰撞体积畸变 |
| **07. 灯光与摄影机**| 对齐相机到当前视口 | `Ctrl + Alt + 小键盘 0` | 将活动摄像机瞬移至当前视角 |
| | 相机飞行漫游导航 | `Shift + ~` (Walk Navigation) | FPS 游戏式 WASD 漫游精细调整机位 |
| **08. 合成后期** | 渲染单帧大图 | `F12` | 启动渲染并自动运行后期合成节点树 |
| | 背景图缩放与平移 | `V` / `Alt + V` / `Alt + 中键` | 缩放与平移合成器背景 Backdrop 画布 |

---

## 🚀 建议学习路径
1. 从 `01_modeling` 开始，双击打开对应 `.blend` 文件，同步阅读其目录下的 `README.md`。
2. 按照每个讲义末尾的 **💡 实践步骤与练习建议** 动手修改 2~3 个核心参数。
3. 2 小时后，即可完整贯通从建模、雕刻、着色、程序化节点、绑定动画、动力学到灯光合成的现代 3D 生产管线！
