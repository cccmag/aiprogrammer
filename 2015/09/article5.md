# 從 Socket 到 ZeroMQ

## 前言

隨著分散式系統的複雜性增加，訊息佇列成為連接元件的重要工具。

---

## 傳統 Socket 的限制

### 複雜性

```python
# TCP 客戶端-伺服器需要手動處理
# 連線管理、錯誤處理、訊息格式定義
# 負載平衡、高可用性都要自己實作
```

### 連線管理

- 需要處理斷線重連
- 需要處理網路分割
- 需要實作確認機制

### 負載平衡

- 需要自己實作
- 很難支援多消費者

---

## 訊息佇列的價值

### 解耦

```
 Producer ──────> 訊息佇列 ──────> Consumer 1
                             ├─> Consumer 2
                             └─> Consumer 3
```

### 特性

- **非同步**：發送者和接收者不需要同時線上
- **緩衝**：吸收流量高峰
- **負載分散**：多個消費者分擔工作
- **可靠性**：訊息持久化

---

## ZeroMQ

### 簡介

ZeroMQ 是一個輕量級的訊息傳遞庫，不是完整的訊息佇列系統。

### 通訊模式

#### 請求-回應 (Request-Reply)

```python
import zmq

# 伺服器
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"收到: {message}")
    socket.send(b"World")

# 客戶端
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send(b"Hello")
message = socket.recv()
print(f"收到: {message}")
```

#### 發布-訂閱 (Publish-Subscribe)

```python
# 發布者
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

while True:
    message = f"更新: {i}"
    pub_socket.send_string(message)

# 訂閱者
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:5556")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "更新:")
```

#### 管道 (Pipeline)

```python
# Ventilator（任務產生者）
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

for i in range(10):
    sender.send_string(f"Task {i}")

# Worker（任務處理者）
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

while True:
    task = receiver.recv_string()
    # 處理任務
    sink.send_string(f"Done: {task}")
```

---

## RabbitMQ

真正的訊息佇列系統。

### 核心概念

- **Exchange**：路由訊息
- **Queue**：儲存訊息
- **Binding**：Exchange 和 Queue 的關聯

### 安裝

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

### 使用範例

```python
import pika

# 連線
connection = pika.BlockingConnection()
channel = connection.channel()

# 宣告佇列
channel.queue_declare(queue='hello')

# 發送
channel.basic_publish(exchange='', routing_key='hello', body='Hello!')

# 接收
def callback(ch, method, properties, body):
    print(f"收到: {body}")

channel.basic_consume(queue='hello', on_message_callback=callback)
channel.start_consuming()
```

---

## Redis Pub/Sub

Redis 內建的發布-訂閱功能。

### 使用範例

```python
import redis

r = redis.Redis()

# 發布者
r.publish('channel', 'message')

# 訂閱者
pubsub = r.pubsub()
pubsub.subscribe('channel')

for message in pubsub.listen():
    print(message)
```

---

## 選擇指南

| 工具 | 適用場景 |
|------|----------|
| Raw Socket | 簡單的點對點通訊 |
| ZeroMQ | 輕量級、嵌入式 |
| RabbitMQ | 企業級、複雜路由 |
| Redis Pub/Sub | 簡單的發布-訂閱 |
| Kafka | 大規模串流處理 |

[搜尋 message queue comparison](https://www.google.com/search?q=message+queue+comparison+2015)

---

## 小結

從 Socket 到訊息佇列代表了不同程度的抽象，選擇合適的工具能大幅簡化分散式系統的開發。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [ZeroMQ 官方網站](https://www.google.com/search?q=ZeroMQ+official)
- [RabbitMQ 官方網站](https://www.google.com/search?q=RabbitMQ+official)