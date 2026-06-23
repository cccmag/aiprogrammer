# Burn 深度學習框架

## 可組合後端, WGPU, 自訂模型（2023-2026）

### 前言

Burn 是 2022 年誕生的 Rust 深度學習框架，與 Candle 不同，Burn 的設計目標是「可組合的後端抽象」——讓同一個模型程式碼可以在 CPU、GPU、甚至瀏覽器中運行。

### 後端抽象設計

Burn 的核心是 `Backend` trait：

```rust
pub trait Backend: Clone + Send + Sync + Debug {
    type TensorPrimitive<const D: usize>: ...;
    type FloatElem: FloatElement;
    type IntElem: IntElement;
    fn name() -> &'static str;
    // ...
}
```

任何實作 `Backend` 的型別都可以作為 Burn 的計算後端：

```rust
use burn::backend::{NdArrayBackend, WgpuBackend};
use burn::tensor::Tensor;

// CPU 推論
type CpuBackend = NdArrayBackend<f32>;
let tensor_1 = Tensor::<CpuBackend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]]);

// WGPU GPU 推論（同一行程式碼！）
type GpuBackend = WgpuBackend;
let tensor_2 = Tensor::<GpuBackend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]]);
```

### 自訂模型

Burn 透過派生宏和 trait 來定義模型：

```rust
use burn::{
    prelude::*,
    nn::{Linear, LinearConfig, Relu},
};

#[derive(Module, Debug)]
pub struct Mlp<B: Backend> {
    fc1: Linear<B>,
    fc2: Linear<B>,
    activation: Relu,
}

impl<B: Backend> Mlp<B> {
    pub fn forward(&self, input: Tensor<B, 2>) -> Tensor<B, 2> {
        let x = self.fc1.forward(input);
        let x = self.activation.forward(x);
        self.fc2.forward(x)
    }
}
```

### WGPU 後端

WGPU 是 Burn 最重要的後端之一，基於 WebGPU 標準：

```rust
use burn::backend::WgpuBackend;
use burn::backend::wgpu::WgpuDevice;

// 自動選擇 GPU
let device = WgpuDevice::default();

// 或指定特定裝置
let device = WgpuDevice::DiscreteGpu(0); // 獨立 GPU
let device = WgpuDevice::IntegratedGpu(0); // 內顯
let device = WgpuDevice::VirtualGpu(0); // 虛擬 GPU
```

WGPU 後端支援：
- Vulkan（Windows/Linux/Android）
- Metal（macOS/iOS）
- DirectX 12（Windows）
- WebGPU（瀏覽器/Wasm）

### Burn 的獨特優勢

| 特性 | Burn | Candle | tract |
|------|------|--------|-------|
| 訓練支援 | ✅ | 有限 | ❌ |
| GPU 後端 | WGPU/CUDA | Metal/CUDA | 有限 |
| 瀏覽器 | WebGPU | Wasm | Wasm |
| 自訂模型 | ✅ | ✅ | ONNX 限定 |
| 動態圖 | ✅ | 靜態 | 靜態 |

### 小結

Burn 是 Rust ML 框架中最靈活的選擇。如果你需要跨平台 GPU 支援、自訂模型定義、或瀏覽器內推論，Burn 提供了最完整的解決方案。

---

**下一步**：[tract ONNX 推論引擎](focus4.md)

## 延伸閱讀

- [Burn book](https://www.google.com/search?q=Burn+deep+learning+Rust+book)
- [Burn WGPU backend](https://www.google.com/search?q=Burn+WGPU+backend+Rust)
- [Burn vs Candle](https://www.google.com/search?q=Burn+vs+Candle+Rust+ML+framework)
