# GloVe 與 FastText

## 三種詞嵌入方法的比較

Word2vec、GloVe 和 FastText 是詞嵌入領域的三種主要方法，各有不同的設計理念。

## GloVe：全局向量

GloVe（Global Vectors for Word Representation）由史丹佛大學在 2014 年提出，結合了矩陣分解和局部上下文視窗的優點：

```python
# GloVe 的核心：詞共現矩陣
# 計算每對詞在語料庫中共同出現的次數
cooccur = np.zeros((vocab_size, vocab_size))
for i in range(len(corpus)):
    for j in range(max(0, i-window), min(len(corpus), i+window+1)):
        if i != j:
            cooccur[corpus[i], corpus[j]] += 1
```

**損失函數**：

```
J = sum(f(X_ij) * (w_i^T * w_j + b_i + b_j - log(X_ij))^2)
```

其中 X_ij 是詞 i 和詞 j 的共現次數，f 是加權函數（限制高頻詞的權重）。

**關鍵洞察**：詞向量之間的比例（而非共現次數本身）編碼了語義。例如：

```
P(ice|solid) / P(steam|solid) 很大  → solid 與 ice 更相關
P(ice|gas)   / P(steam|gas)   很小  → gas 與 steam 更相關
P(ice|water) / P(steam|water)  ≈ 1  → water 與兩者都相關
```

## FastText：子詞資訊

FastText 由 Facebook AI Research 在 2017 年提出，核心創新是**子詞（subword）n-gram**：

```python
# FastText 將每個詞分解為字元 n-gram
word = "apple"
n = 3  # 3-gram
subwords = ["<ap", "app", "ppl", "ple", "le>"]
# 詞的向量 = 所有子詞向量的和
```

**優勢**：

1. **處理未登錄詞**（OOV）：即使詞不在詞彙表中，仍可根據子詞推斷其向量
2. **捕捉詞形變化**：「run」「runs」「running」共享大部分子詞
3. **拼寫相似性**：「經濟」和「經紀」因共享子詞而向量相近

## 對比分析

| 特性 | Word2vec | GloVe | FastText |
|------|----------|-------|----------|
| 核心方法 | 局部預測 | 全局統計 | 局部預測 + 子詞 |
| 資訊來源 | 上下文視窗 | 共現矩陣 | 上下文視窗 |
| OOV 處理 | ❌ | ❌ | ✅ |
| 子詞資訊 | ❌ | ❌ | ✅ |
| 訓練速度 | 快 | 中 | 中 |
| 大語料表現 | 優秀 | 優秀 | 優秀 |

## 使用建議

```python
# Gensim 實作範例
from gensim.models import KeyedVectors, FastText
from gensim.models.word2vec import Word2Vec

# Word2Vec
model_w2v = Word2Vec(sentences, vector_size=100, window=5, sg=1)
# sg=1 表示 Skip-gram, sg=0 表示 CBOW

# FastText（支援 OOV）
model_ft = FastText(sentences, vector_size=100, window=5, sg=1)
vector_oov = model_ft.wv["未登錄詞"]

# GloVe 需要先計算共現矩陣再訓練
```

## 延伸閱讀

- [GloVe 原始論文](https://www.google.com/search?q=GloVe+Global+Vectors+for+Word+Representation)
- [FastText 論文](https://www.google.com/search?q=FastText+Enriching+Word+Vectors+with+Subword+Information)
- [Gensim 詞嵌入教學](https://www.google.com/search?q=gensim+word+embeddings+tutorial)
