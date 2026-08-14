# 模块 01：硬表面与多边形建模 (Hard-Surface Modeling)

## 📌 课程目标 (Duration: ~15 mins)
本模块通过制作一台**复古旁轴相机 (Vintage Rangefinder Camera)**，带领学员掌握 Blender 的多边形建模核心工作流、网格拓扑规范以及常用修改器（Modifiers）的配合使用。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/01_modeling/01_modeling.blend`
- **主要对象结构**：
  - `Camera_Body`：相机机身主体（应用倒角与细分曲面）
  - `Lens_Barrel_Base` / `Lens_Focus_Ring` / `Lens_Front_Element`：多层镜头结构
  - `Mode_Dial` / `Shutter_Button` / `Power_Switch`：机顶旋钮与快门按键
  - `Viewfinder_Window`：取景窗与测距窗

---

## 🛠 核心功能与技术点拆解

### 1. 编辑模式基础与几何体变形
- **点/线/面选择模式**：快捷键 `1`（顶点）、`2`（边）、`3`（面）。
- **挤出 (Extrude)**：`E` 键沿法线挤出面；`Alt + E` 打开挤出菜单（沿各自法线挤出/内插）。
- **内插面 (Inset Faces)**：`I` 键快速为当前多边形向内收缩边缘，建立支撑环线。
- **环切与滑动 (Loop Cut & Slide)**：`Ctrl + R` 添加循环边，滚动鼠标滚轮增减切割数量。

### 2. 非破坏性修改器工作流 (Non-Destructive Modifiers)
- **倒角修改器 (Bevel Modifier)**：
  - `Width`: `0.05m`，`Segments`: `4`。
  - 作用：为硬边缘添加微倒角，使其在光照下反射出真实的高光过渡。
- **细分曲面修改器 (Subdivision Surface)**：
  - 快捷键 `Ctrl + 1` / `Ctrl + 2` 快速添加 1~2 级细分。
  - 作用：将基础低模（Cage Mesh）平滑为高密度的曲面模型。

### 3. 变换应用原则 (Apply Transforms)
- **核心原则**：在对物体进行比例缩放或旋转后，若直接添加修改器，修改器将受到非等比缩放的影响。
- **解决方案**：在物体模式下选中物体，按 `Ctrl + A` -> 选择 **Apply All Transforms (应用全部变换)** 或 **Apply Scale**。

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **视图切换** | `Tab` | 在物体模式 (Object Mode) 与编辑模式 (Edit Mode) 间切换 |
| **点/线/面** | `1` / `2` / `3` | 编辑模式下切换选择元素类型 |
| **挤出** | `E` | 沿法线延伸网格面 |
| **内插面** | `I` | 局部创建向内缩进的同心面 |
| **环切** | `Ctrl + R` | 均匀插入环状分割边 |
| **应用变换** | `Ctrl + A` | 冻结物体的位移、旋转和缩放数据为初始标准态 |
| **平滑着色** | 鼠标右键 -> `Shade Smooth` | 启用法线平滑插值 |

---

## 💡 实践步骤与练习建议
1. 打开 `01_modeling.blend`，选中 `Camera_Body` 进入编辑模式。
2. 尝试关闭/开启右侧修改器面板中的 **Bevel** 与 **Subdivision** 视口图标，观察高光边缘与拓扑变化。
3. 练习在机身侧面使用 `I`（内插）+ `E`（向内挤出）制作一个皮套凹槽。
