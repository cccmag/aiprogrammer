# 程式碼說明 — 年度回顧示範

## 功能概述

`_code/year_review.py` 展示 2018 年 AI 技術的里程碑事件，並以視覺化方式呈現各項技術的發展時間線。這有助於讀者宏觀理解 2018 年 AI 領域的重要進展。

## demo() 函數說明

### 1. 2018 年重要事件時間線
列出 2018 年 AI 領域的關鍵事件，包括模型發布、框架更新、硬體發布等。

### 2. 技術成熟度評估
根據各項技術的採用度與影響力，評估其在 2018 年的成熟度。

### 3. 統計摘要
展示 2018 年的一些關鍵數據，如模型參數量、訓練時間等。

## 執行方式

```bash
cd _code
python3 year_review.py
```

## 輸出範例

```
====================================================
2018 年 AI 技術年度回顧
====================================================

[1] 2018 年重要事件時間線

月份    事件
02     ELMo 發布 — 雙向 LSTM 預訓練語言模型
06     GPT 發布 — 單向 Transformer 生成式預訓練
08     NVIDIA Turing 顯示卡發布
10     BERT 發布 — 雙向 Transformer 預訓練
11     PyTorch 1.0 正式版發布
12     TensorFlow 2.0 預覽版發布

[2] 技術成熟度評估

技術              成熟度    採用度
預訓練語言模型    高       快速增長
Transformer       高       主流
深度學習框架      高       雙雄並立
AI 硬體          高       持續進化

[3] 關鍵數據

最大預訓練模型: ~340M 參數 (BERT-large)
GPU 效能提升: ~50% (vs Pascal)
主要開源框架: TensorFlow, PyTorch

====================================================
回顧完成
====================================================
```

## 參考資源

- https://www.google.com/search?q=2018+AI+年度回顧+代碼+Python+視覺化+時間線
- https://www.google.com/search?q=AI+milestones+2018+timeline+BERT+GPT+ELMo+summary
- https://www.google.com/search?q=2018+AI+technology+review+highlights+Python+demo