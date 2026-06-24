# 主題一：AI 經濟學導論（2020-2028）

## 從技術成本到經濟模型的演進

### 2020：AI 經濟的起點

2020 年是 AI 經濟學的關鍵轉折。GPT-3 的發布讓人們看到大型語言模型的潛力，但其訓練成本估計高達 460 萬美元，推論成本也遠高於傳統機器學習模型。這個時期的核心問題是：**AI 的效益是否值得其成本？**

### 2021-2022：規模化定律與成本曲線

OpenAI 在 2020 年提出的[伸縮定律（Scaling Laws）](https://www.google.com/search?q=scaling+laws+neural+language+models+kaplan)揭示了模型性能與計算量、數據量之間的冪律關係。這意味著：
- 每提升 10 倍性能，計算成本增加約 10 倍
- 訓練成本和推論成本遵循不同的規模化路徑
- 硬體效率每年提升約 2 倍（摩爾定律 + 專用晶片）

```python
def scaling_cost(base_cost: float, performance_gain: float) -> float:
    """Calculate cost for a given performance gain"""
    # Empirical scaling: 10x compute → ~10x performance
    compute = performance_gain
    return base_cost * compute
```

### 2023-2024：API 經濟的成熟

OpenAI 的 ChatGPT 和後續的 GPT-4 建立了 API 定價模型。競爭對手（Anthropic、Google、Meta）紛紛進入市場，形成多層次定價結構：

| 模型層級 | 價格範圍（每百萬 token） | 適用場景 |
|---------|----------------------|---------|
| 旗艦 | $10-30 | 複雜推理、程式碼生成 |
| 標準 | $1-10 | 一般問答、內容生成 |
| 輕量 | $0.1-1 | 分類、摘要、嵌入 |

### 2025-2026：開源模型的衝擊

Llama 系列、Mistral、DeepSeek 等開源模型的崛起改變了經濟格局。開源模型的推論成本可低至閉源模型的 1/10 到 1/100，同時在某些任務上達到接近的性能。

```python
def cost_ratio(open_source_cost: float, closed_source_cost: float) -> float:
    return round(open_source_cost / closed_source_cost, 3)

# Example: Llama-4 vs GPT-4o for classification
print(cost_ratio(0.001, 0.01))  # 0.1 → 10x cheaper
```

### 2027-2028：AI 經濟學新範式

到 2028 年，AI 經濟學已發展為成熟的跨學科領域，包含：
- **Token 經濟學**：Token 成為新的計價單位
- **GPU 經濟學**：算力資源的市場化配置
- **模型即服務（MaaS）**：從 API 到完整解決方案的定價
- **邊緣 AI 經濟學**：設備端推論的成本效益分析

### 核心框架：TCO（總持有成本）

AI 專案的總持有成本包含：
1. **基礎設施成本**：GPU/TPU 租用或採購、網路、儲存
2. **API 成本**：模型調用費用
3. **人力成本**：提示工程師、AI 工程師、領域專家
4. **訓練成本**：數據準備、訓練執行、實驗管理
5. **維護成本**：模型監控、更新、版本管理

```python
def total_cost_of_ownership(
    infra: float, api: float, labor: float,
    training: float, maintenance: float, months: int
) -> dict:
    monthly = infra + api + labor + training / months + maintenance
    yearly = monthly * 12
    return {"monthly": round(monthly, 2), "yearly": round(yearly, 2)}

tco = total_cost_of_ownership(50000, 30000, 80000, 120000, 10000, 12)
print(tco)  # {'monthly': 170000.0, 'yearly': 2040000.0}
```

---

**下一步**: [AI 成本模型與定價策略](focus2.md)

## 延伸閱讀
- [Scaling Laws for Neural Language Models](https://www.google.com/search?q=scaling+laws+neural+language+models+kaplan)
- [AI 經濟學：從成本到價值的分析框架](https://www.google.com/search?q=AI+economics+cost+value+analysis+framework)
- [The Cost of AI: A Survey](https://www.google.com/search?q=survey+AI+cost+analysis+2024)
