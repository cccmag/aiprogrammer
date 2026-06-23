# 人機協作案例研究

## 前言

實際案例最能反映人機協作介面設計的成功關鍵。本文分析三個不同領域的案例，探討設計決策如何影響協作成效。

## 案例一：程式碼審查助手

```python
class CodeReviewAssistant:
    def __init__(self):
        self.rules = {
            "naming": r"[a-z_]+",
            "docstring": r'""".*?"""',
            "type_hint": r":\s*\w+",
        }

    def review(self, code):
        issues = []
        checks = {
            "naming": ("變數命名應採蛇形", self.check_naming),
            "docstring": ("缺少文件字串", self.check_docstring),
            "type_hint": ("缺少型別提示", self.check_type_hint),
        }
        for name, (msg, func) in checks.items():
            if not func(code):
                issues.append(msg)
        return self.generate_report(issues)

    def check_naming(self, code):
        import re
        return bool(re.search(r"def [a-z_]+", code))

    def check_docstring(self, code):
        import re
        return bool(re.search(r'""".*?"""', code, re.DOTALL))

    def check_type_hint(self, code):
        import re
        return bool(re.search(r":\s*\w+", code))

    def generate_report(self, issues):
        if not issues:
            return {"decision": "approve", "message": "✅ 程式碼品質良好"}
        return {"decision": "review", "issues": issues}

# 人機協作流程
class HumanAICollaboration:
    def __init__(self):
        self.ai = CodeReviewAssistant()
        self.history = []

    def process(self, code):
        ai_result = self.ai.review(code)
        self.history.append(("ai", ai_result))
        if ai_result["decision"] == "approve":
            return "自動核准"
        # 人工複審
        human_decision = input(f"AI 發現問題：{ai_result['issues']}\n您的決定：")
        self.history.append(("human", human_decision))
        return f"人工決定：{human_decision}"

reviewer = CodeReviewAssistant()
print(reviewer.review("def add(a, b): return a + b"))
```

## 案例二：醫療診斷輔助系統

```python
class MedicalDiagnosisAssistant:
    def __init__(self):
        self.symptom_db = {
            "發燒": ["感冒", "流感", "COVID-19"],
            "咳嗽": ["感冒", "流感", "支氣管炎"],
            "頭痛": ["偏頭痛", "緊縮性頭痛", "感冒"],
            "胸痛": ["肌肉拉傷", "心臟問題", "焦慮"],
        }
        self.urgency_levels = {
            "胸痛": "high",
            "呼吸困難": "high",
            "頭痛": "medium",
            "咳嗽": "low",
        }

    def analyze(self, symptoms):
        possible = set()
        for s in symptoms:
            if s in self.symptom_db:
                possible.update(self.symptom_db[s])
        return self.prioritize(symptoms, possible)

    def prioritize(self, symptoms, possible):
        urgencies = [self.urgency_levels.get(s, "low") for s in symptoms]
        max_urgency = "low"
        if "high" in urgencies:
            max_urgency = "high"
        elif "medium" in urgencies:
            max_urgency = "medium"
        return {
            "possible_conditions": list(possible),
            "urgency": max_urgency,
            "recommendation": {
                "high": "立即就醫",
                "medium": "建議就醫檢查",
                "low": "觀察症狀變化",
            }[max_urgency],
            "disclaimer": "本系統僅供參考，不構成醫療建議",
        }

assistant = MedicalDiagnosisAssistant()
print(assistant.analyze(["胸痛", "咳嗽"]))
```

## 案例三：設計協作工具

```python
class DesignCollaboration:
    def __init__(self):
        self.canvas = {"shapes": [], "metadata": {}}
        self.suggestions = []

    def add_shape(self, shape_type, x, y, color="blue"):
        shape = {"type": shape_type, "x": x, "y": y, "color": color}
        self.canvas["shapes"].append(shape)
        return shape

    def ai_suggest_layout(self):
        # AI 分析佈局並提出建議
        shapes = self.canvas["shapes"]
        if len(shapes) < 3:
            return "請加入更多元素以獲得佈局建議"
        suggestions = []
        for i, s in enumerate(shapes[:-1]):
            next_s = shapes[i + 1]
            if abs(s["x"] - next_s["x"]) < 20:
                suggestions.append(f"元素 {i} 和 {i + 1} 水平對齊不理想")
        return suggestions

    def human_apply_feedback(self, feedback):
        # 人類決定是否採納 AI 建議
        if "對齊" in feedback:
            for i, shape in enumerate(self.canvas["shapes"]):
                shape["x"] = (i % 3) * 100
            return "已重新對齊元素"
        return "未採納建議"

tool = DesignCollaboration()
tool.add_shape("rect", 10, 20)
tool.add_shape("circle", 30, 40)
tool.add_shape("rect", 50, 60)
print(tool.ai_suggest_layout())
print(tool.human_apply_feedback("將元素對齊"))
```

## 案例啟示

三個案例的共同成功要素：**明確分工**、**透明決策**、**人類最終決定權**。AI 提供分析和建議，人類做出最終判斷，形成互補協作。

---

**延伸閱讀**

- [Human-AI Collaboration Case Studies](https://www.google.com/search?q=human+AI+collaboration+case+studies+2026)
- [AI-Assisted Code Review Tools](https://www.google.com/search?q=AI+assisted+code+review+tools)
- [Clinical Decision Support Systems](https://www.google.com/search?q=clinical+decision+support+AI+systems)
