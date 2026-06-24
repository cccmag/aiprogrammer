# 主題二：AI 成本模型與定價策略（2021-2028）

## API 定價的演變與經濟邏輯

### 2021：Token 定價的誕生

OpenAI 推出 GPT-3 API 時，創造了「每千個 token」的計價單位。Token 既是計算成本的真實代理，又是客戶能直觀理解的計量單位。

```python
def token_cost(tokens: int, price_per_1k: float) -> float:
    return (tokens / 1000) * price_per_1k
```

### 2022-2023：多層次定價模型

OpenAI 引入差異化定價：輸出 token 價格是輸入的 3-4 倍；32K/128K 上下文各有不同定價；批次處理（Batch API）可節省 50% 成本。

```python
def api_cost(prompt_tokens: int, completion_tokens: int,
             input_price: float, output_price: float) -> float:
    return (prompt_tokens * input_price + completion_tokens * output_price) / 1000
```

### 2024：AI 價格戰元年

| 模型 | 年初價格（/1M input） | 年底價格 |
|-----|--------------------|--------|
| GPT-4 Turbo | $10 | $2.5 |
| Claude 3 Sonnet | $3 | $1.5 |
| Gemini 1.5 Pro | $7 | $3.5 |

### 2025-2026：精細化定價

**混合模型路由**：簡單查詢走便宜模型，複雜查詢走昂貴模型：

```python
def cascade_routing(query: str) -> str:
    if len(query) < 50:    return "gemini-2.5"
    elif "code" in query:  return "claude-4"
    else:                  return "gpt-5"
```

承諾用量折扣類似雲端服務的 Reserved Instances，年約客戶可獲 30-50% 折扣。

### 2027-2028：新定價模型

- **性能保證定價（SLA-based）**：保證延遲或品質
- **結果定價**：按成功任務付費
- **算力市場**：GPU 算力的即時拍賣

### 成本最佳化的核心策略

```
簡單任務 → 輕量模型 (90% cases)
中等任務 → 標準模型 (9% cases)
困難任務 → 旗艦模型 (1% cases)
          混合策略可節省 60-80% 成本
```

---

**下一步**: [模型選擇經濟學](focus3.md)

## 延伸閱讀
- [OpenAI API Pricing History](https://www.google.com/search?q=OpenAI+API+pricing+history+timeline)
- [AI Model Pricing Comparison](https://www.google.com/search?q=AI+model+pricing+comparison+2025)
