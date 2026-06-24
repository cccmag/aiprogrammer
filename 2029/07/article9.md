# 事件回應計劃

## 概述

AI 安全事件回應計劃（Incident Response Plan）是組織在遭受 AI 安全攻擊時的標準作業程序。完善的計劃能大幅降低損害。

## 事件分級

```python
from enum import Enum
from datetime import datetime

class IncidentSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Incident:
    def __init__(self, description, severity, model_id):
        self.id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.description = description
        self.severity = severity
        self.model_id = model_id
        self.timestamp = datetime.now()
        self.status = "detected"
```

## 自動化偵測與告警

```python
def detect_anomaly(predictions, threshold=0.95):
    entropy = -np.sum(predictions * np.log(predictions + 1e-10), axis=1)
    if np.mean(entropy) < threshold * np.log(10):
        return Incident("異常預測分布", IncidentSeverity.HIGH, "model_v1")
    return None
```

## 回應 SOP

```python
playbooks = {
    "data_poisoning": lambda i: print(f"處理資料中毒: {i.id}"),
    "model_extraction": lambda i: print(f"處理模型竊取: {i.id}"),
}

def respond(incident):
    isolate_model(incident.model_id)
    handler = playbooks.get(incident.root_cause,
                            lambda i: print(f"預設處理: {i.id}"))
    handler(incident)

def isolate_model(model_id):
    print(f"隔離模型 {model_id}，切換至備用模型")
    save_model_snapshot(model_id)
```

## 改進循環

```python
def post_mortem(incident, response_log):
    lessons = {
        "detection_delay": response_log["detect"] -
                           incident.timestamp,
        "response_time": response_log["resolve"] -
                         response_log["detect"],
        "root_cause": incident.root_cause,
    }
    recommendations = generate_improvements(lessons)
    update_playbook(incident.root_cause, recommendations)
    return recommendations
```

參考資料：https://www.google.com/search?q=AI+incident+response+plan+template+2026
