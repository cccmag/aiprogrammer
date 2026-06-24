# 程式實作：從零實作向量資料庫

## 簡介

本實作從零建構一個迷你向量資料庫，包含向量索引、相似度搜尋、HNSW 近似最近鄰搜尋、元資料過濾和 RAG 整合。完整程式碼在 `_code/vector_db.py`。

## 核心元件

### 1. 向量索引（FlatIndex）

暴力搜尋作為基準線：

```python
index = FlatIndex()
index.add(Document(id="d1", text="...", vector=[...], metadata={...}))
results = index.search(query_vector, k=5, filter_fn=tag_filter(["ai"]))
```

### 2. HNSW 索引（簡化版）

分層可導航小世界圖，提供 O(log N) 搜尋：

```python
hnsw = HNSWIndex(m=3, m_max=5)
hnsw.add(doc)
results = hnsw.search(query_vector, k=3)
```

### 3. 相似度計算

使用 cosine_similarity，支援自訂距離函數：

```python
sim = cosine_similarity(vector_a, vector_b)
```

### 4. 元資料過濾

支援標籤過濾和日期範圍過濾：

```python
results = index.search(q_vec, k=3, filter_fn=tag_filter(["ai", "nlp"]))
```

## 執行方式

```bash
cd _code
python3 vector_db.py
```

## 延伸練習

1. **加入真實嵌入模型**：用 `sentence-transformers` 替換 SimpleEmbedder
2. **實作 IVF**：倒排檔案索引分桶搜尋
3. **持久化儲存**：將向量索引儲存到 SQLite
4. **RAG 管線**：結合 LLM API 實作完整的問答系統
5. **效能基準測試**：比較 FlatIndex 和 HNSW 在不同資料量下的速度
