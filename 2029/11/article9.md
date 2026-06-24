# Agent 經濟法規

## 前言

當 Agent 可以自主簽訂合約、執行交易、管理資產時，法律該如何應對？2026 年，全球監管機構開始關注 Agent 經濟的法律地位。本文探討 Agent 經濟面臨的法規議題。

## Agent 的法律人格

目前法律體系中，Agent 不具備法人資格。解決方案包括「電子代理人」條款與 DAO 法律架構：

```python
from dataclasses import dataclass, field
from enum import Enum

class LegalStatus(Enum):
    TOOL = 1       # Agent 為工具，責任歸屬使用者
    AGENT = 2      # Agent 有有限代理權
    ENTITY = 3     # Agent 為法律實體（DAO）

@dataclass
class AgentLegalProfile:
    agent_id: str
    operator: str        # 負責人 DID
    legal_status: LegalStatus = LegalStatus.TOOL
    jurisdiction: str = ""
    registered_at: str = ""
```

## 合規檢查

Agent 在執行交易前需要進行基本的合規檢查：

```python
class ComplianceChecker:
    def __init__(self):
        self.restricted_services: set[str] = set()
        self.aml_threshold: float = 10000.0
    def check_transaction(self, tx: dict) -> dict:
        issues = []
        if tx["service"] in self.restricted_services:
            issues.append("restricted_service")
        if tx["amount"] > self.aml_threshold:
            issues.append("aml_threshold_exceeded")
        if tx.get("jurisdiction") == "unknown":
            issues.append("unknown_jurisdiction")
        return {"approved": len(issues) == 0, "issues": issues, "tx_id": tx.get("id")}
    def audit_log(self, agent_id: str, action: str, details: dict):
        print(f"[AUDIT] {agent_id}: {action} | {json.dumps(details)}")
```

## 參考資料

- https://www.google.com/search?q=AI+agent+legal+status+regulation+2026
- https://www.google.com/search?q=DAO+legal+framework+autonomous+agent
- https://www.google.com/search?q=electronic+agent+law+contract+formation
