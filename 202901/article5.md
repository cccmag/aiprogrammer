# 工作流監控與可觀測性

## 1. 引言

當工作流從簡化腳本成長為多 Agent 協作的複雜系統時，監控與可觀測性成為不可或缺的基礎設施。沒有良好的可觀測性，工作流的行為就像一個黑盒子，除錯與最佳化無從談起。

## 2. 三支柱模型

可觀測性的三大支柱：日誌 (Logs)、指標 (Metrics) 與追蹤 (Traces)。

```python
import time
import json
from dataclasses import dataclass, field, asdict
from typing import Any
from enum import Enum

class WorkflowStatus(Enum):
    STARTED = "started"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class WorkflowEvent:
    workflow_id: str
    step: str
    status: WorkflowStatus
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0
    error: str = ""
    metadata: dict = field(default_factory=dict)

    def to_log(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
```

## 3. 結構化日誌

```python
import logging
import sys

class WorkflowLogger:
    def __init__(self, name: str = "workflow"):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_event(self, event: WorkflowEvent) -> None:
        entry = event.to_log()
        if event.status == WorkflowStatus.FAILED:
            self.logger.error(entry)
        elif event.status == WorkflowStatus.RETRYING:
            self.logger.warning(entry)
        else:
            self.logger.info(entry)
```

## 4. 指標收集

```python
@dataclass
class WorkflowMetrics:
    total_executions: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_duration_ms: float = 0.0
    token_usage: int = 0
    cost_usd: float = 0.0

class MetricsCollector:
    def __init__(self):
        self.metrics: dict[str, WorkflowMetrics] = {}

    def record(
        self, workflow: str, event: WorkflowEvent, tokens: int = 0
    ) -> None:
        if workflow not in self.metrics:
            self.metrics[workflow] = WorkflowMetrics()
        m = self.metrics[workflow]
        m.total_executions += 1
        m.total_duration_ms += event.duration_ms
        m.token_usage += tokens
        m.cost_usd += tokens * 0.000002  # GPT-4o 估算
        if event.status == WorkflowStatus.SUCCESS:
            m.success_count += 1
        elif event.status == WorkflowStatus.FAILED:
            m.failure_count += 1

    def summary(self) -> dict:
        return {
            name: asdict(m)
            for name, m in self.metrics.items()
        }

    def success_rate(self, workflow: str) -> float:
        m = self.metrics.get(workflow)
        if not m or m.total_executions == 0:
            return 1.0
        return m.success_count / m.total_executions
```

## 5. OpenTelemetry 整合

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("workflow.orchestrator")

class TracedWorkflow:
    async def execute_step(
        self, name: str, func: callable, **kwargs
    ) -> Any:
        with tracer.start_as_current_span(
            f"step.{name}",
            attributes={"step_name": name, **kwargs},
        ) as span:
            try:
                result = await func(**kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(
                    Status(StatusCode.ERROR, str(e))
                )
                raise
```

## 6. 儀表板指標

```python
class DashboardExporter:
    def __init__(self, collector: MetricsCollector):
        self.collector = collector

    def prometheus_metrics(self) -> str:
        lines = []
        for wf, m in self.collector.metrics.items():
            lines.append(
                f'workflow_total{{name="{wf}"}} {m.total_executions}'
            )
            lines.append(
                f'workflow_success{{name="{wf}"}} {m.success_count}'
            )
            lines.append(
                f'workflow_duration_ms{{name="{wf}"}} '
                f"{m.total_duration_ms}"
            )
            lines.append(
                f'workflow_token_usage{{name="{wf}"}} {m.token_usage}'
            )
        return "\n".join(lines)
```

## 7. 實務建議

1. **每個工作流實例有唯一 ID**：追蹤端到端執行軌跡
2. **記錄所有 LLM 呼叫的 token 用量**：成本分析必備
3. **設定 SLA 警報**：執行時間超過閾值時自動通知
4. **保留失敗上下文**：便於回放與除錯
5. **逐步取樣**：高頻工作流可採用取樣降低儲存成本

---

**參考資料**
- [OpenTelemetry 分散式追蹤](https://www.google.com/search?q=OpenTelemetry+distributed+tracing+workflow)
- [Prometheus 指標最佳實踐](https://www.google.com/search?q=Prometheus+metrics+best+practices)
- [結構化日誌指南](https://www.google.com/search?q=structured+logging+JSON+workflow)
