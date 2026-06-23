# AI 行為透明度

## 前言

AI 行為透明度是指系統能清楚展示其推理過程、限制與意圖。透明的 AI 讓使用者更容易理解、預測和控制系統行為，進而建立穩固的協作關係。

## 決策軌跡記錄

```python
from datetime import datetime
import json

class DecisionTrace:
    def __init__(self):
        self.traces = []

    def record(self, action, inputs, logic, output):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "inputs": inputs,
            "logic": logic,
            "output": output,
        }
        self.traces.append(entry)
        return len(self.traces) - 1

    def get_trace(self, trace_id):
        if trace_id < len(self.traces):
            return self.traces[trace_id]
        return None

    def summarize(self, trace_id):
        trace = self.get_trace(trace_id)
        if not trace:
            return "無記錄"
        return (
            f"動作：{trace['action']}\n"
            f"輸入：{trace['inputs']}\n"
            f"邏輯：{trace['logic']}\n"
            f"結果：{trace['output']}"
        )

    def export(self):
        return json.dumps(self.traces, ensure_ascii=False, indent=2)

class TransparentClassifier:
    def __init__(self):
        self.trace = DecisionTrace()

    def classify(self, text, rules):
        reasons = []
        for rule_name, pattern, label in rules:
            if pattern in text:
                reasons.append(f"符合規則「{rule_name}」：包含關鍵詞「{pattern}」")
        final = "positive" if reasons else "negative"
        self.trace.record(
            action="text_classify",
            inputs={"text": text},
            logic=reasons,
            output={"label": final, "reasons": reasons},
        )
        return {"label": final, "reasons": reasons}

classifier = TransparentClassifier()
rules = [("正面用語", "好", "positive"), ("負面用語", "差", "negative")]
result = classifier.classify("這個產品很好", rules)
print(classifier.trace.summarize(0))
```

## 系統狀態可視化

```python
import time

class AIStatusBoard:
    def __init__(self):
        self.modules = {
            "nlp": {"status": "idle", "progress": 0},
            "recommender": {"status": "idle", "progress": 0},
            "planner": {"status": "idle", "progress": 0},
        }

    def update_status(self, module, status, progress=None):
        if module in self.modules:
            self.modules[module]["status"] = status
            if progress is not None:
                self.modules[module]["progress"] = progress

    def display(self):
        status_icons = {
            "idle": "⚪",
            "processing": "🔄",
            "done": "✅",
            "error": "❌",
        }
        for module, info in self.modules.items():
            icon = status_icons.get(info["status"], "⚪")
            bar = "█" * (info["progress"] // 10) + "░" * (10 - info["progress"] // 10)
            print(f"{icon} {module}: [{bar}] {info['status']}")

    def simulate(self):
        self.update_status("nlp", "processing", 30)
        self.update_status("recommender", "processing", 10)
        self.display()
        time.sleep(1)
        self.update_status("nlp", "done", 100)
        self.update_status("recommender", "processing", 60)
        self.display()

board = AIStatusBoard()
board.simulate()
```

## 限制與不確定性溝通

```python
class UncertaintyCommunicator:
    def __init__(self):
        self.known_limits = []

    def add_limit(self, condition, description):
        self.known_limits.append({
            "condition": condition,
            "description": description,
        })

    def check_limits(self, query):
        warnings = []
        for limit in self.known_limits:
            if limit["condition"](query):
                warnings.append(limit["description"])
        return warnings

    def respond_with_uncertainty(self, query, prediction, confidence):
        warnings = self.check_limits(query)
        msg = f"預測結果：{prediction}（信心度：{confidence:.0%}）"
        if confidence < 0.6:
            msg += "\n⚠️ 信心度偏低，建議人工確認"
        for w in warnings:
            msg += f"\n⚠️ 限制說明：{w}"
        return msg

communicator = UncertaintyCommunicator()
communicator.add_limit(
    lambda q: len(q) > 100,
    "輸入長度超過 100 字元，部分模型可能無法完整處理",
)
communicator.add_limit(
    lambda q: "預測" in q and "數值" not in q,
    "定性預測的準確度可能低於定量預測",
)
query = "這個產品在未來市場的表現如何（這是一個很長的查詢...）" * 5
print(communicator.respond_with_uncertainty(query, "正向", 0.45))
```

---

**延伸閱讀**

- [AI Transparency Design](https://www.google.com/search?q=AI+transparency+design+guidelines)
- [Explainable AI Techniques](https://www.google.com/search?q=explainable+AI+techniques+LIME+SHAP)
- [Uncertainty Communication in AI](https://www.google.com/search?q=uncertainty+communication+AI+systems)
