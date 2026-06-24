# 意圖識別與對話管理

## 前言

對話式 UI 的核心挑戰是 **意圖識別**（Intent Recognition）與 **對話管理**（Dialogue Management）。系統必須從使用者的自然語言輸入中推斷真實意圖，並根據對話歷史決定下一步行動。

## 意圖分類器

### 基於嵌入的意圖匹配

現代系統通常使用語義嵌入取代傳統的關鍵字匹配：

```python
import numpy as np
from typing import List, Dict

class IntentClassifier:
    def __init__(self):
        self.intents = {}
        self.threshold = 0.75

    def register_intent(self, name: str, examples: List[str]):
        embeddings = [self._fake_embed(ex) for ex in examples]
        self.intents[name] = {
            "center": np.mean(embeddings, axis=0),
            "examples": examples,
        }

    def _fake_embed(self, text: str) -> np.ndarray:
        np.random.seed(hash(text) % 2**31)
        return np.random.randn(128)

    def classify(self, text: str) -> tuple:
        emb = self._fake_embed(text)
        best_name, best_score = None, 0.0
        for name, data in self.intents.items():
            score = np.dot(emb, data["center"]) / (
                np.linalg.norm(emb) * np.linalg.norm(data["center"])
            )
            if score > best_score:
                best_score = score
                best_name = name
        if best_score >= self.threshold:
            return best_name, best_score
        return "unknown", best_score

clf = IntentClassifier()
clf.register_intent("query_weather", ["今天天氣如何", "會下雨嗎"])
clf.register_intent("set_alarm", ["設鬧鐘", "明天早上叫我"])
print(clf.classify("台北會下雨嗎"))
```

## 槽位填充

### 基於規則的槽位抽取

意圖識別後需要填充必需的參數（slots）：

```python
import re

class SlotFiller:
    def __init__(self):
        self.patterns = {
            "date": r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?",
            "time": r"\d{1,2}[:：]\d{2}",
            "location": r"在(.{2,6})",
            "number": r"\d+",
        }

    def extract(self, text: str) -> Dict[str, str]:
        slots = {}
        for slot_name, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                slots[slot_name] = match.group(0)
        return slots

    def missing_slots(self, intent: str, slots: Dict) -> List[str]:
        required = {
            "set_alarm": ["time", "date"],
            "query_weather": ["date", "location"],
        }
        return [s for s in required.get(intent, []) if s not in slots]

filler = SlotFiller()
text = "明天早上8:00叫我"
print(filler.extract(text))
```

## 對話狀態追蹤

### 狀態機管理

對話管理需要維護一個**對話狀態**，跟蹤已收集的資訊和待辦事項：

```python
class DialogueStateMachine:
    def __init__(self):
        self.state = "init"
        self.slots = {}
        self.history = []

    def transition(self, intent: str, slots: Dict):
        self.history.append((self.state, intent, slots))
        if self.state == "init":
            self.slots.update(slots)
            if intent == "set_alarm":
                if "time" in slots and "date" in slots:
                    self.state = "confirmed"
                else:
                    self.state = "awaiting_slots"
        elif self.state == "awaiting_slots":
            self.slots.update(slots)
            required = ["time", "date"]
            if all(r in self.slots for r in required):
                self.state = "confirmed"
        return self.state

    def next_prompt(self) -> str:
        prompts = {
            "init": "請問需要什麼協助？",
            "awaiting_slots": "請提供日期和時間",
            "confirmed": "已確認設定",
        }
        return prompts.get(self.state, "請重新輸入")
```

## 多輪對話範例

### 完整的對話流程

```python
class DialogueSystem:
    def __init__(self):
        self.clf = IntentClassifier()
        self.filler = SlotFiller()
        self.dsm = DialogueStateMachine()

    def respond(self, user_input: str) -> str:
        intent, score = self.clf.classify(user_input)
        if intent == "unknown":
            return "抱歉，我不太理解您的意思"
        slots = self.filler.extract(user_input)
        state = self.dsm.transition(intent, slots)
        if state == "confirmed":
            params = ", ".join(f"{k}={v}" for k, v in self.dsm.slots.items())
            return f"已設定：{params}"
        return self.dsm.next_prompt()

system = DialogueSystem()
print(system.respond("設鬧鐘"))
print(system.respond("早上 7:00"))
```

## 結語

意圖識別與對話管理是對話式 AI 的骨幹。精確的意圖分類、完整的槽位填充、以及狀態機式的對話管理，共同構成了流暢人機對話的基礎設施。

---

**延伸閱讀**

- [意圖識別技術比較](https://www.google.com/search?q=intent+recognition+NLU+comparison+2026)
- [對話狀態追蹤方法](https://www.google.com/search?q=dialogue+state+tracking+DST)
- [槽位填充演算法](https://www.google.com/search?q=slot+filling+NLP+algorithms)
