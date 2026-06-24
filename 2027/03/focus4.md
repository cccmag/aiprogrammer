# 著色器程式設計：WGSL

## WebGPU Shading Language（2021-2026）

### WGSL 的定位

WGSL（WebGPU Shading Language）是 WebGPU 的官方著色器語言。為什麼不直接用 SPIR-V、HLSL 或 MSL？

- **SPIR-V**：是二進位中間表示，不適合人類編寫
- **HLSL**：僅限 DirectX 生態
- **MSL**：僅限 Apple 生態

WGSL 的設計目標：**一種可讀、安全、跨平台的著色器語言，可以直接編寫，也可以作為其他語言的編譯目標**。

### 語法基礎

WGSL 語法類似於 Rust 和 GLSL 的混合體：

**型別系統**：

```wgsl
// 基本純量型別
let a: i32 = -42;    // 32 位元有號整數
let b: u32 = 42u;     // 32 位元無號整數
let c: f32 = 3.14;    // 32 位元浮點數
let d: bool = true;   // 布林值

// 向量型別
let v2: vec2<f32> = vec2(1.0, 2.0);
let v3: vec3<f32> = vec3(1.0, 2.0, 3.0);
let v4: vec4<f32> = vec4(1.0, 2.0, 3.0, 4.0);

// 矩陣型別（列主序）
let m3: mat3x3<f32> = mat3x3(
    vec3(1, 0, 0),
    vec3(0, 1, 0),
    vec3(0, 0, 1),
);

// 陣列型別
let arr: array<f32, 4> = array(1.0, 2.0, 3.0, 4.0);
```

**函數定義**：

```wgsl
fn lerp(a: f32, b: f32, t: f32) -> f32 {
    return a + (b - a) * t;
}

fn saturate(x: f32) -> f32 {
    return clamp(x, 0.0, 1.0);
}
```

### 頂點著色器完整範例

```wgsl
struct VertexInput {
    @location(0) position: vec3<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
};

struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
    @location(0) world_normal: vec3<f32>,
    @location(1) world_position: vec3<f32>,
    @location(2) tex_coord: vec2<f32>,
};

struct Camera {
    view_proj: mat4x4<f32>,
    world: mat4x4<f32>,
};

@group(0) @binding(0) var<uniform> camera: Camera;

@vertex
fn vs_main(input: VertexInput) -> VertexOutput {
    var output: VertexOutput;
    let world_pos = camera.world * vec4(input.position, 1.0);
    output.clip_position = camera.view_proj * world_pos;
    output.world_normal = mat3x3<f32>(camera.world) * input.normal;
    output.world_position = world_pos.xyz;
    output.tex_coord = input.uv;
    return output;
}
```

**關鍵點**：
- `@location(N)` 對應頂點緩衝區的屬性佈局
- `@builtin(position)` 是 GPU 預設的裁剪空間位置
- `@group(0) @binding(0)` 連接到對應的 BindGroup
- `struct` 用於定義輸入/輸出型別

### 片段著色器完整範例

```wgsl
@group(0) @binding(1) var albedo_texture: texture_2d<f32>;
@group(0) @binding(2) var sampler_: sampler;

@fragment
fn fs_main(input: VertexOutput) -> @location(0) vec4<f32> {
    let albedo = textureSample(albedo_texture, sampler_, input.tex_coord);
    
    // 簡單的光照計算
    let light_dir = normalize(vec3(1.0, 2.0, -1.0));
    let n = normalize(input.world_normal);
    let diff = max(dot(n, light_dir), 0.0);
    
    let base_color = albedo.rgb;
    let ambient = 0.1;
    let final_color = base_color * (ambient + diff);
    
    return vec4(final_color, albedo.a);
}
```

片段著色器返回的 `@location(0)` 對應 `color_attachments[0]`。

### 計算著色器完整範例

```wgsl
@group(0) @binding(0) var<storage, read>  input_data: array<f32>;
@group(0) @binding(1) var<storage, read_write> output_data: array<f32>;

@compute @workgroup_size(256)
fn cs_main(@builtin(global_invocation_id) id: vec3<u32>) {
    let idx = id.x;
    if (idx >= arrayLength(&input_data)) {
        return;
    }
    // 簡單的模糊濾波器
    var sum = input_data[idx] * 0.5;
    if (idx > 0) { sum += input_data[idx - 1] * 0.25; }
    if (idx < arrayLength(&input_data) - 1) { sum += input_data[idx + 1] * 0.25; }
    output_data[idx] = sum;
}
```

### 著色器常數與覆蓋

WGSL 支援著色器常數，允許在管線建立時調整行為：

```wgsl
// 在 WGSL 中定義可覆蓋常數
override enable_normal_mapping: bool = false;
override max_lights: u32 = 4u;
```

在 Rust 端覆蓋：

```rust
let constants = wgpu::ShaderConstants {
    constants: &[
        ("enable_normal_mapping", wgpu::ShaderConstant::Bool(true)),
        ("max_lights", wgpu::ShaderConstant::U32(8)),
    ],
};
let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
    source: wgpu::ShaderSource::Wgsl {
        source: SHADER_SRC.into(),
        constants: &constants,
    },
    ..Default::default()
});
```

這讓同一份著色器程式碼可以根據硬體能力或執行期配置產生不同的變體，而不需要維護多個版本。

### 除錯技巧

**naga** — WGSL 的參考編譯器，提供詳細的錯誤訊息：

```bash
cargo install naga
naga check shader.wgsl
# 輸出：完整的型別檢查和錯誤報告
naga reduce broken.wgsl  # 自動簡化出錯的著色器
```

**Tracy Profiler** — GPU 效能的剖析工具：

```rust
// 在 wgpu 中插入 Tracy 標記
let mut encoder = device.create_command_encoder(&...);
let mut rpass = encoder.begin_render_pass(&...);
rpass.push_debug_group("Shadow Pass");
// ... 渲染陰影 ...
rpass.pop_debug_group();
```

這些標記在 Tracy 中會顯示為巢狀時間軸，幫助定位效能瓶頸。

**Chrome DevTools** — 瀏覽器中的著色器除錯：

- 在 Performance 面板中檢視 GPU 時間線
- 在 Application 面板中檢查 WebGPU 資源
- 使用 `error_scope` 捕捉 GPU 錯誤：

```rust
device.push_error_scope(wgpu::ErrorFilter::Validation);
// ... 可能出錯的操作 ...
device.pop_error_scope().await.unwrap();
// 返回 Option<Error>
```

### 小結

WGSL 是一門年輕但成熟的著色器語言，設計上兼顧了可讀性、安全性和跨平台一致性。它支援三種著色器階段（頂點、片段、計算），透過 `@group/@binding` 與 Rust 端的資源綁定，並提供 `override` 常數用於編譯期配置。

---

**下一步**：[紋理、取樣與材質系統](focus5.md)

## 延伸閱讀

- [WGSL 規範（W3C）](https://www.google.com/search?q=WGSL+WebGPU+shading+language+specification)
- [naga 編譯器文件](https://www.google.com/search?q=naga+WGSL+compiler+tool)
- [Learn WGSL 教學](https://www.google.com/search?q=learn+WGSL+tutorial)
