# 模型量化技術（2019-2028）

## 什麼是量化？

量化是將神經網路權重和激活值從高精度浮點數（FP32）轉換為低精度格式（INT8、FP4 甚至二值）的技術。這可以直接減少 4x 的記憶體用量並加速計算。

## 量化技術發展

```
FP32 ──► FP16 ──► INT8 ──► INT4 ──► FP4/NF4
  │        │         │         │         │
  │     2017年   2019年    2022年    2024年
精度高                   速度更快、記憶體更低
```

## 量化原理

量化將浮點數範圍映射到整數範圍：

```python
import numpy as np

def quantize(fp32_weights, bits=8):
    qmin, qmax = 0, 2**bits - 1
    wmin, wmax = fp32_weights.min(), fp32_weights.max()
    scale = (wmax - wmin) / (qmax - qmin)
    zero_point = round(qmin - wmin / scale)
    
    int_weights = np.round(fp32_weights / scale + zero_point)
    int_weights = np.clip(int_weights, qmin, qmax).astype(np.uint8)
    
    return int_weights, scale, zero_point

def dequantize(int_weights, scale, zero_point):
    return (int_weights.astype(np.float32) - zero_point) * scale
```

## 量化的類型

**Post-Training Quantization（PTQ）：**
訓練後直接量化，不需要重新訓練。最簡單但精度損失較大。

**Quantization-Aware Training（QAT）：**
在訓練過程中模擬量化效果，讓模型適應低精度計算。精度更高但需要完整訓練流程。

```
PTQ: 訓練 ──► 量化 ──► 推論
QAT: 訓練+偽量化 ──► 量化 ──► 推論
```

## 主流量化方法

| 方法 | 精度 | 速度提升 | 支援硬體 |
|------|------|---------|---------|
| INT8 對稱量化 | 高 | 2-4x | GPU、CPU |
| INT8 非對稱量化 | 中高 | 2-4x | CPU |
| INT4 GPTQ | 中 | 3-5x | GPU |
| NF4 QLoRA | 中 | 3x | GPU |
| 二值化 BNN | 低 | 10x+ | 專用硬體 |

## 實際挑戰

量化不是零成本的。當位數降低到 INT4 以下，模型精度可能急劇下降。2023 年的研究發現，某些任務（如數學推理）對量化特別敏感。解決方案包括：

1. **混合精度量化**：不同層使用不同精度
2. **GPTQ**：基於 Hessian 矩陣的最佳化量化
3. **AWQ**：基於激活值感知的權重量化

## 延伸閱讀

- [Quantization and Training of Neural Networks](https://www.google.com/search?q=quantization+aware+training+neural+networks+2017)
- [GPTQ: Accurate Post-Training Quantization](https://www.google.com/search?q=GPTQ+post+training+quantization+LLM)
- [AWQ: Activation-aware Weight Quantization](https://www.google.com/search?q=AWQ+activation+aware+weight+quantization)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之二。*
