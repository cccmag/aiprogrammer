# 即時特徵工程

## 從離線特徵到串流特徵（2018-2028）

### 前言

特徵工程是機器學習的基礎，傳統的離線特徵計算無法滿足即時 AI 的需求。即時特徵工程的核心挑戰在於：**在資料到達的瞬間完成特徵計算**，同時保證時間窗口的準確性。

### 離線 vs. 即時特徵

```python
# 離線特徵（2018 年典型）
# 每天凌晨批次計算
features = spark.sql("""
    SELECT user_id,
           COUNT(*) AS daily_clicks,
           AVG(amount) AS avg_amount
    FROM transactions
    WHERE date = 'yesterday'
    GROUP BY user_id
""")
# 新鮮度：24 小時
```

```python
# 即時特徵（2025 年典型）
# 事件到達即計算
from flink import StreamTableEnvironment

t_env.execute_sql("""
    CREATE TABLE click_features AS
    SELECT user_id,
           COUNT(*) OVER (PARTITION BY user_id
                          ORDER BY ts
                          RANGE BETWEEN INTERVAL '1' HOUR PRECEDING
                          AND CURRENT ROW) AS hour_clicks,
           AVG(amount) OVER (PARTITION BY user_id
                             ORDER BY ts
                             RANGE BETWEEN INTERVAL '10' MINUTE PRECEDING
                             AND CURRENT ROW) AS avg_amount_10m
    FROM clicks
""")
# 新鮮度：毫秒級
```

### 即時特徵儲存（Feature Store）

2020 年起，特徵儲存成為即時特徵工程的核心基礎設施：

```
特徵儲存架構（2023）
┌───────────────────┐
│   線上特徵儲存      │
│  Redis / Aerospike │ ← 低延遲讀取（<1ms）
├───────────────────┤
│   離線特徵儲存      │
│  S3 / Iceberg      │ ← 批次訓練用
├───────────────────┤
│   串流特徵計算      │
│  Flink / Kafka SQL │ ← 即時特徵更新
└───────────────────┘
```

```python
# Feast Feature Store（開源特徵儲存）
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")
features = store.get_online_features(
    features=["user:click_count_1h",
              "user:avg_amount_10m"],
    entity_rows=[{"user_id": "user_123"}]
).to_dict()
```

### 時間窗口處理

即時特徵工程中最容易出錯的是時間窗口：

| 窗口類型 | 定義 | 延遲影響 |
|---------|------|---------|
| Tumbling | 固定時間間隔（每 5 分鐘） | 可能錯過邊界事件 |
| Sliding | 滑動視窗（每 10 秒更新） | 計算量大 |
| Session | 活動區間（30 分鐘無操作結束） | 需要狀態管理 |
| Count-based | 最後 N 筆事件 | 記憶體可控 |

### 特徵新鮮度管理（2023-2028）

```python
# 特徵新鮮度標籤
features = {
    "user_embedding": {        # 每天更新
        "value": embed,
        "freshness": "stale",
        "ttl": 86400
    },
    "session_features": {      # 即時更新
        "value": session_stats,
        "freshness": "fresh",
        "ttl": 300
    }
}
```

即時系統根據新鮮度標籤決定是否重新計算特徵。

### 最新發展（2026-2028）

- **特徵伺服**：專門為即時推論服務的特徵查詢 API
- **自動特徵回溯**：串流特徵自動對齊離線訓練資料的時間點
- **Embedding 即時服務**：使用 Milvus/Pinecone 進行即時向量檢索作為特徵

### 小結

即時特徵工程讓 ML 模型不再需要使用過時的資料做決策。從離線 Spark 到串流 Flink，從靜態 CSV 到即時特徵儲存——特徵工程正在從「批次流程」轉變為「串流基礎設施」。

---

**下一步**：[即時 AI 監控與營運](focus7.md)

## 延伸閱讀

- [即時特徵儲存實戰](https://www.google.com/search?q=real+time+feature+store+Feast+Tecton)
- [串流特徵工程最佳實踐](https://www.google.com/search?q=stream+feature+engineering+best+practices)
- [特徵新鮮度管理](https://www.google.com/search?q=feature+freshness+management+machine+learning)
