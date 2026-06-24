# 模型量化：從 FP32 到 INT8 的 Rust 實作

## 前言

模型量化（Quantization）是將神經網路的權重和激活值從高精度浮點數（FP32）轉換為低精度整數（INT8）的技術。正確實作的量化可以將模型大小縮減 75%，在支援 INT8 運算的硬體上獲得 2-4 倍的推論加速，且精確度損失通常在 1% 以內。

本文實作從 FP32 到 INT8 的完整量化流程。

## 量化理論

### 非對稱量化

非對稱量化使用 scale（縮放因子）和 zero-point（零點）將浮點數映射到整數：

```
x_int = clamp(round(x_float / scale) + zero_point, qmin, qmax)
x_float = (x_int - zero_point) * scale
```

其中：
- scale = (max - min) / (qmax - qmin)
- zero_point = round(qmin - min / scale)

```rust
#[derive(Debug, Clone)]
struct QuantParams {
    scale: f32,
    zero_point: i32,
}

fn quantize(data: &[f32], qmin: i32, qmax: i32) -> (Vec<i8>, QuantParams) {
    let min = data.iter().cloned().fold(f32::INFINITY, f32::min);
    let max = data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);

    let scale = (max - min) / (qmax - qmin) as f32;
    let zero_point = (qmin as f32 - min / scale).round() as i32;

    let quantized: Vec<i8> = data.iter().map(|&x| {
        let q = (x / scale).round() as i32 + zero_point;
        q.clamp(qmin, qmax) as i8
    }).collect();

    (quantized, QuantParams { scale, zero_point })
}

fn dequantize(data: &[i8], params: &QuantParams) -> Vec<f32> {
    data.iter().map(|&x| {
        (x as i32 - params.zero_point) as f32 * params.scale
    }).collect()
}
```

### 對稱量化

對稱量化假設資料對稱於零點，zero_point = 0：

```
x_int = clamp(round(x_float / scale), -127, 127)
```

這種方式計算更簡單，適合權重量化（權重通常對稱分布）。

## Post-Training Quantization (PTQ)

PTQ 是最常見的量化方法：先訓練模型，然後量化權重，最後用校準資料集決定激活值的量化參數。

### 權重量化

```rust
struct QuantizedLinear {
    weight: Vec<i8>,
    weight_params: QuantParams,
    bias: Option<Vec<f32>>,
    in_features: usize,
    out_features: usize,
}

impl QuantizedLinear {
    fn from_float(weight: &[f32], in_features: usize, out_features: usize) -> Self {
        // 對權重進行對稱量化
        let (qweight, params) = quantize_symmetric(weight);
        QuantizedLinear {
            weight: qweight,
            weight_params: params,
            bias: None,
            in_features,
            out_features,
        }
    }
}
```

### 校準資料集

要量化激活值（activation），需要一個校準資料集來觀察 activation 的分布：

```rust
struct Calibrator {
    min_vals: Vec<f32>,
    max_vals: Vec<f32>,
}

impl Calibrator {
    fn new(num_tensors: usize) -> Self {
        Calibrator {
            min_vals: vec![f32::INFINITY; num_tensors],
            max_vals: vec![f32::NEG_INFINITY; num_tensors],
        }
    }

    fn observe(&mut self, idx: usize, data: &[f32]) {
        let min = data.iter().cloned().fold(f32::INFINITY, f32::min);
        let max = data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        self.min_vals[idx] = self.min_vals[idx].min(min);
        self.max_vals[idx] = self.max_vals[idx].max(max);
    }

    fn finalize(&self) -> Vec<QuantParams> {
        self.min_vals.iter().zip(&self.max_vals).map(|(&min, &max)| {
            let scale = (max - min) / 255.0;
            let zero_point = (0.0 - min / scale).round() as i32;
            // 對於 ReLU 後的激活值，min 通常為 0
            QuantParams { scale, zero_point }
        }).collect()
    }
}
```

## 量化矩陣乘法（QMatMul）

量化後的核心運算是 INT8 矩陣乘法，然後反量化為 FP32：

```rust
fn quantized_matmul(
    a: &[i8],    // M×K, 量化後的輸入
    b: &[i8],    // K×N, 量化後的權重
    a_params: &QuantParams,
    b_params: &QuantParams,
    m: usize, k: usize, n: usize,
) -> Vec<f32> {
    let mut result = vec![0.0f32; m * n];

    for i in 0..m {
        for j in 0..n {
            // INT8 點積
            let mut acc: i32 = 0;
            for kk in 0..k {
                acc += a[i * k + kk] as i32 * b[kk * n + j] as i32;
            }
            // 反量化：output = (input - zp_a) * scale_a * (weight - zp_b) * scale_b
            // 但更高效的方式：先反量化累加結果
            result[i * n + j] = acc as f32 * a_params.scale * b_params.scale;
        }
    }
    result
}
```

### SIMD 加速版

使用 Intel SSE4.1 / ARM NEON 可以大幅加速 INT8 點積：

```rust
#[cfg(target_arch = "aarch64")]
fn dot_product_int8_neon(a: &[i8], b: &[i8], len: usize) -> i32 {
    use std::arch::aarch64::*;
    unsafe {
        let mut acc = vdupq_n_s32(0);
        let mut i = 0;
        while i + 16 <= len {
            let va = vld1q_s8(a.as_ptr().add(i));
            let vb = vld1q_s8(b.as_ptr().add(i));
            // int8 乘積累加到 int32
            let prod16 = vmull_s8(vget_low_s8(va), vget_low_s8(vb));
            let prod32 = vmovl_s16(vget_low_s16(prod16));
            acc = vaddq_s32(acc, prod32);
            i += 16;
        }
        // 水平加總
        vaddvq_s32(acc)
    }
}
```

## 完整量化推論流程

```rust
struct QuantizedModel {
    layers: Vec<QuantizedLayer>,
    activation_params: Vec<QuantParams>,
}

impl QuantizedModel {
    fn infer(&self, input: &[f32]) -> Vec<f32> {
        // 量化輸入
        let (mut x, mut x_params) = quantize(input, 0, 255);

        for (i, layer) in self.layers.iter().enumerate() {
            // 量化矩陣乘法
            let raw = quantized_matmul(
                &x, &layer.weight,
                &x_params, &layer.weight_params,
                layer.in_features, layer.out_features,
            );
            // 對輸出進行反量化與重新量化
            x = quantize_activation(&raw, &self.activation_params[i]);
            x_params = self.activation_params[i].clone();
        }

        // 最後一層輸出為 FP32
        // ...
    }
}
```

## 精度評估

### 量化誤差

量化前後的精確度比較：

| 模型 | FP32 準確率 | INT8 準確率 | 差異 |
|------|------------|------------|------|
| ResNet-18 (ImageNet) | 69.76% | 69.23% | -0.53% |
| MobileNet-V2 | 71.88% | 71.12% | -0.76% |
| BERT-Base (SST-2) | 92.7% | 92.1% | -0.60% |
| LLaMA-7B (ARC) | 52.3% | 51.8% | -0.50% |

### Per-Tensor vs Per-Channel

Per-channel 量化（每個輸出通道獨立 scale/zero-point）可以顯著減少精度損失：

```rust
struct QuantizedConv2d {
    // Per-channel 量化參數
    weight: Vec<i8>,
    weight_scales: Vec<f32>,  // 每個輸出通道一個 scale
    weight_zps: Vec<i32>,     // 每個輸出通道一個 zero-point
    // ...
}
```

| 量化粒度 | 權重壓縮率 | ResNet-50 準確率 |
|---------|-----------|-----------------|
| FP32 (基準) | 1.0x | 76.13% |
| Per-Tensor INT8 | 4.0x | 74.82% |
| Per-Channel INT8 | 4.0x | 75.89% |

## 進階：量化感知訓練（QAT）

PTQ 在大模型（>7B 參數）上可能損失較大。量化感知訓練（Quantization-Aware Training）在訓練過程中模擬量化效應：

```rust
fn fake_quantize(x: &Tensor, params: &QuantParams) -> Tensor {
    // 前向傳播時模擬量化
    let q = round(x / params.scale) + params.zero_point;
    let clamped = clamp(q, 0, 255);
    // 反量化回 FP32（但梯度會繞過 clamp 和 round）
    (clamped - params.zero_point) * params.scale
}
```

在 Rust 中，QAT 通常透過 Candle 或 Burn 的自訂運算實現。

## Candle 的量化支援

Candle 內建了量化模型載入功能：

```rust
use candle_core::quantized::QTensor;

// 載入 GGUF 格式的量化模型
let var = Var::load("model.gguf", &device)?;

// 或者動態量化
let qweight = QTensor::quantize(
    &weight,
    candle_core::quantized::QType::Q8_0,
)?;

// 量化矩陣乘法
let output = qweight.matmul(&activation)?;
```

Candle 支援的量化類型：

| 類型 | 位元寬度 | 儲存格式 | 用途 |
|------|---------|---------|------|
| Q8_0 | 8-bit | scale + int8 block | 通用推論 |
| Q4_0 | 4-bit | scale + int4 block | 極端壓縮 |
| Q4_K | 4-bit | K-quants 改良 | LLaMA 最佳化 |
| Q6_K | 6-bit | K-quants | 高精度需求 |

## 總結

模型量化是將深度學習模型部署到邊緣裝置和生產環境的關鍵技術。從 FP32 到 INT8 的轉換涉及 scale/zero-point 的計算、量化矩陣乘法的實作、以及校準資料集的收集。Rust 的零成本抽象和 SIMD 支援使其成為實作量化引擎的理想語言。

---

**參考資料**

- https://www.google.com/search?q=post+training+quantization+INT8+theory
- https://www.google.com/search?q=quantized+matmul+INT8+SIMD+implementation
- https://www.google.com/search?q=Candle+quantized+tensor+GGUF
- https://www.google.com/search?q=per+channel+quantization+vs+per+tensor
- https://www.google.com/search?q=quantization+aware+training+Rust
