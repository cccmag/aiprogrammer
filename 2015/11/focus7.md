# 物聯網安全與隱私

## 前言

物聯網裝置的安全性近年來成為重要議題。從駭客入侵嬰兒監視器到大規模 DDoS 攻擊，物聯網安全事件層出不窮。本期將探討物聯網安全的基本原則和實踐方法。

## 安全威脅

### 常見威脅類型

| 威脅 | 說明 | 影響 |
|------|------|------|
| 資料竊取 | 敏感資料被截獲 | 隱私洩漏 |
| 偽裝攻擊 | 假冒合法裝置 | 未授權存取 |
| 阻斷服務 | 癱瘓服務 | 系統無法使用 |
| 惡意軟體 | 感染和控制 | 成為攻擊跳板 |
| 中間人攻擊 | 攔截通訊 | 資料竄改 |

### 知名事件

**2014 年：Trender 嬰兒監視器漏洞**

研究人員發現多款嬰兒監視器存在安全漏洞，攻擊者可以遠端存取攝影機和麥克風。

**2015 年：黑帽大會 - Jeep Cherokee 入侵**

研究人員遠端入侵 Jeep Cherokee 的娛樂系統，進而控制引擎、剎車等關鍵系統。

**2016 年：Mirai 殭屍網路**

Mirai 惡意軟體感染數十萬 IoT 裝置，發動史上最大規模 DDoS 攻擊。

## 加密基礎

### 對稱加密

加密和解密使用同一把金鑰：

```
明文 ──>[金鑰加密]──> 密文 ──>[同一金鑰解密]──> 明文
```

優點：速度快
缺點：金鑰分發困難

常用演算法：AES、DES、3DES

### 非對稱加密

公鑰加密、私鑰解密：

```
明文 ──>[公鑰加密]──> 密文 ──>[私鑰解密]──> 明文
```

優點：金鑰分發簡單
缺點：速度慢

常用演算法：RSA、ECC

### 雜湊函數

單向轉換，不可逆：

```
資料 ──>[雜湊]──> 固定長度摘要
```

常用演算法：SHA-256、MD5（已不安全）

## WiFi 安全

### WPA2-PSK

適合小型網路：

```cpp
const char* ssid = "YourNetwork";
const char* password = "YourPassword";  // 至少 8 字元
```

### WPA2 Enterprise

適合企業環境，需要 RADIUS 伺服器。

### 安全的 WiFi 程式設計

```cpp
// 驗證 WiFi 連線
bool verifyWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  // 檢查 BSSID 防止 ARP 欺騙
  Serial.print("Connected to: ");
  Serial.println(WiFi.BSSIDstr());

  return true;
}
```

## TLS/SSL 加密

### 憑證驗證

```cpp
#include <WiFiClientSecure.h>

WiFiClientSecure secureClient;

void setup() {
  // 驗證伺服器憑證
  secureClient.setCACert(test_ca_cert);
}
```

### ESP8266 HTTPS

```cpp
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

WiFiClientSecure httpsClient;

void sendSecure() {
  HTTPClient https;
  https.begin(httpsClient, "https://your-server.com/api");
  https.setInsecure();  // 僅測試用

  int httpCode = https.GET();
  if (httpCode > 0) {
    String payload = https.getString();
  }
  https.end();
}
```

## MQTT 安全

### 認證

```cpp
client.setServer(mqtt_server, mqtt_port);
client.setCallback(callback);

// 設定用戶端 ID、使用者名稱、密碼
if (client.connect("device-001", "username", "password")) {
  // 連線成功
}
```

### TLS 加密

```cpp
WiFiClientSecure espClient;
espClient.setCACert(ca_cert);

PubSubClient mqttClient(espClient);
mqttClient.setServer(mqtt_server, 8883);
```

### ACL（存取控制清單）

```python
# Mosquitto ACL 設定檔
user device1
topic read home/sensors/+
topic write home/actuators/+

user device2
topic read home/sensors/+
topic write home/device2/+
```

## API 安全

### API Key

簡單的認證方式：

```cpp
void sendWithAPIKey(float data) {
  HTTPClient http;
  http.begin("http://api.example.com/data");
  http.addHeader("X-API-Key", "your-api-key");
  http.POST(String(data));
}
```

### JWT（JSON Web Token）

```python
import jwt

# 產生 JWT
token = jwt.encode({
    'user_id': 123,
    'exp': datetime.utcnow() + timedelta(hours=1)
}, 'secret_key')

# 驗證 JWT
try:
    payload = jwt.decode(token, 'secret_key')
except jwt.ExpiredSignatureError:
    print("Token expired")
```

### OAuth 2.0

適合第三方應用程式存取：

```
┌─────────┐    授權請求     ┌─────────┐
│  Client │ ───────────────> │  Auth   │
│         │ <──────────────── │ Server  │
└─────────┘    授權碼        └─────────┘
     │                              │
     │    授權碼 + client_id        │
     │ ────────────────────────────> │
     │                              │
     │    存取令牌                  │
     │ <─────────────────────────── │
```

## 密碼安全

### 金鑰管理

1. **不要在程式碼中硬編碼密碼**
2. **使用環境變數或配置文件**
3. **定期更換金鑰**

```cpp
// 不好
const char* password = "secret123";

// 好：使用配置文件
Config config = loadConfig("/config.json");
const char* password = config.wifi_password;
```

### 強密碼建議

- 長度至少 12 字元
- 混合大小寫、數字、特殊字元
- 不要使用常見單詞
- 不要重複使用密碼

## 裝置安全

### 安全開機

1. **驗證韌體簽章**
2. **安全儲存金鑰**
3. **防止 JTAG/SWD 存取**

### OTA 更新

```cpp
#include <ArduinoOTA.h>

void setupOTA() {
  ArduinoOTA.onStart([]() {
    // 更新開始
  });

  ArduinoOTA.onEnd([]() {
    // 更新完成
  });

  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();
}
```

### 序列埠保護

```cpp
// 啟用序列埠密碼保護
if (Serial.available()) {
  String input = Serial.readStringUntil('\n');
  if (input == "secret_password") {
    // 允許存取序列除錯
  }
}
```

## 隱私保護

### 資料最小化

只收集必要的資料：

```python
# 不好：收集過多資料
user_data = {
    'name': 'John',
    'email': 'john@example.com',
    'phone': '1234567890',
    'address': '123 Main St',
    'ssn': '123-45-6789'
}

# 好：只收集必要的資料
user_data = {
    'name': 'John',
    'email': 'john@example.com'
}
```

### 資料加密儲存

```python
from cryptography.fernet import Fernet

# 產生金鑰
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(b"sensitive data")

# 解密
original = cipher.decrypt(encrypted)
```

### 匿名化處理

```python
# 移除可識別資訊
def anonymize(data):
    data['ip'] = hash(data['ip'])  # 保留 IP 類型但不保留原始值
    del data['name']
    del data['email']
    return data
```

## 安全開發實踐

### OWASP IoT Top 10

1. 弱密碼/可猜測密碼
2. 不安全網路服務
3. 不安全介面
4. 使用不安全元件
5. 弱隱私保護
6. 不安全資料傳輸
7. 缺乏系統更新機制
8. 不安全設定
9. 缺乏實體強化
10. 缺少回報機制

### 安全檢查清單

- [ ] 使用強認證機制
- [ ] 加密所有敏感資料
- [ ] 使用 TLS/SSL
- [ ] 定期更新韌體
- [ ] 驗證輸入資料
- [ ] 實作存取控制
- [ ] 記錄安全事件
- [ ] 測試安全漏洞

## 小結

物聯網安全是系統性工程，需要從設計階段就開始考慮：

1. **加密傳輸**：所有網路傳輸都應加密
2. **認證授權**：確認裝置和用戶身份
3. **金鑰管理**：安全地儲存和管理密鑰
4. **OTA 更新**：保持韌體更新
5. **隱私保護**：最小化資料收集
6. **安全設計**：從一開始就考慮安全

安全不是附加功能，而是基本要求。

---

## 延伸閱讀

- [OWASP IoT Top 10](https://www.google.com/search?q=OWASP+IoT+top+10)
- [IoT Security Guidelines](https://www.google.com/search?q=IoT+security+guidelines)
- [TLS/SSL Tutorial](https://www.google.com/search?q=TLS+SSL+tutorial+arduino)