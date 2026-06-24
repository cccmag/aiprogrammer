# Agent 之間的協作協議

## 前言

單一 Agent 的能力有限，多 Agent 協作才能完成複雜任務。Agent 協作協議定義了 Agent 之間如何溝通、分工、同步與結算。2026 年的主流協議包括 ANP（Agent Negotiation Protocol）與 FIPA 相容的互動模式。

## 協作模型

Agent 協作通常遵循「提出→投標→分配→執行→結算」的五階段模式：

```python
import time, uuid
from dataclasses import dataclass, field
from enum import Enum

class TaskStatus(Enum):
    PROPOSED = 1
    BIDDING = 2
    ASSIGNED = 3
    IN_PROGRESS = 4
    COMPLETED = 5
    FAILED = 6

@dataclass
class CollaborativeTask:
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    description: str = ""
    subtasks: list[str] = field(default_factory=list)
    reward: float = 0.0
    status: TaskStatus = TaskStatus.PROPOSED
    assigned_to: str = ""
    created_at: float = field(default_factory=time.time)
```

## 協作協議實作

一個簡單的 Contract Net 協定實作——任務發布者廣播任務，Agent 投標，發布者選擇最佳投標者：

```python
@dataclass
class Bid:
    agent_id: str
    task_id: str
    price: float
    estimated_hours: float

class CollaborationProtocol:
    def __init__(self):
        self.tasks: dict[str, CollaborativeTask] = {}
        self.bids: dict[str, list[Bid]] = {}
    def propose_task(self, task: CollaborativeTask):
        task.status = TaskStatus.BIDDING
        self.tasks[task.task_id] = task
        self.bids[task.task_id] = []
    def submit_bid(self, bid: Bid):
        if bid.task_id in self.bids:
            self.bids[bid.task_id].append(bid)
    def assign_task(self, task_id: str):
        bids = self.bids.get(task_id, [])
        if not bids:
            return None
        best = min(bids, key=lambda b: b.price * b.estimated_hours)
        task = self.tasks[task_id]
        task.assigned_to = best.agent_id
        task.status = TaskStatus.ASSIGNED
        return best
    def complete_task(self, task_id: str):
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
```

## 參考資料

- https://www.google.com/search?q=agent+collaboration+protocol+Contract+Net
- https://www.google.com/search?q=FIPA+agent+communication+language+2026
- https://www.google.com/search?q=multi+agent+task+allocation+algorithm
