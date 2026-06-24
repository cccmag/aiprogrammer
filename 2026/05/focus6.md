# Agent 框架與生態：LangChain、AutoGPT、CrewAI（2023-2026）

## 框架的必要性

2023 年初，開發 AI Agent 意味著從零開始：直接呼叫 LLM API、手動管理上下文、自行實作工具呼叫邏輯。每個專案都在重複造輪子。Agent 框架的出現解決了這個問題。

```
無框架時代（2023 年初）：
每個專案從零開始
├── 自行管理 LLM API 連接
├── 自行實作提示模板
├── 自行處理上下文視窗
├── 自行解析函式呼叫
└── 自行管理對話歷史

有框架時代（2023 年末起）：
框架提供標準元件
├── 內建 LLM 介面抽象
├── 提示模板管理
├── 上下文視窗自動管理
├── 工具呼叫自動解析
└── 記憶系統即插即用
```

## LangChain：Agent 框架的開創者

### LangChain 的崛起

2023 年初，Harrison Chase 發布了 LangChain——第一個廣泛使用的 LLM 應用開發框架。LangChain 的核心理念是「可組合性」（Composability）：將 LLM 應用分解為可以自由組合的標準元件。

```
LangChain 的元件模型：
─────────────────

Models（模型抽象）
├── Chat Models: GPT-4, Claude, Gemini
├── Embedding Models: text-embedding-3, ada
└── LLMs: 各種語言模型

Prompts（提示管理）
├── Prompt Templates: 可複用的提示模板
├── Few-shot Examples: 範例管理
└── Output Parsers: 輸出解析器

Chains（鏈）
├── LLM Chain: 最簡單的 LLM 呼叫
├── Sequential Chain: 依序執行
└── Router Chain: 條件分支

Agents（代理）
├── Agent 類型: ReAct, Plan-and-Execute
├── Tools: 工具註冊系統
└── Toolkits: 工具組

Memory（記憶）
├── Buffer Memory: 緩衝記憶
├── Summary Memory: 摘要記憶
└── Vector Store Memory: 向量記憶

Callbacks（回調）
├── 日誌記錄
├── 監控
└── Token 計數
```

### LangChain Agent 實例

```python
from langchain.agents import create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# 定義工具
tools = [
    Tool(name="search", func=search_web, 
         description="搜尋網路資訊"),
    Tool(name="calculator", func=calculate,
         description="執行數學計算"),
]

# 建立 Agent
agent = create_react_agent(
    llm=ChatOpenAI(model="gpt-6"),
    tools=tools,
    prompt_template=react_prompt
)

# 執行
response = agent.invoke({
    "input": "2026 年台灣 GDP 成長率預測是多少？"
})
```

### LangChain 的貢獻與爭議

**貢獻：**
1. 第一個標準化的 LLM 應用框架
2. 建立了 Agent 開發的基本範式
3. 豐富的第三方整合生態
4. 活躍的社群和文件

**爭議：**
1. 抽象層級過多，學習曲線陡峭
2. 底層實作經常變化，向後相容性差
3. 過度工程化，簡單任務也需要複雜設定
4. 除錯困難，錯誤訊息不明確

## AutoGPT：自主 Agent 的典範

### 架構設計

AutoGPT 的架構與傳統框架不同——它更像是一個「自主 Agent 應用」而非開發框架：

```
AutoGPT 的核心元件：
─────────────────

1. 目標管理（Goal Manager）
   將使用者目標分解為可執行任務

2. 任務執行（Task Executor）
   使用 ReAct 循環執行每個任務

3. 記憶系統（Memory System）
   使用向量資料庫儲存經驗

4. 網路存取（Web Access）
   瀏覽器、API 呼叫能力

5. 程式碼執行（Code Execution）
   在沙箱環境中執行 Python
```

### AutoGPT 的啟發

AutoGPT 雖然在實用性上有限，但它對 Agent 生態的啟發是深遠的：

1. **自主性證明**：展示了 LLM Agent 可以長時間自主運作
2. **任務分解**：將大目標自動分解為子任務的流程
3. **自我反思**：Agent 可以審視自己的輸出並修正
4. **工具使用**：展示 Agent 使用多種工具解決問題

## CrewAI：輕量級多代理框架

### 設計哲學

CrewAI（2024 年發布）代表了 Agent 框架的另一個方向——輕量、簡潔、專注於多代理協作。它的設計哲學是「讓 Agent 像團隊成員一樣協作」：

```python
from crewai import Agent, Task, Crew

# 定義 Agent
researcher = Agent(
    role="研究員",
    goal="找到相關資訊並分析",
    backstory="你是一位經驗豐富的研究分析師",
    tools=[search_tool, analysis_tool]
)

writer = Agent(
    role="作家",
    goal="將研究結果寫成文章",
    backstory="你是一位才華洋溢的科技作家",
)

# 定義任務
research_task = Task(
    description="研究 AI Agent 框架的最新發展",
    agent=researcher
)

writing_task = Task(
    description="根據研究結果撰寫一篇 1000 字的文章",
    agent=writer
)

# 建立團隊
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# 執行
result = crew.kickoff()
```

### CrewAI 的優點

1. **極簡 API**：只需定義 Agent、Task、Crew 三個概念
2. **角色驅動**：透過角色定義自然地實現多代理協作
3. **任務導向**：清晰的工作流程管理
4. **輕量級**：無需學習複雜抽象

## Microsoft Semantic Kernel 與 AutoGen

### Semantic Kernel

微軟的 Semantic Kernel（2023 年發布）將 AI Agent 與傳統的軟體工程模式結合：

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.openai import OpenAIChatCompletion
from semantic_kernel.planners import SequentialPlanner

# 建立核心
kernel = Kernel()
kernel.add_chat_service("gpt6", OpenAIChatCompletion("gpt-6"))

# 註冊外掛（Plugins）
kernel.import_skills_from_directory("./plugins")

# 外掛範例：plugins/EmailPlugin/skprompt.txt
# {{$input}}
# 根據以下內容撰寫一封專業的電子郵件：
# 主旨：{{$subject}}
# 收件人：{{$recipient}}

# 規劃器自動組合外掛
planner = SequentialPlanner(kernel)
plan = planner.create_plan("寄一封會議通知給所有參與者")
result = await plan.invoke()
```

Semantic Kernel 的獨特之處在於將 Agent 能力封裝為「外掛」（Plugin），類似於 VS Code 的外掛系統。

### AutoGen：多代理對話

AutoGen（2023 年底發布）是微軟的另一個 Agent 框架，專注於多代理對話：

```
AutoGen 的核心創新：
─────────────────

1. 代理間對話（Inter-Agent Conversation）
   Agent 可以互相發送訊息、提問、回答

2. 人類參與模式（Human-in-the-Loop）
   在關鍵決策點可以暫停並詢問人類

3. 群組對話（Group Chat）
   多個 Agent 在群組中討論

4. 程式碼執行沙箱
   安全的程式碼執行環境
```

## 框架比較與選型指南

### 主要框架對比

| 框架 | 發布 | 定位 | 學習曲線 | 適合場景 |
|------|------|------|---------|---------|
| LangChain | 2023.01 | 通用 LLM 框架 | 陡峭 | 複雜工作流程 |
| AutoGPT | 2023.03 | 自主 Agent | 中等 | 長時間自主任務 |
| Semantic Kernel | 2023.05 | 企業級整合 | 中等 | .NET/Azure 生態 |
| AutoGen | 2023.10 | 多代理對話 | 中等 | 研究、協作任務 |
| CrewAI | 2024.01 | 輕量多代理 | 平緩 | 快速原型開發 |
| Pydantic AI | 2024.06 | 型別安全 | 平緩 | 需要型別檢查 |
| Mastra | 2025.03 | 工作流程 | 中等 | 業務流程自動化 |

### 選型建議

```
根據需求選擇框架：
─────────────────

你需要快速建立一個簡單的 Agent？
→ CrewAI 或 Pydantic AI

你需要複雜的工作流程和工具整合？
→ LangChain

你在 .NET/Azure 生態中開發？
→ Semantic Kernel

你需要多個 Agent 協作完成任務？
→ AutoGen 或 CrewAI

你需要長時間自主運行的 Agent？
→ AutoGPT 或其後繼者

你需要型別安全和 IDE 支援？
→ Pydantic AI

你需要企業級佈署和管理？
→ Semantic Kernel 或 LangServe
```

## Agent 框架的未來趨勢

### 1. 標準化

MCP 協議的標準化正在促使 Agent 框架走向互操作性：

```
未來願景：框架無關的 Agent 生態
────────────────────

一個用 CrewAI 開發的 Agent
可以無縫使用 LangChain 開發的工具
可以部署到 Semantic Kernel 的執行環境

像 Docker 之於容器 → MCP 之於 Agent
```

### 2. 專用化

針對特定領域的專用框架正在出現：

- **Code Agent**: GitHub Copilot X, Cursor
- **Data Agent**: Pandas AI, Grafana AI
- **DevOps Agent**: Firecrawl, K8sGPT
- **Customer Agent**: Zendesk AI, Intercom Fin

### 3. 輕量化

新一代框架趨向輕量化：

```
框架的演進趨勢：
─────────────────

LangChain (2023) → 抽象豐富，功能全面
    ↓
CrewAI (2024) → 簡潔 API，專注多代理
    ↓
Pydantic AI (2024) → 型別安全，最小抽象
    ↓
Mastra (2025) → 工作流程驅動，自然語法
    ↓
2026 年：走向「框架即函式庫」的微核心設計
```

## 結語

Agent 框架在短短三年內從無到有、從粗放到精細，經歷了快速的演化。LangChain 開創了 LLM 應用框架的先河，AutoGPT 證明了自主 Agent 的可能性，CrewAI 簡化了多代理協作，而 Semantic Kernel 將 Agent 與企業級開發整合。

選擇框架時最重要的考量是：**你的需求是什麼？** 一個簡單的客服 Agent 不需要 LangChain 的完整抽象，而一個複雜的多代理工作流程也不適合用最基礎的 API 從頭打造。

下一篇文章將探討自主系統面臨的安全、可靠性和倫理挑戰，以及未來的發展方向。

---

## 延伸閱讀

- [LangChain 文件](https://www.google.com/search?q=LangChain+documentation)
- [CrewAI 使用指南](https://www.google.com/search?q=CrewAI+guide+tutorial)
- [Microsoft AutoGen](https://www.google.com/search?q=Microsoft+AutoGen+framework)
- [Pydantic AI](https://www.google.com/search?q=Pydantic+AI+framework)

---

*本篇文章為「AI 程式人雜誌 2026 年 5 月號」歷史回顧系列之一。*
