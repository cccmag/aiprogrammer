# 量化與模型最佳化

## FP32→FP16→INT8, 剪枝, 蒸餾（2022-2026）

### 前言

模型量化是將 ML 模型從高精度浮點數轉換為低精度表示的技術。這是邊緣部署的關鍵——一個 FP32 模型在 MCU 上可能根本無法載入，但 INT8 模型可以。

### 量化層級

| 精度 | 位元寬度 | 模型大小比 | 推論速度比 | 精度損失 |
|------|---------|-----------|-----------|---------|
| FP32 | 32-bit | 1.0x | 1.0x | 基準 |
| FP16 | 16-bit | 0.5x | ~1.5x | 極小 |
| INT8 | 8-bit | 0.25x | ~2-3x | 中等 |
| INT4 | 4-bit | 0.125x | ~3-4x | 顯著 |

### FP32 → FP16 量化

FP16 量化幾乎沒有精度損失，但可以減半模型大小：

```rust
// Candle 中的 FP16 轉換
let tensor_f32 = Tensor::from_slice(&data, shape, &device)?;
let tensor_f16 = tensor_f32.to_dtype(DType::F16)?;

// 儲存為 FP16 safetensors
tensor_f16.save_safetensors("model_f16.safetensors")?;
```

### FP32 → INT8 量化

INT8 量化需要校準（Calibration）過程——透過少量校準資料計算縮放因子：

```rust
// 量化參數結構
struct QuantizationParams {
    scale: f32,       // 縮放因子
    zero_point: i32,  // 零點偏移
}

impl QuantizationParams {
    fn calibrate(data: &[f32]) -> Self {
        let min = data.iter().cloned().fold(f32::MAX, f32::min);
        let max = data.iter().cloned().fold(f32::MIN, f32::max);
        let scale = (max - min) / 255.0;
        let zero_point = (-min / scale).round() as i32;
        QuantizationParams { scale, zero_point }
    }

    fn quantize(&self, data: &[f32]) -> Vec<i8> {
        data.iter()
            .map(|&x| ((x / self.scale) + self.zero_point as f32).round() as i8)
            .collect()
    }
}
```

### 量化感知訓練（QAT）

傳統的訓練後量化（PTQ）可能導致較大精度損失。量化感知訓練（QAT）在訓練過程中模擬量化效果：

```
PTQ: 訓練 (FP32) → 量化 (INT8) → 部署
QAT: 訓練 (FP32 + FakeQuant) → 量化 (INT8) → 部署
```

QAT 通常能保留更高的精度，但需要在 PyTorch 訓練階段就整合量化邏輯。

### 模型剪枝

剪枝移除不重要權重來壓縮模型：

```rust
fn prune_weights(weights: &[f32], threshold: f32) -> (Vec<f32>, Vec<usize>) {
    // 保留絕對值大於 threshold 的權重
    let pruned: Vec<(usize, f32)> = weights.iter()
        .enumerate()
        .filter(|(_, &w)| w.abs() > threshold)
        .map(|(i, &w)| (i, w))
        .collect();

    let indices: Vec<usize> = pruned.iter().map(|(i, _)| *i).collect();
    let values: Vec<f32> = pruned.iter().map(|(_, w)| *w).collect();
    (values, indices)
}
```

### 知識蒸餾

蒸餾是用一個大模型（Teacher）訓練一個小模型（Student）的技術：

```
Teacher (LLaMA 7B) → Soft Labels → Student (TinyLLaMA 1B)
                          ↓
                  蒸餾損失函式
```

蒸餾後的小模型可以在邊緣裝置上運行，保留大模型的大部分能力。

### Rust 在量化工具中的角色

Rust 通常不參與訓練階段，但在部署階段扮演關鍵角色：
1. **執行量化模型**——載入 INT8 權重並執行低精度運算
2. **校準工具**——用 Rust 實作校準資料處理和量化參數計算
3. **格式轉換**——在 safetensors/ONNX 等格式間轉換

### 小結

量化是 Rust ML 部署的核心技術。一個 500MB 的 FP32 模型量化為 INT8 後只有 125MB，可以在 Raspberry Pi 上即時執行。2027 年的 Rust ML 生態已經提供了完整的量化工具鏈。

---

**下一步**：[AI 輔助 Rust 開發](focus7.md)

## 延伸閱讀

- [Model quantization techniques](https://www.google.com/search?q=model+quantization+FP32+FP16+INT8)
- [Quantization aware training](https://www.google.com/search?q=quantization+aware+training+PyTorch)
- [Knowledge distillation](https://www.google.com/search?q=knowledge+distillation+machine+learning)
