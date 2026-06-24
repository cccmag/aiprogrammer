# 嵌入模型比較：text-embedding-3 到 BGE

## 1. 嵌入模型的重要性

向量搜尋的品質 90% 取決於嵌入模型的品質。一個好的嵌入模型能將語義相似的文件映射到相近的向量空間，而差的模型則會讓語義相關的內容相距甚遠。本文從實戰角度比較目前主流的嵌入模型。

## 2. OpenAI text-embedding-3 系列

OpenAI 在 2024 年推出了 text-embedding-3 系列，是目前使用最廣泛的商業嵌入模型。

| 模型 | 維度 | 最大 Token | 特性 |
|------|------|-----------|------|
| text-embedding-3-small | 1536 | 8191 | 成本低，性價比高 |
| text-embedding-3-large | 3072 | 8191 | 高精度，可降維 |

text-embedding-3 支援 **降維**（Matryoshka Representation Learning），無需重新訓練即可縮減向量維度：

```python
from openai import OpenAI

client = OpenAI()

# 完整 3072 維
resp = client.embeddings.create(
    model="text-embedding-3-large",
    input="AI 原生資料庫的未來"
)
full_vec = resp.data[0].embedding  # 3072 維

# 降維到 256 維，速度更快、儲存更少
resp = client.embeddings.create(
    model="text-embedding-3-large",
    input="AI 原生資料庫的未來",
    dimensions=256
)
small_vec = resp.data[0].embedding  # 256 維
```

降維到 256 維仍能保留約 95% 的檢索效能，但儲存空間僅為原來的 1/12。

## 3. BGE（BAAI General Embedding）

BGE 是由北京智源研究院（BAAI）開發的開源嵌入模型系列，在 MTEB（Massive Text Embedding Benchmark）榜單上長期名列前茅。

```python
from sentence_transformers import SentenceTransformer

# BGE 多語言模型（支援繁體中文）
model = SentenceTransformer("BAAI/bge-m3")

# 支援密集向量與稀疏向量
docs = ["AI 原生資料庫改變了資料管理的方式",
        "向量搜尋是 RAG 系統的核心"]

dense_vecs = model.encode(docs)  # 1024 維密集向量
sparse_vecs = model.encode(docs, return_sparse=True)  # 稀疏向量
```

BGE-M3 的特色是**多語言**、**多粒度**（詞級到文件級）和**多功能**（密集+稀疏+ColBERT 式互動編碼）。

## 4. 其他重要嵌入模型

### Cohere Embed v3
```python
import cohere
co = cohere.Client()
resp = co.embed(texts=["..."], model="embed-english-v3.0",
                input_type="search_query")
```

支援三種 input_type（search_query、search_document、classification），針對不同任務最佳化。

### Jina Embeddings v2
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("jinaai/jina-embeddings-v2-base-zh")
vec = model.encode("支援中文的嵌入模型")
```

支援 8192 Token 長文本，適合處理完整文件而非短句。

### e5-mistral-7b-instruct
微軟基於 Mistral 7B 的嵌入模型，目前是 MTEB 排行榜的頂尖模型，但需要較多 GPU 記憶體。

## 5. MTEB 評測結果（BEIR 子集）

| 模型 | NDCG@10 | 維度 | 開源 | 多語言 |
|------|---------|------|------|--------|
| text-embedding-3-large | 64.6 | 3072 | 否 | 是 |
| BGE-M3 | 63.8 | 1024 | 是 | 是 |
| Cohere Embed v3 | 63.2 | 1024 | 否 | 否 |
| jina-embeddings-v2 | 61.5 | 768 | 是 | 是 |
| text-embedding-3-small | 62.3 | 1536 | 否 | 是 |

## 6. 實戰選擇指南

- **預算充足、追求最佳效果**：text-embedding-3-large（降維到 512-768 維）
- **需要開源、自建部署**：BGE-M3（最佳開源多語言模型）
- **處理長文本**：Jina Embeddings v2（8K Token 支援）
- **成本敏感**：text-embedding-3-small（價格為 large 的 1/5）
- **需要稀疏向量**：BGE-M3 或 Cohere（支援密集+稀疏混合）

## 7. 模型評估的維度

選擇嵌入模型時應考慮：
1. **領域適應性**：法律、醫療等專業領域可能需要微調
2. **語言支援**：繁體中文的表現因模型差異很大
3. **延遲要求**：大模型推理時間可能相差 10 倍
4. **維度權衡**：高維度提升準確率但增加儲存和搜尋成本

## 參考資料

- [MTEB 排行榜](https://www.google.com/search?q=MTEB+leaderboard+text+embedding)
- [OpenAI Embeddings 文件](https://www.google.com/search?q=openai+text+embedding+3)
- [BGE 模型](https://www.google.com/search?q=BAAI+BGE+embedding+model)
