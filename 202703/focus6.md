# WebGPU 與 WASM：瀏覽器端渲染

## Rust → WASM 編譯與 Canvas 整合（2021-2026）

### 前言

WebGPU 的殺手級應用——在瀏覽器中執行 Rust 編寫的 3D 渲染引擎。Rust 編譯成 WebAssembly（WASM），WebGPU 提供 GPU 存取，兩者結合讓瀏覽器成為一個高效能的 3D 渲染平台。

### Rust → WASM 編譯流程

**工具鏈選擇**：

| 工具 | 用途 | 命令 |
|------|------|------|
| `wasm-pack` | 打包 Rust crates 為 npm 套件 | `wasm-pack build --target web` |
| `trunk` | 一體化 WASM 應用建置工具 | `trunk serve` |
| `wasm-bindgen` | Rust-JS 綁定產生器 | 內建於 wasm-pack |

**使用 trunk（推薦方式）**：

建立專案結構：

```
my_app/
├── Cargo.toml
├── index.html
└── src/
    └── main.rs
```

`Cargo.toml`：

```toml
[package]
name = "my_app"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wgpu = "23.0"
wasm-bindgen = "0.2"
js-sys = "0.3"
web-sys = { version = "0.3", features = ["Window", "Document", "HtmlCanvasElement"] }
```

`index.html`：

```html
<!DOCTYPE html>
<html>
<head><title>wgpu WASM Demo</title></head>
<body>
    <canvas id="gpu-canvas"></canvas>
    <script type="module">
        import init from './pkg/my_app.js';
        init().catch(console.error);
    </script>
</body>
</html>
```

`src/main.rs`：

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen(start)]
pub async fn run() {
    // 取得 Canvas
    let document = web_sys::window().unwrap().document().unwrap();
    let canvas = document
        .get_element_by_id("gpu-canvas")
        .unwrap()
        .dyn_into::<web_sys::HtmlCanvasElement>()
        .unwrap();

    // 建立 wgpu Instance（瀏覽器模式）
    let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor::default());
    let surface = instance.create_surface_from_canvas(canvas).unwrap();
    let adapter = instance.request_adapter(&wgpu::RequestAdapterOptions {
        compatible_surface: Some(&surface),
        ..Default::default()
    }).await.unwrap();
    let (device, queue) = adapter.request_device(&Default::default(), None).await.unwrap();

    // ... 其餘流程與原生版本完全相同 ...
}
```

執行：

```bash
trunk serve
# 在 http://127.0.0.1:8080 開啟
```

### Canvas 整合與 requestAnimationFrame

瀏覽器中的渲染迴圈使用 `requestAnimationFrame`（rAF）驅動：

```rust
use wasm_bindgen::prelude::*;
use web_sys::window;

fn start_render_loop(device: wgpu::Device, queue: wgpu::Queue, surface: wgpu::Surface) {
    let f = Closure::<dyn FnMut()>::new(move || {
        // 渲染一幀
        let frame = surface.get_current_texture().unwrap();
        let view = frame.texture.create_view(&Default::default());
        let mut encoder = device.create_command_encoder(&Default::default());
        {
            let mut rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
                color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                    view: &view,
                    ops: wgpu::Operations {
                        load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                        store: wgpu::StoreOp::Store,
                    },
                    ..Default::default()
                })],
                ..Default::default()
            });
            rpass.set_pipeline(&pipeline);
            rpass.draw(0..3, 0..1);
        }
        queue.submit(Some(encoder.finish()));
        frame.present();

        // 請求下一幀
        window().unwrap().request_animation_frame(
            // 需要重新排程 Closure
        ).unwrap();
    });

    window().unwrap().request_animation_frame(f.as_ref().unchecked_ref()).unwrap();
    f.forget(); // 防止 Closure 被 drop
}
```

**rAF 的行為**：
- 與顯示器的更新頻率同步（通常 60Hz 或 120Hz）
- 當頁面在背景頁籤時自動暫停（省電）
- 提供 `DOMHighResTimeStamp` 參數用於動畫計算

### WebGPU vs WebGL 2.0

| 特性 | WebGL 2.0 | WebGPU |
|------|-----------|--------|
| 著色器語言 | GLSL ES 300 | WGSL |
| 管線模型 | 狀態機 | PSO（管線狀態物件） |
| 多執行緒 | 不支援 | 支援 OffscreenCanvas + Worker |
| 計算著色器 | 無（需要擴展） | 原生支援 |
| 非同步操作 | 阻塞 | 非同步 |
| 除錯能力 | 有限 | Chrome DevTools 完整支援 |
| 效能 | 驅動開銷大 | 低開銷，接近原生 |
| 行動裝置支援 | 廣泛 | 持續增長 |

**效能實測（典型場景）**：

```
Draw Call 開銷：
  WebGL 2.0:  ~0.5-1.0 µs per draw call
  WebGPU:     ~0.05-0.1 µs per draw call  (5-10x 改善)

初始載入時間（萬個三角形場景）：
  WebGL 2.0:  ~2.5s（著色器編譯阻塞主執行緒）
  WebGPU:     ~0.8s（非同步編譯）
```

### 瀏覽器中的除錯與效能調校

**Chrome DevTools 的 WebGPU 工具**：

1. **Performance 面板**：
   - 勾選「WebGPU」追蹤來檢視 GPU 命令佇列時間線
   - 辨識管線屏障和資源轉換的瓶頸

2. **Memory 面板**：
   - 檢視所有 GPU 資源（紋理、緩衝區、BindGroup）
   - 監控 GPU 記憶體使用量

3. **Application 面板**：
   - 檢查 WebGPU 配接器資訊和功能支援
   - 檢視著色器原始碼和編譯後的中間表示

**利用 WebGPU 的錯誤範圍**：

```rust
device.push_error_scope(wgpu::ErrorFilter::Validation);

// 執行可能出錯的操作
let invalid_texture = device.create_texture(&wgpu::TextureDescriptor {
    size: wgpu::Extent3d { width: 0, height: 0, depth_or_array_layers: 1 }, // 無效尺寸
    ..Default::default()
});

if let Some(err) = device.pop_error_scope().await.unwrap() {
    web_sys::console::error_1(&format!("WebGPU Error: {:?}", err).into());
}
```

**常見的瀏覽器瓶頸**：

```
瓶頸 1：緩衝區上傳（CPU→GPU 傳輸）
   解決：使用 staging belt 批次上傳，減少 submit 次數

瓶頸 2：過多的 Draw Call
   解決：使用 instancing 或 indirect draw

瓶頸 3：著色器編譯時間
   解決：使用 pipeline cache，預先編譯常用著色器

瓶頸 4：WASM 與 JS 的通訊開銷
   解決：減少 wasm-bindgen 跨語言呼叫，批次處理
```

### OffscreenCanvas 與 Worker

WebGPU 的一大優勢是支援在 Worker 執行緒中執行渲染：

```js
// main.js
const canvas = document.getElementById('gpu-canvas');
const offscreen = canvas.transferControlToOffscreen();
const worker = new Worker('renderer.js');
worker.postMessage({ canvas: offscreen }, [offscreen]);
```

這讓主執行緒可以專注於 UI 響應，而 GPU 渲染在背景執行緒中進行——對需要大量計算的 3D 應用尤為重要。

### 小結

Rust + WASM + WebGPU 是當前瀏覽器端 3D 渲染的最強組合。Rust 提供了記憶體安全和高效能，WASM 讓 Rust 程式碼在瀏覽器中執行，而 WebGPU 則提供了接近原生的 GPU 存取能力。三者結合，讓網頁 3D 應用的效能和品質達到了前所未有的高度。

---

**下一步**：[AI 輔助 3D 渲染與著色器開發](focus7.md)

## 延伸閱讀

- [Rust WASM 開發指南](https://www.google.com/search?q=Rust+WebAssembly+wasm+pack+tutorial)
- [WebGPU 瀏覽器支援狀態](https://www.google.com/search?q=WebGPU+browser+support+2026)
- [Chrome DevTools WebGPU 除錯](https://www.google.com/search?q=Chrome+DevTools+WebGPU+debugging)
