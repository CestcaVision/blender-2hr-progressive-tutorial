# 模块 05：角色动画、骨骼装配与面部形态键 (Character Animation: Blender Studio Open Movie Character Rig)

## 📌 课程目标 (Duration: ~15 mins)
本模块引入 **Blender Studio 官方开源大电影《Sprite Fright》女主角艾莉专业角色工程 (Blender Studio "Ellie" Production Rig & Pose Library)**，让学员直观接触好莱坞/国际院线级角色资产。掌握工业级骨骼体系 (Armature Hierarchy)、姿态模式 (Pose Mode)、姿态库资产 (Pose Assets)、挥手动画关键帧与面部形态键（`Blink`, `Smile`, `OpenMouth`, `Surprise`）的高阶混合驱动。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/05_character_animation/05_character_animation.blend`
- **主要对象结构**：
  - `Char_Armature` (`RIG-Ellie`)：**Blender Studio 官方影视级全身绑定骨架**（包含千余根专业控制骨骼、IK/FK 切换与姿态库）
  - `Char_Head` (`GEO-ellie_head` / `GEO-ellie_body`)：**官方高精度角色头部与五官**（内嵌眨眼、微笑、口型与表情形态键）
  - `Animation Camera`：官方影视预设电影运镜摄影机
- **时间线预设**：第 1~120 帧包含官方挥手动画（`Ellie full waving`）与面部表情情绪律动。

---

### 1. Blender Studio 《Sprite Fright》官方教程与资源出处
- **官方开源电影**：Blender Studio 第 13 部开源大电影《Sprite Fright》(2021)，由前 Pixar 故事总监 Matthew Luhn 执导、Hjalti Hjalmarsson 担任动画总监。
- **官方教程与制作文档**：
  1. **[Blender Studio Sprite Fright Production Hub](https://studio.blender.org/films/sprite-fright/)**：包含全片所有制作镜头分解、角色资产库与原画概念图。
  2. **[Character Rigging with CloudRig (绑定系统精讲)](https://studio.blender.org/training/cloudrig/)**：由 Blender Studio 首席绑定师 Demeter Dzadik 主讲，深入剖析 Ellie 角色的骨架体系与驱动器（Drivers）实现。
  3. **[Animating with the Pose Library (姿态库动画实战)](https://studio.blender.org/training/pose-library-training/)**：由动画总监 Hjalti Hjalmarsson 详细讲解如何利用姿态库快速做表情混合与肢体节奏。

---

## 🛠 核心功能与技术点拆解

### 1. 在 Sprite Fright / Ellie 中调整面部表情与 Shape Key 的三种工作流

#### 🔹 工作流 A：姿态库资产交互混合 (Asset Browser / Pose Library) —— 【最推荐】
1. 在窗口底部或侧边调出 **Asset Browser (资产浏览器)**，或在 **Pose Mode (姿态模式)** 下按 `N` 打开右侧栏进入 **Animation** 选项卡。
2. 过滤资产库中的 **Ellie** 表情预设（包含 `Ellie mouth smileopen`, `Ellie mouth smileclosed`, `Ellie eyemask closed` 闭眼, `Ellie face excited` 兴奋, `Ellie eyemask scared` 惊恐）。
3. 选中角色面部骨骼，点击姿态库资产并左右拖拽鼠标，即可实现 $0\% \sim 100\%$ 的交互式平滑表情混合，随后按 `I` 键打入关键帧。

#### 🔹 工作流 B：骨骼控制器驱动 (Pose Mode Bone Controllers & Drivers) —— 【工业级正统】
- **原理**：在影视级生产管线中，网格形态键（Shape Keys）通常挂接在面部骨骼控制柄上（通过 Drivers 驱动器实时映射）。
- **操作**：
  - 选中 `Char_Armature`，按 `Ctrl + Tab` 进入 **Pose Mode**。
  - 选择嘴角控制骨骼（`MSTR-mouth`）、眼睑控制骨骼（`eyelid`）或眉毛控制骨骼（`brow`），按 `G`（移动）或 `R`（旋转），即可实时拉扯嘴唇与眼眶，底层自动驱动形态键。

#### 🔹 工作流 C：原生网格形态键调整与自制 (Mesh Data Shape Keys)
- **原理**：Shape Key 记录网格顶点相对于基础状态（`Basis`）的相对偏移向量，通过 `0.0 ~ 1.0` 的权重滑块实现平滑形变混合。
- **操作与打帧**：
  1. 选中角色头部 `Char_Head`，在右侧属性面板进入 **Data (网格数据属性 - 绿色倒三角)** $\rightarrow$ **Shape Keys (形态键)**。
  2. 调节 `Blink` (眨眼)、`Smile` (微笑)、`OpenMouth` (张嘴)、`Surprise` (惊讶) 的 `Value` 滑块。
  3. 鼠标悬停在 `Value` 滑块上按 `I` 键即可插入表情动画关键帧。
- **新建自制表情**：点击右侧 `+` 新建形态键（如 `Wink_L`） $\rightarrow$ 保持该形态键选中，进入 **Sculpt Mode (雕刻模式)** 或 **Edit Mode (编辑模式)** 调整面部顶点 $\rightarrow$ 退出后即可获得属于您自己的全新表情滑块！

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
