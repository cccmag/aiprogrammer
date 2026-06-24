# 嵌入式 ML 推論 — TFLite Micro vs Rust 方案對比

## 為什麼在 MCU 上跑 ML

邊緣推論的三個核心驅動力：

1. **延遲**：雲端推論的往返延遲通常是 50–500ms，本地推論可以壓到 1ms 以下
2. **隱私**：感測器資料不需要離開裝置
3. **離線**：即使網路中斷，裝置仍能正常工作

## TFLite Micro 概述

TensorFlow Lite Micro 是 Google 為 MCU 設計的推論引擎：

- **C++ 實作**：約 20KB Flash footprint
- **支援模型**：透過 TensorFlow 訓練後轉換為 TFLite 格式
- **算子集合**：精簡的算子集（Conv2D、DepthwiseConv2D、FullyConnected 等）
- **記憶體管理**：靜態記憶體分配，無動態配置

在 Rust 中使用 TFLite Micro：

```rust
use tflite_micro_rust::Interpreter;

let model = include_bytes!("model.tflite");
let mut interpreter = Interpreter::new(model).unwrap();
interpreter.input(0).copy_from_slice(&input_data);
interpreter.invoke();
let output = interpreter.output(0);
```

## Rust 原生方案

### Candle

Hugging Face 的 Candle 提供純 Rust 實作：

```rust
use candle_core::Tensor;
use candle_nn::VarBuilder;

let model = candle_nn::ops::conv2d(&input, ...);
```

優點：純 Rust、GPU 支援、與 HuggingFace 生態整合
限制：設計目標是 GPU/CPU，對 MCU 的 Flash/RAM 限制較高

### burn-embedded

Burn 的嵌入式子專案：

```rust
use burn::tensor::backend::NdArrayBackend;
type Backend = NdArrayBackend<f32>;

let model = model::init::<Backend>(&device);
let output = model.forward(input);
```

優點：Burn 生態系整合、支援量化
限制：仍處於早期開發階段

### micro-ai crate

社群開發的超輕量推論框架：

```rust
use micro_ai::nn::Dense;

let layer = Dense::<16, 4>::new(weights, bias);
let output = layer.forward(&input);
```

優點：極小 footprint、no_std 相容、編譯期維度檢查
限制：算子覆蓋率有限

## 對比分析

| 面向 | TFLite Micro | Candle | burn-embedded | micro-ai |
|------|-------------|--------|--------------|----------|
| 語言 | C++ | Rust | Rust | Rust |
| Flash (最小) | ~20 KB | ~200 KB | ~150 KB | ~5 KB |
| RAM 需求 | ~10 KB | ~1 MB | ~256 KB | ~2 KB |
| no_std | ✗ | ✗ | ✓ | ✓ |
| 算子數量 | 80+ | 50+ | 30+ | 10+ |
| 量化支援 | ✓ | ✓ | ✓ | ✗ |
| 模型轉換 | TFLite | PyTorch/SafeTensors | Burn | 自訂 |

## 關鍵決策因素

### 何時選 TFLite Micro

- 需要大量預訓練模型的相容性
- 團隊熟悉 TensorFlow 生態
- 目標 MCU 有足夠的 Flash（>256 KB）

### 何時選 Rust 原生

- 專案已經是 Rust 生態
- 需要 no_std 相容
- 記憶體極度受限（<64 KB Flash）
- 只需少量固定運算

## 實戰：關鍵字辨識

使用 micro-ai 在 STM32F4 上實作簡單的關鍵字辨識：

```rust
// MFCC 特徵提取 + 小型神經網路
let features = compute_mfcc(audio_buffer);
let result = keyword_model.forward(&features);
let max_idx = result.argmax();
let keyword = ["silence", "yes", "no", "unknown"][max_idx];
```

## 延伸閱讀

- [TFLite Micro 官方文件](https://www.google.com/search?q=TensorFlow+Lite+Micro+documentation)
- [Candle Rust ML 框架](https://www.google.com/search?q=Candle+Rust+ML+framework)
- [嵌入式 ML 模型最佳化](https://www.google.com/search?q=embedded+ML+model+optimization+quantization)
- [TinyML 應用案例](https://www.google.com/search?q=TinyML+keyword+spotting+MCU)
