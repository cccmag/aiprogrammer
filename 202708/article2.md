# AutoGen 深入：Microsoft 多代理框架實戰

## 前言

AutoGen 是 Microsoft 推出的開源多代理框架，核心設計理念是讓多個 LLM Agent 透過對話協作來解決複雜任務。本文將深入探討 AutoGen 0.4+ 版本的架構設計、核心模式，並透過 Python 程式碼展示實際應用。

---

## 一、AutoGen 核心架構

### 1.1 三種核心 Agent 類型

AutoGen 0.4+ 重新設計了 Agent 模型，基於三個核心抽象：

```python
from autogen_agent import AssistantAgent, UserProxyAgent
from autogen_agent.group import GroupChat, GroupChatManager
```

| Agent 類型 | 角色 | 典型用途 |
|-----------|------|---------|
| **AssistantAgent** | LLM 驅動的助手 | 程式碼生成、推理、回答問題 |
| **UserProxyAgent** | 代理人類執行行動 | 執行程式碼、讀寫檔案、呼叫 API |
| **GroupChatManager** | 群組對話調度 | 協調多個 Agent 的對話流程 |

### 1.2 AssistantAgent

AssistantAgent 是 AutoGen 中最基本也最常用的 Agent，它封裝了一個 LLM 模型和一組工具：

```python
from autogen_agent import AssistantAgent

assistant = AssistantAgent(
    name="coder",
    system_message="你是一位專業的 Python 工程師。",
    llm_config={
        "model": "gpt-4",
        "api_key": "...",
        "temperature": 0.1,
    },
)
```

---

## 二、兩 Agent 協作模式

### 2.1 程式碼生成與執行

最經典的 AutoGen 模式是 AssistantAgent 生成程式碼，UserProxyAgent 執行並回傳結果：

```python
from autogen_agent import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    system_message="你精通 Python，擅長資料分析與視覺化。",
    llm_config={"model": "gpt-4", "temperature": 0},
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # 直接在主機執行
    },
)

user_proxy.initiate_chat(
    assistant,
    message="從 CSV 讀取銷售資料，計算每月總額並繪製長條圖。",
)
```

UserProxyAgent 的 `human_input_mode` 有三種設定：

| 模式 | 行為 | 適用場景 |
|------|------|---------|
| `ALWAYS` | 每次回覆前詢問使用者 | 需人類監督的任務 |
| `TERMINATE` | 僅在 Agent 要求終止時詢問 | 半自動工作流 |
| `NEVER` | 完全自動 | 可信任的批次任務 |

---

## 三、多 Agent 群組對話

### 3.1 GroupChat 架構

GroupChat 允許多個 Agent 在同一對話中輪流發言，由 GroupChatManager 控制對話流程：

```python
from autogen_agent import AssistantAgent, GroupChat, GroupChatManager

planner = AssistantAgent(
    name="planner",
    system_message="你負責規劃任務步驟。給出詳細的執行計畫。",
    llm_config={"model": "gpt-4"},
)

coder = AssistantAgent(
    name="coder",
    system_message="你負責根據計畫撰寫程式碼。",
    llm_config={"model": "gpt-4"},
)

critic = AssistantAgent(
    name="critic",
    system_message="你負責審查程式碼，指出問題並提出改善建議。",
    llm_config={"model": "gpt-4"},
)

group_chat = GroupChat(
    agents=[planner, coder, critic],
    messages=[],
    max_round=12,
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"model": "gpt-4"},
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
)

user_proxy.initiate_chat(
    manager,
    message="建立一個 Flask Web 應用，提供 REST API 進行待辦事項管理。",
)
```

### 3.2 自訂對話順序

AutoGen 0.4+ 允許自訂 Agent 的發言順序和條件：

```python
from autogen_agent import AfterWorkOption, speak_order

@speak_order
def custom_order(last_speaker, group_chat):
    if last_speaker.name == "planner":
        return "coder"
    elif last_speaker.name == "coder":
        return "critic"
    elif last_speaker.name == "critic":
        return AfterWorkOption.TERMINATE
    return AfterWorkOption.ROUND_ROBIN
```

---

## 四、AutoGen vs CrewAI vs LangGraph

| 特性 | AutoGen | CrewAI | LangGraph |
|------|---------|--------|-----------|
| 核心模型 | 對話式協作 | 角色扮演團隊 | 有向圖（DAG）工作流 |
| Agent 通訊 | 自然語言對話 | 任務佇列 | 狀態圖傳遞 |
| 學習曲線 | 中 | 低 | 高 |
| 彈性 | 中（基於對話） | 低（角色固定） | 高（完全可控） |
| 除錯 | 對話可讀性高 | 任務鏈清晰 | 狀態機可追蹤 |
| 適合場景 | 協作推理、程式碼生成 | 結構化團隊任務 | 複雜工作流管線 |

### 4.1 CrewAI 範例對比

```python
# CrewAI 風格（角色驅動）
from crewai import Agent, Task, Crew

researcher = Agent(role="研究員", goal="收集資料", ...)
writer = Agent(role="撰寫者", goal="撰寫報告", ...)

task1 = Task(description="搜尋 AI Agent 最新發展", agent=researcher)
task2 = Task(description="根據資料撰寫摘要", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
crew.kickoff()
```

### 4.2 LangGraph 範例對比

```python
# LangGraph 風格（圖驅動）
from langgraph.graph import StateGraph

graph = StateGraph(MultiAgentState)
graph.add_node("researcher", research_node)
graph.add_node("writer", write_node)
graph.add_edge("researcher", "writer")
graph.set_entry_point("researcher")
graph.set_finish_point("writer")
app = graph.compile()
```

---

## 五、實戰注意事項

1. **Token 成本控制**：多 Agent 對話會產生大量 Token，建議為每個 Agent 設定 `max_tokens` 限制
2. **終止條件**：務必設定 `max_round` 和明確的終止訊號，避免無窮對話
3. **Agent 角色分工**：角色定義越清晰，協作效果越好
4. **序列化**：AutoGen 支援對話歷史的序列化，可用於後續分析和除錯

---

## 結語

AutoGen 以其直覺的對話式協作模型，成為目前最受歡迎的多 Agent 框架之一。它在協作推理、程式碼生成等場景表現優異。對於需要更精細控制的工作流（如條件分支、循環），LangGraph 可能是更好的選擇；而對於結構化的團隊任務，CrewAI 提供了更簡潔的 API。選擇哪個框架取決於你的具體需求。

---

**參考資料**

- AutoGen 官方文檔：https://microsoft.github.io/autogen/
- CrewAI 文檔：https://docs.crewai.com/
- LangGraph 文檔：https://langchain-ai.github.io/langgraph/
- "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", https://arxiv.org/abs/2308.08155
