# Agent 工作流監控

## 可觀測性的重要性

多步驟 Agent 工作流中，任何一步出錯都可能導致最終結果偏差。監控系統提供即時狀態、錯誤追蹤與效能分析。

## 日誌追蹤系統

```python
import time
import uuid
from dataclasses import dataclass, field

@dataclass
class TraceSpan:
    step_id: str
    parent_id: str = None
    start_time: float = 0.0
    end_time: float = 0.0
    status: str = "pending"
    input: str = ""
    output: str = ""
    error: str = ""
    children: list = field(default_factory=list)

class TraceCollector:
    def __init__(self):
        self.traces = {}

    def start_span(self, name, parent_id=None):
        span = TraceSpan(
            step_id=f"{name}-{uuid.uuid4().hex[:8]}",
            parent_id=parent_id,
            start_time=time.time()
        )
        self.traces[span.step_id] = span
        return span.step_id

    def end_span(self, span_id, status="success", output="", error=""):
        span = self.traces[span_id]
        span.end_time = time.time()
        span.status = status
        span.output = output
        span.error = error

    def get_tree(self, root_id):
        root = self.traces[root_id]
        root.children = [s for s in self.traces.values()
                         if s.parent_id == root_id]
        return root
```

## 監控儀表板

```python
class AgentMonitor:
    def __init__(self):
        self.tracer = TraceCollector()
        self.metrics = {"total_calls": 0, "errors": 0, "avg_latency": 0}

    def instrument(self, func):
        def wrapper(*args, **kwargs):
            self.metrics["total_calls"] += 1
            span_id = self.tracer.start_span(func.__name__)
            start = time.time()
            try:
                result = func(*args, **kwargs)
                self.tracer.end_span(span_id, output=str(result)[:500])
                return result
            except Exception as e:
                self.metrics["errors"] += 1
                self.tracer.end_span(span_id, status="error", error=str(e))
                raise
            finally:
                latency = time.time() - start
                n = self.metrics["total_calls"]
                self.metrics["avg_latency"] = (
                    (self.metrics["avg_latency"] * (n - 1) + latency) / n
                )
        return wrapper
```

## 警報與除錯

設定閾值：單步延遲 > 30s 發出警報、錯誤率 > 5% 暫停服務。保留完整 trace 供事後分析。詳見 https://www.google.com/search?q=LLM+agent+monitoring+observability。
