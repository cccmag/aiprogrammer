# 主題三：模型選擇經濟學（2022-2028）

## 如何在性能與成本之間取得平衡

### 問題定義

核心問題：給定一個任務，選擇哪個模型能使效用最大化、成本最小化？

```python
def model_efficiency(quality: float, cost: float) -> float:
    return quality / cost if cost > 0 else 0
```

### 2022-2023：初期選擇

早期模型選擇簡單——價格與性能成正比：Davinci > Curie > Babbage > Ada。

### 2024：模型爆炸

可選模型從個位數暴增到上百個，評估維度擴展為：
1. **質量** — 基準測試表現
2. **成本** — 每百萬 token 價格
3. **延遲** — 首 token 時間
4. **上下文長度** — 可處理輸入量

```python
def model_score(quality: float, cost_per_m: float,
                latency_ms: float, ctx_window: int) -> float:
    cost_score = 1 / (cost_per_m + 0.1)
    latency_score = 1000 / (latency_ms + 100)
    ctx_score = min(ctx_window / 128000, 1.0)
    return round(quality * 0.5 + cost_score * 0.2 +
                 latency_score * 0.2 + ctx_score * 0.1, 3)
```

### 2025-2026：最佳化框架

模型選擇成為正式的最佳化問題——在預算限制下選擇最優模型組合：

```python
def optimal_model_selection(tasks: list[dict], models: list[dict],
                            budget: float) -> list[str]:
    from itertools import product
    best = {"cost": float('inf'), "assignment": []}
    for a in product(models, repeat=len(tasks)):
        tc = sum(m['cost'] for m in a)
        if tc <= budget and tc < best["cost"]:
            best = {"cost": tc, "assignment": [m['name'] for m in a]}
    return best["assignment"]
```

### 2027-2028：動態路由

**分層路由**：先由低成本模型處理，信心不足時升級：

```python
def cascade(q: str, conf: float) -> dict:
    if conf > 0.95: return {"model": "llama-4-70b", "cost": 0.0005}
    elif conf > 0.8: return {"model": "claude-4", "cost": 0.003}
    else:            return {"model": "gpt-5", "cost": 0.01}
```

### 黃金法則

```
task_quality / cost > threshold → 選擇該模型
否則 → 微調小模型或使用人工
```

---

**下一步**: [推論成本最佳化策略](focus4.md)

## 延伸閱讀
- [模型選擇最佳化指南](https://www.google.com/search?q=AI+model+selection+optimization+guide)
- [成本感知的 AI 模型選擇](https://www.google.com/search?q=cost+aware+AI+model+selection)
