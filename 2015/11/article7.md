# MQTT 物聯網通訊協定

## MQTT 簡介

MQTT（Message Queue Telemetry Transport）是一種輕量級的發布/訂閱訊息傳遞協定：

- 由 IBM 開發
- 專為受限裝置設計
- 基於 TCP/IP
- 開放標準（OASIS）

## 架構

```
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Publisher│        │ Broker │        │ Subscriber│
└─────────┘         └─────────┘         └─────────┘
     │                    │                    │
     │────── publish ────>│                    │
     │                    │                    │
     │                    │<───── subscribe ───┤
```

## MQTT 主題

```
home/livingroom/temperature   # 精確主題
home/+/temperature           # + 匹配任意一層
home/#                       # # 匹配多層
```

## QoS 等級

| 等級 | 語義 | 保證 |
|------|------|------|
| 0 | 最多一次 | 可能遺失 |
| 1 | 至少一次 | 不會遺失 |
| 2 | 恰好一次 | 不會重複 |

## Arduino 範例

```cpp
#include <PubSubClient.h>

const char* mqtt_server = "broker.mqtt-dashboard.com";
const char* topic = "home/temperature";

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, int length) {
  // 處理訊息
}

void setup() {
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // 連線 WiFi...

  if (client.connect("arduino")) {
    client.subscribe(topic);
  }
}

void loop() {
  client.loop();

  // 發布訊息
  client.publish(topic, "25.5");
  delay(5000);
}
```

## Python 範例

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result {rc}")
    client.subscribe("home/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqtt-dashboard.com", 1883, 60)
client.loop_forever()
```

## Broker 選擇

| Broker | 開發者 | 特點 |
|--------|--------|------|
| Mosquitto | Eclipse | 輕量、开源 |
| HiveMQ | HiveMQ | 企業級 |
| AWS IoT | Amazon | 雲端整合 |
| Azure IoT Hub | Microsoft | 雲端整合 |

## 安全性

- **TLS/SSL**：加密傳輸
- **認證**：用戶名/密碼
- **ACL**：存取控制

## 小結

MQTT 是物聯網領域最重要的通訊協定之一，其輕量級和發布/訂閱模式非常適合資源受限的嵌入式裝置。

---

## 延伸閱讀

- [MQTT Official Site](https://www.google.com/search?q=MQTT+official+specification)
- [MQTT Tutorial](https://www.google.com/search?q=MQTT+tutorial+beginners)