# 物聯網通訊協定比較

## 前言

物聯網（IoT）有多種通訊協定，每種適用於不同的場景。

---

## 主要協定比較

| 協定 | 傳輸方式 | 耗電 | 頻寬 | 適用場景 |
|------|----------|------|------|----------|
| MQTT | TCP | 低 | 低 | 遠端監控 |
| CoAP | UDP | 極低 | 極低 | 感測器網路 |
| HTTP | TCP | 中 | 中 | Web 整合 |
| WebSocket | TCP | 中 | 中 | 即時應用 |
| AMQP | TCP | 中 | 中 | 企業訊息 |
| XMPP | TCP | 中 | 低 | 聊天應用 |

---

## MQTT (Message Queuing Telemetry Transport)

### 特點

- 輕量級發布/訂閱模式
- 設計用於受限裝置
- QoS 等級支援

### 運作模式

```
發布者 ──> Broker ──> 訂閱者
          (中介)
```

### 使用範例

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("連線成功")
    client.subscribe("sensors/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.example.com", 1883)
client.loop_forever()
```

### QoS 等級

| 等級 | 說明 |
|------|------|
| QoS 0 | 最多傳送一次 |
| QoS 1 | 至少傳送一次 |
| QoS 2 | 恰好傳送一次 |

---

## CoAP (Constrained Application Protocol)

### 特點

- 專為受限裝置設計
- 類似 HTTP 的 REST 模型
- 支援觀察模式

### 使用範例

```python
from coapthon.client.helperclient import HelperClient

client = HelperClient(server=("localhost", 5683))

# GET 請求
response = client.get("sensor/temperature")
print(response.payload)

# PUT 請求
client.put("actuator/led", "on")
```

### 與 HTTP 的比較

| 特性 | CoAP | HTTP |
|------|------|------|
| 傳輸 | UDP | TCP |
| 標頭大小 | 4 bytes | 數十 bytes |
| 方法 | GET,POST,PUT,DELETE | GET,POST,PUT,DELETE |
| 安全性 | DTLS | TLS |

---

## XMPP (Extensible Messaging and Presence Protocol)

### 特點

- 基於 XML
- 即時通訊起源
- 點對點架構

### 使用範例

```python
import sleekxmpp

class IoTBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("message", self.message)
    
    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            print(msg["body"])

xmpp = IoTBot("device@example.com", "password")
xmpp.connect()
xmpp.process()
```

---

## 選擇指南

### 遠端監控

```python
# MQTT 是最好的選擇
# 低頻寬、低功耗、社群支援豐富
```

### 受限感測器

```python
# CoAP 最合適
# 極低資源消耗、UDP 傳輸
```

### Web 整合

```python
# HTTP/REST 仍是主流
# 易於與現有系統整合
```

### 即時應用

```python
# WebSocket 適合
# 雙向通訊、低延遲
```

---

## 安全性

### MQTT 安全

```python
# 認證
client.username_pw_set("username", "password")
client.tls_set()

# ACL
# 設定主題存取權限
```

### CoAP 安全 (DTLS)

```python
# 使用 DTLS
from coapthon.layers.dtlssocket import DTLSSocket
```

---

## 閘道器設計

```
感測器網路 ──> IoT 閘道器 ──> 雲端服務
   (Zigbee)    │
   (BLE)       │ (MQTT/HTTP)
   (Z-Wave)    │
               ▼
         本地處理/儲存
```

### Raspberry Pi 閘道器

```python
# 讀取 BLE 感測器
from bluepy import btle

# 轉發到 MQTT
import paho.mqtt.client as mqtt

def forward_to_mqtt(data):
    client.publish("sensors/data", data)
```

[搜尋 IoT protocol comparison](https://www.google.com/search?q=IoT+protocol+comparison+MQTT+CoAP)

---

## 小結

選擇正確的 IoT 通訊協定取決於具體的應用場景、裝置能力和網路環境。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [MQTT 官方網站](https://www.google.com/search?q=MQTT+official)
- [CoAP 規格](https://www.google.com/search?q=CoAP+specification)