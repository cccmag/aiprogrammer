# Raspberry Pi 與單板電腦

## 前言

Raspberry Pi 是一款由英國 Raspberry Pi 基金會開發的信用卡大小的單板電腦。自 2012 年推出以來，已經售出超過數百萬台，成為教育、嗜好和商業應用的熱門選擇。

## Raspberry Pi 型號比較

### 主流型號

| 型號 | 處理器 | RAM | USB | 網路 | 特點 |
|------|--------|-----|-----|------|------|
| Pi 1 Model A+ | 700MHz ARM11 | 256MB | 1 | 無 | 超低功耗 |
| Pi 1 Model B+ | 700MHz ARM11 | 512MB | 4 | 乙太網路 | 经典款 |
| Pi 2 Model B | 900MHz 四核 Cortex-A7 | 1GB | 4 | 乙太網路 | 效能提升 |
| Pi 3 Model B | 1.2GHz 四核 Cortex-A53 | 1GB | 4 | WiFi + BT | 內建無線 |
| Pi Zero | 1GHz ARM11 | 512MB | 1 (OTG) | 無 | 極小尺寸 |

### 選擇指南

- **初學者**：Raspberry Pi 3 Model B
- **行動專案**：Raspberry Pi Zero
- **工業應用**：Compute Module 3
- **需要低功耗**：Model A+

## 作業系統安裝

### 所需材料

- microSD 卡（至少 8GB，Class 10 推薦）
- 5V/2.5A Micro USB 電源供應器
- HDMI 線和顯示器
- USB 鍵盤和滑鼠

### 安裝步驟

#### 1. 下載映像檔

從 [raspberrypi.org](https://www.raspberrypi.org/downloads/) 下載 Raspbian 映像檔。

#### 2. 燒錄映像檔

使用 Etcher 或 dd 燒錄：

```bash
# 使用 dd（類 Unix 系統）
sudo dd bs=4M if=2015-11-21-raspbian-jessie.img of=/dev/sdX status=progress
sync
```

#### 3. 首次啟動

1. 將 microSD 卡插入 Raspberry Pi
2. 連接 HDMI、鍵鼠、電源
3. 開機後跟隨初始設定精靈

### 進階：無頭設定

不需要螢幕和鍵鼠，通過 SSH 存取：

1. 在燒錄後，在 boot 分區建立名為 `ssh` 的空白檔案
2. 在 boot 分區建立 `wpa_supplicant.conf`：

```
country=TW
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="your_SSID"
    psk="your_PASSWORD"
}
```

3. 啟動後可通過 SSH 連接（預設帳號：pi，密碼：raspberry）

## GPIO 程式設計

### GPIO 简介

GPIO（General Purpose Input/Output）是 Raspberry Pi 與硬體互動的介面：

```
        GPIO 針腳分布（40 針）
        
    3.3V  ───  1  2 ───  5V
    GPIO2 ───  3  4 ───  5V
    GPIO3 ───  5  6 ───  GND
    GPIO4 ───  7  8 ───  GPIO14
      GND ───  9 10 ───  GPIO15
   GPIO17 ─── 11 12 ───  GPIO18
   GPIO27 ─── 13 14 ───  GND
   GPIO22 ─── 15 16 ───  GPIO23
    3.3V ─── 17 18 ───  GPIO24
   GPIO10 ─── 19 20 ───  GND
    ...
```

### Python + RPi.GPIO

```python
import RPi.GPIO as GPIO
import time

# 設定編號模式
GPIO.setmode(GPIO.BOARD)  # 使用針腳編號

LED_PIN = 11

GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

### Python + GPIO Zero

更簡潔的 API：

```python
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

### 讀取按鈕輸入

```python
from gpiozero import Button

button = Button(2)

while True:
    if button.is_pressed:
        print("Button pressed!")
    sleep(0.1)
```

## I2C 通訊

### 啟用 I2C

```bash
sudo raspi-config
# 選擇 Interfacing Options → I2C → Enable
sudo reboot
```

### I2C 掃描工具

```python
import smbus2

bus = smbus2.SMBus(1)

print("Scanning I2C devices...")
for address in range(0x03, 0x78):
    try:
        bus.read_byte(address)
        print(f"Found device at 0x{address:02X}")
    except:
        pass
```

### 使用 BMP180 氣壓感測器

```python
import smbus2
import time

class BMP180:
    def __init__(self, address=0x77):
        self.bus = smbus2.SMBus(1)
        self.address = address

    def read_temperature(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x2E)
        time.sleep(0.005)
        data = self.bus.read_word_data(self.address, 0xF6)
        return data

# 使用
sensor = BMP180()
temp = sensor.read_temperature()
print(f"Temperature: {temp}")
```

## SPI 通訊

### 啟用 SPI

```bash
sudo raspi-config
# Interfacing Options → SPI → Enable
```

### Python + spidev

```python
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # 匯流排 0，裝置 0
spi.max_speed_hz = 1350000

while True:
    response = spi.xfer2([0x01, 0x80, 0x00])
    print(f"Response: {response}")
    time.sleep(1)

spi.close()
```

## Web 服務器範例

Raspberry Pi 可以作為 Web 伺服器：

```python
# Flask 範例
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

@app.route('/')
def index():
    return 'Raspberry Pi Web Server'

@app.route('/led/on')
def led_on():
    GPIO.output(11, GPIO.HIGH)
    return 'LED ON'

@app.route('/led/off')
def led_off():
    GPIO.output(11, GPIO.LOW)
    return 'LED OFF'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

## 遠端存取

### VNC 伺服器

```bash
# 安裝
sudo apt-get install tightvncserver

# 啟動
vncserver :1

# 客戶端連接：IP:5901
```

### 檔案傳輸

```bash
# 使用 scp
scp file.txt pi@192.168.1.100:/home/pi/

# 使用 sftp
sftp pi@192.168.1.100
```

## 效能優化

### 散熱

Raspberry Pi 3 在負載下可能過熱：

- 使用散熱片
- 安裝散熱風扇
- 考慮購買帶外殼的散熱套件

### 電源

使用合格的 5V/2.5A 電源供應器：

- 供電不足可能導致不穩定
- 建議使用官方電源供應器

## 小結

Raspberry Pi 是一款功能強大的單板電腦，適合需要網路連接和更強處理能力的專案。通過本章的學習，你應該已經能夠：

- 安裝和設定 Raspberry Pi
- 使用 GPIO 控制硬體
- 建立簡單的網頁服務器
- 通過 I2C/SPI 連接感測器

Raspberry Pi 與 Arduino 各有優缺點，選擇哪個取決於你的專案需求。

---

**下一步**：[感測器與輸入裝置](focus3.md)

## 延伸閱讀

- [Raspberry Pi Official Documentation](https://www.google.com/search?q=Raspberry+Pi+documentation)
- [GPIO Zero Documentation](https://www.google.com/search?q=gpiozero+python+library)
- [RPi.GPIO Documentation](https://www.google.com/search?q=RPi.GPIO+tutorial)