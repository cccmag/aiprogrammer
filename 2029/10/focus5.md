# AI 問責機制

## 從模型稽核到法律歸責（2023-2029）

### 前言

當 AI 系統犯錯時，誰來負責？是開發者？部署者？還是 AI 本身？2023 年之後，各國立法與技術標準開始回答這個問題。AI 問責不再只是倫理討論，而是具體的工程與法規要求。

### 模型稽核管線

制度化的 AI 稽核是問責的技術基礎：

```python
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class AuditLogEntry:
    """AI 稽核日誌的標準格式"""
    timestamp: datetime
    model_version: str
    input_hash: str
    prediction: float
    confidence: float
    explanation: dict
    decision_outcome: str
    reviewer_id: str = ""

class AuditTrail:
    """不可篡改的稽核軌跡"""
    
    def __init__(self):
        self.entries: list = []
        self._chain_hash = "0"  # 區塊鏈式哈希鏈
    
    def log(self, entry: AuditLogEntry) -> str:
        """記錄一次 AI 決策，返回區塊哈希"""
        entry_dict = {
            'timestamp': entry.timestamp.isoformat(),
            'model_version': entry.model_version,
            'input_hash': entry.input_hash,
            'prediction': entry.prediction,
            'confidence': entry.confidence,
            'explanation': entry.explanation,
            'decision_outcome': entry.decision_outcome,
            'prev_hash': self._chain_hash,
        }
        
        # 簡化哈希計算（實際使用 SHA-256）
        import hashlib
        content = json.dumps(entry_dict, sort_keys=True)
        current_hash = hashlib.sha256(
            (content + self._chain_hash).encode()
        ).hexdigest()
        
        entry_dict['hash'] = current_hash
        self._chain_hash = current_hash
        self.entries.append(entry_dict)
        return current_hash
    
    def verify_chain(self) -> bool:
        """驗證稽核鏈的完整性"""
        prev_hash = "0"
        for entry in self.entries:
            stored_hash = entry.pop('hash', None)
            content = json.dumps(entry, sort_keys=True)
            expected = hashlib.sha256(
                (content + prev_hash).encode()
            ).hexdigest()
            if stored_hash != expected:
                return False
            prev_hash = stored_hash
            entry['hash'] = stored_hash
        return True

# 使用範例
audit = AuditTrail()
entry = AuditLogEntry(
    timestamp=datetime.now(),
    model_version="v2.1.0",
    input_hash="abc123",
    prediction=0.87,
    confidence=0.92,
    explanation={"income": 0.45, "history": 0.32},
    decision_outcome="APPROVED",
)
hash_val = audit.log(entry)
print(f"Entry hash: {hash_val}")
print(f"Chain intact: {audit.verify_chain()}")
```

### 問責層級模型

不同問責層級對應不同程度的控制權：

```python
from enum import Enum

class AccountabilityLevel(Enum):
    """AI 問責的六個層級"""
    LEVEL_0 = "無問責"           # 純自動，無人工審查
    LEVEL_1 = "日誌追蹤"          # 僅記錄決策
    LEVEL_2 = "可解釋"            # 能解釋為什麼
    LEVEL_3 = "人工覆審"          # 關鍵決策需人工確認
    LEVEL_4 = "可逆轉"            # 決策可以被撤銷
    LEVEL_5 = "完全問責"          # 端到端可追溯+可修正

class AISystemGovernance:
    """AI 系統治理框架"""
    
    def __init__(self, level: AccountabilityLevel):
        self.level = level
        self.audit_trail = AuditTrail()
        self.override_log = []
    
    def decide(self, input_data: dict) -> dict:
        """執行 AI 決策並根據問責層級處理"""
        # 1. 模型預測
        prediction = self._model_predict(input_data)
        
        # 2. 根據層級決定是否需要人工審查
        if self.level.value >= AccountabilityLevel.LEVEL_3.value:
            if self._requires_review(prediction):
                decision = self._human_review(input_data, prediction)
            else:
                decision = prediction
        else:
            decision = prediction
        
        # 3. 記錄稽核軌跡
        self._log_decision(input_data, prediction, decision)
        
        return {
            'decision': decision,
            'level': self.level.name,
            'audit_hash': self.audit_trail._chain_hash,
        }
    
    def _model_predict(self, data: dict) -> dict:
        return {'score': 0.85, 'approved': True}
    
    def _requires_review(self, prediction: dict) -> bool:
        return prediction.get('score', 0) < 0.6
    
    def _human_review(self, data: dict, prediction: dict) -> dict:
        return {'score': 0.0, 'approved': False, 'reviewed': True}
    
    def _log_decision(self, input_data, prediction, decision):
        entry = AuditLogEntry(
            timestamp=datetime.now(),
            model_version="v2.1.0",
            input_hash=hash(json.dumps(input_data, sort_keys=True)),
            prediction=prediction['score'],
            confidence=0.92,
            explanation={},
            decision_outcome="APPROVED" if decision['approved'] else "REJECTED",
        )
        self.audit_trail.log(entry)
```

### 法律問責框架比較

不同司法管轄區的 AI 問責制度：

```python
@dataclass
class JurisdictionFramework:
    """司法管轄區的 AI 問責框架"""
    region: str
    regulation: str
    liability_model: str  # 嚴格責任 / 過失責任 / 產品責任
    human_oversight_required: bool
    penalty_for_violation: str

frameworks = [
    JurisdictionFramework(
        region="歐盟",
        regulation="AI Act (2024)",
        liability_model="嚴格責任（高風險系統）",
        human_oversight_required=True,
        penalty_for_violation="全球年營收 7%",
    ),
    JurisdictionFramework(
        region="美國",
        regulation="AI Bill of Rights (2023)",
        liability_model="混合（行業別差異大）",
        human_oversight_required=False,
        penalty_for_violation="依具體法規",
    ),
    JurisdictionFramework(
        region="中國",
        regulation="生成式 AI 管理辦法 (2023)",
        liability_model="平台責任",
        human_oversight_required=True,
        penalty_for_violation="情節嚴重者吊銷許可",
    ),
    JurisdictionFramework(
        region="日本",
        regulation="AI 治理指南 (2024)",
        liability_model="軟性法（guideline）",
        human_oversight_required=False,
        penalty_for_violation="無直接罰則",
    ),
]

for fw in frameworks:
    print(f"{fw.region}: {fw.regulation} -> {fw.liability_model}")
```

### 技術與法規演進

| 年份 | 事件 |
|------|------|
| 2023 | 歐盟 AI Act 草案、生成式 AI 責任討論 |
| 2024 | AI Act 正式通過、美國 AI 行政命令 |
| 2025 | 各國強制 AI 稽核上路 |
| 2026 | ISO 42001 AI 管理系統驗證 |
| 2027 | AI 責任保險產品出現 |
| 2029 | 跨國 AI 問責互認框架 |

### 小結

AI 問責從「誰該負責」的哲學問題，演化為具體的技術架構（稽核軌跡）+ 法規架構（AI Act）的雙層系統。對於開發者，建立不可篡改的決策日誌，是避免法律風險的第一步。

---

**下一步**：[全球 AI 監管比較](focus6.md)

## 延伸閱讀

- [EU AI Act](https://www.google.com/search?q=EU+AI+Act+2024)
- [US AI Bill of Rights](https://www.google.com/search?q=AI+Bill+of+Rights+White+House)
- [ISO/IEC 42001](https://www.google.com/search?q=ISO+42001+AI+management)
