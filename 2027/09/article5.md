# RAG 資料管線設計與最佳化

## 1. RAG 系統的資料挑戰

RAG（Retrieval-Augmented Generation）是 2025-2026 年最受歡迎的 LLM 應用模式。但在實務中，許多 RAG 系統表現不佳，原因往往不是 LLM 不夠強，而是**資料管線的品質出了問題**。髒資料進，髒結果出——這句話在 RAG 系統中格外真實。

## 2. RAG 資料管線架構

一個完整的 RAG 資料管線包含以下階段：

```
原始資料 → 清理 → 分割 → 嵌入 → 索引 → 持續更新
```

### 2.1 資料清理

資料清理是最容易被忽略但最重要的環節：

```python
import re

def clean_document(text):
    # 移除 HTML 標籤
    text = re.sub(r'<[^>]+>', '', text)
    # 移除過多重複的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 移除空白字元過多的行
    lines = [line.strip() for line in text.split('\n')
             if line.strip() and len(line.strip()) > 10]
    # 過濾無意義內容
    lines = [line for line in lines
             if not is_boilerplate(line)]
    return '\n'.join(lines)
```

**常見資料問題**：重複文件、過時資訊、格式不一致、廣告/導航等樣板內容。

### 2.2 智慧分割

單純按字元數分割會破壞語義單元。更好的做法是**語義分割**：

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=128,
    separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_documents(documents)
```

**分割策略選擇**：
- 程式碼：按函式/類別分割
- 技術文件：按章節標題分割
- 對話紀錄：按輪次分割
- PDF 報告：按段落分割，保留表格結構

### 2.3 嵌入與元資料

每個 Chunk 應包含豐富的元資料，提升搜尋精確度：

```python
class DocumentChunk:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = {
            "source": metadata.get("source"),
            "page": metadata.get("page"),
            "section": metadata.get("section"),
            "chunk_index": metadata.get("chunk_index"),
            "total_chunks": metadata.get("total_chunks"),
            "title": metadata.get("title"),
            "last_updated": metadata.get("last_updated"),
        }
        self.embedding = embed_model.encode(content)
```

## 3. 進階最佳化技術

### 3.1 HyDE（Hypothetical Document Embedding）

先讓 LLM 根據查詢生成一個「假設文件」，再用這個假設文件進行向量搜尋，可以顯著提升召回率：

```python
def hyde_search(query, llm, retriever, top_k=5):
    prompt = f"根據問題，寫一段包含答案的文字：{query}"
    hypothetical_doc = llm.generate(prompt)
    return retriever.search(hypothetical_doc, top_k)
```

### 3.2 多層級檢索

```
查詢 → 粗篩（向量，Top-100）→ 精篩（重新排序，Top-10）→ LLM 生成
```

每一層使用不同的模型：粗篩用輕量模型（text-embedding-3-small），精篩用 Cross-encoder（BGE ReRanker）。

### 3.3 查詢轉換

將複雜查詢拆解為多個子查詢，分別檢索後合併結果：

```python
def decompose_query(complex_query, llm):
    prompt = f"將以下問題拆解為多個子問題：{complex_query}"
    sub_queries = llm.generate(prompt).split("\n")
    results = []
    for sq in sub_queries:
        results.extend(retriever.search(sq, top_k=5))
    return deduplicate(results)
```

## 4. 監控與評估

RAG 系統需要持續監控以下指標：

```python
def evaluate_rag_pipeline(test_questions, retriever, llm):
    metrics = {
        "context_relevance": [],   # 檢索到的文件與問題的相關性
        "answer_faithfulness": [], # 答案是否基於檢索到的文件
        "answer_relevance": [],    # 答案是否回答問題
    }
    for q in test_questions:
        docs = retriever.search(q)
        answer = llm.generate(q, docs)
        metrics["context_relevance"].append(
            compute_relevance(q, docs)
        )
        metrics["answer_faithfulness"].append(
            check_faithfulness(answer, docs)
        )
    return {k: np.mean(v) for k, v in metrics.items()}
```

RAGAS 框架提供了標準化的 RAG 評估指標，建議整合進 CI/CD 流程。

## 5. 資料更新策略

| 策略 | 適用場景 | 更新頻率 |
|------|---------|---------|
| 全量重建 | 資料規模小，需要高一致性 | 每日/每週 |
| 增量更新 | 持續新增文件 | 即時 |
| 滾動更新 | 大規模索引，分區重建 | 每小時 |
| 雙緩衝 | 需要零停機時間 | 按需 |

## 參考資料

- [RAG 管線設計模式](https://www.google.com/search?q=RAG+pipeline+design+patterns)
- [RAGAS 評估框架](https://www.google.com/search?q=RAGAS+rag+evaluation+framework)
- [LangChain RAG 文件](https://www.google.com/search?q=LangChain+rag+documentation)
