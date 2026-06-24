# AI 原生應用的架構模式

## 前言

AI 原生應用不是簡單地呼叫 LLM API，而是從架構層面將 AI 整合為核心元件。本文探討三種主流架構模式。

## 模式一：Chain Pipeline

將 AI 處理流程拆解為多個串聯步驟，每個步驟由一個獨立的 LLM 呼叫或傳統邏輯處理：

```python
from dataclasses import dataclass

@dataclass
class ChainContext:
    query: str
    context: str = ""
    draft: str = ""
    final: str = ""

class PipelineStep:
    async def execute(self, ctx: ChainContext) -> ChainContext:
        raise NotImplementedError

class RetrieverStep(PipelineStep):
    async def execute(self, ctx: ChainContext) -> ChainContext:
        ctx.context = await search_knowledge_base(ctx.query)
        return ctx

class DraftStep(PipelineStep):
    async def execute(self, ctx: ChainContext) -> ChainContext:
        ctx.draft = await call_llm(
            f"根據以下資料回答問題：\n{ctx.context}\n\n問題：{ctx.query}"
        )
        return ctx

class PolishStep(PipelineStep):
    async def execute(self, ctx: ChainContext) -> ChainContext:
        ctx.final = await call_llm(
            f"潤飾以下回答，使其更流暢專業：\n{ctx.draft}"
        )
        return ctx

class ChainPipeline:
    def __init__(self):
        self.steps = [RetrieverStep(), DraftStep(), PolishStep()]

    async def run(self, query: str) -> str:
        ctx = ChainContext(query=query)
        for step in self.steps:
            ctx = await step.execute(ctx)
        return ctx.final
```

## 模式二：Agentic Loop

以 LLM 作為決策核心，動態決定下一步行動：

```python
import json
from typing import Callable

class Tool:
    def __init__(self, name: str, fn: Callable, description: str):
        self.name = name
        self.fn = fn
        self.description = description

class Agent:
    def __init__(self, tools: list[Tool], max_steps: int = 10):
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps

    async def run(self, task: str) -> str:
        messages = [{"role": "user", "content": task}]
        for _ in range(self.max_steps):
            response = await call_llm(messages, tools=list(self.tools.values()))
            if response.get("content"):
                return response["content"]
            tool_call = json.loads(response["tool_calls"])
            result = self.tools[tool_call["name"]].fn(**tool_call["args"])
            messages.append({"role": "tool", "content": result})
        return "Max steps reached"
```

## 模式三：Event-Driven Architecture

透過事件匯流排非同步驅動 AI 處理：

```python
import asyncio
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.handlers = defaultdict(list)

    def on(self, event: str):
        def wrapper(fn):
            self.handlers[event].append(fn)
            return fn
        return wrapper

    async def emit(self, event: str, data: dict):
        for handler in self.handlers[event]:
            asyncio.create_task(handler(data))

bus = EventBus()

@bus.on("user_message")
async def handle_message(data: dict):
    intent = await classify_intent(data["text"])
    if intent == "question":
        await bus.emit("question", data)
    elif intent == "command":
        await bus.emit("command", data)

@bus.on("question")
async def answer_question(data: dict):
    answer = await call_llm(f"回答：{data['text']}")
    await bus.emit("response", {"answer": answer, "user_id": data["user_id"]})
```

## 選擇指南

| 模式 | 適用場景 | 複雜度 |
|------|---------|--------|
| Chain Pipeline | 流程固定、步驟明確 | 低 |
| Agentic Loop | 動態決策、多工具呼叫 | 中 |
| Event-Driven | 高併發、非同步處理 | 高 |

## 結語

選擇架構模式時，應根據應用的複雜度、延遲要求和維護成本來決定。建議從 Chain Pipeline 開始，逐步引入 Agentic Loop 和 Event-Driven 模式。

---

**延伸閱讀**

- [LLM 應用架構模式](https://www.google.com/search?q=LLM+application+architecture+patterns)
- [LangChain 架構解析](https://www.google.com/search?q=LangChain+architecture)
- [事件驅動架構設計](https://www.google.com/search?q=event+driven+architecture+patterns)
