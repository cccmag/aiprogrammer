# wgpu 核心 API 入門

## Instance、Adapter、Device、Queue、SwapChain、BindGroup（2019-2026）

### 前言

wgpu 的 API 設計遵循 WebGPU 規範的物件模型。與 OpenGL 的全域狀態機不同，wgpu 採用明確的資源所有權和層次化建立流程。理解這個流程是掌握 wgpu 的第一步。

### 四大核心物件

```
Instance（實例）
   ↓ 請求
Adapter（介面卡 — 代表一個 GPU 或軟體實作）
   ↓ 請求
Device（裝置 — GPU 資源的管理者）+ Queue（佇列 — 命令提交通道）
   ↓
Pipeline / Buffer / Texture / BindGroup（實際 GPU 資源）
```

**Instance** — GPU 存取的入口：

```rust
let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor {
    backends: wgpu::Backends::all(), // 自動選擇 Vulkan/Metal/DX12
    flags: wgpu::InstanceFlags::default(),
    ..Default::default()
});
```

`Instance` 也負責建立 Surface——連接到作業系統視窗的橋樑：

```rust
let surface = instance.create_surface(&window).unwrap();
```

**Adapter** — 代表一個實體 GPU：

```rust
let adapter = instance
    .request_adapter(&wgpu::RequestAdapterOptions {
        power_preference: wgpu::PowerPreference::HighPerformance,
        compatible_surface: Some(&surface),
        ..Default::default()
    })
    .await
    .unwrap();

// 查詢介面卡資訊
println!("Adapter: {:?}", adapter.get_info());
// 輸出範例: "AdapterInfo { name: \"Apple M3\", vendor: 0, device: 0, ... }"
```

**Device + Queue** — GPU 資源的控制中樞：

```rust
let (device, queue) = adapter
    .request_device(
        &wgpu::DeviceDescriptor {
            label: Some("main device"),
            required_features: wgpu::Features::empty(),
            required_limits: wgpu::Limits::default(),
            memory_hints: wgpu::MemoryHints::Performance,
        },
        None, // 追蹤回呼
    )
    .await
    .unwrap();
```

`Device` 負責建立所有 GPU 資源（管線、緩衝區、紋理、綁定組），而 `Queue` 用於將命令提交給 GPU：

```rust
// Device：建立資源
let buffer = device.create_buffer(&...);
let pipeline = device.create_render_pipeline(&...);
let texture = device.create_texture(&...);

// Queue：提交工作
queue.submit(Some(encoder.finish()));
```

### 交換鏈與幀緩衝

交換鏈是雙緩衝（或三緩衝）機制的核心——它讓 GPU 在渲染一個幀的同時，顯示器顯示另一個幀：

```rust
// 設定交換鏈
let caps = surface.get_capabilities(&adapter);
let format = caps.formats[0];

let config = wgpu::SurfaceConfiguration {
    usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
    format,
    width: size.width,
    height: size.height,
    present_mode: wgpu::PresentMode::Fifo, // 垂直同步
    alpha_mode: caps.alpha_modes[0],
    view_formats: vec![],
    desired_maximum_frame_latency: 2,
};
surface.configure(&device, &config);

// 每一幀的流程
fn render_frame(device: &wgpu::Device, queue: &wgpu::Queue, surface: &wgpu::Surface) {
    // 1. 取得當前可用的幀緩衝
    let frame = surface.get_current_texture().expect("Failed to acquire frame");
    
    // 2. 建立幀緩衝的檢視（View）
    let view = frame.texture.create_view(&wgpu::TextureViewDescriptor::default());
    
    // ... 在此渲染到 view ...
    
    // 3. 顯示結果
    frame.present();
}
```

`PresentMode` 的選擇影響效能和功耗：

| 模式 | 行為 | 適用場景 |
|------|------|---------|
| `Fifo` | 佇列先入先出，垂直同步 | 預設，最省電 |
| `Mailbox` | 永遠使用最新幀，垂直同步 | 遊戲（低延遲） |
| `Immediate` | 立即顯示，不等待垂直同步 | 最快但可能畫面撕裂 |
| `AutoVsync` | 自動選擇（2024 新增） | 通用 |

### 綁定組與佈局

BindGroup 是 wgpu 中最具設計巧思的概念之一。它相當於 Vulkan 的 Descriptor Set——將著色器需要的資源（緩衝區、紋理、取樣器）打包成一個不可變的組。

```rust
// 第一步：定義 BindGroup 的佈局
let bind_group_layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
    label: Some("camera layout"),
    entries: &[
        wgpu::BindGroupLayoutEntry {
            binding: 0,
            visibility: wgpu::ShaderStages::VERTEX | wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Uniform,
                has_dynamic_offset: false,
                min_binding_size: None,
            },
            count: None,
        },
        wgpu::BindGroupLayoutEntry {
            binding: 1,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Texture {
                sample_type: wgpu::TextureSampleType::Float { filterable: true },
                view_dimension: wgpu::TextureViewDimension::D2,
                multisampled: false,
            },
            count: None,
        },
    ],
});

// 第二步：建立實際的 BindGroup
let bind_group = device.create_bind_group(&wgpu::BindGroupDescriptor {
    layout: &bind_group_layout,
    entries: &[
        wgpu::BindGroupEntry {
            binding: 0,
            resource: wgpu::BindingResource::Buffer(camera_buffer.as_entire_buffer_binding()),
        },
        wgpu::BindGroupEntry {
            binding: 1,
            resource: wgpu::BindingResource::TextureView(&texture_view),
        },
    ],
});
```

在著色器中透過 `@group(N)` 和 `@binding(M)` 存取：

```wgsl
@group(0) @binding(0) var<uniform> camera: CameraUniform;
@group(0) @binding(1) var texture: texture_2d<f32>;
```

### 命令緩衝區與編碼器

命令編碼器是 wgpu 高效能的關鍵——它讓開發者可以在 CPU 端預先記錄渲染命令，然後一次性提交：

```rust
// 建立命令編碼器
let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
    label: Some("main encoder"),
});

// 記錄渲染 Pass
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
        depth_stencil_attachment: None,
        ..Default::default()
    });
    rpass.set_pipeline(&pipeline);
    rpass.set_bind_group(0, &bind_group, &[]);
    rpass.set_vertex_buffer(0, vertex_buffer.slice(..));
    rpass.set_index_buffer(index_buffer.slice(..), wgpu::IndexFormat::Uint32);
    rpass.draw_indexed(0..num_indices, 0, 0..1);
}

// 可以記錄多個 Pass（相同或不同編碼器）
{
    let mut cpass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
        label: Some("compute pass"),
    });
    cpass.set_pipeline(&compute_pipeline);
    cpass.set_bind_group(0, &compute_bind_group, &[]);
    cpass.dispatch_workgroups(64, 64, 1);
}

// 一次性提交所有命令
queue.submit(Some(encoder.finish()));
```

這種設計允許開發者將多個渲染 Pass 和計算 Pass 串聯在同一個命令緩衝區中，減少了 CPU-GPU 之間的同步次數。

### 資源生命週期管理

wgpu 使用 Rust 的所有權模型管理 GPU 資源——當資源被 drop 時，其對應的 GPU 記憶體也會被釋放。不需要手動的 `vkDestroyBuffer` 或 `glDeleteTextures`：

```rust
{
    let temp_buffer = device.create_buffer(&...);
    // 使用 temp_buffer
} // temp_buffer 離開作用域，GPU 緩衝區自動釋放
```

### 小結

wgpu 的四層架構（Instance → Adapter → Device/Queue → 資源）提供了清晰的資源管理層次。BindGroup 的設計消除了執行期綁定錯誤，而命令編碼器讓 CPU 端的記錄和 GPU 端的執行有效分離。掌握這些核心概念後，建立複雜的渲染管線就只是組合這些元件的問題了。

---

**下一步**：[著色器程式設計：WGSL](focus4.md)

## 延伸閱讀

- [wgpu 官方文件](https://www.google.com/search?q=wgpu+rust+documentation)
- [Learn WGPU 教學](https://www.google.com/search?q=learn+wgpu+tutorial+rust)
- [WebGPU API 中文指南](https://www.google.com/search?q=WebGPU+API+cookbook)
