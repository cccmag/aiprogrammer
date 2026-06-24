# Kafka 分散式訊息佇列

## 前言

Apache Kafka 是用於構建即時資料管道和串流應用的分散式事件串流平台。它最初由 LinkedIn 開發，現已成為 Apache 軟體基金會的頂級專案。

## Kafka 核心概念

```
Kafka 架構：
────────────────────────────────

Producer ──▶ Topic ──▶ Partition ──▶ Consumer
                  │
                  └── 分區副本（多副本）

關鍵特性：
- 持久化：訊息寫入磁片，持久保留
- 可擴展：透過分割區平行處理
- 高吞吐：每秒處理百萬級訊息
```

## 主題與分區

```python
from kafka import KafkaProducer, KafkaConsumer

# 生產者
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for i in range(10):
    producer.send('my-topic', key=f'key-{i}'.encode(), value=f'value-{i}'.encode())

producer.flush()
producer.close()

# 消費者
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['localhost:9092'],
    group_id='my-consumer-group',
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"key={message.key.decode()}, value={message.value.decode()}")
```

## 訊息持久化

```
Kafka 日誌結構：
────────────────────────────────

Topic: my-topic
  Partition: 0
    ├── Offset 0: Message(key, value, timestamp)
    ├── Offset 1: Message(key, value, timestamp)
    └── Offset 2: Message(key, value, timestamp)
  Partition: 1
    ├── Offset 0: Message(key, value, timestamp)
    └── ...

特點：
- 訊息依 offset 順序存取
- Offset 由 Kafka 管理
- 可回放任何 offset 的訊息
```

## 延伸閱讀

- [Kafka 官方網站](https://www.google.com/search?q=Apache+Kafka+official)
- [Kafka Streams 文件](https://www.google.com/search?q=Kafka+Streams+documentation)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*