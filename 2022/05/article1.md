# 詞袋模型與 TF-IDF

## 文本的數值化表示

在機器學習處理文本之前，必須將文字轉換為數值向量。詞袋模型（Bag-of-Words, BoW）是最基礎的文本表示方法。

## 詞袋模型

BoW 的直覺很簡單：建立一個詞彙表，忽略詞序，只統計每個詞的出現次數：

```python
from collections import Counter

def bow_vectorize(document, vocabulary):
    vec = [0] * len(vocabulary)
    words = document.split()
    for word in words:
        if word in vocabulary:
            idx = vocabulary[word]
            vec[idx] += 1
    return vec

corpus = ["the cat sat on the mat",
          "the dog sat on the log"]
vocab = {w: i for i, w in enumerate(set(" ".join(corpus).split()))}

for doc in corpus:
    print(bow_vectorize(doc, vocab))
```

**優點**：簡單直觀，計算快速。

**缺點**：
- 稀疏性：向量長度等於詞彙量（數萬維），大部分為 0
- 忽略詞序：無法捕捉「貓追狗」和「狗追貓」的差異
- 未考慮詞的區分能力：高頻的「的」「是」等停用詞帶來大量噪音

## TF-IDF

TF-IDF（Term Frequency-Inverse Document Frequency）改進了 BoW，降低高頻詞的權重，提升低頻但重要詞的權重：

```
TF(t, d) = 詞 t 在文檔 d 中出現的次數 / 文檔 d 的總詞數
IDF(t) = log(總文檔數 / 包含詞 t 的文檔數)
TF-IDF(t, d) = TF(t, d) * IDF(t)
```

```python
import math

def tf(word, document):
    words = document.split()
    return words.count(word) / len(words)

def idf(word, corpus):
    doc_count = sum(1 for doc in corpus if word in doc.split())
    return math.log(len(corpus) / (doc_count + 1))

def tfidf(word, document, corpus):
    return tf(word, document) * idf(word, corpus)
```

## 實作範例

```python
corpus = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "cats and dogs are pets"
]
"""
TF-IDF 的直覺：
- "cat" 只在文檔 1 中出現 → IDF高 → 重要
- "the" 在所有文檔中出現  → IDF低 → 不重要
- "mat" 只在文檔 1 中出現 → 雖然 IDF高但 TF低
"""
```

## 應用場景

BoW 和 TF-IDF 雖然簡單，但在以下場景中仍然有效：

1. **文本分類**：垃圾郵件偵測、新聞分類
2. **資訊檢索**：搜索引擎的文件排序
3. **主題建模**：LDA 的輸入特徵
4. **文檔相似度**：計算兩篇文章的餘弦相似度

## 局限與改進

TF-IDF 的主要局限在於無法捕捉語義和上下文。例如，「車」和「汽車」在不同文檔中使用時無法被理解為相關詞。這需要下一篇文章中介紹的詞嵌入方法來解決。

## 延伸閱讀

- [TF-IDF 維基百科](https://www.google.com/search?q=TF-IDF+wikipedia)
- [Scikit-learn 文本特徵提取](https://www.google.com/search?q=scikit+learn+text+feature+extraction)
