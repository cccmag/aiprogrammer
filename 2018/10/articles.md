# 文章索引

## 技術基礎回顧 (article1–5)

這五篇文章回顧 BERT 出現前的 NLP 基礎技術，包括詞嵌入、序列模型、Attention 機制等，這些技術是理解 BERT 的必備知識。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [Word2Vec 與詞嵌入回顧](article1.md) | 詞嵌入的原理、Word2Vec 訓練方法、詞向量應用場景 |
| 2 | [LSTM 與序列模型](article2.md) | LSTM 的結構與門控機制，如何處理序列資料 |
| 3 | [Attention 機制詳解](article3.md) | Attention 的計算方式、為何有效、與 RNN 的比較 |
| 4 | [ELMo 與預訓練語言模型](article4.md) | ELMo 的雙向語言模型方法、預訓練概念介紹 |
| 5 | [BERT 原論文導讀](article5.md) | BERT 論文核心內容導讀，重點結構分析 |

## 實作與應用 (article6–10)

這五篇文章深入 BERT 的實作細節與應用場景，涵蓋模型實作、微調策略與實際應用。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [雙向 Transformer 實作](article6.md) | 從零實作簡化版雙向 Transformer 層 |
| 7 | [BERT 微調實驗](article7.md) | 使用 PyTorch 進行 BERT 微調的完整流程 |
| 8 | [自然語言推理任務](article8.md) | NLI 任務介紹與 BERT 應用方法 |
| 9 | [問答系統應用](article9.md) | 使用 BERT 處理問答任務的技術細節 |
| 10 | [BERT 生態系與工具](article10.md) | Hugging Face Transformers、模型下載、微調工具 |

## 閱讀建議

建議讀者依序閱讀 article1 到 article5，打好 NLP 基礎知識，再進入 article6 到 article10 的實作部分。所有程式碼範例皆可在 `_code/` 目錄中找到對應的實作。

本期提供了整合的 `_code/bert_demo.py` 腳本，展示 BERT 的核心概念，包括文本向量化、位置編碼、Transformer 層運算與 MLM 損失計算。

## 參考資源

- https://www.google.com/search?q=BERT+NLP+fundamentals+Word2Vec+LSTM+attention+教程
- https://www.google.com/search?q=BERT+implementation+tutorial+fine-tuning+Hugging+Face+PyTorch+2018