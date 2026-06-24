# GraphRAG 實作深入

## 前言

GraphRAG 是微軟在 2024 年提出的架構，將知識圖譜與 RAG 結合，解決傳統向量檢索缺乏結構化推理能力的問題。本文深入探討 GraphRAG 的實作細節，從圖建構、圖檢索到答案生成的完整管線。

## GraphRAG 的核心架構

GraphRAG 包含三個層次：**實體萃取層**、**圖索引層**、**圖檢索層**。實體萃取層從原始文件中識別命名實體與關係；圖索引層建立實體之間的多層次連結；圖檢索層根據查詢走訪圖結構收集上下文。

不同於傳統 RAG 僅檢索 Top-K 向量片段，GraphRAG 可以沿著關係路徑發現間接相關的知識。例如查詢「Transformer 的影響」時，系統不僅找到 Transformer 的相關文件，還能走訪到「BERT → Transformer → NLP 應用」的完整脈絡。

## 實體萃取與圖建構

使用 LLM 進行實體萃取是 GraphRAG 的關鍵步驟。以下是簡化的實作：

```python
import json
from openai import OpenAI

def extract_entities_and_relations(text: str) -> dict:
    prompt = f"""從以下文本中萃取實體與關係，以 JSON 格式回覆：
實體格式：[{{"name": "...", "type": "..."}}]
關係格式：[{{"source": "...", "target": "...", "relation": "..."}}]

文本：{text}"""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

## 圖檢索策略

實作中以 BFS 或 DFS 走訪知識圖譜，收集實體與關係作為 LLM 上下文：

```python
def graph_retrieve(kg: KnowledgeGraph, seed_entities: list[str],
                   depth: int = 2) -> str:
    context = []
    visited = set(seed_entities)
    queue = [(e, 0) for e in seed_entities]

    while queue:
        current, d = queue.pop(0)
        if current in kg.entities:
            e = kg.entities[current]
            context.append(f"{'  ' * d}{e.name} ({e.type})")
            for r in kg.relations:
                if r.source == current and r.target not in visited:
                    visited.add(r.target)
                    queue.append((r.target, d + 1))
                elif r.target == current and r.source not in visited:
                    visited.add(r.source)
                    queue.append((r.source, d + 1))

    return "\n".join(context)
```

## 社群偵測與摘要

GraphRAG 進階功能之一是將圖譜分割為社群（community），並對每個社群生成摘要。這使得檢索可以先定位到相關社群，再深入查找：

```python
def detect_communities(kg: KnowledgeGraph) -> dict:
    """Simple Label Propagation"""
    labels = {eid: eid for eid in kg.entities}
    for _ in range(10):
        for entity_id in kg.entities:
            neighbors = kg.get_neighbors(entity_id)
            if neighbors:
                neighbor_labels = [labels[n] for n in neighbors]
                labels[entity_id] = max(set(neighbor_labels),
                                        key=neighbor_labels.count)
    communities = {}
    for eid, label in labels.items():
        communities.setdefault(label, []).append(eid)
    return communities
```

## GraphRAG vs. 傳統 RAG

向量 RAG 擅長語意相似度比對，但不懂實體之間的結構關係。GraphRAG 在需要多步推理（multi-hop reasoning）的場景中明顯佔優，例如問「A 公司的競爭對手採用了哪些技術？」這類需要跨越多個關係的問題。

然而 GraphRAG 的建構成本較高，不僅需要 LLM 呼叫來萃取實體，圖索引的更新也較複雜。實務中建議採用**混合檢索**：先用向量檢索找出相關文檔，再用 GraphRAG 進行結構化推理。

## 總結

GraphRAG 代表了 RAG 技術從「向量相似度比對」到「結構化知識推理」的重要演進。將知識圖譜納入 RAG 管線後，LLM 能夠理解實體之間的關係脈絡，回答需要多步推理的複雜問題。下一篇文章將探討如何利用 Neo4j 等圖資料庫實作生產級的知識圖譜。

---

**參考資料**

- https://www.google.com/search?q=GraphRAG+Microsoft+knowledge+graph+retrieval
- https://www.google.com/search?q=entity+extraction+LLM+knowledge+graph
- https://www.google.com/search?q=BFS+DFS+graph+traversal+RAG
- https://www.google.com/search?q=community+detection+graphrag
