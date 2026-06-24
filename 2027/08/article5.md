# 多 Agent 工作流設計模式

## 前言

多 Agent 系統的威力來自於 Agent 之間的協作方式。不同的工作流模式適用於不同的場景——從簡單的序列執行到複雜的辯論反思。本文將介紹六種經典的工作流設計模式，並提供完整的 Python 實作。

---

## 一、序列模式（Sequential）

### 1.1 Chain of Agents

最簡單的模式，Agent 按照固定順序依次處理：

```python
from dataclasses import dataclass, field
from typing import List, Callable

@dataclass
class Agent:
    name: str
    system_prompt: str
    llm: Callable

    def process(self, input_text: str) -> str:
        prompt = f"{self.system_prompt}\n\n輸入：{input_text}"
        return self.llm(prompt)

class SequentialWorkflow:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, initial_input: str) -> str:
        output = initial_input
        for agent in self.agents:
            print(f"─── {agent.name} 處理中 ───")
            output = agent.process(output)
        return output

# 使用範例
researcher = Agent(
    name="研究員",
    system_prompt="搜尋並整理相關資料。",
    llm=call_llm,
)
writer = Agent(
    name="撰寫者",
    system_prompt="根據資料撰寫文章。",
    llm=call_llm,
)
editor = Agent(
    name="編輯",
    system_prompt="校對並修改文章。",
    llm=call_llm,
)

workflow = SequentialWorkflow([researcher, writer, editor])
result = workflow.run("寫一篇關於量子計算的科普文章")
```

---

## 二、扇出/扇入模式（Fan-out / Fan-in）

多個 Agent 並行處理，再匯總結果：

```python
import asyncio
from typing import List

class FanOutFanInWorkflow:
    def __init__(self, workers: List[Agent], aggregator: Agent):
        self.workers = workers
        self.aggregator = aggregator

    async def _run_worker(self, agent: Agent, task: str) -> str:
        return agent.process(task)

    async def run(self, task: str, subtasks: List[str]) -> str:
        # Fan-out：所有 worker 並行處理
        results = await asyncio.gather(
            *[self._run_worker(w, t) for w, t in zip(self.workers, subtasks)]
        )

        # Fan-in：匯總到 aggregator
        combined = "\n\n".join(
            f"## {w.name} 的結果\n{r}"
            for w, r in zip(self.workers, results)
        )
        final = self.aggregator.process(
            f"原始任務：{task}\n\n各 worker 結果：\n{combined}\n\n請整合為最終答案。"
        )
        return final

# 使用範例
async def main():
    workflow = FanOutFanInWorkflow(
        workers=[
            Agent("市場分析", "分析市場趨勢", call_llm),
            Agent("技術評估", "評估技術可行性", call_llm),
            Agent("風險分析", "識別潛在風險", call_llm),
        ],
        aggregator=Agent("整合者", "整合多份報告", call_llm),
    )
    result = await workflow.run(
        task="評估推出新產品的可行性",
        subtasks=[
            "分析 2027 年 AI 晶片市場規模",
            "評估 RISC-V 架構的技術成熟度",
            "分析供應鏈中斷風險",
        ],
    )
```

---

## 三、辯論模式（Debate）

多個 Agent 持不同觀點辯論，產生更全面的結論：

```python
class DebateWorkflow:
    def __init__(self, agents: List[Agent], rounds: int = 3):
        self.agents = agents
        self.rounds = rounds

    def run(self, topic: str) -> str:
        statements = [f"請就以下主題提出你的觀點：{topic}"]
        print(f"辯論主題：{topic}")

        for r in range(self.rounds):
            print(f"\n=== 第 {r+1} 輪 ===")
            new_statements = []
            for agent in self.agents:
                context = "\n".join(
                    f"{a.name}（第 {i+1} 輪）：{s}"
                    for a, s in zip(self.agents, statements)
                )
                prompt = (
                    f"你是 {agent.name}。\n"
                    f"辯論主題：{topic}\n\n"
                    f"歷史發言：\n{context}\n\n"
                    f"請回應並反駁對手的觀點。"
                )
                response = agent.llm(prompt)
                new_statements.append(response)
                print(f"{agent.name}：{response[:80]}...")
            statements = new_statements

        # 最終總結
        summary_agent = self.agents[0]
        summary = summary_agent.llm(
            f"請總結辯論共識：\n{chr(10).join(statements)}"
        )
        return summary
```

---

## 四、反思模式（Reflection）

Agent 對自己的輸出進行自我審查和改進：

```python
class ReflectionWorkflow:
    def __init__(self, generator: Agent, critic: Agent, max_iterations: int = 3):
        self.generator = generator
        self.critic = critic
        self.max_iterations = max_iterations

    def run(self, task: str) -> str:
        current = self.generator.process(task)

        for i in range(self.max_iterations):
            feedback = self.critic.process(
                f"請審查以下內容，指出問題和改進建議：\n\n{current}"
            )
            print(f"反饋 {i+1}：{feedback[:100]}...")

            current = self.generator.process(
                f"原始任務：{task}\n\n"
                f"之前的版本：\n{current}\n\n"
                f"審查意見：\n{feedback}\n\n"
                f"請根據審查意見改進。"
            )

        return current
```

---

## 五、批評-修改模式（Critique-Revise）

專為程式碼生成設計的模式，reviewer 和 coder 交替運作：

```python
class CodeReviewWorkflow:
    def __init__(self, coder: Agent, reviewer: Agent):
        self.coder = coder
        self.reviewer = reviewer

    def run(self, requirement: str, max_rounds: int = 5) -> dict:
        code = self.coder.process(
            f"請根據以下需求撰寫 Python 程式碼：\n{requirement}"
        )

        history = [{"role": "coder", "content": code}]

        for r in range(max_rounds):
            review = self.reviewer.process(
                f"請審查以下程式碼的正確性、效能和安全性：\n{code}"
            )
            history.append({"role": "reviewer", "content": review})

            if "無問題" in review or "已通過" in review:
                return {"code": code, "rounds": r + 1, "status": "approved"}

            code = self.coder.process(
                f"原始需求：{requirement}\n\n"
                f"當前程式碼：\n{code}\n\n"
                f"審查意見：\n{review}\n\n"
                f"請根據審查意見修改程式碼。"
            )
            history.append({"role": "coder", "content": code})

        return {"code": code, "rounds": max_rounds, "status": "max_rounds"}
```

---

## 六、DAG 式工作流

使用有向無環圖來定義更複雜的工作流：

```python
from collections import deque

class DAGWorkflow:
    def __init__(self):
        self.nodes: dict = {}
        self.edges: dict = {}  # node -> [dependencies]

    def add_node(self, name: str, agent: Agent):
        self.nodes[name] = agent
        self.edges[name] = []

    def add_edge(self, from_node: str, to_node: str):
        self.edges[to_node].append(from_node)

    def run(self, inputs: dict) -> dict:
        """inputs: {node_name: input_text}"""
        results = {}
        # 拓撲排序
        in_degree = {n: len(deps) for n, deps in self.edges.items()}
        queue = deque([n for n, d in in_degree.items() if d == 0])

        while queue:
            node = queue.popleft()
            agent = self.nodes[node]
            node_input = inputs.get(node, "")

            # 收集依賴節點的輸出作為輸入
            dep_outputs = "\n".join(
                f"{dep} 輸出：{results[dep]}"
                for dep in self.edges[node]
                if dep in results
            )
            if dep_outputs:
                node_input = f"{dep_outputs}\n\n任務：{node_input}"

            results[node] = agent.process(node_input)
            print(f"{node} 完成")

            # 更新入度
            for n, deps in self.edges.items():
                if node in deps:
                    in_degree[n] -= 1
                    if in_degree[n] == 0:
                        queue.append(n)

        return results
```

---

## 七、錯誤處理與重試

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_attempts - 1:
                        raise
                    print(f"重試 {i+1}/{max_attempts}：{e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class ResilientWorkflow:
    def __init__(self, workflow, max_retries: int = 3):
        self.workflow = workflow
        self.max_retries = max_retries

    @retry(max_attempts=3)
    def run_with_retry(self, task: str) -> str:
        result = self.workflow.run(task)
        if not result:
            raise ValueError("Workflow 回傳空結果")
        return result
```

---

## 結語

選擇正確的工作流模式取決於你的具體場景：序列模式適合管線處理，扇出/扇入模式適合並行探索，辯論模式適合需要多角度分析的決策場景，反思和批評-修改模式適合品質敏感的輸出。複雜的場景可以組合使用多種模式，建構出強大的多 Agent 協作系統。

---

**參考資料**

- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", https://arxiv.org/abs/2201.11903
- LangGraph 工作流文檔：https://langchain-ai.github.io/langgraph/
- AutoGen 工作流模式：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/workflow-patterns.html
