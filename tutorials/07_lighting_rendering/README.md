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

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **切换到摄影机视角** | `Numpad 0` (小键盘0) 或 `~` 键选 `View Camera` | 进入/退出主摄像机取景框 |
| **摄影机视角漫游模式** | `Shift + ~` (Walk Navigation) | 像 FPS 游戏一样使用 `WASD` 自由漫游调整机位 |
| **锁定摄影机到视图** | 按 `N` 打开侧边栏 -> `View` -> 勾选 `Camera to View` | 旋转视口时自动同步更新摄影机位置 |
| **渲染单张静帧** | `F12` | 启动渲染窗口 |
| **渲染动画序列** | `Ctrl + F12` | 批量渲染所有时间线帧并输出文件 |

---

## 💡 实践步骤与练习建议
1. 打开 `07_lighting_rendering.blend`，按小键盘 `0` 进入 85mm 摄影机视图。
2. 按 `Z` 选择 **Rendered** 模式查看实时光影。
3. 尝试选中 `Rim_Light_Cyan`，修改其灯光颜色或将其功率从 800W 提升至 1500W，观察水晶边缘的高光勾边变化。
4. 选中摄影机，在右侧绿色摄影机属性中尝试将 `F-Stop` 从 2.0 调至 0.8，观察前后景深虚化程度的剧增。
