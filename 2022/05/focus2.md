# Word2vec 與詞嵌入

## 詞嵌入的革命

Word2vec 由 Mikolov 在 2013 年提出，是自然語言處理領域最重要的突破之一。它的核心思想是：**一個詞的意義由其上下文決定**（「You shall know a word by the company it keeps」）。

Word2vec 將每個詞映射到一個低維稠密向量（通常 100-300 維），使得語義相近的詞在向量空間中彼此靠近。

## 兩種架構

### CBOW（Continuous Bag-of-Words）

CBOW 使用上下文詞來預測目標詞：

```
上下文：["the", "cat", "on", "the"] → 目標："sat"
```

訓練過程：
1. 對上下文詞向量取平均
2. 透過權重矩陣投影到詞彙空間
3. softmax 計算目標詞的機率
4. 反向傳播更新詞向量

### Skip-gram

Skip-gram 與 CBOW 相反，使用目標詞來預測上下文詞：

```
目標："sat" → 上下文：["the", "cat", "on", "the"]
```

Skip-gram 在稀有詞上的表現更好，因為每個詞會產生更多的訓練樣本。

## Word2vec 的驚人特性

訓練完成的詞向量展現了令人驚嘆的語義和語法規律性：

```
vector("king") - vector("man") + vector("woman") ≈ vector("queen")
vector("Paris") - vector("France") + vector("Italy") ≈ vector("Rome")
vector("walking") - vector("walk") + vector("swim") ≈ vector("swimming")
```

這種類比能力證明詞向量不僅捕捉了詞義，還編碼了詞之間的關係。

## 實作要點

```python
# Word2Vec Skip-gram 的負採樣變體
# 不使用完整的 softmax（計算成本太高）
# 而是將任務轉換為二分類：判斷 (目標詞, 上下文詞) 是否為正樣本

def skipgram_loss(target, context, noise_words):
    # 正樣本：讓 (target, context) 的相似度盡量大
    pos_score = dot(target, context)
    # 負樣本：讓 (target, noise_word) 的相似度盡量小
    neg_scores = sum(dot(target, noise))
    return -log(sigmoid(pos_score)) - sum(log(sigmoid(-neg_scores)))
```

**負採樣**（Negative Sampling）是 Word2vec 的關鍵技巧，每次只更新 k 個負樣本的權重，大幅降低了計算複雜度。

## 影響與局限

Word2vec 的革命性影響：
- 詞嵌入成為 NLP 的標準預處理步驟
- 為後續的上下文編碼模型（ELMo、BERT）鋪平了道路

主要局限：
- 靜態向量：每個詞只有一個固定表示，無法處理一詞多義
- 僅利用局部上下文，忽略了全局統計資訊

---

**下一步**：[RNN 語言模型](focus3.md)

## 延伸閱讀

- [Word2Vec 原始論文](https://www.google.com/search?q=Efficient+Estimation+of+Word+Representations+in+Vector+Space)
- [Word2Vec 參數詳解](https://www.google.com/search?q=word2vec+parameters+explained)
- [詞向量類比範例](https://www.google.com/search?q=word+embeddings+analogy+examples)
