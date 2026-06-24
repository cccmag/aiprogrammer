# Rust ML 生態總覽

## Candle/Burn/tract, 何時用 Rust vs Python（2021-2026）

### 前言

Rust 的 ML 推論生態在 2021–2026 年間從零到一快速成長。三大框架——Candle、Burn、tract——各自佔據了不同的生態位。本主題概述它們的定位與選擇基準。

### 三大框架一覽

| 框架 | 發布 | 維護者 | 核心設計 | 主要場景 |
|------|------|--------|---------|---------|
| Candle | 2023 | Hugging Face | 最小依賴、純 Rust | 輕量部署、嵌入式 |
| Burn | 2022 | 社群驅動 | 可組合後端 | 跨平台 GPU/CPU 推論 |
| tract | 2021 | Sonos | ONNX 原生引擎 | 模型互通、生產部署 |

### Candle：輕量極簡

Candle 的目標是最小化依賴。不需要 CUDA、cuDNN 或任何 C++ 函式庫，只需要 Rust 編譯器：

```rust
use candle_core::{Device, Tensor};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;
    let a = Tensor::new(&[[1.0f32, 2.0], [3.0, 4.0]], &device)?;
    let b = Tensor::new(&[[5.0f32, 6.0], [7.0, 8.0]], &device)?;
    let c = a.matmul(&b)?;
    println!("{c:?}");
    Ok(())
}
```

Candle 的程式碼風格接近 PyTorch，但不需要 Python 執行期。這使得 Candle 非常適合容器化部署和嵌入式場景。

### Burn：可組合後端

Burn 的創新在於後端抽象設計。它定義了統一的 `Backend` trait：

```rust
use burn::tensor::{Tensor, backend::Backend};

fn forward<B: Backend>(input: Tensor<B, 2>) -> Tensor<B, 2> {
    input.matmul(input.clone()) + 0.5
}
```

同一個程式碼可以無縫切換到不同的後端：
- `NdArrayBackend` — CPU 純 Rust
- `WgpuBackend` — GPU（Vulkan/Metal/DX12）
- `CudaBackend` — NVIDIA GPU
- `TokioBackend` — 非同步批次處理

### tract：ONNX 互通

tract 直接讀取 ONNX 格式，不需要中間轉換：

```rust
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    let model = onnx()
        .model_for_path("model.onnx")?
        .with_input_fact(0, InferenceFact::dt_shape(f32::datum_type(), tvec!(1, 3, 224, 224)))?
        .into_optimized()?
        .into_runnable()?;

    let result = model.run(tvec!(Tensor::from(raw_input)))?;
    Ok(())
}
```

tract 的 ONNX 原生支援意味著任何可以匯出 ONNX 的框架（PyTorch、TensorFlow、Scikit-learn）都可以直接用在 Rust 中。

### 何時用 Rust vs Python

| 場景 | 建議語言 | 原因 |
|------|---------|------|
| 模型訓練 | Python | PyTorch 生態無法取代 |
| 研究與實驗 | Python | Jupyter/interactive 開發 |
| 伺服器推論 | Rust | 低延遲、高吞吐、安全 |
| 邊緣裝置 | Rust | 交叉編譯、無執行期 |
| 嵌入式 MCU | Rust | no_std 支援 |
| 瀏覽器推論 | Rust→Wasm | WebGPU/Burn |
| 快速原型 | Python | 開發速度優先 |

### 小結

Rust ML 生態已從「能不能用」發展到「好不好用」。選擇框架的關鍵在於部署目標：邊緣嵌入式選 Candle、跨平台 GPU 選 Burn、ONNX 互通選 tract。

---

**下一步**：[Candle 框架](focus2.md)

## 延伸閱讀

- [Candle framework](https://www.google.com/search?q=Candle+ML+framework+Rust)
- [Burn deep learning](https://www.google.com/search?q=Burn+deep+learning+Rust)
- [tract ONNX](https://www.google.com/search?q=tract+ONNX+Rust)
- [Rust ML ecosystem 2026](https://www.google.com/search?q=Rust+machine+learning+ecosystem+2026)
