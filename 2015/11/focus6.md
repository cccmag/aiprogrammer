# 嵌入式系統網路連接

## 前言

網路連接是物聯網裝置的核心功能。將感測器資料上傳到雲端，或從雲端接收指令，都需要網路通訊。本期將介紹嵌入式系統的網路連接技術。

## WiFi 模組

### ESP8266

ESP8266 是一款低成本、功能完整的 WiFi 微控制器：

| 規格 | 數值 |
|------|------|
| 處理器 | Tensilica Xtensa LX106 |
| 時脈 | 80 MHz |
| WiFi | 802.11 b/g/n |
| GPIO | 16 腳 |
| 價格 | 約 $2-5 |

### ESP8266 初始化

```cpp
#include <ESP8266WiFi.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void loop() {}
```

### ESP8266 作為 Web 伺服器

```cpp
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

void handleRoot() {
  server.send(200, "text/html", "<h1>ESP8266 Web Server</h1>");
}

void handleLED() {
  String state = server.arg("state");
  if (state == "on") {
    digitalWrite(LED_BUILTIN, LOW);
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  server.send(200, "text/plain", "LED " + state);
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  server.on("/", handleRoot);
  server.on("/led", handleLED);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

### ESP8266 HTTP 請求

```cpp
#include <ESP8266HTTPClient.h>

void sendData(float temperature) {
  HTTPClient http;
  http.begin("http://your-server.com/api/temperature");
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"temperature\":" + String(temperature) + "}";
  int httpCode = http.POST(payload);

  if (httpCode > 0) {
    String response = http.getString();
  }

  http.end();
}
```

## TCP/IP 程式設計

### ESP8266 TCP 用戶端

```cpp
#include <WiFiClient.h>

const char* host = "192.168.1.100";
const int port = 8080;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (!client.connect(host, port)) {
    delay(1000);
  }
}

void loop() {
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  if (Serial.available()) {
    char c = Serial.read();
    client.print(c);
  }
}
```

### ESP8266 TCP 伺服器

```cpp
#include <WiFiServer.h>

WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("New client");
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        client.write(c);  // 回顯
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}
```

## UDP 通訊

### ESP8266 UDP

```cpp
#include <WiFiUDP.h>

WiFiUDP udp;
const int udpPort = 1234;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  udp.begin(udpPort);
}

void loop() {
  // 發送封包
  udp.beginPacket("192.168.1.255", udpPort);
  udp.print("Hello from ESP8266");
  udp.endPacket();

  delay(1000);

  // 接收封包
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char packetBuffer[255];
    int len = udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.println(packetBuffer);
  }
}
```

## 安全傳輸

### HTTPS

```cpp
#include <WiFiClientSecure.h>

const char* host = "api.example.com";
const int httpsPort = 443;

WiFiClientSecure client;

void setup() {
  client.setInsecure();  // 僅用於測試，生產環境應使用憑證
}

void sendSecureData() {
  if (!client.connect(host, httpsPort)) {
    return;
  }

  String url = "/api/data";
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: ESP8266\r\n" +
               "Connection: close\r\n\r\n");

  while (client.available()) {
    String line = client.readStringUntil('\n');
  }
}
```

### SSL 憑證

```cpp
#include <WiFiClientSecure.h>

// 拇指紋驗證（更安全）
const char* fingerprint = "AA BB CC DD EE FF...";

bool verifyFingerprint(WiFiClientSecure& client) {
  if (!client.connect(host, httpsPort)) {
    return false;
  }

  if (client.verify(fingerprint, host)) {
    return true;
  }

  return false;
}
```

## 低功耗模式

### ESP8266 睡眠模式

```cpp
// 淺睡眠
delay(1000);  // CPU 暂停但 WiFi 保持連接

// 深度睡眠
ESP.deepSleep(10e6);  // 10 秒，唤醒需要硬體 reset
```

### 喚醒觸發

```
ESP8266 Deep Sleep
                │
                ▼
┌───────────────────────────────────────┐
│                                       │
│   GPIO 16 ──> RESET (需要連接)        │
│                                       │
│   計時器觸發或外部信號喚醒             │
│                                       │
└───────────────────────────────────────┘
```

## MQTT 連線

### 完整 MQTT 範例

```cpp
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* mqtt_server = "broker.mqtt-dashboard.com";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe("home/led");
    } else {
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // 發布感測器資料
  float temperature = 25.5;
  char tempStr[10];
  dtostrf(temperature, 4, 2, tempStr);
  client.publish("home/temperature", tempStr);

  delay(5000);
}
```

## 網路除錯

### 序列除錯

```cpp
void printWiFiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
```

### 連線診斷

```cpp
void diagnoseConnection() {
  Serial.println("Connection diagnostics:");
  Serial.print("WiFi.status(): ");
  Serial.println(WiFi.status());

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected successfully");
    printWiFiStatus();
  } else {
    Serial.println("Connection failed");
  }
}
```

## 常用 AT 指令（ESP-01）

```cpp
// AT 指令用於純 ESP-01 模組
Serial.begin(115200);

// AT 測試
Serial.println("AT");

// 設定模式
Serial.println("AT+CWMODE=1");  // Station 模式

// 連接 WiFi
Serial.println("AT+CWJAP=\"SSID\",\"PASSWORD\"");

// 查詢 IP
Serial.println("AT+CIFSR");
```

## 小結

網路連接是物聯網裝置的核心功能：

1. **WiFi 模組**：ESP8266 是最具性價比的選擇
2. **協定選擇**：HTTP 適合簡單請求，MQTT 適合持續連線
3. **安全傳輸**：生產環境應使用 HTTPS
4. **功耗優化**：睡眠模式可大幅降低功耗
5. **除錯技巧**：序列輸出是最簡單的除錯方式

掌握這些網路連接技術，可以將你的嵌入式專案連接到更廣闊的網路世界。

---

**下一步**：[物聯網安全與隱私](focus7.md)

## 延伸閱讀

- [ESP8266 WiFi Tutorial](https://www.google.com/search?q=ESP8266+WiFi+tutorial)
- [IoT Network Security](https://www.google.com/search?q=IoT+network+security+best+practices)
- [MQTT Security Guide](https://www.google.com/search?q=MQTT+security+best+practices)