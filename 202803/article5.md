# Agentic RAG 模式

## 前言

傳統 RAG 是「一發一收」的被動檢索——使用者提問、系統檢索、LLM 回答。Agentic RAG 則讓 LLM 化身為主動的 Agent，可以自行決定檢索時機、選擇檢索工具、評估檢索結果，甚至反覆修正查詢。本文介紹四種 Agentic RAG 模式。

## 模式一：ReAct RAG

ReAct（Reasoning + Acting）讓 LLM 在推理過程動態決定是否檢索：

```python
import json

class ReActRAG:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools

    def run(self, question: str, max_steps: int = 10) -> str:
        messages = [
            {"role": "system", "content": (
                "你是 RAG Agent。你可以使用以下工具：\n"
                + "\n".join(f"- {k}: {v['desc']}" for k, v in self.tools.items())
                + "\n回答格式：\n思考：你的推理\n動作：工具名稱\n輸入：參數"
            )},
            {"role": "user", "content": question}
        ]

        for step in range(max_steps):
            response = self.llm.generate(messages)
            if "最終答案：" in response:
                return response.split("最終答案：")[1]
            action = self._parse_action(response)
            if action:
                result = self.tools[action["name"]]["fn"](action["input"])
                messages.append({"role": "user", "content": f"觀察：{result}"})

        return "無法在限制步數內回答"
```

## 模式二：Plan & Execute

先規劃檢索步驟，再逐步執行：

```python
class PlanExecuteRAG:
    def plan(self, question: str) -> list[str]:
        steps = self.llm.generate(
            f"為「{question}」規劃檢索步驟，列出需要查詢的子問題。"
        )
        return [s.strip() for s in steps.split("\n") if s.strip()]

    def execute(self, plan: list[str], retriever) -> str:
        context = []
        for step in plan:
            docs = retriever.retrieve(step)
            context.extend(docs)
        return context
```

## 模式三：Tool-Using RAG

Agent 擁有多種檢索工具，根據需求選擇最合適的：

```python
rag_tools = {
    "vector_search": {
        "desc": "語意搜尋非結構化文件",
        "fn": lambda q: vector_store.similarity_search(q, k=5)
    },
    "sql_query": {
        "desc": "查詢結構化資料庫",
        "fn": lambda q: nl_to_sql_and_execute(q)
    },
    "web_search": {
        "desc": "搜尋最新網路資訊",
        "fn": lambda q: web_search(q)
    },
    "code_interpreter": {
        "desc": "執行程式碼計算或分析",
        "fn": lambda q: execute_python(q)
    }
}
```

## 模式四：自省式 RAG（Self-Reflective RAG）

Agent 評估自身檢索結果是否足夠，不足時自動修正：

```python
class SelfReflectiveRAG:
    def retrieve_with_reflection(self, question: str, max_retries: int = 3):
        for attempt in range(max_retries):
            docs = self.retriever.retrieve(question)
            quality = self.llm.evaluate(
                f"這些文件足以回答「{question}」嗎？"
                f"文件：{docs[:500]}"
            )
            if quality.score >= 0.7:
                return docs
            question = self.llm.refine_query(question, quality.reason)
        return docs
```

## 實戰對比

考慮問題：「2025 年 Q3 公司的毛利率為何？」。傳統 RAG 可能檢索到不相關的財務文件。Agentic RAG 的 ReAct 模式會先查 SQL 取得營收與成本數據，再自行計算毛利率，最後確認計算無誤後回答。

## 實作要點

Agentic RAG 的關鍵在於**工具定義的清晰度**與**錯誤處理**。每個工具應有明確的輸入輸出規格，Agent 應在工具呼叫失敗時有備案策略：

```python
def safe_call(tool_fn, input_data, fallback="查詢失敗"):
    try:
        return tool_fn(input_data)
    except Exception as e:
        return f"{fallback}：{str(e)}"
```

## 總結

Agentic RAG 將 RAG 從「被動檢索」提升到「主動求知」的層次。透過 ReAct、Plan & Execute、Tool-Using、Self-Reflective 等模式，LLM Agent 能夠規劃檢索策略、選用多種工具、並自我修正檢索結果。這使得 RAG 系統可以應對更複雜的查詢。

---

**參考資料**

- https://www.google.com/search?q=Agentic+RAG+ReAct+pattern
- https://www.google.com/search?q=ReAct+reasoning+acting+LLM+agent
- https://www.google.com/search?q=plan+execute+retrieval+agent
- https://www.google.com/search?q=self+reflective+RAG+retrieval+quality
