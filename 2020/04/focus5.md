# 5. BERT 與預訓練方法

## BERT 的創新

2018 年 Google 發布 BERT（Bidirectional Encoder Representations from Transformers），在 NLP 領域掀起革命。BERT 的核心創新在於雙向 Transformer 編碼器與掩碼語言模型訓練目標。

傳統的語言模型只能單向學習（左到右或右到左），而 BERT 同時利用左右上下文。這種「雙向性」使得 BERT 能夠更全面地理解語義，特別適合需要完整語境理解的任務。

## 掩碼語言模型

BERT 的預訓練使用兩種任務：

1. **掩碼語言模型（MLM）**：隨機遮蓋輸入中 15% 的單詞，訓練模型預測被遮蓋的詞。這允許雙向學習。

2. **下一句預測（NSP）**：訓練模型判斷兩個句子是否連續出現。這幫助模型理解句子間的關係，對問答等任務有幫助。

## BERT 的應用

BERT 在多個 NLP 任務上取得突破：

- 文字分類
- 命名實體識別
- 問答系統
- 自然語言推論
- 句子相似度判斷

微調 BERT 通常只需要：
1. 在 BERT 輸出上添加分類層
2. 在任務資料上進行少量 epoch 的訓練
3. 整個模型（包括 BERT）一起訓練

## RoBERTa 與後續改進

Facebook 的 RoBERTa 對 BERT 進行了多項改進：
- 使用更多訓練資料與更長訓練時間
- 移除 NSP 任務（發現對效能影響不大）
- 使用更大的批次大小
- 動態遮蓋策略

這些改進使 RoBERTa 在多個基準測試上超越 BERT。

## ALBERT 的引數共享

Google 的 ALBERT（ALite BERT）透過跨層引數共享與句子順序預測（SOP）任務，大幅減少模型參數量的同時保持性能。這種效率改進對部署大型模型有重要意義。

## 參考資源

- https://www.google.com/search?q=BERT+Google+pre-training+masked+language+model+bidirectional+2018
- https://www.google.com/search?q=RoBERTa+ALBERT+BERT+improvements+comparisons+NLP+2019
- https://www.google.com/search?q=BERT+fine-tuning+text+classification+question+answering+applications