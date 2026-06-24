# Agent 角色設計與專業化（2016-2026）

## 角色定義：System Prompt + 能力邊界

一個 Agent 的角色本質上由其系統提示詞（System Prompt）和可使用的工具共同定義。系統提示詞決定 Agent 的「人格」與「行為準則」，工具則決定其「能力範圍」。

```python
class Agent:
    def __init__(self, name: str, system_prompt: str, tools: list):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = {t.name: t for t in tools}
        self.memory = []

    def run(self, task: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.memory,
            {"role": "user", "content": task}
        ]
        response = self.llm.chat(messages, tools=list(self.tools.values()))
        self.memory.append({"role": "assistant", "content": response})
        return response

# 兩個不同角色的 Agent
coder = Agent(
    name="Coder",
    system_prompt="你是一個資深 Python 工程師。請寫出可執行的、符合 PEP 8 規範的程式碼。",
    tools=[python_executor, file_reader, code_reviewer]
)

reviewer = Agent(
    name="Reviewer",
    system_prompt="你是一個程式碼審查專家。檢查程式碼的正確性、安全性和效能。",
    tools=[code_analyzer, security_scanner]
)
```

## Agent 專業化策略

### 工具綁定

專業化的核心是「控制工具的可見性」。搜尋 Agent 不應該看到檔案系統，計算 Agent 不應該看到網路 API：

```python
# 工具可見性隔離
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, agent_type: str, tool):
        if agent_type not in self.tools:
            self.tools[agent_type] = []
        self.tools[agent_type].append(tool)

    def get_tools(self, agent_type: str) -> list:
        return self.tools.get(agent_type, [])

registry = ToolRegistry()
registry.register("researcher", web_search_tool)
registry.register("researcher", document_reader)
registry.register("calculator", python_executor)  # 計算 Agent 只能執行程式
```

### 知識庫隔離

不同 Agent 使用不同的向量資料庫或索引，避免不相關的上下文污染：

```python
class KnowledgeBase:
    def __init__(self, name: str, documents: list):
        self.name = name
        self.vector_store = VectorStore(documents)

    def query(self, question: str, top_k: int = 3) -> list:
        return self.vector_store.similarity_search(question, k=top_k)

rust_kb = KnowledgeBase("Rust docs", rust_documents)
python_kb = KnowledgeBase("Python docs", python_documents)

rust_agent = Agent("Rust Expert", "你擅長 Rust 系統程式設計", tools=[rust_kb])
```

## 函數呼叫（Function Calling）的設計模式

Function Calling 是 Agent 與外部世界互動的標準介面。設計良好的工具定義是 Agent 效能的關鍵：

```python
# 工具定義（OpenAI 格式）
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜尋網路獲取最新資訊",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜尋關鍵字"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "最大結果數",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }
]
```

## 記憶管理

記憶是 Agent 專業化的另一個維度。三種記憶類型各有用途：

| 記憶類型 | 儲存位置 | 生命週期 | 範例 |
|---------|---------|---------|------|
| 短期記憶 | LLM Context Window | 單次對話 | 當前任務上下文 |
| 長期記憶 | 向量資料庫 | 跨對話 | 使用者偏好、專案知識 |
| 共用記憶 | 共用資料庫 | 跨 Agent | 團隊決策記錄 |

```python
class MemoryManager:
    def __init__(self):
        self.short_term = []
        self.long_term = VectorStore()
        self.shared = SharedStore()

    def add_short_term(self, message: dict):
        self.short_term.append(message)
        if len(self.short_term) > 100:
            self.short_term.pop(0)

    def save_to_long_term(self, key: str, content: str):
        self.long_term.add(key, content)

    def save_to_shared(self, key: str, content: str):
        self.shared.set(key, content, ttl=3600)
```

---

**下一步**：[任務分解與排程](focus3.md)

## 延伸閱讀

- [Function Calling 最佳實踐](https://www.google.com/search?q=OpenAI+function+calling+best+practices)
- [Agent 角色設計](https://www.google.com/search?q=LLM+agent+role+design+system+prompt)
- [RAG 與知識庫隔離](https://www.google.com/search?q=RAG+knowledge+base+isolation+multi+agent)
