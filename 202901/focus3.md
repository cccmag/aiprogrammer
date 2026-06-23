# 工作流編排引擎（2024-2029）

## 從 LangChain 到自建編排器

### 前言

工作流編排引擎是 Agent 系統的「操作系統」——它管理任務排程、狀態追蹤和錯誤處理。2024 年以來，這個領域經歷了爆炸式成長。

### LangChain：先驅者（2024-2026）

LangChain 是最早普及鏈式工作流的框架：

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template("總結以下內容：{text}")
)
result = chain.run(text="長篇文章...")
```

LangChain 引入了 **Chain**、**Agent**、**Tool** 的核心抽象，但後來因過度抽象化受到批評。

### CrewAI：多 Agent 編排（2025-2027）

CrewAI 專注於多 Agent 協作場景：

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="收集資訊")
writer = Agent(role="作家", goal="撰寫文章")

task1 = Task(description="研究 AI 趨勢", agent=researcher)
task2 = Task(description="撰寫報告", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff()
```

### 事件驅動編排（2027-2029）

2027 年後，業界轉向事件驅動架構：

```python
# 事件驅動工作流
class EventDrivenWorkflow:
    def __init__(self):
        self.handlers = {}
    
    def on(self, event, handler):
        self.handlers[event] = handler
    
    def emit(self, event, data):
        handler = self.handlers.get(event)
        if handler:
            return handler(data)

wf = EventDrivenWorkflow()
wf.on("research_done", lambda d: llm(f"基於研究結果撰寫：{d}"))
wf.on("writing_done", lambda d: llm(f"審閱文章：{d}"))
```

### 圖形化編排（DAG）

複雜工作流通常用 DAG（有向無環圖）表示：

```python
# DAG-based workflow
from collections import defaultdict

class DAGWorkflow:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_step(self, step, depends_on=None):
        if depends_on:
            self.graph[depends_on].append(step)
    
    def execute(self):
        # 拓撲排序後依序執行
        pass
```

### 小結

編排引擎的演進方向：從**厚重框架**到**輕量事件驅動**，從**單一 Agent** 到**多 Agent 動態協作**。

---

**下一步**：[人機協作工作流](focus4.md)

## 延伸閱讀

- [LangChain 框架介紹](https://www.google.com/search?q=LangChain+framework+agent+workflow)
- [CrewAI 多 Agent 系統](https://www.google.com/search?q=CrewAI+multi+agent+orchestration)
- [事件驅動 Agent 架構](https://www.google.com/search?q=event+driven+agent+architecture+LLM)
