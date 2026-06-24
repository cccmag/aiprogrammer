# 對話式 UI 設計原則（2020-2029）

## 從 GUI 到 CUI

對話式 UI（Conversational UI）重新定義了人機互動的基本單位——從「點擊」變成了「對話」。

### 核心設計原則

#### 1. 漸進式揭露

不要一次給出所有資訊，而是根據對話脈絡逐步呈現：

```python
class ProgressiveDisclosure:
    def __init__(self):
        self.context_depth = 0

    def respond(self, query: str, user_expertise: str) -> str:
        if user_expertise == "beginner":
            return f"簡單來說：{self.simplify(query)}"
        elif user_expertise == "expert":
            self.context_depth += 1
            return f"深入分析（層級{self.context_depth}）：{self.detail(query)}"
        return f"說明：{self.summarize(query)}"

    def simplify(self, q: str) -> str:
        return q[:50] + "..."

    def detail(self, q: str) -> str:
        return q + "（含技術規格與參考文獻）"

    def summarize(self, q: str) -> str:
        return q[:100]
```

參見：[漸進式揭露設計](https://www.google.com/search?q=progressive+disclosure+conversational+UI+design)

#### 2. 容錯與修復

對話式 UI 必須處理模糊與錯誤：

```python
class ErrorRecovery:
    def handle_ambiguity(self, intent: str, confidence: float) -> str:
        if confidence < 0.3:
            return "抱歉，我不太確定您的意思。可以換個說法嗎？"
        if confidence < 0.7:
            return f"我猜您想「{intent}」，對嗎？"
        return f"好的，正在執行「{intent}」。"
```

#### 3. 上下文記憶

有效的對話 UI 必須記住對話歷史：

```python
class ConversationalMemory:
    def __init__(self):
        self.turns: list[dict] = []

    def add_turn(self, role: str, message: str):
        self.turns.append({"role": role, "msg": message, "time": time.time()})

    def recall(self, key: str) -> list[str]:
        return [t["msg"] for t in self.turns if key in t["msg"]]

    def context_window(self, n: int = 5) -> str:
        recent = self.turns[-n:]
        return "\n".join(f"{t['role']}: {t['msg']}" for t in recent)
```

### 設計演化時間線

| 年份 | 里程碑 | 影響 |
|------|--------|------|
| 2020 | GPT-3 問世 | 自然語言理解門檻大幅降低 |
| 2021 | 多輪對話框架成熟 | 上下文管理標準化 |
| 2022 | ChatGPT 發布 | 對話式 UI 成為主流 |
| 2023 | Plugin 生態系 | 對話介面連結外部工具 |
| 2024 | 多模態對話 | 文字+圖片+語音混合 |
| 2025 | 主動對話 AI | AI 可主動發起對話 |
| 2026 | 長期記憶對話 | 跨 session 記憶 |

## 關鍵研究

- [對話式 UI 設計模式](https://www.google.com/search?q=conversational+UI+design+patterns+2024)
- [ChatGPT 對 UI 設計的影響](https://www.google.com/search?q=ChatGPT+impact+on+UI+design+2023)
- [對話式 UX 最佳實踐](https://www.google.com/search?q=conversational+UX+best+practices+2025)

## 結語

好的對話式 UI 不是模仿人類對話，而是創造人類與 AI 之間最高效的溝通管道。

---

*本篇文章為「AI 程式人雜誌 2026 年 9 月號」人機協作介面設計系列之二。*
