# GPU 管線基礎

## 固定功能管線到可編程管線（1990-2026）

### 前言

GPU 的發展史本質上是一部從「固定功能」走向「可編程」的歷史。理解這個演變，是掌握現代圖形 API（包括 WebGPU）的關鍵。

### 固定功能管線時代（1990-2000s）

早期的 GPU 像是一條硬體工廠流水線——每個階段的功能是固定的，開發者只能透過參數調整行為：

```
應用程式 → 頂點變換 → 光柵化 → 紋理貼圖 → 深度測試 → 輸出
   (固定)    (固定)    (固定)    (固定)     (固定)
```

**OpenGL 1.0（1992）** 是這個時代的代表。開發者使用 `glTranslatef()`、`glRotatef()` 等函數來控制變換，使用 `glLightfv()` 設定光照參數。所有計算都在 GPU 上用固定電路完成。

優點是簡單直觀；缺點是缺乏彈性——如果你想實現自訂的光照模型或非標準的變換效果，固定功能管線無法滿足。

### 可編程管線的革命（2001-2010）

**NVIDIA GeForce 3（2001）** 引入了第一款可編程頂點著色器。這是 GPU 架構的分水嶺——開發者現在可以編寫小程式（shader）來控制 GPU 的特定階段。

```
應用程式 → 頂點著色器 → 光柵化 → 片段著色器 → 混合 → 輸出
   (可編程)    (可編程)   (固定)    (可編程)     (固定)
```

著色器語言的演進：

| 階段 | 語言 | 代表 API | 年份 |
|------|------|---------|------|
| 組合器著色器 | NV_vertex_program | OpenGL 擴展 | 2001 |
| 高階著色器 | Cg、HLSL、GLSL | DirectX 9 / OpenGL 2.0 | 2003-2004 |
| 統一架構 | GLSL / HLSL | DirectX 10 / OpenGL 3.3 | 2006-2010 |
| 通用計算 | CUDA / OpenCL / Compute Shader | GPGPU | 2007-2012 |

### 現代 GPU 管線架構

當前的 GPU 管線由多個可編程階段和固定功能階段交錯組成：

```
頂點輸入
   ↓
⦿ 頂點著色器（Vertex Shader）— 可編程
   ↓   每個頂點執行一次：位置變換、權重混合、頂點動畫
曲面細分（Tessellation）— 可選可編程
   ↓   將三角形細分為更小的三角形
幾何著色器（Geometry Shader）— 可選可編程
   ↓   產生/消滅圖元
光柵化（Rasterization）— 固定功能
   ↓   將三角形轉換為像素片段
⦿ 片段著色器（Fragment Shader）— 可編程
   ↓   每個片段執行一次：光照、紋理、顏色計算
深度/模板測試 — 固定功能
   ↓
顏色混合 — 固定功能
   ↓
幀緩衝（Frame Buffer）
```

### 計算著色器（Compute Shader）

2012 年之後，GPU 加入了第三種著色器——**計算著色器**。它不屬於傳統的渲染管線，而是讓 GPU 作為通用並行處理器：

```wgsl
// 計算著色器範例：矩陣乘法
@compute @workgroup_size(16, 16)
fn cs_main(
    @builtin(global_invocation_id) id: vec3<u32>,
    @group(0) @binding(0) var<storage, read>  a: array<f32>,
    @group(0) @binding(1) var<storage, read>  b: array<f32>,
    @group(0) @binding(2) var<storage, read_write> c: array<f32>,
) {
    let row = id.y;
    let col = id.x;
    // 計算 C[row][col] = A[row][:] · B[:][col]
    var sum = 0.0;
    for (var k = 0u; k < 256u; k++) {
        sum += a[row * 256 + k] * b[k * 256 + col];
    }
    c[row * 256 + col] = sum;
}
```

計算著色器的應用遠超圖形：物理模擬、後處理特效、AI 推理、雜湊計算。

### 管線狀態物件（PSO）

在 Vulkan、DirectX 12 和 WebGPU 中，**管線狀態物件（Pipeline State Object）** 是渲染管線的完整描述。它是一個不可變的物件，包含了管線的所有配置：

```
RenderPipelineDescriptor {
    vertex:   { module, entry_point, buffers[] }
    fragment: { module, entry_point, targets[] }
    primitive: { topology, cull_mode, front_face }
    depth_stencil: { format, depth_write, depth_compare }
    multisample: { count, mask }
    layout: { bind_group_layouts[] }
}
```

PSO 的設計理念：**將管線狀態固化為不可變物件**。與傳統 OpenGL 的「全域狀態機」不同，PSO 消除了狀態洩漏和隱式依賴，讓驅動程式可以在建立時完成所有驗證和最佳化。

### 圖形 API 的抽象層級

| 層級 | API | 抽象程度 | 開發者控制 |
|------|-----|---------|-----------|
| 高層 | Three.js / Babylon.js | 最高 | 最少 |
| 中層 | WebGPU / wgpu | 中 | 中 |
| 底層 | Vulkan / DX12 / Metal | 低 | 高 |
| 硬體 | GPU 指令集 | 最低 | 最高 |

### 小結

從固定功能到可編程管線，GPU 的演進反映了電腦圖形學對靈活性和效能的不斷追求。現代的 GPU 管線由頂點著色器、片段著色器和計算著色器三大支柱構成，而 PSO 則是將這些元件統一起來的設計模式。WebGPU/wgpu 將這些概念以安全、跨平台的方式呈現，讓開發者可以直接控制 GPU 管線的各個階段。

---

**下一步**：[WebGPU 設計哲學](focus2.md)

## 延伸閱讀

- [GPU 管線架構](https://www.google.com/search?q=GPU+pipeline+architecture+vertex+fragment+shader)
- [Graphics Pipeline - NVIDIA Developer](https://www.google.com/search?q=NVIDIA+graphics+pipeline+overview)
- [WebGPU Render Pipeline](https://www.google.com/search?q=WebGPU+render+pipeline+state+object)
