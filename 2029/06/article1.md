# 對話式 UI 設計模式

## 前言

人機協作的第一道關卡就是對話。對話式 UI（Conversational UI）從早期的命令列發展到當代的大型語言模型介面，已成為 AI 與人類溝通的主流模式。本文探討核心設計模式。

## 基礎架構

對話式 UI 的核心是 **turn-taking**（輪流發言）機制。以下是一個基礎的對話管理器：

```python
import json
from datetime import datetime
from typing import List, Dict

class TurnManager:
    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.max_history = max_history

    def add_turn(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

    def get_context(self) -> str:
        return "\n".join(
            f"{t['role']}: {t['content']}"
            for t in self.history[-6:]
        )

manager = TurnManager()
manager.add_turn("user", "幫我安排明天的行程")
manager.add_turn("assistant", "請問明天幾點出發？")
print(manager.get_context())
```

## 四種核心模式

### 1. 引導式對話

當使用者輸入模糊時，系統應主動引導而非猜測：

```python
def guided_clarification(user_input: str) -> str:
    ambiguity_patterns = {
        "安排": ["時間", "地點", "人數"],
        "查詢": ["關鍵字", "日期範圍", "排序方式"],
    }
    for keyword, slots in ambiguity_patterns.items():
        if keyword in user_input:
            missing = [s for s in slots if s not in user_input]
            if missing:
                return f"請問您要指定的{','.join(missing)}是什麼？"
    return ""
```

### 2. 確認回圈

重要操作採用**先確認再執行**的雙階段模式：

```python
class ConfirmationLoop:
    def __init__(self):
        self.pending_actions = {}

    def propose(self, action_id: str, action: str, params: dict):
        self.pending_actions[action_id] = (action, params)
        return f"確認要執行「{action}」嗎？參數：{json.dumps(params, ensure_ascii=False)}"

    def confirm(self, action_id: str) -> str:
        if action_id in self.pending_actions:
            action, params = self.pending_actions.pop(action_id)
            return f"已執行「{action}」"
        return "無待確認的操作"
```

### 3. 漸進式揭露

一次呈現過多資訊會造成認知負擔。採用分層展示：

```python
def progressive_disclosure(data: List[str], level: int = 1):
    if level == 1:
        return f"共有 {len(data)} 筆結果"
    elif level == 2:
        return "\n".join(data[:5])
    elif level >= 3:
        return "\n".join(data)

results = ["結果A", "結果B", "結果C", "結果D", "結果E", "結果F"]
print(progressive_disclosure(results, 1))
print(progressive_disclosure(results, 2))
```

### 4. 錯誤預期

預先考慮可能的錯誤並提供修正建議：

```python
def fuzzy_command_match(command: str, commands: dict) -> str:
    from difflib import get_close_matches
    if command in commands:
        return commands[command]
    close = get_close_matches(command, commands.keys(), n=1, cutoff=0.6)
    if close:
        return f"您是否想輸入「{close[0]}」？"
    return "不支援的指令"
```

## 結語

良好的對話式 UI 設計需要平衡**效率**與**安全性**。引導式對話減少使用者困惑，確認回圈防止誤操作，漸進式揭露避免資訊過載，錯誤預期提升容錯能力。

---

**延伸閱讀**

- [對話式 UI 設計原則](https://www.google.com/search?q=conversational+UI+design+patterns+2026)
- [Turn-taking 機制研究](https://www.google.com/search?q=conversational+turn+taking+design)
- [大型語言模型對話系統](https://www.google.com/search?q=LLM+conversation+system+design)
