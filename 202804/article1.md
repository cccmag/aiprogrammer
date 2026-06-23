# Airflow 與 Prefect：資料管線編排雙雄

## 前言

資料管線是 AI 專案的命脈。從原始資料擷取、清洗、轉換到特徵工程，每一步都需要可靠的排程和監控。Apache Airflow 和 Prefect 是當前最主流的兩個開源管線編排框架，本文比較兩者的設計哲學與實戰應用。

## Airflow：業界標準

Airflow 以 DAG（有向無環圖）定義管線，每個節點是任務，邊代表依賴關係。

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    return [{"id": 1, "text": "hello"}, {"id": 2, "text": "world"}]

def transform(raw):
    return [{"id": r["id"], "tokens": r["text"].split()} for r in raw]

def load(processed):
    print(f"寫入 {len(processed)} 筆資料")

with DAG("etl_pipeline", start_date=datetime(2024, 1, 1), schedule="@daily"):
    raw_data = PythonOperator(task_id="extract", python_callable=extract)
    processed = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    raw_data >> processed >> load_task
```

Airflow 的排程器（Scheduler）會根據 DAG 定義自動觸發任務，支援 Cron 表達式與資料感知排程。

## Prefect：新一代選擇

Prefect 2.0 採用「宣告式」設計，使用 Python decorator 定義管線，內建重試、快取和狀態管理。

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def fetch_data(api_url: str) -> list:
    import requests
    return requests.get(api_url).json()

@task(retries=3, retry_delay_seconds=10)
def clean_data(raw: list) -> list:
    return [item for item in raw if item.get("status") == "active"]

@task
def compute_features(clean: list) -> dict:
    return {"count": len(clean), "avg": sum(d["value"] for d in clean) / len(clean)}

@flow(name="feature_pipeline")
def feature_pipeline(api_url: str):
    raw = fetch_data(api_url)
    clean = clean_data(raw)
    features = compute_features(clean)
    return features

result = feature_pipeline("https://api.example.com/data")
```

Prefect 的特色是「任務即函式」，開發者只需要專注於業務邏輯，執行引擎會自動處理並行、重試和錯誤通知。

## 關鍵差異

| 面向 | Airflow | Prefect |
|------|---------|---------|
| 定義方式 | DAG 類別 | Python Decorator |
| 排程器 | 獨立 Scheduler 進程 | Server + Agent |
| 重試機制 | 需自訂 | 內建重試策略 |
| 快取 | 無 | 輸入雜湊快取 |
| 即時監控 | 較弱 | 強大的 UI 儀表板 |

## 結語

選擇 Airflow 還是 Prefect 取決於團隊需求：Airflow 生態系成熟、社群龐大、適合大型組織；Prefect 上手快、開發體驗好、適合資料科學團隊快速迭代。建議新專案從 Prefect 開始，當規模擴大再考慮遷移。

---

**延伸閱讀**

- [Apache Airflow 官方文件](https://www.google.com/search?q=Apache+Airflow+documentation)
- [Prefect 2.0 入門指南](https://www.google.com/search?q=Prefect+2.0+tutorial)
- [資料管線編排框架比較](https://www.google.com/search?q=Airflow+vs+Prefect+comparison+2024)
