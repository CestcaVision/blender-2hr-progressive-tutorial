# 模块 05：人物动画、骨骼绑定与面部形态键 (Character Animation, Rigging & Shape Keys)

## 📌 课程目标 (Duration: ~20 mins)
本模块通过制作一个**风格化卡通角色 (Stylized Animated Character)**，系统讲解角色骨骼搭建 (Armature)、姿态模式 (Pose Mode) 关键帧动画、权重绘制原理 (Weight Painting)，以及使用**形态键 (Shape Keys)** 驱动丰富的面部表情（眨眼、微笑、张嘴发音、惊讶）。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/05_character_animation/05_character_animation.blend`
- **主要对象结构**：
  - `Char_Head`：头部网格，内嵌 4 组面部形态键（`Basis`, `Blink`, `Smile`, `OpenMouth`, `Surprise`）
  - `Char_Torso` / `Char_Arm_L` / `Char_Arm_R` / `Char_Leg_L` / `Char_Leg_R`：身体部位网格
  - `Char_Armature`：角色主骨骼架构（包含 Root、Spine、Chest、Head、Arm.L/R、Leg.L/R）
- **时间线预设**：第 1~120 帧已包含一段挥手动作与表情情绪转换的关键帧动画。

---

## 🛠 核心功能与技术点拆解

### 1. 面部表情形态键 (Facial Shape Keys)
- **原理**：Shape Key 记录网格顶点相对于基础状态（`Basis`）的相对偏移向量，通过 `0.0 ~ 1.0` 的权重滑块实现平滑形变混合。
- **本工程 4 组形态键**：
  1. `Blink` (眨眼)：上下眼睑闭合。
  2. `Smile` (微笑)：嘴角向上向后拉伸，颧肌上提。
  3. `OpenMouth` (张嘴)：下颌骨部位顶点下移，用于口型发音匹配。
  4. `Surprise` (惊讶)：眉毛挑起，嘴巴形成 "O" 型。
- **关键帧记录**：在属性面板的 Shape Keys 列表上，将鼠标悬停在 `Value` 滑块上按 `I` 键即可直接插入表情关键帧。

### 2. 骨骼装配与层次关系 (Armature Rigging)
- **骨骼层级链**：
  - `Root` (根骨骼) -> `Chest` (胸腔) -> `Head` (头部)
  - `Chest` -> `Arm_L` / `Arm_R` (手臂)
  - `Root` -> `Leg_L` / `Leg_R` (腿部)
- **父子级连接**：在编辑模式下选中子骨骼再选父骨骼，按 `Ctrl + P` -> `Keep Offset` (保持偏移)。

### 3. 姿态模式与动画曲线 (Pose Mode & Graph Editor)
- **姿态模式 (Pose Mode - `Ctrl + Tab`)**：用于旋转移动骨骼并打关键帧（`I` 键 -> `Location & Rotation`）。
- **摄影表 (Dope Sheet)**：直观调整关键帧的时间节点与节奏。
- **曲线编辑器 (Graph Editor)**：调节 F-Curve 贝塞尔控制柄，控制动作的缓入缓出 (Ease In / Ease Out)。

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **切换姿态模式** | 选中骨骼按 `Ctrl + Tab` | 进入/退出骨骼动画姿态调节 |
| **插入关键帧** | `I` | 弹出关键帧插入菜单（位置/旋转/缩放/全部） |
| **清除姿态变换** | `Alt + R` (旋转) / `Alt + G` (位移) | 快速让骨骼归位重置为默认绑定姿态 (Rest Pose) |
| **反向动力学 (IK)** | `Shift + I` | 为骨骼快速添加反向运动学约束 |
| **权重绘制模式** | 选中骨骼+网格按 `Ctrl + Tab` 选 `Weight Paint` | 绘制骨骼对顶点的受影响程度（蓝0 ~ 红1） |

---

## 💡 实践步骤与练习建议
1. 打开 `05_character_animation.blend`，按下空格键 `Space` 播放第 1~120 帧。
2. 观察角色右臂抬起挥手以及头部表情从眨眼、微笑到惊讶的连贯过渡。
3. 选中 `Char_Head`，在右侧绿色倒三角网格属性面板中找到 **Shape Keys**。
4. 拖动 `Smile` 和 `OpenMouth` 的滑块数值，实时观察二者混合叠加出的欢笑表情。
5. 选中 `Char_Armature` 进入 **Pose Mode**，尝试使用 `R` 旋转左臂或头部，并在第 60 帧按 `I` 插入属于您自己的姿态。
