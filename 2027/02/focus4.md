# 3D 遊戲開發與著色器（2022-2026）

## Bevy 3D 渲染管線

Bevy 的 3D 渲染基於 wgpu——Rust 對 WebGPU 標準的低階實作。wgpu 提供跨平台圖形 API 抽象，底層可以選擇 Vulkan、Metal、DirectX 12 或 WebGPU。

```
應用程式層級
    │
Bevy Renderer (ECS System)
    │
bevy_render / bevy_pbr
    │
wgpu (跨平台圖形抽象)
    │
Vulkan │ Metal │ D3D12 │ WebGPU
```

渲染管線在 ECS 中透過 Render Graph 描述。每個渲染階段（陰影貼圖、幾何體渲染、後處理）都是一個節點，節點之間以 GPU 紋理或緩衝區連接。

## WGSL 著色器程式設計

WGSL（WebGPU Shading Language）是 WebGPU 的官方著色器語言，語法類似 Rust，型別安全。Bevy 使用 WGSL 作為其著色器標準。

### 頂點著色器範例

以下是一個基本的頂點著色器，處理頂點位置與法線：

```wgsl
struct VertexInput {
    @location(0) position: vec3<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
};

struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
    @location(0) world_normal: vec3<f32>,
    @location(1) uv: vec2<f32>,
};

struct Uniforms {
    model: mat4x4<f32>,
    view: mat4x4<f32>,
    projection: mat4x4<f32>,
};

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

@vertex
fn vertex_main(input: VertexInput) -> VertexOutput {
    var output: VertexOutput;
    let world_pos = uniforms.model * vec4<f32>(input.position, 1.0);
    output.clip_position = uniforms.projection * uniforms.view * world_pos;
    output.world_normal = normalize(mat3x3<f32>(uniforms.model) * input.normal);
    output.uv = input.uv;
    return output;
}
```

### 片元著色器範例

```wgsl
@group(0) @binding(1) var base_color_texture: texture_2d<f32>;
@group(0) @binding(2) var base_color_sampler: sampler;

@fragment
fn fragment_main(input: VertexOutput) -> @location(0) vec4<f32> {
    let albedo = textureSample(base_color_texture, base_color_sampler, input.uv);
    let light_dir = normalize(vec3<f32>(1.0, 1.0, 1.0));
    let diffuse = max(dot(input.world_normal, light_dir), 0.0);
    return albedo * (diffuse + 0.1); // 漫反射 + 環境光
}
```

## PBR 材質與光照

Bevy 內建基於物理的渲染（PBR），透過 `StandardMaterial` 設定：

```rust
fn setup_3d(
    mut commands: Commands,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut meshes: ResMut<Assets<Mesh>>,
) {
    // 球體
    commands.spawn(PbrBundle {
        mesh: meshes.add(Mesh::from(Sphere { radius: 1.0 })),
        material: materials.add(StandardMaterial {
            base_color: Color::rgb(0.8, 0.2, 0.2),
            metallic: 0.5,
            perceptual_roughness: 0.3,
            ..default()
        }),
        transform: Transform::from_xyz(0.0, 1.0, 0.0),
        ..default()
    });

    // 光源
    commands.spawn(PointLightBundle {
        point_light: PointLight {
            intensity: 1500.0,
            color: Color::rgb(1.0, 1.0, 0.9),
            ..default()
        },
        transform: Transform::from_xyz(4.0, 8.0, 4.0),
        ..default()
    });

    // 攝影機
    commands.spawn(Camera3dBundle {
        transform: Transform::from_xyz(-3.0, 2.0, 5.0).looking_at(Vec3::ZERO, Vec3::Y),
        ..default()
    });
}
```

Bevy 的 PBR 實作支援：
- **多種光源**：方向光（太陽）、點光源（燈泡）、聚光燈（手電筒）
- **陰影貼圖**：透過 Render Graph 自動產生陰影
- **IBL（Image-Based Lighting）**：使用 HDR 環境貼圖實現間接光照
- **法線貼圖**：凹凸細節
- **環境遮擋**（AO）：接觸陰影

## GLTF 模型載入與動畫

實際遊戲很少用程式碼生成幾何體——通常使用 3D 建模工具匯出 GLTF 格式：

```rust
fn load_model(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn(SceneBundle {
        scene: asset_server.load("models/character.gltf#Scene0"),
        transform: Transform::from_xyz(0.0, 0.0, 0.0),
        ..default()
    });
}
```

Bevy 原生支援 GLTF 2.0，包括：
- 網格與材質
- 骨架動畫（Skinning）
- 形態目標（Morph Targets）
- 攝影機與光源
- 節點層級結構

播放動畫需要透過 `AnimationPlayer`：

```rust
fn play_animation(
    mut players: Query<&mut AnimationPlayer>,
    mut done: Local<bool>,
) {
    if !*done {
        if let Ok(mut player) = players.get_single_mut() {
            player.play(AnimationClip::default()).repeat();
            *done = true;
        }
    }
}
```

## 自訂著色器外觀

Bevy 允許開發者用自訂 WGSL 著色器取代預設 PBR 管線：

```rust
impl Material for CustomMaterial {
    fn fragment_shader() -> ShaderRef {
        "shaders/custom_material.wgsl".into()
    }
}
```

這種機制讓遊戲可以實現卡通渲染、鹽酸效果、水體模擬、全螢幕後處理等特效。

## 參考

- [Bevy 3D 教學](https://www.google.com/search?q=Bevy+3D+rendering+tutorial)
- [WGSL 語法參考](https://www.google.com/search?q=WGSL+shading+language+syntax)
- [wgpu 入門](https://www.google.com/search?q=wgpu+Rust+graphics+tutorial)
- [GLTF 2.0 規格](https://www.google.com/search?q=GLTF+2.0+format+specification)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
