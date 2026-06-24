# 推論成本與效能權衡

## 成本結構分析

LLM 推論成本由三個關鍵因素決定：

- **計算成本**：GPU 使用時間 × 每小時價格
- **記憶體成本**：模型權重 + KV cache 佔用
- **延遲 SLA**：使用者可接受的最大等待時間

## 成本模型

```python
def inference_cost(model_size_b: float, tokens_per_sec: float,
                   gpu_cost_per_hour: float = 3.0):
    """Calculate cost per million tokens"""
    hours_per_million = (1_000_000 / tokens_per_sec) / 3600
    cost = hours_per_million * gpu_cost_per_hour
    return cost

def gpu_memory_required(model_size_b: float, bits: int,
                        max_seq_len: int, batch_size: int):
    """Estimate GPU memory for inference"""
    weights_gb = model_size_b * bits / 8  # weights
    # KV cache: layers * 2 * batch * seq_len * dim
    kv_cache_gb = (model_size_b / 2) * 2 * batch_size * max_seq_len * 0.001
    return weights_gb + kv_cache_gb + 2  # overhead
```

## 權衡曲線

```python
import matplotlib.pyplot as plt

def plot_tradeoff():
    """Simulate the latency-cost Pareto frontier"""
    precisions = {
        "FP16": {"latency": 1.0, "cost": 1.0, "quality": 1.0},
        "INT8": {"latency": 0.6, "cost": 0.5, "quality": 0.995},
        "INT4": {"latency": 0.4, "cost": 0.25, "quality": 0.97},
        "FP8":  {"latency": 0.7, "cost": 0.6, "quality": 0.99},
    }
    return precisions

tradeoffs = plot_tradeoff()
for prec, metrics in tradeoffs.items():
    print(f"{prec}: latency={metrics['latency']:.1f}x, "
          f"cost={metrics['cost']:.2f}x, quality={metrics['quality']:.3f}")
```

## 量化與成本的關係

INT4 量化可以將成本降低至 FP16 的 **1/4**，但品質下降通常小於 **3%**。關鍵是找到可接受的品質底線：

```python
def find_optimal_precision(quality_threshold: float = 0.97):
    tradeoffs = plot_tradeoff()
    candidates = [
        (p, m) for p, m in tradeoffs.items()
        if m["quality"] >= quality_threshold
    ]
    return min(candidates, key=lambda x: x[1]["cost"])
```

## 部署策略選擇

| 策略 | 延遲 | 吞吐量 | 成本 | 場景 |
|------|------|-------|------|------|
| FP16 裸跑 | 1x | 1x | $$$ | 品質至上 |
| INT8 量化 | 0.6x | 1.7x | $$ | 通用生產 |
| INT4 + KV cache 共享 | 0.4x | 3x | $ | 成本敏感 |
| 蒸餾 + INT8 | 0.3x | 4x | $ | 邊緣裝置 |
| 持續批次 + INT8 | 0.5x | 5x | $$ | 高吞吐 API |

## 實際成本對比

假設 A100 80GB 每小時 $3，LLaMA-70B 推論：

| 配置 | 每秒 token | 每百萬 token 成本 |
|------|-----------|-----------------|
| FP16 (單卡) | 5 | $166 |
| INT8 (單卡) | 12 | $69 |
| INT4 (單卡) | 20 | $42 |
| INT4 + TP-4 | 60 | $14 |

## 延伸閱讀

- [LLM 推理成本計算](https://www.google.com/search?q=LLM+inference+cost+estimation)
- [模型量化經濟學](https://www.google.com/search?q=model+quantization+economics)
- [AI 推論 SLA 設計](https://www.google.com/search?q=AI+inference+SLA+latency+budget)

推論最佳化的本質是經濟學問題：在品質、延遲、成本之間找到最優解。INT4 量化搭配持續批次是目前性價比最高的組合，可將每百萬 token 成本降低 10 倍以上。
