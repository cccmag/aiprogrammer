# 多跳檢索策略比較

## 前言

多跳檢索（Multi-hop Retrieval）是進階 RAG 的核心能力——當問題需要跨越多個知識片段才能回答時，系統必須能夠「跳躍」到相關但間接的資訊上。本文比較五種主流多跳檢索策略的優劣。

## 策略一：BFS/DFS 圖遍歷

基於知識圖譜的 BFS 或 DFS 遍歷是最直觀的多跳檢索方式。從種子實體出發，逐層探索關聯實體：

```python
def bfs_retrieve(kg, start: str, max_hops: int = 3):
    visited = {start}
    queue = [(start, 0)]
    results = []
    while queue:
        node, depth = queue.pop(0)
        if depth < max_hops:
            for neighbor in kg.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    results.append((neighbor, depth + 1))
                    queue.append((neighbor, depth + 1))
    return results
```

優點：實作簡單、保證最短路徑。缺點：需要完整的知識圖譜、缺乏語意理解。

## 策略二：迭代式向量檢索

每次檢索後從結果中萃取關鍵詞或實體，作為下一次檢索的查詢：

```python
def iterative_vector_retrieve(query: str, vector_store, max_hops: int = 3):
    all_results = []
    current_query = query
    for hop in range(max_hops):
        results = vector_store.similarity_search(current_query, k=5)
        all_results.extend(results)
        # Extract entities from results for next query
        entities = extract_entities(results)
        if not entities:
            break
        current_query = " ".join(entities)
    return all_results
```

優點：不需要事先建構圖譜、可與現有向量資料庫整合。缺點：誤差累積（error propagation），前期檢索錯誤會影響後續。

## 策略三：LLM 自導向檢索

讓 LLM 自行決定檢索方向與策略。LLM 生成一系列子問題，逐一檢索後綜合回答：

```python
def llm_guided_retrieve(question: str, llm, retriever):
    prompt = f"為了回答「{question}」，需要哪些子問題？"
    sub_questions = llm.generate(prompt)

    context = []
    for sq in sub_questions:
        docs = retriever.retrieve(sq)
        context.extend(docs)

    return llm.answer(question, context)
```

優點：彈性高、可處理複雜問題。缺點：LLM 呼叫成本高、檢索延遲較大。

## 策略四：MCR（Multi-hop Chain Retrieval）

MCR 使用「推理鏈」記錄每一步的檢索結果與推理過程，類似 Chain-of-Thought 但在檢索層級：

```python
class MCRetrieval:
    def retrieve(self, query: str, max_hops: int = 3):
        chain = [{"step": 0, "query": query, "results": []}]
        for step in range(1, max_hops + 1):
            prev = chain[-1]
            next_query = self._refine_query(query, prev["results"])
            results = self.vector_store.similarity_search(next_query, k=3)
            chain.append({"step": step, "query": next_query, "results": results})
            if self._is_sufficient(results):
                break
        return chain
```

## 策略比較

| 策略 | 圖譜需求 | 成本 | 延遲 | 準確度 |
|------|---------|------|------|--------|
| BFS/DFS 遍歷 | 高 | 低 | 低 | 中 |
| 迭代向量檢索 | 無 | 低 | 中 | 中高 |
| LLM 自導向 | 無 | 高 | 高 | 高 |
| MCR 推理鏈 | 無 | 中 | 中 | 高 |

## 混合策略建議

實務中建議將 BFS 圖遍歷作為主幹，輔以 LLM 自導向進行跳躍決策：

```python
def hybrid_retrieve(kg, query: str, llm, max_hops: int = 3):
    seeds = extract_entities(query)
    direction = llm.decide_direction(seeds, query)
    if direction == "deep":
        return bfs_retrieve(kg, seeds[0], max_hops)
    else:
        return llm_guided_retrieve(query, llm, kg)
```

## 總結

多跳檢索沒有銀彈。圖遍歷適合結構化知識庫，迭代檢索適合純文字場景，LLM 自導向則在複雜推理問題上表現最佳。選擇策略需考量資料特性、延遲要求與成本預算。

---

**參考資料**

- https://www.google.com/search?q=multi+hop+retrieval+RAG+comparison
- https://www.google.com/search?q=iterative+retrieval+vs+graph+based+retrieval+RAG
- https://www.google.com/search?q=LLM+guided+multi+hop+retrieval
- https://www.google.com/search?q=chain+of+retrieval+MCR+multi+hop
