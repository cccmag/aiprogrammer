# tract ONNX 推論引擎 — ONNX 格式、載入執行、最佳化

## 1. 引言

ONNX（Open Neural Network Exchange）已成為 ML 模型互通的事實標準。tract 是純 Rust 的 ONNX 推論引擎，由 Sonos 開發並開源。本文深入探討 ONNX 格式規範、tract 的載入執行機制、最佳化技術與量化推論。

## 2. ONNX 格式深入

ONNX 使用 Protocol Buffers 序列化模型：

```protobuf
// ONNX 核心定義（簡化）
message ModelProto {
    int64 ir_version = 1;
    OperatorSetIdProto[] opset_import = 2;
    string producer_name = 3;
    GraphProto graph = 4;
}

message GraphProto {
    ValueInfoProto[] input = 1;     // 輸入定義
    ValueInfoProto[] output = 2;    // 輸出定義
    NodeProto[] node = 3;           // 計算節點
    TensorProto[] initializer = 4;  // 常數權重
    string name = 5;
}

message NodeProto {
    string[] input = 1;             // 輸入名稱
    string[] output = 2;            // 輸出名稱
    string op_type = 3;             // 算子類型 (Conv, Relu...)
    string domain = 4;
    AttributeProto[] attribute = 5; // 算子屬性
}
```

從 PyTorch 匯出 ONNX：

```python
import torch
import torch.onnx

model = torch.load("model.pth")
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}},
    opset_version=19,
)
```

## 3. tract 載入與執行

tract 的載入流程分為四個階段：

```rust
use tract_onnx::prelude::*;

fn tract_pipeline() -> TractResult<()> {
    // Phase 1: 載入 ONNX 模型
    let model = onnx()
        .model_for_path("model.onnx")?;

    // Phase 2: 宣告輸入規格
    let model = model
        .with_input_fact(0, InferenceFact::dt_shape(
            f32::datum_type(),
            tvec!(1, 3, 224, 224)
        ))?
        .with_output_fact(0, InferenceFact::dt_shape(
            f32::datum_type(),
            tvec!(1, 1000)
        ))?;

    // Phase 3: 分析與最佳化
    let model = model
        .into_optimized()?;  // 常數摺疊 + 節點融合 + 形狀推導

    // Phase 4: 編譯為可執行引擎
    let engine = model
        .into_runnable()?;  // 記憶體規劃 + 執行排程

    // 執行推論
    let input = Tensor::from_shape(&[1, 3, 224, 224])?;
    let result = engine.run(tvec!(input))?;
    Ok(())
}
```

## 4. 模型最佳化

tract 的最佳化管道包含多個階段：

```rust
// 手動控制最佳化選項
use tract_onnx::optim::OptimConfig;

let model = onnx()
    .model_for_path("model.onnx")?
    .with_optim_config(OptimConfig {
        enable_folding: true,       // 常數摺疊
        enable_fusion: true,        // 算子融合
        enable_quantization: true,  // 量化最佳化
        enable_memory_planning: true, // 記憶體規劃
        ..Default::default()
    })?
    .into_optimized()?;
```

常見的算子融合：

```
原始計算圖：
  Conv → BatchNorm → Relu → MaxPool

融合後：
  ConvFusedBNRelu → MaxPool

效益：減少記憶體讀寫次數 2-3 倍
```

## 5. 量化推論

tract 支援 ONNX 標準的量化模型：

```rust
fn quantized_inference() -> TractResult<()> {
    // 載入量化後的 ONNX 模型
    let model = onnx()
        .model_for_path("model.quant.onnx")?
        .with_input_fact(0, InferenceFact::dt_shape(
            u8::datum_type(), tvec!(1, 3, 224, 224)
        ))?
        .into_optimized()?
        .into_runnable()?;

    // INT8 輸入資料
    let input_data: Vec<u8> = preprocess_image_uint8("image.jpg");
    let input = Tensor::from_shape(&[1, 3, 224, 224])?
        .into_tensor();
    // 填入 input_data...

    let result = model.run(tvec!(input))?;
    Ok(())
}
```

## 6. 生產部署

tract 在生產環境中的常見配置：

```rust
use std::sync::Arc;
use tract_onnx::prelude::*;

pub struct ModelServer {
    engine: Arc<SimpleTract>,
}

impl ModelServer {
    pub fn load(path: &str) -> TractResult<Self> {
        let engine = onnx()
            .model_for_path(path)?
            .with_input_fact(0, InferenceFact::dt_shape(
                f32::datum_type(), tvec!(None, 3, 224, 224)  // 動態批次
            ))?
            .into_optimized()?
            .into_runnable()?;
        Ok(Self { engine: Arc::new(engine) })
    }

    pub fn infer(&self, input: Tensor) -> TractResult<Tensor> {
        let result = self.engine.run(tvec!(input))?;
        Ok(result[0].clone())
    }
}
```

## 7. 效能數據

| 模型 | 框架 | 推論時間 (CPU) | 模型大小 |
|------|------|---------------|---------|
| MobileNetV2 | tract | 12ms | 14MB |
| MobileNetV2 | Candle | 14ms | 14MB |
| ResNet-50 | tract | 85ms | 98MB |
| ResNet-50 | Candle | 95ms | 98MB |
| MobileNetV2 INT8 | tract | 5ms | 3.8MB |

## 8. 結語

tract 是 ONNX 推論的最成熟 Rust 解決方案。對於已有 ONNX 格式模型的團隊，tract 提供了一條順暢的 Rust 部署路徑。它的最佳化管道可以自動提升執行效率，而 INT8 量化支援讓邊緣部署成為可能。

## 延伸閱讀

- [tract ONNX optimization](https://www.google.com/search?q=tract+ONNX+optimization+Rust)
- [ONNX format specification](https://www.google.com/search?q=ONNX+format+specification+Protocol+Buffers)
- [PyTorch to ONNX export](https://www.google.com/search?q=PyTorch+export+ONNX+model)
