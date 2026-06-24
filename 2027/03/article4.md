# wgpu 非同步編譯與資產管線

## 前言

在現代 3D 應用中，資產載入與著色器編譯的耗時可能遠超過渲染本身。wgpu 作為非同步友好的圖形 API，提供了非同步編譯、資產並行載入、以及漸進式串流等機制。本文將探討如何在 Rust 中建構高效的 wgpu 資產管線。

## 非同步著色器編譯

### 傳統同步載入的問題

許多 wgpu 教學使用 `include_str!("shader.wgsl")` 在編譯時將 WGSL 原始碼嵌入二進制，然後同步呼叫 `device.create_shader_module()`。這種方式在開發階段沒問題，但在生產環境中，著色器可能需要從網路載入或動態生成：

```rust
// 同步載入——阻塞主線程
let source = std::fs::read_to_string("shaders/particle.wgsl").unwrap();
let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
    label: Some("Particle Shader"),
    source: wgpu::ShaderSource::Wgsl(Cow::Owned(source)),
});
// 主線程在此阻塞等待檔案 I/O 和編譯
```

### Shader Module Descriptor 的非同步路徑

wgpu 的 `device.create_shader_module()` 本身是同步的，但編譯工作實際上在 GPU 驅動層平行進行。更有效的策略是將 I/O 與管線建立分離：

```rust
use std::sync::Arc;
use tokio::task::spawn_blocking;

#[derive(Clone)]
struct ShaderManager {
    device: Arc<wgpu::Device>,
    cache: Arc<dashmap::DashMap<String, wgpu::ShaderModule>>,
}

impl ShaderManager {
    async fn load_shader(&self, path: &str) -> wgpu::ShaderModule {
        // 先檢查快取
        if let Some(module) = self.cache.get(path) {
            return module.clone();
        }

        // 在 blocking threadpool 上讀取檔案
        let source = spawn_blocking({
            let path = path.to_string();
            move || std::fs::read_to_string(&path)
        }).await.unwrap().unwrap();

        // 在主線程建立 shader module
        let module = self.device.create_shader_module(
            wgpu::ShaderModuleDescriptor {
                label: Some(path),
                source: wgpu::ShaderSource::Wgsl(Cow::Owned(source)),
            }
        );

        self.cache.insert(path.to_string(), module.clone());
        module
    }

    fn compile_all(&self, sources: &[(&str, &str)]) -> Vec<wgpu::ShaderModule> {
        sources.iter().map(|(name, source)| {
            self.device.create_shader_module(wgpu::ShaderModuleDescriptor {
                label: Some(name),
                source: wgpu::ShaderSource::Wgsl(Cow::Owned(source.to_string())),
            })
        }).collect()
    }
}
```

### 管線編譯的惰性初始化

建立 `RenderPipeline` 時，驅動層會對著色器進行完整的編譯與最佳化。對於大型專案，可以將管線建立分散到多幀：

```rust
struct PipelineCompiler {
    device: Arc<wgpu::Device>,
    pending: Vec<PipelineTask>,
    maximum_per_frame: usize,
}

struct PipelineTask {
    label: String,
    vs_source: String,
    fs_source: String,
    layout: wgpu::PipelineLayout,
    format: wgpu::TextureFormat,
    result: Option<wgpu::RenderPipeline>,
}

impl PipelineCompiler {
    fn enqueue(&mut self, task: PipelineTask) {
        self.pending.push(task);
    }

    fn process_frame(&mut self) -> usize {
        let count = self.pending.len().min(self.maximum_per_frame);
        for task in self.pending.drain(..count) {
            let vs = self.device.create_shader_module(
                wgpu::ShaderModuleDescriptor {
                    label: Some(&format!("{} VS", task.label)),
                    source: wgpu::ShaderSource::Wgsl(Cow::Owned(task.vs_source)),
                }
            );
            let fs = self.device.create_shader_module(
                wgpu::ShaderModuleDescriptor {
                    label: Some(&format!("{} FS", task.label)),
                    source: wgpu::ShaderSource::Wgsl(Cow::Owned(task.fs_source)),
                }
            );

            let pipeline = self.device.create_render_pipeline(
                &wgpu::RenderPipelineDescriptor {
                    label: Some(&task.label),
                    layout: Some(&task.layout),
                    vertex: wgpu::VertexState {
                        module: &vs,
                        entry_point: "vs_main",
                        buffers: &[],
                    },
                    fragment: Some(wgpu::FragmentState {
                        module: &fs,
                        entry_point: "fs_main",
                        targets: &[Some(task.format.into())],
                    }),
                    ..Default::default()
                }
            );

            // 回呼通知管線就緒
            (task.callback)(pipeline);
        }
        count
    }
}
```

## 資產載入管線

### 多執行緒資產解碼

紋理和模型的解碼（如 JPEG/PNG 解壓、glTF 解析）應在背景執行緒進行，避免阻塞渲染主線程：

```rust
use tokio::task::spawn_blocking;

struct TextureAsset {
    pub view: wgpu::TextureView,
    pub extent: wgpu::Extent3d,
    pub format: wgpu::TextureFormat,
}

async fn load_texture_async(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    path: &str,
) -> TextureAsset {
    // 在背景執行緒讀取並解碼
    let decoded = spawn_blocking({
        let path = path.to_string();
        move || -> Result<(Vec<u8>, u32, u32), image::ImageError> {
            let img = image::open(&path)?;
            let rgba = img.to_rgba8();
            let (w, h) = rgba.dimensions();
            Ok((rgba.into_raw(), w, h))
        }
    }).await.unwrap().unwrap();

    let (data, width, height) = decoded;

    let texture_size = wgpu::Extent3d {
        width,
        height,
        depth_or_array_layers: 1,
    };

    let texture = device.create_texture(&wgpu::TextureDescriptor {
        label: Some(path),
        size: texture_size,
        mip_level_count: 1,
        sample_count: 1,
        dimension: wgpu::TextureDimension::D2,
        format: wgpu::TextureFormat::Rgba8UnormSrgb,
        usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
    });

    let view = texture.create_view(&wgpu::TextureViewDescriptor::default());

    queue.write_texture(
        wgpu::ImageCopyTexture {
            texture: &texture,
            mip_level: 0,
            origin: wgpu::Origin3d::ZERO,
            aspect: wgpu::TextureAspect::All,
        },
        &data,
        wgpu::ImageDataLayout {
            offset: 0,
            bytes_per_row: Some(4 * width),
            rows_per_image: Some(height),
        },
        texture_size,
    );

    TextureAsset { view, extent: texture_size, format: wgpu::TextureFormat::Rgba8UnormSrgb }
}
```

### 背景紋理解壓縮

對於 DXT/BC 壓縮紋理，解壓縮應在背景執行緒處理：

```rust
async fn load_compressed_texture(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    path: &str,
) -> TextureAsset {
    // 背景執行緒讀取並解析 DDS/KTX 檔案
    let compressed = spawn_blocking({
        let path = path.to_string();
        move || -> Vec<u8> {
            std::fs::read(&path).unwrap()
        }
    }).await.unwrap();

    // 解析 header（簡化範例，實務應使用 ktx2 或 dds crate）
    let (header, data) = compressed.split_at(128);
    let width = u32::from_le_bytes(header[..4].try_into().unwrap());
    let height = u32::from_le_bytes(header[4..8].try_into().unwrap());

    let texture = device.create_texture(&wgpu::TextureDescriptor {
        label: Some(path),
        size: wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
        mip_level_count: 1,
        sample_count: 1,
        dimension: wgpu::TextureDimension::D2,
        format: wgpu::TextureFormat::Bc1RgbaUnorm,  // BC1/DXT1
        usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
    });

    queue.write_texture(
        wgpu::ImageCopyTexture {
            texture: &texture,
            mip_level: 0,
            origin: wgpu::Origin3d::ZERO,
            aspect: wgpu::TextureAspect::All,
        },
        data,
        wgpu::ImageDataLayout {
            offset: 0,
            bytes_per_row: Some((width / 4) * 8), // BC1: 8 bytes per 4x4 block
            rows_per_image: Some(height / 4),
        },
        wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
    );

    let view = texture.create_view(&wgpu::TextureViewDescriptor::default());
    TextureAsset { view, extent: wgpu::Extent3d { width, height, depth_or_array_layers: 1 }, format: wgpu::TextureFormat::Bc1RgbaUnorm }
}
```

## 漸進式載入策略

### 優先級佇列

資產載入不應該是先到先服務（FIFO）。靠近攝影機的物件、UI 紋理、以及當前場景必需的資源應優先載入：

```rust
#[derive(PartialEq, Eq, PartialOrd, Ord)]
enum LoadPriority {
    Critical = 0,
    High = 1,
    Normal = 2,
    Low = 3,
    Background = 4,
}

struct AssetTask {
    priority: LoadPriority,
    path: String,
    asset_type: AssetType,
}

struct AsyncAssetLoader {
    device: Arc<wgpu::Device>,
    queue: Arc<wgpu::Queue>,
    task_queue: std::collections::BinaryHeap<AssetTask>,
    loading: Vec<AssetTask>,
    max_concurrent: usize,
}

impl AsyncAssetLoader {
    async fn process(&mut self) {
        // 按優先級取出任務
        while self.loading.len() < self.max_concurrent {
            if let Some(task) = self.task_queue.pop() {
                self.loading.push(task);
            } else {
                break;
            }
        }

        // 並行載入
        let mut handles = Vec::new();
        for task in self.loading.drain(..) {
            let device = self.device.clone();
            let queue = self.queue.clone();
            handles.push(tokio::spawn(async move {
                match task.asset_type {
                    AssetType::Texture => load_texture_async(&device, &queue, &task.path).await,
                    AssetType::Model => load_model_async(&device, &queue, &task.path).await,
                    AssetType::Shader => load_shader_async(&device, &task.path).await,
                }
            }));
        }

        for handle in handles {
            handle.await.unwrap();
        }
    }
}
```

### 串流載入（Streaming Loading）

對於大型場景，不可能等待所有資產載入完成才開始渲染。串流載入的核心思想是「先看到先載入」：

```rust
struct StreamingScene {
    loaded_chunks: HashSet<ChunkId>,
    visible_chunks: Vec<ChunkId>,
    loader: AsyncAssetLoader,
}

impl StreamingScene {
    fn update_visibility(&mut self, camera_pos: &Vec3) {
        // 根據攝影機位置計算可見 chunk
        let new_visible = self.compute_visible_chunks(camera_pos);

        // 對新出現的 chunk 發出載入請求
        for chunk in &new_visible {
            if !self.loaded_chunks.contains(chunk) {
                self.loader.enqueue(AssetTask {
                    priority: LoadPriority::High,
                    path: format!("chunks/{}_{}.bin", chunk.x, chunk.y),
                    asset_type: AssetType::Model,
                });
            }
        }

        // 對遠離的 chunk 排程卸載
        for chunk in &self.loaded_chunks {
            if !new_visible.contains(chunk) {
                self.loader.schedule_unload(chunk);
            }
        }

        self.visible_chunks = new_visible;
    }

    fn compute_visible_chunks(&self, camera_pos: &Vec3) -> Vec<ChunkId> {
        // 使用 frustum culling 計算可見範圍
        vec![]  // 簡化
    }
}
```

## 整合 Tokio 與 wgpu

### 共用執行時期

應用程式通常只需要一個 tokio runtime，wgpu 的 non-blocking 操作（如 `map_async`）與 tokio 配合良好：

```rust
#[tokio::main]
async fn main() {
    // 初始化 wgpu
    let instance = wgpu::Instance::new(wgpu::InstanceDescriptor::default());
    let adapter = instance.request_adapter(&wgpu::RequestAdapterOptions::default()).await.unwrap();
    let (device, queue) = adapter.request_device(&wgpu::DeviceDescriptor::default(), None).await.unwrap();

    let device = Arc::new(device);
    let queue = Arc::new(queue);

    // 在背景載入資產
    let loader = AsyncAssetLoader::new(device.clone(), queue.clone());

    // 載入必要資產（等待完成）
    let critical_texture = load_texture_async(&device, &queue, "textures/ui_background.png").await;

    // 其餘資產在背景載入
    tokio::spawn({
        let loader = loader.clone();
        async move {
            loader.load_all("assets/manifest.json").await;
        }
    });

    // 渲染循環
    loop {
        // 檢查已完成的非同步載入
        loader.process().await;

        // 渲染
        render_frame(&device, &queue, &surface, &config)?;
    }
}
```

### 非同步 Buffer Mapping 的整合

`map_async` 的非同步回呼可以與 tokio 的 oneshot channel 結合：

```rust
async fn read_buffer_async(
    device: &wgpu::Device,
    buffer: &wgpu::Buffer,
) -> Vec<u8> {
    let (tx, rx) = tokio::sync::oneshot::channel();

    let slice = buffer.slice(..);
    slice.map_async(wgpu::MapMode::Read, move |result| {
        let _ = tx.send(result);
    });
    device.poll(wgpu::Maintain::Wait);

    rx.await.unwrap().unwrap();

    let data = slice.get_mapped_range().to_vec();
    drop(data);
    buffer.unmap();

    data
}
```

這種模式讓 GPU 計算結果的讀回可以融入 tokio 的非同步流程，避免 busy waiting。

## 載入畫面與過渡

在資產載入期間，應顯示載入畫面或過渡動畫：

```rust
struct LoadingScreen {
    pipeline: wgpu::RenderPipeline,
    progress: f32,
}

impl LoadingScreen {
    fn render(&self, encoder: &mut wgpu::CommandEncoder, view: &wgpu::TextureView) {
        let mut rpass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
            label: Some("Loading Screen"),
            color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                view,
                resolve_target: None,
                ops: wgpu::Operations {
                    load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                    store: wgpu::StoreOp::Store,
                },
            })],
            depth_stencil_attachment: None,
        });

        rpass.set_pipeline(&self.pipeline);
        // 渲染進度條或動畫
    }
}

fn run_loading_loop(device: &wgpu::Device, queue: &wgpu::Queue, surface: &wgpu::Surface, config: &wgpu::SurfaceConfiguration) {
    let loading = LoadingScreen::new(device);
    let mut loaded = false;

    while !loaded {
        let output = surface.get_current_texture().unwrap();
        let view = output.texture.create_view(&wgpu::TextureViewDescriptor::default());

        let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor::default());
        loading.render(&mut encoder, &view);

        queue.submit(Some(encoder.finish()));
        output.present();

        // 檢查資產載入狀態
        loaded = check_loading_progress();
    }
}
```

## 總結

建構高效的 wgpu 資產管線需要從三個層面著手：非同步著色器編譯避免主線程阻塞、多執行緒資產解碼將 I/O 與計算密集工作移到背景、漸進式載入確保使用者無需等待所有資產就緒即可開始互動。

將這些機制與 tokio 的非同步執行時期整合，可以建立一個完全非阻塞的渲染管線。在大規模場景中，這種架構可以讓數 GB 的資產在背景載入，同時維持 60fps 的流暢渲染。

---

**參考資料**

- https://www.google.com/search?q=wgpu+async+shader+compilation
- https://www.google.com/search?q=wgpu+asset+loading+pipeline+tokio
- https://www.google.com/search?q=webgpu+progressive+loading+streaming
- https://www.google.com/search?q=wgpu+texture+decompression+background+thread
