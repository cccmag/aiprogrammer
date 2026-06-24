# 主題總覽：BERT 與預訓練革命

2018 年 10 月，Google 發表了 BERT 模型，這是自然語言處理領域繼 Word2Vec 之後最重要的突破。BERT 採用雙向 Transformer 架構，透過大規模預訓練與任務特定微調，在各項 NLP 基準測試中達到前所未有的準確率。本期將帶領讀者深入了解 BERT 的技術原理與其帶來的典範轉移。

## BERT 的核心創新

傳統的語言模型（如 ELMo）僅使用單向的上下文，要么從左到右，要么從右到左。BERT 的突破在於使用真正的雙向 Transformer encoder，讓每個位置都能夠同時參照左右兩側的上下文資訊。這種雙向性使得 BERT 能夠學習更豐富的語言表示。

BERT 的預訓練採用兩個任務：
1. **Masked Language Model (MLM)**：隨機遮蓋輸入中 15% 的 token，模型需要根據上下文預測被遮蓋的詞
2. **Next Sentence Prediction (NSP)**：判斷兩個句子是否為連續的上下文

這種預訓練方式讓 BERT 學習深層的語義與語法知識，再透過微調應用於各種下游任務。

## 預訓練革命的影響

BERT 的成功催生了一系列預訓練語言模型，如 GPT、RoBERTa、XLNet 等。這些模型奠定了「預訓練 + 微調」範式的地位，大幅降低了 NLP 任務的進入門檻。開發者不再需要從頭訓練模型，只需在大型語料庫上預训练的模型基礎上，針對特定任務進行微調。

## 學習路徑

建議依序閱讀 focus1 到 focus7 了解 BERT 的各個面向，再透過 article1 到 article10 深入實作細節。每篇文章都包含可直接執行的程式碼範例。

## 本期結構

- focus1–7：BERT 與預訓練革命的各個面向
- article1–5：NLP 基礎技術回顧
- article6–10：BERT 實作與應用
- _code/bert_demo.py：BERT 概念示範

## 參考資源

- https://www.google.com/search?q=BERT+pre-training+revolution+NLP+transformer+bidirectional+2018
- https://www.google.com/search?q=BERT+Masked+Language+Model+Next+Sentence+Prediction+pre-training+tasks
- https://www.google.com/search?q=pre-trained+language+models+GPT+ELMo+transfer+learning+NLP