# ML 模型量化與最佳化 — FP32→FP16→INT8、剪枝、蒸餾

## 1. 引言

模型量化是 Rust ML 部署的關鍵技術。一個 FP32 的 ResNet-50 約 98MB，量化為 INT8 後僅 25MB，可以在 Raspberry Pi 上達到即時推論。本文從實作角度探討量化的原理與技術。

## 2. 量化原理

### 線性量化

將浮點數範圍映射到整數範圍：

```
FP32: [-3.0, 2.5]
INT8: [-128, 127]

scale = (2.5 - (-3.0)) / 255 = 0.02157
zero_point = round(-(-3.0) / 0.02157) = 139

量化公式: q = round(r / scale) + zero_point
反量化公式: r = (q - zero_point) * scale
```

Rust 實作：

```rust
#[derive(Debug, Clone)]
pub struct QuantizedTensor {
    data: Vec<i8>,
    scale: f32,
    zero_point: i32,
    shape: Vec<usize>,
}

impl QuantizedTensor {
    pub fn quantize(data: &[f32]) -> Self {
        let min = data.iter().cloned().fold(f32::MAX, f32::min);
        let max = data.iter().cloned().fold(f32::MIN, f32::max);
        let scale = (max - min) / 255.0;
        let zero_point = (-min / scale).round() as i32;

        let quantized: Vec<i8> = data.iter()
            .map(|&x| {
                let q = (x / scale).round() as i32 + zero_point;
                q.clamp(-128, 127) as i8
            })
            .collect();

        Self {
            data: quantized,
            scale,
            zero_point,
            shape: vec![data.len()],
        }
    }

    pub fn dequantize(&self) -> Vec<f32> {
        self.data.iter()
            .map(|&q| (q as i32 - self.zero_point) as f32 * self.scale)
            .collect()
    }
}
```

## 3. 量化層級選擇

| 精度 | 位元 | 模型大小 | 速度增益 | 適合場景 |
|------|------|---------|---------|---------|
| FP32 | 32 | 100% | 1.0x | 精度關鍵的部署 |
| FP16 | 16 | 50% | 1.5x | GPU 推論 |
| INT8 | 8 | 25% | 2-3x | 邊緣 CPU 推論 |
| INT4 | 4 | 12.5% | 3-4x | 極端邊緣場景 |

## 4. 訓練後量化（PTQ）

最簡單的量化方式，在訓練後直接轉換：

```rust
use candle_core::{Tensor, DType, Device};

fn convert_to_fp16(t: &Tensor) -> Result<Tensor, candle_core::Error> {
    t.to_dtype(DType::F16)
}

fn convert_to_int8(t: &Tensor) -> Result<Tensor, candle_core::Error> {
    t.to_dtype(DType::I8)
}

fn quantize_model_weights(model_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;

    // 載入 FP32 權重
    let weights = std::fs::read(model_path)?;
    let tensors = safetensors::SafeTensors::deserialize(&weights)?;

    // 逐層量化為 INT8
    let mut quantized = Vec::new();
    for tensor_name in tensors.names() {
        let tensor = tensors.tensor(tensor_name)?;
        let data = tensor.data();
        let quantized_data = QuantizedTensor::quantize(
            &bytemuck::cast_slice::<u8, f32>(data)
        );
        quantized.push((tensor_name.to_string(), quantized_data));
    }

    Ok(())
}
```

## 5. 量化感知訓練（QAT）

QAT 在訓練過程中模擬量化效應：

```python
# PyTorch 中的 QAT
import torch
import torch.quantization

model = MyModel()
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model = torch.quantization.prepare_qat(model, inplace=True)

# 正常訓練...
for data, target in dataloader:
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()

# 轉換為量化模型
model = torch.quantization.convert(model, inplace=True)
torch.onnx.export(model, dummy_input, "model.qat.onnx")
```

QAT 通常比 PTQ 多保留 1-3% 的準確率。

## 6. 模型剪枝

剪枝移除貢獻較小的權重：

```rust
pub struct PrunedLinear {
    indices: Vec<usize>,    // 非零權重的索引
    values: Vec<i8>,         // INT8 量化後的權重值
    bias: Vec<f32>,
    input_size: usize,
    output_size: usize,
    sparsity: f32,           // 稀疏度 (0.0 ~ 1.0)
}

impl PrunedLinear {
    pub fn new(weights: &[f32], sparsity: f32) -> Self {
        let threshold = Self::find_threshold(weights, sparsity);

        let pruned: Vec<(usize, f32)> = weights.iter()
            .enumerate()
            .filter(|(_, &w)| w.abs() > threshold)
            .map(|(i, &w)| (i, w))
            .collect();

        Self {
            indices: pruned.iter().map(|(i, _)| *i).collect(),
            values: pruned.iter().map(|(_, w)| (*w * 127.0) as i8).collect(),
            bias: vec![0.0; output_size],
            sparsity,
            input_size,
            output_size,
        }
    }

    pub fn forward(&self, input: &[f32]) -> Vec<f32> {
        let mut output = self.bias.clone();
        for (&idx, &val) in self.indices.iter().zip(self.values.iter()) {
            let out_idx = idx / self.input_size;
            let in_idx = idx % self.input_size;
            output[out_idx] += input[in_idx] * (val as f32 / 127.0);
        }
        output
    }
}
```

## 7. 知識蒸餾

蒸餾的核心公式：

```
L_total = α * L_hard(y_student, y_true) + (1-α) * L_soft(y_student, y_teacher / T)
```

其中 T 是溫度參數，控制軟標籤的平滑度。

蒸餾可以顯著壓縮模型而不損失太多精度：
- Teacher: ResNet-152 (60M 參數) → 準確率 78.3%
- Student: MobileNetV2 (3.5M 參數) → 準確率 76.8%（蒸餾後）
- 壓縮比: 17x, 精度損失: 1.5%

## 8. 完整的 Rust 部署管線

```rust
// 從量化模型載入到部署的完整流程
pub struct DeployedModel {
    layers: Vec<QuantizedLinear>,
}

impl DeployedModel {
    pub fn from_quantized(path: &str) -> Result<Self, Error> {
        // 1. 載入量化後的 safetensors
        // 2. 重建為 QuantizedLinear 層
        // 3. 驗證輸入輸出精度
        // 4. 回傳部署準備完成的模型
    }

    pub fn infer(&self, input: &[f32]) -> Vec<f32> {
        let mut x = input.to_vec();
        for layer in &self.layers {
            x = layer.forward(&x);
        }
        x
    }
}
```

## 9. 結語

模型量化是 Rust ML 邊緣部署的核心技術。從 FP32→FP16→INT8，每一步量化都伴隨著精度與效能的取捨。2027 年的 Rust ML 生態已提供了完整的量化工具鏈，開發者可以專注於選擇最適合部署場景的量化策略。

## 延伸閱讀

- [Model quantization techniques](https://www.google.com/search?q=model+quantization+techniques+deep+learning)
- [Quantization aware training](https://www.google.com/search?q=quantization+aware+training+PyTorch+QAT)
- [Knowledge distillation](https://www.google.com/search?q=knowledge+distillation+machine+learning+survey)
