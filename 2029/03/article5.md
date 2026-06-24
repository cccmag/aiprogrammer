# AI 應用監控實戰

## 前言

AI 應用不同於傳統軟體：LLM 輸出不確定性高、延遲波動大、成本可變。完善的監控系統是保障服務品質的關鍵。

## 關鍵指標

```python
from dataclasses import dataclass, field
from datetime import datetime
import statistics

@dataclass
class LLMMetrics:
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_cost: float
    model: str
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error_type: str = ""

class MetricsCollector:
    def __init__(self):
        self.metrics: list[LLMMetrics] = []

    def record(self, metric: LLMMetrics):
        self.metrics.append(metric)

    def summary(self, minutes: int = 5) -> dict:
        cutoff = datetime.now().timestamp() - minutes * 60
        recent = [
            m for m in self.metrics
            if m.timestamp.timestamp() > cutoff
        ]
        if not recent:
            return {}

        latencies = [m.latency_ms for m in recent]
        costs = [m.total_cost for m in recent]
        tokens = [m.prompt_tokens + m.completion_tokens for m in recent]

        return {
            "p50_latency": statistics.median(latencies),
            "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)],
            "total_cost": sum(costs),
            "avg_tokens": statistics.mean(tokens),
            "total_calls": len(recent),
            "error_rate": sum(1 for m in recent if not m.success) / len(recent),
        }
```

## 成本追蹤

```python
from collections import defaultdict

MODEL_PRICING = {
    "gpt-4o": {"input": 0.01, "output": 0.03},
    "gpt-4o-mini": {"input": 0.0015, "output": 0.006},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
}

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o-mini"])
    return (prompt_tokens / 1000 * pricing["input"] +
            completion_tokens / 1000 * pricing["output"])

class CostTracker:
    def __init__(self, budget: float):
        self.budget = budget
        self.daily_costs: dict[str, float] = defaultdict(float)

    def record_call(self, model: str, prompt_tokens: int, completion_tokens: int):
        cost = calculate_cost(model, prompt_tokens, completion_tokens)
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_costs[today] += cost

    def daily_spend(self) -> float:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.daily_costs.get(today, 0.0)

    def budget_remaining(self) -> float:
        total = sum(self.daily_costs.values())
        return self.budget - total
```

## 異常偵測

```python
class AnomalyDetector:
    def __init__(self, collector: MetricsCollector):
        self.collector = collector

    def detect(self) -> list[str]:
        alerts = []
        summary = self.collector.summary(minutes=5)

        if summary.get("p99_latency", 0) > 10000:
            alerts.append("P99 latency exceeds 10s threshold")

        if summary.get("error_rate", 0) > 0.05:
            alerts.append("Error rate exceeds 5% threshold")

        if summary.get("total_cost", 0) > 10:
            alerts.append("5-minute spend exceeds $10 threshold")

        return alerts

async def monitor_llm_call(coro, collector: MetricsCollector):
    start = datetime.now()
    try:
        result = await coro
        elapsed = (datetime.now() - start).total_seconds() * 1000
        collector.record(LLMMetrics(
            latency_ms=elapsed,
            prompt_tokens=result.usage["prompt_tokens"],
            completion_tokens=result.usage["completion_tokens"],
            total_cost=calculate_cost(result.model, **result.usage),
            model=result.model,
        ))
        return result
    except Exception as e:
        elapsed = (datetime.now() - start).total_seconds() * 1000
        collector.record(LLMMetrics(
            latency_ms=elapsed, prompt_tokens=0,
            completion_tokens=0, total_cost=0.0,
            model="unknown", success=False, error_type=str(e)
        ))
        raise
```

## 結語

監控是 AI 原生應用不可或缺的基礎設施。即時掌握延遲、成本、錯誤率等指標，才能在問題惡化前快速應對，確保服務穩定可靠。

---

**延伸閱讀**

- [LLM 應用監控最佳實踐](https://www.google.com/search?q=LLM+application+monitoring+best+practices)
- [AI 可觀測性工具](https://www.google.com/search?q=AI+observability+tools+2026)
- [OpenTelemetry for LLM](https://www.google.com/search?q=OpenTelemetry+LLM+tracing)
