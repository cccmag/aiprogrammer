# 即時 AI 系統概述

## 從批次處理到毫秒級回應（2015-2028）

### 前言

2015 年以前，AI 系統幾乎都是批次處理——訓練一個模型要數天，推論也要秒級延遲。即時 AI 系統的崛起來自三個驅動力：物聯網裝置爆炸、5G 低延遲網路、以及使用者對即時互動的期望。

### 即時系統的定義

即時 AI 系統指在**嚴格時間限制內**完成資料處理與推論的系統：

```
延遲層級:
  批次（>1s）    → 傳統 ML 管線
  準即時（100ms） → 串流分析
  即時（<10ms）  → 自動駕駛、語音互動
  超即時（<1ms） → FPGA 加速推論
```

### 即時 AI 的關鍵挑戰（2015-2020）

**資料側**：傳統 ML 管線依賴 `pandas` 批次處理，無法應對串流資料。

```python
# 批次處理（2015 年典型做法）
import pandas as pd
df = pd.read_csv("transactions.csv")
features = df.groupby("user_id").agg(...)
model.predict(features)  # 延遲：>1s
```

**模型側**：大型模型（VGG、BERT）推論需要 GPU，無法部署在邊緣裝置。

**架構側**：資料庫 → 模型 → 結果的端到端管線缺乏延遲預算管理。

### 架構演進（2020-2025）

2020 年起，即時 AI 架構開始標準化為**串流-推論-反饋**三層：

```
┌─────────┐    ┌──────────┐    ┌─────────┐
│ 串流層   │ → │ 推論層    │ → │ 反饋層   │
│ Kafka   │    │ Triton   │    │ Kafka   │
│ Flink   │    │ ONNX     │    │ 特徵儲存 │
└─────────┘    └──────────┘    └─────────┘
```

### 即時 AI 的成熟（2025-2028）

截至 2028 年，即時 AI 已成為基礎設施：

- **延遲預算分解**：每個環節分配毫秒級預算
- **端到端監控**：從資料入口到推論結果的即時可觀測性
- **自動補償**：當延遲超標時自動降級（降解析度、用輕量模型）

### 關鍵技術時間線

| 年份 | 里程碑 |
|------|--------|
| 2015 | Spark Streaming 支援 ML |
| 2017 | TensorFlow Serving 發布 |
| 2019 | NVIDIA Triton Inference Server |
| 2021 | 邊緣 TPU 量產 |
| 2023 | 即時特徵平台成熟 |
| 2025 | 端到端即時 ML 平台 |
| 2028 | 自主即時 AI 系統 |

### 小結

即時 AI 系統的核心矛盾是**精度 vs. 延遲**。十年的發展告訴我們：沒有單一架構適合所有場景，系統設計必須在資料新鮮度、模型精度和回應速度之間取得平衡。

---

**下一步**：[串流資料處理架構](focus2.md)

## 延伸閱讀

- [即時機器學習系統設計](https://www.google.com/search?q=real+time+machine+learning+system+design)
- [ML 系統延遲最佳化指南](https://www.google.com/search?q=ML+inference+latency+optimization+guide)
- [Uber 的即時 ML 平台](https://www.google.com/search?q=Uber+real+time+machine+learning+platform)
