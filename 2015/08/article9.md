# 物聯網與邊緣計算

## 前言

物聯網 (IoT) 和邊緣計算正在改變我們與實體世界互動的方式。

---

## 物聯網架構

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   感測器    │ ──> │   閘道器    │ ──> │    雲端     │
│ (Sensors)  │     │  (Gateway)  │     │   (Cloud)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           v
                    ┌─────────────┐
                    │   邊緣     │
                    │ (Edge)     │
                    └─────────────┘
```

### 層級架構

1. **裝置層**：感測器、致動器
2. **網路層**：通訊協定、閘道器
3. **邊緣層**：本地處理、儲存
4. **雲端層**：分析、儲存、應用

---

## 常見通訊協定

### MQTT

輕量級發布/訂閱協定，專為 IoT 設計。

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("sensors/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.example.com", 1883, 60)
client.loop_forever()
```

### CoAP

專為受限裝置設計的 Web 協定。

### HTTP/REST

傳統的 Web 介面。

[搜尋 MQTT vs CoAP IoT](https://www.google.com/search?q=MQTT+vs+CoAP+IoT+protocol)

---

## 邊緣計算

### 為什麼需要邊緣計算

- **延遲**：即時處理需求
- **頻寬**：減少傳輸資料量
- **隱私**：敏感資料本地處理
- **可靠性**：網路中斷時仍可運作

### 邊緣運算架構

```
┌──────────────────────────────────────────┐
│              雲端資料中心                 │
└──────────────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         v                     v
┌─────────────┐        ┌─────────────┐
│  Edge Node  │        │  Edge Node  │
│ (工廠)      │        │ (商店)      │
└─────────────┘        └─────────────┘
         │                     │
         v                     v
┌─────────────┐        ┌─────────────┐
│  感測器    │        │  感測器    │
└─────────────┘        └─────────────┘
```

---

## 嵌入式系統

### Raspberry Pi

```bash
# 安裝作業系統
dd if=raspbian.img of=/dev/sdX bs=4M

# 遠端連線
ssh pi@raspberrypi.local

# GPIO 控制
gpio -g mode 18 out
gpio -g write 18 1
```

### Arduino

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
}
```

---

## 嵌入式 Linux

### Buildroot

建構自訂嵌入式 Linux 系統。

```bash
make menuconfig
make
```

### Yocto Project

工業級嵌入式 Linux 發行版。

```bash
# 建立環境
source poky/oe-init-build-env
bitbake core-image-minimal
```

---

## 案例研究

### 智慧工廠

```
感測器 ──> 邊緣伺服器 ──> 本地控制
             │
             v
         雲端分析 ──> 生產優化
```

### 智慧城市

```
交通感測器 ──> Edge ──> 即時交通控制
                     │
                     v
                 雲端 ──> 長期規劃
```

---

## 安全考量

### 威脅

- 裝置被入侵
- 網路攻擊
- 資料竊取
- 韌體漏洞

### 防護措施

```bash
# 安全的遠端存取
ssh -i key.pem pi@device.local

# 定期更新韌體
fwupdmgr get-updates
fwupdmgr update

# 網路隔離
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT
```

---

## 工具與平台

| 平台 | 說明 |
|------|------|
| AWS IoT | 托管 IoT 服務 |
| Google Cloud IoT | 邊緣和雲端整合 |
| Azure IoT Hub | 裝置管理 |
| ThingsBoard | 開源 IoT 平台 |
| Node-RED | 視覺化流程編輯器 |

---

## 小結

IoT 和邊緣計算代表著運算範式的轉變，從集中式雲端到分散式邊緣。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [MQTT 官方網站](https://www.google.com/search?q=MQTT+official+website)
- [Raspberry Pi 官方網站](https://www.google.com/search?q=Raspberry+Pi+official+website)
- [IoT 安全最佳實踐](https://www.google.com/search?q=IoT+security+best+practices)