# wgpu 中的記憶體管理：緩衝區與紋理

## 前言

在 GPU 程式設計中，記憶體管理是效能與穩定性的核心。wgpu 作為跨平台的圖形 API 抽象層，提供了統一且型別安全的緩衝區（Buffer）與紋理（Texture）管理機制。本文將深入探討 wgpu 中的各類緩衝區、紋理的建立與上傳策略、記憶體對映（mapping）技術，以及資源清理的最佳實務。

## 緩衝區類型與用途

wgpu 的 `Buffer` 是 GPU 可存取的一塊連續記憶體區域，透過 `wgpu::BufferDescriptor` 來描述其用途與屬性。緩衝區的核心屬性包括 `size`（大小）、`usage`（用途標記）和 `mapped_at_creation`（建立時是否立即對映）。

### Vertex Buffer（頂點緩衝區）

Vertex buffer 儲存頂點資料，如位置、法線、UV 座標等。其 usage 標記為 `wgpu::BufferUsages::VERTEX`。

```rust
let vertex_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Vertex Buffer"),
    contents: bytemuck::cast_slice(&vertices),
    usage: wgpu::BufferUsages::VERTEX,
});
```

建立後透過 `render_pass.set_vertex_buffer(slot, buffer.slice(..))` 將其綁定到管線。實務上建議將頂點資料打包為交錯（interleaved）格式，以提升 GPU 快取命中率。

### Index Buffer（索引緩衝區）

Index buffer 儲存三角形索引，可減少頂點資料重複。

```rust
let index_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Index Buffer"),
    contents: bytemuck::cast_slice(&indices),
    usage: wgpu::BufferUsages::INDEX,
});
```

使用 `render_pass.set_index_buffer(index_buffer.slice(..), wgpu::IndexFormat::Uint32)` 設定後，即可透過 `draw_indexed` 進行索引繪製。索引格式可選 `Uint16` 或 `Uint32`，前者節省記憶體但限制頂點數在 65535 以內。

### Uniform Buffer（統一緩衝區）

Uniform buffer 用於傳遞渲染管線中不常變化的資料，如變換矩陣、光源參數、材質屬性。其大小通常限制在 64KB 以內（依裝置而異）。

```rust
let uniform_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Uniform Buffer"),
    contents: bytemuck::cast_slice(&[uniform_data]),
    usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
});
```

Uniform buffer 透過 bind group 綁定到著色器。由於其大小限制，當需要傳遞大量資料時應考慮 storage buffer。

### Storage Buffer（儲存緩衝區）

Storage buffer 突破了 uniform buffer 的大小限制，支援更大容量的資料讀寫。這是 GPU 粒子系統、後處理特效等場景的關鍵工具。

```rust
let storage_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Storage Buffer"),
    contents: bytemuck::cast_slice(&initial_data),
    usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_DST | wgpu::BufferUsages::COPY_SRC,
});
```

在 WGSL 中將 storage buffer 宣告為 `var<storage, read_write>` 即可在計算著色器中讀寫。

### Indirect Buffer（間接緩衝區）

Indirect buffer 讓 GPU 自行決定繪製參數，適合 GPU driven rendering 管線。

```rust
let indirect_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Indirect Buffer"),
    contents: bytemuck::cast_slice(&[wgpu::DrawIndirectArgs {
        vertex_count: 3,
        instance_count: 1,
        first_vertex: 0,
        first_instance: 0,
    }]),
    usage: wgpu::BufferUsages::INDIRECT,
});
```

使用 `render_pass.multi_draw_indirect(indirect_buffer, 0, 1)` 即可由 GPU 驅動繪製。配合計算著色器產生間接參數，可實現可見性裁剪（occlusion culling）等進階技術。

## 紋理建立與上傳策略

Texture 在 wgpu 中透過 `TextureDescriptor` 建立，支援 1D、2D、3D、立方體紋理以及陣列紋理。

### 紋理描述

```rust
let texture = device.create_texture(&wgpu::TextureDescriptor {
    label: Some("Diffuse Texture"),
    size: wgpu::Extent3d { width: 1024, height: 1024, depth_or_array_layers: 1 },
    mip_level_count: 4,
    sample_count: 1,
    dimension: wgpu::TextureDimension::D2,
    format: wgpu::TextureFormat::Rgba8UnormSrgb,
    usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
});
```

`mip_level_count` 控制 mipmap 層級數量，`sample_count` 用於多重取樣抗鋸齒（MSAA）。紋理格式需謹慎選擇：`Rgba8UnormSrgb` 適用於一般顏色紋理，`Rgba32Float` 用於 HDR 或計算資料，`Depth32Float` 用於深度測試。

### 紋理資料上傳

上傳紋理資料的標準方式是透過 `queue.write_texture()`。這種方式無需建立中間緩衝區，但要求資料已在 CPU 端準備好：

```rust
queue.write_texture(
    wgpu::ImageCopyTexture {
        texture: &texture,
        mip_level: 0,
        origin: wgpu::Origin3d::ZERO,
        aspect: wgpu::TextureAspect::All,
    },
    &raw_pixels,
    wgpu::ImageDataLayout {
        offset: 0,
        bytes_per_row: Some(4 * 1024),
        rows_per_image: Some(1024),
    },
    wgpu::Extent3d { width: 1024, height: 1024, depth_or_array_layers: 1 },
);
```

`bytes_per_row` 必須是 256 的倍數（wgpu 的對齊要求），這是最常見的初學者踩坑點。

另一種方式是透過 staging buffer 上傳，先用 `COPY_DST` buffer 接收 CPU 資料，再用 `copy_buffer_to_texture` 命令複製到紋理：

```rust
let staging_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Staging Buffer"),
    contents: &raw_pixels,
    usage: wgpu::BufferUsages::COPY_SRC,
});

let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor::default());
encoder.copy_buffer_to_texture(
    wgpu::ImageCopyBuffer {
        buffer: &staging_buffer,
        layout: wgpu::ImageDataLayout {
            offset: 0,
            bytes_per_row: Some(4 * 1024),
            rows_per_image: Some(1024),
        },
    },
    wgpu::ImageCopyTexture {
        texture: &texture,
        mip_level: 0,
        origin: wgpu::Origin3d::ZERO,
        aspect: wgpu::TextureAspect::All,
    },
    wgpu::Extent3d { width: 1024, height: 1024, depth_or_array_layers: 1 },
);
queue.submit(Some(encoder.finish()));
```

這種方式適合在批次載入大量紋理時使用，可以透過 command buffer 批次提交。

## 記憶體對映（Memory Mapping）

wgpu 的 buffer mapping 讓 CPU 可以直接存取 GPU 記憶體。這是讀取 GPU 計算結果（如粒子位置）或上傳動態資料的關鍵機制。

### Buffer Mapping API

```rust
let mapped_buffer = device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("Mapped Buffer"),
    size: 4096,
    usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
    mapped_at_creation: false,
});

// 對映操作需要非同步處理
let buffer_slice = mapped_buffer.slice(..);
buffer_slice.map_async(wgpu::MapMode::Read, |result| {
    match result {
        Ok(()) => {
            let data = buffer_slice.get_mapped_range();
            // 讀取資料...
            drop(data);
            mapped_buffer.unmap();
        }
        Err(e) => eprintln!("Map failed: {:?}", e),
    }
});
device.poll(wgpu::Maintain::Wait);
```

`mapped_at_creation` 參數控制在建立緩衝區時是否立即對映。設定為 `true` 時，可以在 `create_buffer` 之後直接呼叫 `buffer.slice(..).get_mapped_range_mut()` 寫入資料，然後 `unmap()` 提交給 GPU。這對 uniform buffer 或小型上傳非常方便：

```rust
let buffer = device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("Dynamic Uniform"),
    size: std::mem::size_of::<UniformData>() as u64,
    usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
    mapped_at_creation: true,
});
{
    let mut mapped = buffer.slice(..).get_mapped_range_mut();
    let typed: &mut UniformData = bytemuck::from_bytes_mut(&mut mapped);
    typed.model = Matrix4::identity();
} // drop 自動觸發 unmap
```

`get_mapped_range()` 回傳的 `BufferView` 或 `BufferViewMut` 在 drop 時會解除參照。一定要在 `unmap()` 之前 drop，否則會 panic。

### 雙緩衝策略

動態資料（如每幀更新的 uniform buffer）建議使用雙緩衝或環形緩衝區（ring buffer），避免 CPU 寫入與 GPU 讀取的競爭：

```rust
const NUM_FRAMES: usize = 3;
let uniform_buffers: Vec<wgpu::Buffer> = (0..NUM_FRAMES)
    .map(|i| device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some(&format!("Uniform Frame {}", i)),
        contents: bytemuck::cast_slice(&[default_uniform]),
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
    }))
    .collect();
```

渲染循環中根據 `frame_index % NUM_FRAMES` 選擇當前可用的緩衝區，並使用 `queue.write_buffer()` 更新內容。

## 資源清理與回收

wgpu 的資源管理遵循 RAII 原則——當 `Buffer` 或 `Texture` 物件離開作用域時，其對應的 GPU 資源會被自動釋放。但實務上需要注意以下幾點：

### 命令編碼器的生命週期

`CommandEncoder` 在 `finish()` 之後仍持有資源參照，直到 submit 的 command buffer 被 GPU 執行完畢。建議在每幀結束時明確 drop：

```rust
fn render_frame(device: &wgpu::Device, queue: &wgpu::Queue, ...) {
    let mut encoder = device.create_command_encoder(...);
    // ... 記錄命令
    let cmd_buf = encoder.finish();
    queue.submit([cmd_buf]);
    // encoder 在此處 drop
}
```

### TextureView 與 Sampler 的管理

每次建立 `TextureView` 都會增加內部參照計數。在動態建立 view 的場景（如 rendertarget swap），應盡量重用 view 而非每次重新建立：

```rust
// 避免：在渲染循環內重複建立
for _ in 0..frames {
    let view = texture.create_view(&wgpu::TextureViewDescriptor::default());
    // ...
}

// 建議：在初始化時建立一次
let view = texture.create_view(&wgpu::TextureViewDescriptor::default());
for _ in 0..frames {
    // 重用 view
}
```

### 透過 Device::destroy 強制釋放

當確定某個資源不再需要時，可以呼叫 `buffer.destroy()` 或 `texture.destroy()` 強制釋放 GPU 記憶體。這在資源池（resource pool）場景中尤其重要：

```rust
fn recycle_buffer(device: &wgpu::Device, buffer: &wgpu::Buffer) {
    // 先 destroy 釋放 GPU 資源
    buffer.destroy();
}
```

### 資源洩漏偵測

wgpu 在 debug 模式下會追蹤所有活躍的資源。在應用程式關閉時，若仍有未釋放的資源，控制台會印出警告。開發時建議啟用 `wgpu::Backends::all()` 與 `wgpu::PowerPreference::HighPerformance` 搭配驗證層。

## 總結

wgpu 的記憶體管理機制提供了對 GPU 記憶體的完整控制，同時保持了跨平台的統一抽象。理解不同緩衝區類型（vertex、index、uniform、storage、indirect）的用途與限制，掌握紋理建立與上傳的兩種策略（`write_texture` 與 staging buffer），以及正確使用 memory mapping 和資源清理機制，是編寫高效能 wgpu 應用的基礎。

在實務專案中，建議建立統一的資源管理器，追蹤所有活躍 buffer 和 texture 的生命週期，並在幀結束時統一回收不再使用的資源。下一篇文章將探討如何利用 storage buffer 與計算著色器實現 GPU 粒子系統。

---

**參考資料**

- https://www.google.com/search?q=wgpu+buffer+usage+flags
- https://www.google.com/search?q=wgpu+texture+upload+staging+buffer
- https://www.google.com/search?q=wgpu+buffer+mapping+map_async
- https://www.google.com/search?q=wgpu+resource+management+RAII
