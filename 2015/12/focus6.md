# 物聯網與嵌入式系統

## 前言

2015 年是物聯網（IoT）和嵌入式系統發展的關鍵一年。標準化工作取得進展、邊緣運算概念興起、多種開發板和技術持續演進。

## IoT 標準化進展

### OCF 與 IoTivity

Open Connectivity Foundation 發布了 IoTivity 1.0：

- **目標**：統一的 IoT 互操作性標準
- **支援公司**：Intel、Samsung、LG
- **開源實現**：IoTivity 專案

### Thread 網路協定

Nest 宣布 Thread 正式可用：

| 特性 | Thread | ZigBee | Z-Wave |
|------|--------|--------|--------|
| 網路層 | IP-based | IEEE 802.15.4 | IEEE 802.15.4 |
| 協定 | Thread | 802.15.4 + ZigBee | Z-Wave |
| _mesh | 是 | 是 | 是 |
| 低功耗 | 是 | 是 | 是 |
| 安全性 | AES-128 | AES-128 | AES-128 |

### AllSeen Alliance

AllJoyn 框架持續發展：

```javascript
// AllJoyn 範例
var AllJoyn = require('alljoyn');
var bus = AllJoyn.BusAttachment;

bus.connect("tcp://192.168.1.100:9955", function(err) {
    if (!err) {
        console.log("Connected to AllJoyn bus");
    }
});
```

## ARM mbed OS 5

### 發布與特點

ARM 在 2015 年發布了 mbed OS 5：

- **完整 RTOS**：即時作業系統
- **C++ API**：現代化介面
- **物聯網優化**：低功耗設計
- **安全性**：TLS、DtlsSecurity

### 架構

```
┌─────────────────────────────────────────────────────────────┐
│                     mbed OS 架構                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   應用層                                                     │
│      │                                                        │
│   mbed OS                                                    │
│      ├── Thread Stack ────> 6LoWPAN、Thread、CoAP           │
│      ├── BLE Stack ────────> Bluetooth LE                   │
│      ├── Socket API ────────> TCP/UDP/TLS                   │
│      ├── Storage API ───────> LittleFS、FAT                  │
│      └── Security ─────────> TLS、PSA Security              │
│                                                             │
│   硬體抽象層（HAL）                                          │
│      ├── STM32                                               │
│      ├── NXP                                                 │
│      └── Nordic                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 開發板生態

### 2015 年新品

| 開發板 | 發布時間 | 特點 |
|--------|---------|------|
| Arduino Tian | 3 月 | 64-bit MIPS + WiFi |
| Arduino Gemma | 6 月 | 可穿戴裝置 |
| Particle Electron | 9 月 | 蜂巢式 IoT |
| BBC micro:bit | 7 月 | 英國兒童教育 |
| ESP8266 | 全年 | 超低價 WiFi |
| Intel Curie | 9 月 | 紐扣大小 |

### Arduino 生態

```cpp
// Arduino 1.6/1.7 改進
#include <ArduinoJson.h>

void setup() {
    Serial.begin(9600);

    // 更好的序列埠
    Serial.println("Hello, World!");
}

void loop() {
    // 改進的 PWM
    analogWrite(9, 128);

    delay(100);
}
```

## Python 在嵌入式

### MicroPython

MicroPython 在 2015 年持續發展：

```python
# MicroPython on ESP8266
import machine
import network
import urequests

# WiFi 連線
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ssid', 'password')

# HTTP 請求
response = urequests.get('http://api.example.com/data')
print(response.json())
```

### Raspberry Pi

Raspberry Pi 在 2015 年推出了 Compute Module 3 和新版樹莓派：

```python
# Raspberry Pi GPIO Zero
from gpiozero import LED, Button

led = LED(17)
button = Button(2)

button.when_pressed = led.on
button.when_released = led.off
```

## 邊緣運算

### 概念興起

邊緣運算（Edge Computing）在 2015 年成為熱門話題：

- **延遲降低**：本地處理
- **頻寬節省**：減少上傳資料
- **隱私保護**：資料留在本地
- **離線支援**：網路斷開也能運作

### 架構對比

```
傳統架構：
感測器 ──────────────> 雲端 ──────────────> 使用者
                        │
                    所有處理

邊緣架構：
感測器 ──> 邊緣閘道器 ──> 雲端 ──────────────> 使用者
              │
          本地處理
```

## LPWAN 技術

### 低功耗廣域網路

| 技術 | 範圍 | 功耗 | 頻段 |
|------|------|------|------|
| LoRa | 2-10km | 低 | 未授權 |
| Sigfox | 3-10km | 極低 | 未授權 |
| NB-IoT | 1-10km | 低 | 授權頻段 |
| Weightless | 2-5km | 低 | 授權頻段 |

### 應用場景

- **智慧城市**：路燈、停車
- **資產追蹤**：物流、農業
- **環境監測**：水質、空氣
- **智慧建築**：能源管理

## 安全考量

### 2015 年安全事件

- **Jeep  Cherokee 入侵**：遠端控制
- **嬰兒監視器漏洞**：隱私風險
- **路由器漏洞**：家庭網路
- **智慧門鎖**：實體安全

### 安全實踐

```cpp
// 安全的 IoT 程式設計
#include <wolfssl/ssl.h>

// TLS 加密
WOLFSSL_CTX* ctx = wolfSSL_CTX_new(wolfSSLv3_client_method());
wolfSSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, 0);
```

## 未來展望

### 2016 年預期

1. **更多 LPWAN 部署**：城市級網路
2. **Edge AI**：邊緣裝置上的 ML
3. **Matter 標準**：智慧家庭互通
4. **5G 進展**：行動 IoT
5. **安全標準**：強制性安全要求

## 小結

2015 年物聯網領域的關鍵發展：

- **標準化推進**：OCF、Thread
- **mbed OS 5**：ARM 的 IoT OS
- **LPWAN 興起**：LoRa、Sigfox
- **邊緣運算**：分散式智慧
- **安全關注**：2015 年成為 IoT 安全元年

物聯網將在未來幾年繼續快速發展，改變我們的生活和工作方式。

---

## 延伸閱讀

- [IoTivity Official](https://www.google.com/search?q=IoTivity+official+project)
- [Thread Protocol](https://www.google.com/search?q=Thread+protocol+IoT)
- [ARM mbed OS](https://www.google.com/search?q=ARM+mbed+OS+5)