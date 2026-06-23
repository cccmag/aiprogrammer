# 主題六：AI 專案 ROI 評估（2020-2028）

## 從技術投資到商業回報

### ROI 評估框架

```python
def ai_roi(dev: float, monthly_op: float, monthly_rev: float,
           monthly_savings: float, months: int = 12) -> dict:
    total_inv = dev + monthly_op * months
    total_ret = (monthly_rev + monthly_savings) * months
    roi = ((total_ret - total_inv) / total_inv) * 100
    return {"investment": round(total_inv), "return": round(total_ret),
            "roi": round(roi, 1)}
```

### 常見 ROI 案例

| 場景 | 投資 | 年化回報 | ROI |
|-----|-----|---------|-----|
| 客服自動化 | $100-500K | $200K-1M | 100-300% |
| 程式碼輔助 | $50-200K | $150-600K | 200-400% |
| 內容生成 | $30-100K | $100-300K | 200-500% |

```python
def productivity_roi(emps: int, rate: float, hrs: float,
                     tool: float, impl: float) -> dict:
    savings = emps * rate * hrs * 48
    cost = impl + tool * 12
    net = savings - cost
    return {"net": round(net), "roi": round(net / cost * 100, 1)}

print(productivity_roi(50, 100, 5, 20000, 100000))
# ROI = 239.3%
```

### 2024-2025：風險調整

**風險因素**：技術風險 (20-40%)、採用風險 (10-30%)、維護風險 (10-20%)、合規風險 (5-15%)。

```python
def risk_adjusted(raw: float, risks: list[float]) -> float:
    cr = 1 - (1 - sum(risks) / len(risks)) ** len(risks)
    return round(raw * (1 - cr), 1)

print(risk_adjusted(200, [0.3, 0.2, 0.15, 0.1]))  # 119%
```

### 2026-2028：動態 ROI

成本每年下降 40-60%，收益持續成長：

```python
def dynamic_roi(inv: float, cost: float, benefit: float,
                months: int = 36) -> list:
    results, ci, cr = [], inv, 0
    for m in range(1, months + 1):
        c = cost * 0.985 ** m
        b = benefit * 1.03 ** m
        ci += c; cr += b
        results.append((m, round((cr - ci) / ci * 100, 1)))
    return results

print(dynamic_roi(200000, 15000, 35000, 24)[-1])
```

### 關鍵教訓

1. **不要為了 AI 而 AI** — 負 ROI 專案不該執行
2. **從小處著手** — MVP 先跑一個月
3. **成本在下降** — 今天的負 ROI 可能在半年後轉正
4. **無形回報** — 知識積累、品牌形象也是回報

---

**下一步**: [AI 經濟的未來](focus7.md)

## 延伸閱讀
- [AI 專案 ROI 評估指南](https://www.google.com/search?q=AI+project+ROI+evaluation+guide)
- [McKinsey: AI 的經濟潛力](https://www.google.com/search?q=McKinsey+AI+economic+potential+report)
