# 程式實作：wgpu 三角形渲染器

## 簡介

本實作示範如何使用 wgpu 在 Rust 中建立一個完整的 GPU 渲染管線，從實例建立到螢幕上繪製三角形。完整程式碼在 `_code/src/main.rs`。

## 核心步驟

### 1. 建立 Instance

`wgpu::Instance` 是 GPU 存取的入口點：

```rust
let instance = wgpu::Instance::new(wgpu::InstanceDescriptor {
    backends: wgpu::Backends::all(),
    ..Default::default()
});
```

`Backends::all()` 會自動選擇 Vulkan (Linux/Windows)、Metal (macOS) 或 DX12 (Windows)。

### 2. 請求 Adapter

Adapter 代表一個實體 GPU 或軟體實作：

```rust
let adapter = instance
    .request_adapter(&wgpu::RequestAdapterOptions {
        power_preference: wgpu::PowerPreference::HighPerformance,
        compatible_surface: Some(&surface),
        ..Default::default()
    })
    .await
    .unwrap();
```

### 3. 建立 Device 與 Queue

Device 是 GPU 資源的主要控制介面，Queue 用於提交命令：

```rust
let (device, queue) = adapter
    .request_device(&wgpu::DeviceDescriptor {
        required_features: wgpu::Features::empty(),
        required_limits: wgpu::Limits::default(),
        label: None,
        memory_hints: wgpu::MemoryHints::Performance,
    }, None)
    .await
    .unwrap();
```

### 4. 設定 Surface 與交換鏈

Surface 將 GPU 輸出連接到視窗：

```rust
let config = wgpu::SurfaceConfiguration {
    usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
    format,
    width: size.width,
    height: size.height,
    present_mode: wgpu::PresentMode::Fifo,
    alpha_mode: surface_caps.alpha_modes[0],
    view_formats: vec![],
    desired_maximum_frame_latency: 2,
};
surface.configure(&device, &config);
```

### 5. 建立著色器模組

WGSL 原始碼編譯為著色器模組：

```rust
let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
    label: Some("triangle shader"),
    source: wgpu::ShaderSource::Wgsl(SHADER_SRC.into()),
});
```

### 6. 建立渲染管線

渲染管線將著色器與狀態結合：

```rust
let pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
    label: Some("triangle pipeline"),
    layout: None,
    vertex: wgpu::VertexState {
        module: &shader,
        entry_point: "vs_main",
        buffers: &[],  // 無頂點緩衝區（使用內建位置）
        compilation_options: Default::default(),
    },
    fragment: Some(wgpu::FragmentState { ... }),
    primitive: wgpu::PrimitiveState {
        topology: wgpu::PrimitiveTopology::TriangleList,
        cull_mode: Some(wgpu::Face::Back),
        ..Default::default()
    },
    ..Default::default()
});
```

### 7. 渲染迴圈

每一幀：
1. 取得當前幀緩衝（`get_current_texture`）
2. 建立命令編碼器
3. 開始渲染 pass，設定管線，繪製
4. 提交命令，顯示結果

```rust
fn render(&mut self) {
    let frame = self.surface.get_current_texture().unwrap();
    let view = frame.texture.create_view(&Default::default());
    let mut encoder = self.device.create_command_encoder(&Default::default());
    {
        let mut rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
            color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                view: &view,
                ops: wgpu::Operations {
                    load: wgpu::LoadOp::Clear(wgpu::Color {
                        r: 0.05, g: 0.05, b: 0.1, a: 1.0,
                    }),
                    store: wgpu::StoreOp::Store,
                },
                ..Default::default()
            })],
            ..Default::default()
        });
        rpass.set_pipeline(&self.pipeline);
        rpass.draw(0..3, 0..1);  // 3 個頂點
    }
    self.queue.submit(Some(encoder.finish()));
    frame.present();
}
```

## WGSL 著色器

### 頂點著色器

```wgsl
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    let pos = array<vec2<f32>, 3>(
        vec2( 0.0,  0.8),  // 頂點 0：上方
        vec2(-0.7, -0.5),  // 頂點 1：左下
        vec2( 0.7, -0.5),  // 頂點 2：右下
    );
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
```

### 片段著色器

```wgsl
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.2, 0.6, 0.9, 1.0);  // 淡藍色
}
```

## 執行方式

```bash
cd _code
cargo build
cargo run    # 開啟視窗顯示藍色三角形
```

## 延伸練習

1. **加入頂點緩衝區**：使用 `VertexBuffer` 代替硬編碼位置
2. **加入 uniform**：透過 BindGroup 傳入變換矩陣
3. **加入索引緩衝區**：使用 `IndexBuffer` 繪製更複雜的幾何
4. **動畫**：每幀更新 uniform 中的旋轉矩陣
5. **多重三角形**：使用 instances draw 繪製多個物體
