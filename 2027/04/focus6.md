# 推論引擎最佳化

## 算子融合、記憶體規劃、rayon、CUDA Graph、WebGPU（2018-2026）

### 算子融合（Kernel Fusion）

算子融合是推論引擎中最基本的優化技術。它的核心思想很簡單：**將多個連續的運算合併為單一 kernel，減少記憶體往返和 kernel launch 開銷**。

考慮一個常見的模式：`LayerNorm → ReLU → Linear`。在不融合的情況下：

```
┌───────────┐    ┌───────────┐    ┌───────────┐
│ LayerNorm │ →  │   ReLU    │ →  │  Linear   │
│ 寫入記憶體 │    │ 讀/寫記憶體│    │ 讀取記憶體 │
│ GPU kernel│    │ GPU kernel│    │ GPU kernel│
└───────────┘    └───────────┘    └───────────┘
      ↓ 寫入          ↓ 寫入
     VRAM           VRAM
```

三次 kernel launch + 兩次不必要的記憶體讀寫。融合後：

```
┌──────────────────────────────┐
│ FusedLayerNormReLULinear     │
│ LayerNorm → ReLU → Linear    │
│ 單一 GPU kernel              │
│ 不需要中間寫入                │
└──────────────────────────────┘
      ↓ 寫入 (僅一次)
     VRAM
```

在 Rust 中，算子融合可以透過**模式匹配**自動完成：

```rust
// tract 的算子融合（概念）
fn fuse_ops(graph: &mut Graph) {
    loop {
        let mut fused = false;
        for node in graph.nodes() {
            // 匹配 LayerNorm → ReLU
            if let (Op::LayerNorm(params), Op::Relu) =
                (&node.op, &graph.next(node).op)
            {
                graph.fuse(node, FusedOp::LayerNormRelu(params));
                fused = true;
            }
            // 匹配 ReLU → Linear 等
        }
        if !fused { break; }
    }
}
```

### 記憶體複用與記憶體規劃

在深度學習推理中，記憶體是稀缺資源——特別是在 GPU 和邊緣裝置上。記憶體規劃（memory planning）解決的是：**如何讓多個張量共享同一個記憶體區塊**。

張量的生命週期可以透過**存活區間分析（liveness analysis）**來確定：

```
張量 A:  ████████░░░░░░░░░░░░  (存續時間 [0, 8))
張量 B:  ░░████░░░░░░░░░░░░░░  (存續時間 [2, 6))
張量 C:  ░░░░████████░░░░░░░░  (存續時間 [4, 12))
張量 D:  ░░░░░░░░██████████░░  (存續時間 [8, 18))
────────────────────────────
記憶體槽 0: A (0-8) → D (8-18)
記憶體槽 1: B (2-6) → C (4-12)  (碰撞！需新槽)
```

這本質上是一個**區間著色問題**——每個張量是一個區間，不重疊的區間可以共享記憶體。Rust 的實作可以利用 `BTreeMap` 來追蹤存活區間：

```rust
use std::collections::BTreeMap;

struct MemoryPlanner {
    pool: Vec<Vec<u8>>,           // 實體記憶體區塊
    allocations: BTreeMap<usize, AllocInfo>,  // 張量ID → 分配資訊
    free_list: Vec<(usize, usize)>, // (偏移, 大小) — 空閒塊
}

impl MemoryPlanner {
    fn allocate(&mut self, size: usize, lifetime: Range<usize>)
        -> Option<AllocInfo>
    {
        // 最佳適配（best-fit）演算法
        let (idx, offset) = self.free_list.iter()
            .enumerate()
            .filter(|(_, &(_, s))| s >= size)
            .min_by_key(|(_, &(_, s))| s - size)?;
        // ... 分割空閒塊
    }
}
```

Candle 使用 `cuda_malloc_async` 搭配記憶體池來避免頻繁的 cudaMalloc 呼叫。

### 多執行緒推論（rayon）

在 CPU 推理中，利用多核心是關鍵。Rust 的 **rayon** crate 提供了無痛資料並行：

```rust
use rayon::prelude::*;

fn batch_inference(model: &Model, inputs: &[Tensor]) -> Vec<Tensor> {
    inputs.par_iter()  // 自動分配到所有 CPU 核心
        .map(|input| {
            model.forward(input)
        })
        .collect()
}
```

對於單一輸入的內部並行化——例如矩陣乘法的分塊——rayon 也能勝任：

```rust
fn matmul_parallel(a: &[f32], b: &[f32], m: usize, n: usize, k: usize)
    -> Vec<f32>
{
    let mut c = vec![0.0f32; m * n];
    c.par_chunks_mut(n).enumerate().for_each(|(i, row)| {
        for j in 0..n {
            for l in 0..k {
                row[j] += a[i * k + l] * b[l * n + j];
            }
        }
    });
    c
}
```

### CUDA Graph

CUDA Graph 是 NVIDIA 在 CUDA 10 中引入的功能。傳統的 GPU 推理流程是：

```
CPU: submit kernel A → submit kernel B → submit kernel C → ...
GPU: [launch A] [launch B] [launch C] [launch D]
```

每次 kernel launch 都有 ~5-10μs 的開銷。對於有小算子疊加（如 Transformer 的 attention 計算）的模型，這個開銷很可觀。

CUDA Graph 的解決方案是：

```
階段 1 (capture): CPU 記錄所有 kernel launch
階段 2 (replay):   GPU 直接執行完整的 kernel 序列
```

```rust
// Candle 風格的 CUDA graph 使用（概念）
fn capture_and_replay(device: &CudaDevice, model: &dyn CudaGraphCompatible) {
    // 1. 啟動 capture
    let mut graph = device.graph_capture_begin();
    
    // 2. 執行一次前向（所有 kernel launch 被記錄）
    model.forward_cuda(&graph);
    
    // 3. 結束 capture
    let exec = graph.end_capture_and_instantiate();
    
    // 4. 後續推論：直接 replay，不需要 CPU 介入
    for _ in 0..1000 {
        exec.replay().unwrap();
    }
}
```

CUDA Graph 在推論場景中可以減少 30-50% 的 launch 開銷。

### WebGPU 計算著色器

Burn 的 WebGPU 後端讓 AI 模型可以在瀏覽器中執行。關鍵在於**計算著色器（compute shader）**：

```wgsl
// WebGPU 計算著色器：矩陣乘法（分塊版本）
@compute @workgroup_size(16, 16)
fn matmul_kernel(
    @builtin(global_invocation_id) id: vec3<u32>,
    @group(0) @binding(0) var<storage, read>  a: array<f32>,
    @group(0) @binding(1) var<storage, read>  b: array<f32>,
    @group(0) @binding(2) var<storage, read_write> c: array<f32>,
) {
    let M = 1024u; let K = 1024u; let N = 1024u;
    let row = id.y;
    let col = id.x;
    var sum = 0.0f;
    for (var k = 0u; k < K; k++) {
        sum += a[row * K + k] * b[k * N + col];
    }
    c[row * N + col] = sum;
}
```

WebGPU 的優勢是跨平台（Windows/macOS/Linux/Android/iOS/瀏覽器）且不需要安裝 CUDA 或驅動程式。挑戰是目前 GPU 的計算著色器效能仍落後於原生 CUDA 約 30-50%。

---

**下一步**：[AI 輔助 AI 框架開發](focus7.md)

## 延伸閱讀

- [Kernel fusion in deep learning](https://www.google.com/search?q=kernel+fusion+operator+deep+learning+optimization)
- [Memory planning for neural networks](https://www.google.com/search?q=memory+planning+neural+network+inference)
- [Rayon data parallelism in Rust](https://www.google.com/search?q=rayon+Rust+data+parallelism)
- [CUDA Graph optimization](https://www.google.com/search?q=CUDA+graph+capture+replay+deep+learning)
- [WebGPU compute shader for ML inference](https://www.google.com/search?q=WebGPU+compute+shader+ML+inference)
