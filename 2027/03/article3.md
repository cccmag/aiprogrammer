# 從 WebGL 遷移到 WebGPU：逐步指南

## 前言

WebGPU 作為 WebGL 的下一代替代者，不僅帶來了更低的 API 開銷和更高效能，更重要的是從根本上改變了開發者與 GPU 互動的心智模型。WebGL 基於 OpenGL ES 的即時狀態機設計，而 WebGPU 借鑑了 Vulkan、Metal、DirectX 12 的現代顯式 API 設計哲學。本文將協助擁有 WebGL 經驗的開發者順利遷移到 WebGPU。

## 心智模型的核心差異

### 狀態機 vs. 資源物件

WebGL 的本質是一個巨大的狀態機。`gl.enable(GL_DEPTH_TEST)`、`gl.blendFunc(...)`、`gl.bindBuffer(...)` 等呼叫逐一修改全域狀態，繪製命令的結果取決於當前所有狀態的組合。這種設計雖然靈活，但在多執行緒場景下不安全，且驅動層需要推測開發者的意圖，增加了開銷。

WebGPU 則採用**資源物件**模型。管線狀態（`RenderPipeline`）、資源綁定（`BindGroup`）、命令編碼（`CommandEncoder`）都是獨立的不可變物件。繪製前需要明確組合這些物件：

```rust
// WebGL 的狀態機模式
gl.useProgram(program);
gl.bindBuffer(GL_ARRAY_BUFFER, vbo);
gl.vertexAttribPointer(0, 3, GL_FLOAT, false, 0, 0);
gl.enableVertexAttribArray(0);
gl.uniformMatrix4fv(u_modelLoc, false, model);
gl.drawArrays(GL_TRIANGLES, 0, 36);

// WebGPU 的資源物件模式
render_pass.set_pipeline(&pipeline);
render_pass.set_vertex_buffer(0, vertex_buffer.slice(..));
render_pass.set_bind_group(0, &bind_group, &[]);
render_pass.draw(0..36, 0..1);
```

### 全域綁定 vs. Bind Group

WebGL 中，uniform、texture、buffer 等資源透過全域綁定點設定，且綁定點在不同著色器之間可能衝突：

```javascript
// WebGL：全域綁定容易衝突
gl.activeTexture(gl.TEXTURE0);
gl.bindTexture(gl.TEXTURE_2D, diffuseMap);
gl.uniform1i(u_diffuseLoc, 0);

gl.activeTexture(gl.TEXTURE1);
gl.bindTexture(gl.TEXTURE_2D, specularMap);
gl.uniform1i(u_specularLoc, 1);
```

WebGPU 使用 `BindGroup` 將相關資源打包成一組，一次性綁定：

```rust
let bind_group = device.create_bind_group(&wgpu::BindGroupDescriptor {
    label: Some("Material Bind Group"),
    layout: &bind_group_layout,
    entries: &[
        wgpu::BindGroupEntry { binding: 0, resource: wgpu::BindingResource::TextureView(&diffuse_view) },
        wgpu::BindGroupEntry { binding: 1, resource: wgpu::BindingResource::TextureView(&specular_view) },
        wgpu::BindGroupEntry { binding: 2, resource: wgpu::BindingResource::Sampler(&sampler) },
    ],
});

render_pass.set_bind_group(0, &bind_group, &[]);
```

這種設計確保資源綁定是型別安全的，且驅動層可以提前知道完整的資源組合，進行最佳化。

### 即時編譯 vs. 預先編譯

WebGL 在 `gl.compileShader()` 時編譯 GLSL，`gl.linkProgram()` 時連結。編譯失敗在運行時才暴露。

WebGPU 的著色器編譯在 `create_shader_module()` 時進行，而管線驗證在 `create_render_pipeline()` 時完成。錯誤訊息更加詳細，且可以非同步編譯。

## GLSL 到 WGSL 的轉換

### 資料型別對應

| GLSL | WGSL | 說明 |
|------|------|------|
| `float` | `f32` | 32 位元浮點數 |
| `vec2` | `vec2<f32>` | 2 分量向量 |
| `vec4` | `vec4<f32>` | 4 分量向量 |
| `mat4` | `mat4x4<f32>` | 4x4 矩陣 |
| `sampler2D` | `sampler` + `texture_2d<f32>` | 分開為取樣器與紋理型別 |
| `int` | `i32` | 32 位元整數 |
| `uint` | `u32` | 32 位元無號整數 |

### 變數修飾詞轉換

| GLSL | WGSL | 說明 |
|------|------|------|
| `uniform` | `var<uniform>` | 統一緩衝區 |
| `attribute` / `in` | `@location(n)` | 頂點輸入 |
| `varying` / `out` | `@location(n)` / `@builtin(...)` | 頂點輸出 / 片段輸入 |
| `layout(location=0) out` | `@location(0)` | 片段輸出 |

### 範例：簡單的頂點著色器

GLSL 寫法：

```glsl
#version 300 es
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_uv;

uniform mat4 u_modelViewProj;

out vec2 v_uv;

void main() {
    v_uv = a_uv;
    gl_Position = u_modelViewProj * vec4(a_position, 1.0);
}
```

對應的 WGSL：

```wgsl
struct Uniforms {
    model_view_proj: mat4x4<f32>,
}

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(
    @location(0) a_position: vec3<f32>,
    @location(1) a_uv: vec2<f32>,
) -> VertexOutput {
    var out: VertexOutput;
    out.uv = a_uv;
    out.position = uniforms.model_view_proj * vec4<f32>(a_position, 1.0);
    return out;
}
```

### 範例：片段著色器

GLSL 寫法：

```glsl
#version 300 es
precision highp float;

in vec2 v_uv;
uniform sampler2D u_diffuse;

layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(u_diffuse, v_uv);
}
```

對應的 WGSL：

```wgsl
@group(0) @binding(1) var diffuse_texture: texture_2d<f32>;
@group(0) @binding(2) var diffuse_sampler: sampler;

@fragment
fn fs_main(@location(0) v_uv: vec2<f32>) -> @location(0) vec4<f32> {
    return textureSample(diffuse_texture, diffuse_sampler, v_uv);
}
```

WGSL 將取樣器與紋理分開宣告，這是與 GLSL 的重要差異。這種分離允許驅動層更靈活地管理紋理快取。

## 渲染管線的建立

### WebGL 的 Program 建立

```javascript
const vs = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vs, vsSource);
gl.compileShader(vs);

const fs = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(fs, fsSource);
gl.compileShader(fs);

const program = gl.createProgram();
gl.attachShader(program, vs);
gl.attachShader(program, fs);
gl.linkProgram(program);
gl.useProgram(program);
```

### WebGPU 的 Pipeline 建立

```rust
let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
    label: Some("Shader"),
    source: wgpu::ShaderSource::Wgsl(Cow::Borrowed(include_str!("shader.wgsl"))),
});

let pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
    label: Some("Main Pipeline"),
    layout: Some(&pipeline_layout),
    vertex: wgpu::VertexState {
        module: &shader,
        entry_point: "vs_main",
        buffers: &[vertex_buffer_layout],
    },
    fragment: Some(wgpu::FragmentState {
        module: &shader,
        entry_point: "fs_main",
        targets: &[Some(swapchain_format.into())],
    }),
    primitive: wgpu::PrimitiveState {
        topology: wgpu::PrimitiveTopology::TriangleList,
        front_face: wgpu::FrontFace::Ccw,
        cull_mode: Some(wgpu::Face::Back),
        ..Default::default()
    },
    depth_stencil: Some(wgpu::DepthStencilState {
        format: wgpu::TextureFormat::Depth32Float,
        depth_write_enabled: true,
        depth_compare: wgpu::CompareFunction::Less,
        stencil: Default::default(),
    }),
    multisample: wgpu::MultisampleState::default(),
});
```

WebGPU 的管線描述必須在建立時提供所有狀態（拓撲、面剔除、深度測試等），而 WebGL 的這些狀態是透過獨立的 API 呼叫設定的。

## Frame Buffer Object 到 Texture View

WebGL 的 FBO：

```javascript
const fb = gl.createFramebuffer();
gl.bindFramebuffer(GL_FRAMEBUFFER, fb);
gl.framebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, colorTex, 0);
```

WebGPU 的 Render Pass：

```rust
let color_view = texture.create_view(&wgpu::TextureViewDescriptor::default());

let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor::default());
let rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
    label: Some("Offscreen Render Pass"),
    color_attachments: &[Some(wgpu::RenderPassColorAttachment {
        view: &color_view,
        resolve_target: None,
        ops: wgpu::Operations {
            load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
            store: wgpu::StoreOp::Store,
        },
    })],
    depth_stencil_attachment: None,
});
```

WebGPU 將渲染目標的概念整合到 `RenderPassDescriptor` 中，每個 `color_attachment` 對應一個 `TextureView`。Load/Store operations 明確指定每個 pass 開始和結束時的行為。

## 遷移檢查清單

### 初始化階段

| 項目 | WebGL | WebGPU |
|------|-------|--------|
| Canvas 取得 | `canvas.getContext('webgl2')` | `canvas.getContext('webgpu')` |
| 裝置取得 | 隱含 | `navigator.gpu.requestAdapter()` → `adapter.requestDevice()` |
| Swap Chain | 由 canvas 管理 | 需建立 `Surface` 和 `SurfaceConfiguration` |
| 著色器語言 | GLSL ES 3.0 | WGSL |
| 資源管理 | 隱含 GC | 明確的 RAII 或 destroy() |

### 資源創建

| 資源 | WebGL | WebGPU |
|------|-------|--------|
| 頂點 Buffer | `gl.createBuffer()` + `gl.bufferData()` | `device.createBufferInit()` |
| 紋理 | `gl.createTexture()` + `gl.texImage2D()` | `device.createTexture()` + `queue.writeTexture()` |
| Sampler | `gl.texParameteri()` 設定紋理參數 | `device.createSampler()` 獨立物件 |
| Uniform | `gl.uniform*()` 逐個設定 | Uniform Buffer + Bind Group |

### 渲染循環

| 項目 | WebGL | WebGPU |
|------|-------|--------|
| 清除畫面 | `gl.clear(COLOR_BUFFER_BIT)` | `LoadOp::Clear` 在 RenderPass 層級 |
| 繪製呼叫 | `gl.drawArrays()` / `gl.drawElements()` | `render_pass.draw()` |
| 狀態管理 | 逐個 API 呼叫修改 | Pipeline 物件一次性設定 |
| 資源綁定 | 全域綁定點 | Bind Group 物件 |

### 偵錯工具

| 工具 | 用途 |
|------|------|
| `wgpu::Backends::all()` | 啟用所有後端以捕獲跨平台問題 |
| `device.push_error_scope()` | 類似 WebGL 的 `getError()` 但更精確 |
| `wgpu::Dx12Compiler::Dxc` | Windows 上使用 DXC 編譯器獲得更好錯誤訊息 |
| Chrome `about://gpu` | 查看 WebGPU 裝置資訊與功能限制 |

## 效能展望

WebGPU 在典型 3D 渲染場景中比 WebGL 2.0 有 20-50% 的效能提升，主要原因包括：

1. **減少驅動開銷**：Pipeline State Object (PSO) 快取管線編譯結果，避免重複驗證。
2. **更低的 CPU 負擔**：Command buffer 的批次提交減少 CPU-GPU 通訊次數。
3. **更佳的記憶體管理**：顯式資源生命週期減少驅動推測開銷。

## 總結

從 WebGL 遷移到 WebGPU 不僅是 API 的替換，更是對 GPU 程式設計思維的升級。WebGL 的狀態機模型雖然入門簡單，但在複雜場景下難以預測與最佳化。WebGPU 的顯式資源模型雖需要更多初始化程式碼，但帶來了更好的效能、更清晰的生命週期管理、以及跨平台的一致性。

建議遷移時採用漸進策略：先將著色器翻譯為 WGSL，然後逐一取代資源建立與綁定邏輯，最後重構渲染循環。保留 WebGL 實作作為對照組，在遷移過程中持續驗證渲染結果的一致性。

---

**參考資料**

- https://www.google.com/search?q=WebGL+to+WebGPU+migration+guide
- https://www.google.com/search?q=GLSL+to+WGSL+translation+cheat+sheet
- https://www.google.com/search?q=WebGPU+bind+group+vs+WebGL+uniform
- https://www.google.com/search?q=WebGPU+performance+vs+WebGL+benchmark
