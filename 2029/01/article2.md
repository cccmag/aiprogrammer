# 人機協作工作流設計

## 1. 引言

AI 代理並非總是能獨立完成所有任務。在關鍵決策、倫理判斷或低信度場景中，將人類納入工作流是提升可靠性的必要手段。本文探討人機協作工作流的設計模式與實作方式。

## 2. 人在迴圈 (Human-in-the-Loop)

HITL 是最基本的人機協作模式：AI 代理在遇到不確定的情況時，暫停執行並等待人類審核。

```python
from enum import Enum
from typing import Optional

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class HumanInTheLoop:
    def __init__(self):
        self.status: dict[str, ApprovalStatus] = {}

    async def request_approval(
        self, task_id: str, context: dict
    ) -> ApprovalStatus:
        self.status[task_id] = ApprovalStatus.PENDING
        print(f"[審核請求] 任務 {task_id}")
        print(f"  上下文: {context}")
        print(f"  請輸入 'y' 核准 / 'n' 拒絕: ", end="")

        while self.status[task_id] == ApprovalStatus.PENDING:
            user_input = await self._wait_for_input()
            if user_input == "y":
                self.status[task_id] = ApprovalStatus.APPROVED
            elif user_input == "n":
                self.status[task_id] = ApprovalStatus.REJECTED

        return self.status[task_id]

    async def _wait_for_input(self) -> str:
        import asyncio
        return await asyncio.to_thread(input)
```

## 3. 信心值閘道模式

更進階的做法是讓 AI 代理自我評估信心值，只在低信心時請求人類介入。

```python
class ConfidenceGate:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    async def decide(self, agent_output: dict) -> str:
        confidence = agent_output.get("confidence", 0.0)
        if confidence >= self.threshold:
            return "auto_proceed"
        if confidence >= self.threshold * 0.5:
            return "review_suggested"
        return "human_required"

    async def execute(self, agent_output: dict) -> str:
        decision = await self.decide(agent_output)
        if decision == "auto_proceed":
            print(f"[自動] 信心 {agent_output['confidence']:.2f}，直接執行")
            return agent_output["action"]
        if decision == "review_suggested":
            print(f"[建議審查] 信心 {agent_output['confidence']:.2f}")
            return await self._human_review(agent_output)
        return await self._human_decide(agent_output)
```

## 4. 例外處理設計

```python
class EscalationPolicy:
    def __init__(self):
        self.escalation_chain = ["team_lead", "manager", "compliance"]

    async def handle_exception(
        self, error: Exception, context: dict
    ) -> dict:
        for level in self.escalation_chain:
            print(f"[升級] 通知 {level}: {str(error)[:50]}")
            result = await self._notify(level, context)
            if result.get("resolved"):
                return result
        raise RuntimeError("所有升級層級均無法處理")
```

## 5. 非同步審核佇列

在生產環境中，使用訊息佇列管理審核請求，允許人類操作員以非同步方式處理。

```python
import asyncio
from dataclasses import dataclass

@dataclass
class ReviewTask:
    id: str
    payload: dict
    callback_url: str

class ReviewQueue:
    def __init__(self):
        self.queue: asyncio.Queue[ReviewTask] = asyncio.Queue()

    async def submit(self, task: ReviewTask) -> None:
        await self.queue.put(task)

    async def process_reviews(self) -> None:
        while True:
            task = await self.queue.get()
            print(f"[佇列] 處理審核 {task.id}")
            decision = await self._get_operator_decision(task)
            await self._callback(task.callback_url, decision)
```

## 6. 設計原則

1. **最小干預原則**：只在 AI 無法處理的邊界案例請求人類介入
2. **上下文完整**：提供足夠的決策背景資訊，降低人類認知負荷
3. **超時處理**：人類審核應有超時機制，避免工作流無限等待
4. **審計軌跡**：所有人工決策應記錄留存，供後續分析與合規使用

---

**參考資料**
- [Human-in-the-Loop 設計模式](https://www.google.com/search?q=Human+in+the+Loop+HITL+workflow+design)
- [信心校準與閘道策略](https://www.google.com/search?q=AI+confidence+threshold+human+review)
- [非同步審核架構](https://www.google.com/search?q=asynchronous+approval+queue+workflow)
