# 工作流編排工具

## 從單一 Agent 到多步驟工作流

複雜任務需拆解為多個步驟：規劃 → 執行 → 驗證 → 迭代。工作流編排工具管理這些步驟的順序與資料傳遞。

## 圖形化工作流設計

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class WorkflowStep:
    name: str
    action: Callable
    depends_on: list[str] = None
    retry: int = 3

class WorkflowEngine:
    def __init__(self):
        self.steps = {}
        self.results = {}

    def add_step(self, step: WorkflowStep):
        self.steps[step.name] = step

    def run(self, initial_input):
        pending = set(self.steps.keys())
        while pending:
            ready = {n for n in pending
                     if all(d in self.results for d in
                            (self.steps[n].depends_on or []))}
            for name in ready:
                step = self.steps[name]
                inputs = {d: self.results[d]
                          for d in (step.depends_on or [])}
                for attempt in range(step.retry):
                    try:
                        self.results[name] = step.action(inputs)
                        break
                    except Exception as e:
                        if attempt == step.retry - 1:
                            raise
            pending -= ready
        return self.results
```

## DAG 執行範例

```python
engine = WorkflowEngine()

def search_web(ctx):
    return web_search(ctx["query"])

def extract_sources(ctx):
    return parse_urls(ctx["search_web"])

def generate_report(ctx):
    return llm.summarize(ctx["extract_sources"])

engine.add_step(WorkflowStep("search_web", search_web))
engine.add_step(WorkflowStep("extract_sources", extract_sources,
                              depends_on=["search_web"]))
engine.add_step(WorkflowStep("generate_report", generate_report,
                              depends_on=["extract_sources"]))

result = engine.run({"query": "2026 AI 發展趨勢"})
```

## 條件分支與循環

進階引擎支援條件判斷（if-else）與循環（for-each）。可參考 LangGraph 與 Temporal.io 的設計理念，詳見 https://www.google.com/search?q=LLM+workflow+orchestration+tool。
