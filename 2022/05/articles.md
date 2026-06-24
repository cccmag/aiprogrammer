# 文章集錦

## 大規模語言模型專輯

### 程式相關（5 篇）

#### 1. [詞袋模型與 TF-IDF](article1.md)

從最基礎的文本表示方法開始，介紹詞袋模型（Bag-of-Words）和 TF-IDF 的概念與實作。包含完整的 Python 程式碼範例，展示如何將文本轉換為數值向量，以及如何計算詞頻和逆文檔頻率。

#### 2. [Word2vec Skip-gram 實作](article2.md)

深入 Word2vec 的 Skip-gram 架構，從零使用 NumPy 實作訓練過程。詳細解釋負採樣、學習率和詞向量的可視化。附有完整的 Python 程式碼和實驗結果。

#### 3. [GloVe 與 FastText](article3.md)

比較三種主流的詞嵌入方法：Word2vec、GloVe 和 FastText。GloVe 利用全局共現統計，FastText 處理子詞資訊。包含各方法的優缺點分析和使用建議。

#### 4. [RNN 語言模型實戰](article4.md)

使用 PyTorch 實作一個完整的 RNN 語言模型，包括資料處理、模型定義、訓練循環和文本生成。包含字級和詞級語言模型的對比實驗。

#### 5. [LSTM 文本生成](article5.md)

以金庸小說為訓練資料，使用 LSTM 訓練文本生成模型。涵蓋中文分詞、字元編碼、溫度參數調整等實戰問題。

### AI 相關（5 篇）

#### 6. [Beam Search 解碼](article6.md)

深入介紹 Beam Search 解碼演算法，包括貪婪解碼、Beam Search、Top-k 採樣和 Top-p（nucleus）採樣的對比。包含 Python 實作和可視化分析。

#### 7. [BERT 微調分類任務](article7.md)

使用 Hugging Face Transformers 對 BERT 進行微調，以情感分析為例展示完整的微調流程。包含資料準備、模型載入、訓練和評估的逐步指南。

#### 8. [GPT 提示工程](article8.md)

介紹提示工程（Prompt Engineering）的核心技術，包括角色設定、思維鏈提示、few-shot 學習和提示模板的最佳化技巧。

#### 9. [語言模型評估：困惑度](article9.md)

深入探討語言模型的各種評估方法。困惑度、BLEU、ROUGE 等指標的計算方式和適用場景，以及人類評估的重要性。

#### 10. [從語言模型到對話 AI](article10.md)

回顧從語言模型到現代對話 AI 的發展歷程，涵蓋 Eliza、Seq2Seq 聊天機器人、GPT 驅動的對話系統和 RLHF 技術。
