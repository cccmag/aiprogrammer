# 模型版本與回滾

## 前言

模型版本管理是 AI 可觀測性的基礎。沒有清晰的版本紀錄，漂移檢測與回滾都無從談起。

---

## 一、版本標記策略

借鑑 SemVer：

```
MAJOR.MINOR.PATCH
- MAJOR：架構變更、資料格式不相容
- MINOR：新特徵、超參數調整
- PATCH：Bug 修復、重新訓練
```

中繼資料記錄：

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModelVersion:
    version: str
    model_type: str
    created_at: datetime = None
    training_data_range: tuple = None
    metrics: dict = None
    git_commit: str = None
    tags: list = None
```

---

## 二、版本儲存

### 2.1 檔案系統

```
models/fraud-detector/
├── 1.0.0/
│   ├── model.pkl
│   └── metadata.json
├── 1.1.0/
│   ├── model.pkl
│   └── preprocessor.pkl
└── 2.0.0/
    ├── model.onnx
    └── config.yaml
```

### 2.2 MLflow Model Registry

```python
import mlflow
client = mlflow.tracking.MlflowClient()

def promote_to_production(model_name, version):
    client.transition_model_version_stage(
        name=model_name, version=version,
        stage="Production", archive_existing_versions=True
    )
```

---

## 三、回滾機制

### 3.1 健康分數追蹤

```python
class VersionHealthTracker:
    def __init__(self):
        self.health_records = {}

    def record_health(self, version, accuracy, latency, drift):
        score = 0.5 * accuracy + 0.3 * (1 - min(latency / 1000, 1)) + 0.2 * (1 - min(drift, 1))
        self.health_records.setdefault(version, []).append(score)
        return score

    def get_best_version(self, versions):
        averages = {v: sum(s)/len(s) for v, s in self.health_records.items() if v in versions}
        return max(averages, key=averages.get)
```

### 3.2 安全檢查

```python
def safe_rollback_check(current, target):
    checks = [
        check_version_exists(target),
        check_version_healthy(target),
        check_schema_compatible(current, target),
    ]
    if not all(checks):
        raise RuntimeError("回滾檢查失敗")
```

---

## 四、版本保留政策

| 政策 | 說明 |
|------|------|
| 保留最近 N 版 | 生產保留最近 5 版 |
| 階段性清理 | Staging 保留 7 天 |
| 黃金版本 | 標記 Gold 永久保留 |
| 自動封存 | 超過 90 天未使用自動封存 |

---

## 結語

搭配健康分數追蹤與自動化檢查，可將回滾從緊急事件降級為常規操作。

---

## 參考資料

- https://www.google.com/search?q=MLflow+model+version+management
- https://www.google.com/search?q=model+rollback+strategy+production
- https://www.google.com/search?q=semantic+versioning+ML+models
