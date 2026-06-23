# 從單一 Agent 到多 Agent（1956-2026）

## Agent 概念的起源

「Agent」一詞在 AI 領域的歷史可以追溯到 1956 年的達特茅斯會議——AI 作為一門學科的誕生時刻。與會者 John McCarthy 提出了「人工智慧」這個術語，同時也埋下了 Agent 概念的種子：一個能感知環境、做出決策、採取行動的自主實體。

從 1960 年代的 STRIPS 規劃系統（Stanford Research Institute Problem Solver）到 1980 年代的 SOAR 架構，AI Agent 經歷了從符號主義到行為主義的多次轉向。但直到 2022 年，LLM-based Agent 的出現才真正讓「Agent」這個概念進入主流視野。

### 為什麼 LLM 讓 Agent 變得可行？

傳統 Agent 的問題在於「通用性」與「靈活度」之間的取捨。規劃系統需要預先定義所有可能的動作和狀態。LLM 改變了這個局面：

```python
# 傳統 Agent vs LLM Agent
class TraditionalAgent:
    def act(self, state: str) -> str:
        # 必須預先定義所有轉換規則
        if state == "door_closed" and self.has_key:
            return "open_door"
        raise ValueError("Unknown state")

class LLMAgent:
    def act(self, observation: str) -> str:
        # LLM 可以理解任意自然語言描述的狀態
        prompt = f"當前環境：{observation}\n請決定下一步行動："
        return self.llm.generate(prompt)
```

## 為什麼需要多 Agent？

單一 Agent 的能力再強，也有其邊界。多 Agent 系統的優勢來自三個方面：

**1. 複雜任務分解**：一個撰寫整本書的 Agent 不如一個 Editor + 多個 Writer 協作有效率。

**2. 專業化**：每個 Agent 可以綁定不同的工具和知識庫——一個專精 Python 的 Coder Agent 不需要載入 Java 文件。

**3. 容錯**：當一個 Agent 產生幻覺時，其他 Agent 可以透過交叉驗證發現錯誤。

```python
# 多 Agent 交叉驗證範例
responses = []
for agent in [coder_agent, reviewer_agent, tester_agent]:
    responses.append(agent.run(task))

# 只有兩個以上 Agent 同意的結果才接受
if sum(r == responses[0] for r in responses) >= 2:
    final_result = responses[0]
else:
    final_result = orchestrator.resolve_conflict(responses)
```

## 多 Agent 架構模式

### Orchestrator + Workers（協調者—工作者模式）

最常見的模式。一個 Orchestrator Agent 負責分解任務、分派給 Worker Agent、合併結果：

```
使用者 → Orchestrator → [Coder, Reviewer, Tester]
                          → 結果合併 → 使用者
```

### Peer-to-Peer（點對點模式）

Agent 之間可以直接溝通，沒有中心協調者。適用於 Agent 數量較少且互信的場景：

```python
# Peer-to-Peer 訊息傳遞
class PeerAgent:
    def __init__(self, name, peers=None):
        self.name = name
        self.peers = peers or []

    def broadcast(self, message):
        for peer in self.peers:
            peer.receive(self.name, message)

    def receive(self, sender, message):
        response = self.process(message)
        return response
```

### Marketplace（市場模式）

Agent 透過「市場」發布任務和競標。適合動態組合團隊的場景：

```
任務發布 → Agent 競標 → 最適合者得標 → 執行 → 付款
```

## 2026 年 Agent 生態全景

| 層次 | 代表性專案 | 特點 |
|------|-----------|------|
| 框架 | AutoGen、CrewAI、LangGraph | 高階抽象，快速搭建 |
| 協定 | A2A（Google）、Anthropic MCP | 標準化通訊與工具 |
| 工具 | Function Calling、Code Interpreter | 能力擴展 |
| 模型 | GPT-5、Claude 4、Gemini 3 | 基礎推理能力 |
| 監控 | LangSmith、Weights & Biases | 可觀測性 |

---

**下一步**：[Agent 角色設計與專業化](focus2.md)

## 延伸閱讀

- [Multi-Agent 系統概述](https://www.google.com/search?q=multi+agent+system+overview+2026)
- [AutoGen 架構](https://www.google.com/search?q=AutoGen+multi+agent+architecture)
- [Agent 生態全景](https://www.google.com/search?q=LLM+agent+ecosystem+2026)
