# 模块 05：角色动画、骨骼装配与面部形态键 (Character Animation, Armature Rigging & Shape Keys)

## 📌 课程目标 (Duration: ~15 mins)
本模块引入 **Blender 官方开源项目基础拓扑人头资产 (Blender Foundation Human Base Meshes - Stylized Character Head)**，让学员接触真正符合工业级循环边拓扑（Edge Loops）的面部资产。系统学习在生产级角色上构建 **Armature 骨架装配**、姿态模式 (Pose Mode) 摆姿动效、4 组核心**面部表情形态键 (Facial Shape Keys: 眨眼/微笑/张嘴/惊讶)** 以及时间线曲线混合控制。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/05_character_animation/05_character_animation.blend`
- **主要对象结构**：
  - `Char_Head`：**官方标准环形拓扑角色人头**（包含 `Basis`, `Blink`, `Smile`, `OpenMouth`, `Surprise` 5 组形态键）
  - `Char_Eye_L` / `Char_Eye_R`：官方写实眼球眼眶
  - `Char_Torso`, `Char_Arm_L`/`R`, `Char_Leg_L`/`R`：机械/躯干肢体组件
  - `Char_Armature`：包含 7 根骨骼（Root, Chest, Head, Arm_L, Arm_R, Leg_L, Leg_R）的关节骨架体系
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

## 📝 完整分步实战构建指南 (Step-by-Step Character Animation Walkthrough)

### 步骤 1：头部面部形态键制作 (Facial Shape Keys Authoring)
1. 选中角色头部 `Char_Head`，在右侧属性面板进入 **Data (网格数据属性 - 绿色倒三角)**。
2. 展开 **Shape Keys (形态键)** 栏：
   - 点击 `+` 创建基础形态 `Basis`（角色默认无表情状态）。
   - 再次点击 `+` 新建表情键：`Blink`（眨眼）、`Smile`（微笑）、`OpenMouth`（张嘴说话）、`Surprise`（眉毛上挑与惊讶）。
3. 选中 `Blink` 键，进入 **Edit Mode (编辑模式)** 将眼睑向下微调，退出后滑动 `Value (0.0 -> 1.0)` 即可看到眼睑闭合！

### 步骤 2：单骨骼与肢体骨架搭建 (Armature Skeleton Extrusion)
1. 按 `Shift + A` -> `Armature` -> `Single Bone`，在物体属性开启 `In Front (在前面显示)`。
2. 进入 **Edit Mode (编辑模式)**，按 `E` 向上挤出构建骨骼链：`Root (根骨)` $\rightarrow$ `Chest (胸腔)` $\rightarrow$ `Head (头部)`。
3. 从胸部两侧分别挤出并断开连接创建 `Arm_L / Arm_R (左右手臂)`，从根部分离创建 `Leg_L / Leg_R (左右腿部)`，并正确指定父级关系。

### 步骤 3：骨骼绑定与父级指定 (Bone Parenting / Weighting)
1. 依次选中各个身体部件网格（头部、躯干、手臂、腿部）。
2. 最后加选骨架 `Char_Armature`，按 `Ctrl + P` 选择 **Bone (骨骼绑定)** 或 **With Automatic Weights (附带自动权重)**。
3. 进入 **Pose Mode (姿态模式)**，旋转手臂骨骼即可实时带动肢体运动！

### 步骤 4：时间线姿态关键帧制作 (Pose Keyframing & Arm Wave)
1. 将时间线指针移动到第 `1` 帧，在姿态模式下选中右手 `Arm_R`，按 `I` 插入 `Rotation (旋转)` 关键帧。
2. 移动到第 `30` 帧，按 `R` 将手臂向上抬起举过头顶（挥手准备动作），按 `I` 插入旋转帧。
3. 在第 `50` 帧与第 `70` 帧之间左右轻微摇摆手臂，第 `120` 帧手臂放下复位。

### 步骤 5：面部表情混合过渡 (Emotional Transition & F-Curve Polish)
1. 选中头部 `Char_Head`，在第 `1` 帧为 `Blink`、`Smile` 插入 Value=0 关键帧（在 Value 滑块上右键选择 `Insert Keyframe` 或快捷键 `I`）。
2. 在第 `45` 帧打上 `Smile = 1.0`（伴随挥手微笑），在第 `55` 帧打上 `OpenMouth = 0.8`（张口打招呼），在第 `95` 帧切换为 `Surprise = 1.0`。
3. 打开底部 **Graph Editor (曲线编辑器)**，调整贝塞尔控制手柄（`V` -> `Automatic`），让眨眼与微笑表情过渡自然灵动！

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **切换姿态模式** | 选中骨架按 `Ctrl + Tab` | 快速进出 Pose Mode |
| **插入关键帧** | 视口中按 `I`，或在数值滑块上按 `I` | 为选中通道/骨骼打上关键帧 |
| **清除姿态变换** | 姿态模式下全选骨骼按 `Alt + R` / `Alt + G` | 重置骨骼旋转/位移回到静止姿态 (Rest Pose) |
| **形态键滑块打帧** | 鼠标悬停在 Shape Key Value 滑块上按 `I` | 快速为表情权重插入关键帧 |
| **曲线编辑器** | 切换编辑器为 `Graph Editor` (快捷键 `Shift + F6`) | 细调缓入缓出与动画运动曲线 |
| **播放/暂停动画** | `Space` (空格键) | 实时预览肢体挥手与面部表情动画 |

---

## 💡 实践步骤与课后练习
1. 打开 `05_character_animation.blend`，按下空格键 `Space` 播放 1~120 帧。
2. 观察角色如何在抬手挥手的同时，协同完成眨眼、微笑、张嘴与惊讶的表情流转。
3. 进入 **Pose Mode**，尝试为左手臂 `Arm_L` 在第 40 帧打上手插口袋或叉腰的新姿态。
4. 尝试在 Shape Keys 面板同时将 `Smile` 设为 0.5、`OpenMouth` 设为 0.5，观察多形态键线性叠加出的欢笑表情。
5. 选中 `Char_Armature` 进入 **Pose Mode**，尝试使用 `R` 旋转头部，并在第 60 帧按 `I` 插入属于您自己的关键帧。
