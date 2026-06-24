# WiFi 模組 ESP8266 應用

## ESP8266 概述

ESP8266 是一款內建 WiFi 功能的低成本微控制器：

- 價格：約 $2-5
- WiFi：802.11 b/g/n
- 時脈：80MHz
- GPIO：16 腳
- 快閃記憶體：4MB（典型）

## AT 指令模式

最基本的 ESP8266 使用方式：

```cpp
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("AT");
  delay(1000);

  Serial.println("AT+CWMODE=1");  // Station 模式
  delay(1000);

  Serial.println("AT+CWJAP=\"SSID\",\"PASSWORD\"");
  delay(5000);
}
```

## Web 伺服器

```cpp
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "text/html",
    "<html><body><h1>ESP8266 Web Server</h1></body></html>");
}

void setup() {
  WiFi.begin("SSID", "PASSWORD");
  server.on("/", handleRoot);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

## MQTT 連線

```cpp
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  client.setServer("broker.mqtt-dashboard.com", 1883);
  client.setCallback(callback);

  WiFi.begin("SSID", "PASSWORD");
}

void loop() {
  if (!client.connected()) {
    client.connect("ESP8266");
    client.subscribe("home/sensor");
  }
  client.loop();
}
```

## 功耗模式

| 模式 | 功耗 | 喚醒方式 |
|------|------|----------|
| 正常 | 70mA | - |
| 淺睡眠 | 15mA | 定時 |
| 深度睡眠 | 0.9mA | RESET |
| 關閉 | 0.1uA | 重新供電 |

## OTA 更新

```cpp
#include <ArduinoOTA.h>

void setup() {
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();
}
```

## ESP8266 vs ESP32

| 特性 | ESP8266 | ESP32 |
|------|---------|-------|
| 價格 | $2-5 | $6-10 |
| 核心 | 1 | 2 |
| WiFi | b/g/n | b/g/n |
| 藍牙 | 無 | 4.2 |
| GPIO | 16 | 34 |

## 小結

ESP8266 是物聯網開發的最佳選擇之一，價格實惠、功能完整、文檔豐富。從簡單的 WiFi 連線到複雜的 MQTT 應用，ESP8266 都能勝任。

---

## 延伸閱讀

- [ESP8266 Official Forum](https://www.google.com/search?q=ESP8266+official+forum)
- [ESP8266 Arduino Core](https://www.google.com/search?q=ESP8266+arduino+core+github)