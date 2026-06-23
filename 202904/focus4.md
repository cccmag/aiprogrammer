# 多模態記憶與檢索（2025-2029）

## 為何需要多模態記憶

傳統 Agent 只記住文字對話歷史。多模態 Agent 需要記住「看過的圖片」、「聽過的語音」、「做過的動作」，並在未來決策時檢索這些記憶。舉例來說，使用者在星期一上傳了一張電路圖，星期五問「上次那張圖的電阻值是多少？」——Agent 必須能跨模態、跨時間檢索。

## 多模態 Embedding

將不同模態的資料映射到同一向量空間是核心技術。CLIP、ImageBind、LanguageBind 等模型讓文字與圖像共用 embedding 空間：

```python
from sentence_transformers import SentenceTransformer

class MultimodalEmbedding:
    def __init__(self):
        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text):
        return self.text_model.encode(text)

    def embed_image(self, image_tensor):
        # 使用 CLIP 或其他多模態編碼器
        pass
```

## 多模態 RAG（MRAG）

2025 年提出的多模態檢索增強生成，讓 Agent 能從知識庫中同時檢索文字與圖像。檢索結果包含圖片與文字片段，LLM 根據兩者生成回答。

```python
import chromadb

class MultimodalMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient()
        self.collection = self.client.create_collection("memory")

    def store(self, text, image_embedding, metadata):
        self.collection.add(
            embeddings=[image_embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[metadata["id"]]
        )

    def retrieve(self, query_embedding, top_k=5):
        return self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
```

## 記憶的三大類型

1. **短期記憶**：當前對話中的多模態上下文，儲存在 sliding window 內
2. **長期記憶**：跨對話的多模態經驗，儲存在向量資料庫中
3. **情景記憶**：特定場景下的多模態知識，如產品使用手冊的圖文對照

## 2026 年的突破：跨模態關聯

Google Gemini 1.5 和 GPT-4o 實現了「看圖→聽解說→文字回答」的跨模態推理。記憶不再只是同模態間的檢索，而是異模態間的聯想，例如用語音查詢來搜尋相關圖片。

## 挑戰與展望

多模態 embedding 的對齊品質直接影響檢索準確度；影片記憶的儲存成本仍然高昂；遺忘機制與重要性排序需要更先進的演算法。2027 年後預計出現專為多模態設計的記憶資料庫。

## 參考資源

- https://www.google.com/search?q=multimodal+RAG+retrieval+augmented+generation+2025
- https://www.google.com/search?q=CLIP+multimodal+embedding+memory
- https://www.google.com/search?q=ImageBind+multimodal+retrieval
