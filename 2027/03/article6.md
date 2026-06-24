# LLM 生成 3D 素材：從文字到模型的管線

## 前言

傳統 3D 模型製作需要美術設計師花費數小時到數天，使用 Blender、Maya 或 3ds Max 等工具手動建立模型與貼圖。2022 年以來，文字到 3D（Text-to-3D）生成技術快速成熟——從 OpenAI 的 Point-E、Shap-E 到 Google 的 DreamFusion，LLM 與擴散模型的結合讓「一句話生成 3D 模型」成為現實。本文將探討如何將這些 AI 生成的模型整合到 wgpu 渲染管線中，並討論 Rust 在格式轉換和渲染整合中的角色。

## 文字到 3D 的核心技術

### Point-E：點雲生成與曲面重建

OpenAI 在 2022 年末發布的 Point-E 是文字到 3D 的早期突破。它透過兩階段管線運作：先由文字生成點雲（point cloud），再由點雲重建為網格（mesh）。Point-E 的關鍵創新在於將 3D 生成轉化為兩個較簡單的 2D 生成問題——首先從文字生成物體的多視角圖像，再從這些圖像推導出 3D 點雲。

```python
# Point-E 使用範例（簡化）
from point_e.diffusion.configs import DIFFUSION_CONFIGS
from point_e.diffusion.sampler import PointCloudSampler

sampler = PointCloudSampler(
    device="cuda",
    **DIFFUSION_CONFIGS["point_cloud_diffusion"]
)
samples = sampler.sample_batch(
    batch_size=1,
    model=point_cloud_model,
    text="a red sports car with metallic finish",
)
```

Point-E 的最大優勢是速度——在單張 GPU 上只需 1-2 分鐘即可生成一個模型。但點雲格式僅包含不帶拓撲結構的離散點集，需要經過曲面重建才能轉換為 wgpu 可渲染的三角形網格。常用的曲面重建演算法包括 Poisson 重建和 Ball-Pivoting 演算法。

### Shap-E：隱式神經表示

Shap-E 是 OpenAI 的後續作品，直接生成隱式神經表示（NeRF 風格的輻射場），再透過 Marching Cubes 演算法轉換為網格或紋理。與 Point-E 相比，Shap-E 的輸出品質更高，且可以直接生成紋理座標和材質資訊。

```rust
// 使用 marching cubes 從 Shap-E 輸出的密度場提取網格
use rust_geometry::marching_cubes;

fn extract_mesh_from_implicit(
    field: &[f32],          // Shap-E 輸出的密度場
    grid_size: (usize, usize, usize),
    threshold: f32,          // 等值面閾值
) -> (Vec<Vertex>, Vec<u32>) {
    let mesh = marching_cubes::extract(
        field,
        grid_size.0,
        grid_size.1,
        grid_size.2,
        threshold,
    );
    let vertices: Vec<Vertex> = mesh.vertices.iter().map(|v| Vertex {
        position: v.position,
        normal: v.normal,
        uv: [v.position.x * 0.5 + 0.5, v.position.z * 0.5 + 0.5],
    }).collect();
    (vertices, mesh.indices)
}
```

### DreamFusion 與 SDS 技術

Google 的 DreamFusion 引入了 Score Distillation Sampling（SDS）技術，讓 2D 擴散模型可以指導 3D 表示的優化。SDS 的核心思想是：用一個可微分的渲染器將 3D 表示渲染為 2D 圖像，然後用預訓練的 2D 擴散模型來評估該圖像的「真實度」，並將梯度反向傳播回 3D 表示進行優化。

DreamFusion 輸出的 NeRF 體積密度場經過後處理，可以匯出為標準的 glTF/OBJ 格式。2025 年後的改良版本（如 MVDream、Zero123++）進一步支援了多視角一致性，大幅減少了傳統方法的「Janus 問題」（物體正面重複出現）。

## 將 AI 模型整合到 wgpu 渲染管線

### 格式轉換與 Rust 工具鏈

AI 生成的模型通常以 `.obj`、`.glb` 或 `.ply` 格式匯出。Rust 生態中有成熟的載入支援：

```rust
use gltf::Gltf;
use wgpu::util::DeviceExt;

fn load_ai_generated_model(
    path: &str,
    device: &wgpu::Device,
) -> (wgpu::Buffer, wgpu::Buffer, u32) {
    let (gltf, buffers, _) = gltf::Gltf::open(path).unwrap();
    let mesh = gltf.meshes().next().unwrap();
    let primitive = mesh.primitives().next().unwrap();
    let reader = primitive.reader(|buffer| Some(&buffers[buffer.index()]));

    let positions: Vec<[f32; 3]> = reader.read_positions().unwrap().collect();
    let normals: Vec<[f32; 3]> = reader.read_normals().unwrap().collect();
    let indices: Vec<u32> = reader.read_indices().unwrap().into_u32().collect();

    let vertex_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("AI Model Vertex Buffer"),
        contents: bytemuck::cast_slice(&positions),
        usage: wgpu::BufferUsages::VERTEX,
    });
    let index_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("AI Model Index Buffer"),
        contents: bytemuck::cast_slice(&indices),
        usage: wgpu::BufferUsages::INDEX,
    });
    (vertex_buffer, index_buffer, indices.len() as u32)
}
```

### Prompt 工程技巧

生成高品質 3D 模型的 prompt 需要精確描述。以下是經過實證有效的 prompt 結構：

| 要素 | 範例 | 說明 |
|------|------|------|
| 物體 | `a vintage wooden desk with carved legs` | 具體名詞 + 形容詞 |
| 材質 | `oak texture, brass handles, leather top` | 表面屬性 |
| 風格 | `low-poly game art, PBR ready` | 美術風格 |
| 視角 | `isometric view, three-quarter angle` | 視角參考 |
| 限制 | `no background, manifold mesh, under 5000 triangles` | 技術約束 |

不良 prompt 範例：`"a car"` → 產生物體不明確、面數過高、無法直接使用的模型。

## 實務挑戰與解決方案

AI 生成的網格經常包含非流形幾何、退化三角形或錯誤的法線方向。載入後必須進行清理：

```rust
fn cleanup_mesh(vertices: &mut Vec<Vertex>, indices: &mut Vec<u32>) {
    // 移除退化三角形（面積為零）
    indices.chunks_mut(3).retain(|tri| {
        let v0 = &vertices[tri[0] as usize];
        let v1 = &vertices[tri[1] as usize];
        let v2 = &vertices[tri[2] as usize];
        let e1 = v1.position - v0.position;
        let e2 = v2.position - v0.position;
        e1.cross(e2).length() > 0.0001
    });
    compute_normals(vertices, indices);
}
```

對於面數過高的模型，使用網格簡化演算法（如 Quadric Error Metrics）在載入後減少頂點數量，再上傳到 GPU。

## 未來方向

2026 年的 Text-to-3D 領域正朝即時生成邁進。MVDream 和 Zero123++ 等模型已經能在數秒內產生可用的 3D 資產。配合 wgpu 的跨平台能力，未來的遊戲引擎和 3D 應用將實現：使用者輸入文字 → AI 即時生成模型 → wgpu 即時渲染的完整管線，大幅降低 3D 內容創作的門檻。

## 參考資料

- [Point-E 官方實作](https://www.google.com/search?q=Point-E+OpenAI+3D+generation)
- [Shap-E 轉換工具](https://www.google.com/search?q=Shap-E+mesh+conversion+tutorial)
- [DreamFusion SDS 技術](https://www.google.com/search?q=DreamFusion+score+distillation+sampling)
- [wgpu gltf 載入](https://www.google.com/search?q=wgpu+rust+gltf+loading+tutorial)
- [rust-3d 格式轉換](https://www.google.com/search?q=rust+tobj+gltf+3d+model+conversion)
