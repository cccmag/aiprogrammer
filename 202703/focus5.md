# 紋理、取樣與材質系統

## 從檔案載入到 PBR 材質管線（2020-2026）

### 前言

紋理是 GPU 渲染中最常用的資源類型之一。從簡單的 2D 圖片到 PBR（Physically Based Rendering）材質系統，紋理的存在讓 3D 場景從單色塑膠變成逼真的世界。

### 紋理建立

**從檔案載入**：

在 wgpu 中，紋理的建立通常經過三個步驟：載入圖片資料、建立紋理物件、上傳資料到 GPU：

```rust
// 1. 載入圖片（使用 image crate）
let img = image::open("assets/albedo.png").unwrap();
let rgba = img.to_rgba8();
let dimensions = img.dimensions();

// 2. 建立紋理
let texture = device.create_texture(&wgpu::TextureDescriptor {
    label: Some("albedo texture"),
    size: wgpu::Extent3d {
        width: dimensions.0,
        height: dimensions.1,
        depth_or_array_layers: 1,
    },
    mip_level_count: 1,
    sample_count: 1,
    dimension: wgpu::TextureDimension::D2,
    format: wgpu::TextureFormat::Rgba8UnormSrgb,
    usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
    view_formats: &[],
});

// 3. 上傳資料
queue.write_texture(
    wgpu::TexelCopyTextureInfo {
        texture: &texture,
        mip_level: 0,
        origin: wgpu::Origin3d::ZERO,
        aspect: wgpu::TextureAspect::All,
    },
    &rgba,
    wgpu::TexelCopyBufferLayout {
        offset: 0,
        bytes_per_row: Some(dimensions.0 as u32 * 4),
        rows_per_image: Some(dimensions.1 as u32),
    },
    wgpu::Extent3d {
        width: dimensions.0,
        height: dimensions.1,
        depth_or_array_layers: 1,
    },
);
```

**常用紋理格式**：

| 格式 | 每像素位元數 | 用途 |
|------|------------|------|
| `Rgba8UnormSrgb` | 32 | 彩色紋理（sRGB 色彩空間） |
| `Rgba8Unorm` | 32 | 資料紋理（法線貼圖、粗糙度） |
| `R32Float` | 32 | 單通道資料（高度圖） |
| `Bc7RgbaUnorm` | 變長 | 壓縮紋理（GPU 直接解壓縮） |
| `Rgba16Float` | 64 | HDR 紋理 |

**程序化紋理生成**：

不需要圖片檔案，直接用程式碼產生紋理資料：

```rust
// 程序化棋盤格紋理
let size = 512u32;
let mut pixels = Vec::with_capacity((size * size * 4) as usize);
for y in 0..size {
    for x in 0..size {
        let is_white = (x / 32 + y / 32) % 2 == 0;
        let c = if is_white { 255u8 } else { 0u8 };
        pixels.extend_from_slice(&[c, c, c, 255]);
    }
}
// 然後用 queue.write_texture 上傳
```

### 取樣器配置

取樣器決定 GPU 如何讀取紋理像素：

```rust
let sampler = device.create_sampler(&wgpu::SamplerDescriptor {
    label: Some("default sampler"),
    address_mode_u: wgpu::AddressMode::Repeat,
    address_mode_v: wgpu::AddressMode::Repeat,
    address_mode_w: wgpu::AddressMode::ClampToEdge,
    mag_filter: wgpu::FilterMode::Linear,
    min_filter: wgpu::FilterMode::Linear,
    mipmap_filter: wgpu::FilterMode::Linear,
    lod_min_clamp: 0.0,
    lod_max_clamp: f32::MAX,
    max_anisotropy: 16,  // 各向異性過濾
    compare: None,
    ..Default::default()
});
```

**取樣器參數的視覺效果**：

- **過濾模式**：`Nearest`（銳利但鋸齒）/ `Linear`（模糊但平滑）
- **夾持模式**：`ClampToEdge`（邊緣延伸）/ `Repeat`（重複拼接）/ `MirrorRepeat`（鏡像重複）
- **mipmap**：預先計算的小尺寸版本，減少遠處物體的渲染成本
- **各向異性過濾**：從傾斜角度觀看紋理時保持清晰度，`max_anisotropy: 16` 是最佳設定

### mipmap 產生

```rust
// 自動產生 mipmap 鏈
let mip_count = (dimensions.0.max(dimensions.1) as f32).log2().floor() as u32 + 1;

let texture = device.create_texture(&wgpu::TextureDescriptor {
    size: wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
    mip_level_count: mip_count,
    ..Default::default()
});

// 產生 mipmap 需要計算 Pass 或專用工具
// wgpu 不自動產生——你需要自己實作或使用 wgpu_mipmap crate
```

### PBR 材質管線

PBR（Physically Based Rendering）是現代遊戲和渲染引擎的主流材質模型。一套完整的 PBR 材質由多張紋理組成：

```
PBR 材質集：
├── albedo（漫反射顏色） → texture_2d<f32>
├── normal（法線貼圖） → texture_2d<f32>
├── roughness（粗糙度） → texture_2d<f32>
└── metallic（金屬度） → texture_2d<f32>
```

在 wgpu 中的部署：

```rust
// 建立 PBR 材質的 BindGroup 佈局
let pbr_layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
    entries: &[
        // binding 0: albedo
        wgpu::BindGroupLayoutEntry {
            binding: 0,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Texture { .. },
            count: None,
        },
        // binding 1: normal
        wgpu::BindGroupLayoutEntry {
            binding: 1,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Texture { .. },
            count: None,
        },
        // binding 2: roughness/metallic (packed)
        wgpu::BindGroupLayoutEntry {
            binding: 2,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Texture { .. },
            count: None,
        },
        // binding 3: sampler
        wgpu::BindGroupLayoutEntry {
            binding: 3,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Sampler { .. },
            count: None,
        },
    ],
    label: Some("PBR material layout"),
});
```

在 WGSL 中的對應：

```wgsl
@group(1) @binding(0) var albedo_map: texture_2d<f32>;
@group(1) @binding(1) var normal_map: texture_2d<f32>;
@group(1) @binding(2) var arm_map: texture_2d<f32>;  // roughness in G, metallic in B
@group(1) @binding(3) var mat_sampler: sampler;

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let albedo = textureSample(albedo_map, mat_sampler, in.uv);
    let normal = normalize(textureSample(normal_map, mat_sampler, in.uv).rgb * 2.0 - 1.0);
    let arm = textureSample(arm_map, mat_sampler, in.uv);
    let roughness = arm.g;
    let metallic = arm.b;
    
    // PBR 光照計算（Cook-Torrance BRDF）
    // ... 完整實作需要約 100 行程式碼 ...
}
```

### 材質系統與 BindGroup 整合

在實際應用中，材質通常會被組織成一個系統：

```rust
pub struct PbrMaterial {
    pub albedo: wgpu::Texture,
    pub normal: wgpu::Texture,
    pub arm: wgpu::Texture,       // 粗糙度 + 金屬度
    pub bind_group: wgpu::BindGroup,
}

impl PbrMaterial {
    pub fn new(device: &wgpu::Device, queue: &wgpu::Queue, layout: &wgpu::BindGroupLayout) -> Self {
        // 載入紋理...
        let bind_group = device.create_bind_group(&wgpu::BindGroupDescriptor {
            layout,
            entries: &[
                wgpu::BindGroupEntry { binding: 0, resource: wgpu::BindingResource::TextureView(&albedo_view) },
                wgpu::BindGroupEntry { binding: 1, resource: wgpu::BindingResource::TextureView(&normal_view) },
                wgpu::BindGroupEntry { binding: 2, resource: wgpu::BindingResource::TextureView(&arm_view) },
                wgpu::BindGroupEntry { binding: 3, resource: wgpu::BindingResource::Sampler(&sampler) },
            ],
            label: Some("PBR material"),
        });
        Self { albedo, normal, arm, bind_group }
    }
}

// 渲染時
rpass.set_bind_group(1, &material.bind_group, &[]);
```

這樣每個材質只需要一個 `set_bind_group` 呼叫，渲染多個物體時可以快速切換材質。

### 小結

紋理系統是 wgpu 中最重要的資源管理之一。從基本紋理建立到 PBR 材質管線，wgpu 提供了完整的支援。取樣器配置決定了紋理的視覺品質，而 BindGroup 的設計讓材質系統可以高效地組織和管理。

---

**下一步**：[WebGPU 與 WASM：瀏覽器端渲染](focus6.md)

## 延伸閱讀

- [PBR 材質理論](https://www.google.com/search?q=physically+based+rendering+PBR+theory)
- [wgpu 紋理範例](https://www.google.com/search?q=wgpu+texture+loading+example)
- [Learn OpenGL PBR](https://www.google.com/search?q=learn+OpenGL+PBR+tutorial)
