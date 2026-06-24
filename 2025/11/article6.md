# RabbitMQ 入門

## 訊息佇列的核心概念與 Python 實作

## RabbitMQ 是什麼？

RabbitMQ 是最受歡迎的開源訊息佇列之一，使用 Erlang 語言編寫，支援多種訊息協議（AMQP、MQTT、STOMP）。它實現了生產者-消費者模式，讓服務之間可以非同步通訊。

### 核心概念

```
Producer（生產者）
  │
  ▼
Exchange（交換器）— 決定訊息路由
  │
  ▼
Queue（佇列）— 儲存訊息
  │
  ▼
Consumer（消費者）— 處理訊息
```

---

## 安裝與設定

```bash
# macOS
brew install rabbitmq
brew services start rabbitmq

# Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management

# 管理介面：http://localhost:15672 (guest/guest)
```

---

## Python 實作

### 安裝依賴

```bash
pip install pika
```

### 簡單的生產者-消費者

**生產者（send.py）**

```python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

# 宣告佇列（如果不存在則建立）
channel.queue_declare(queue="hello")

channel.basic_publish(
    exchange="",
    routing_key="hello",
    body="Hello, RabbitMQ!"
)
print("Sent: Hello, RabbitMQ!")

connection.close()
```

**消費者（receive.py）**

```python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

channel.queue_declare(queue="hello")

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

channel.basic_consume(
    queue="hello",
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for messages...")
channel.start_consuming()
```

---

## 交換器類型

RabbitMQ 的核心是交換器（Exchange），它決定訊息如何路由到佇列。

### Direct Exchange

根據 Routing Key 精確匹配。

```
Producer → [Direct Exchange] → Queue (routing_key = "info")
                               → Queue (routing_key = "error")
```

```python
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

# 生產者
channel.basic_publish(
    exchange="direct_logs",
    routing_key="error",
    body="Something went wrong"
)

# 消費者
channel.queue_bind(
    exchange="direct_logs",
    queue="error_queue",
    routing_key="error"
)
```

### Fanout Exchange

廣播到所有綁定的佇列。

```
Producer → [Fanout Exchange] → Queue A
                              → Queue B
                              → Queue C
```

```python
channel.exchange_declare(exchange="broadcast", exchange_type="fanout")

# 所有綁定的佇列都會收到訊息
channel.basic_publish(
    exchange="broadcast",
    routing_key="",
    body="Important announcement"
)
```

### Topic Exchange

根據 Routing Key 模式匹配。

```
* 表示一個單詞
# 表示零個或多個單詞

routing_key = "user.created"
匹配模式 "user.*"    → 命中
匹配模式 "user.#"    → 命中
匹配模式 "*.created" → 命中
```

```python
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

# 生產者
channel.basic_publish(
    exchange="topic_logs",
    routing_key="user.created",
    body='{"user_id": 1}'
)

# 消費者：接收所有 user 相關事件
channel.queue_bind(
    exchange="topic_logs",
    queue="user_events",
    routing_key="user.#"
)
```

---

## 工作佇列（Work Queue）

多個消費者共享同一個佇列，輪詢處理訊息。

```python
import time

def callback(ch, method, properties, body):
    print(f"Worker received: {body.decode()}")
    time.sleep(body.count(b"."))  # 模擬處理時間
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)  # 一次只處理一個
channel.basic_consume(queue="task_queue", on_message_callback=callback)
channel.start_consuming()
```

`basic_qos(prefetch_count=1)` 確保 RabbitMQ 不會同時分發多個訊息給一個消費者——這實現了公平排程。

---

## 訊息確認與持久化

### 手動確認

```python
def callback(ch, method, properties, body):
    try:
        process(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```

### 持久化

```python
# 佇列持久化
channel.queue_declare(queue="durable_queue", durable=True)

# 訊息持久化
channel.basic_publish(
    exchange="",
    routing_key="durable_queue",
    body="Important message",
    properties=pika.BasicProperties(
        delivery_mode=2,  # 持久化訊息
    )
)
```

---

## 實際案例：訂單處理系統

```python
class OrderService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare("orders", "topic")

    def create_order(self, user_id, items):
        order = {"user_id": user_id, "items": items, "status": "created"}
        self.channel.basic_publish(
            exchange="orders",
            routing_key="order.created",
            body=json.dumps(order)
        )
        return order

class InventoryService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare("orders", "topic")
        result = self.channel.queue_declare("", exclusive=True)
        self.channel.queue_bind(result.method.queue, "orders", "order.created")
        self.channel.basic_consume(
            queue=result.method.queue,
            on_message_callback=self.handle_order
        )

    def handle_order(self, ch, method, properties, body):
        order = json.loads(body)
        print(f"Deducting inventory for order {order['user_id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
```

---

## 監控與管理

```bash
# RabbitMQ 管理 CLI
rabbitmqctl list_queues
rabbitmqctl list_exchanges
rabbitmqctl list_bindings

# 管理介面：http://localhost:15672
# 查看佇列深度、訊息速率、連線數
```

---

## 延伸閱讀

- [RabbitMQ Official Tutorials](https://www.google.com/search?q=RabbitMQ+official+tutorials+Python)
- [AMQP Protocol](https://www.google.com/search?q=AMQP+protocol+rabbitmq)
- [RabbitMQ vs Kafka](https://www.google.com/search?q=RabbitMQ+vs+Kafka+message+queue+comparison)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之六。*
