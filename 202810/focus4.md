# 主題四：推論成本最佳化策略（2023-2028）

## 從 API 調用到邊緣部署的成本控制

### 2023-2024：推論成本挑戰

GPT-4 推論成本高達 $30/1M tokens，催生了推論最佳化需求。

**量化（Quantization）**：將 FP16 權重降到 INT8/INT4：

```python
def quantization_savings(orig: float, bits: int) -> float:
    return round(orig - (orig * 16 / bits * 1.1), 4)

print(quantization_savings(0.01, 8))   # $0.0055 saved
```

**KV Cache 最佳化**：透過 PagedAttention（vLLM）、記憶體共享減少 60-80% 記憶體。

| 引擎 | 關鍵技術 | 速度提升 |
|-----|---------|---------|
| vLLM | PagedAttention | 2-4x |
| TensorRT-LLM | 圖優化 | 3-5x |
| llama.cpp | CPU 推論 | 0 GPU 成本 |

### 2025：提示壓縮與快取

**提示壓縮**：將提示壓縮到原本的 20-30%：

```python
def compression_savings(tokens: int, ratio: float = 0.3) -> dict:
    saved = tokens - int(tokens * ratio)
    return {"saved_tokens": saved, "savings_pct": round(saved / tokens * 100, 1)}
```

**語義快取**：重複或相似查詢直接返回快取結果：

```python
class SemanticCache:
    def __init__(self, threshold=0.95):
        self.cache, self.hits, self.misses = {}, 0, 0
    
    def get(self, q: str) -> str | None:
        for cq, r in self.cache.items():
            sim = len(set(q.split()) & set(cq.split()))
            sim /= max(len(set(q.split()) | set(cq.split())), 1)
            if sim > 0.95:
                self.hits += 1; return r
        self.misses += 1; return None
```

### 2026-2028：邊緣推論經濟學

邊緣設備推論成本趨近於零（一次硬體投資）：

```python
def edge_vs_cloud(edge_dev: float, cloud_per: float,
                  calls: int, months: int) -> tuple:
    edge = edge_dev
    cloud = cloud_per * calls * 30 * months
    be = edge_dev / (cloud_per * calls * 30)
    return ("edge" if edge < cloud else "cloud", round(be, 1))
```

### 實戰策略

1. **路由**：簡單走輕量，困難走重型
2. **批次**：累積請求享 50% 折扣
3. **快取**：語義快取減少重複調用
4. **壓縮**：提示壓縮降 70% token

---

**下一步**: [訓練成本管理](focus5.md)

## 延伸閱讀
- [vLLM: 高效 LLM 推論](https://www.google.com/search?q=vLLM+efficient+LLM+inference)
- [邊緣 AI 推論的成本分析](https://www.google.com/search?q=edge+AI+inference+cost+analysis)
