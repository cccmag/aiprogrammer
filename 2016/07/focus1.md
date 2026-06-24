# 電腦圖學導論

## 什麼是電腦圖學？

電腦圖學（Computer Graphics）是研究如何用電腦產生、處理和顯示圖形的學問。它涵蓋了從 2D 平面設計到 3D 立體渲染的廣泛領域。

## 3D 繪圖的歷史演進

### 1960-1970 年代：開創期

- 1963 年：Ivan Sutherland 開發 Sketchpad，開創互動式電腦圖形
- 1968 年：Wylie 等人提出深度緩沖演算法（Z-Buffer）
- 1970 年代：Appel 提出光線追蹤（Ray Tracing）概念

### 1980 年代：消費化萌芽

- 1981 年：IBM 發布 PC 與 CGA 圖形介面
- 1984 年：SGI 推出第一台圖形工作站
- 幾何處理開始從主機轉移到專用硬體

### 1990 年代：3D 遊戲興起

- 1992 年：id Software 發布《Wolfenstein 3D》
- 1993 年：《DOOM》引領第一人稱射擊遊戲風潮
- 1996 年：《Quake》展示完整的 3D 引擎
- 固定功能圖形加速卡（如 3dfx Voodoo）問世

### 2000 年代：可程式化時代

- 2001 年：DirectX 8 引入著色器（Shader）概念
- 2004 年：NVIDIA GeForce 6800 支援 Cg/HLSL 著色器
- GPU 從固定功能走向完全可程式化

### 2010 年代：即時光追蹤

- 2018 年：NVIDIA RTX 系列顯示卡支援硬體光線追蹤
- 2020 年代：光追技術開始普及到消費級遊戲

## 光柵化與光線追蹤

### 光柵化（Rasterization）

光柵化是現代即時 3D 圖形的核心技術。它將 3D 場景中的三角形投射到 2D 螢幕上，計算每個像素的顏色。

```
3D 場景 → 視窗變換 → 剪裁 → 透視除法 → 視口變換 → 光柵化 → 像素
```

**優點**：
- 速度極快，適合即時渲染
- 硬體支援成熟

**缺點**：
- 全域光照效果難以類比
- 陰影、反射需要額外技術

### 光線追蹤（Ray Tracing）

光線追蹤模擬真實光線的行為，從眼睛發射光線穿過每個像素，追蹤光線與場景中物體的交互。

```python
for each pixel:
    ray = create_ray_from_camera_through_pixel(pixel)
    color = trace_ray(ray, scene)
    set_pixel_color(pixel, color)

def trace_ray(ray, scene, depth):
    hit = scene.intersect(ray)
    if hit is None:
        return background_color
    return compute_lighting(hit, ray, scene)
```

**優點**：
- 自然處理反射、折射、陰影
- 結果逼真

**缺點**：
- 計算量大，需要專用硬體加速

## 圖學流水線概述

### 應用程式階段

在 CPU 端進行：
- 場景圖管理
- 幾何資料準備
- 可見性裁剪

### 幾何處理階段

在 GPU 頂點著色器中執行：
- 模型座標 → 世界座標 → 視圖座標 → 剪裁座標
- 頂點光照計算
- 投影變換

### 光柵化階段

- 三角形設定
- 三角形遍歷
- 片段生成

### 片段處理階段

在 GPU 片段著色器中執行：
- 紋理取樣
- 像素光照
- 深度測試
- 混合輸出

## 常見座標系統

| 座標系統 | 說明 |
|---------|------|
| 模型座標 | 模型的本地座標 |
| 世界座標 | 場景中的全局座標 |
| 視圖座標 | 攝影機為原點的座標 |
| 剪裁座標 | 透視投影後的座標 |
| NDC | 正規化裝置座標 |
| 螢幕座標 | 實際像素位置 |

## 參考資料

- [電腦圖學歷史](https://www.google.com/search?q=history+of+computer+graphics+timeline)
- [光柵化 vs 光線追蹤](https://www.google.com/search?q=rasterization+vs+ray+tracing+explained)
- [3D 圖形流水線](https://www.google.com/search?q=3D+graphics+pipeline+explained)