# Word2Vec 與 GloVe 比較

## Word2Vec 原理

Google 2013 年發表的 Word2Vec 包含兩種訓練演算法：

### Skip-gram
輸入中心詞，輸出預測周圍詞的機率。
適用於小型語料庫，對稀有詞效果較好。

目標函數：
```
max Σ log P(context | center_word)
```

### CBOW（Continuous Bag of Words）
輸入周圍詞，輸出預測中心詞的機率。
訓練速度較快，對常見詞效果較好。

## Word2Vec 的加速技巧

### 層次 Softmax
使用霍夫曼編碼樹，減少輸出層的計算複雜度：
- 從 O(V) 降到 O(log V)
- V 為詞彙表大小

### 負採樣（Negative Sampling）
只更新少數負樣本：
- 正樣本：實際的上下文詞
- 負樣本：隨機選擇的詞
- 將多分類問題轉為二元分類

## GloVe 原理

Stanford 2014 年發表的 GloVe 結合了：
- 全局詞共現統計
- 局部上下文方法

損失函數：
```
J = Σ f(X_ij)(w_i · w_j + b_i + b_j - log(X_ij))^2
```
- X_ij：詞 i 在詞 j 上下文中出現的次數
- f：加權函數，避免過度強調常見詞

## 比較

| 特性 | Word2Vec | GloVe |
|------|----------|-------|
| 訓練目標 | 預測周圍詞 | 重構共現機率 |
| 使用資訊 | 局部上下文 | 全局統計 |
| 訓練速度 | 快 | 中等 |
| 記憶體需求 | 低 | 中等 |
| 類比推理 | 優秀 | 優秀 |
| 共現任務 | 一般 | 優秀 |

## 實際選擇

兩種方法在多數任務上表現相近：
- Word2Vec 訓練速度快，適合快速原型
- GloVe 提供預訓練模型，直接下載使用
- 建議兩種都嘗試，選擇效果較好的

## 使用範例

```python
# Gensim Word2Vec
from gensim.models import Word2Vec
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# Gensim 可以載入 GloVe 格式
from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format('glove.txt', binary=False)
```

## 參考資源

- https://www.google.com/search?q=Word2Vec+skip-gram+CBOW+負採樣+層次softmax+原理+詳解
- https://www.google.com/search?q=GloVe+詞向量+共現矩陣+損失函數+原理
- https://www.google.com/search?q=Word2Vec+vs+GloVe+比较+优缺点+选择+使用