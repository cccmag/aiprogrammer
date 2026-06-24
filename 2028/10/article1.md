# API 成本追蹤實戰

## 1. 引言

在 AI 專案中，API 呼叫費用往往是最大的營運支出之一。以 OpenAI GPT-4 為例，每百萬個輸出 Token 收費高達 60 美元，若不加以追蹤，月底帳單可能令人震驚。本文將介紹如何使用 Python 實作 API 成本追蹤系統。

## 2. Token 計費機制

主流 AI API 採用按 Token 計費的模式。一個 Token 約等於 0.75 個英文字詞或 0.5 個中文字。以下公式為基礎：

```
成本 = (輸入 Token 數 × 輸入價格 + 輸出 Token 數 × 輸出價格) / 1,000,000
```

## 3. Python 實作成本追蹤器

```python
import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class APICallRecord:
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: float = field(default_factory=time.time)
    latency_ms: Optional[float] = None

class CostTracker:
    # 以 GPT-4o 為例，價格單位為美元 / 百萬 Token
    PRICING = {
        "gpt-4o":        {"input": 2.50, "output": 10.00},
        "gpt-4o-mini":   {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    }

    def __init__(self):
        self.records: list[APICallRecord] = []

    def record(self, model: str, input_tks: int, output_tks: int,
               latency_ms: Optional[float] = None):
        self.records.append(APICallRecord(
            model=model, input_tokens=input_tks,
            output_tokens=output_tks, latency_ms=latency_ms,
        ))

    def total_cost(self) -> dict[str, float]:
        cost = {}
        for r in self.records:
            pricing = self.PRICING.get(r.model)
            if not pricing:
                continue
            c = (r.input_tokens * pricing["input"] +
                 r.output_tokens * pricing["output"]) / 1_000_000
            cost[r.model] = cost.get(r.model, 0) + c
        return cost

    def summary(self) -> str:
        cost = self.total_cost()
        total = sum(cost.values())
        lines = [f"=== API 成本摘要 ==="]
        for model, c in sorted(cost.items()):
            lines.append(f"  {model}: ${c:.4f}")
        lines.append(f"  總計: ${total:.4f}")
        lines.append(f"  總呼叫次數: {len(self.records)}")
        return "\n".join(lines)

# 使用範例
tracker = CostTracker()
tracker.record("gpt-4o", input_tks=1500, output_tks=400)
tracker.record("gpt-4o-mini", input_tks=8000, output_tks=2000, latency_ms=320)
tracker.record("gpt-4o", input_tks=3000, output_tks=1200)
print(tracker.summary())
```

## 4. 成本監控儀表板

加入簡單的 CSV 匯出功能：

```python
import csv
from pathlib import Path

class CostExporter:
    @staticmethod
    def to_csv(records: list[APICallRecord], path: str = "api_cost.csv"):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "model", "input_tokens",
                             "output_tokens", "cost_usd", "latency_ms"])
            for r in records:
                price = CostTracker.PRICING.get(r.model, {})
                cost = (r.input_tokens * price.get("input", 0) +
                        r.output_tokens * price.get("output", 0)) / 1_000_000
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(r.timestamp)),
                    r.model, r.input_tokens, r.output_tokens,
                    f"{cost:.6f}", r.latency_ms or "",
                ])

CostExporter.to_csv(tracker.records)
```

## 5. 實務建議

每週檢視成本報表，對異常高峰設置警報。可搭配 [Google Cloud Monitoring](https://www.google.com/search?q=cloud+cost+monitoring+best+practices) 或自建 Grafana 儀表板。

## 6. 結語

API 成本追蹤不應是事後補救，而應嵌入開發流程。透過上述 Python 工具，團隊能在第一時間掌握 AI 開支，做出精準的最佳化決策。下一篇文章將探討如何在不同模型之間進行成本比較。
