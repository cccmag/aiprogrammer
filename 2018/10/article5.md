# BERT 原論文導讀

## 論文基本資訊

標題：BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
作者：Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova (Google AI Language)
發表：2018 年 10 月

## 論文核心貢獻

1. **提出 MLM 預訓練目標**：透過遮蓋語言模型實現真正的雙向預訓練
2. **提出 NSP 預訓練任務**：學習句子級的語義關係
3. **展示「預訓練 + 微調」範式**：在大規模通用語料預訓練，針對任務微調
4. **11 項 NLP 任務刷新紀錄**：驗證方法的有效性

## 論文結構

### 1. Introduction
說明預訓練語言模型的背景、BERT 的設計動機與主要貢獻。

### 2. Related Work
回顧語言模型預訓練的相關工作，包括 ELMo、GPT 等，比較差異。

### 3. BERT
詳細描述模型架構與預訓練/微調方法：
- 輸入表示（詞嵌入 + 位置編碼 + 段落編碼）
- Masked LM 目標函數
- Next Sentence Prediction 目標函數
- 微調策略

### 4. Experiments
在 11 項 NLP 任務上進行實驗：
- GLUE 基準（SST-2, CoLA, MRPC, QQP, MNLI, QNLI, RTE, WNLI）
- SQuAD 問答
- SQuAD 2.0
- SWAG 語義推理

### 5. Ablation Studies
消融實驗分析各 component 的貢獻：
- MLM vs NSP 的重要性
- 模型規模的影響
- 預訓練步數的影響

## 關鍵設計決策

### 為何使用 MLM？
GPT 使用傳統語言模型，只能單向。ELMo 表面雙向但實際是兩個單向模型的拼接。MLM 讓真正的雙向表示學習成為可能。

### 為何加入 NSP？
句子級關係對問答、自然語言推理等任務很重要。NSP 任務強迫模型學習句子間關係。

### 為何只使用 Encoder？
BERT 專注於理解任務，Encoder 勝任。生成任務需要 Decoder，所以 GPT 使用 Decoder。

## 閱讀建議

建議讀者先閱讀「Attention is All You Need」了解 Transformer 基礎，再讀 BERT 論文。論文的數學公式較少，建議配合部落格文章理解。

## 參考資源

- https://www.google.com/search?q=BERT+原始論文+導讀+核心內容+結構分析
- https://www.google.com/search?q=BERT+paper+Devlin+2018+Google+pre-training+deep+bidirectional+transformers
- https://www.google.com/search?q=BERT+論文+MLM+NSP+預訓練+任務+詳解