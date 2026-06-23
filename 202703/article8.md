# 神經渲染：在 Rust 中整合 NeRF

## 前言

神經輻射場（Neural Radiance Fields, NeRF）是 2020 年由 Mildenhall 等人提出的革命性技術——它用一個小型多層感知器（MLP）隱式編碼 3D 場景的體積密度和顏色資訊。與傳統的多邊形網格渲染不同，NeRF 直接從 5D 輸入——三維空間位置加上二維視角方向——映射到 4D 輸出（RGB 顏色加上體積密度），實現了照片級的真實視圖合成。本文將探討如何在 Rust 和 wgpu 環境中整合 NeRF 推論，讓神經渲染成為即時 3D 應用程式的一部分。

## NeRF 的核心數學原理

### 體積渲染方程式

NeRF 的核心是體積渲染的離散近似。沿著每條射線採樣 N 個點，依序累積顏色和透光度：

```
C(r) = Σᵢ₌₁ᴺ Tᵢ × αᵢ × cᵢ

其中各項的物理意義：
Tᵢ = exp(-Σⱼ₌₁ⁱ⁻¹ σⱼ × δⱼ)   累積透光度（光線穿透率）
αᵢ = 1 - exp(-σᵢ × δᵢ)        第 i 個採樣點的不透明度
cᵢ = 神經網路在該點輸出的 RGB 顏色
σᵢ = 神經網路在該點輸出的體積密度
δᵢ = 相鄰採樣點之間的距離
```

這個公式模擬了光線穿過半透明介質時的物理過程：光線在行進過程中逐漸被吸收，同時每個微小的體積元素都會發出顏色光。NeRF 的目標就是讓神經網路學會正確的 σ 和 c 分布，使得從任意視角渲染的 2D 圖像都與真實照片一致。

### 位置編碼

NeRF 使用位置編碼（Positional Encoding）將低維輸入映射到高維空間，幫助 MLP 學習高頻細節：

```rust
fn positional_encode(x: &[f32; 3], num_frequencies: u32) -> Vec<f32> {
    let mut encoded = Vec::with_capacity((num_frequencies * 6) as usize);
    for i in 0..num_frequencies {
        let freq = 2.0_f32.powi(i as i32);
        encoded.push((freq * x[0]).sin());
        encoded.push((freq * x[0]).cos());
        encoded.push((freq * x[1]).sin());
        encoded.push((freq * x[1]).cos());
        encoded.push((freq * x[2]).sin());
        encoded.push((freq * x[2]).cos());
    }
    encoded
}
```

## 在 wgpu 中執行 NeRF 推論

### 計算著色器實現 MLP 前向傳播

將 NeRF 的 MLP 前向傳播實作為 WGSL 計算著色器，可以在 GPU 上平行處理大量射線。每個工作組負責一組像素的射線計算：

```wgsl
struct LayerWeights {
    weight: array<f32, 256>,
    bias: array<f32, 256>,
}

@group(0) @binding(0) var<storage, read> layers: array<LayerWeights>;
@group(0) @binding(1) var<storage, read_write> rays: array<RayOutput>;

@compute @workgroup_size(8, 8, 1)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let pixel_x = id.x;
    let pixel_y = id.y;

    // 為此像素生成射線，沿射線採樣
    var accumulated_color = vec3<f32>(0.0, 0.0, 0.0);
    var transmittance = 1.0;

    for (var s = 0u; s < 64u; s++) {
        let t = (f32(s) + 0.5) / 64.0;
        let pos = get_ray_position(pixel_x, pixel_y, t);
        let dir = get_ray_direction(pixel_x, pixel_y);

        // 位置編碼
        var pe: array<f32, 63>;
        positional_encode(pos, &pe, 10);

        // MLP 前向傳播
        var h = pe;
        for (var l = 0u; l < 8u; l++) {
            h = mat_vec_mul(&layers[l], h);
            h = relu(h);
        }

        let sigma = relu(h[0]);
        let rgb = vec3<f32>(
            sigmoid(h[1]),
            sigmoid(h[2]),
            sigmoid(h[3]),
        );

        // 體積渲染累積
        let alpha = 1.0 - exp(-sigma * 0.01);
        accumulated_color += transmittance * alpha * rgb;
        transmittance *= 1.0 - alpha;
    }

    // 寫入最終像素顏色
    let pixel_idx = pixel_y * 1024 + pixel_x;
    rays[pixel_idx].color = accumulated_color;
}
```

### Rust 側的 ONNX Runtime 整合

對於完整的預訓練 NeRF 模型（如 Instant NGP、Nerfacto），更務實的做法是使用 ONNX Runtime 進行推論。`tract-onnx` 是 Rust 生態中最成熟的 ONNX 推論庫，支援 GPU 加速：

```rust
use tract_onnx::prelude::*;

fn load_nerf_model(path: &str) -> TractModel {
    let model = onnx::Model::load(path).unwrap();
    model
        .into_optimized()
        .unwrap()
        .into_runnable()
        .unwrap()
}

fn render_nerf_view(
    model: &TractModel,
    camera: &Camera,
    resolution: (u32, u32),
) -> Vec<u8> {
    let (w, h) = resolution;
    let mut pixels = vec![0u8; (w * h * 4) as usize];
    let rays = generate_rays(camera, w, h);

    // 分批執行推理以控制 GPU 記憶體使用
    for (chunk_idx, chunk) in rays.chunks(4096).enumerate() {
        let input = tensor2(chunk);
        let result = model.run(tvec!(input)).unwrap();
        let output = result[0].to_array_view::<f32>().unwrap();

        for (i, pixel) in output.outer_iter().enumerate() {
            let idx = chunk_idx * 4096 + i;
            pixels[idx * 4..][..3].copy_from_slice(&[
                (pixel[0].min(1.0).max(0.0) * 255.0) as u8,
                (pixel[1].min(1.0).max(0.0) * 255.0) as u8,
                (pixel[2].min(1.0).max(0.0) * 255.0) as u8,
            ]);
            pixels[idx * 4 + 3] = 255;
        }
    }
    pixels
}
```

### 實時體積渲染的挑戰

Naive NeRF 的渲染速度約為每幀數十秒，距離 60fps 的實時渲染有巨大差距。目前主流的最佳化技術：

| 方法 | 發表年份 | 原理 | 速度提升 | 品質影響 |
|------|---------|------|---------|---------|
| Plenoxels | 2022 | 稀疏體素網格替代 MLP | ~100x | 微小 |
| Instant NGP | 2022 | 多解析度 Hash Encoding | ~1000x | 可忽略 |
| 3D Gaussian Splatting | 2023 | 高斯橢球體直接表示 | ~100x | 微小 |
| Zip-NeRF | 2023 | 多尺度抗鋸齒採樣 | ~10x | 無 |

其中 3D Gaussian Splatting（3DGS）在 2024-2026 年間迅速成為主流——它將場景表示為數百萬個高斯橢球體，使用類似點雲的渲染方式，可以在消費級 GPU 上達到 30fps 以上，且能與傳統光柵化管線整合。

## 混合渲染：NeRF + 傳統網格

在實際應用中，靜態背景使用 NeRF 渲染，動態物體使用傳統網格渲染，可以兼顧品質和互動性：

```rust
fn hybrid_render(
    encoder: &mut wgpu::CommandEncoder,
    nerf_target: &wgpu::TextureView,
    mesh_target: &wgpu::TextureView,
    final_target: &wgpu::TextureView,
) {
    // 階段 1：NeRF 計算著色器渲染背景
    {
        let mut cpass = encoder.begin_compute_pass(&Default::default());
        cpass.set_pipeline(&nerf_pipeline);
        cpass.set_bind_group(0, &nerf_bind_group, &[]);
        cpass.dispatch_workgroups(width / 8, height / 8, 1);
    }

    // 階段 2：傳統網格渲染動態物體
    {
        let mut rpass = encoder.begin_render_pass(
            &wgpu::RenderPassDescriptor {
                color_attachments: &[wgpu::RenderPassColorAttachment {
                    view: final_target,
                    ops: wgpu::Operations { load: wgpu::LoadOp::Load, store: wgpu::StoreOp::Store },
                    ..Default::default()
                }],
                ..Default::default()
            }
        );
        rpass.set_pipeline(&mesh_pipeline);
        rpass.draw(0..num_indices, 0..1);
    }
}
```

## 未來展望

2026 年的神經渲染領域正快速收斂到實時應用。Instant NGP 的 Hash Encoding 技術已經被整合到多個遊戲引擎的實驗分支中。配合 Rust 的所有權模型和 wgpu 的跨後端能力，開發者可以建構出同時使用傳統光柵化、光線追蹤和神經渲染的混合管線。隨著專用 AI 加速器（Tensor Core、Neural Engine）在 GPU 中的普及，NeRF 級別的神經渲染將在 2027-2028 年成為 3D 應用程式的標準功能。

## 參考資料

- [NeRF 原始論文](https://www.google.com/search?q=NeRF+Neural+Radiance+Fields+Mildenhall)
- [Instant NGP GPU 加速](https://www.google.com/search?q=Instant+Neural+Graphics+Primitives+hash+encoding)
- [3D Gaussian Splatting](https://www.google.com/search?q=3D+Gaussian+Splatting+real+time+rendering)
- [tract-onnx Rust Crate](https://www.google.com/search?q=tract+onnx+rust+inference+GPU)
- [wgpu 計算著色器範例](https://www.google.com/search?q=wgpu+compute+shader+tutorial+rust)
