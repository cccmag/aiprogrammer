# AI 行為透明度

## 前言

當 AI 做出一個決策時，使用者有權利知道「為什麼」。**行為透明度**（Behavioral Transparency）要求系統能夠解釋自己的推理過程、顯示當前的內部狀態，並接受使用者的追問。

## 解釋引擎

### 決策追溯

透明度從可回溯的決策紀錄開始：

```python
import json
from datetime import datetime
from typing import List, Dict, Any

class DecisionRecord:
    def __init__(self, decision_id: str):
        self.decision_id = decision_id
        self.timestamp = datetime.now().isoformat()
        self.inputs = {}
        self.reasoning_steps = []
        self.final_output = None
        self.confidence = 0.0

    def add_reasoning(self, step: str, evidence: str):
        self.reasoning_steps.append({
            "step": step,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat(),
        })

    def explain(self) -> str:
        lines = [f"決策 ID：{self.decision_id}"]
        lines.append(f"時間：{self.timestamp}")
        lines.append("推理過程：")
        for i, rs in enumerate(self.reasoning_steps, 1):
            lines.append(f"  {i}. {rs['step']}（依據：{rs['evidence']}）")
        lines.append(f"結論：{self.final_output}（信心：{self.confidence:.2f}）")
        return "\n".join(lines)
```

## 可解釋性 API

### 查詢介面

讓使用者可以深入追問 AI 的決策細節：

```python
class ExplainableClassifier:
    def __init__(self):
        self.feature_names = ["長度", "關鍵字", "語意", "情緒"]
        self.weights = [0.3, 0.4, 0.2, 0.1]

    def classify(self, text: str) -> Dict[str, Any]:
        features = {
            "長度": len(text),
            "關鍵字": sum(1 for w in ["urgent", "重要", "錯誤"] if w in text),
            "語意": 0.85,
            "情緒": 0.7,
        }
        score = sum(
            features[name] * w
            for name, w in zip(self.feature_names, self.weights)
        )
        category = "高優先" if score > 0.5 else "普通"
        return {
            "category": category,
            "score": score,
            "features": features,
            "weights": dict(zip(self.feature_names, self.weights)),
        }

    def explain_feature(self, feature: str, value: float) -> str:
        explanations = {
            "長度": f"文字長度 {value}，較長的文字通常包含更多資訊",
            "關鍵字": f"包含 {int(value)} 個重要關鍵字",
            "語意": f"語意相似度 {value:.2f}",
            "情緒": f"情緒強度 {value:.2f}",
        }
        return explanations.get(feature, f"{feature} = {value}")

clf = ExplainableClassifier()
result = clf.classify("緊急：系統發生重大錯誤")
print(f"分類：{result['category']}")
for feat, val in result['features'].items():
    print(clf.explain_feature(feat, val))
```

## 狀態可視化

### 心智模型展示

將 AI 的內部狀態以可理解的方式呈現：

```python
class AIStateVisualizer:
    def __init__(self):
        self.state = {
            "processing": "idle",
            "queue_length": 0,
            "current_task": None,
            "error_count": 0,
        }

    def update_state(self, **kwargs):
        self.state.update(kwargs)

    def render_state(self) -> str:
        status = "🟢" if self.state["error_count"] == 0 else "🟡"
        lines = [
            f"狀態：{status}",
            f"處理器：{self.state['processing']}",
            f"佇列長度：{'█' * self.state['queue_length']}{self.state['queue_length']}",
        ]
        if self.state["current_task"]:
            lines.append(f"當前任務：{self.state['current_task']}")
        return "\n".join(lines)

viz = AIStateVisualizer()
viz.update_state(processing="analysing", queue_length=3, current_task="分類文件")
print(viz.render_state())
```

## 反事實解釋

### 「如果…會怎樣？」

幫助使用者理解 AI 決策的邊界條件：

```python
class CounterfactualExplainer:
    def explain(self, original_input: dict, decision: str) -> List[str]:
        counterfactuals = []
        for key, value in original_input.items():
            opposite = not value if isinstance(value, bool) else value * 0.5
            counterfactuals.append(
                f"如果 {key} 從 {value} 改為 {opposite}，決策可能不同"
            )
        return counterfactuals

    def minimal_change(self, original: dict, target: str, model: callable) -> dict:
        for key in original:
            modified = original.copy()
            modified[key] = not modified[key]
            if model(modified) == target:
                return {key: modified[key]}
        return None
```

## 透明度等級

### 分級揭露

不是所有情況下都需要完整解釋：

```python
class TransparencyLevelManager:
    def __init__(self):
        self.transparency_levels = {
            "basic": self._basic_explain,
            "detailed": self._detailed_explain,
            "full": self._full_explain,
        }

    def _basic_explain(self, decision: str) -> str:
        return f"決策結果：{decision}"

    def _detailed_explain(self, decision: str) -> str:
        return f"決策：{decision}\n主要因素：參數 A > 臨界值"

    def _full_explain(self, decision: str, trace: DecisionRecord) -> str:
        return trace.explain()

    def get_explanation(self, level: str, decision: str, trace: DecisionRecord = None) -> str:
        explainer = self.transparency_levels.get(level, self._basic_explain)
        if level == "full":
            return explainer(decision, trace)
        return explainer(decision)
```

## 結語

行為透明度不是為了讓使用者理解 AI 的每一個數學細節，而是為了建立**可問責性**。當使用者知道 AI 為什麼做出某個決定，並且可以挑戰或修正它時，人機協作才能真正平等。

---

**延伸閱讀**

- [可解釋 AI 方法論](https://www.google.com/search?q=explainable+AI+XAI+methods+2026)
- [反事實解釋技術](https://www.google.com/search?q=counterfactual+explanations+AI)
- [透明度分級框架](https://www.google.com/search?q=AI+transparency+levels+framework)
