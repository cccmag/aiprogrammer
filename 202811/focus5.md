# 邊緣推論硬體（2020-2028）

## 硬體格局

邊緣 AI 的硬體生態多元，從極低功耗的 MCU NPU 到數十 TOPs 的邊緣 GPU，涵蓋三個主要層級：

### 微控制器層級（mW 級）

- **Syntiant NDP200**（2020）— 超低功耗神經決策處理器，1mW 以下執行關鍵字辨識。
- **Arm Ethos-U55/U65**（2021）— 針對 Cortex-M 與 Cortex-A 的微神經網路處理器，支援 256 MAC/週期。
- **Alif Semiconductor Ensemble**（2024）— 首款整合 Ethos-U85 的 MCU，AI 推論功耗低於 5mW。
- **Ambiq Apollo4**（2025）— 使用 SPOT 平台，主打亞閾值運算的 AI MCU。

### 應用處理器層級（W 級）

- **NVIDIA Jetson Orin NX**（2022）— 70 TOPs 算力，適合機器人與智慧相機（[Google 搜尋](https://www.google.com/search?q=NVIDIA+Jetson+Orin+edge+AI)）。
- **Qualcomm Snapdragon 8 Elite**（2024）— 整合 Hexagon NPU，手機端 AI 算力達 45 TOPs。
- **MediaTek Dimensity 9400**（2025）— 搭載第八代 APU，支援 INT4 量化推論。
- **Apple M4**（2025）— 16 核心 NPU，38 TOPs，Mac 與 iPad 的邊緣 AI 主力。

### 加速卡與推論晶片（10-100W）

- **Hailo-8**（2021）— 26 TOPs，USB 外接式 AI 加速器（[Google 搜尋](https://www.google.com/search?q=Hailo-8+edge+AI+accelerator)）。
- **Google Coral Edge TPU**（2020）— 4 TOPs，USB 與 M.2 規格。
- **Intel Movidius Myriad X**（2020）— 4 TOPs，內建硬體神經網路加速引擎。

## 關鍵指標比較

| 晶片 | 算力 (TOPs) | 功耗 | 發布年份 |
|------|-------------|------|----------|
| Arm Ethos-U55 | 0.5 | 50mW | 2021 |
| Google Edge TPU | 4 | 2W | 2020 |
| Hailo-8 | 26 | 2.5W | 2021 |
| Jetson Orin NX | 70 | 15W | 2022 |
| Snapdragon X Elite | 45 | 5W | 2024 |

## 新興技術

### 記憶體內運算（Compute-in-Memory, CIM）

2024 年起，Samsung 與 TSMC 開始量產 SRAM 型 CIM 晶片，在記憶體內直接進行 MAC 運算，大幅減少資料搬運能耗。預估 2027 年 CIM 將使邊緣 AI 能耗再降 10 倍。

### 光學神經網路

2026 年 Lightmatter 與 Lightelligence 開始推出光子 AI 加速晶片原型，專注於資料中心邊緣節點。

## 參考資源

- [Google 搜尋：Edge AI hardware comparison 2026](https://www.google.com/search?q=edge+AI+hardware+NPU+comparison+2026)
- [Google 搜尋：Compute-in-memory AI chip](https://www.google.com/search?q=compute+in+memory+AI+chip+2025)
