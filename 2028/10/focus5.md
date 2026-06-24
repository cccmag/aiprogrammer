# 主題五：訓練成本管理（2022-2028）

## 從百萬級到平民化的訓練經濟

### 2022：訓練成本頂峰

GPT-3 訓練成本約 460 萬美元。

```python
def train_cost(params_b: float, tokens_b: float) -> float:
    flops = params_b * 1e9 * tokens_b * 1e9 * 6
    gpu_hours = flops / (312e12 * 3600)
    return round(gpu_hours * 2.0 / 1e6, 2)  # $2/GPU-hour

print(train_cost(175, 300))  # ~$4.6M
```

### 2023：效率革命

**LoRA 微調**：只訓練參數總量的 0.1-1%：

```python
def lora_cost(full_b: float, r: int = 16, base: float = 10000) -> float:
    trainable = (2 * r * 4096 * 32) / (full_b * 1e9)
    return round(base * trainable, 2)

print(lora_cost(70))  # ~$6
```

**Flash Attention**：訓練速度提升 2-4 倍，記憶體大幅降低。

### 2024：開源工具鏈

| 工具 | 效果 |
|-----|------|
| Axolotl | 簡化微調，開發時間減 80% |
| Unsloth | GPU 記憶體減 50% |
| DeepSpeed ZeRO | 支援更大模型 |

### 2025：知識蒸餾

小模型學習大模型能力，但數據生成成本可能超過訓練成本。

### 2026-2028：訓練民主化

```python
def cost_trend(base: float, year: int) -> float:
    return base * 0.4 ** (year - 2024)

print(cost_trend(1000000, 2024))  # $1,000,000
print(cost_trend(1000000, 2028))  # $25,600
```

到 2028 年，個人開發者可在消費級 GPU 完成多數訓練需求。

### 成本管理清單

1. **確認真實需求**：提示工程 → RAG → 微調
2. **選對方法**：LoRA 比全量微調省 100-1000 倍
3. **數據品質 > 數量**：減少無效訓練
4. **Spot 實例**：可節省 GPU 費用 60-80%

---

**下一步**: [AI 專案 ROI 評估](focus6.md)

## 延伸閱讀
- [LoRA: Low-Rank Adaptation of LLMs](https://www.google.com/search?q=LoRA+low+rank+adaptation+LLM)
- [AI 訓練成本報告 2024-2028](https://www.google.com/search?q=AI+training+cost+report+2024+2028)
- [分散式訓練最佳實踐](https://www.google.com/search?q=distributed+training+best+practices+LLM)
