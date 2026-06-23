# Rust ML 生態入門 — Candle/Burn/tract 框架定位與選擇

## 1. 引言

機器學習模型的訓練由 Python 主宰已是業界共識。但模型的**部署推論**（Inference）是截然不同的場景——它需要低延遲、小體積、高吞吐，並且經常需要在沒有 GPU 的邊緣設備上運行。Rust ML 生態在 2021–2026 年間快速成熟，形成了以 Candle、Burn、tract 三大框架為核心的推論生態。

本文從宏觀角度比較這三大框架，幫助讀者根據實際需求選擇合適的工具。

## 2. 三大框架的定位

### Candle：輕量極簡

由 Hugging Face 於 2023 年發布。核心理念是「最小依賴」——不需要任何 C++ 函式庫。

**適合場景**：
- 嵌入式/邊緣裝置（交叉編譯友善）
- Docker 容器部署（減小映像大小）
- 需要從 Hugging Face Hub 直接載入模型
- 快速原型開發（API 風格接近 PyTorch）

**不適合**：
- 需要完整訓練支援
- 複雜的動態計算圖

### Burn：可組合後端

社群驅動的深度學習框架，2022 年誕生。Burn 的設計圍繞 `Backend` trait 展開。

**適合場景**：
- 跨平台部署（同一程式碼在不同硬體上執行）
- 需要 GPU 加速但不使用 CUDA（macOS/行動裝置）
- 瀏覽器內 ML 推論（WebGPU）
- 需要訓練+部署的完整工作流程

**不適合**：
- 最簡單的「載入→推論」場景（Burn 的抽象層次較高）

### tract：ONNX 原生引擎

由 Sonos 開發，2021 年發布。tract 不做通用 ML 框架，而是專注 ONNX 格式。

**適合場景**：
- 已有 ONNX 格式的模型
- 企業級生產部署
- 需要模型互通性（PyTorch → ONNX → tract）
- 音訊/訊號處理管線

**不適合**：
- 需要自訂模型架構訓練
- 非 ONNX 生態的模型

## 3. Hello World 比較

### Candle 版本

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

### Burn 版本

```rust
use burn::tensor::{Tensor, backend::NdArrayBackend};

fn main() {
    type Backend = NdArrayBackend<f32>;
    let a = Tensor::<Backend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]]);
    let b = Tensor::<Backend, 2>::from_data([[5.0, 6.0], [7.0, 8.0]]);
    let c = a.matmul(b);
    println!("{c:?}");
}
```

### tract 版本

```rust
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    let model = onnx()
        .model_for_path("model.onnx")?
        .with_input_fact(0, InferenceFact::dt_shape(
            f32::datum_type(), tvec!(1, 784)
        ))?
        .into_optimized()?
        .into_runnable()?;

    let input = Tensor::from_shape(&[1, 784])?;
    let output = model.run(tvec!(input))?;
    println!("{:?}", output);
    Ok(())
}
```

## 4. 效能比較

| 指標 | Candle | Burn (NdArray) | Burn (WGPU) | tract |
|------|--------|---------------|-------------|-------|
| 啟動時間 | ~5µs | ~50µs | ~5ms | ~10µs |
| CPU 推論 | 快 | 中 | N/A | 快 |
| GPU 推論 | Metal/CUDA | N/A | Vulkan/Metal/DX12 | 有限 |
| 二進位大小 | ~5MB | ~8MB | ~15MB | ~2MB |
| 外部依賴 | 無 | 無 | WGPU 原生庫 | 無 |

## 5. 選擇指南

```
需要 ONNX 互通？ → tract
需要 GPU 跨平台？ → Burn (WGPU)
需要極小體積？ → Candle 或 tract
需要瀏覽器中執行？ → Burn (WebGPU)
需要訓練+部署？ → Burn
最簡單的開始？ → Candle
```

## 6. 學習資源

- **Candle**：官方範例庫（GitHub）+ Hugging Face 文件
- **Burn**：Burn Book + 官方範例
- **tract**：官方文件 + 社群教學

## 7. 結語

Rust ML 推論生態已經成熟到可以支援生產級部署。三大框架各有優勢，選擇時應考慮部署目標、硬體限制和既有模型格式。如果還有疑慮，從 Candle 開始是最安全的選擇——它的學習曲線最平緩，且遷移到其他框架的成本很低。

## 延伸閱讀

- [Candle vs Burn vs tract](https://www.google.com/search?q=Candle+Burn+tract+Rust+ML+comparison)
- [Rust ML frameworks overview](https://www.google.com/search?q=Rust+machine+learning+frameworks+2026+overview)
- [Choosing Rust ML framework](https://www.google.com/search?q=how+to+choose+Rust+ML+framework+deployment)
