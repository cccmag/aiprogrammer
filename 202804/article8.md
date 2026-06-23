# 資料治理與合規

## 前言

隨著 GDPR、CCPA 和各國 AI 監管法規陸續生效，資料治理已從選項變為義務。對於 AI 資料工程團隊而言，資料治理涵蓋資料血緣、存取控制、隱私保護和稽核日誌等面向。

## 資料血緣追蹤

資料血緣（Data Lineage）記錄資料從源頭到最終使用的完整路徑：

```python
""" 使用 OpenLineage 追蹤資料血緣 """
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client.event import Dataset
from datetime import datetime

client = OpenLineageClient(url="http://localhost:5000")

def track_pipeline(pipeline_name: str, input_datasets: list, output_dataset: str):
    run_id = "run-" + datetime.now().isoformat()

    event = RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=datetime.now().isoformat(),
        run=Run(runId=run_id),
        job=Job(namespace="data_engineering", name=pipeline_name),
        inputs=[
            Dataset(namespace="s3", name=ds) for ds in input_datasets
        ],
        outputs=[
            Dataset(namespace="s3", name=output_dataset)
        ],
    )
    client.emit(event)
    print(f"血緣事件已發送: {pipeline_name}")

track_pipeline(
    "user_features_etl",
    input_datasets=["raw/users", "raw/orders"],
    output_dataset="features/user_features",
)
```

## PII 偵測與脫敏

自動識別個人身份資訊（PII）並進行脫敏處理：

```python
import re
import hashlib

class PIIDetector:
    patterns = {
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+",
        "phone": r"0\d{1,3}-\d{6,8}",
        "credit_card": r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}",
        "id_number": r"[A-Z]\d{9}",
    }

    @classmethod
    def detect(cls, text: str) -> list:
        found = []
        for pii_type, pattern in cls.patterns.items():
            matches = re.findall(pattern, text)
            for m in matches:
                found.append({"type": pii_type, "value": m})
        return found

    @classmethod
    def anonymize(cls, text: str) -> str:
        for pii_type, pattern in cls.patterns.items():
            text = re.sub(pattern, lambda m: hashlib.sha256(m.group().encode()).hexdigest()[:12], text)
        return text

text = "用戶 email 是 alice@example.com，手機 0912-345-678"
print(f"偵測到 PII: {PIIDetector.detect(text)}")
print(f"脫敏後: {PIIDetector.anonymize(text)}")
```

## 存取控制與稽核

實作最低權限原則和完整的稽核日誌：

```python
import logging
from enum import Enum
from datetime import datetime

class DataRole(Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    SCIENTIST = "scientist"
    ANALYST = "analyst"
    AUDITOR = "auditor"

class DataAccessControl:
    def __init__(self):
        self.audit_log = []
        self.permissions = {
            DataRole.ADMIN: {"raw", "clean", "features", "models"},
            DataRole.ENGINEER: {"raw", "clean", "features"},
            DataRole.SCIENTIST: {"clean", "features"},
            DataRole.ANALYST: {"features"},
            DataRole.AUDITOR: set(),  # 唯讀存取
        }

    def check_access(self, user: str, role: DataRole, dataset: str) -> bool:
        allowed = dataset in self.permissions[role]
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "role": role.value,
            "dataset": dataset,
            "allowed": allowed,
        })
        return allowed

    def get_audit_trail(self, user: str = None) -> list:
        if user:
            return [e for e in self.audit_log if e["user"] == user]
        return self.audit_log

access = DataAccessControl()
print(access.check_access("alice", DataRole.SCIENTIST, "raw"))  # False
print(access.check_access("bob", DataRole.ENGINEER, "raw"))     # True
```

## 結語

資料治理不是阻礙創新的枷鎖，而是確保 AI 系統可信賴的基礎。自動化血緣追蹤、PII 偵測和存取控制，讓團隊在合規的前提下快速迭代。

---

**延伸閱讀**

- [OpenLineage 資料血緣](https://www.google.com/search?q=OpenLineage+data+lineage)
- [GDPR 資料保護規範](https://www.google.com/search?q=GDPR+data+protection+AI)
- [資料治理框架指南](https://www.google.com/search?q=data+governance+framework+best+practices)
