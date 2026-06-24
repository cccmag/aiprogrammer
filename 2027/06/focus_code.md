# 程式實作：迷你 Transformer 與 RAG 系統

## 簡介

本實作從零建構一個迷你 Transformer 語言模型和 RAG（檢索增強生成）系統，幫助理解 LLM 的核心運作原理。完整程式碼在 `_code/transformer.py` 和 `_code/rag.py`。

## 迷你 Transformer

### 1. 多頭注意力

Scaled Dot-Product Attention 是 Transformer 的核心：

```python
scores = Q @ K.T / sqrt(d_k)
attention = softmax(scores) @ V
```

多頭注意力將輸入投影到 `n_heads` 組 Q、K、V：

```python
class MultiHeadAttention:
    def forward(self, x, mask=None):
        Q = x @ self.W_q  # 投影
        K = x @ self.W_k
        V = x @ self.W_v
        # 分割為多頭
        Q = Q.reshape(seq_len, n_heads, d_k).transpose(1, 0, 2)
        # Scaled dot-product
        scores = Q @ K.transpose(0, 2, 1) / sqrt(d_k)
        # 遮罩（因果）
        if mask is not None:
            scores = scores + mask
        attn = softmax(scores)
        return (attn @ V).transpose(1, 0, 2).reshape(seq_len, d_model) @ W_o
```

### 2. Transformer 區塊

每個區塊包含：注意力 → 殘差連接 → LayerNorm → FFN → 殘差連接 → LayerNorm

```python
class TransformerBlock:
    def forward(self, x, mask=None):
        x = x + self.attention.forward(self.norm1.forward(x), mask)
        x = x + self.ffn.forward(self.norm2.forward(x))
        return x
```

### 3. 位置編碼

使用正弦餘弦函數編碼位置資訊：

```python
def sinusoidal_encoding(seq_len, d_model):
    pos = np.arange(seq_len)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / d_model)
    pe[:, 0::2] = np.sin(pos * angle_rates[:, 0::2])
    pe[:, 1::2] = np.cos(pos * angle_rates[:, 1::2])
```

### 4. 訓練與生成

使用字元級詞彙表在小型語料庫上訓練：

```
step   0, loss = 3.46
step 200, loss = 2.60
```

## RAG 系統

### 1. 嵌入與向量儲存

將文檔轉換為向量，用餘弦相似度檢索：

```python
class VectorStore:
    def search(self, query_vector, k=3):
        scores = normalized_vectors @ normalized_query
        return top_k_documents
```

### 2. RAG 查詢流程

```
使用者提問 → 嵌入查詢 → 向量資料庫檢索 → 
擷取相關文檔 → 加入提示詞 → 生成回覆
```

## 執行方式

```bash
cd _code
python3 transformer.py    # 迷你 Transformer 訓練與生成
python3 rag.py            # RAG 檢索示範
```

## 延伸練習

1. **完整訓練**：使用更大語料庫（如 Shakespeare）訓練 Transformer
2. **真正嵌入**：使用 `sentence-transformers` 替換隨機嵌入
3. **LLM API 整合**：串接 OpenAI/Claude API 作為生成器
4. **多輪對話**：加入對話歷史管理
5. **評估指標**：實作 MRR、NDCG 等檢索評估指標
