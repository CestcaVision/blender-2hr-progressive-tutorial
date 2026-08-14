# 模块 07：灯光、摄影机与渲染引擎 (Lighting, Camera & Rendering)

## 📌 课程目标 (Duration: ~15 mins)
本模块通过一个**电影感暗调水晶雕塑场景 (Cinematic Crystal Studio)**，系统讲解经典三点布光法（Three-Point Lighting）、摄影机焦段与景深（Depth of Field）、构图辅助线，以及 Blender 渲染引擎（Cycles 光线追踪与 EEVEE 实时光栅化）的设置。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/07_lighting_rendering/07_lighting_rendering.blend`
- **主要对象结构**：
  - `Hero_Crystal_Sculpture`：透光水晶高反射主体（带有高折射率 IOR 与微表面平滑）
  - `Curved_Studio_Backdrop`：无缝弧形摄影棚暗色背景
  - `Key_Light_Warm`：暖色主光 (Area Light - 500W, 45度斜照)
  - `Fill_Light_Cool`：冷色柔和补光 (Area Light - 150W, 照亮阴影暗部)
  - `Rim_Light_Cyan`：青色边缘轮廓光 (Spot Light - 800W, 锐利勾勒背光边缘)
  - `Cinematic_Camera_85mm`：85mm 人像长焦电影摄影机（开启 f/2.0 大光圈景深）

---

## 🛠 核心功能与技术点拆解

### 1. 经典三点布光法 (Three-Point Studio Lighting)
```
             [Rim Light / 轮廓光]
                   \   /
                     O  <-- [Hero Asset / 主体]
                   /   \
  [Key Light / 主光]     [Fill Light / 补光]
        (暖调, 强)           (冷调, 软)
```
- **Key Light (主光)**：确立场景的主要光照方向与明暗调性，通常呈 45 度角斜射。
- **Fill Light (补光)**：强度约为初始主光的 20%~40%，用于柔化主光投射出的生硬死黑阴影，提供冷暖色彩冷暖对比。
- **Rim Light (轮廓光/背光)**：从物体后侧方投射，在物体边缘打出一条极亮的高光轮廓线，将主体与深色背景彻底分离。

### 2. 摄影机与景深控制 (Camera & Depth of Field)
- **焦段选择 (Focal Length)**：
  - `24mm ~ 35mm`：广角镜头（透视夸张、视野开阔，适合大场景）。
  - `50mm`：标准镜头（接近人眼自然透视）。
  - `85mm ~ 135mm`：中长焦镜头（压缩空间感、背景虚化强烈，适合静物与特写）。
- **景深虚化 (Depth of Field)**：
  - 勾选 `Depth of Field`，将 `Focus on Object` 绑定到主体。
  - 调整 `F-Stop`（光圈值，如 `f/1.8` 或 `f/2.0`），数值越小，背景景深虚化越强烈。

### 3. 渲染引擎与色彩管理 (Cycles vs. EEVEE)
- **Cycles**：基于物理路径追踪的离线渲染器，计算精确的光线多次反弹、真焦散与透射折射。
- **EEVEE (EEVEE-Next)**：基于现代化 GPU 计算着色器的实时渲染引擎，支持光线追踪屏幕空间反射（Raytracing Screen Space）与快速渲染。
- **Color Management (色彩管理)**：
  - `View Transform`：推荐选用 `AgX` 或 `Filmic`（相比默认 Standard 拥有更宽广的高光宽容度与动态范围，防止高光过曝死白）。
  - `Look`：选用 `Medium High Contrast` 增强画面纵深感。

---

## 📝 完整分步实战构建指南 (Step-by-Step Lighting & Camera Walkthrough)

### 步骤 1：搭建暗调摄影棚与主体 (Studio Backdrop & Hero Crystal)
1. 打开 `07_lighting_rendering.blend`，正中央放置高折射率（`IOR: 1.65`）的水晶几何雕塑 `Hero_Crystal_Sculpture`。
2. 地面铺设大尺寸暗色吸光摄影棚背景 `Curved_Studio_Backdrop`（粗糙度 `0.2`，提供温和的地面镜面反射）。

### 步骤 2：布置三点布光系统 (Three-Point Lighting Setup)
1. **主光 (Key Light - `Key_Light_Warm`)**：
   - 类型选择 **Area (面光)**，尺寸设为 `2.5m`（大光源带来柔和阴影过渡）。
   - 放置在主体右前方 45 度角（`X: 3.5, Y: -3.5, Z: 4.0`），功率设为 `500W`，微暖暖光（`#FFE6BF`）。
2. **辅光 (Fill Light - `Fill_Light_Cool`)**：
   - 放置在主体左侧（`X: -4.0, Y: -2.5, Z: 2.5`），功率降为 `150W`（约为主要光强度的 1/3~1/4），超大柔光板（`Size: 4.0m`），冷蓝调（`#A6CCFF`），提亮暗部细节并形成冷暖对比。
3. **轮廓光/背光 (Rim Light - `Rim_Light_Cyan`)**：
   - 放置在主体后上方（`X: -2.0, Y: 3.5, Z: 3.5`），类型为 **Spot (聚光灯)**，功率高达 `800W`，青色亮光（`#33E6FF`），勾勒出水晶雕塑边缘晶莹剔透的高光轮廓。

### 步骤 3：配置 85mm 电影感景深摄像机 (85mm Cinematic Camera & DoF)
1. 按 `Shift + A` -> `Camera`，重命名为 `Cinematic_Camera_85mm`，按 `Ctrl + Alt + Numpad 0` 将相机对准当前视口视角。
2. 在相机属性面板将 **Focal Length (焦距)** 设为经典人像/特写镜头 `85.0 mm`（压缩透视，突出主体）。
3. 勾选 **Depth of Field (景深)**：
   - **Focus Object (对焦目标)** 选取 `Hero_Crystal_Sculpture`。
   - **F-Stop (光圈值)** 设为 `2.0`（大光圈产生奶油般的背景虚化散景 Bokeh）。

### 步骤 4：设置 AgX 现代色彩管理 (AgX Color Management)
1. 在右侧属性面板进入 **Render Properties (渲染属性)** -> **Color Management (色彩管理)**。
2. 将 **View Transform (色彩视图变换)** 设为 **AgX**（Blender 4.0+ 引入的下一代色彩空间，能完美还原高光色彩不发白褪色）。
3. 将 **Look (色彩风格)** 设为 **AgX - Medium High Contrast (中高对比度)**，立刻获得通透深邃的电影级质感！

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **对齐相机到视口** | `Ctrl + Alt + 小键盘 0` | 将活动摄像机迅速移动并对齐当前观察视角 |
| **切换相机视图** | `小键盘 0` (Numpad 0) | 进入/退出摄像机取景框 |
| **相机视角漫游飞行** | `Shift + ~` (波浪键) | 使用 WASD 键像第一人称游戏一样自由飞行调整构图 |
| **锁定相机到视图** | 侧边栏 `N` -> `View` -> 勾选 `Camera to View` | 旋转缩放视口时同步调整相机机位 |
| **开启渲染预览** | `Z` -> 饼菜单选 `Rendered` (或按 `Shift + Z`) | 视口实时查看光影、反射与景深虚化 |
| **渲染静态单帧** | `F12` | 执行最终高质量图像离线渲染 |

---

## 💡 实践步骤与课后练习
1. 打开 `07_lighting_rendering.blend`，按 `小键盘 0` 进入摄影机视角，按 `Z` 切换为 **Rendered (渲染预览)**。
2. 依次在大纲树中隐藏 `Key_Light`、`Fill_Light`、`Rim_Light`，直观体会三盏灯各自在场景中扮演的关键光影角色。
3. 选中相机，尝试将 `F-Stop` 从 `2.0` 改为 `16.0`，观察背景虚化从极其强烈到全景清晰的景深变化。
4. 切换渲染引擎为 `Cycles`（GPU 加速），对比物理光线追踪在水晶内部折射与玻璃焦散（Caustics）上的极致真实质感。
