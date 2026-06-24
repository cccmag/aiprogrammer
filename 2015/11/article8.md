# RTOS 入門指南

## 即時作業系統基礎

RTOS（Real-Time Operating System）是一種能夠在確定時間內回應事件的作業系統：

### 硬即時 vs 軟即時

| 類型 | 要求 | 範例 |
|------|------|------|
| 硬即時 | 嚴格時限 | 汽車安全氣囊 |
| 軟即時 | 平均時限 | 影片播放 |

## 為什麼需要 RTOS？

### 任務管理

```c
// 裸機程式
void loop() {
  readSensor();
  processData();
  controlMotor();
  networkCheck();
}

// RTOS：並行執行
void sensorTask(void* param) {
  while(1) {
    readSensor();
    vTaskDelay(100);
  }
}

void motorTask(void* param) {
  while(1) {
    controlMotor();
    vTaskDelay(50);
  }
}
```

### 任務優先級

```c
// 高優先級
void highPriorityTask(void* param) {
  while(1) {
    // 緊急處理
  }
}

// 低優先級
void lowPriorityTask(void* param) {
  while(1) {
    // 背景處理
    vTaskDelay(1000);
  }
}

xTaskCreate(highPriorityTask, "High", 2048, NULL, 2, NULL);
xTaskCreate(lowPriorityTask, "Low", 2048, NULL, 1, NULL);
```

## FreeRTOS

最受歡迎的開源 RTOS：

- **支援平台**：Arduino、ESP32、Raspberry Pi、STM32
- **授權**：MIT
- **功能**：任務管理、排程、同步

### ESP32 FreeRTOS

```cpp
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void sensorTask(void* param) {
  while(1) {
    // 讀取感測器
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void displayTask(void* param) {
  while(1) {
    // 更新顯示
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void setup() {
  xTaskCreate(sensorTask, "Sensor", 2048, NULL, 2, NULL);
  xTaskCreate(displayTask, "Display", 2048, NULL, 1, NULL);
}

void loop() {}
```

### 任務間通訊

```cpp
// 佇列
QueueHandle_t queue;

void senderTask(void* param) {
  int value = 0;
  while(1) {
    xQueueSend(queue, &value, 0);
    value++;
    vTaskDelay(1000);
  }
}

void receiverTask(void* param) {
  int value;
  while(1) {
    if (xQueueReceive(queue, &value, portMAX_DELAY)) {
      Serial.println(value);
    }
  }
}
```

## 常見 RTOS

| RTOS | 開發者 | 特點 |
|------|--------|------|
| FreeRTOS | Amazon | 開源、廣泛使用 |
| Zephyr | Linux Foundation | 現代化設計 |
| RT-Thread | 中國 | 輕量、功能豐富 |
| mbed OS | ARM | 針對 Cortex-M |

## 何時使用 RTOS

適合：
- 多個並行任務
- 嚴格的即時需求
- 複雜的系統架構

不適合：
- 簡單的單一任務
- 資源極度受限
- 學習曲線高的場景

## 小結

RTOS 是嵌入式開發的重要工具，適合需要處理多個並行任務的複雜系統。FreeRTOS 是學習和入門的最佳選擇。

---

## 延伸閱讀

- [FreeRTOS Official Site](https://www.google.com/search?q=FreeRTOS+official+website)
- [FreeRTOS Documentation](https://www.google.com/search?q=FreeRTOS+tutorial+beginners)