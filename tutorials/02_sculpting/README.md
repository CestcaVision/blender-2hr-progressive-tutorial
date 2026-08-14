# 模块 02：雕刻与有机形态 (Sculpting & Organic Modeling)

## 📌 课程目标 (Duration: ~15 mins)
本模块通过制作一件**古代遗迹徽章/浮雕勋章 (Organic Medallion Relic)**，讲解 Blender 雕刻模式的核心笔刷动态、体素重构网格 (Voxel Remesh)、动态拓扑 (Dyntopo) 以及多级精度修改器 (Multiresolution Modifier) 的运用。

---

## 📂 工程文件信息
- **工程路径**：`tutorials/02_sculpting/02_sculpting.blend`
- **主要对象结构**：
  - `Sculpt_Organic_Relic`：雕刻主体，已挂载 3 级细分的多级精度修改器 (Multiresolution)
  - `Display_Stand_Base` / `Display_Stand_Pillar`：展示台基座

---

## 🛠 核心功能与技术点拆解

### 1. 雕刻工作区与基础笔刷组
- **Draw / Clay Strips (粘土条笔刷 - `X`)**：用于大体积的形体塑造与快速堆叠泥层。
- **Crease (折痕笔刷 - `Shift + C`)**：快速拉出锐利的凹槽、刻线与硬边缘褶皱。
- **Inflate (膨胀笔刷 - `I`)**：向表面法线方向均匀充气膨胀。
- **Grab / Snake Hook (抓取/蛇钩笔刷 - `G` / `K`)**：大范围拉伸外轮廓形态与角/触须结构。
- **Smooth (平滑 - 按住 `Shift`)**：任意笔刷下按住 `Shift` 即可快速平滑过渡。

### 2. 拓扑控制策略对比
- **Voxel Remesh (体素重构)**：
  - 快捷键 `Ctrl + R` 执行重构，`Shift + R` 调整体素网格预览大小。
  - 适用场景：概念设计草图阶段，合并多个相交网格并重新生成均匀分布的四边网格。
- **Multiresolution Modifier (多级精度修改器)**：
  - 本工程所用方案。保留最底层的简单拓扑，在上方分级雕刻（Level 1 粗胚，Level 2 中轮廓，Level 3 微细节与划痕）。
  - 优势：可随时烘焙法线贴图 (Bake Normal Map)，适合生产管线。

### 3. 对称与镜像控制 (Symmetry)
- 视口右上角支持一键开启 `X / Y / Z` 轴对称。
- 径向对称 (Radial Symmetry)：适用于制作车轮、魔法阵或徽章上的花纹结构。

---

## ⌨️ 常用快捷键速查表

| 操作 | 快捷键 | 功能说明 |
| :--- | :--- | :--- |
| **进入雕刻模式** | `Ctrl + Tab` -> 向上滑选 `Sculpt` | 快速模式切换饼菜单 |
| **调整笔刷半径** | `F` | 鼠标左右滑动快速缩放笔刷大小 |
| **调整笔刷强度** | `Shift + F` | 调整笔刷作用力深度 |
| **正反向雕刻** | 按住 `Ctrl` | 默认凸起变凹陷，反之亦然 |
| **平滑笔刷** | 按住 `Shift` | 随时对局部区域进行软化平滑 |
| **隐藏/遮罩** | `M` (Mask) / `Alt + M` (Clear) | 绘制遮罩保护特定区域不被雕刻变形 |

---

## 💡 实践步骤与练习建议
1. 打开 `02_sculpting.blend`，默认已选中雕刻主体。
2. 按 `Ctrl + Tab` 切换至 **Sculpt Mode**。
3. 选择 **Clay Strips**（或按快捷键 `X`），按 `F` 调整笔刷大小，在勋章表面雕刻出浮雕神兽纹理或几何符文。
4. 使用 **Crease** 笔刷沿轮廓划出深槽，按住 `Shift` 轻扫平滑接缝。
