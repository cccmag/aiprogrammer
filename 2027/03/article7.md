# 程序化紋理生成與 AI 風格轉換

## 前言

紋理是 3D 渲染中決定視覺真實感的關鍵要素。傳統紋理依賴美術人員手繪或相機拍攝的真實照片，再經過 UV 展開貼合到模型表面。程序化紋理（Procedural Texture）則完全透過數學函數即時生成紋理顏色——它具有無限解析度、無縫平鋪、零儲存空間的優勢。然而，純程序化紋理往往缺乏真實世界的複雜細節。AI 風格轉換（Style Transfer）的出現改變了這個局面：將程序化生成的核心圖案與 AI 學習的材質風格相結合，可以兼顧可控性和真實感。

## WGSL 中的程序化紋理演算法

### 雜訊函數

Perlin 和 Simplex 雜訊是程序化紋理的基石。以下是直接在 WGSL 中實作的 Value Noise：

```wgsl
fn hash(p: vec2<u32>) -> u32 {
    var h: u32 = p.x * 374761393u + p.y * 668265263u;
    h = (h ^ (h >> 13u)) * 1274126177u;
    return h ^ (h >> 16u);
}

fn smooth_noise(uv: vec2<f32>) -> f32 {
    let i = floor(uv);
    let f = uv - i;
    let u = f * f * (3.0 - 2.0 * f);  // smoothstep 插值

    let a = f32(hash(vec2<u32>(i))) / 4294967295.0;
    let b = f32(hash(vec2<u32>(i + vec2(1.0, 0.0)))) / 4294967295.0;
    let c = f32(hash(vec2<u32>(i + vec2(0.0, 1.0)))) / 4294967295.0;
    let d = f32(hash(vec2<u32>(i + vec2(1.0, 1.0)))) / 4294967295.0;

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
```

分形布朗運動（FBM）透過疊加不同頻率和振幅的雜訊層，生成自然紋理：

```wgsl
fn fbm(uv: vec2<f32>, octaves: u32) -> f32 {
    var value = 0.0;
    var amplitude = 0.5;
    var frequency = 1.0;
    for (var i = 0u; i < octaves; i++) {
        value += amplitude * smooth_noise(uv * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```

### Voronoi 紋理

Voronoi 圖適用於生成瓷磚、細胞、有機紋理和石頭裂縫等效果：

```wgsl
fn voronoi(uv: vec2<f32>) -> f32 {
    let i = floor(uv);
    let f = uv - i;
    var min_dist = 1.0;
    for (var y = -1; y <= 1; y++) {
        for (var x = -1; x <= 1; x++) {
            let neighbor = vec2(f32(x), f32(y));
            // 用 hash 產生隨機點位置
            let point = vec2(
                f32(hash(vec2<u32>(i + neighbor + vec2(0.1, 0.1)))) 
                    / 4294967295.0,
                f32(hash(vec2<u32>(i + neighbor + vec2(0.2, 0.2)))) 
                    / 4294967295.0,
            );
            let diff = neighbor + point - f;
            min_dist = min(min_dist, dot(diff, diff));
        }
    }
    return min_dist;
}
```

### 大理石材質

結合 FBM 和正弦波可生成逼真的大理石紋路。這是程序化紋理的經典範例——用少量的數學運算模擬出複雜的自然圖案：

```wgsl
fn marble(uv: vec2<f32>, time: f32) -> vec3<f32> {
    let n = fbm(uv * 4.0, 6);
    let vein = sin(uv.x * 10.0 + uv.y * 5.0 + n * 2.0 + time * 0.2);
    let t = vein * 0.5 + 0.5;
    let light = vec3<f32>(0.95, 0.92, 0.85);  // 淺色紋路
    let dark = vec3<f32>(0.30, 0.25, 0.20);   // 深色紋路
    return mix(light, dark, t);
}
```

## AI 風格轉換在紋理上的應用

### 神經風格轉換的運作原理

Neural Style Transfer（NST）使用預訓練的 VGG 或 MobileNet CNN 模型，分離內容圖像的結構特徵和風格圖像的紋理特徵。透過 Gram 矩陣捕捉風格的統計特性，再以梯度下降法最小化內容損失和風格損失的加權和。將 NST 應用於紋理生成時，開發者可以指定「像木頭一樣的紋理走向」或「帶有水彩渲染風格的金屬質感」。

Rust 整合 NST 模型的流程如下：

```rust
use tract_onnx::prelude::*;

fn apply_style_transfer(
    content_texture: &[f32],
    style: &str,
    width: u32,
    height: u32,
) -> Vec<f32> {
    let model = onnx::Model::load(
        &format!("models/style_{}.onnx", style)
    ).unwrap();

    let input = tensor4(content_texture)
        .into_shape(&[1, 3, height as i64, width as i64])
        .unwrap();

    let result = model.run(tvec!(input.into())).unwrap();
    result[0].to_array_view::<f32>().unwrap().to_owned().into_raw_vec()
}
```

### 程序化 + AI 的混合管線

純程序化紋理缺乏真實世界的隨機細節，純 AI 紋理則難以精確控制。最佳方案是混合管線：

```
輸入參數（顏色、粗糙度、圖案類型）
      ↓
程序化核心（雜訊疊加、voronoi 分割、fbm 頻譜）→ 基礎紋理
      ↓
AI 細節增強（超解析度重建、真實化生成對抗網路）
      ↓
風格轉換（統一美術風格：油畫、水彩、像素風）
      ↓
最終紋理 → wgpu 紋理綁定
```

### 即時執行考量

在 WGSL 中執行完整的風格轉換神經網路對行動 GPU 來說負擔過重。實際部署時採用以下策略：

- **蒸餾模型**：使用 TinyGAN 或 MobileStyleNet 等輕量網路，將參數量壓縮到 1MB 以下
- **快取策略**：對靜態物體預先計算紋理並存入 GPU texture array，避免每幀重新生成
- **解析度分級**：近距離使用完整風格轉換，遠距離使用純程序化近似版本

## Rust 整合範例

以下是使用計算著色器在 GPU 上生成程序化紋理、再傳遞給渲染管線的完整流程：

```rust
fn create_procedural_texture(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    width: u32,
    height: u32,
    compute_pipeline: &wgpu::ComputePipeline,
    bind_group: &wgpu::BindGroup,
) -> wgpu::Texture {
    let texture = device.create_texture(&wgpu::TextureDescriptor {
        size: wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
        format: wgpu::TextureFormat::Rgba8UnormSrgb,
        usage: wgpu::TextureUsages::STORAGE_BINDING
            | wgpu::TextureUsages::TEXTURE_BINDING,
        ..Default::default()
    });

    let mut encoder = device.create_command_encoder(&Default::default());
    {
        let mut cpass = encoder.begin_compute_pass(&Default::default());
        cpass.set_pipeline(compute_pipeline);
        cpass.set_bind_group(0, bind_group, &[]);
        cpass.dispatch_workgroups(width / 8, height / 8, 1);
    }
    queue.submit(Some(encoder.finish()));
    texture
}
```

## 未來趨勢

2026 年即時神經紋理壓縮（Neural Texture Compression，NTC）和 AI 驅動的材質球生成正在改變遊戲和影視管線。NTC 使用小型神經網路壓縮紋理，以極低的記憶體消耗維持高品質。配合 wgpu 的跨平台 compute shader 支援，開發者可以直接在 GPU 上完成從程序化生成到 AI 風格轉換的完整材質管線，無需 CPU 中繼。

## 參考資料

- [WGSL 雜訊函數實作合集](https://www.google.com/search?q=WGSL+noise+function+shader+code)
- [神經風格轉換原始論文](https://www.google.com/search?q=neural+style+transfer+Gatys+paper)
- [MobileStyleNet 輕量化方案](https://www.google.com/search?q=MobileStyleNet+real+time+style+transfer)
- [程序化紋理大全](https://www.google.com/search?q=procedural+texture+shader+examples+Inigo+Quilez)
- [wgpu 計算著色器紋理](https://www.google.com/search?q=wgpu+compute+shader+texture+generation)
