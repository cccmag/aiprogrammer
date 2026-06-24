# RAG 整合設計模式

## 前言

檢索增強生成（Retrieval-Augmented Generation, RAG）是解決 LLM 知識不足和幻覺問題的關鍵技術。本文介紹 RAG 系統的設計模式與實作。

## 基礎 RAG Pipeline

```python
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Document:
    content: str
    metadata: dict
    embedding: List[float]

class EmbeddingService:
    async def embed(self, text: str) -> List[float]:
        response = await call_llm_embedding(text)
        return response

class VectorStore:
    def __init__(self):
        self.documents: List[Document] = []

    def add(self, doc: Document):
        self.documents.append(doc)

    async def search(self, query_embedding: List[float], k: int = 3) -> List[Document]:
        scores = [
            self.cosine_similarity(query_embedding, doc.embedding)
            for doc in self.documents
        ]
        top_indices = np.argsort(scores)[-k:][::-1]
        return [self.documents[i] for i in top_indices]

    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class RAGEngine:
    def __init__(self, embedder: EmbeddingService, store: VectorStore):
        self.embedder = embedder
        self.store = store

    async def query(self, question: str) -> str:
        query_embedding = await self.embedder.embed(question)
        docs = await self.store.search(query_embedding)
        context = "\n\n".join(d.content for d in docs)
        prompt = f"根據以下資料回答問題：\n\n{context}\n\n問題：{question}"
        return await call_llm(prompt)
```

## 進階：Hybrid Search

結合關鍵字與向量搜尋提升召回率：

```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.bm25 = None

    def build_bm25(self, documents: List[Document]):
        tokenized = [doc.content.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    async def hybrid_search(self, query: str, k: int = 3, alpha: float = 0.5) -> List[Document]:
        query_embedding = await self.embedder.embed(query)
        vector_results = await self.vector_store.search(query_embedding, k * 2)

        query_tokens = query.split()
        bm25_scores = self.bm25.get_scores(query_tokens)
        bm25_indices = np.argsort(bm25_scores)[-k * 2:][::-1]

        combined = {}
        for i, doc in enumerate(vector_results):
            combined[id(doc)] = combined.get(id(doc), 0) + alpha * (1 - i / (k * 2))
        for i, idx in enumerate(bm25_indices):
            doc = self.vector_store.documents[idx]
            combined[id(doc)] = combined.get(id(doc), 0) + (1 - alpha) * (1 - i / (k * 2))

        sorted_docs = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return [doc for doc_id, _ in sorted_docs[:k]]
```

## Chunking 策略

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", "。", "，", " ", ""]
        )

    def chunk(self, text: str, source: str) -> List[Document]:
        chunks = self.splitter.split_text(text)
        return [
            Document(content=chunk, metadata={"source": source}, embedding=[])
            for chunk in chunks
        ]
```

## 結語

RAG 的品質取決於嵌入模型、向量檢索、分塊策略和提示詞設計。Hybrid Search 和適當的 Chunking 能顯著提升回答準確度。

---

**延伸閱讀**

- [RAG 技術綜述](https://www.google.com/search?q=RAG+retrieval+augmented+generation+survey)
- [向量資料庫比較](https://www.google.com/search?q=vector+database+comparison+2026)
- [Hybrid Search 實作](https://www.google.com/search?q=hybrid+search+BM25+vector+embeddings)
