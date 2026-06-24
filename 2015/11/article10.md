# 物聯網雲端平台比較

## 主要平台

### AWS IoT Core

**優點**：
- 完整的 AWS 生態整合
- 成熟的機器學習服務
- 全球基礎設施

**缺點**：
- 學習曲線較陡
- 成本複雜

### Azure IoT Hub

**優點**：
- 與 Microsoft 產品整合
- 強大的企業功能
- 混合雲支援

**缺點**：
- 價格較高
- 設備配置複雜

### Google Cloud IoT

**優點**：
- 與 Google AI 服務整合
- 強大的資料分析能力
- 靈活的定價

**缺點**：
- 區域可用性較少
- 學習資源相對較少

## 功能比較

| 功能 | AWS IoT | Azure IoT | Google Cloud |
|------|---------|-----------|-------------|
| 裝置管理 | ✓ | ✓ | ✓ |
| 訊息代理 | ✓ | ✓ | ✓ |
| 邊緣運算 | ✓ | ✓ | ✓ |
| 規則引擎 | ✓ | ✓ | ✗ |
| 機器學習 | ✓ | ✓ | ✓ |
| 免費方案 | 12 個月 | 12 個月 | 90 天 |

## 定價比較

### AWS IoT Core

- 連線：$0.08/百萬訊息
- 訊息：$1.00/百萬訊息

### Azure IoT Hub

- S1：$50/百萬訊息
- S2：$10/百萬訊息
- S3：$1/百萬訊息

### Google Cloud IoT

- 裝置連線：$0.06/百萬分鐘
- 訊息：$0.01/百萬訊息

## 程式範例

### AWS IoT SDK

```python
import boto3

iot = boto3.client('iot-data')

def publish():
    iot.publish(
        topic='home/sensor',
        qos=1,
        payload='{"temperature": 25}'
    )
```

### Azure IoT SDK

```python
from azure.iot.hub import IoTHubRegistryManager

registry_manager = IoTHubRegistryManager("conn_string")

def send():
    registry_manager.send_message("device_id", "payload")
```

## 選擇指南

| 場景 | 推薦平台 |
|------|---------|
| 已有 AWS 服務 | AWS IoT |
| 微軟生態系 | Azure IoT |
| AI/ML 需求 | Google Cloud |
| 成本敏感 | Google Cloud |
| 企業級需求 | Azure IoT |

## 自託管方案

如果不想使用雲端服務，可以考慮：

- **Mosquitto**：開源 MQTT Broker
- **ThingsBoard**：開源物聯網平台
- **Home Assistant**：智慧家庭平台

## 小結

選擇雲端平台需要考慮多種因素：現有技術棧、預算、功能需求、團隊技能。建議從小型專案開始，逐步擴展到更完整的解決方案。

---

## 延伸閱讀

- [AWS IoT Documentation](https://www.google.com/search?q=AWS+IoT+Core+documentation)
- [Azure IoT Hub Documentation](https://www.google.com/search?q=Azure+IoT+Hub+documentation)
- [Google Cloud IoT Documentation](https://www.google.com/search?q=Google+Cloud+IoT+documentation)