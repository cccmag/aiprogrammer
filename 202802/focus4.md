# 模型量化與編譯

## 從 FP32 到 INT4 的十年（2020-2028）

### 前言

模型量化是降低推論延遲最有效的手段之一。從 2020 年的 FP32→INT8 量化，到 2028 年的 INT4 和混合精度編譯——模型體積縮小 8 倍，速度提升 10 倍，精度損失不到 1%。

### 量化的基本原理

將神經網路的權重和激活值從高精度浮點數（FP32）映射到低精度整數（INT8/INT4）：

```python
# 量化公式（對稱量化）
scale = max(abs(weights)) / 127  # INT8 範圍 [-127, 127]
quantized = np.round(weights / scale).astype(np.int8)

# 反量化
dequantized = quantized.astype(np.float32) * scale
```

### 量化技術的三個世代

**第一代：訓練後量化 PTQ（2020-2022）**

```python
# PyTorch 訓練後量化
import torch
model = torch.load("bert_fp32.pth")
quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
# 簡單但精度損失較大（~2%）
```

**第二代：量化感知訓練 QAT（2022-2025）**

```python
# QAT：訓練時模擬量化效果
class QuantizeLinear(torch.nn.Linear):
    def forward(self, x):
        # 前向傳播時插入假量化節點
        q_x = fake_quantize(x, self.scale, self.zero_point)
        w_q = fake_quantize(self.weight, self.w_scale, self.w_zp)
        return torch.nn.functional.linear(q_x, w_q, self.bias)
```

QAT 讓模型在訓練過程中適應量化噪聲，精度損失可降至 0.5% 以下。

**第三代：自動化混合精度（2025-2028）**

2025 年後，量化工具開始自動選擇每層的最佳精度：

```
Layer 0: FP16 (敏感層)
Layer 1: INT8
Layer 2: INT4
Layer 3: INT8
...
```

### 模型編譯器

**TensorRT（NVIDIA）**

```python
# TensorRT 編譯 ONNX 模型
import tensorrt as trt
logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network()
parser = trt.OnnxParser(network, logger)
parser.parse_from_file("model.onnx")
engine = builder.build_cuda_engine(network)
# 自動融合 Conv+Bias+ReLU 等 kernel
```

**Apache TVM（開源編譯器棧）**

TVM 將模型編譯為針對特定硬體的機器碼：

```
ONNX/TorchScript → TVM IR → AutoTVM 搜尋 → 機器碼（CPU/GPU/NPU）
```

### 量化在即時 AI 中的應用

| 精度 | 模型大小 | 速度增益 | 適用場景 |
|------|---------|---------|---------|
| FP32 | 100% | 1x | 訓練、對精度極度敏感 |
| FP16 | 50% | 2x | GPU 推論 |
| INT8 | 25% | 4x | 邊緣裝置、即時推論 |
| INT4 | 12.5% | 8x | 行動裝置、IoT |
| FP8 | 25% | 3x | H100 GPU 原生支援 |

### 最新的發展（2027-2028）

- **FP8 原生支援**：NVIDIA H100/B100 原生 FP8 Tensor Core
- **動態量化**：運行時根據輸入分布動態調整量化參數
- **結構化剪枝+量化**：聯合最佳化，模型壓縮 20x

### 小結

模型量化與編譯讓「在智慧型手機上運行 GPT 等級模型」不再是不可能的事情。從 FP32 到 INT4，從手動調參到自動化編譯——這十年的進步讓即時 AI 在算力受限的場景中成為可能。

---

**下一步**：[邊緣-雲端協同推論](focus5.md)

## 延伸閱讀

- [神經網路量化指南](https://www.google.com/search?q=neural+network+quantization+guide+INT8+INT4)
- [TensorRT 開發者文件](https://www.google.com/search?q=TensorRT+developer+documentation)
- [Apache TVM 開源編譯器](https://www.google.com/search?q=Apache+TVM+deep+learning+compiler)
