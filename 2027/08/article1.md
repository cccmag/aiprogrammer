# 從零實作 AI Agent：ReAct 模式與工具使用

## 前言

ReAct（Reasoning + Acting）是由 Shunyu Yao 等人於 2022 年提出的一種 Agent 設計模式，核心思想是讓 LLM 在「推理」與「行動」之間循環交替，透過觀察環境回饋來逐步解決問題。本文將帶領讀者從零開始，用 Python 實作一個完整的 ReAct Agent。

---

## 一、ReAct 的核心循環

ReAct 的基本循環為：**觀察（Observe）→ 思考（Think）→ 行動（Act）→ 觀察（Observe）**。與單純的 Chain-of-Thought（CoT）不同，ReAct 允許 Agent 在推理過程中呼叫外部工具，並將工具的輸出納入下一步的推理依據。

CoT 與 ReAct 的關鍵差異：

| 特性 | Chain-of-Thought | ReAct |
|------|-----------------|-------|
| 推理方式 | 內化思考鏈 | 思考 + 外部行動 |
| 工具使用 | 不支援 | 原生支援 |
| 資訊更新 | 依賴訓練資料 | 即時查詢 |
| 適用場景 | 純推理問題 | 需要外部資訊的任務 |

---

## 二、從零實作 ReAct Agent

### 2.1 工具定義

首先定義工具的抽象基底：

```python
from abc import ABC, abstractmethod
from typing import Any

class Tool(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def run(self, input: str) -> str: ...

class CalculatorTool(Tool):
    def name(self): return "calculator"

    def description(self):
        return "計算數學表達式，輸入範例：'2 + 3 * 4'"

    def run(self, input: str) -> str:
        try:
            return str(eval(input, {"__builtins__": {}}, {}))
        except Exception as e:
            return f"錯誤：{e}"

class SearchTool(Tool):
    def __init__(self):
        self.knowledge = {
            "台灣人口": "約 2,350 萬人（2025年）",
            "Python 作者": "Guido van Rossum",
        }

    def name(self): return "web_search"

    def description(self):
        return "搜尋網路資訊，輸入搜尋關鍵字"

    def run(self, input: str) -> str:
        return self.knowledge.get(input, f"找不到 '{input}' 的結果")
```

### 2.2 ReAct Agent 實作

```python
import json
import re
from typing import List

class ReActAgent:
    def __init__(self, llm, tools: List[Tool], max_steps: int = 10):
        self.llm = llm
        self.tools = {t.name(): t for t in tools}
        self.max_steps = max_steps

    def _build_prompt(self, task: str, history: List[str]) -> str:
        tools_desc = "\n".join(
            f"- {t.name()}: {t.description()}" for t in self.tools.values()
        )
        return f"""你是一個可以使用工具的 AI 助手。

可用工具：
{tools_desc}

回答格式：
思考：<你的推理過程>
行動：<工具名稱>
輸入：<工具輸入>

當你準備好回答時，使用：
思考：我已經有足夠資訊
回答：<最終答案>

任務：{task}

歷史：
{chr(10).join(history)}
"""

    def _parse_action(self, response: str) -> dict:
        patterns = {
            "思考": r"思考：(.+?)(?=\n行動：|\n回答：|$)",
            "行動": r"行動：(.+?)(?=\n輸入：|\n思考：|$)",
            "輸入": r"輸入：(.+?)(?=\n思考：|\n回答：|$)",
            "回答": r"回答：(.+)",
        }
        result = {}
        for key, pat in patterns.items():
            m = re.search(pat, response, re.DOTALL)
            if m:
                result[key] = m.group(1).strip()
        return result

    def run(self, task: str) -> str:
        history = []
        for step in range(self.max_steps):
            prompt = self._build_prompt(task, history)
            response = self.llm(prompt)
            parsed = self._parse_action(response)

            if "回答" in parsed:
                return parsed["回答"]

            action_name = parsed.get("行動", "")
            action_input = parsed.get("輸入", "")
            thought = parsed.get("思考", "")

            if action_name in self.tools:
                result = self.tools[action_name].run(action_input)
                history.append(f"思考：{thought}")
                history.append(f"行動：{action_name}")
                history.append(f"輸入：{action_input}")
                history.append(f"觀察：{result}")
            else:
                history.append(f"觀察：未知工具 '{action_name}'")

        return "已達最大步驟數，無法完成任務。"
```

### 2.3 使用範例

```python
# 使用 OpenAI API 作為 LLM 後端
def call_llm(prompt: str) -> str:
    import openai
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content

agent = ReActAgent(call_llm, [CalculatorTool(), SearchTool()])

result = agent.run("台灣人口是多少？將這個數字乘以 2")
print(result)
```

---

## 三、擴充工具生態

### 3.1 檔案操作工具

```python
import os

class FileReadTool(Tool):
    def name(self): return "read_file"

    def description(self):
        return "讀取檔案內容，輸入檔案路徑"

    def run(self, input: str) -> str:
        if not os.path.exists(input):
            return f"檔案不存在：{input}"
        with open(input, "r") as f:
            return f.read()
```

### 3.2 API 呼叫工具

```python
import requests

class APITool(Tool):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def name(self): return "api_call"

    def description(self):
        return "呼叫外部 REST API"

    def run(self, input: str) -> str:
        try:
            resp = requests.get(f"{self.base_url}/{input}", timeout=10)
            return resp.text[:1000]
        except Exception as e:
            return f"API 錯誤：{e}"
```

---

## 四、ReAct 的最佳實踐

1. **工具描述要精確**：LLM 依賴工具的描述來決定何時使用，描述應包含使用範例和限制
2. **錯誤處理**：工具執行可能失敗，Agent 需要具備重試和替代方案
3. **步驟限制**：設定 `max_steps` 防止無限循環
4. **溫度控制**：推理任務建議使用較低的溫度（0.0–0.3）
5. **格式解析**：使用正則表達式解析 LLM 輸出時，要處理格式異常的情況

---

## 結語

ReAct 模式是現代 AI Agent 系統的基石。透過「推理—行動—觀察」的循環，LLM 不再只是一個文字生成器，而是能夠與外部世界互動的自主系統。在下一篇文章中，我們將探討如何將多個 Agent 組合起來，形成更強大的協作系統。

---

**參考資料**

- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", https://arxiv.org/abs/2210.03629
- OpenAI Function Calling 文檔：https://platform.openai.com/docs/guides/function-calling
- LangChain ReAct 文件：https://python.langchain.com/docs/modules/agents/agent_types/react
