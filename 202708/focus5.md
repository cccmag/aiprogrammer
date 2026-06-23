# 多 Agent 除錯與可觀測性（2022-2026）

## Agent 軌跡記錄（Trajectory Logging）

多 Agent 系統的除錯遠比單一 Agent 困難——問題可能出在任何一個 Agent 的推理過程、工具使用、或是 Agent 之間的通訊。軌跡記錄是除錯的第一道防線：

```python
import json
from datetime import datetime, timezone

class TrajectoryLogger:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.events = []

    def log(self, event_type: str, data: dict):
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": self.agent_name,
            "type": event_type,
            "data": data
        })

    def log_llm_call(self, messages: list, response: str):
        self.log("llm_call", {
            "messages": messages,
            "response": response,
            "tokens": {"input": len(str(messages)), "output": len(response)}
        })

    def log_tool_call(self, tool_name: str, args: dict, result: str):
        self.log("tool_call", {
            "tool": tool_name,
            "arguments": args,
            "result": result[:500]  # 避免記錄過大
        })

    def export(self) -> str:
        return json.dumps(self.events, ensure_ascii=False, indent=2)

# 在 Agent 中使用
class ObservableAgent(Agent):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.logger = TrajectoryLogger(name)

    def run(self, task: str) -> str:
        self.logger.log("task_start", {"task": task})
        response = super().run(task)
        self.logger.log("task_end", {"response": response})
        return response
```

## 訊息流可視化工具

多 Agent 系統的除錯需要看到「誰跟誰說了什麼」。使用有向圖可視化訊息流：

```python
class MessageFlowGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = []  # (sender, receiver, message_type)

    def record_message(self, sender: str, receiver: str,
                       msg_type: str, content: str):
        self.nodes.add(sender)
        self.nodes.add(receiver)
        self.edges.append((sender, receiver, msg_type, content))

    def to_mermaid(self) -> str:
        # 生成 Mermaid 流程圖
        lines = ["flowchart TD"]
        for node in self.nodes:
            lines.append(f"    {node}[{node}]")

        for sender, receiver, msg_type, _ in self.edges:
            lines.append(f"    {sender} -->|{msg_type}| {receiver}")

        return "\n".join(lines)
```

生成的 Mermaid 圖可以直接嵌入 Markdown，視覺化整個協作過程。

## 重放（Replay）除錯策略

重放是除錯多 Agent 系統最有效的手段：記錄所有輸入，然後逐步重放，觀察每個決策點：

```python
class ReplayDebugger:
    def __init__(self, trajectory: list):
        self.trajectory = trajectory
        self.position = 0
        self.breakpoints = set()

    def add_breakpoint(self, event_type: str):
        self.breakpoints.add(event_type)

    def step(self) -> dict:
        if self.position >= len(self.trajectory):
            return None

        event = self.trajectory[self.position]
        self.position += 1

        if event["type"] in self.breakpoints:
            print(f"🛑 中斷點：{event['type']}")
            print(f"   時間：{event['timestamp']}")
            print(f"   Agent：{event['agent']}")
            input("按 Enter 繼續...")

        return event

    def rewind(self, steps: int = 1):
        self.position = max(0, self.position - steps)

    def search(self, agent_name: str = None,
               event_type: str = None) -> list:
        results = []
        for event in self.trajectory:
            if agent_name and event["agent"] != agent_name:
                continue
            if event_type and event["type"] != event_type:
                continue
            results.append(event)
        return results
```

## 多 Agent 系統評估指標

評估多 Agent 系統比單一 Agent 更複雜——除了個別 Agent 的準確率，還需要衡量協作效率：

| 指標 | 定義 | 計算方式 |
|------|------|---------|
| 任務完成率 | 成功完成的任務比例 | 完成數 / 總任務數 |
| 協作開銷 | Agent 間通訊的成本 | 訊息數 / 任務數 |
| 衝突率 | Agent 間產生意見分歧的頻率 | 衝突次數 / 互動次數 |
| 恢復時間 | 從錯誤中恢復所需的步數 | 平均重試次數 |
| 工具利用率 | Agent 使用工具的效率 | 有效工具呼叫 / 總工具呼叫 |

```python
class SystemEvaluator:
    def __init__(self):
        self.metrics = {
            "tasks_completed": 0,
            "tasks_total": 0,
            "messages_sent": 0,
            "conflicts": 0,
            "retries": 0
        }

    def evaluate(self, trajectory: list) -> dict:
        for event in trajectory:
            if event["type"] == "task_end":
                self.metrics["tasks_total"] += 1
                if event["data"].get("success"):
                    self.metrics["tasks_completed"] += 1
            elif event["type"] == "message":
                self.metrics["messages_sent"] += 1
            elif event["type"] == "conflict":
                self.metrics["conflicts"] += 1
            elif event["type"] == "retry":
                self.metrics["retries"] += 1

        total = self.metrics["tasks_total"]
        if total == 0:
            return self.metrics

        return {
            **self.metrics,
            "task_completion_rate": self.metrics["tasks_completed"] / total,
            "avg_messages_per_task": self.metrics["messages_sent"] / total,
            "conflict_rate": self.metrics["conflicts"] / total
        }
```

---

**下一步**：[安全與治理](focus6.md)

## 延伸閱讀

- [LangSmith Agent 追蹤](https://www.google.com/search?q=LangSmith+agent+trajectory+logging)
- [多 Agent 可觀測性](https://www.google.com/search?q=multi+agent+observability+tracing)
- [Agent 評估框架](https://www.google.com/search?q=LLM+agent+evaluation+benchmark)
