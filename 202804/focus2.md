# 資料管線架構與編排（2017-2028）

## 從 Cron 到 DAG

資料管線的核心問題很簡單：**一連串的資料處理步驟，如何自動化、可靠地執行？**

2017 年以前，大多數資料管線仰賴 Cron job 加上 Shell script。這種做法在步驟少時可行，但當管線擴張到數十個步驟，依賴關係錯綜複雜時，Cron 完全無法勝任。

```python
# Cron 時代的典型管線（2016）
# 每個步驟都是獨立 script，靠檔案傳遞
# 0 2 * * * /usr/bin/python3 extract.py
# 0 3 * * * /usr/bin/python3 transform.py
# 0 5 * * * /usr/bin/python3 load.py
```

Airflow 在 2015 年由 Airbnb 開源，2017 年成為 Apache 頂級專案，確立了「DAG 即管線」的業界標準。

## DAG 為核心的編排模型

```
        extract_users.py ──┐
                           ├─── join_datasets.py ──→ train_model.py
        extract_orders.py ─┘           │
                                       ↓
                               evaluate_model.py
```

每個節點是一個任務（Task），邊代表依賴關係。Airflow 的 DAG 定義就是 Python 程式碼：

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG("ml_pipeline", schedule="@daily") as dag:
    extract = PythonOperator(task_id="extract", python_callable=extract_fn)
    transform = PythonOperator(task_id="transform", python_callable=transform_fn)
    train = PythonOperator(task_id="train", python_callable=train_fn)

    extract >> transform >> train
```

## 現代管線編排工具

| 工具 | 年份 | 核心特點 | 部署方式 |
|------|------|---------|---------|
| Airflow | 2015 | 穩定成熟、社群龐大 | 自管 |
| Prefect | 2018 | Pythonic API、自動重試 | 雲端/自管 |
| Dagster | 2019 | Asset 為中心、型別感知 | 自管 |
| Kestra | 2021 | YAML 宣告式、事件驅動 | 自管 |

Prefect 2018 年以「Airflow 的現代替代」問世，最大的創新是引入了 **狀態引擎**——每個任務執行都有明確的狀態機，支援自動重試、快取、並行執行。

## Prefect 範例

```python
from prefect import task, flow

@task
def fetch_data(url: str) -> list:
    return [{"id": 1, "value": 100}]

@task
def transform(data: list) -> list:
    return [{"id": d["id"], "value": d["value"] * 2} for d in data]

@flow
def data_pipeline(url: str):
    raw = fetch_data(url)
    transformed = transform(raw)
    return transformed
```

## 即時管線的挑戰

2020 年後，即時資料管線需求暴增。Kafka + Flink 成為即時處理的黃金組合。2023 年 RisingWave 作為即時資料庫崛起，提供了 SQL-based 的串流處理。

```
批次管線：Airflow + Spark → 小時級延遲
即時管線：Kafka + Flink → 秒級延遲
Lambda 架構：同時支援批次 + 即時
Kappa 架構：純即時，捨棄批次管道
```

## 延伸閱讀

- [Apache Airflow](https://www.google.com/search?q=Apache+Airflow+workflow+management)
- [Prefect vs Airflow comparison](https://www.google.com/search?q=Prefect+vs+Airflow+data+pipeline)
- [Kappa Architecture](https://www.google.com/search?q=Kappa+architecture+stream+processing)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之二。*
