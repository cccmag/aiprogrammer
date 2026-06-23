# 向量嵌入與語義搜尋（2013-2026）

## 從 Word2Vec 到語義表示

### 嵌入的起源

2013 年 Google 發表 Word2Vec，首次讓文字能以稠密向量表示，且向量之間的距離反映了語義相似度：

```
vector("king") - vector("man") + vector("woman") ≈ vector("queen")
```

這個著名的等式展示了一件事：向量嵌入不僅能表達「相似性」，還能捕捉**語義關係**。

### 嵌入模型的演進

| 年份 | 模型 | 維度 | 特點 |
|------|------|------|------|
| 2013 | Word2Vec | 300 | 靜態詞向量 |
| 2018 | BERT | 768 | 上下文感知 |
| 2020 | Sentence-BERT | 384-768 | 句子層級嵌入 |
| 2022 | text-embedding-ada-002 | 1536 | OpenAI 通用嵌入 |
| 2024 | text-embedding-3-large | 3072 | 多語言、高品質 |
| 2025 | multilingual-e5 | 1024 | 開源高效 |
| 2026 | 原生多模態嵌入 | 2048+ | 文字+圖片+音訊 |

### 相似度度量

選擇哪種度量取決於你的應用場景：

```python
import numpy as np

def cosine_similarity(a, b):
    """餘弦相似度：關注方向，忽略長度（文字嵌入常用）"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
    """歐幾里得距離：關注絕對位置（圖像嵌入常用）"""
    return np.linalg.norm(a - b)

def dot_product(a, b):
    """點積：高效率，但受向量長度影響""""
    return np.dot(a, b)

# 使用範例
embedding_query = np.random.randn(384)  # 假設查詢向量
embedding_doc = np.random.randn(384)    # 假設文件向量

score = cosine_similarity(embedding_query, embedding_doc)
print(f"語義相似度：{score:.4f}")
```

### 多模態嵌入

2022 年 OpenAI 的 CLIP 與 2024 年後的後繼模型，讓同一個向量空間可以容納文字和圖像：

```python
# 多模態搜尋示意
def multimodal_search(text_query, image_query=None):
    if text_query:
        query_emb = text_encoder(text_query)
    elif image_query:
        query_emb = image_encoder(image_query)
    else:
        query_emb = text_encoder("")  # 空查詢
    
    # 在同一向量空間中搜尋
    results = vector_db.query(query_emb)
    return results
```

### 嵌入的實務考量

1. **維度選擇**：高維度（1536+）更精確但儲存成本高；低維度（384）查詢快但可能損失細微語義
2. **正規化**：使用餘弦相似度時，先將向量正規化可將餘弦相似度簡化為點積
3. **批次嵌入**：使用批次 API 可大幅降低 embedding 延遲
4. **快取策略**：頻繁查詢的嵌入應快取，避免重複計算

### 2026 年的嵌入趨勢

2026 年嵌入技術的主要發展方向是**動態嵌入**——同一個詞在不同的上下文中自動調整向量表示，以及**壓縮嵌入**——用 64-128 維的量化嵌入達到接近 768 維的表現。

---

**下一步**：[近似最近鄰搜尋演算法](focus3.md)

## 延伸閱讀

- [Word2Vec 論文解讀](https://www.google.com/search?q=Word2Vec+efficient+estimation+word+representations)
- [Sentence-BERT 嵌入技術](https://www.google.com/search?q=Sentence+BERT+semantic+textual+similarity)
