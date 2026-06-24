# 物聯網架構與通訊協定

## 前言

物聯網系統的核心挑戰之一是讓各種不同的裝置能夠可靠地交換資料。選擇合適的通訊協定對於系統的效能、功耗和可靠性至關重要。

## 物聯網系統架構

### 常見架構模式

#### 三層架構

```
┌─────────────────┐
│   應用層        │  資料展示、使用者介面
├─────────────────┤
│   網路層        │  資料傳輸、路由
├─────────────────┤
│   感知層        │  感測器、致動器
└─────────────────┘
```

#### 四層架構

```
┌─────────────────┐
│   應用服務層     │  業務邏輯、資料處理
├─────────────────┤
│   平台層        │  資料儲存、分析
├─────────────────┤
│   網路傳輸層     │  閘道器、路由器
├─────────────────┤
│   終端裝置層     │  感測器、致動器
└─────────────────┘
```

### 霧運算 vs 雲端運算

| 特性 | 雲端運算 | 霧運算 |
|------|---------|--------|
| 位置 | 遠端資料中心 | 網路邊緣 |
| 延遲 | 高 | 低 |
| 頻寬 | 需要網路 | 減少傳輸 |
| 處理 | 集中 | 分散 |
| 範例 | AWS IoT | EdgeX Foundry |

## 通訊協定分類

### 依網路層分類

#### 網際網路協定

- **TCP/IP**：可靠的連接導向傳輸
- **UDP**：快速的無連接傳輸
- **HTTP/WebSocket**：網頁應用

#### 物聯網特定協定

- **MQTT**：輕量級發布/訂閱
- **CoAP**：針對受限裝置最佳化
- **AMQP**：企業級訊息

### 依傳輸層分類

| 協定 | 傳輸層 | 特點 |
|------|--------|------|
| MQTT | TCP | 輕量、發布/訂閱 |
| CoAP | UDP | 似 HTTP、適合受限裝置 |
| HTTP | TCP | 通用、相容性高 |
| WebSocket | TCP | 雙向即時 |

## MQTT 協定

MQTT（Message Queue Telemetry Transport）是最流行的物聯網通訊協定之一。

### 特點

- **輕量級**：最小的協定開銷（僅 2 位元組 header）
- **發布/訂閱**：鬆耦合的訊息傳遞
- **QoS 等級**：三種服務品質等級
- **最後遺囑**：連線中斷通知

### MQTT 架構

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Publisher │ ────> │  Broker  │ ────> │ Subscriber │
│  (Publisher) │     │  (Broker) │     │ (Subscriber) │
└──────────┘     └──────────┘     └──────────┘
```

### MQTT 主題（Topic）

```
home/livingroom/temperature
home/bedroom/temperature
home/+/temperature        # + 萬用字元
```

### Arduino MQTT 範例

```cpp
#include <PubSubClient.h>
#include <ESP8266WiFi.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* mqtt_server = "broker.mqtt-dashboard.com";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void callback(char* topic, byte* payload, unsigned int length) {
  // 處理接收到的訊息
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("arduinoClient")) {
      client.subscribe("home/sensor");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
```

### Python (Paho MQTT) 範例

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("home/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqtt-dashboard.com", 1883, 60)
client.loop_forever()
```

## CoAP 協定

CoAP（Constrained Application Protocol）專為資源受限的裝置設計。

### 特點

- 似 HTTP 的 REST 模型
- 支援觀察（Observe）模式
- 基於 UDP
- 支援服務發現

### 與 HTTP 的比較

| 特性 | HTTP | CoAP |
|------|------|------|
| 傳輸 | TCP | UDP |
| 開銷 | 高 | 低 |
| 模型 | 請求/回應 | 請求/回應 + 觀察 |
| 快取 | 可 | 不可 |

### CoAP 範例

```python
# aiocoap 範例
import asyncio
from aiocoap import *

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://[device]/temperature')
    response = await protocol.request(request).response

    print(response.payload)

asyncio.run(main())
```

## HTTP 協定

HTTP 是傳統的 Web 通訊協定，在物聯網中仍廣泛使用。

### RESTful API

```cpp
// Arduino HTTP POST 範例
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

void sendData(float temperature) {
  WiFiClient client;
  HTTPClient http;

  http.begin(client, "http://your-server.com/api/temperature");
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"temperature\":" + String(temperature) + "}";
  int httpCode = http.POST(payload);

  if (httpCode > 0) {
    String response = http.getString();
  }

  http.end();
}
```

## 傳輸層比較

| 特性 | WiFi | Bluetooth LE | LoRa | ZigBee |
|------|------|-------------|------|--------|
| 功耗 | 高 | 中 | 低 | 低 |
| 距離 | 100m | 10m | 10km+ | 100m |
| 頻寬 | 高 | 中 | 低 | 低 |
| 成本 | 中 | 低 | 中 | 低 |

## 雲端平台整合

### AWS IoT

```python
import boto3

# AWS IoT Core
iot = boto3.client('iot-data')

iot.publish(
    topic='home/sensor',
    qos=1,
    payload='{"temperature": 25}'
)
```

### Google Cloud IoT

```python
from google.cloud import iot_v1

# Google Cloud IoT Core
client = iot_v1.SubscriberClient()
```

### Azure IoT Hub

```python
from azure.iot.hub import IoTHubRegistryManager

# Azure IoT Hub
registry_manager = IoTHubRegistryManager("connection-string")
```

## 通訊協定選擇指南

| 場景 | 推薦協定 |
|------|---------|
| 低功耗感測器 | MQTT-SN, CoAP |
| 即時監控 | WebSocket, MQTT |
| 大量裝置 | MQTT, AMQP |
| 受限裝置 | CoAP |
| 標準 Web 整合 | HTTP, MQTT |

## 小結

物聯網通訊協定的選擇取決於多種因素：

1. **裝置能力**：記憶體、處理器、功耗
2. **網路條件**：頻寬、延遲、可靠性
3. **應用需求**：即時性、資料量
4. **系統架構**：集中式 vs 分散式
5. **生態系統**：既有系統的相容性

理解這些通訊協定是設計可靠物聯網系統的基礎。

---

**下一步**：[馬達控制與致動器](focus5.md)

## 延伸閱讀

- [MQTT Protocol Guide](https://www.google.com/search?q=MQTT+protocol+tutorial)
- [CoAP Protocol Guide](https://www.google.com/search?q=CoAP+protocol+tutorial)
- [IoT Communication Protocols](https://www.google.com/search?q=IoT+communication+protocols+comparison)