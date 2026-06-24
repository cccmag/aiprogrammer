# AI Agent 設計模式：工具使用與多步驟推理

## 前言

2025 年以來，AI Agent 成為 LLM 領域最熱門的主題。Agent 不僅能對話，還能使用工具、規劃步驟、記憶上下文，並從錯誤中恢復。本文將深入剖析 Agent 的核心設計模式，並用 Python 實作 ReAct、Plan-and-Execute 等主流架構。

## Agent 核心架構

一個完整的 Agent 系統包含四個層次：

1. **感知層**：接收使用者輸入與環境回饋
2. **推理層**：LLM 決定下一步動作
3. **行動層**：執行工具呼叫
4. **記憶層**：儲存對話歷史與執行狀態

## ReAct 模式：推理 + 行動

ReAct（Reasoning + Acting）是目前最廣泛使用的 Agent 模式，讓 LLM 交替進行推理與行動：

```python
import json
import requests
from typing import List, Dict, Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

class ReActAgent:
    def __init__(self, llm, tools: List[Tool], max_steps=10):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps

    def run(self, user_input: str) -> str:
        system_prompt = f"""你是一個使用工具的 AI 助手。
可用工具：{', '.join(f'{t.name}: {t.description}' for t in self.tools.values())}

遵循以下格式：
思考：<你的推理過程>
行動：<工具名稱>
行動輸入：<JSON 參數>
觀察：<工具回傳結果>
...（重複）
最終答案：<回答使用者>"""

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}]

        for step in range(self.max_steps):
            response = self.llm.invoke(messages)
            content = response.content

            if "最終答案：" in content:
                return content.split("最終答案：")[-1].strip()

            # 解析工具呼叫
            if "行動：" in content and "行動輸入：" in content:
                action_name = content.split("行動：")[1].split("\n")[0].strip()
                action_input = content.split("行動輸入：")[1].split("\n")[0].strip()

                if action_name in self.tools:
                    try:
                        params = json.loads(action_input)
                        observation = self.tools[action_name].func(**params)
                    except Exception as e:
                        observation = f"錯誤：{str(e)}"
                else:
                    observation = f"錯誤：未知工具 {action_name}"

                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"觀察：{observation}"})

        return "已達最大步驟數，無法完成任務。"

# 定義工具
def search_web(query: str) -> str:
    return f"關於「{query}」的搜尋結果..."

def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"計算錯誤：{e}"

tools = [
    Tool("search", "搜尋網路資訊", search_web),
    Tool("calculate", "執行數學運算", calculate),
]

agent = ReActAgent(llm=llm, tools=tools)
result = agent.run("2024 年台灣 GDP 成長率是多少？如果成長 5% 會是多少？")
```

## Plan-and-Execute 模式

先規劃再執行，適合複雜的多步驟任務：

```python
class PlanAndExecute:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def plan(self, task: str) -> List[str]:
        prompt = f"""將以下任務分解為數個步驟：

任務：{task}

請以 JSON 陣列回傳步驟列表（每個步驟包含 description 與 tool_needed）：
[{{"step": 1, "description": "...", "tool": "..."}}]"""
        response = self.llm.invoke(prompt)
        return json.loads(response.content)

    def execute(self, task: str) -> str:
        plan = self.plan(task)
        results = []

        for step in plan:
            step_result = self.execute_step(step)
            results.append(step_result)

            # 動態調整：必要時重新規劃
            if step_result.get("needs_replan"):
                plan = self.plan(f"根據進度重新規劃：{task}")
                return self.execute_from_plan(plan, results)

        return self.synthesize(results)

    def execute_step(self, step):
        if step["tool"] in self.tools:
            tool = self.tools[step["tool"]]
            return tool.func(step["description"])
        return {"error": f"找不到工具 {step['tool']}"}
```

## 多 Agent 協作模式

多 Agent 系統讓不同角色協作完成複雜任務：

```python
class MultiAgentSystem:
    def __init__(self, llm):
        self.agents = {
            "分析師": self.create_agent("你負責分析問題與拆解任務"),
            "程式師": self.create_agent("你負責撰寫與執行程式碼"),
            "審查員": self.create_agent("你負責檢查結果的正確性"),
        }

    def create_agent(self, role_prompt):
        def agent_fn(input_text, context=""):
            messages = [
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": f"背景：{context}\n\n任務：{input_text}"}
            ]
            return self.llm.invoke(messages).content
        return agent_fn

    def solve(self, task: str) -> str:
        # 分析階段
        analysis = self.agents["分析師"](f"分析任務：{task}")
        # 執行階段
        code = self.agents["程式師"](f"實作解決方案", context=analysis)
        # 審查階段
        review = self.agents["審查員"](f"審查結果：\n{code}")
        return f"分析：{analysis}\n\n實作：{code}\n\n審查：{review}"
```

## 記憶與狀態管理

Agent 的記憶分為短期（對話上下文）與長期（向量資料庫）：

```python
from collections import deque

class AgentMemory:
    def __init__(self, max_history=20):
        self.short_term = deque(maxlen=max_history)
        self.long_term = None  # 向量資料庫實例

    def add(self, role, content):
        self.short_term.append({"role": role, "content": content})

    def get_context(self, window=10):
        return list(self.short_term)[-window:]

    def retrieve_relevant(self, query, k=3):
        if self.long_term:
            return self.long_term.similarity_search(query, k=k)
        return []
```

## 錯誤恢復策略

Agent 必須能從錯誤中恢復：

```python
class RobustAgent:
    def execute_with_recovery(self, action, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = action()
                if self.validate_result(result):
                    return result
                else:
                    print(f"嘗試 {attempt+1} 結果無效，重試中...")
            except Exception as e:
                print(f"嘗試 {attempt+1} 失敗：{e}")
                if attempt < max_retries - 1:
                    self.recover(attempt, e)
        return self.fallback_response()
```

## 參考資源

- [ReAct 論文](https://www.google.com/search?q=ReAct+synergizing+reasoning+and+acting+in+language+models)
- [LangChain Agent 文件](https://www.google.com/search?q=langchain+agent+documentation)
- [OpenAI Function Calling](https://www.google.com/search?q=openai+function+calling+guide)
