# 訓練成本降低策略

## 1. 引言

訓練大型語言模型的成本極高。Meta 的 Llama 3.1 405B 訓練估計花費超過 6,000 萬美元。對於資源有限的團隊，如何在有限的預算內有效訓練模型是關鍵課題。

## 2. 訓練成本構成

大型模型訓練成本主要來自：

- **運算資源**（約 70%）：GPU/TPU 租用費用
- **資料處理**（約 15%）：清洗、標註、儲存
- **實驗迭代**（約 10%）：超參數調優、失敗實驗
- **人事與管理**（約 5%）

## 3. LoRA 微調策略

LoRA（Low-Rank Adaptation）是當前最主流的低成本微調方法：

```python
import torch
import torch.nn as nn

class LoRALayer(nn.Module):
    def __init__(self, in_features: int, out_features: int, rank: int = 8):
        super().__init__()
        self.lora_a = nn.Parameter(torch.randn(in_features, rank) * 0.02)
        self.lora_b = nn.Parameter(torch.zeros(rank, out_features))
        self.scaling = 1.0 / rank

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return (x @ self.lora_a @ self.lora_b) * self.scaling

def estimate_lora_savings(base_params: int, lora_params: int) -> dict:
    """估算 LoRA 相較於全參數微調的節省。"""
    base_memory = base_params * 4 / 1e9  # FP32, GB
    lora_memory = lora_params * 4 / 1e9  # 僅訓練 LoRA 權重
    return {
        "trainable_params": f"{lora_params:,}",
        "memory_saved_gb": round(base_memory - lora_memory, 2),
        "memory_reduction_pct": round((1 - lora_memory/base_memory) * 100),
    }

# LLaMA 7B 全參數微調 vs LoRA (rank=8)
full = 7e9  # 70 億參數
lora = 7e9 * 8 * 2 / 4096  # LoRA A/B 參數
savings = estimate_lora_savings(full, lora)
print(f"可訓練參數: {savings['trainable_params']}")
print(f"記憶體節省: {savings['memory_saved_gb']} GB")
print(f"記憶體降幅: {savings['memory_reduction_pct']}%")
```

## 4. 混合精度訓練

使用 FP16/BF16 可將記憶體需求減半：

```python
def compare_precision(model_size_params: int):
    precisions = {
        "FP32": 4,
        "FP16": 2,
        "BF16": 2,
        "INT8": 1,
    }
    for name, bytes_per_param in precisions.items():
        memory = model_size_params * bytes_per_param / 1e9
        cost = memory * 0.5  # 假設每 GB 每小時 $0.5
        print(f"{name:5s} 記憶體: {memory:.1f} GB, 每小時成本: ${cost:.2f}")

compare_precision(7e9)
```

## 5. 資料效率訓練

減少所需訓練資料量可直接降低成本：

```python
def data_efficiency_training(original_samples: int, method: str):
    efficiency = {
        "instruction_tuning": 0.3,   # 只需 30% 資料
        "curriculum_learning": 0.5,  # 只需 50% 資料
        "active_learning": 0.2,      # 只需 20% 資料
    }
    ratio = efficiency.get(method, 1.0)
    reduced = original_samples * ratio
    saved = original_samples - reduced
    print(f"原始資料量: {original_samples:,}")
    print(f"使用方法: {method}")
    print(f"實際需要: {int(reduced):,}")
    print(f"節省資料: {int(saved):,} ({ratio*100:.0f}%)")

data_efficiency_training(1_000_000, "active_learning")
```

## 6. 雲端 GPU 選擇

比較不同 GPU 的訓練成本效益：

```python
gpus = {
    "A100 80GB":   {"cost": 3.50, "speed": 1.0},
    "H100 80GB":   {"cost": 5.00, "speed": 1.8},
    "H200 141GB":   {"cost": 7.00, "speed": 2.5},
    "B200":         {"cost": 10.00, "speed": 4.0},
}
for gpu, spec in gpus.items():
    cost_per_unit = spec["cost"] / spec["speed"]
    print(f"{gpu:15s} $/小時: ${spec['cost']:.2f}, "
          f"成本效率: ${cost_per_unit:.2f}")
```

## 7. 結語

搭配 [Google Cloud Training](https://www.google.com/search?q=cloud+GPU+training+cost+optimization) 的預留實例與 Spot 實例，可再節省 60-70% 的訓練成本。LoRA + 混合精度 + 資料效率訓練是當前最具成本效益的組合策略。
