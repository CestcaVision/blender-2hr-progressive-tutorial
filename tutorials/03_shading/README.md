# 模块 03：材质与 PBR 真实着色 (Shading & PBR Materials)

## 📌 课程目标 (Duration: ~15 mins)
本模块通过一个**标准材质测试球阵列 (Shader Ball Array)**，系统讲解基于物理的渲染 (PBR) 原理、Principled BSDF 原理化着色器核心通道，以及利用程序化噪波 (Procedural Noise) 与凹凸 (Bump) 节点搭建逼真表面质感。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/03_shading/03_shading.blend`
- **主要对象结构**：
  - `ShaderBall_M_Weathered_Gold`：金属 PBR 材质（高金属度、微粗糙度与噪波凹凸）
  - `ShaderBall_M_SciFi_Damaged_Armor`：车漆/清漆材质（双层高光 Clearcoat/Coat 通道）
  - `ShaderBall_M_Subsurface_Jade`：次表面散射材质（玉石/皮肤/蜡质透光 SSS）
  - `ShaderBall_M_Dispersion_Glass`：透射与折射材质（全透光玻璃、IOR 折射率）
  - `Studio_Backdrop`：摄影棚吸光深色地面

---

## 🛠 核心功能与技术点拆解

### 1. PBR 与 Principled BSDF 核心参数映射
- **Base Color (基础色)**：表面的本征漫反射颜色（金属材质的基础色决定其镜面反射颜色）。
- **Metallic (金属度)**：非导电介质为 `0.0`（塑料、木材、石头），纯金属为 `1.0`。
- **Roughness (粗糙度)**：`0.0` 为完全镜面高光，`1.0` 为完全漫散射无光泽表面。
- **Transmission (透射/玻璃)**：权重设为 `1.0` 时物体变为折射介质（玻璃/水/水晶），搭配 `IOR`（折射率，如水 1.33，玻璃 1.52，钻石 2.42）。
- **Subsurface Scattering (次表面散射)**：光线穿透物体并在内部发生多次散射后再透出，模拟玉石、蜡烛、果冻与人体皮肤。

### 2. 程序化噪波与微表面细节 (Procedural Micro-detail)
- **Noise Texture (噪波纹理)**：生成无接缝的连续数学噪波值（Scale 缩放控制频率，Detail 控制分形阶数，Roughness 控制微噪波锐度）。
- **Bump 节点 (凹凸映射)**：将黑白高度图（Height）转换为视口法线向量（Normal），在不增加多边形面的前提下呈现凹凸不平的破损与铸造质感。

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **切换着色预览模式** | `Z` -> 饼菜单选 `Material Preview` / `Rendered` | 快速查看视口材质渲染效果 |
| **材质着色器工作区** | 顶部标签页切换到 `Shading` | 打开材质节点编辑器与 3D 视图联动 |
| **新建节点** | `Shift + A` | 打开着色器节点添加菜单 |
| **快速框选整理** | `Ctrl + J` | 为选中的节点创建 Frame 边框分组 |
| **静音/禁用节点** | `M` | 临时开启/关闭当前选中的节点作用 |

---

## 💡 实践步骤与练习建议
1. 打开 `03_shading.blend`，按 `Z` 选择 **Material Preview**。
2. 选中 `ShaderBall_M_Weathered_Gold`，进入 Shading 工作区。
3. 调节 `Noise Texture` 的 **Scale**（如从 15 改为 50），观察微划痕密度的变化。
4. 调节 `Principled BSDF` 的 **Roughness** 滑块，观察反光从镜面金到拉丝哑光金的渐变过程。
