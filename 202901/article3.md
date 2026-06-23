# Agent 編排模式：Sequential / Fan-out / Debate

## 1. 引言

當工作流需要協調多個 AI Agent 時，編排模式決定了代理人如何互動、共享資訊與達成共識。本文介紹三種核心編排模式：Sequential、Fan-out 與 Debate。

## 2. Sequential 模式

最基礎的模式，Agent 們如同組裝線依序執行，前一個的輸出是下一個的輸入。

```python
from typing import Any, Callable
import asyncio

class SequentialPipeline:
    def __init__(self):
        self.steps: list[Callable] = []

    def add_step(self, fn: Callable) -> "SequentialPipeline":
        self.steps.append(fn)
        return self

    async def execute(self, initial_input: Any) -> Any:
        result = initial_input
        for i, step in enumerate(self.steps):
            print(f"[步驟 {i+1}/{len(self.steps)}] 執行中...")
            result = await step(result)
        return result

# 使用範例
async def main():
    pipe = SequentialPipeline()
    pipe.add_step(lambda x: f"分析: {x}")
    pipe.add_step(lambda x: f"處理: {x}")
    pipe.add_step(lambda x: f"總結: {x}")
    result = await pipe.execute("原始資料")
    print(result)
```

Sequential 模式**簡單可靠**，適合步驟間依賴性強的工作流，但無法平行化，吞吐量受限。

## 3. Fan-out 模式

多個 Agent 並行處理同一份輸入，適合需要多元觀點或平行處理的場景。

```python
class FanOutOrchestrator:
    def __init__(self):
        self.workers: list[Callable] = []

    def add_worker(self, fn: Callable) -> "FanOutOrchestrator":
        self.workers.append(fn)
        return self

    async def execute(self, input_data: Any) -> list[Any]:
        tasks = [worker(input_data) for worker in self.workers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

class FanInAggregator:
    async def aggregate(
        self, results: list[Any]
    ) -> str:
        valid = [r for r in results if not isinstance(r, Exception)]
        return f"彙總 {len(valid)} 個結果:\n" + "\n".join(str(r) for r in valid)

# 使用範例
async def main():
    orchestrator = FanOutOrchestrator()
    orchestrator.add_worker(lambda x: f"分析師 A: {x}")
    orchestrator.add_worker(lambda x: f"分析師 B: {x}")
    orchestrator.add_worker(lambda x: f"分析師 C: {x}")
    results = await orchestrator.execute("市場報告")
    aggregator = FanInAggregator()
    print(await aggregator.aggregate(results))
```

Fan-out 模式**大幅提升吞吐量**，但需要處理部分工作失敗的情況，且 Fan-in 階段的聚合邏輯需謹慎設計。

## 4. Debate 模式

Agent 們扮演不同觀點的辯論者，透過多輪互動達到共識或凸顯分歧。

```python
class DebateAgent:
    def __init__(self, name: str, stance: str):
        self.name = name
        self.stance = stance

    async def argue(self, topic: str, opponent: str) -> str:
        return f"{self.name}({self.stance}): 針對 {opponent} 的論點，我認為..."

class DebateOrchestrator:
    def __init__(self, rounds: int = 3):
        self.agents: list[DebateAgent] = []
        self.rounds = rounds

    def add_agent(self, agent: DebateAgent) -> "DebateOrchestrator":
        self.agents.append(agent)
        return self

    async def debate(self, topic: str) -> list[str]:
        transcript = []
        for r in range(self.rounds):
            print(f"\n=== 第 {r+1} 輪 ===")
            for agent in self.agents:
                opponents = [
                    a.name for a in self.agents if a.name != agent.name
                ]
                arg = await agent.argue(topic, ", ".join(opponents))
                transcript.append(arg)
                print(arg)
        return transcript
```

Debate 模式**能產出更高品質的決策**，因為 Agent 透過彼此挑戰來修正盲點。但成本是 N 倍於單 Agent 的 LLM 呼叫，適合高風險決策場景。

## 5. 混合編排實務

實務上常混合使用三種模式：

```python
class HybridOrchestrator:
    async def execute_complex_task(self, task: dict) -> dict:
        # 1. Sequential：任務分解
        subtasks = await self._decompose(task)

        # 2. Fan-out：平行分析
        analyses = await asyncio.gather(
            *[self._analyze(s) for s in subtasks]
        )

        # 3. Debate：關鍵決策
        decision = await self._debate_critical(analyses)

        return decision
```

## 6. 選擇指南

| 模式 | 適合場景 | 成本 | 延遲 |
|------|---------|------|------|
| Sequential | 依賴性強、流程固定 | 低 | 高 (線性) |
| Fan-out | 獨立分析、多元觀點 | 中 | 低 (並行) |
| Debate | 高風險、需共識 | 高 | 高 (多輪) |

---

**參考資料**
- [Agent 編排模式指南](https://www.google.com/search?q=AI+agent+orchestration+patterns+sequential+fanout+debate)
- [多 Agent 辯論研究](https://www.google.com/search?q=multi+agent+debate+consensus+LLM)
- [Fan-out/Fan-in 架構](https://www.google.com/search?q=fan+out+fan+in+pattern+distributed+systems)
