# 多模態 RAG

## 1. 從文字到多模態

傳統 RAG 只處理文字。多模態 RAG 擴展檢索範圍至圖像、PDF、表格，讓 Agent 能從更多元來源找到資訊。

## 2. 多模態嵌入與索引

```python
from sentence_transformers import SentenceTransformer
from PIL import Image
import chromadb

class MultiIndex:
    def __init__(self):
        self.tmodel = SentenceTransformer("all-MiniLM-L6-v2")
        self.vmodel = SentenceTransformer("clip-ViT-B-32")
        self.db = chromadb.Client().create_collection("rag")

    def add(self, doc_id, text=None, images=None):
        for t in [text] if text else []:
            self.db.add(embeddings=[self.tmodel.encode(t).tolist()], documents=[t], ids=[doc_id+"_t"])
        for img in (images or []):
            emb = self.vmodel.encode(Image.open(img)).tolist()
            self.db.add(embeddings=[emb], documents=[f"[IMG] {img}"], ids=[doc_id+"_v"])
```

## 3. 混合檢索

```python
class HybridRetriever:
    def __init__(self, index):
        self.index = index

    def retrieve(self, query, k=5):
        emb = SentenceTransformer("all-MiniLM-L6-v2").encode(query).tolist()
        return self.index.db.query(query_embeddings=[emb], n_results=k)["documents"][0]
```

## 4. 影像描述作為索引

無法直接向量檢索圖像時，先讓 VLM 生成描述再索引：

```python
def caption_index(vlm, image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    r = vlm.chat.completions.create(model="gpt-4o", messages=[{
        "role": "user", "content": [
            {"type": "text", "text": "詳細描述這張圖"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
        ]}])
    return r.choices[0].message.content
```

## 5. 結語

多模態 RAG 讓 Agent 知識庫從純文字擴展到圖像與表格。2026 年趨勢是端到端多模態檢索模型。

- https://www.google.com/search?q=multimodal+RAG+retrieval+augmented+generation
- https://www.google.com/search?q=CLIP+embedding+multimodal+search
