# 實作一個小型 Agent 框架

## 前言

理論說得再多，不如親手實作一個 AI Agent 框架。本篇文章將帶領讀者從零開始，用 Python 實作一個名為「MiniAgent」的小型 ReAct Agent 框架。

MiniAgent 支援：
- ReAct 循環（思考 → 行動 → 觀察）
- 工具註冊與執行
- 簡單的記憶系統
- 多代理團隊協作
- 模擬 LLM 模式（無需 API 金鑰即可測試）

---

## 原始碼

完整的 Python 實作請參考：[_code/miniagent.py](_code/miniagent.py)

```python
#!/usr/bin/env python3
"""MiniAgent - A minimal ReAct agent framework"""

import json
import re
from dataclasses import dataclass
from typing import Any, Callable

# =====================
# Data Types
# =====================

@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters: dict

@dataclass
class AgentMessage:
    role: str
    content: str

# =====================
# Memory
# =====================

class SimpleMemory:
    def __init__(self):
        self.messages = []
        self.summary = ""

    def add(self, role, content):
        self.messages.append(AgentMessage(role, content))
        if len(self.messages) > 20:
            self.compress()

    def compress(self):
        early = [m.content for m in self.messages[:10]]
        summary = " | ".join(early)
        self.summary = f"[SUMMARY] {summary} [END_SUMMARY]" if not self.summary else f"{self.summary} -> {summary[:100]}"
        self.messages = self.messages[-10:]

    def get_context(self):
        ctx = []
        if self.summary:
            ctx.append(("system", f"Previous conversation summary: {self.summary}"))
        for m in self.messages:
            ctx.append((m.role, m.content))
        return ctx

# =====================
# Tools
# =====================

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, description, func, parameters=None):
        self.tools[name] = Tool(name, description, func, parameters or {})

    def execute(self, name, **kwargs):
        if name not in self.tools:
            return f"Error: unknown tool '{name}'"
        try:
            return self.tools[name].func(**kwargs)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def get_descriptions(self):
        return "\n".join([
            f"- {t.name}: {t.description}"
            for t in self.tools.values()
        ])

# =====================
# LLM Interface
# =====================

class LLMInterface:
    def generate(self, messages, tools_desc="") -> str:
        raise NotImplementedError

class MockLLM(LLMInterface):
    def __init__(self, responses=None):
        self.responses = responses or []
        self.idx = 0

    def generate(self, messages, tools_desc=""):
        if self.idx < len(self.responses):
            r = self.responses[self.idx]
            self.idx += 1
            return r
        return "Thought: I have completed the task.\nFinal Answer: Task completed."

# =====================
# ReAct Agent
# =====================

REACT_PROMPT = """You are an AI assistant with access to the following tools:

{tools}

You must respond in the following format:

Thought: your reasoning about what to do next
Action: tool_name
Action Input: {{"param": "value"}}

Or if you have the final answer:

Thought: I have all the information needed
Final Answer: your answer here

Begin!"""

class ReActAgent:
    def __init__(self, llm, tools: ToolRegistry, max_steps=10):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.memory = SimpleMemory()

    def run(self, task: str) -> str:
        self.memory.add("user", task)
        context = self.memory.get_context()
        tools_desc = self.tools.get_descriptions()

        system_prompt = REACT_PROMPT.format(tools=tools_desc)
        messages = [("system", system_prompt)]
        messages.extend(context)

        for step in range(self.max_steps):
            response = self.llm.generate(messages)

            if "Final Answer:" in response:
                answer = response.split("Final Answer:")[-1].strip()
                self.memory.add("assistant", answer)
                return answer

            action = self._parse_action(response)
            if action:
                tool_name = action.get("tool")
                params = action.get("params", {})
                result = self.tools.execute(tool_name, **params)
                messages.append(("assistant", response))
                messages.append(("system", f"Observation: {result}"))
                self.memory.add("assistant", f"{response}\nObservation: {result}")

        return "Max steps reached without final answer."

    def _parse_action(self, response):
        tool_match = re.search(r"Action:\s*(\w+)", response)
        input_match = re.search(r"Action Input:\s*(\{.+?\}|.+)", response, re.DOTALL)
        if not tool_match:
            return None
        tool_name = tool_match.group(1)
        params = {}
        if input_match:
            try:
                params = json.loads(input_match.group(1))
            except json.JSONDecodeError:
                raw = input_match.group(1).strip()
                params = {"input": raw}
        return {"tool": tool_name, "params": params}

# =====================
# Built-in Tools
# =====================

def build_default_tools():
    registry = ToolRegistry()

    def calculator(expression: str):
        safe = re.sub(r'[^0-9+\-*/().,% ]', '', expression)
        try:
            return str(eval(safe))
        except Exception as e:
            return f"Error: {e}"

    def search_web(query: str):
        return f'[Simulated] Search results for "{query}": Found relevant information about {query}.'

    def get_time():
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    registry.register("calculator", "Execute mathematical expressions", calculator, {
        "expression": "string"
    })
    registry.register("search_web", "Search the web for information", search_web, {
        "query": "string"
    })
    registry.register("get_time", "Get the current date and time", get_time)

    return registry

# =====================
# Multi-Agent Team
# =====================

class AgentTeam:
    def __init__(self):
        self.agents = {}

    def add_agent(self, name, agent):
        self.agents[name] = agent

    def run(self, workflow):
        results = {}
        for step in workflow:
            agent_name = step["agent"]
            task = step["task"].format(**results)
            result = self.agents[agent_name].run(task)
            results[step.get("output_key", agent_name)] = result
        return results

# =====================
# Test
# =====================

def test():
    tools = build_default_tools()

    mock_responses = [
        """Thought: I need to calculate 2 + 3 first, then multiply by 4.
Action: calculator
Action Input: {"expression": "2 + 3"}""",
        """Observation: 5
Thought: Now I multiply 5 by 4.
Action: calculator
Action Input: {"expression": "5 * 4"}""",
        """Observation: 20
Thought: I have the result.
Final Answer: The result of (2 + 3) * 4 is 20.""",
    ]

    llm = MockLLM(mock_responses)
    agent = ReActAgent(llm, tools)

    result = agent.run("What is (2 + 3) * 4?")
    print(f"Task: (2 + 3) * 4")
    print(f"Result: {result}")
    print()

    mock_responses2 = [
        """Thought: I need to check the current time first.
Action: get_time
Action Input: {}""",
        """Observation: Current time: 2026-05-15 10:30:00
Thought: Now I have the time information.
Final Answer: The current time is 2026-05-15 10:30:00.""",
    ]

    llm2 = MockLLM(mock_responses2)
    agent2 = ReActAgent(llm2, tools)
    result2 = agent2.run("What time is it?")
    print(f"Task: What time is it?")
    print(f"Result: {result2}")
    print()

    print("=== Multi-Agent Team Demo ===")
    researcher = ReActAgent(MockLLM([
        """Thought: I need to search for information.
Action: search_web
Action Input: {"query": "latest AI news 2026"}""",
        """Thought: I found the information.
Final Answer: In 2026, AI technology has advanced significantly with GPT-6 and Llama 4."""
    ]), tools)

    writer = ReActAgent(MockLLM([
        """Thought: I need to organize the research into an article.
Final Answer: ## AI in 2026\n\nArtificial intelligence has made remarkable progress in 2026, with major releases from OpenAI (GPT-6) and Meta (Llama 4)."""
    ]), tools)

    team = AgentTeam()
    team.add_agent("researcher", researcher)
    team.add_agent("writer", writer)

    workflow = [
        {"agent": "researcher", "task": "Research latest AI developments", "output_key": "research"},
        {"agent": "writer", "task": "Write an article based on: {research}", "output_key": "article"},
    ]

    team_results = team.run(workflow)
    print(f"Research: {team_results['research']}")
    print(f"Article: {team_results['article']}")

if __name__ == "__main__":
    test()
```

---

## 執行結果

```
$ python miniagent.py
Task: (2 + 3) * 4
Result: The result of (2 + 3) * 4 is 20.

Task: What time is it?
Result: The current time is 2026-05-15 10:30:00.

=== Multi-Agent Team Demo ===
Research: In 2026, AI technology has advanced significantly with GPT-6 and Llama 4.
Article: ## AI in 2026

Artificial intelligence has made remarkable progress in 2026, with major releases from OpenAI (GPT-6) and Meta (Llama 4).
```

---

## 如何使用

### 建立一個簡單的 Agent

```python
from miniagent import ReActAgent, build_default_tools, MockLLM

# 建立工具
tools = build_default_tools()

# 定義 LLM 回應（模擬模式）
responses = [
    "Thought: I need to search for AI news.\nAction: search_web\nAction Input: {\"query\": \"AI 2026\"}",
    "Observation: Found AI news...\nThought: I can answer now.\nFinal Answer: AI in 2026 is advancing rapidly."
]

# 建立 Agent
llm = MockLLM(responses)
agent = ReActAgent(llm, tools)

# 執行任務
result = agent.run("What's new in AI?")
print(result)
```

### 使用真實 LLM

若要使用真實的 LLM API，只需繼承 `LLMInterface` 並實作 `generate` 方法：

```python
from openai import OpenAI

class MyLLM(LLMInterface):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, messages, tools_desc=""):
        response = self.client.chat.completions.create(
            model="gpt-6",
            messages=[{"role": r, "content": c} for r, c in messages]
        )
        return response.choices[0].message.content
```

## 設計細節

### ReAct 循環

MiniAgent 的核心是 ReAct 循環（取自 focus2.md 介紹的 ReAct 論文）：

```
1. Thought（思考）：LLM 決定下一步該做什麼
2. Action（行動）：LLM 選擇要呼叫的工具和參數
3. Observation（觀察）：工具執行結果反饋給 LLM
4. 重複直到 LLM 給出 Final Answer
```

### 工具系統

工具的定義包含四個部分：

- `name`：工具名稱（LLM 用此名稱來呼叫）
- `description`：工具描述（LLM 根據描述決定何時使用）
- `func`：實際執行的 Python 函式
- `parameters`：參數 Schema（用於文件化和驗證）

### 記憶系統

`SimpleMemory` 實現了基本的記憶管理：
- 自動壓縮：超過 20 條訊息時自動生成摘要
- 上下文建構：將歷史訊息和摘要組合成 LLM 的輸入

### 多代理團隊

`AgentTeam` 支援順序工作流程：
1. 定義多個 Agent（研究員、作家等）
2. 定義工作流程（每個步驟指定 Agent 和任務）
3. 前一個 Agent 的輸出可作為下一個 Agent 的輸入

---

## 延伸練習

有興趣的讀者可以嘗試以下改進：

1. **加入 MCP 支援**：實作 MCP Client 來動態發現工具
2. **加入向量記憶**：使用 Chroma 或簡單的 TF-IDF 實現長期記憶
3. **加入並行執行**：使用 asyncio 實現多個 Agent 並行工作
4. **加入錯誤恢復**：當工具執行失敗時自動重試
5. **加入人類審查**：在關鍵決策點暫停並詢問使用者

---

## 結語

MiniAgent 雖然只有不到 250 行 Python 程式碼，但它實現了現代 AI Agent 框架的核心功能：

- ReAct 推理循環
- 工具註冊與執行
- 多步驟工作流程
- 多代理協作

這個實作展示了 Agent 框架的設計模式——當你理解了 ReAct 循環和工具系統這兩個核心概念，你就可以在此基礎上建構任意複雜的 AI Agent 應用。

詳細的技術背景請參考：
- [ReAct 與思考鏈](focus2.md) — Agent 的推理核心
- [工具使用與 MCP 協議](focus3.md) — 工具系統的標準化
- [多代理系統](focus4.md) — 團隊協作模式
