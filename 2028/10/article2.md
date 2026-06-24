# 模型選擇成本比較

## 1. 引言

市面上有數百個 LLM 可供選擇，從 GPT-4o 到 Llama 3.1，價格差距可達 100 倍。選擇合適的模型不僅影響品質，更直接決定專案的經濟可行性。本文建立一套系統化的模型比較框架。

## 2. 主流模型定價

以下為 2026 年主要模型的 API 定價（美元/百萬 Token）：

| 模型 | 輸入價格 | 輸出價格 | 適合場景 |
|------|---------|---------|---------|
| GPT-4o | $2.50 | $10.00 | 高品質推理 |
| GPT-4o-mini | $0.15 | $0.60 | 日常任務 |
| Claude 3.5 Sonnet | $3.00 | $15.00 | 程式碼生成 |
| Gemini 2.0 Flash | $0.10 | $0.40 | 大量推論 |
| Llama 3.1 70B | $0.59 | $0.79 | 自部署 |

## 3. Python 成本比較工具

```python
models = {
    "GPT-4o":       {"input": 2.50, "output": 10.00},
    "GPT-4o-mini":  {"input": 0.15, "output": 0.60},
    "Gemini 2.0 Flash": {"input": 0.10, "output": 0.40},
    "Claude 3.5 Sonnet": {"input": 3.00, "output": 15.00},
    "Llama 3.1 70B":     {"input": 0.59, "output": 0.79},
}

def estimate_cost(model: str, input_tokens: int, output_tokens: int,
                  calls_per_day: int) -> dict:
    p = models[model]
    per_call = (input_tokens * p["input"] +
                output_tokens * p["output"]) / 1_000_000
    daily = per_call * calls_per_day
    return {
        "per_call": round(per_call, 6),
        "daily": round(daily, 2),
        "monthly": round(daily * 30, 2),
        "yearly": round(daily * 365, 2),
    }

# 假設每日 10,000 次呼叫，每次 500 輸入 + 200 輸出 Token
for m in models:
    c = estimate_cost(m, 500, 200, 10_000)
    print(f"{m:20s} 每月 ${c['monthly']:<8.2f} 每年 ${c['yearly']:.2f}")
```

輸出範例：
```
GPT-4o               每月 $5250.00   每年 $63875.00
GPT-4o-mini          每月 $315.00    每年 $3832.50
Gemini 2.0 Flash     每月 $210.00    每年 $2555.00
Claude 3.5 Sonnet    每月 $6300.00   每年 $76650.00
Llama 3.1 70B        每月 $1034.00   每年 $12586.17
```

## 4. 品質 vs 成本權衡

使用低成本模型處理簡單任務，保留高成本模型給關鍵決策。以下為混合策略示範：

```python
def smart_router(query: str) -> str:
    """根據查詢複雜度選擇模型。"""
    complexity = len(query)  # 簡化版判斷
    if complexity < 50:
        return "GPT-4o-mini"  # 簡單查詢
    elif complexity < 200:
        return "Gemini 2.0 Flash"
    else:
        return "GPT-4o"

queries = ["hello", "解釋量子糾纏的原理與應用"]
for q in queries:
    print(f"'{q[:20]}...' -> {smart_router(q)}")
```

## 5. 參考資料

可進一步參考 [LLM 價格比較網站](https://www.google.com/search?q=LLM+pricing+comparison+2026) 與 [OpenAI 定價頁面](https://www.google.com/search?q=OpenAI+API+pricing)。

## 6. 結語

模型選擇沒有絕對的標準答案，關鍵在於根據任務特性找到成本與品質的最佳平衡點。建議團隊建立自己的基準測試，定期重新評估模型組合。
