# WebGPU 設計哲學

## 安全、非同步、跨平台的 GPU 標準（2017-2026）

### 為何需要新的 Web 圖形 API

WebGL 是 OpenGL ES 的瀏覽器移植版，始於 2011 年。十五年後，它的設計缺陷變得越來越明顯：

- **狀態機架構**：所有渲染狀態（紋理、緩衝區、著色器）都綁定到一個全域上下文。狀態變更的順序可能產生隱藏的 Bug。
- **同步操作**：著色器編譯、紋理上傳都會阻塞主執行緒，導致頁面卡頓。
- **缺乏多執行緒**：WebGL 不支援從 worker 執行緒發出繪圖命令。
- **效能開銷**：驅動程式需要處理大量隱式狀態推斷，無法有效平行化。

與此同時，新一代原生 GPU API——Vulkan（2016）、DirectX 12（2015）、Metal（2014）——從設計上解決了這些問題。但它們的 API 過於底層，不適合直接暴露在瀏覽器中使用。

### WebGPU 的誕生

2017 年，Apple、Google、Mozilla 和 Microsoft 聯手啟動了一個新項目——最初名為「WebGPU」。目標是設計一個：

> 比 Vulkan 安全、比 Metal 跨平台、比 DirectX 12 簡潔——同時保留現代 GPU API 的效能優勢。

標準化歷程：

| 年份 | 里程碑 |
|------|--------|
| 2017 | W3C GPU for the Web Community Group 成立 |
| 2018 | 第一版草案：核心概念（Device、Queue、Pipeline） |
| 2019 | WGSL 被選為 WebGPU 的著色器語言 |
| 2020 | wgpu-native 實作在 Firefox 中試驗 |
| 2021 | WebGPU 在 Chrome 中預設啟用 |
| 2022 | Safari 開始支援 WebGPU（Metal 後端） |
| 2023 | WebGPU 1.0 候選推薦標準 |
| 2024 | WebGPU 成為 W3C 正式推薦標準 |
| 2025 | WebGPU 2.0 工作開始（子群組、動態渲染） |
| 2026 | 所有主流瀏覽器完整支援 WebGPU |

### 與 Vulkan/DX12/Metal 的比較

```
WebGPU  ─── 跨平台抽象層
   │
   ├── 後端：Vulkan ─── Windows / Linux / Android
   ├── 後端：Metal  ─── macOS / iOS
   ├── 後端：DX12  ─── Windows 10+
   └── 後端：Dawn  ─── 軟體實作 / 無頭渲染
```

| 特性 | Vulkan | DX12 | Metal | WebGPU |
|------|--------|------|-------|--------|
| 記憶體管理 | 顯式 | 顯式 | 自動 | 自動（引用計數） |
| 著色器語言 | SPIR-V | HLSL | MSL | WGSL |
| 管線狀態 | PSO | PSO | MTLRenderPipelineState | RenderPipeline |
| 同步原語 | Semaphore/Fence | Fence | Fence | 自動（Queue 序列化） |
| 綁定模型 | Descriptor Set | Descriptor Heap | Argument Buffer | BindGroup |
| 除錯工具 | Vulkan Validation Layers | PIX | GPU Capture | Chrome DevTools |

WebGPU 的核心取捨：**在保留底層控制力的同時，消除最常見的錯誤模式**。

### 三大設計原則

**1. 安全**

WebGPU 從 API 層級消除了大量錯誤：

```rust
// 安全：WebGPU 不允許懸空指標
let texture = device.create_texture(&desc);
let view = texture.create_view(&view_desc);
// texture 被 drop 時，view 也會自動失效
// 沒有 use-after-free 的可能

// 安全：BindGroup 佈局在建立時驗證
let bind_group = device.create_bind_group(&BindGroupDescriptor {
    layout: &bind_group_layout,  // 型別檢查！
    entries: &[...],             // 條目數量和型別必須與佈局匹配
});
// 執行期不會有「綁定型別錯誤」
```

與 Vulkan 的明顯對比：Vulkan 中不正確的 descriptor set 配置可能導致 GPU 崩潰或隨機錯誤；WebGPU 在裝置端（CPU）進行完整驗證。

**2. 非同步**

所有可能耗時的操作都是非同步的：

```rust
// 著色器編譯非同步——不阻塞主執行緒
let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor { ... });
// 立即返回，編譯在背景執行

// Adapter 請求非同步
let adapter = instance.request_adapter(&options).await;
// 不會凍結 UI

// 緩衝區映射非同步
let buf = device.create_buffer(&desc);
buf.slice(..).map_async(wgpu::MapMode::Read, |result| {
    // 這個回呼在映射完成時執行
});
```

這對瀏覽器環境尤為重要——主執行緒的任何阻塞都會直接影響用戶體驗。

**3. 跨平台**

同一份 WebGPU 程式碼可以在不同平台上獲得一致的結果：

```rust
let instance = wgpu::Instance::new(wgpu::InstanceDescriptor {
    backends: wgpu::Backends::PRIMARY, // Vulkan + Metal + DX12
    ..Default::default()
});
// 不需要 `#[cfg(target_os = "...")]` 條件編譯
// 不需要平台特定的表面創建程式碼
```

wgpu 更進一步：它在瀏覽器外使用原生後端，在瀏覽器內使用 WebGPU 標準——同一份 Rust 程式碼可以編譯成原生執行檔和 WASM 模組。

### 參考實作

- **wgpu**（Rust）：最成熟的 WebGPU 實作，也是 Firefox 的內建引擎
- **Dawn**（C++）：Google 的實作，用於 Chrome
- **D3D12 後端**：僅在 Windows 上使用

三個實作都通過了 WebGPU CTS（一致性測試套件），確保 API 行為在各平台間一致。

### 小結

WebGPU 不是「Web 版的 Vulkan」。它是一個全新的設計：汲取了現代 GPU API 的精華，同時去除了它們的複雜性和安全隱患。對於 Rust 開發者來說，wgpu 讓 GPU 程式設計變得可接觸、安全且跨平台——這是 OpenGL 和 Vulkan 從未實現過的承諾。

---

**下一步**：[wgpu 核心 API 入門](focus3.md)

## 延伸閱讀

- [WebGPU Specification](https://www.google.com/search?q=WebGPU+specification)
- [W3C GPU for the Web Working Group](https://www.google.com/search?q=W3C+GPU+for+the+Web+Working+Group)
- [WebGPU vs Vulkan vs Metal vs DirectX 12](https://www.google.com/search?q=WebGPU+vs+Vulkan+vs+Metal+vs+DirectX+12+comparison)
