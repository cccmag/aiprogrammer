# Kafka/Flink 串流處理實戰

## 為什麼需要串流處理

即時 AI 系統的核心挑戰是「資料不等人」。批次處理的延遲通常在分鐘級，而即時推論要求在毫秒到秒級完成。Apache Kafka 作為分散式訊息佇列，搭配 Apache Flink 的串流處理引擎，成為業界標準的即時資料管道方案。

## Kafka 基本架構

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# 生產者：發送即時事件
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 發送使用者點擊事件
producer.send('user-events', {
    'user_id': 'u123',
    'event': 'click',
    'timestamp': 1709000000,
    'page': '/product/42'
})
producer.flush()
```

Kafka 的 Topic 分割（partition）機制讓串流可以水平擴展。每個分割區內的訊息順序保證，讓 Exactly-Once 語意成為可能。

## Flink 串流處理

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types

env = StreamExecutionEnvironment.get_execution_environment()

# 從 Kafka 讀取串流
ds = env.add_source(
    KafkaSource.builder()
    .set_bootstrap_servers('localhost:9092')
    .set_topics('user-events')
    .set_group_id('ai-group')
    .set_starting_offsets(KafkaOffsetsInitializer.latest())
    .build()
)

# 特徵提取轉換
def extract_features(event):
    return {
        'user_id': event['user_id'],
        'page_category': event['page'].split('/')[1],
        'hour_of_day': event['timestamp'] % 86400 // 3600
    }

features_stream = ds.map(extract_features)
features_stream.sink_to(create_kafka_sink('features'))
env.execute('realtime-feature-pipeline')
```

## 時間語意與水位線

Flink 支援事件時間（Event Time）而非單純的處理時間：

```python
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.time import Time

# 每 10 秒的滑動視窗統計
windowed = features_stream \
    .key_by(lambda f: f['page_category']) \
    .window(TumblingEventTimeWindows.of(Time.seconds(10))) \
    .aggregate(CountAggregate())
```

水位線（Watermark）機制解決亂序到達的問題，在即時系統中至關重要。

## 狀態儲存與容錯

Flink 的 Checkpoint 機制讓串流處理具備 Exactly-Once 語意：

```python
env.enable_checkpointing(5000)  # 每 5 秒
env.get_checkpoint_config() \
   .set_checkpoint_storage_dir('file:///tmp/flink-cp')
```

狀態後端可以選擇 RocksDB（百 GB 級別）或 Heap（高效能）。

## 延伸閱讀

- [Apache Kafka 官方文件](https://www.google.com/search?q=Apache+Kafka+documentation)
- [Flink 串流處理教學](https://www.google.com/search?q=Flink+stream+processing+tutorial)
- [Kafka Streams vs Flink 比較](https://www.google.com/search?q=Kafka+Streams+vs+Flink+comparison)
- [PyFlink 入門](https://www.google.com/search?q=PyFlink+getting+started)
