# AI 問責機制

## 模型註冊、審計軌跡、人機協作決策（2023-2029）

### 問責的關鍵要素

AI 問責不只是事後追責——它需要貫穿模型生命週期的完整機制：**註冊**（註冊 AI 系統）、**審計**（記錄決策過程）、**補救**（建立申訴管道）。

### 模型註冊與資產管理

```python
import json
from datetime import datetime

class AiModelRegistry:
    def __init__(self):
        self.models = {}

    def register(self, model_id: str, metadata: dict) -> str:
        entry = {
            "model_id": model_id,
            "registered_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "versions": [],
            "incidents": [],
        }
        self.models[model_id] = entry
        return model_id

    def log_inference(self, model_id: str, input_hash: str, output: str):
        entry = self.models.get(model_id)
        if not entry:
            raise ValueError("Model not registered")
        entry["versions"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "input_hash": input_hash,
            "output": output,
        })

    def report_incident(self, model_id: str, description: str, severity: str):
        entry = self.models.get(model_id)
        entry["incidents"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "description": description,
            "severity": severity,  # low / medium / high / critical
        })

    def audit_trail(self, model_id: str) -> dict:
        return self.models.get(model_id, {})
```

### 決策審計軌跡

每個 AI 決策都應能被完整回顧：

```python
from dataclasses import dataclass, field, asdict

@dataclass
class AiDecision:
    decision_id: str
    model_id: str
    version: str
    timestamp: str
    inputs: dict
    output: dict
    confidence: float
    human_reviewed: bool = False
    human_decision: str | None = None

class DecisionLogger:
    def __init__(self):
        self.decisions: list[AiDecision] = []

    def log(self, decision: AiDecision):
        self.decisions.append(decision)

    def export(self, path: str):
        with open(path, "w") as f:
            json.dump([asdict(d) for d in self.decisions], f, indent=2)

    def query(self, model_id: str = None, start: str = None, end: str = None):
        results = self.decisions
        if model_id:
            results = [d for d in results if d.model_id == model_id]
        if start:
            results = [d for d in results if d.timestamp >= start]
        if end:
            results = [d for d in results if d.timestamp <= end]
        return results
```

### 人機協作決策（Human-in-the-loop）

高風險場景不允許完全自動化決策：

```python
class HumanInTheLoop:
    def __init__(self, confidence_threshold: float = 0.9):
        self.confidence_threshold = confidence_threshold
        self.pending_reviews = []

    def decide(self, decision: AiDecision) -> dict:
        if decision.confidence >= self.confidence_threshold:
            return {
                "action": "auto_approve",
                "decision": decision.output,
                "reason": f"Confidence {decision.confidence:.2f} >= {self.confidence_threshold}",
            }
        self.pending_reviews.append(decision)
        return {
            "action": "require_review",
            "decision_id": decision.decision_id,
            "reason": f"Low confidence: {decision.confidence:.2f}",
        }

    def review_count(self) -> int:
        return len(self.pending_reviews)
```

### 問責機制比較

| 國家/地區 | 機制 | 強制性 |
|-----------|------|--------|
| 歐盟 | AI Act 高風險註冊 | ✅ 強制 |
| 美國 | AI 行政命令自願報告 | ⚠️ 自願 |
| 中國 | 演算法備案制度 | ✅ 強制 |
| 日本 | AI 準則（軟法） | 無 |

2024 年歐盟 AI Office 啟動了「高風險 AI 系統資料庫」，所有高風險系統必須註冊才能上市——這是全球第一個具強制力的 AI 問責基礎設施。

---

**下一步**：[全球 AI 監管比較](focus6.md)

## 延伸閱讀

- [EU AI Office](https://www.google.com/search?q=EU+AI+Office+high+risk+register)
- [AI Accountability Framework](https://www.google.com/search?q=AI+accountability+framework+audit)
- [Human in the Loop AI](https://www.google.com/search?q=human+in+the+loop+AI+decision+making)
