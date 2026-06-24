# Rust 與 Python ML 協作模式 — PyTorch 訓練→Rust 部署

## 1. 引言

現實世界中的 ML 專案很少只用一種語言。典型的模式是：**Python 負責訓練，Rust 負責部署**。本文探討這種協作模式的完整流程、工具鏈與最佳實務。

## 2. 協作模式總覽

```
Python 訓練階段
  ├── PyTorch 模型定義與訓練
  ├── 權重儲存 (.pth / .safetensors)
  └── ONNX 匯出

      │ 格式轉換 / 模型傳遞
      ▼

Rust 部署階段
  ├── 模型載入 (Candle/Burn/tract)
  ├── 量化 (FP32→INT8)
  ├── 推論管線
  └── 生產部署
```

## 3. 模型匯出

### 方法一：ONNX 匯出

這是最通用的跨語言橋樑：

```python
import torch

# 訓練好的模型
model = MyModel()
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# 匯出為 ONNX
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    opset_version=19,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={
        "input": {0: "batch_size"},
        "output": {0: "batch_size"},
    },
)
```

Rust 端用 tract 載入：

```rust
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    let engine = onnx()
        .model_for_path("model.onnx")?
        .with_input_fact(0, InferenceFact::dt_shape(
            f32::datum_type(), tvec!(1, 3, 224, 224)
        ))?
        .into_optimized()?
        .into_runnable()?;
    Ok(())
}
```

### 方法二：safetensors 直接交換

適用於 Candle 和 Burn：

```python
# Python 端：儲存為 safetensors
from safetensors.torch import save_file

state_dict = model.state_dict()
save_file(state_dict, "model.safetensors")
```

```rust
// Rust 端：載入 safetensors
use candle_core::{Device, Tensor};
use candle_nn::VarBuilder;

let weights = std::fs::read("model.safetensors")?;
let vb = VarBuilder::from_safetensors(
    vec![weights.into()],
    DType::F32,
    &Device::Cpu
)?;
```

## 4. 精度驗證

部署後必須確保 Rust 推論結果與 Python 一致：

```python
# Python 端：產生參考輸出
import numpy as np

test_input = np.random.randn(1, 3, 224, 224).astype(np.float32)
with torch.no_grad():
    reference_output = model(torch.from_numpy(test_input)).numpy()

# 儲存測試資料
np.savez("test_data.npz",
    input=test_input,
    output=reference_output)
```

```rust
// Rust 端：對比輸出
fn validate_precision() -> Result<(), Box<dyn std::error::Error>> {
    // 載入測試資料
    let test_data = ndarray::npz::NpzFile::open("test_data.npz")?;
    let reference: ndarray::ArrayD<f32> = test_data.by_name("output")?;

    // Rust 推論
    let rust_output = model.predict(&test_input)?;

    // 計算誤差
    let mse: f32 = rust_output.iter()
        .zip(reference.iter())
        .map(|(a, b)| (a - b).powi(2))
        .sum::<f32>() / rust_output.len() as f32;

    assert!(mse < 1e-3, "MSE 過大: {}", mse);
    Ok(())
}
```

## 5. CI/CD 整合

將 Rust ML 部署整合到 CI/CD 管線中：

```yaml
# .github/workflows/deploy.yml
name: ML Model Deployment

on:
  push:
    paths:
      - 'model/**'
      - 'rust-inference/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python 驗證
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install torch onnx
          python scripts/export_onnx.py
          python scripts/generate_test_data.py

      - name: Rust 驗證
        run: |
          cd rust-inference
          cargo build --release
          cargo test validate_precision

      - name: 交叉編譯邊緣部署
        run: |
          cd rust-inference
          rustup target add aarch64-unknown-linux-gnu
          cargo build --target aarch64-unknown-linux-gnu --release

      - name: 部署到邊緣裝置
        run: |
          scp target/aarch64/release/inference pi@device:~
          scp model.quant.onnx pi@device:~
```

## 6. 版本管理

ML 模型的版本管理比一般軟體複雜：

```
model-registry/
├── v1.0.0/
│   ├── model.pth           # PyTorch 原始權重
│   ├── model.onnx          # ONNX 格式
│   ├── model.quant.onnx    # 量化版本
│   └── test_data.npz       # 驗證資料
├── v1.1.0/
│   └── ...
└── v2.0.0/
    └── ...
```

Rust 端對應版本號：

```rust
const MODEL_VERSION: &str = "1.1.0";
const MODEL_PATH: &str = "models/v1.1.0/model.quant.onnx";
const EXPECTED_ACCURACY: f32 = 0.95;

fn load_model() -> TractResult<SimpleTract> {
    let engine = onnx()
        .model_for_path(MODEL_PATH)?
        .with_input_fact(/* ... */)?
        .into_optimized()?
        .into_runnable()?;

    // 核對模型版本
    assert_eq!(engine.model_version(), MODEL_VERSION);
    Ok(engine)
}
```

## 7. 實際案例：影像分類服務

一個完整的 Python 訓練 → Rust 部署案例：

| 階段 | 語言 | 工作內容 |
|------|------|---------|
| 資料準備 | Python | 下載 ImageNet、資料擴增 |
| 模型訓練 | Python | ResNet-50 微調 |
| 模型轉換 | Python | ONNX 匯出 + QAT 量化 |
| 部署服務 | Rust | Axum + tract 推論 API |
| 效能監控 | Rust/Tokio | Prometheus 指標 + 延遲追蹤 |

## 8. 結語

Python 訓練 + Rust 部署的協作模式是當前 ML 領域的最佳實務。Python 提供了訓練的靈活性，Rust 提供了部署的效能與安全性。正確的 CI/CD 整合和精度驗證流程是這種協作模式成功的關鍵。

## 延伸閱讀

- [PyTorch to ONNX](https://www.google.com/search?q=PyTorch+export+ONNX+tutorial)
- [Rust Python ML workflow](https://www.google.com/search?q=Rust+Python+machine+learning+workflow)
- [MLOps with Rust](https://www.google.com/search?q=MLOps+Rust+deployment+pipeline)
