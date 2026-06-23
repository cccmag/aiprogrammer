# MLflow 模型監控實戰

## 前言

MLflow 是目前最受歡迎的開源 ML 生命週期管理平台之一。除了實驗追蹤與模型註冊之外，MLflow 2.0 之後強化了模型監控（Model Monitoring）能力，讓資料科學團隊可以在模型上線後持續掌握其健康狀態。本文將示範如何使用 MLflow 的監控功能來追蹤模型表現、偵測資料漂移，並設定自動化警報。

---

## 一、MLflow 模型監控架構

MLflow 的監控系統以 **Model Registry** 為核心，搭配 **MLflow Tracing** 與 **MLflow Evaluations** 兩個子系統：

- **Model Registry**：管理模型版本、階段（Staging/Production/Archived）與轉移歷程
- **MLflow Tracing**：自動擷取每次推論請求的輸入、輸出、延遲與中繼資料
- **MLflow Evaluations**：定期對生產流量進行評估，計算準確率、精確率、召回率等指標

### 1.1 啟用 Tracing

```python
import mlflow
from mlflow.tracing import enable

mlflow.set_tracking_uri("http://localhost:5000")
enable()

@mlflow.trace(span_type="predict")
def predict(model_input: dict) -> dict:
    response = model_client.predict(model_input)
    return response
```

每次 `predict` 被呼叫時，MLflow 會自動記錄輸入 Schema、輸出值、執行時間與異常資訊。

---

## 二、即時指標收集

MLflow 提供 `mlflow.log_metrics` 的延伸 API，專門用於生產環境的即時指標：

```python
from mlflow.monitoring import log_performance_metric

def monitor_prediction(y_true, y_pred, threshold=0.8):
    accuracy = (y_true == y_pred).mean()
    log_performance_metric("production_accuracy", accuracy)
    if accuracy < threshold:
        mlflow.log_param("alert", "accuracy_drop")
```

這些指標會被寫入 MLflow Tracking Server 的 `metrics` 表中，可以透過 UI 或 API 查詢。

---

## 三、資料漂移檢測

MLflow 內建了基於統計檢定的漂移檢測模組：

```python
from mlflow.evaluation.drift import compute_drift
import pandas as pd

reference = pd.read_parquet("training_data.parquet")
production = pd.read_parquet("production_batch.parquet")

drift_report = compute_drift(
    reference=reference,
    production=production,
    columns=["age", "income", "credit_score"],
    method="psi"  # Population Stability Index
)
print(drift_report)
```

支援的方法包括 PSI、KS 檢定、KL 散度與 JS 散度。

---

## 四、儀表板與警報整合

MLflow 的監控 UI 提供可自訂的儀表板，並可與 PagerDuty、Slack 等工具整合：

```python
from mlflow.monitoring import create_alert

create_alert(
    metric="production_accuracy",
    condition="< 0.75",
    duration_minutes=10,
    notification_channels=["slack://#alerts", "pagerduty://default"]
)
```

當 production_accuracy 連續 10 分鐘低於 0.75 時，系統會自動發送警報。

---

## 五、生產部署建議

| 考量項目 | 建議 |
|---------|------|
| 取樣率 | 100% 記錄前 7 天，之後降為 10% |
| 儲存後端 | PostgreSQL + S3（artifacts） |
| 保留政策 | 原始日誌保留 30 天，聚合指標保留 1 年 |
| 警報靜默 | 同一警報 24 小時內不重複發送 |

---

## 結語

MLflow 的監控功能讓模型上線不再是黑箱。透過 Tracing、即時指標與漂移檢測，團隊可在問題惡化前介入處理。

---

## 參考資料

- https://www.google.com/search?q=MLflow+model+monitoring+production
- https://www.google.com/search?q=MLflow+tracing+observability
