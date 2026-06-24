# ReAct 與思考鏈：Agent 的推理核心（2022-2024）

## 從提示工程到推理模式

2022 年末，ChatGPT 的發布讓全世界看到了大語言模型的對話能力。但很快，研究者和開發者發現：單純的「問答」模式遠遠不夠——要讓 LLM 真正解決複雜問題，需要引導它進行 **推理**。

這標誌著從「提示工程」（Prompt Engineering）到「推理工程」（Reasoning Engineering）的轉變。

## Chain-of-Thought：讓 LLM 學會思考

### 什麼是思考鏈（CoT）？

2022 年 1 月，Google 研究員 Jason Wei 等人發表了「Chain-of-Thought Prompting」論文——這項簡單卻強大的技術，開啟了 LLM 推理能力的大門。

核心思想：**不要直接問答案，而是引導 LLM 產生中間推理步驟**。

```
傳統提示：
Q：羅傑有 5 個網球，他又買了 2 罐，每罐有 3 個。他現在有多少個？
A：11

思考鏈提示：
Q：羅傑有 5 個網球，他又買了 2 罐，每罐有 3 個。他現在有多少個？
A：羅傑一開始有 5 個網球。
   2 罐網球，每罐 3 個，共 2 × 3 = 6 個。
   總共 5 + 6 = 11 個。
   答案是 11。
```

### 思考鏈的幾種變體

**1. 零樣本思考鏈（Zero-shot CoT）**

只需在提示後加上「讓我們一步步思考」：

```
Q：羅傑有 5 個網球，他又買了 2 罐，每罐有 3 個。他現在有多少個？
A：讓我們一步步思考。
```

LLM 會自動生成推理步驟。

**2. 自動思考鏈（Auto-CoT）**

自動將問題分為多個階段，無需手動編寫範例。

**3. 多樣化思考鏈（Diverse CoT）**

生成多個不同的推理路徑，然後投票選出最一致的答案——這類似於「集體智慧」的概念。

## Tree-of-Thoughts：從線性到樹狀推理

### 超越線性思維

2023 年，普林斯頓大學的研究者提出了 Tree-of-Thoughts（ToT）——將 CoT 的線性推理擴展為樹狀搜索：

```
Chain-of-Thought（線性）：
    思考1 → 思考2 → 思考3 → 思考4 → 答案

Tree-of-Thoughts（樹狀）：
                 思考1
                /    \
           思考2a    思考2b
           /    \    /    \
       思考3a 思考3b 思考3c 思考3d
           \    /     \    /
           答案1      答案2
```

### ToT 的核心演算法

```
┌───────────────────────────────────────────────┐
│           Tree-of-Thoughts 演算法              │
├───────────────────────────────────────────────┤
│                                                 │
│  1. 從初始狀態開始                               │
│  2. 生成下一階段的 k 個候選想法                   │
│  3. 評估每個候選的「前景」                        │
│  4. 選擇最有前景的候選繼續探索                    │
│  5. 如果遇到死胡同則回溯                         │
│  6. 找到滿足條件的完整路徑即為解答                │
│                                                 │
│  BFS 版本：逐層探索所有分支                      │
│  DFS 版本：深入探索最有希望的路徑                │
│                                                 │
└─────────────────────────────────────────────────┘
```

ToT 的關鍵洞察是：**人類解決複雜問題時，並不是沿著一條直線思考的——我們會考慮多種可能性，在遇到困難時回溯，嘗試不同的路徑**。

## ReAct：推理與行動的交織

### 從思考到行動

2022 年 10 月，Google 的另一組研究者（Shunyu Yao 等人）發表了 ReAct——這可能是 LLM Agent 領域最重要的單篇論文。

ReAct 的核心思想非常簡單：**讓推理軌跡（Reasoning）和行動（Acting）交替進行**。

```
┌───────────────────────────────────────────────┐
│              ReAct 循環                          │
├───────────────────────────────────────────────┤
│                                                 │
│  問題：今天的台北天氣如何？適合去陽明山嗎？      │
│                                                 │
│  Thought 1: 我需要先查台北的天氣               │
│  Action 1: search_weather("台北")               │
│  Observation 1: 台北今天 25°C，多雲             │
│                                                 │
│  Thought 2: 25°C 多雲很適合戶外活動，            │
│             再來查陽明山的即時狀況               │
│  Action 2: search_info("陽明山 即時")            │
│  Observation 2: 陽明山目前人潮中等，步道開放     │
│                                                 │
│  Thought 3: 天氣和路況都適合，建議去             │
│  Final Answer: 非常適合！今天台北 25°C 多雲，    │
│                陽明山步道開放，建議早上出發...    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### ReAct 為什麼有效？

ReAct 的優勢來自於推理與行動的協同作用：

1. **推理引導行動**：LLM 的常識推理告訴它需要什麼資訊
2. **行動豐富推理**：外部工具的觀測結果為推理提供事實基礎
3. **減少幻覺**：透過查詢外部來源，Agent 不再完全依賴模型參數中的知識
4. **可解釋性**：Thought → Action → Observation 的完整軌跡讓決策過程透明化

### ReAct 的 Python 實作框架

```python
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm        # 語言模型
        self.tools = tools    # 可用工具列表
        self.memory = []      # 互動歷史
    
    def run(self, task):
        self.memory.append(f"Task: {task}")
        
        for step in range(max_steps):
            # 1. 思考：下一步該做什麼
            thought = self.llm.generate(
                self.memory + ["Thought:"]
            )
            self.memory.append(f"Thought: {thought}")
            
            # 2. 行動：執行特定工具
            action = self.parse_action(thought)
            if action["type"] == "final_answer":
                return action["answer"]
            
            result = self.execute_tool(action)
            self.memory.append(f"Observation: {result}")
        
        return "Max steps reached"
```

## Graph-of-Thoughts：更高級的推理結構

### 從樹到圖

2023 年，研究者進一步提出了 Graph-of-Thoughts（GoT），將推理結構從樹擴展為有向無環圖：

```
Graph-of-Thoughts（圖狀）：
    
    思考1 ──┬── 思考3 ── 思考5 ── 答案
            │
    思考2 ──┴── 思考4 ── 思考6 ── 答案
    
    - 思考1 和 思考2 可以合併到 思考3
    - 思考3 和 思考4 可以同時饋入 思考5 和 思考6
    - 支援「聚合」、「合併」、「循環」等操作
```

GoT 允許 Agent 進行更靈活的推理——合併多個思路、回溯到前面的節點、甚至形成推理循環。

## 從提示模式到 Agent 框架

### 2023 年的 Agent 爆發

2023 年是 LLM Agent 的元年。幾項關鍵發展推動了從「提示模式」到「完整 Agent 框架」的轉變：

**1. AutoGPT（2023 年 3 月）**

AutoGPT 是第一個引起廣泛關注的自主 Agent 系統。它使用 GPT-4，能夠：
- 將大任務分解為子任務
- 使用瀏覽器、程式碼執行器等工具
- 自我反思和改進
- 長期執行數小時的複雜任務

雖然 AutoGPT 的實作相對粗糙（容易陷入循環、幻覺嚴重），但它證明了 LLM Agent 的潛力。

**2. BabyAGI（2023 年 4 月）**

BabyAGI 展示了基於任務佇列的 Agent 架構：
```
┌───────────────────────────────────────────────┐
│              BabyAGI 任務循環                    │
├───────────────────────────────────────────────┤
│                                                 │
│  1. 從任務佇列中取出最優先的任務                  │
│  2. 使用 LLM 執行任務                            │
│  3. 根據結果生成新的子任務                        │
│  4. 將新任務加入佇列，設定優先級                  │
│  5. 重複直到任務佇列為空                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**3. 函式呼叫（Function Calling）**

2023 年 6 月，OpenAI 發布了 GPT-4 的函式呼叫能力——這是 LLM Agent 工具使用的關鍵突破。從此，Agent 不再需要從文字中解析工具呼叫，LLM 可以結構化地輸出工具參數：

```json
// 使用者：台北天氣如何？
// LLM 輸出：
{
  "function": "get_weather",
  "parameters": {
    "location": "台北",
    "unit": "celsius"
  }
}
```

## 從 CoT 到 Agent 的橋樑

### 思考模式的分類

| 思考模式 | 結構 | 工具使用 | 適用場景 |
|---------|------|---------|---------|
| CoT | 線性 | 否 | 數學推理、邏輯問題 |
| ToT | 樹狀 | 否 | 創意寫作、策略規劃 |
| ReAct | 循環 | 是 | 資訊檢索、任務執行 |
| GoT | 圖狀 | 是 | 複雜分析、研究任務 |

### 從推理到行動的連續譜

```
純推理                    純行動
  │                         │
  CoT ── ToT ── ReAct ── Agent ── AutoGPT
  │        │        │        │        │
  只有     樹狀     推理+    完整     完全
  思考     思考     單步     工具     自主
                    行動     使用     執行
```

## 結語

2022-2024 年是 LLM Agent 推理能力的奠基時期。Chain-of-Thought 讓 LLM 學會了「思考」，ReAct 讓 LLM 學會了「行動」，而 Tree/Graph-of-Thoughts 讓 LLM 學會了「探索不同可能性」。

這些技術的發展揭示了 LLM Agent 的核心設計原則：**推理與行動不是分離的——最好的 Agent 在行動中思考，在思考中行動**。

下一篇文章將介紹 Agent 的工具使用能力——從 OpenAI 的 Function Calling 到 MCP 標準協議，Agent 如何獲得「雙手」和「感官」。

---

## 延伸閱讀

- [Chain-of-Thought Prompting](https://www.google.com/search?q=Chain-of-Thought+Prompting+Wei+2022)
- [Tree-of-Thoughts](https://www.google.com/search?q=Tree-of-Thoughts+LLM+reasoning)
- [ReAct: Synergizing Reasoning and Acting](https://www.google.com/search?q=ReAct+reasoning+acting+paper)
- [AutoGPT 原始碼](https://www.google.com/search?q=AutoGPT+github)

---

*本篇文章為「AI 程式人雜誌 2026 年 5 月號」歷史回顧系列之一。*
