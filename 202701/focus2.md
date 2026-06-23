# Candle 框架

## 輕量級設計, no-CUDA, 模型 zoo（2023-2026）

### 前言

Candle 是 Hugging Face 於 2023 年發布的純 Rust ML 框架。其核心設計哲學是「最小依賴」——不需要 CUDA、cuDNN、cuBLAS 或任何 C++ 函式庫。

### 設計哲學

Candle 的 API 設計受到 PyTorch 的深遠影響，但完全用 Rust 實作：

```rust
use candle_core::{Device, Tensor, DType};

// 在 GPU 上建立張量（如果可用）
let device = Device::new_metal(0).or_else(|_| Device::Cpu)?;
let t = Tensor::from_slice(&[1.0f32, 2.0, 3.0, 4.0], (2, 2), &device)?;
let t = t.matmul(&t)?;

// 支援多種資料型別
let t_f16 = t.to_dtype(DType::F16)?;
let t_i8 = t_f16.to_dtype(DType::I8)?;
```

Candle 沒有使用 BLAS 函式庫——它的矩陣乘法是純 Rust 實作（雖然可以選用加速函式庫）。

### 支援的模型架構

Candle 的模型 zoo 涵蓋主流架構：

| 模型 | 類型 | Candle 支援 |
|------|------|------------|
| LLaMA 2/3 | 文本生成 | `candle-llama` |
| Mistral | 文本生成 | `candle-mistral` |
| Phi-3 | 小型 LLM | `candle-phi` |
| Whisper | 語音辨識 | `candle-whisper` |
| Stable Diffusion | 影像生成 | `candle-diffusion` |
| YOLOv8 | 物件偵測 | `candle-yolo` |
| BERT | 文本嵌入 | `candle-bert` |
| CLIP | 多模態 | `candle-clip` |

### 從 PyTorch 移植到 Candle

PyTorch 模型移植到 Candle 的典型步驟：

```python
# PyTorch 中：torch.save(model.state_dict(), "model.safetensors")
# 使用 safetensors 格式（Candle 原生支援）
```

```rust
// Candle 中載入權重
use candle_nn::{Linear, VarBuilder};
use safetensors::SafeTensors;

let weights = SafeTensors::deserialize(&std::fs::read("model.safetensors")?)?;
let vb = VarBuilder::from_safetensors(weights, DType::F32, &Device::Cpu);

// 定義與 PyTorch 相同的網路結構
let linear = candle_nn::linear(768, 256, vb.pp("linear"))?;
```

### 在邊緣裝置上的優勢

Candle 沒有外部依賴的特性使其特別適合嵌入式部署：
- 二進位大小：約 5MB（靜態編譯）
- 啟動時間：微秒級
- 記憶體使用：精確控制
- 交叉編譯：只需 `--target aarch64-unknown-linux-gnu`

### 小結

Candle 是 Rust ML 框架中最輕量的選擇。如果你需要一個沒有外部依賴、可以交叉編譯到任何平台的 ML 推論引擎，Candle 是最佳選擇。

---

**下一步**：[Burn 深度學習框架](focus3.md)

## 延伸閱讀

- [Candle GitHub](https://www.google.com/search?q=Candle+GitHub+HuggingFace)
- [Candle examples](https://www.google.com/search?q=Candle+ML+examples+Rust)
- [HuggingFace Candle](https://www.google.com/search?q=HuggingFace+Candle+Rust)
