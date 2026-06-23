# 文章索引

## 程式設計篇（5 篇）

### 1. [嵌入式 Rust 入門指南](article1.md)
**no_std、cortex-m-rt、embedded-hal 從零開始**

從 `#![no_std]` 的概念出發，逐步建立嵌入式 Rust 開發環境：目標 triple 配置、panic_handler 撰寫、cortex-m-rt 啟動碼、embedded-hal trait 的理解。適合初學者建立完整的嵌入式 Rust 知識框架。

### 2. [GPIO 與中斷程式設計](article2.md)
**暫存器操作、NVIC、外部中斷**

深入 MCU 的 GPIO 暫存器層級操作，介紹 ARM Cortex-M NVIC 中斷控制器的使用方法。從輪詢模式到中斷驅動，展示 Rust 型別系統如何防止 GPIO 方向錯誤。

### 3. [UART/SPI/I2C 通訊實戰](article3.md)
**輪詢/中斷/DMA 模式對比**

從 UART 的 Hello World 開始，逐步深入 SPI 與 I2C 通訊協定。詳細比較三種傳輸模式（輪詢、中斷、DMA）的取捨，並介紹 embedded-hal 的 blocking 與 async trait。

### 4. [RTIC 框架即時系統開發](article4.md)
**優先權模型、資源管理、任務排程**

RTIC 是 Rust 嵌入式生態最重要的即時框架。本文深入 RTIC 的優先權模型、`lock()` 資源管理機制、任務間通訊模式，以及編譯期排程分析的原理。

### 5. [低功耗設計與最佳化](article5.md)
**睡眠模式、喚醒源、堆疊分析**

嵌入式系統的功耗最佳化是產品成敗的關鍵。介紹 MCU 的各種睡眠模式、喚醒源配置、堆疊使用量分析，以及 Rust 編譯器層級的最佳化策略。

## AI 應用篇（5 篇）

### 6. [AI 在嵌入式程式碼生成中的應用](article6.md)
**LLM 生成 PAC/HAL/驅動程式碼**

LLM 正在改變嵌入式開發的方式。本文探討如何利用 AI 從 datasheet 和 SVD 檔案自動生成 PAC 層暫存器定義、HAL 實作，以及常見感測器的驅動程式碼。

### 7. [嵌入式 ML 推論](article7.md)
**TFLite Micro vs Rust 方案對比**

將機器學習模型部署到 MCU 上執行推論。對比 TensorFlow Lite Micro 和純 Rust 方案（Candle、burn-embedded）在記憶體使用、推論速度、開發體驗上的差異。

### 8. [Rust 嵌入式生態深度解析](article8.md)
**embedded-hal、HAL crate、BSP 三層架構**

深入理解 Rust 嵌入式生態的層次化設計：PAC（svd2rust）→ HAL（embedded-hal 實作）→ BSP（開發板支援）。分析各層的設計哲學與使用場景。

### 9. [感測器資料處理與邊緣運算](article9.md)
**資料融合、濾波、上雲**

連接真實感測器（溫度、IMU、光學）的完整流程：原始資料讀取、數位濾波（卡爾曼濾波、互補濾波）、感測器融合，以及透過 WiFi/LoRa 上傳雲端。

### 10. [嵌入式 Rust 專案架構設計](article10.md)
**模組化、測試、CI 實戰**

如何組織一個生產級的嵌入式 Rust 專案：模組劃分策略、單元測試與整合測試、硬體在迴路測試（HIL）、CI/CD 管線設計，以及版本管理最佳實務。
