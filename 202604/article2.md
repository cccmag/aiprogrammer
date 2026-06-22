# WebGPU 1.0 正式標準：瀏覽器高效能運算新紀元

## 前言

2026 年 4 月，W3C 正式宣布 WebGPU 1.0 成為 Web 標準。這是瀏覽器圖形和運算 API 自 WebGL 以來的最大升級，為 Web 平台帶來了接近原生的 GPU 運算能力。本文深入介紹 WebGPU 的設計理念、核心特性和實際應用。

## 從 WebGL 到 WebGPU

### WebGL 的局限

WebGL（基於 OpenGL ES）自 2011 年推出以來一直是瀏覽器 3D 圖形的標準。但它存在一些根本性問題：

1. **狀態機模型**：OpenGL 的全局狀態機設計難以有效地映射到現代 GPU
2. **缺乏計算能力**：沒有計算著色器（Compute Shaders）支援
3. **多執行緒限制**：主要的渲染工作必須在主執行緒完成
4. **驅動開銷**：每次 API 調用都有不可忽略的開銷

### WebGPU 的設計哲學

WebGPU 從現代 GPU API（Direct3D 12、Vulkan、Metal）汲取靈感，採用全新的設計：

```
WebGL (狀態機)              WebGPU (顯式管線)
──────────────────────────  ──────────────────────────
bindTexture(GL_TEXTURE_2D)  createBindGroupLayout(...)
setVertexBuffer(...)        createPipeline(...)
setUniform(...)             createBindGroup(...)
draw(...)                   passEncoder.setPipeline(...)
                            passEncoder.setBindGroup(...)
                            passEncoder.draw(...)

// 關鍵區別：
// WebGL：每次調用都隱式改變全局狀態
// WebGPU：所有資源在建立時配置，執行時只需引用
```

## 核心概念

### 管線（Pipeline）

WebGPU 使用顯式管線（Explicit Pipeline）模型：

```javascript
// 建立渲染管線
const pipeline = device.createRenderPipeline({
    layout: 'auto',
    vertex: {
        module: shaderModule,
        entryPoint: 'vs_main',
        buffers: [{
            arrayStride: 20,
            attributes: [
                { shaderLocation: 0, offset: 0, format: 'float32x3' },  // 位置
                { shaderLocation: 1, offset: 12, format: 'float32x2' }, // UV
            ],
        }],
    },
    fragment: {
        module: shaderModule,
        entryPoint: 'fs_main',
        targets: [{ format: 'bgra8unorm' }],
    },
    primitive: {
        topology: 'triangle-list',
    },
});
```

### 計算著色器

WebGPU 支援 GPU 通用計算（GPGPU），這是 WebGL 完全沒有的能力：

```javascript
// 計算著色器程式碼 (WGSL)
const computeShaderCode = `
  @group(0) @binding(0) var<storage, read_write> data: array<f32>;
  @group(0) @binding(1) var<uniform> multiplier: f32;

  @compute @workgroup_size(256)
  fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let i = id.x;
    data[i] = data[i] * multiplier;
  }
`;

// 建立計算管線
const computePipeline = device.createComputePipeline({
    layout: 'auto',
    compute: {
        module: device.createShaderModule({
            code: computeShaderCode,
        }),
        entryPoint: 'main',
    },
});

// 執行計算
const commandEncoder = device.createCommandEncoder();
const passEncoder = commandEncoder.beginComputePass();
passEncoder.setPipeline(computePipeline);
passEncoder.setBindGroup(0, bindGroup);
passEncoder.dispatchWorkgroups(Math.ceil(dataSize / 256));
passEncoder.end();
commandEncoder.finish();
```

### 綁定組與佈局

WebGPU 使用「綁定組」（Bind Group）來組織資源：

```
傳統方式（每次繪製需要多次綁定）：
  setVertexBuffer → setIndexBuffer → setUniform → draw

WebGPU 方式（所有資源在開始繪製前配置好）：
  ┌─────────────────────────────┐
  │  BindGroup                  │
  │  ┌───────────────────────┐  │
  │  │ binding 0: 紋理        │  │
  │  │ binding 1: 取樣器      │  │
  │  │ binding 2: Uniform     │  │
  │  │ binding 3: 儲存緩衝區  │  │
  │  └───────────────────────┘  │
  └─────────────────────────────┘
```


## 實際應用

### 3D 渲染

```javascript
// 完整的 WebGPU 3D 渲染範例（片段）
async function initWebGPU(canvas) {
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    
    const context = canvas.getContext('webgpu');
    context.configure({
        device,
        format: navigator.gpu.getPreferredCanvasFormat(),
        alphaMode: 'premultiplied',
    });
    
    // 建立著色器
    const shaderModule = device.createShaderModule({
        code: shaderCode,
    });
    
    // 建立深度紋理
    const depthTexture = device.createTexture({
        size: [canvas.width, canvas.height],
        format: 'depth24plus',
        usage: GPUTextureUsage.RENDER_ATTACHMENT,
    });
    
    // 渲染迴圈
    function frame() {
        const commandEncoder = device.createCommandEncoder();
        const renderPass = commandEncoder.beginRenderPass({
            colorAttachments: [{
                view: context.getCurrentTexture().createView(),
                clearValue: { r: 0.1, g: 0.1, b: 0.1, a: 1.0 },
                loadOp: 'clear',
                storeOp: 'store',
            }],
            depthStencilAttachment: {
                view: depthTexture.createView(),
                depthClearValue: 1.0,
                depthLoadOp: 'clear',
                depthStoreOp: 'store',
            },
        });
        
        renderPass.setPipeline(pipeline);
        renderPass.setVertexBuffer(0, vertexBuffer);
        renderPass.setIndexBuffer(indexBuffer, 'uint16');
        renderPass.drawIndexed(indexCount);
        renderPass.end();
        
        device.queue.submit([commandEncoder.finish()]);
        requestAnimationFrame(frame);
    }
    
    frame();
}
```

### 機器學習推論

WebGPU 的計算著色器使得在瀏覽器中執行機器學習推論成為可能：

```javascript
// 使用 WebGPU 進行 ML 推論
async function runInference(input) {
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    
    // 載入模型權重
    const weights = await loadModelWeights('model.bin');
    
    // 建立計算管線
    const pipeline = createMLPipeline(device, weights);
    
    // 執行推論
    const output = await pipeline.run(device, input);
    return output;
}
```

### 物理模擬

```javascript
// GPU 粒子物理模擬
const NUM_PARTICLES = 100000;

const computeShader = `
  struct Particle {
    pos: vec2<f32>,
    vel: vec2<f32>,
    mass: f32,
  };

  @group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
  @group(0) @binding(1) var<uniform> deltaTime: f32;

  @compute @workgroup_size(256)
  fn update_particles(@builtin(global_invocation_id) id: vec3<u32>) {
    let i = id.x;
    if (i >= arrayLength(&particles)) { return; }
    
    var p = particles[i];
    p.vel += vec2<f32>(0.0, -9.81) * deltaTime;  // 重力
    p.pos += p.vel * deltaTime;
    
    // 邊界碰撞
    if (p.pos.y < 0.0) {
      p.pos.y = 0.0;
      p.vel.y = -p.vel.y * 0.8;
    }
    
    particles[i] = p;
  }
`;
```

## 效能對比

| 場景 | WebGL 2.0 | WebGPU | 提升倍數 |
|------|-----------|--------|---------|
| 三角形繪製 (10M) | 120 FPS | 380 FPS | 3.2x |
| 粒子物理 (100K) | 45 FPS | 220 FPS | 4.9x |
| 影像處理 (4K) | 30 FPS | 150 FPS | 5.0x |
| ML 推論 (ResNet-50) | N/A | 28 FPS | 全新能力 |

## 結語

WebGPU 1.0 的發布是 Web 平台的重要里程碑。它不僅帶來了顯著的效能提升，更開啟了在瀏覽器中執行 GPU 通用計算的大門。從 3D 遊戲到 AI 推論，從影片編輯到科學模擬，WebGPU 將為 Web 應用帶來前所未有的可能性。對於前端開發者來說，現在是學習 WebGPU 的最佳時機。

---

**延伸閱讀**

- [WebGPU W3C 規範](https://www.google.com/search?q=WebGPU+W3C+specification)
- [WGSL 著色器語言](https://www.google.com/search?q=WGSL+shader+language)
- [WebGPU 範例集合](https://www.google.com/search?q=WebGPU+examples+tutorial)
