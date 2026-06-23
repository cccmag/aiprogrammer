# 本期焦點

## Rust 與 WebGPU — 從 wgpu 到瀏覽器端的 3D 渲染

### 引言

過去十年，網頁 3D 渲染被 WebGL 統治。WebGL 是 OpenGL ES 的瀏覽器移植版，但它的設計始於 2000 年代初期——狀態機架構、全域綁定、缺乏多執行緒支援——這些包袱讓現代 GPU 無法充分發揮。

WebGPU 的出現改變了這一切。作為新一代圖形 API，WebGPU 借鑒了 DirectX 12、Vulkan 和 Metal 的設計理念，但以更安全、更跨平台的方式呈現。而 Rust——透過 wgpu crate——成為了 WebGPU 的「一等公民」語言。

wgpu 是 WebGPU 規範的 Rust 實作。它不僅能在瀏覽器中執行（透過 WASM），也能原生執行（透過 Vulkan/Metal/DX12 後端），甚至能在 Linux 伺服器上進行無頭渲染。這意味著：**同一份渲染程式碼，可以在瀏覽器、桌面、行動裝置和伺服器上無縫執行**。

本期將帶領你從 GPU 管線的基礎概念開始，逐步深入 wgpu 的程式設計模型，最後探討 AI 如何輔助 3D 渲染與著色器開發。

---

## 大綱

* [程式：實作 wgpu 三角形渲染器](focus_code.md)
   - wgpu 實例、設備、佇列
   - 渲染管線與著色器
   - 頂點緩衝區與索引緩衝區
   - 遊戲/渲染迴圈

1. [GPU 管線基礎（1990-2026）](focus1.md)
   - 固定功能管線 vs 可編程管線
   - 頂點著色器、片段著色器、計算著色器
   - 渲染管線狀態物件（PSO）

2. [WebGPU 設計哲學（2017-2026）](focus2.md)
   - WebGPU 的誕生與標準化歷程
   - 與 Vulkan/DX12/Metal 的比較
   - 安全、非同步、跨平台

3. [wgpu 核心 API 入門（2019-2026）](focus3.md)
   - 實例、介面卡、設備的建立
   - 交換鏈與幀緩衝
   - 綁定組與佈局

4. [著色器程式設計：WGSL（2021-2026）](focus4.md)
   - WGSL 語法基礎
   - 頂點/片段/計算著色器範例
   - 著色器除錯與最佳化

5. [紋理、取樣與材質系統（2020-2026）](focus5.md)
   - 紋理建立與上傳
   - 取樣器配置
   - PBR 材質管線實作

6. [WebGPU 與 WASM：瀏覽器端渲染（2021-2026）](focus6.md)
   - Rust → WASM 編譯流程
   - Canvas 整合與事件處理
   - 效能調校與 DevTools

7. [AI 輔助 3D 渲染與著色器開發（2024-2026）](focus7.md)
   - LLM 生成 WGSL 著色器
   - AI 驅動的材質生成
   - 神經渲染與 NeRF 整合

---

## 渲染管線層次

```
應用層 (遊戲邏輯、場景管理、物理)
      │  命令編碼
wgpu 核心 (Device、Queue、SwapChain、BindGroup)
      │  GPU 驅動層
圖形 API 後端 (Vulkan / Metal / DirectX 12)
      │
GPU 硬體 (頂點處理、光柵化、片段處理、計算)
```

## 濃縮回顧

### 圖形 API 演進

| 時代 | API | 設計哲學 | 語言 |
|------|-----|---------|------|
| 1990s | OpenGL 1.0 | 固定功能管線 | C |
| 2000s | OpenGL 2.0+ / D3D9 | 可編程著色器 | C/C++ |
| 2010s | OpenGL ES / WebGL | 行動/瀏覽器移植 | JS/GLSL |
| 2016+ | Vulkan / D3D12 / Metal | 高效顯式控制 | C/C++/MSL |
| 2020+ | WebGPU / wgpu | 安全跨平台 GPU | WGSL/Rust |

### 為什麼 Rust + WebGPU？

- **記憶體安全**：wgpu 在 Rust 中利用所有權模型管理 GPU 資源，消除懸空指標和 use-after-free
- **非同步編譯**：著色器編譯回傳 `Future`，不阻塞主執行緒
- **零成本抽象**：BindGroup 佈局在編譯期檢查，無執行期開銷
- **跨平台一致**：同一份程式碼在 Windows (DX12)、macOS (Metal)、Linux (Vulkan)、Web (WASM+WebGPU) 上執行

### wgpu 核心模式

wgpu 遵循 GPU 管線的現代設計：

```rust
// 1. 建立實例與設備
let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor::default());
let adapter = instance.request_adapter(&wgpu::RequestAdapterOptions::default()).await.unwrap();
let (device, queue) = adapter.request_device(&wgpu::DeviceDescriptor::default(), None).await.unwrap();

// 2. 建立交換鏈
let config = wgpu::SurfaceConfiguration { ... };
surface.configure(&device, &config);

// 3. 建立渲染管線
let pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
    vertex: wgpu::VertexState { module: &shader, entry_point: "vs_main", ... },
    fragment: Some(wgpu::FragmentState { module: &shader, entry_point: "fs_main", ... }),
    ...
});

// 4. 渲染迴圈
loop {
    let frame = surface.get_current_texture().unwrap();
    let view = frame.texture.create_view(&wgpu::TextureViewDescriptor::default());
    let mut encoder = device.create_command_encoder(...);
    {
        let mut rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor { ... });
        rpass.set_pipeline(&pipeline);
        rpass.draw(0..3, 0..1);
    }
    queue.submit(Some(encoder.finish()));
    frame.present();
}
```

### 著色器範例 (WGSL)

```wgsl
// 頂點著色器
@vertex
fn vs_main(@builtin(vertex_index) in_vertex_index: u32) -> @builtin(position) vec4<f32> {
    let pos = array<vec2<f32>, 3>(
        vec2( 0.0,  0.5),
        vec2(-0.5, -0.5),
        vec2( 0.5, -0.5),
    );
    return vec4<f32>(pos[in_vertex_index], 0.0, 1.0);
}

// 片段著色器
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.3, 0.6, 0.9, 1.0); // 淡藍色
}
```

---

**下一步**：[程式實作](focus_code.md) → [GPU 管線基礎](focus1.md)

## 延伸閱讀

- [WebGPU 規範](https://www.google.com/search?q=WebGPU+specification)
- [wgpu 官方文件](https://www.google.com/search?q=wgpu+rust+documentation)
- [WGSL 規範](https://www.google.com/search?q=WGSL+shading+language)
- [Learn WGPU](https://www.google.com/search?q=learn+wgpu+tutorial)
