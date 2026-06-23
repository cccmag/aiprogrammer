# 協作工作區設計

## 前言

協作工作區是人機共同完成任務的共享空間。設計良好的工作區需要考慮權責分配、溝通機制和任務協調。本文從 Python 角度探討協作工作區的設計模式。

## 任務協調器

```python
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    HUMAN = "human"
    AI = "ai"
    REVIEW = "review"
    DONE = "done"

class Task:
    def __init__(self, tid, description, assigned="ai"):
        self.tid = tid
        self.description = description
        self.assigned = assigned
        self.status = TaskStatus.PENDING
        self.result = None

class CollaborationWorkspace:
    def __init__(self):
        self.tasks = {}
        self.history = []

    def add_task(self, description, assigned="ai"):
        tid = len(self.tasks) + 1
        self.tasks[tid] = Task(tid, description, assigned)
        return tid

    def assign_task(self, tid, assignee):
        task = self.tasks.get(tid)
        if not task:
            return False
        task.assigned = assignee
        task.status = TaskStatus.PENDING
        self.history.append(f"任務 {tid} 分配給 {assignee}")
        return True

    def complete_task(self, tid, result):
        task = self.tasks.get(tid)
        if not task:
            return False
        task.result = result
        if task.assigned == "human" and task.status == TaskStatus.HUMAN:
            task.status = TaskStatus.REVIEW
            self.history.append(f"任務 {tid} 完成，等待 AI 審核")
        else:
            task.status = TaskStatus.DONE
            self.history.append(f"任務 {tid} 已完成")
        return True

    def start_task(self, tid):
        task = self.tasks.get(tid)
        if not task:
            return
        task.status = TaskStatus.AI if task.assigned == "ai" else TaskStatus.HUMAN
        self.history.append(f"開始執行任務 {tid} ({task.description})")

    def get_workload(self):
        return {
            "pending": sum(1 for t in self.tasks.values()
                          if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in self.tasks.values()
                              if t.status in (TaskStatus.HUMAN, TaskStatus.AI)),
            "review": sum(1 for t in self.tasks.values()
                         if t.status == TaskStatus.REVIEW),
            "done": sum(1 for t in self.tasks.values()
                       if t.status == TaskStatus.DONE),
        }

ws = CollaborationWorkspace()
ws.add_task("分析客戶數據", "ai")
ws.add_task("審閱合約條款", "human")
ws.start_task(1)
ws.complete_task(1, {"average_spend": 3200})
print(ws.get_workload())
```

## 即時通訊機制

```python
import asyncio
from datetime import datetime

class Message:
    def __init__(self, sender, content, msg_type="text"):
        self.sender = sender
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now()

class CollaborationChannel:
    def __init__(self):
        self.messages = []
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def send(self, sender, content, msg_type="text"):
        msg = Message(sender, content, msg_type)
        self.messages.append(msg)
        for cb in self.subscribers:
            cb(msg)
        return msg

    def get_context(self, limit=10):
        return [
            {"sender": m.sender, "content": m.content}
            for m in self.messages[-limit:]
        ]

class AIAgent:
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        channel.subscribe(self.on_message)

    def on_message(self, msg):
        if msg.sender == self.name:
            return
        if "分析" in msg.content:
            self.channel.send(self.name, f"AI {self.name} 正在分析資料...")
            self.channel.send(self.name, "分析完成：趨勢向上")

channel = CollaborationChannel()
agent = AIAgent("分析師", channel)
channel.send("使用者", "請分析本月數據")
for m in channel.messages:
    print(f"{m.sender}: {m.content}")
```

---

**延伸閱讀**

- [Collaborative Workspace Design](https://www.google.com/search?q=collaborative+workspace+design+human+AI)
- [Real-time Collaboration Systems](https://www.google.com/search?q=real+time+collaboration+system+design)
- [Human-AI Task Allocation](https://www.google.com/search?q=human+AI+task+allocation+framework)
