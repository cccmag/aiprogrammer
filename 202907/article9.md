# 事件回應計劃

## 前言

任何 AI 系統都無法保證 100% 的安全。當安全事件發生時——無論是模型遭攻擊、敏感資料外洩、還是系統產生有害輸出——一套完善的事件回應計劃（Incident Response Plan）是將損害降至最低的關鍵。

## 事件分級

根據影響範圍與嚴重程度，將 AI 安全事件分為四級：

```python
INCIDENT_LEVELS = {
    1: "輕微：單一用戶遭遇異常輸出，無資料外洩",
    2: "中等：少量敏感資訊暴露，影響範圍受控",
    3: "嚴重：模型被成功注入或萃取，大量用戶受影響",
    4: "災難性：訓練資料或模型權重被竊取，系統失控",
}

def classify_incident(description, impact_scope, data_exposed):
    if data_exposed == "weights" or impact_scope == "all":
        return 4
    if data_exposed == "training_data" or impact_scope == "many":
        return 3
    if data_exposed == "user_data" or impact_scope == "some":
        return 2
    return 1
```

## 回應流程

自動化回應腳本是加速應變的關鍵：

```python
def incident_response(incident):
    level = incident["level"]
    if level >= 3:
        isolate_model(incident["model_id"])
    rollback_to_checkpoint(incident["model_id"])
    enable_audit_logging()
    notify_stakeholders(level)
    if level >= 2:
        launch_forensic_analysis(incident)
```

## 事後復原

安全事件結束後，需執行完整的根因分析（RCA），更新威脅模型，並將學到的教訓回饋到安全開發流程。推薦的 IR 框架與範本可參考 [https://www.google.com/search?q=AI+incident+response+plan+2026](https://www.google.com/search?q=AI+incident+response+plan+2026)。
