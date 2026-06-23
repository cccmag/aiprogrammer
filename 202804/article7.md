# 即時特徵管線

## 前言

在廣告推薦、 fraud detection 等低延遲場景中，模型需要即時取得最新特徵。即時特徵管線結合串流處理引擎和特徵儲存，在毫秒級內完成特徵計算和服務。

## 整體架構

即時特徵管線的典型流程：Kafka → Flink/Spark Streaming → Feast Online Store → 推論服務。

```python
""" 使用 Kafka-Python 模擬串流資料生產 """
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode()
)

def generate_click_event():
    return {
        "user_id": random.randint(1, 10000),
        "item_id": random.randint(1, 5000),
        "timestamp": int(time.time()),
        "click_duration": random.uniform(0.5, 60.0),
        "device": random.choice(["mobile", "desktop", "tablet"]),
    }

# 模擬每秒 100 筆點擊事件
while True:
    events = [generate_click_event() for _ in range(100)]
    for event in events:
        producer.send("click_events", event)
    print(f"已發送 {len(events)} 筆事件")
    time.sleep(1)
```

## Flink 即時特徵計算

使用 PyFlink 進行串流特徵工程：

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common import Types
import json

env = StreamExecutionEnvironment.get_execution_environment()

# 定義特徵計算函數
def compute_features(events):
    """每分鐘滑動視窗聚合特徵"""
    window_stats = {}
    for e in events:
        uid = e["user_id"]
        if uid not in window_stats:
            window_stats[uid] = {"count": 0, "total_duration": 0.0}
        window_stats[uid]["count"] += 1
        window_stats[uid]["total_duration"] += e["click_duration"]

    return [
        {
            "user_id": uid,
            "click_count_1m": stats["count"],
            "avg_click_duration_1m": stats["total_duration"] / stats["count"],
            "device_count": len(set(e["device"] for e in events if e["user_id"] == uid)),
        }
        for uid, stats in window_stats.items()
    ]

# Kafka 來源
source = KafkaSource.builder() \
    .set_bootstrap_servers("localhost:9092") \
    .set_topics("click_events") \
    .build()

stream = env.from_source(source)
# 每分鐘觸發一次視窗計算
result = stream.map(compute_features)
result.print()

env.execute("realtime_feature_pipeline")
```

## 寫入 Feast 線上儲存

即時計算出的特徵需要立即寫入特徵儲存：

```python
from feast import FeatureStore
import redis

store = FeatureStore(repo_path="./feature_repo")

def write_online_features(features: list):
    """將即時特徵寫入 Redis 線上儲存"""
    feature_rows = []
    for f in features:
        feature_rows.append({
            "user_id": f["user_id"],
            "feature_vector": {
                "click_count_1m": f["click_count_1m"],
                "avg_click_duration_1m": f["avg_click_duration_1m"],
            }
        })

    store.write_to_online_store(
        feature_view_name="user_realtime_features",
        df=feature_rows,
    )
    print(f"已更新 {len(feature_rows)} 筆即時特徵")
```

## 結語

即時特徵管線讓 ML 模型從批次更新進化為即時反應。關鍵在於端到端的延遲控制——從事件產生到特徵就緒，整個流程必須在秒級內完成。Kafka + Flink + Redis 是目前最成熟的即時特徵技術棧。

---

**延伸閱讀**

- [Apache Kafka 即時串流](https://www.google.com/search?q=Apache+Kafka+stream+processing)
- [PyFlink 串流處理](https://www.google.com/search?q=PyFlink+stream+processing+tutorial)
- [即時特徵儲存設計](https://www.google.com/search?q=real+time+feature+store+design)
