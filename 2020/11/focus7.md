# Lambda 架構與 Kappa：即時與批量處理的統一

## 大資料處理架構的演進

### 從批次到即時

```
大資料處理演進：
────────────────────────────────

早期：純批次處理
  └── Hadoop/MapReduce
  └── T+1 或 T+N 延遲

中期：Lambda 架構
  └── 批次 + 即時 雙通道
  └── 平衡延遲和準確性

現代：Kappa 架構
  └── 統一流處理
  └── 簡化架構
```

## Lambda 架構

### 核心概念

Lambda 架構提出用兩種方式處理大資料：

```
Lambda 架構：
────────────────────────────────

           輸入資料
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────┐     ┌──────────┐
│  Master  │     │  Serving │
│  Dataset │     │   Layer  │
│  (批次)  │     │  (查詢)  │
└────┬─────┘     └────┬─────┘
     │                 ▲
     ▼                 │
┌──────────┐     ┌──────────┐
│  Batch   │     │  Batch   │
│   Layer  │     │   View   │
└────┬─────┘     └────┬─────┘
     │                 ▲
     │                 │
┌────┴─────┐     ┌────┴─────┐
│  Speed   │     │  Serving │
│  Layer   │────▶│   Layer  │
│ (即時)   │     │          │
└──────────┘     └──────────┘
     │
     ▼
┌──────────┐
│  Speed   │
│   View   │
└──────────┘
```

### 為什麼需要 Lambda？

```python
"""
Lambda 架構的問題和解決方案：

問題：
- 批次處理延遲高（數小時）
- 即時處理精度低

解決方案：
- 批次層：保證高精確度，但延遲高
- 速度層：提供低延遲近似結果
- 服務層：合併兩個視圖的結果
"""

# 查詢時合併結果
def query(lambda_system, query):
    # 從批次視圖讀取精確結果
    batch_result = lambda_system.serving_layer.get(query)
    
    # 從速度視圖讀取即時結果
    speed_result = lambda_system.speed_view.get(query)
    
    # 合併：批次結果為主，速度結果填補空白
    if batch_result.complete and speed_result.recent:
        return merge_results(batch_result, speed_result)
```

### Lambda 的缺點

```
Lambda 的問題：
────────────────────────────────

1. 雙重實現
   └── 同一個查詢需要實現兩次
   └── 批次視圖和速度視圖邏輯可能不同

2. 維護成本高
   └── 兩套系統需要獨立維護

3. 一致性問題
   └── 兩個視圖可能返回不一致的結果

4. 延遲仍然存在
   └── 批次層仍然有數小時延遲
```

## Kappa 架構

### 核心思想

Kappa 架構由 Jay Kreps 提出，主張用統一的流處理替代 Lambda：

```
Kappa 架構：
────────────────────────────────

           輸入資料
               │
               ▼
      ┌─────────────────┐
      │   Kafka 或     │
      │   其他佇列     │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │  Stream        │
      │  Processing    │
      │  (統一處理)    │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │  Serving       │
      │  Layer         │
      └─────────────────┘
```

### 將批次視為流的一個特例

```python
# Kappa 的核心思想
"""
Kappa 認為：如果能夠重放 Kafka 的訊息，
那麼批次處理只是流處理的一個特例

歷史資料處理：
- 從 Kafka 起始位置開始重放
- 使用同樣的流處理邏輯
- 避免了雙重實現
"""

# 使用 Kafka 重放歷史資料
class KappaProcessor:
    def __init__(self, kafka_consumer):
        self.consumer = kafka_consumer
    
    def reprocess_from_beginning(self):
        # 重置到最開始的位置
        self.consumer.seek_to_beginning()
        
        # 重新處理所有訊息
        for message in self.consumer:
            self.process(message)
    
    def reprocess_from_timestamp(self, timestamp):
        # 或者從特定時間點重放
        self.consumer.seek(timestamp)
        
        for message in self.consumer:
            self.process(message)
```

## Apache Kafka

### Kafka 的核心概念

```
Kafka 架構：
────────────────────────────────

Producer ──▶ Topic ──▶ Partition ──▶ Consumer
                  │
                  └── 多副本复制

特點：
- 持久化：訊息寫入磁片
- 可重放：Offset 可以重置
- 擴展性：分區並行處理
```

### Kafka Streams 示例

```python
# Kafka Streams 實作 Word Count

from kafka import KafkaProducer, KafkaConsumer
from collections import defaultdict

# 設定 consumer 從頭重放
consumer = KafkaConsumer(
    'input-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

# 單次處理
counts = defaultdict(int)

for message in consumer:
    text = message.value.decode('utf-8')
    for word in text.split():
        counts[word] += 1
    
    # 可選：定期輸出結果
    if message.offset % 1000 == 0:
        print(dict(counts))
    
    consumer.commit()
```

## Apache Flink

### Flink 的流處理能力

Flink 是一個強大的流處理框架，支援精確一次語意：

```python
# Flink Word Count

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import FlatMapFunction
from pyflink.common.typeinfo import Types

env = StreamExecutionEnvironment.get_execution_environment()

# 從 Kafka 讀取
env.add_source(KafkaSource(...)) \
   .flat_map(Tokenizer()) \
   .key_by(lambda x: x[0], key_type=Types.STRING) \
   .sum(1) \
   .print()

env.execute()

class Tokenizer(FlatMapFunction):
    def flat_map(self, value, collector):
        for word in value.split():
            collector.collect((word, 1))
```

## 架構選擇

### Lambda vs Kappa

```
何時使用 Lambda：
────────────────────────────────

- 現有系統已經複雜
- 需要非常精確的批次結果
- 團隊有足夠資源維護雙系統
- 有嚴格的數據質量要求

何時使用 Kappa：
────────────────────────────────

- 追求簡單架構
- 即時性要求高
- 資料變化頻率高
- 希望統一維護
```

## 延伸閱讀

- [Lambda 架構](https://www.google.com/search?q=lambda+architecture+big+data)
- [Kappa 架構](https://www.google.com/search?q=kappa+architecture+streaming)
- [Kafka Streams](https://www.google.com/search?q=Kafka+Streams+example)
- [Apache Flink 文件](https://www.google.com/search?q=Apache+Flink+documentation)
- [流處理框架比較](https://www.google.com/search?q=streaming+framework+comparison+flink+spark)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*