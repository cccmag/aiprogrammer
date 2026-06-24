# Raspberry Pi 2 Model B 評測

## 硬體規格

| 項目 | Raspberry Pi 2 Model B |
|------|------------------------|
| 處理器 | BCM2836 ARM Cortex-A7 四核 900MHz |
| RAM | 1GB LPDDR2 |
| USB | 4 個 |
| 網路 | 乙太網路 10/100 |
| GPIO | 40 針 |
| 價格 | 約 $35 |

## 與 Model B+ 比較

| 項目 | Pi 1 B+ | Pi 2 B |
|------|---------|--------|
| 處理器 | 單核 700MHz | 四核 900MHz |
| RAM | 512MB | 1GB |
| 效能 | 基準 1x | 基準 4-6x |

## 效能測試

```python
# Python 效能測試
import time

start = time.time()
for i in range(1000000):
    x = i * i
end = time.time()
print(f"Time: {end - start:.2f}s")
```

Pi 2 大約是 Pi 1 的 4-6 倍速度。

## 作業系統

- **Raspbian**：官方推薦
- **Ubuntu MATE**：輕量桌面
- **Windows 10 IoT Core**：微軟生態
- **OSMC**：媒體中心

## 散熱問題

Pi 2 在高負載下會過熱：

- 建議使用散熱片
- 可選配風扇
- 外殼應有通風孔

## 適用場景

優點：
- 效能足夠跑完整 Linux
- GPIO 支援多種介面
- 網路功能完整
- 價格實惠

缺點：
- 不支援 WiFi（需要 USB 介面卡）
- 類比輸入需要外部 ADC

## 小結

Raspberry Pi 2 Model B 是目前最具性價比的單板電腦之一，適合需要較強處理能力和網路功能的專案。

---

## 延伸閱讀

- [Raspberry Pi 2 Official Page](https://www.google.com/search?q=Raspberry+Pi+2+specifications)
- [Raspberry Pi Comparison](https://www.google.com/search?q=Raspberry+Pi+model+comparison)