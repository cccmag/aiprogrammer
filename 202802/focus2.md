# 串流資料處理架構

## 從日誌收集到即時特徵（2016-2028）

### 前言

串流處理是即時 AI 的資料基礎。從 Kafka 的發布到 Flink 的崛起，串流引擎經歷了從「批次微批次」到「真正即時」的演進。

### 串流引擎的三個世代

**第一代：日誌收集（2016）**

```python
# Apache Kafka：分散式日誌
# Producer
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('clicks', b'user:123,event:click')
```

Kafka 最初只是日誌收集工具，但它的發布-訂閱模型和日誌儲存能力，使它成為串流架構的基礎設施。

**第二代：微批次處理（2017-2019）**

```python
# Spark Streaming（微批次，間隔 100ms-1s）
from pyspark.streaming import StreamingContext
ssc = StreamingContext(spark, 1)  # 1 秒批次
stream = ssc.socketTextStream("localhost", 9999)
stream.map(lambda x: x.split(",")).pprint()
ssc.start()
```

Spark Streaming 的微批次模式引入了**至少一次**語義，但無法做到真正的事件時間處理。

**第三代：真正即時串流（2020-2028）**

```python
# Flink SQL：真正的即時串流
# SELECT user_id, COUNT(*) AS click_cnt
# FROM clicks
# GROUP BY TUMBLE(ts, INTERVAL '5' SECOND), user_id
# WHERE event = 'click'
```

Flink 的事件時間處理、恰好一次語義和狀態管理，使它在即時 AI 場景中脫穎而出。

### 串流-批次統一架構（2022-2025）

2022 年起，串流處理出現了新的架構模式：

```
Kafka Streams     → 輕量級即時（延遲 <10ms）
Apache Flink      → 有狀態串流（延遲 <100ms）
RisingWave        → 串流資料庫（延遲 <1s）
Delta/Kafka 合流  → 流批一體
```

**Kappa 架構**取代了早期的 Lambda 架構——不再區分串流層和批次層，所有資料都透過串流管道處理。

### 即時 AI 的資料模式

```python
# 即時特徵管道（2025 年典型）
from confluent_kafka import Consumer, Producer

def feature_processor():
    consumer = Consumer({'bootstrap.servers': 'kafka:9092',
                         'group.id': 'feat-pipeline'})
    consumer.subscribe(['raw_events'])
    while True:
        msg = consumer.poll(1.0)
        if msg:
            features = extract_features(msg.value())
            # 寫入即時特徵儲存
            feature_store.set(msg.key(), features)
```

### 最新的發展（2026-2028）

- **串流資料庫**：RisingWave、Materialize 讓串流查詢像 Postgres 一樣簡單
- **串流 ML 框架**：ByteDance 的 CloudWeGo、Uber 的 Streaming ML
- **Unified Pipeline**：一個管道同時支援 training 和 serving

### 小結

串流處理架構從 2016 年的 Kafka 日誌收集，到 2028 年的流批一體資料平台——即時 AI 的資料基礎已經從「能不能處理串流資料」進化到「能不能以資料庫的體驗處理串流」。

---

**下一步**：[低延遲模型推論](focus3.md)

## 延伸閱讀

- [Apache Flink 官方文件](https://www.google.com/search?q=Apache+Flink+stream+processing)
- [Kafka Streams 實戰手冊](https://www.google.com/search?q=Kafka+Streams+tutorial+real+time+AI)
- [流批一體架構設計](https://www.google.com/search?q=stream+batch+unified+architecture+kappa)
