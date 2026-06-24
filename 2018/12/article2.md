# BERT 完整回顧

## BERT 發表

2018 年 10 月，Google 發表「BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding」。這是 2018 年最重要的 NLP 突破。

## 核心創新

### 雙向 Transformer Encoder
不同於 GPT 的單向 Decoder，BERT 使用雙向 Encoder：
- 每個位置可以看到完整的上下文
- 真正的雙向語言理解

### Masked Language Model
BERT 的預訓練任務之一：
- 隨機遮蓋 15% 的輸入 token
- 根據上下文預測被遮蓋的詞
- 這種「填空」式任務強迫雙向學習

### Next Sentence Prediction
第二個預訓練任務：
- 50% 是實際相連的句子
- 50% 是隨機組合的句子
- 學習句子間的關係

## 模型規模

| 版本 | 層數 | 隱藏維度 | 頭數 | 參數 |
|------|------|----------|------|------|
| Base | 12 | 768 | 12 | 110M |
| Large | 24 | 1024 | 16 | 340M |

## 任務表現

BERT 在 11 項 NLP 任務上刷新紀錄：

| 任務 | 以往最佳 | BERT |
|------|----------|------|
| SQuAD (EM) | 91.1% | 93.2% |
| SQuAD (F1) | 92.3% | 96.6% |
| GLUE | 72.8% | 80.5% |

## 對 NLP 的影響

### 預訓練 + 微調範式
BERT 確立了這種方法：
1. 在大型語料上預訓練
2. 在任務資料上微調
3. 大幅減少任務特定資料需求

### 產業應用
- Google 將 BERT 應用於搜尋引擎
- 多家公司採用 BERT 提升產品
- 加速 NLP 應用的普及

### 社群響應
- Hugging Face Transformers 快速支持
- 研究者積極改進與擴展
- 預訓練模型生態蓬勃發展

## BERT 的局限

1. **計算成本高**：預訓練需要大量 TPU
2. **生成能力弱**：雙向 Encoder 不適合生成
3. **靜態遮蓋**：訓練與推理不一致

## 後續發展

BERT 開創了一系列研究：
- RoBERTa：去除 NSP，增加訓練
- ALBERT：參數共享
- DistilBERT：蒸餾壓縮
- 各种领域适配版本

## 參考資源

- https://www.google.com/search?q=BERT+完整回顧+2018+原理+實現+影響+NLP
- https://www.google.com/search?q=BERT+預訓練+微調+GLUE+SQuAD+任務+性能+表現
- https://www.google.com/search?q=BERT+影響+NLP+產業+應用+生態+2018+年度回顧