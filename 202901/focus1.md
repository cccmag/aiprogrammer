# 從工作流到自主 Agent（2018-2029）

## 工作流自動化的十年演進

### 前言

2018 年，AI 工作流還停留在「if-this-then-that」的規則引擎時代。2029 年，自主 Agent 已經能動態規劃、執行和修正多步驟任務。這十年間發生了什麼？

### 規則引擎時代（2018-2020）

早期的 AI 工作流依賴預定義的規則鏈：

```python
# 2018：規則引擎式工作流
if intent == "book_flight":
    search_flight()
    if price < budget:
        confirm_booking()
        send_email()
    else:
        ask_for_budget_increase()
```

這種方式的問題是**缺乏彈性**——任何未預見的邊界情況都會導致流程中斷。

### Prompt 鏈時代（2021-2023）

LLM 的出現催生了 Prompt 鏈（Prompt Chaining）：

```python
# 2022：Prompt 鏈工作流
def research_pipeline(topic):
    outline = llm(f"為 '{topic}' 生成大綱")
    sections = [llm(f"撰寫章節：{s}") for s in outline]
    summary = llm(f"總結：{''.join(sections)}")
    return summary
```

每個步驟的輸出成為下一步的輸入——簡單但脆弱。

### Agent 框架興起（2024-2026）

ReAct（Reasoning + Acting）模式改變了遊戲規則：

```python
# 2025：ReAct Agent
class Agent:
    def run(self, task):
        while not self.done:
            thought = self.llm.reason(observation)
            action = self.llm.act(thought)
            result = self.execute(action)
            observation = f"Action result: {result}"
```

Agent 不再遵循固定流程，而是**即時推理下一步**。

### 多 Agent 協作（2027-2029）

2027 年後，工作流從單一 Agent 進化為多 Agent 協作：

```python
# 2029：多 Agent 協作工作流
orchestrator = Orchestrator([
    Researcher(), Planner(), Coder(), Reviewer()
])
result = orchestrator.run("建立一個電商網站")
```

### 小結

從 2018 的規則引擎到 2029 的自主多 Agent 系統，工作流自動化的核心轉變是：**從預定義路徑到動態規劃，從單一執行到協作推理**。

---

**下一步**：[Agent 工作流設計模式](focus2.md)

## 延伸閱讀

- [ReAct 模式介紹](https://www.google.com/search?q=ReAct+Reasoning+Acting+AI+agent)
- [多 Agent 協作架構](https://www.google.com/search?q=multi+agent+orchestration+2024+2025)
- [LLM 工作流演進史](https://www.google.com/search?q=LLM+workflow+evolution+2018+2024)
