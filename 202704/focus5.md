# 模型序列化與部署

## ONNX、INT8 量化、Candle、tract、無 Python 執行期（2016-2026）

### ONNX：模型交換的通用格式

2017 年，Microsoft 和 Facebook 聯合發布了 **ONNX（Open Neural Network Exchange）**。它的目標是成為深度學習模型的「JPEG」——一個可以跨框架交換的通用格式。

ONNX 使用 protobuf（Protocol Buffers）作為序列化格式。一個 ONNX 模型檔案的結構如下：

```
ModelProto
  ├── ir_version: 9         # ONNX 版本
  ├── opset_import: [...]   # 算子版本
  ├── graph: GraphProto
  │   ├── node: [NodeProto]  # 計算圖節點
  │   │   ├── input: ["x", "w1"]
  │   │   ├── output: ["h1"]
  │   │   ├── op_type: "Gemm"  # 通用矩陣乘法
  │   │   └── attribute: [...] # 參數（transA, transB, alpha, beta）
  │   ├── initializer: [TensorProto]  # 權重資料
  │   ├── input: [ValueInfoProto]     # 模型輸入描述
  │   └── output: [ValueInfoProto]    # 模型輸出描述
  └── metadata_props: [...]  # 中繼資料（框架、作者等）
```

在 Rust 中解析 ONNX 需要 protobuf 綁定。`tract` 框架使用 `prost` crate 生成 ONNX 的 Rust 型別：

```rust
// tract 的 ONNX 載入流程（簡化）
use prost::Message;

fn load_onnx(path: &str) -> Result<InferenceModel, TractError> {
    let bytes = std::fs::read(path)?;
    let onnx_model = onnx::ModelProto::decode(bytes.as_slice())?;
    
    // 遍歷計算圖節點，轉換為 tract 的內部表示
    for node in &onnx_model.graph.as_ref().unwrap().node {
        let op = match node.op_type.as_str() {
            "Gemm" => parse_gemm(node)?,
            "Relu" => Op::Relu,
            "Conv" => parse_conv(node)?,
            // ...
            other => bail!("Unsupported op: {}", other),
        };
        model.add_op(op, &node.input, &node.output);
    }
    Ok(model)
}
```

ONNX 的挑戰在於**算子版本的碎片化**。不同框架導出的 ONNX 可能使用不同的算子版本（opset），導致相容性問題。

### 量化技術

量化（quantization）是減少模型大小的關鍵技術，對於邊緣部署至關重要。

**INT8 量化**：將 FP32 權重映射到 INT8 範圍 [-128, 127]：

```rust
struct QuantizedTensor {
    data: Vec<i8>,        // INT8 資料
    scale: f32,           // 縮放因子
    zero_point: i8,       // 零點
}

impl QuantizedTensor {
    // 量化：FP32 → INT8
    fn quantize(fp32: &[f32]) -> Self {
        let max_val = fp32.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
        let scale = max_val / 127.0;
        let data: Vec<i8> = fp32.iter()
            .map(|v| (v / scale).round().clamp(-128.0, 127.0) as i8)
            .collect();
        QuantizedTensor { data, scale, zero_point: 0 }
    }

    // 反量化：INT8 → FP32（運算時隱式進行）
    fn dequantize(&self) -> Vec<f32> {
        self.data.iter()
            .map(|&v| (v as f32) * self.scale)
            .collect()
    }
}
```

INT8 量化的好處：模型大小縮減為 1/4，推論速度提升 2-4 倍（受惠於 INT8 指令集如 AVX-512 VNNI）。

**FP16 量化**（又稱半精度）：將 FP32 截斷為 FP16。好處是精度損失極小（適合推理），GPU 上 FP16 運算比 FP32 快約 2 倍。

**動態量化**：不在訓練時量化，而是在推理時動態決定縮放因子。特別適合 LSTM 和 Transformer 中的線性層。

### 邊緣裝置部署

Rust 框架在邊緣部署上的優勢是壓倒性的：

| 框架 | 最小二進位 | 執行期依賴 | 支援平台 |
|------|-----------|-----------|---------|
| PyTorch (LibTorch) | ~100 MB | libc++、libtorch | x86_64、ARM64 |
| TensorFlow Lite | ~1 MB | libc | x86_64、ARM、RISC-V |
| Candle | ~500 KB | 無（純 Rust） | x86_64、ARM、WASM |
| tract | ~300 KB | 無（可 no_std） | x86_64、ARM、RISC-V |

**tract** 是 Rust 生態中最成熟的推論引擎之一，特別適合邊緣部署：

```rust
// tract 推論範例
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    // 載入 ONNX 模型（無 Python 執行期！）
    let model = onnx()
        .model_for_path("model.onnx")?
        .with_optimizations()?  // 自動最佳化
        .into_runnable()?;

    // 準備輸入
    let input = Tensor::from_shape(&[1, 3, 224, 224])?;
    
    // 執行推論
    let result = model.run(tvec!(input.into()))?;
    
    // 取得輸出
    let output = result[0].to_array_view::<f32>()?;
    println!("Predicted class: {}", output.argmax());
    Ok(())
}
```

### 無 Python 執行期的優勢

這可能是 Rust AI 框架最具革命性的特性：

1. **部署簡單**：一個靜態連結的二進位檔案，拷貝到目標裝置就能執行
2. **無版本衝突**：沒有 Python 3.x 和 pip package 的依賴地獄
3. **啟動快速**：不等待 Python 直譯器初始化（節省 100-500ms）
4. **嵌入式友好**：可以在 RTOS 或 bare-metal 環境中執行

Candle 在 Hugging Face 的生產環境中已經驗證了這些優勢——數百萬次 LLM 推論請求通過純 Rust 服務處理，不需要 Python 執行期。

---

**下一步**：[推論引擎最佳化](focus6.md)

## 延伸閱讀

- [ONNX specification](https://www.google.com/search?q=ONNX+format+specification+protobuf)
- [INT8 quantization techniques](https://www.google.com/search?q=INT8+quantization+deep+learning+inference)
- [tract: Rust ONNX inference engine](https://www.google.com/search?q=tract+ONNX+Rust+inference+engine)
- [Candle deployment guide](https://www.google.com/search?q=Candle+Rust+model+deployment)
- [ONNX Runtime vs Candle vs tract](https://www.google.com/search?q=ONNX+Runtime+vs+Candle+vs+tract+benchmark)
