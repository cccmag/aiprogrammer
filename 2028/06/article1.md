# GPTQ/AWQ 量化實戰

## 量化為何重要

大型語言模型推理時，權重佔據絕大多數記憶體。LLaMA-65B 的 FP16 權重需要 130 GB——一張 A100 也不夠。量化將 FP16 降為 INT4，記憶體立即縮減 4 倍，且推理速度倍增。

## GPTQ — 一次校準、全域量化

GPTQ（2023）是後訓練量化方法，不需要重新訓練。它利用少量校準資料，逐層最小化量化誤差：

```python
import torch
import torch.nn as nn

def gptq_quantize(layer: nn.Linear, calib: torch.Tensor, bits: int = 4):
    """Simulated GPTQ layer quantization"""
    W = layer.weight.data.float()
    H = calib.T @ calib  # Hessian approximation
    diag = torch.diag(H)
    err = torch.zeros_like(W)

    Q = torch.zeros_like(W)
    scale = W.max() / (2**(bits - 1) - 1)

    for col in range(W.shape[1]):
        w = W[:, col]
        q = torch.round(w / scale).clamp(-2**(bits - 1), 2**(bits - 1) - 1)
        Q[:, col] = q
        d = (w - q * scale) / diag[col].clamp(min=1e-10)
        if col < W.shape[1] - 1:
            W[:, col + 1:] -= d.unsqueeze(1) @ H[col, col + 1:].unsqueeze(0)

    return Q * scale
```

## AWQ — 活化感知量化

AWQ 觀察到：**權重中對應大活化值的通道更關鍵**。它不直接量化所有權重，而是先對重要通道做尺度保護：

```python
def awq_scale_weights(W: torch.Tensor, activations: torch.Tensor, alpha: float = 0.5):
    """AWQ: scale important channels before quantization"""
    importance = activations.abs().mean(dim=0)
    scale = importance.pow(alpha)
    W_scaled = W * scale.unsqueeze(0)
    return W_scaled, scale
```

## 實務建議

| 方法 | 位寬 | 困惑度上升 | 速度增益 |
|------|------|-----------|---------|
| FP16 | 16   | 0%        | 1x      |
| GPTQ INT8 | 8 | ~0.5%     | ~1.5x   |
| GPTQ INT4 | 4 | ~2-5%    | ~2.5x   |
| AWQ INT4  | 4 | ~1-3%    | ~2.5x   |

## 工具鏈

- [AutoGPTQ](https://www.google.com/search?q=AutoGPTQ+quantization)
- [AWQ 官方實作](https://www.google.com/search?q=AWQ+activation+aware+weight+quantization)
- [llama.cpp 的 GGUF 格式](https://www.google.com/search?q=llama.cpp+GGUF+quantization)

## 總結

GPTQ 與 AWQ 都是以極低成本讓大模型在消費級硬體上運行的關鍵技術。INT4 量化在維持可接受品質的前提下，將記憶體與延遲同時降低至 1/4，是生產部署的第一優先考量。
