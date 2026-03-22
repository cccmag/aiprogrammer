# RAG 技術演進：從檢索增強到知識蒸餾

## 前言

檢索增強生成（Retrieval-Augmented Generation, RAG）在 2026 年已成為企業 AI 應用的核心技術。從最初的簡單向量檢索，到如今結合知識圖譜、混合搜尋和知識蒸餾的複雜系統，RAG 技術經歷了快速的演進。本文追蹤這條技術演進路線，探討最新趨勢和最佳實踐。

## RAG 的基本原理

### 經典 RAG 流程

```python
class BasicRAG:
    """
    經典的 RAG 實現
    """
    
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store  # e.g., ChromaDB, Pinecone
        self.llm = llm
    
    def retrieve(self, query: str, top_k: int = 5) -> list:
        # 將查詢轉為向量
        query_embedding = self.embed(query)
        
        # 檢索相似文件
        results = self.vector_store.similarity_search(
            query_embedding, 
            k=top_k
        )
        return results
    
    def generate(self, query: str, context: list) -> str:
        # 構造 prompt
        prompt = f"""
        根據以下上下文回答問題。
        
        上下文：
        {chr(10).join(context)}
        
        問題：{query}
        
        答案：
        """
        
        return self.llm.generate(prompt)
    
    def answer(self, query: str) -> str:
        docs = self.retrieve(query)
        context = [doc.content for doc in docs]
        return self.generate(query, context)
```

## 第一階段：基礎向量檢索

### 早期的 RAG 實現

最早的 RAG 系統採用純向量相似度搜尋：

```python
# 簡單的向量檢索
import chromadb

client = chromadb.Client()
collection = client.create_collection("documents")

# 檢索
results = collection.query(
    query_texts=["人工智慧的發展"],
    n_results=5
)
```

### 挑戰與限制

- **語義鸿沟**：關鍵字匹配與語義理解的差距
- **冷啟動問題**：新文件缺乏足夠的檢索信號
- **召回率瓶頸**：單一檢索方法難以覆蓋所有相關內容
- **幻覺問題**：模型仍可能產生與檢索內容不符的輸出

## 第二階段：混合搜尋

### 結合向量與關鍵字

混合搜尋結合了向量相似度和 BM25 關鍵字匹配：

```python
class HybridRAG:
    def __init__(self, vector_store, bm25_index, llm, alpha=0.5):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.llm = llm
        self.alpha = alpha  # 向量權重
    
    def hybrid_search(self, query: str, top_k: int = 10):
        # 向量搜尋
        vector_results = self.vector_store.similarity_search(query, k=top_k*2)
        
        # BM25 關鍵字搜尋
        bm25_results = self.bm25_index.search(query, k=top_k*2)
        
        # Reciprocal Rank Fusion
        fused_scores = {}
        for i, (doc, score) in enumerate(vector_results):
            fused_scores[doc.id] = fused_scores.get(doc.id, 0) + self.alpha / (60 + i)
        
        for i, (doc, score) in enumerate(bm25_results):
            fused_scores[doc.id] = fused_scores.get(doc.id, 0) + (1-self.alpha) / (60 + i)
        
        # 排序並返回
        ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return [self.get_doc(doc_id) for doc_id, _ in ranked[:top_k]]
```

### 重新排序（Re-ranking）

```python
from sentence_transformers import CrossEncoder

class RerankedRAG(HybridRAG):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
    
    def rerank(self, query: str, candidates: list, top_k: int = 5):
        # 構造查詢-文件對
        pairs = [(query, doc.content) for doc in candidates]
        
        # 交叉編碼器重排序
        scores = self.reranker.predict(pairs)
        
        # 按分數排序
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[:top_k]]
```

## 第三階段：知識圖譜增強

### 結構化知識的引入

將知識圖譜整合到 RAG 中：

```python
class KnowledgeGraphRAG:
    def __init__(self, graph_db, vector_store, llm):
        self.graph_db = graph_db  # Neo4j, NebulaGraph
        self.vector_store = vector_store
        self.llm = llm
    
    def retrieve_with_graph(self, query: str):
        # 1. 向量檢索
        vector_docs = self.vector_store.similarity_search(query, k=10)
        
        # 2. 實體提取
        entities = self.extract_entities(query)
        
        # 3. 圖譜查詢
        graph_context = []
        for entity in entities:
            related = self.graph_db.query(f"""
                MATCH (e)-[r]-(related)
                WHERE e.name = '{entity}'
                RETURN e, r, related
                LIMIT 5
            """)
            graph_context.extend(related)
        
        # 4. 融合上下文
        return self.fuse_context(vector_docs, graph_context)
    
    def extract_entities(self, text: str) -> list:
        # 使用 NER 提取實體
        response = self.llm.generate(f"""
            從以下文字中提取所有實體：
            
            {text}
            
            只返回實體名稱，用逗號分隔。
        """)
        return [e.strip() for e in response.split(",")]
```

### 查詢擴展

```python
class QueryExpansionRAG:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store
    
    def expand_query(self, query: str) -> list:
        """使用 LLM 擴展查詢"""
        prompt = f"""
        為以下查詢生成 3-5 個相關的替代表述，以擴展檢索範圍。
        確保包含同義詞、相關概念和不同表述方式。
        
        原查詢：{query}
        
        替代表述：
        """
        
        response = self.llm.generate(prompt)
        expansions = [query] + [line.strip() for line in response.split("\n") if line.strip()]
        return expansions[:5]
    
    def multi_query_retrieve(self, query: str, top_k: int = 5):
        # 擴展查詢
        queries = self.expand_query(query)
        
        # 平行檢索
        all_results = []
        for q in queries:
            results = self.vector_store.similarity_search(q, k=top_k)
            all_results.extend(results)
        
        # 去重和排序
        seen = set()
        unique_results = []
        for doc in all_results:
            if doc.id not in seen:
                seen.add(doc.id)
                unique_results.append(doc)
        
        return unique_results[:top_k]
```

## 第四階段：知識蒸餾

### 從檢索到蒸餾

知識蒸餾是 RAG 技術的最新演進，旨在將外部知識更有效地整合到模型中：

```python
class KnowledgeDistillationRAG:
    def __init__(self, llm, vector_store, knowledge_base):
        self.llm = llm
        self.vector_store = vector_store
        self.knowledge_base = knowledge_base
    
    def distill_knowledge(self, query: str) -> str:
        """
        知識蒸餾：將檢索到的知識轉化為模型可直接使用的格式
        """
        # 1. 檢索相關文件
        docs = self.vector_store.similarity_search(query, k=10)
        
        # 2. 提取關鍵資訊
        key_info = self.extract_key_information(docs)
        
        # 3. 結構化知識
        structured = self.structure_knowledge(key_info, query)
        
        # 4. 生成蒸餾後的知識
        distilled = self.llm.generate(f"""
            將以下資訊蒸餾為簡潔、準確的知識陳述，直接回答查詢。
            
            查詢：{query}
            
            相關資訊：
            {docs}
            
            蒸餾後的知識（直接回答問題）：
        """)
        
        return distilled
    
    def extract_key_information(self, docs: list) -> str:
        """從文件列表中提取關鍵資訊"""
        combined = "\n\n".join([doc.content for doc in docs])
        return self.llm.generate(f"""
            從以下文件中提取與回答問題最相關的資訊：
            
            文件：
            {combined}
            
            提取關鍵事實、數據和關係：
        """)
    
    def structure_knowledge(self, info: str, query: str) -> dict:
        """將知識結構化"""
        response = self.llm.generate(f"""
            將以下資訊結構化為 JSON 格式：
            
            資訊：{info}
            
            格式：
            {{
                "answer": "直接回答",
                "supporting_facts": ["關鍵事實"],
                "confidence": "高/中/低",
                "sources": ["來源標識"]
            }}
        """)
        return json.loads(response)
```

### 自適應檢索

```python
class AdaptiveRAG:
    """
    自適應 RAG：根據問題難度選擇檢索策略
    """
    
    def __init__(self, llm, simple_retriever, complex_retriever):
        self.llm = llm
        self.simple_retriever = simple_retriever
        self.complex_retriever = complex_retriever
    
    def classify_query(self, query: str) -> str:
        """分類查詢難度"""
        response = self.llm.generate(f"""
            評估以下查詢的複雜度和所需資訊：
            
            查詢：{query}
            
            分類：
            - "simple": 簡單事實查詢，無需深度檢索
            - "standard": 標準問題，單次檢索即可
            - "complex": 複雜問題，需要多步驟檢索
            - "research": 研究級問題，需要深度分析
            
            只返回分類名稱。
        """)
        return response.strip().lower()
    
    def answer(self, query: str):
        category = self.classify_query(query)
        
        if category == "simple":
            # 簡單問題直接回答
            return self.llm.generate(f"回答：{query}")
        
        elif category == "standard":
            # 標準檢索
            docs = self.simple_retriever.search(query)
            return self.generate_with_context(query, docs)
        
        elif category == "complex":
            # 多次檢索和推理
            docs = self.complex_retriever.multi_hop_search(query)
            return self.generate_with_context(query, docs)
        
        else:  # research
            # 深度研究和蒸餾
            return self.distill_and_answer(query)
```

## 最新實踐：Router 與管道

### 智慧路由

```python
class IntelligentRouter:
    def __init__(self):
        self.routes = {
            "factual": FactualRAG(),
            "analytical": AnalyticalRAG(),
            "creative": CreativeAgent(),
            "code": CodeRAG()
        }
    
    def route(self, query: str) -> str:
        """根據查詢類型選擇最適合的 RAG 管道"""
        response = self.llm.generate(f"""
            判斷以下查詢最適合哪種處理方式：
            
            查詢：{query}
            
            選項：
            - factual: 事實查詢，需要準確資訊
            - analytical: 分析問題，需要推理
            - creative: 創意問題，需要想像力
            - code: 程式碼相關問題
            
            只返回一個選項。
        """)
        return response.strip().lower()
    
    def answer(self, query: str):
        route_type = self.route(query)
        return self.routes[route_type].answer(query)
```

## 效能優化

### 快取策略

```python
class CachedRAG:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm
        self.query_cache = LRUCache(maxsize=1000)
        self.doc_cache = LRUCache(maxsize=10000)
    
    def retrieve(self, query: str):
        # 查詢快取
        if query in self.query_cache:
            return self.query_cache[query]
        
        # 檢索
        results = self.vector_store.similarity_search(query)
        
        # 存入快取
        self.query_cache[query] = results
        return results
```

## 未來趨勢

### Agentic RAG

讓 RAG 系統具有自主規劃和執行能力：

```python
class AgenticRAG:
    """
    自主 RAG Agent
    """
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def plan(self, query: str) -> list:
        """規劃檢索策略"""
        return self.llm.generate(f"""
            為以下問題規劃檢索步驟：
            
            問題：{query}
            
            可用工具：search, knowledge_graph, web_search, calculator
            
            規劃步驟（JSON 陣列）：
            [
                {{"tool": "...", "query": "..."}},
                ...
            ]
        """)
    
    def execute(self, query: str):
        plan = self.plan(query)
        results = []
        
        for step in plan:
            tool = self.tools[step["tool"]]
            result = tool.execute(step["query"])
            results.append(result)
        
        return self.synthesize(query, results)
```

## 結語

RAG 技術從最初的簡單向量檢索，發展到如今融合混合搜尋、知識圖譜和知識蒸餾的複雜系統。這條演進路線反映了我們對「如何讓 AI 有效利用外部知識」這一問題的深入理解。隨著 Agentic RAG 和自適應檢索技術的成熟，RAG 正在從被動的資訊檢索轉變為主動的知識獲取和整合系統。建議開發者根據應用場景選擇適合的 RAG 層級，不必追求最複雜的方案，而是找到效能與成本的平衡點。

---

**延伸閱讀**

- [RAG 技術survey論文](https://www.google.com/search?q=RAG+retrieval+augmented+generation+survey)
- [LangChain RAG 文件](https://www.google.com/search?q=LangChain+RAG+tutorial)
- [Haystack 框架](https://www.google.com/search?q=Haystack+RAG+framework)
