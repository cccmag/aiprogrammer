# 1. BERT 誕生背景

## 從詞嵌入到預訓練

在 BERT 之前，NLP 領域經歷了漫長的發展歷程。2013 年 Word2Vec 的出現讓「詞嵌入」概念普及，透過神經網路學習詞彙的向量表示，使語義相似的詞在向量空間中彼此接近。隨後 GloVe、FastText 等方法相繼問世，持續改進詞嵌入的品質。

然而，詞嵌入存在根本限制：每個詞只對應一個固定的向量，無法處理一詞多義。例如「bank」可以指銀行或河岸，但在傳統詞嵌入中只有一個表示。這個問題促使研究者探索更動態、更深層的語言表示方式。

## ELMo 的啟示

2018 年初，Peters 等人發表 ELMo（Embeddings from Language Models），採用雙向 LSTM 架構。ELMo 的創新在於使用語言模型任務進行預訓練，讓每個詞的表示可以根據上下文動態調整。ELMo 在多項 NLP 任務上取得顯著改進，驗證了預訓練方法的有效性。

但 ELMo 仍有局限：它使用 LSTM 而非當時最新的 Transformer 架構，且採用淺層的雙向組合，無法充分捕捉深層語義。

## Transformer 的崛起

2017 年，Google 發表「Attention is All You Need」論文，提出 Transformer 架構，完全使用注意力機制取代傳統的 RNN。Transformer 的優勢在於：
- **平行計算**：不受序列依賴限制，可大幅加速訓練
- **長距離依賴**：注意力機制直接建模任意距離的關係
- **可擴展性**：易於擴展到更大的模型與資料集

這些特性使 Transformer 成為大規模預訓練模型的理想基礎。

## BERT 的誕生

2018 年 10 月，Google 發表 BERT，結合了預訓練語言模型的思想與 Transformer encoder 架構。BERT 的名稱正是「Bidirectional Encoder Representations from Transformers」的縮寫，強調其雙向性與基於 Transformer 的特性。

BERT 在 SQuAD、GLUE、MultiNLI 等 11 項 NLP 基準測試中創下新紀錄，有些甚至超越人類表現。這個成功關鍵在於：
1. 真正的雙向 Transformer encoder
2. 大規模預訓練（BooksCorpus 與 English Wikipedia）
3. 簡單有效的微調策略

## 參考資源

- https://www.google.com/search?q=BERT+origin+history+pre-trained+language+models+ELMo+Word2Vec+background
- https://www.google.com/search?q=ELMo+bidirectional+LSTM+language+model+Peters+2018
- https://www.google.com/search?q=Transformer+attention+mechanism+RNN+replacement+2017+Google