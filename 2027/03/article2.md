# 計算著色器實戰：GPU 粒子系統

## 前言

粒子系統是 GPU 通用計算（GPGPU）的經典入門案例。透過計算著色器（compute shader），我們可以將數十萬個粒子的位置更新完全交由 GPU 處理，避免 CPU-GPU 之間的資料傳輸瓶頸。本文將帶領讀者從零開始，在 wgpu 中實作一個完整的 GPU 粒子系統。

## WGSL 計算著色器基礎

WebGPU Shading Language (WGSL) 是 wgpu 的原生著色器語言。與 GLSL 或 HLSL 不同，WGSL 的語法借鑑了 Rust 的型別系統與安全性設計。

### 計算著色器的結構

一個最簡單的計算著色器如下：

```wgsl
@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;

struct Particle {
    position: vec4<f32>,
    velocity: vec4<f32>,
    lifetime: f32,
    _pad: f32,
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let i = id.x;
    if (i >= arrayLength(&particles)) {
        return;
    }

    let dt = 0.016;  // 約 60fps 的幀時間
    particles[i].position += particles[i].velocity * dt;
    particles[i].lifetime -= dt;

    if (particles[i].lifetime <= 0.0) {
        // 重置粒子
        particles[i].position = vec4<f32>(0.0, 0.0, 0.0, 1.0);
        particles[i].velocity = vec4<f32>(
            (f32(id.x % 100u) - 50.0) * 0.1,
            f32(id.x / 100u) * 0.1 - 5.0,
            0.0, 0.0
        );
        particles[i].lifetime = 1.0 + f32(id.x % 60u) * 0.1;
    }
}
```

關鍵點說明：

- `@workgroup_size(64)` 定義每個工作群組包含 64 個執行緒。總執行緒數 = workgroup 數量 x workgroup size。
- `@builtin(global_invocation_id)` 提供全域唯一的執行緒 ID，用來索引粒子陣列。
- `var<storage, read_write>` 宣告可讀寫的 storage buffer。

## Storage Buffer 的 Rust 端設定

在 Rust 中，我們需要建立對應的 storage buffer 並將其綁定到計算管線：

```rust
#[repr(C)]
#[derive(Copy, Clone, bytemuck::Pod, bytemuck::Zeroable)]
struct Particle {
    position: [f32; 4],
    velocity: [f32; 4],
    lifetime: f32,
    _pad: f32,
}

const PARTICLE_COUNT: u32 = 262_144;  // 2^18 個粒子

fn create_particle_buffer(device: &wgpu::Device) -> wgpu::Buffer {
    let initial_particles: Vec<Particle> = (0..PARTICLE_COUNT)
        .map(|i| Particle {
            position: [0.0, 0.0, 0.0, 1.0],
            velocity: [
                (i as f32 % 100.0 - 50.0) * 0.1,
                (i as f32 / 100.0) * 0.1 - 5.0,
                0.0,
                0.0,
            ],
            lifetime: 1.0 + (i as f32 % 60.0) * 0.1,
            _pad: 0.0,
        })
        .collect();

    device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("Particle Buffer"),
        contents: bytemuck::cast_slice(&initial_particles),
        usage: wgpu::BufferUsages::STORAGE
            | wgpu::BufferUsages::COPY_DST
            | wgpu::BufferUsages::COPY_SRC,
    })
}
```

`COPY_SRC` 是選用的，用於將粒子資料讀回 CPU 進行除錯。

## 計算管線的建立

計算管線與渲染管線的建立流程類似，但不需要 rasterizer state、depth stencil 等設定：

```rust
fn create_compute_pipeline(
    device: &wgpu::Device,
    shader_module: &wgpu::ShaderModule,
) -> wgpu::ComputePipeline {
    let bind_group_layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some("Particle Bind Group Layout"),
        entries: &[wgpu::BindGroupLayoutEntry {
            binding: 0,
            visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: false },
                has_dynamic_offset: false,
                min_binding_size: None,
            },
            count: None,
        }],
    });

    let pipeline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some("Compute Pipeline Layout"),
        bind_group_layouts: &[&bind_group_layout],
        push_constant_ranges: &[],
    });

    device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("Particle Compute Pipeline"),
        layout: Some(&pipeline_layout),
        module: shader_module,
        entry_point: "main",
    })
}
```

Bind group layout 宣告了著色器中 `@group(0) @binding(0)` 對應的資源——這是一個可讀寫的 storage buffer。

## 幀更新循環中的計算派遣

每幀中，我們需要先執行計算管線更新粒子位置，再執行渲染管線繪製粒子：

```rust
fn update_particles(
    encoder: &mut wgpu::CommandEncoder,
    compute_pipeline: &wgpu::ComputePipeline,
    bind_group: &wgpu::BindGroup,
    particle_count: u32,
) {
    let mut cpass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
        label: Some("Particle Compute Pass"),
    });
    cpass.set_pipeline(compute_pipeline);
    cpass.set_bind_group(0, bind_group, &[]);
    // 計算需要的 workgroup 數量：ceil(particle_count / workgroup_size)
    let workgroup_count = (particle_count + 63) / 64;
    cpass.dispatch_workgroups(workgroup_count, 1, 1);
}
```

`dispatch_workgroups` 的三個參數分別對應 X、Y、Z 方向的 workgroup 數量。對於一維粒子陣列，只需設定 X 維度。

## 渲染管線的整合

計算完粒子位置後，我們需要將粒子渲染到螢幕上。最簡單的方式是使用點精靈（point sprite）渲染：

```rust
fn create_render_pipeline(
    device: &wgpu::Device,
    swapchain_format: wgpu::TextureFormat,
    particle_shader: &wgpu::ShaderModule,
) -> wgpu::RenderPipeline {
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some("Render Pipeline Layout"),
        bind_group_layouts: &[],
        push_constant_ranges: &[],
    });

    device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
        label: Some("Particle Render Pipeline"),
        layout: Some(&layout),
        vertex: wgpu::VertexState {
            module: particle_shader,
            entry_point: "vs_main",
            buffers: &[wgpu::VertexBufferLayout {
                array_stride: std::mem::size_of::<Particle>() as u64,
                step_mode: wgpu::VertexStepMode::Instance,
                attributes: &[
                    wgpu::VertexAttribute {
                        format: wgpu::VertexFormat::Float32x4,
                        offset: 0,
                        shader_location: 0,
                    },
                ],
            }],
        },
        fragment: Some(wgpu::FragmentState {
            module: particle_shader,
            entry_point: "fs_main",
            targets: &[Some(swapchain_format.into())],
        }),
        primitive: wgpu::PrimitiveState {
            topology: wgpu::PrimitiveTopology::PointList,
            ..Default::default()
        },
        ..Default::default()
    })
}
```

關鍵在於 `VertexStepMode::Instance`——粒子 buffer 被視為 instance 資料，每個粒子對應一個 instance。繪製時使用 `draw(1, PARTICLE_COUNT, 0, 0)`，表示繪製 1 個頂點、PARTICLE_COUNT 個 instance。

頂點著色器從 instance 資料中讀取粒子位置：

```wgsl
struct Particle {
    position: vec4<f32>,
}

@vertex
fn vs_main(@location(0) position: vec4<f32>) -> @builtin(position) vec4<f32> {
    return position;
}

@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(1.0, 1.0, 1.0, 1.0);
}
```

## 完整幀循環

整合計算與渲染的完整幀循環如下：

```rust
fn render_frame(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    swapchain: &wgpu::Surface,
    config: &wgpu::SurfaceConfiguration,
    compute_pipeline: &wgpu::ComputePipeline,
    render_pipeline: &wgpu::RenderPipeline,
    particle_buffer: &wgpu::Buffer,
    compute_bind_group: &wgpu::BindGroup,
) -> Result<(), wgpu::SurfaceError> {
    let output = swapchain.get_current_texture()?;
    let view = output.texture.create_view(&wgpu::TextureViewDescriptor::default());

    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
        label: Some("Frame Encoder"),
    });

    // 1. 計算階段：更新粒子
    {
        let mut cpass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor::default());
        cpass.set_pipeline(compute_pipeline);
        cpass.set_bind_group(0, compute_bind_group, &[]);
        cpass.dispatch_workgroups((PARTICLE_COUNT + 63) / 64, 1, 1);
    }

    // 2. 渲染階段：繪製粒子
    {
        let mut rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
            label: Some("Particle Render Pass"),
            color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                view: &view,
                resolve_target: None,
                ops: wgpu::Operations {
                    load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                    store: wgpu::StoreOp::Store,
                },
            })],
            depth_stencil_attachment: None,
        });
        rpass.set_pipeline(render_pipeline);
        rpass.set_vertex_buffer(0, particle_buffer.slice(..));
        rpass.draw(1..PARTICLE_COUNT, 0..1);
    }

    queue.submit(Some(encoder.finish()));
    output.present();

    Ok(())
}
```

## 進階技巧

### 多個 Storage Buffer

複雜的粒子系統可能需要多個 buffer 分別儲存不同屬性。例如將位置、顏色、大小分離到不同的 buffer，以提升記憶體存取效率：

```wgsl
@group(0) @binding(0) var<storage, read_write> positions: array<vec4<f32>>;
@group(0) @binding(1) var<storage, read_write> velocities: array<vec4<f32>>;
@group(0) @binding(2) var<storage, read_write> lifetimes: array<f32>;
```

Rust 端需要對應多個 `BindGroupLayoutEntry`。

### 使用共享記憶體（Workgroup Shared Memory）

粒子間有交互作用時（如流體模擬），需要利用 `workgroup` 共享記憶體減少全域記憶體存取：

```wgsl
var<workgroup> shared_pos: array<vec4<f32>, 256>;

@compute @workgroup_size(256)
fn main(@builtin(global_invocation_id) gid: vec3<u32>,
        @builtin(local_invocation_id) lid: vec3<u32>) {
    shared_pos[lid.x] = positions[gid.x];
    workgroupBarrier();
    // 從 shared_pos 讀取鄰居粒子資料
    let neighbor = shared_pos[(lid.x + 1) % 256];
    // ...
    positions[gid.x] = shared_pos[lid.x];
}
```

`workgroupBarrier()` 確保所有執行緒完成寫入後才能開始讀取。

### 幀間一致性與 Double Buffering

為了避免 GPU 讀寫衝突，在計算與渲染分離的場景中，最好使用雙 buffer 輪換：

```rust
let particle_buffers: [wgpu::Buffer; 2] = [create_buffer(&device), create_buffer(&device)];
let mut read_idx = 0;
let mut write_idx = 1;

// 每幀交換
fn update(encoder, &particle_buffers[write_idx], &particle_buffers[read_idx]);
std::mem::swap(&mut read_idx, &mut write_idx);
```

著色器中讀取 `read` buffer、寫入 `write` buffer，渲染時讀取 `write` buffer。

## 效能考量

- **Workgroup size**：64-256 是主流 GPU 的最佳範圍。太小不足以隱藏記憶體延遲；太大可能導致 register pressure。
- **Buffer 大小**：每個粒子 36 bytes（3 個 vec4 + lifetime），262,144 個粒子約 9 MB。在主流 GPU 上可以輕鬆支援數百萬粒子。
- **GPU 與 CPU 同步**：避免每幀將粒子資料讀回 CPU。如需讀回，使用獨立的 `MAP_READ` buffer 並隔離幀查詢。

## 總結

計算著色器讓 GPU 粒子系統變得優雅而高效。透過 wgpu 的 storage buffer 機制，我們可以在計算管線中更新粒子狀態，然後直接在同一個 command buffer 中渲染，實現完全的 GPU 駐留處理。這種模式不僅適用於粒子系統，還擴展到物理模擬、布料模擬、流體力學等眾多 GPGPU 應用。

下一步，讀者可以嘗試加入碰撞檢測、顏色漸變、紋理點精靈等效果，打造完整的視覺特效系統。

---

**參考資料**

- https://www.google.com/search?q=wgpu+compute+shader+tutorial
- https://www.google.com/search?q=WGSL+storage+buffer+read_write
- https://www.google.com/search?q=GPU+particle+system+compute+shader
- https://www.google.com/search?q=wgpu+dispatch+workgroups
