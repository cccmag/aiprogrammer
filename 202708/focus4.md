# Agent 通訊協議（2020-2026）

## 訊息格式設計

Agent 之間的通訊需要結構化的訊息格式。JSON 是最常見的選擇，但在高效能場景下 Protocol Buffers 更適合：

```python
# Agent 訊息結構（JSON）
message = {
    "id": "msg_001",
    "sender": "orchestrator",
    "receiver": "coder_agent",
    "type": "task_assignment",
    "payload": {
        "task_id": "t_42",
        "description": "實作使用者登入 API",
        "dependencies": ["t_40", "t_41"],
        "deadline": "2026-08-15T10:00:00Z"
    },
    "metadata": {
        "priority": "high",
        "ttl": 300,
        "conversation_id": "conv_007"
    },
    "signature": "..."  # 可選的數位簽章
}
```

```python
# Protocol Buffers 定義（高效能場景）
"""
message AgentMessage {
    string id = 1;
    string sender = 2;
    string receiver = 3;
    MessageType type = 4;
    bytes payload = 5;
    map<string, string> metadata = 6;
    int64 timestamp = 7;
}
"""
```

## 同步 vs 非同步通訊

兩種模式適用於不同場景：

| 特性 | 同步（Request-Reply） | 非同步（Message Queue） |
|------|---------------------|----------------------|
| 延遲 | 低（直接回應） | 較高（佇列緩衝） |
| 耦合度 | 高（雙方需同時在線） | 低（可離線處理） |
| 使用場景 | 快速查詢、函數呼叫 | 長時間任務、事件廣播 |
| 容錯 | 呼叫方需處理 timeout | 佇列自動重試 |

```python
import asyncio
from queue import Queue

class AsyncMessageBus:
    def __init__(self):
        self.queues = {}  # agent_name -> Queue

    def register(self, agent_name: str):
        self.queues[agent_name] = Queue()

    def send(self, receiver: str, message: dict):
        if receiver in self.queues:
            self.queues[receiver].put(message)

    def broadcast(self, message: dict, exclude: str = None):
        for name, queue in self.queues.items():
            if name != exclude:
                queue.put(message)

    async def poll(self, agent_name: str, timeout: float = 1.0) -> dict:
        queue = self.queues.get(agent_name)
        if not queue:
            raise ValueError(f"Unknown agent: {agent_name}")
        return queue.get(timeout=timeout)
```

## A2A（Agent-to-Agent）通訊標準

2025 年 Google 發布的 Agent2Agent Protocol（A2A）是首個跨平台 Agent 通訊標準。其核心概念：

**Agent Card**：每個 Agent 發布一個「能力卡片」描述自身能力：

```python
agent_card = {
    "agent": {"name": "code_reviewer", "version": "2.1.0"},
    "capabilities": [
        {"name": "review_code", "description": "審查程式碼品質"},
        {"name": "check_security", "description": "掃描安全漏洞"}
    ],
    "skills": ["Python", "JavaScript", "Rust"],
    "auth": {"type": "api_key", "endpoint": "https://..."}
}
```

A2A 的互動流程：

```
Agent A → 發現 Agent B（查詢 Agent Card）
       → 發送任務（POST /tasks）
       → 接收回應（streaming 或 polling）
       → 確認完成
```

## 協定模式

### Request-Reply

最簡單的模式。一個 Agent 發送請求，另一個回應：

```python
def request_reply(bus, sender, receiver, request):
    bus.send(receiver, {
        "type": "request",
        "sender": sender,
        "payload": request,
        "reply_to": sender
    })
    response = bus.poll(sender, timeout=30)
    return response["payload"]
```

### Publish-Subscribe

一對多通訊。發布者不知道誰會接收訊息：

```python
class PubSubBus:
    def __init__(self):
        self.topics = {}

    def subscribe(self, agent: str, topic: str):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(agent)

    def publish(self, topic: str, message: dict):
        for agent in self.topics.get(topic, []):
            self.send(agent, message)

# 範例：日志 Agent 監聽所有事件
bus.subscribe("logger", "system.event")
bus.subscribe("logger", "agent.error")
bus.publish("agent.error", {"code": 500, "message": "LLM timeout"})
```

### Event-Driven

Agent 響應特定事件觸發行動。適合自主行為的 Agent：

```python
class EventDrivenAgent:
    def __init__(self, name: str):
        self.name = name
        self.handlers = {}

    def on(self, event_type: str, handler):
        self.handlers[event_type] = handler

    def receive_event(self, event: dict):
        handler = self.handlers.get(event["type"])
        if handler:
            return handler(event["data"])
        return None

# 事件驅動的工作流程
review_agent = EventDrivenAgent("reviewer")
review_agent.on("code.submitted", lambda data: review_code(data))
review_agent.on("review.finished", lambda data: notify_author(data))
```

---

**下一步**：[多 Agent 除錯與可觀測性](focus5.md)

## 延伸閱讀

- [Google A2A Protocol](https://www.google.com/search?q=Google+Agent2Agent+protocol)
- [Agent 訊息傳遞模式](https://www.google.com/search?q=agent+communication+patterns+LLM)
- [Protocol Buffers Agent](https://www.google.com/search?q=protobuf+agent+communication)
