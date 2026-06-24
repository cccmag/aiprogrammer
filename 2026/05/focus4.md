# 多代理系統：協作與分工（2024-2026）

## 為什麼需要多個 Agent？

單一 Agent 的能力是有限的——就像一個萬能工匠，雖然什麼都會一點，但無法同時處理多個任務。多代理系統（Multi-Agent Systems, MAS）的理念來自於人類社會：**複雜任務需要分工協作**。

```
單一 Agent vs 多 Agent 的對比
─────────────────────────────────────────────

單一 Agent：
  一個 Agent 要做所有事情
  → 上下文視窗有限
  → 容易忘記前面做了什麼
  → 無法平行處理

多 Agent 系統：
  每個 Agent 專注於特定角色
  → 每個 Agent 有自己的上下文
  → 可以平行處理不同任務
  → 專業分工提高品質
```

## 多代理系統的基礎概念

### Agent 角色定義

在多代理系統中，每個 Agent 都有自己的「角色定義」（Role Prompt）：

```python
# 定義不同的 Agent 角色
agents = {
    "pm": Agent(
        role="專案經理",
        system_prompt="""你是一位經驗豐富的專案經理。
        你的職責是：
        1. 將使用者需求分解為具體任務
        2. 分配任務給適合的開發者
        3. 審查交付成果
        4. 確保專案按時完成"""
    ),
    "developer": Agent(
        role="工程師",
        system_prompt="""你是一位資深全端工程師。
        你的職責是：
        1. 根據規格實作程式碼
        2. 編寫測試
        3. 確保程式碼品質和效能
        4. 遇到問題時及時尋求協助"""
    ),
    "qa": Agent(
        role="測試工程師",
        system_prompt="""你是一位嚴謹的測試工程師。
        你的職責是：
        1. 設計測試案例
        2. 執行測試
        3. 報告並追蹤缺陷
        4. 驗證修復"""
    ),
}
```

### 協作模式

多代理系統主要有三種協作模式：

**1. 順序模式（Sequential）**

Agent 依序處理任務，每個 Agent 的輸出是下一個 Agent 的輸入：

```
使用者需求 → PM Agent → Developer Agent → QA Agent → 交付
                │             │               │
          分解任務        實作程式碼        測試驗證
```

**2. 層級模式（Hierarchical）**

有一個「管理員 Agent」負責協調多個「工人 Agent」：

```
                ┌──────────┐
                │  協調者   │
                │  (PM)    │
                └────┬─────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │ 工程師 1 │ │ 工程師 2 │ │ 測試員  │
    └─────────┘ └─────────┘ └─────────┘
```

**3. 圖狀模式（Graph）**

Agent 之間可以任意通訊，形成複雜的協作網路：

```
    搜尋 Agent ── 分析 Agent
        │              │
        └──────┬───────┘
               │
           撰寫 Agent ── 審查 Agent
                            │
                        輸出結果
```

## AutoGPT 與 BabyAGI 的啟發

### AutoGPT：第一個自主多代理系統

2023 年 3 月發布的 AutoGPT 雖然名義上是單一 Agent，但它內部實現了多代理的核心概念：

```
AutoGPT 的內部結構：
─────────────────

Agent 本體：
  ├── 任務生成器（Task Creator）
  │    └── 將大目標分解為子任務
  ├── 任務執行器（Task Executor）
  │    └── 使用工具執行每個子任務
  ├── 記憶系統（Memory System）
  │    └── 儲存已完成任務和經驗
  └── 優先級排序器（Priority Sorter）
       └── 決定先做哪個任務
```

AutoGPT 的局限性在於：所有元件共享同一個 LLM 上下文，導致：
- 任務一多就「忘記」前面的目標
- 沒有真正的專業分工
- 容易陷入重複循環

### BabyAGI：任務驅動的架構

BabyAGI（2023 年 4 月）引入了更清晰的任務佇列架構：

```python
class BabyAGI:
    def __init__(self):
        self.task_queue = []      # 任務佇列
        self.completed_tasks = [] # 已完成任務
        self.results = {}         # 任務結果
    
    def run(self, objective):
        # 1. 生成初始任務
        initial_tasks = self.create_initial_tasks(objective)
        self.task_queue.extend(initial_tasks)
        
        while self.task_queue:
            # 2. 取出最高優先級任務
            task = self.task_queue.pop(0)
            
            # 3. 執行任務
            result = self.execute_task(task)
            self.completed_tasks.append(task)
            self.results[task.id] = result
            
            # 4. 根據結果生成新任務
            new_tasks = self.create_tasks(
                objective, task, result
            )
            self.task_queue.extend(new_tasks)
```

BabyAGI 的任務佇列模式影響了後來許多 Agent 框架的設計。

## 多代理協作的關鍵技術

### 1. 代理間通訊（Inter-Agent Communication）

Agent 之間如何交換資訊？

```python
# 方法一：共享記憶體（Shared Memory）
shared_memory = {
    "project_status": "開發中",
    "current_sprint": "Sprint 3",
    "blockers": ["等待 API 文件"]
}

def pm_agent(shared_memory):
    # 讀取共享記憶體
    status = shared_memory["project_status"]
    # 做出決策
    shared_memory["next_action"] = "開始前端開發"

# 方法二：訊息傳遞（Message Passing）
message_queue = []

class AgentMessage:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

def agent_loop(agent_id, message_queue):
    while True:
        msg = message_queue.get()
        if msg.receiver == agent_id:
            response = process_message(msg)
            # 發送回應
            message_queue.put(
                AgentMessage(agent_id, msg.sender, response)
            )
```

### 2. 共識機制（Consensus）

多個 Agent 意見不一致時如何達成共識？

```
共識策略：
─────────────────

1. 投票（Voting）
   每個 Agent 投票，多數決
   適用於：程式碼審查、內容審核

2. 辯論（Debate）
   Agent 輪流發表觀點並回應對方的論點
   適用於：決策分析、策略規劃

3. 層級裁決（Hierarchical）
   上級 Agent 做出最終決定
   適用於：專案管理、資源分配

4. 加權平均（Weighted）
   根據 Agent 的信譽度加權
   適用於：專家諮詢系統
```

### 3. 任務分配與排程

```python
class TaskOrchestrator:
    def assign_task(self, task, agents):
        # 評估每個 Agent 的適合度
        best_agent = None
        best_score = -1
        
        for agent in agents:
            score = self.evaluate_fit(task, agent)
            if score > best_score:
                best_score = score
                best_agent = agent
        
        # 分配任務
        best_agent.assign(task)
        return best_agent
    
    def evaluate_fit(self, task, agent):
        score = 0
        # 技能匹配
        if task.required_skill in agent.skills:
            score += 10
        # 當前工作量
        score -= agent.current_load * 2
        # 歷史表現
        score += agent.performance_history * 3
        return score
```

## 實際應用的多代理模式

### 軟體開發團隊

這是最常見的多代理應用場景：

```
┌───────────────────────────────────────────────┐
│           AI 軟體開發團隊                        │
├───────────────────────────────────────────────┤
│                                                 │
│  產品經理 Agent                                 │
│  ├── 分析需求，撰寫規格                         │
│  ├── 分配任務給開發者                           │
│  └── 驗驗交付成果                               │
│                                                 │
│  開發者 Agent（可多個）                         │
│  ├── 根據規格實作功能                           │
│  ├── 撰寫單元測試                               │
│  └── 程式碼自我審查                             │
│                                                 │
│  測試 Agent                                     │
│  ├── 設計整合測試                               │
│  ├── 執行回歸測試                               │
│  └── 報告缺陷                                   │
│                                                 │
│  審查 Agent                                     │
│  ├── 程式碼風格檢查                             │
│  ├── 安全漏洞掃描                               │
│  └── 效能分析                                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 科學研究團隊

```
研究 Agent 團隊的協作流程：

1. 文獻回顧 Agent：搜尋並總結相關論文
2. 實驗設計 Agent：設計實驗方案
3. 資料分析 Agent：分析實驗資料
4. 論文撰寫 Agent：整理結果並撰寫論文
5. 審查 Agent：檢查邏輯漏洞和格式問題

使用案例：MIT 的研究團隊使用多 Agent 系統
在 2025 年完成了一篇材料的論文，從文獻回顧
到論文提交僅用了 48 小時。
```

### 客服中心

現代客服中心是多代理系統的經典應用：

```
客戶問題
    │
    ▼
分類 Agent → 判斷類別
    │
    ├── 帳務問題 → 帳務 Agent（查詢帳單、付款）
    ├── 技術問題 → 技術支援 Agent（排障、引導）
    ├── 退貨問題 → 退貨 Agent（申請退貨、退款）
    └── 複雜問題 → 升級給人類客服
```

## Microsoft AutoGen 的創新

### 多代理對話框架

AutoGen（2023 年 10 月發布）是 Microsoft 的多代理對話框架，引入了「代理間對話」的概念：

```python
from autogen import AssistantAgent, UserProxyAgent

# 定義 Agent
planner = AssistantAgent(
    name="Planner",
    system_message="你是一個規劃專家，負責制定計畫"
)

executor = AssistantAgent(
    name="Executor",
    system_message="你是一個執行者，負責執行程式碼"
)

critic = AssistantAgent(
    name="Critic",
    system_message="你是一個評論家，負責找出問題"
)

# 啟動多代理對話
def solve_problem(task):
    # Planner 制定計畫
    plan = planner.generate_reply(task)
    
    # Executor 執行
    result = executor.generate_reply(plan)
    
    # Critic 審查
    feedback = critic.generate_reply(result)
    
    return feedback
```

AutoGen 的關鍵創新是：Agent 之間不只需要共享結果，更需要進行「對話」——包括提問、回答、質疑、辯論。

## 多代理系統的挑戰

### 1. 通訊開銷

隨著 Agent 數量增加，通訊成本呈平方級增長：

```
Agent 數量    通訊通道數
    2             1
    5            10
   10            45
   20           190
  100         4,950

解決方案：
- 使用 Agent 分組（Team）
- 引入管理員角色
- 使用匯流排（Bus）模式
```

### 2. 協調失敗

```
常見的多代理協調問題：

1. 任務重複：兩個 Agent 做了同一件事
   解決：工作鎖定（Task Locking）

2. 資源競爭：多個 Agent 爭奪同一資源
   解決：資源調度器（Resource Scheduler）

3. 矛盾指令：不同 Agent 給出衝突的指示
   解決：版本控制（Version Control）

4. 級聯錯誤：一個 Agent 的錯誤被放大
   解決：隔離邊界（Isolation Boundary）
```

### 3. 除錯困難

「哪個 Agent 做了什麼？」——當系統出錯時，追溯責任非常困難。

## 結語

多代理系統代表了 AI Agent 從「單兵作戰」到「團隊協作」的進化。從 AutoGPT 的雛形到 AutoGen 的成熟框架，多代理協作正在成為處理複雜任務的標準方法。

關鍵的經驗是：**不是 Agent 越多越好——好的多代理系統需要清晰的角色定義、有效的溝通機制，以及合理的錯誤處理策略**。

下一篇文章將介紹 Agent 的記憶與知識管理——如何讓 Agent 記住過去的經驗並有效利用知識。

---

## 延伸閱讀

- [AutoGPT 架構](https://www.google.com/search?q=AutoGPT+architecture+design)
- [Microsoft AutoGen](https://www.google.com/search?q=Microsoft+AutoGen+multi-agent)
- [CrewAI 多代理框架](https://www.google.com/search?q=CrewAI+multi-agent+framework)
- [多代理系統設計模式](https://www.google.com/search?q=multi-agent+system+design+patterns)

---

*本篇文章為「AI 程式人雜誌 2026 年 5 月號」歷史回顧系列之一。*
