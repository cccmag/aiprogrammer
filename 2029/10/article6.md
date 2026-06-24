# 演算法問責機制：建立可追溯的 AI 決策鏈

## 前言

當 AI 系統做出錯誤決策時，誰該負責？演算法問責（Algorithmic Accountability）要求組織能夠追溯、解釋和挑戰 AI 系統的每一項決策。本文探討如何建立完整的問責機制。

## 決策記錄系統

```python
import json
from datetime import datetime, timezone

class DecisionRecorder:
    def __init__(self):
        self.log: list = []

    def record(self, decision_id: str, model_version: str,
               input_data: dict, prediction, confidence: float,
               human_reviewer: str = None):
        entry = {
            "decision_id": decision_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_version": model_version,
            "input_hash": hash(json.dumps(input_data, sort_keys=True)),
            "prediction": prediction,
            "confidence": confidence,
            "human_reviewer": human_reviewer,
            "status": "auto" if not human_reviewer else "reviewed"
        }
        self.log.append(entry)
        return entry

    def get_decision(self, decision_id: str):
        for entry in self.log:
            if entry["decision_id"] == decision_id:
                return entry
        return None

    def get_decisions_by_version(self, model_version: str):
        return [e for e in self.log if e["model_version"] == model_version]

    def export_audit_trail(self, path: str):
        with open(path, "w") as f:
            json.dump(self.log, f, indent=2)

recorder = DecisionRecorder()
recorder.record("DEC-001", "cv-v3.2", {"age": 35, "income": 80000}, "核准", 0.91)
recorder.record("DEC-002", "cv-v3.2", {"age": 22, "income": 30000}, "拒絕", 0.78, "reviewer@bank.com")
print(json.dumps(recorder.get_decision("DEC-001"), indent=2))
```

## 自動化爭議處理流程

```python
class DisputeHandler:
    def __init__(self, recorder: DecisionRecorder):
        self.recorder = recorder

    def request_review(self, decision_id: str, reason: str):
        entry = self.recorder.get_decision(decision_id)
        if not entry:
            return {"error": "找不到該決策紀錄"}
        return {
            "decision_id": decision_id,
            "original_prediction": entry["prediction"],
            "reason": reason,
            "review_status": "pending",
            "assigned_reviewer": None,
            "escalation_path": ["基層審查", "主管審查", "倫理委員會"]
        }

handler = DisputeHandler(recorder)
print(handler.request_review("DEC-001", "收入資料有誤"))
```

## 結語

演算法問責不是阻礙創新的絆腳石。完善的問責機制反而能增加使用者信任、降低法律風險，是負責任 AI 的基石。

---

**延伸閱讀**

- [Algorithmic Accountability Act 草案](https://www.google.com/search?q=Algorithmic+Accountability+Act+US+2023)
- [可解釋 AI 方法](https://www.google.com/search?q=explainable+AI+XAI+methods+Python)
- [AI 稽核框架](https://www.google.com/search?q=AI+audit+frameworks+accountability+best+practices)
