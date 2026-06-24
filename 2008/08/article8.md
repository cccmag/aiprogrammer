# 推薦系統的效能調優

## 向量索引

```python
# 使用 FAISS 加速相似性搜尋
import faiss
index = faiss.IndexFlatL2(128)
index.add(vectors)
D, I = index.search(query_vector, k=10)
```

## 結論

效能優化使即時推薦成為可能。

---

**延伸閱讀**

- [Recommender+system+scalability](https://www.google.com/search?q=recommender+system+scalability)