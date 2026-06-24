# 跨後端開發：在 Vulkan、Metal、DX12 上測試 wgpu

## 前言

wgpu 最大的價值在於其跨平台抽象——同一份 Rust 程式碼可以無縫運行在 Vulkan（Linux/Windows/Android）、Metal（macOS/iOS）、DirectX 12（Windows）以及瀏覽器的 WebGPU 實現上。然而，每個後端都有其獨特的限制與行為差異。本文將探討如何編寫真正的跨後端 wgpu 應用程式，並提供測試與除錯策略。

## wgpu 的後端抽象層

### 後端選擇機制

wgpu 透過 `Instance` 的 `Backends` 參數控制可用的後端：

```rust
use wgpu::{Backends, Instance, InstanceDescriptor};

// 在所有平台上啟用所有可用的後端
let instance = Instance::new(InstanceDescriptor {
    backends: Backends::all(),
    ..Default::default()
});

// 明確指定後端（常用於除錯）
let instance = Instance::new(InstanceDescriptor {
    backends: Backends::VULKAN | Backends::METAL,
    ..Default::default()
});

// 僅 WebGPU（瀏覽器環境）
let instance = Instance::new(InstanceDescriptor {
    backends: Backends::BROWSER_WEBGPU,
    ..Default::default()
});
```

### Instance::enumerate_adapters

可以列舉系統中所有可用的 GPU 後端配接器：

```rust
let adapters = instance.enumerate_adapters(wgpu::Backends::all());
for adapter in adapters {
    println!("Found adapter: {:?} ({:?})", adapter.get_info().name, adapter.get_info().backend);
}
```

`AdapterInfo` 提供了後端類型、廠商 ID、裝置 ID 等重要資訊：

```rust
#[derive(Debug)]
pub struct AdapterInfo {
    pub name: String,
    pub vendor: u32,
    pub device: u32,
    pub device_type: DeviceType,
    pub backend: Backend,
}
```

## 後端特定的功能與限制

### Vulkan（Linux/Android/Windows）

Vulkan 是 wgpu 功能最完整的後端，支援所有核心功能：

| 功能 | 支援程度 |
|------|---------|
| 綁定群組 | 完全支援 |
| 計算著色器 | 完全支援 |
| Ray Tracing | 部分支援（需 VK_KHR_ray_tracing 擴展） |
| Push Constants | 128 bytes |
| Timestamp Queries | 支援 |
| Pipeline Cache | 支援 |

Vulkan 的限制主要在於 Android 裝置的碎片化。不同 Android GPU 對紋理格式、取樣器參數、著色器精確度的支援差異很大。

### Metal（macOS/iOS）

Apple 的 Metal 後端在 macOS 和 iOS 上提供最佳效能：

```rust
// Metal 特有的限制
let limits = device.limits();
// Metal 的 max_buffer_size 可能比 Vulkan 小
// Metal 對 texture 格式的支援較少（尤其是壓縮紋理）
```

**已知限制：**

1. **Indirect buffer 的限制**：Metal 對 indirect draw 的參數有對齊要求（4 bytes）。
2. **Texture format 支援**：某些 Vulkan 支援的格式在 Metal 上不可用（如 `R8G8B8A8UnormSrgb` 在部分舊裝置上）。
3. **Max compute workgroup size**：Metal 的 `maxTotalThreadsPerThreadgroup` 通常為 1024，低於 Vulkan 的典型值。
4. **Max vertex attributes**：部分 Apple GPU 僅支援 31 個 vertex attributes。

```rust
// 查詢 Metal 裝置限制
let limits = device.limits();
assert!(limits.max_vertex_attributes <= 31);
```

### DirectX 12（Windows）

DX12 後端在 Windows 上提供接近 Vulkan 的效能，但有幾個重要差異：

1. **Shader model**：DX12 需要 Shader Model 6.0+，部分舊 GPU 可能不支援。
2. **Root signature**：DX12 的 root signature 限制了 push constants 的大小和 bind group 的數量。
3. **Feature level**：透過 `dxc` 編譯器支援 HLSL 到 SPIR-V 的轉換。

```rust
// DX12 後端的特化處理
#[cfg(target_os = "windows")]
fn configure_for_dx12(device: &wgpu::Device) {
    // DX12 需要明確指定 DXC 編譯器路徑
    // 部分舊 GPU 不支援 DX12 feature level 12.0
}
```

### 瀏覽器 WebGPU

瀏覽器的 WebGPU 實現（如 Chrome 的 Dawn、Firefox 的 wgpu）是最嚴格的後端：

| 限制 | 說明 |
|------|------|
| 無檔案系統 | 無法讀取本地檔案，所有資產需透過 fetch |
| 著色器編譯 | 瀏覽器在首次繪製時才編譯著色器 |
| Timestamp Queries | 瀏覽器中不可用（安全性考量） |
| Buffer Mapping | 需要使用 Promise 或 callback |
| 裝置遺失 | 瀏覽器可能因為多種原因重置 GPU 裝置 |

```rust
// 瀏覽器環境的特殊處理
#[cfg(target_arch = "wasm32")]
fn handle_device_loss() {
    // 監聽 device loss 事件並準備重建資源
    let for_wasm = true;
}
```

## 測試策略

### 多後端整合測試

為每個後端建立獨立的測試案例是確保跨平台相容性的最佳方法：

```rust
#[cfg(test)]
mod tests {
    use wgpu::{Backends, Instance, InstanceDescriptor};

    fn create_device_for_test(backends: Backends) -> (wgpu::Device, wgpu::Queue) {
        let instance = Instance::new(InstanceDescriptor {
            backends,
            ..Default::default()
        });
        let adapter = pollster::block_on(instance.request_adapter(
            &wgpu::RequestAdapterOptions::default(),
        )).expect("No adapter found");

        pollster::block_on(adapter.request_device(
            &wgpu::DeviceDescriptor::default(),
            None,
        )).expect("Failed to create device")
    }

    #[test]
    fn test_particle_system_vulkan() {
        let (device, queue) = create_device_for_test(Backends::VULKAN);
        run_particle_test(&device, &queue);
    }

    #[test]
    fn test_particle_system_metal() {
        let (device, queue) = create_device_for_test(Backends::METAL);
        run_particle_test(&device, &queue);
    }

    #[test]
    fn test_particle_system_dx12() {
        let (device, queue) = create_device_for_test(Backends::DX12);
        run_particle_test(&device, &queue);
    }

    #[test]
    fn test_all_backends() {
        // 在所有可用後端上執行測試
        for backend in [Backends::VULKAN, Backends::METAL, Backends::DX12] {
            if let Ok((device, queue)) = create_device_for_test(backend) {
                run_particle_test(&device, &queue);
            }
        }
    }
}
```

### 渲染結果驗證

跨後端渲染的結果應逐像素一致。可以使用 screenshot 比較：

```rust
fn capture_and_compare(device: &wgpu::Device, queue: &wgpu::Queue, texture: &wgpu::Texture, reference: &[u8]) -> bool {
    let buffer_size = (texture.width() * texture.height() * 4) as u64;
    let staging = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("Staging"),
        size: buffer_size,
        usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });

    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor::default());
    encoder.copy_texture_to_buffer(
        wgpu::ImageCopyTexture {
            texture,
            mip_level: 0,
            origin: wgpu::Origin3d::ZERO,
            aspect: wgpu::TextureAspect::All,
        },
        wgpu::ImageCopyBuffer {
            buffer: &staging,
            layout: wgpu::ImageDataLayout {
                offset: 0,
                bytes_per_row: Some(4 * texture.width()),
                rows_per_image: Some(texture.height()),
            },
        },
        wgpu::Extent3d { width: texture.width(), height: texture.height(), depth_or_array_layers: 1 },
    );
    queue.submit(Some(encoder.finish()));

    // 讀取並比較（簡化）
    true
}
```

### CI 中的多後端測試

在 CI 環境中，通常只有一個後端可用。可以透過條件編譯矩陣來測試所有平台：

```yaml
# .github/workflows/ci.yml（範例）
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - run: cargo test --all-features
```

每個平台會使用其原生後端：Linux 用 Vulkan、macOS 用 Metal、Windows 用 DX12。

## 除錯後端特定問題

### 啟用驗證層

```rust
let instance = Instance::new(InstanceDescriptor {
    backends: Backends::all(),
    flags: wgpu::InstanceFlags::VALIDATION | wgpu::InstanceFlags::DEBUG,
    ..Default::default()
});

// 啟用 GPU 驗證層
let device = adapter.request_device(
    &wgpu::DeviceDescriptor {
        label: Some("Debug Device"),
        features: wgpu::Features::empty(),
        limits: wgpu::Limits::default(),
    },
    Some(std::path::Path::new("wgpu_debug_output")),
).await.unwrap();
```

### 常用的除錯技巧

1. **使用 push_error_scope / pop_error_scope**：

```rust
device.push_error_scope(wgpu::ErrorFilter::Validation);
// 執行可能失敗的操作
device.pop_error_scope().await.map(|error| {
    if let Some(err) = error {
        eprintln!("Validation error: {:?}", err);
    }
});
```

2. **檢查功能支援**：

```rust
fn check_feature_support(adapter: &wgpu::Adapter) {
    let features = adapter.features();
    let required = wgpu::Features::TIMESTAMP_QUERY | wgpu::Features::TEXTURE_COMPRESSION_BC;

    if !features.contains(required) {
        eprintln!("Warning: Required features not supported on this backend");
    }
}
```

3. **後端資訊日誌**：

```rust
fn log_adapter_info(adapter: &wgpu::Adapter) {
    let info = adapter.get_info();
    match info.backend {
        wgpu::Backend::Vulkan => println!("Running on Vulkan"),
        wgpu::Backend::Metal => println!("Running on Metal"),
        wgpu::Backend::Dx12 => println!("Running on DirectX 12"),
        wgpu::Backend::BrowserWebGpu => println!("Running on Browser WebGPU"),
        other => println!("Running on {:?}", other),
    }
    println!("GPU: {} (type: {:?})", info.name, info.device_type);
}
```

## 運行時後端選擇

最佳實踐是讓使用者在運行時選擇後端，而非編譯時決定：

```rust
#[derive(clap::ValueEnum, Clone)]
enum GpuBackend {
    Auto,
    Vulkan,
    Metal,
    Dx12,
}

fn select_backend(selection: &GpuBackend) -> wgpu::Backends {
    match selection {
        GpuBackend::Auto => {
            #[cfg(target_os = "macos")]
            { Backends::METAL }
            #[cfg(target_os = "windows")]
            { Backends::DX12 | Backends::VULKAN }
            #[cfg(target_os = "linux")]
            { Backends::VULKAN }
            #[cfg(target_arch = "wasm32")]
            { Backends::BROWSER_WEBGPU }
        }
        GpuBackend::Vulkan => Backends::VULKAN,
        GpuBackend::Metal => Backends::METAL,
        GpuBackend::Dx12 => Backends::DX12,
    }
}

// 使用者可以透過命令列參數指定後端
// cargo run -- --backend vulkan
```

也可以提供 fallback 鏈：

```rust
fn create_device_with_fallback() -> (wgpu::Device, wgpu::Queue) {
    let backends_in_order = [Backends::VULKAN, Backends::METAL, Backends::DX12, Backends::BROWSER_WEBGPU];
    let instance = Instance::new(InstanceDescriptor { backends: Backends::all(), ..Default::default() });

    for backends in backends_in_order {
        let instance = Instance::new(InstanceDescriptor { backends, ..Default::default() });
        if let Some(adapter) = pollster::block_on(instance.request_adapter(
            &wgpu::RequestAdapterOptions::default(),
        )) {
            if let Ok(result) = pollster::block_on(adapter.request_device(
                &wgpu::DeviceDescriptor::default(),
                None,
            )) {
                return result;
            }
        }
    }
    panic!("No suitable backend found");
}
```

## 常見跨後端陷阱

| 問題 | 說明 | 解決方案 |
|------|------|---------|
| `bytes_per_row` 對齊 | 某些後端要求 256 byte 對齊 | 使用 `wgpu::util::TextureDataLayout` 輔助函數 |
| 紋理格式不可用 | BC 壓縮在 Metal 上可能不支援 | 使用 `adapter.features()` 檢查 |
| Vertex buffer stride 對齊 | Metal 要求 4 bytes 對齊 | 確保 `array_stride` 是 4 的倍數 |
| 著色器精度差異 | `f32` 在不同後端計算結果可能不同 | 使用 epsilon 比較而非等號 |
| SwapChain 格式 | 某些後端不支援 `Rgba16Float` | 首選 `Bgra8UnormSrgb` |

## 總結

跨後端開發是 wgpu 的核心價值所在，但「寫一次到處運行」並非理所當然。理解每個後端的獨特限制、建立多後端測試矩陣、並在運行時提供後端選擇與 fallback 機制，是建構真正可移植 wgpu 應用的關鍵。

建議開發者在日常開發中定期在所有目標後端上測試應用程式。在 CI 中使用平台矩陣，並撰寫自動化的渲染結果比較測試，可以及早捕獲後端特定的問題。隨著 wgpu 生態的成熟，後端之間的差異正在逐步縮小，但開發者的警覺與測試仍然是確保跨平台品質的最後防線。

---

**參考資料**

- https://www.google.com/search?q=wgpu+backend+selection+runtime
- https://www.google.com/search?q=wgpu+Vulkan+Metal+DX12+differences
- https://www.google.com/search?q=wgpu+multi+backend+testing+strategy
- https://www.google.com/search?q=wgpu+backend+specific+limitations
