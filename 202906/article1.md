# 對話式 UI 設計模式

## 前言

對話式 UI（Conversational UI）是人機協作最直觀的介面形式。從簡單的問答機器人到複雜的多輪對話系統，設計模式決定了使用者體驗的成敗。本文探討對話式 UI 的核心設計模式及 Python 實作。

## 基礎對話模式

### 線性對話

最簡單的問答模式，適用於表單填寫類任務：

```python
class LinearDialog:
    def __init__(self):
        self.steps = [
            ("name", "請輸入您的姓名："),
            ("email", "請輸入電子郵件："),
            ("goal", "您想達成什麼目標？"),
        ]
        self.responses = {}

    def run(self):
        for key, prompt in self.steps:
            self.responses[key] = input(prompt)
        return self.responses

    def validate_email(self):
        import re
        email = self.responses.get("email", "")
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

dialog = LinearDialog()
result = dialog.run()
print(f"驗證結果：{dialog.validate_email()}")
```

### 分支對話

根據使用者意圖動態選擇對話路徑：

```python
class BranchingDialog:
    def __init__(self):
        self.state = "start"

    def handle(self, user_input):
        if self.state == "start":
            if "問題回報" in user_input:
                self.state = "bug_report"
                return "請描述您遇到的問題："
            elif "功能建議" in user_input:
                self.state = "feature_request"
                return "請描述您想要的功能："
            return "請選擇：問題回報 / 功能建議 / 其他"
        elif self.state == "bug_report":
            self.state = "confirm"
            return f"已記錄問題：{user_input}，是否回傳系統日誌？（是/否）"
        elif self.state == "feature_request":
            self.state = "done"
            return f"感謝您的建議：{user_input}，我們會評估此功能"
        elif self.state == "confirm":
            return "感謝您的回報，我們將盡快處理" if "是" in user_input else "已記錄，感謝"
        return "我不太理解您的意思，請重新輸入"

dialog = BranchingDialog()
for msg in ["功能建議", "增加深色模式", "否"]:
    print(f"使用者：{msg}")
    print(f"系統：{dialog.handle(msg)}")
```

## 對話管理原則

好的對話 UI 需遵循幾項關鍵原則：

1. **可撤銷性**：使用者應能回退到上一步
2. **預測性回應**：根據上下文預測使用者可能的下一步
3. **錯誤寬容**：對輸入錯誤保持彈性
4. **狀態提示**：清楚顯示當前對話階段

## 多輪對話狀態機

```python
from enum import Enum

class DialogState(Enum):
    GREETING = 1
    COLLECT_INFO = 2
    CONFIRMATION = 3
    COMPLETION = 4

class MultiTurnDialog:
    def __init__(self):
        self.state = DialogState.GREETING
        self.context = {}

    def process(self, text):
        if self.state == DialogState.GREETING:
            self.state = DialogState.COLLECT_INFO
            return "您好！請問有什麼可以協助您的？"
        elif self.state == DialogState.COLLECT_INFO:
            self.context["request"] = text
            self.state = DialogState.CONFIRMATION
            return f"您想要：{text}，是否確認？（是/否）"
        elif self.state == DialogState.CONFIRMATION:
            if "是" in text:
                self.state = DialogState.COMPLETION
                return "已收到您的請求，正在處理中"
            self.state = DialogState.COLLECT_INFO
            return "請重新描述您的需求"
        return "感謝您的使用"

dialog = MultiTurnDialog()
for turn in ["您好", "我需要設定提醒", "是"]:
    print(dialog.process(turn))
```

---

**延伸閱讀**

- [Conversational UI Design Patterns](https://www.google.com/search?q=Conversational+UI+design+patterns)
- [Chatbot Dialog Management](https://www.google.com/search?q=chatbot+dialog+management+state+machine)
- [Human-AI Conversation Design](https://www.google.com/search?q=human+AI+conversation+design+guidelines)
