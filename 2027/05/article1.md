# 瀏覽器中的 WebAssembly — 從 WebGL 到 WebGPU 的實戰應用

## 1. 引言

WebAssembly 在瀏覽器中的應用已經超越了 MVP 時代的「計算加速器」角色。從影像處理、3D 渲染到資料視覺化，WASM 在瀏覽器中扮演著愈來愈重要的角色。而 WebGPU 的到來更開啟了 WASM 直接操控 GPU 的大門。

## 2. WebGL 時代的 WASM

在 WebGPU 到來之前，WebGL 是瀏覽器中唯一的高效能圖形 API。WASM 與 WebGL 的結合模式非常成熟：

```rust
use wasm_bindgen::prelude::*;
use web_sys::WebGlRenderingContext;

#[wasm_bindgen]
pub fn draw_triangle(ctx: &WebGlRenderingContext) {
    let vs_source = include_str!("shader.vert");
    let fs_source = include_str!("shader.frag");

    // 在 WASM 中編譯 WebGL 著色器
    let vs = ctx.create_shader(WebGlRenderingContext::VERTEX_SHADER).unwrap();
    ctx.shader_source(&vs, vs_source);
    ctx.compile_shader(&vs);

    let fs = ctx.create_shader(WebGlRenderingContext::FRAGMENT_SHADER).unwrap();
    ctx.shader_source(&fs, fs_source);
    ctx.compile_shader(&fs);

    let program = ctx.create_program().unwrap();
    ctx.attach_shader(&program, &vs);
    ctx.attach_shader(&program, &fs);
    ctx.link_program(&program);
    ctx.use_program(Some(&program));

    // 繪製三角形
    ctx.draw_arrays(WebGlRenderingContext::TRIANGLES, 0, 3);
}
```

這種模式的核心優勢在於：**WASM 可以直接操作 WebGL 物件的指標，無需經過 JavaScript 中介**。這對於需要大量 WebGL 呼叫的場景（如批次繪製數萬個頂點）意義重大。

## 3. 資料視覺化與 Canvas 2D

對於 2D 資料視覺化，WASM + Canvas 2D 的組合具有明顯的效能優勢：

```rust
use wasm_bindgen::prelude::*;
use web_sys::CanvasRenderingContext2d;

#[wasm_bindgen]
pub fn render_scatter_plot(
    ctx: &CanvasRenderingContext2d,
    data_x: &[f64],
    data_y: &[f64],
    width: f64,
    height: f64,
) {
    // 清除畫布
    ctx.clear_rect(0.0, 0.0, width, height);

    // 批次繪製數萬個資料點
    for (&x, &y) in data_x.iter().zip(data_y.iter()) {
        let px = (x * width) as f64;
        let py = (y * height) as f64;
        ctx.begin_path();
        ctx.arc(px, py, 2.0, 0.0, std::f64::consts::PI * 2.0).unwrap();
        ctx.fill();
    }
}
```

當資料點數量超過 10,000 時，WASM 版本的渲染速度可以達到純 JavaScript 版本的 **3-5 倍**。原因是 WASM 避免了 JavaScript 的動態型別開銷，且迴圈中的向量化最佳化更有效。

## 4. WebGPU：WASM 與 GPU 的直接橋接

WebGPU 是 WebGL 的下一代替代品，提供了更接近 Vulkan/Metal/DirectX 12 的 GPU 控制能力。WASM + WebGPU 的組合讓瀏覽器中的 GPU 運算達到前所未有的效能：

```rust
use wasm_bindgen::prelude::*;
use web_sys::{
    GpuAdapter, GpuDevice, GpuBuffer,
    GpuComputePipeline, GpuBindGroup,
};

#[wasm_bindgen]
pub struct GpuComputeEngine {
    device: GpuDevice,
    pipeline: GpuComputePipeline,
    bind_group: GpuBindGroup,
    output_buffer: GpuBuffer,
}

#[wasm_bindgen]
impl GpuComputeEngine {
    pub async fn new(adapter: GpuAdapter) -> Result<GpuComputeEngine, JsValue> {
        let device = adapter.request_device(&JsValue::null(), None).await?;

        // 編譯計算著色器（WGSL）
        let shader_module = device.create_shader_module(&{
            let mut desc = web_sys::GpuShaderModuleDescriptor::new(
                include_str!("compute.wgsl")
            );
            desc
        });

        let pipeline = device.create_compute_pipeline(&{
            web_sys::GpuComputePipelineDescriptor::new(
                &web_sys::GpuProgrammableStageDescriptor::new(
                    &shader_module, "main"
                ),
            )
        });

        // 建立 GPU 緩衝區
        let output_buffer = device.create_buffer(&{
            let mut desc = web_sys::GpuBufferDescriptor::new(
                1024 * 1024, // 1MB
                web_sys::GpuBufferUsage::STORAGE
                    | web_sys::GpuBufferUsage::COPY_SRC,
            );
            desc
        });

        Ok(GpuComputeEngine { device, pipeline, bind_group, output_buffer })
    }

    pub fn compute(&self, input: &[f32]) -> Vec<f32> {
        // 將輸入資料上傳到 GPU
        let staging_buffer = self.device.create_buffer_with_data(
            bytemuck::cast_slice(input),
            web_sys::GpuBufferUsage::COPY_DST,
        );

        // 建立命令編碼器
        let encoder = self.device.create_command_encoder(&JsValue::null());

        {
            let pass = encoder.begin_compute_pass(&JsValue::null());
            pass.set_pipeline(&self.pipeline);
            pass.set_bind_group(0, &self.bind_group, &[]);
            pass.dispatch_workgroups(32, 32, 1);
            pass.end();
        }

        // 讀取結果
        encoder.copy_buffer_to_buffer(
            &self.output_buffer, 0,
            &staging_buffer, 0,
            1024 * 1024,
        );

        self.device.queue().submit(&[encoder.finish()]);

        // 將 GPU 緩衝區映射到 WASM 線性記憶體
        let promise = self.output_buffer.map_async(
            web_sys::GpuMapMode::READ,
        );
        // ... 等待 Promise 完成

        let mapped_range = self.output_buffer.get_mapped_range();
        let result: Vec<f32> = bytemuck::cast_slice(&mapped_range).to_vec();
        self.output_buffer.unmap();

        result
    }
}
```

WebGPU 的計算著色器（Compute Shader）讓 WASM 可以將大量平行運算卸載到 GPU。對於矩陣乘法、卷積神經網路、粒子模擬等任務，效能提升可達 **10-50 倍**。

## 5. JS-WASM-GPU 三層架構

現代瀏覽器應用常採用三層架構：

```
三層協作模式：
─────────────────────────

JavaScript（協調層）
├── DOM 操作
├── 事件處理
├── 網路請求
├── 生命週期管理
│
WASM（計算層）
├── 演算法邏輯
├── 資料處理
├── WebGPU API 呼叫
├── 記憶體管理
│
GPU（硬體加速層）
├── 頂點處理
├── 計算著色器
├── 光柵化
└── 紋理取樣
```

## 6. 記憶體管理最佳化

瀏覽器 WASM 的記憶體管理是效能的關鍵：

```rust
// 使用 wasm-bindgen 的共享記憶體機制
use wasm_bindgen::Clamped;
use js_sys::Uint8Array;

#[wasm_bindgen]
pub fn process_image(
    buffer: Clamped<Vec<u8>>,
    width: u32,
    height: u32,
) -> Clamped<Vec<u8>> {
    // 直接操作線性記憶體中的像素資料
    // 無需跨邊界複製
    let pixels = buffer.0;
    let mut result = pixels.clone();

    for y in 0..height {
        for x in 0..width {
            let idx = ((y * width + x) * 4) as usize;
            // 應用 Sobel 邊緣檢測
            if x > 0 && x < width - 1 && y > 0 && y < height - 1 {
                let gx = sobel_x(&pixels, width, x, y);
                let gy = sobel_y(&pixels, width, x, y);
                let mag = ((gx * gx + gy * gy) as f64).sqrt() as u8;
                result[idx] = mag;
                result[idx + 1] = mag;
                result[idx + 2] = mag;
            }
        }
    }

    Clamped(result)
}
```

## 7. 結語

瀏覽器中的 WASM 已經從「JavaScript 的加速器」進化為「GPU 應用的控制中樞」。結合 WebGPU 的硬體加速能力，WASM 正在重新定義瀏覽器應用的效能邊界。對於密集計算型應用，Rust + WASM + WebGPU 已成為瀏覽器開發的首選技術棧。

---

## 延伸閱讀

- [WebGPU W3C 規範](https://www.google.com/search?q=WebGPU+W3C+specification)
- [Rust + WebGPU 教學](https://www.google.com/search?q=Rust+WebGPU+tutorial)
- [wasm-bindgen WebGL 綁定](https://www.google.com/search?q=wasm-bindgen+WebGL)
- [Canvas 2D 高效能渲染](https://www.google.com/search?q=Canvas+2D+performance+optimization)
