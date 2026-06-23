# Burn 深度學習框架 — 可組合後端設計、WGPU GPU 推論

## 1. 引言

Burn 是 Rust 生態中最具野心的深度學習框架。與 Candle 的「輕量極簡」和 tract 的「ONNX 專注」不同，Burn 追求的是**可組合的後端抽象**——同一份模型程式碼可以在 CPU、GPU、甚至瀏覽器中無縫執行。

## 2. 後端抽象設計

Burn 的核心是 `Backend` trait：

```rust
pub trait Backend: Clone + Send + Sync + Debug {
    type TensorPrimitive<const D: usize>: ...;
    type FloatElem: FloatElement;
    type IntElem: IntElement;
    fn ad_enabled() -> bool { false }
    fn name() -> &'static str;
}
```

框架提供了多種後端實作：

```rust
use burn::backend::{
    NdArrayBackend,    // CPU 純 Rust
    WgpuBackend,       // GPU (Vulkan/Metal/DX12)
    CudaBackend,       // NVIDIA CUDA
    LibTorchBackend,   // LibTorch 橋接
    TokioBackend,      // 非同步批次處理
};
```

## 3. 模型定義

Burn 透過 `#[derive(Module)]` 和結構體來定義模型：

```rust
use burn::{
    prelude::*,
    nn::{
        conv::Conv2d,
        pooling::AdaptiveAvgPool2d,
        Linear, Dropout,
    },
};

#[derive(Module, Debug)]
pub struct CNN<B: Backend> {
    conv1: Conv2d<B>,
    conv2: Conv2d<B>,
    pool: AdaptiveAvgPool2d,
    fc1: Linear<B>,
    fc2: Linear<B>,
    dropout: Dropout,
    activation: Relu,
}

impl<B: Backend> CNN<B> {
    pub fn forward(&self, input: Tensor<B, 4>) -> Tensor<B, 2> {
        let x = self.conv1.forward(input);
        let x = self.activation.forward(x);
        let x = self.conv2.forward(x);
        let x = self.activation.forward(x);
        let x = self.pool.forward(x);
        let x = x.flatten(1, 3);
        let x = self.fc1.forward(x);
        let x = self.activation.forward(x);
        let x = self.dropout.forward(x, true);
        self.fc2.forward(x)
    }
}
```

## 4. 訓練與推論

Burn 支援完整的訓練流程：

```rust
use burn::{
    prelude::*,
    train::{
        LearnerBuilder,
        metric::AccuracyMetric,
    },
    optim::Adam,
    data::dataloader::DataLoaderBuilder,
};

#[derive(Config)]
pub struct TrainingConfig {
    pub num_epochs: usize,
    pub batch_size: usize,
    pub learning_rate: f64,
}

pub fn train<B: Backend>(config: TrainingConfig) {
    let device = B::Device::default();

    let model = CNN::<B>::new(&CNNConfig::new(10, 3), &device);
    let optim = Adam::new(&model, config.learning_rate.into());

    let learner = LearnerBuilder::new("model")
        .epochs(config.num_epochs)
        .batch_size(config.batch_size)
        .metric(AccuracyMetric::new())
        .build(model, optim, config.loss_fn());

    // 訓練
    let trained = learner.fit(train_data, test_data);
}
```

## 5. WGPU GPU 推論

WGPU 是 Burn 最重要的後端，基於 WebGPU 標準：

```rust
use burn::backend::WgpuBackend;
use burn::backend::wgpu::{WgpuDevice, GraphicsApi};

// 自動選擇裝置
let device = WgpuDevice::default();

// 或明確指定
let device = WgpuDevice::DiscreteGpu(0); // 第一張獨立 GPU

// 建立模型並移動到 GPU
let model = CNN::<WgpuBackend>::new(&config, &device);
let input = Tensor::<WgpuBackend, 4>::from_data(raw_data)
    .to_device(&device);

// GPU 推論
let output = model.forward(input);
```

WGPU 的跨平台能力：

| 平台 | API | 支援 |
|------|-----|------|
| Windows | Vulkan/DX12 | ✅ |
| Linux | Vulkan | ✅ |
| macOS | Metal | ✅ |
| iOS | Metal | ✅ |
| Android | Vulkan | ✅ |
| 瀏覽器 | WebGPU | ✅ |

## 6. 瀏覽器內推論

Burn + WebGPU 讓 Rust ML 可以直接在瀏覽器中執行：

```rust
// 編譯為 Wasm
#[wasm_bindgen]
pub fn predict(input: &[f32]) -> Vec<f32> {
    let device = WgpuDevice::default();
    let model = load_model(&device);
    let tensor = Tensor::<WgpuBackend, 2>::from_data(input.to_vec())
        .to_device(&device);
    let output = model.forward(tensor);
    output.to_data().value
}
```

## 7. Burn 的生態定位

| 比較維度 | Burn | Candle | tract |
|---------|------|--------|-------|
| 訓練 | 完整支援 | 有限 | 無 |
| 後端抽象 | 核心設計 | 固定 | 固定 |
| GPU 選項 | WGPU/CUDA/LibTorch | Metal/CUDA | 有限 |
| 瀏覽器 | WebGPU | Wasm | Wasm |
| 學習曲線 | 較陡 | 平緩 | 中等 |
| 自訂算子 | 需要 Backend trait | Custom Kernel API | ONNX 算子 |

## 8. 結語

Burn 是 Rust ML 框架中最靈活的選擇。它的後端抽象設計讓開發者可以用同一份程式碼涵蓋 CPU 推論、GPU 加速、行動裝置和瀏覽器。對於需要跨平台部署或完整訓練支援的專案，Burn 提供了無可比擬的靈活性。

## 延伸閱讀

- [Burn book](https://www.google.com/search?q=Burn+deep+learning+Rust+book)
- [Burn WGPU backend](https://www.google.com/search?q=Burn+WGPU+backend+setup)
- [Burn web assembly](https://www.google.com/search?q=Burn+WebAssembly+WebGPU)
