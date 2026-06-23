# 多模態 RAG（2023-2026）

## 從文字 RAG 到多模態 RAG

RAG 已成 LLM 應用的標準，但傳統 RAG 只能處理文字。多模態 RAG 的目標：**讓檢索系統理解並搜尋所有模態的內容**。

## 多模態 RAG 的三種策略

### 策略一：單一模態索引（先轉文字再搜）

最簡單的方案：非文字內容先轉成文字描述，再用傳統文字 RAG：

```python
def rag_naive(query, docs):
    """非文字 → 文字描述 → 文字 RAG"""
    chunks = []
    for doc in docs:
        if doc.type == "image":
            chunks.append(vlm_caption(doc.image))
        elif doc.type == "audio":
            chunks.append(whisper_transcribe(doc.audio))
        else:
            chunks.append(doc.text)
    return llm(query + "\n".join(chunks))
```

### 策略二：多模態嵌入（統一向量空間）

用 CLIP/ImageBind 直接把所有內容嵌入同一空間：

所有模態直接用 CLIP/ImageBind 嵌入同一向量空間，無需文字轉換：

```python
class VectorIndex:
    def __init__(self, embedder):
        self.embedder = embedder
        self.store = []  # (vector, content, modality)
    
    def search(self, query, k=5):
        qv = self.embedder.embed(query, "text")
        scored = [(c, m, cosine_similarity(qv, v))
                  for v, c, m in self.store]
        scored.sort(key=lambda x: -x[2])
        return scored[:k]
```

### 策略三：分層檢索（先粗篩再細看）

快速嵌入檢索大量候選後，用 VLM 精確判斷相關性：

```python
def hierarchical_retrieve(query, docs, k_rough=50, k_fine=5):
    qv = fast_embed(query)
    cand = sorted([(cosine_similarity(qv, d.vec), d) 
                   for d in docs], reverse=True)[:k_rough]
    scored = sorted([(vlm_relevance(query, d), d) 
                     for _, d in cand], reverse=True)
    return scored[:k_fine]
```

## 多模態 RAG 的應用場景

| 場景 | 輸入 | 檢索目標 | 範例 |
|------|------|---------|------|
| 圖表分析 | 文字問題 | 圖表圖片 | 「Q3 營收趨勢為何？」 |
| 文件問答 | PDF 圖片 | 掃描文件 | 合約條款檢索 |
| 教學助理 | 課本圖片 | 相關教材 | 教科書圖文對照 |
| 影片搜尋 | 文字描述 | 影片片段 | 「找到示範程式碼的片段」 |

## 技術挑戰

| 挑戰 | 說明 |
|------|------|
| 模態遺失 | 嵌入時損失細節（如圖表精確數字） |
| 檢索偏差 | 某些模態在向量空間中過度密集 |
| 延遲問題 | VLM 精確檢索成本高 |
| 評估困難 | 缺乏標準的多模態檢索評測集 |

## 未來方向

| 年份 | 發展 |
|------|------|
| 2023 | 文字 RAG 成熟，多模態 RAG 萌芽 |
| 2024 | 多模態嵌入 + 文字 RAG 混和 |
| 2025 | 分層檢索、多模態重新排名 |
| 2026 | 端到端多模態檢索生成、即時多模態搜尋 |

## 小結

多模態 RAG 是讓 AI 應用處理真實世界資料的關鍵技術。策略從文字化轉換到統一向量空間，再到分層精確檢索。選擇取決於應用對延遲、精確度和模態多樣性的需求。

---

**下一步**：[影像生成與編輯技術](focus6.md)

## 延伸閱讀

- [Retrieval-Augmented Generation Survey](https://www.google.com/search?q=Retrieval+Augmented+Generation+survey+paper)
- [Multimodal RAG 架構](https://www.google.com/search?q=multimodal+RAG+architecture+retrieval+augmented+generation)
- [ColPali: 多模態檢索](https://www.google.com/search?q=ColPali+Efficient+Document+Retrieval+with+Vision+Language+Models)
