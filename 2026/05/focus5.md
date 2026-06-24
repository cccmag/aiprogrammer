# 記憶與知識管理：長期記憶與 RAG（2023-2026）

## Agent 的記憶困境

早期的 LLM Agent 有一個根本性的缺陷：**沒有記憶**。每次對話都是從零開始，Agent 無法記住之前說過的話、做過的事、學到的經驗。

```
無記憶的 Agent：
─────────────────

使用者：幫我安排一個去日本的行程（第 1 天）
Agent：好的！讓我查詢日本旅遊資訊...

使用者：我喜歡文化體驗（第 2 天）
Agent：（忘記了第 1 天的對話）
        好的！日本有哪些文化體驗呢？

使用者：昨天不是說要去日本嗎？（第 3 天）
Agent：（還是沒記住）
        抱歉，讓我們重新開始...

→ 使用者崩潰！
```

## 短期記憶：上下文視窗

### 什麼是上下文視窗？

LLM 的「短期記憶」就是上下文視窗（Context Window）——模型一次能「看到」的 token 數量。

```
上下文視窗的演進：
─────────────────

2022  GPT-3.5    4K tokens  (~3,000 字)
2023  GPT-4      8K/32K    (~6,000-24,000 字)
2024  Claude 3  200K       (~150,000 字)
2025  Gemini    2M         (~1,500,000 字)
2026  GPT-6     10M        (~7,500,000 字)
```

### 上下文視窗的限制

雖然上下文視窗在快速增長，但仍然有物理限制：

1. **計算成本**：注意力機制的計算量與上下文長度的平方成正比
2. **注意力稀釋**：模型在極長上下文中難以關注到關鍵資訊
3. **輸入成本**：每次 API 呼叫傳送大量 token 的費用很高

### 視窗管理技術

```python
class ContextManager:
    def __init__(self, max_tokens=128000):
        self.max_tokens = max_tokens
        self.messages = []
        self.current_tokens = 0
    
    def add_message(self, role, content):
        tokens = count_tokens(content)
        
        # 如果超出限制，需要壓縮
        while self.current_tokens + tokens > self.max_tokens:
            removed = self.messages.pop(0)
            self.current_tokens -= count_tokens(removed.content)
        
        self.messages.append({"role": role, "content": content})
        self.current_tokens += tokens
    
    def summarize(self):
        """將早期對話壓縮為摘要"""
        if len(self.messages) > 10:
            early = self.messages[:5]
            summary = llm.summarize(early)
            self.messages = [
                {"role": "system", "content": f"先前的對話摘要：{summary}"}
            ] + self.messages[5:]
```

## RAG：檢索增強生成

### RAG 的誕生

2023 年，Lewis 等人發表了「Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks」——RAG 從此成為 AI Agent 知識管理的基本模式。

RAG 的核心思想：**不把所有的知識放進提示中，而是讓 Agent 在需要時「查資料庫」**。

```
┌───────────────────────────────────────────────┐
│              RAG 架構                           │
├───────────────────────────────────────────────┤
│                                                 │
│  使用者問題                                     │
│      │                                          │
│      ▼                                          │
│  ┌──────────┐                                   │
│  │  嵌入模型  │──→ 向量資料庫 ─→ 相關文檔       │
│  │ (Embed)   │     (Vector DB)                   │
│  └──────────┘                                   │
│      │                                          │
│      ▼                                          │
│  ┌──────────┐                                   │
│  │  LLM     │ ←── 原始問題 + 相關文檔           │
│  │ (生成)   │                                    │
│  └──────────┘                                   │
│      │                                          │
│      ▼                                          │
│  最終答案                                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

### RAG 的實現

```python
class RAGSystem:
    def __init__(self, documents):
        self.embedder = EmbeddingModel()
        self.vector_db = VectorDatabase()
        self.llm = LLM()
        
        # 索引文件
        for doc in documents:
            chunks = self.chunk_document(doc)
            for chunk in chunks:
                embedding = self.embedder.embed(chunk)
                self.vector_db.add(chunk, embedding)
    
    def query(self, question, k=3):
        # 1. 將問題轉為向量
        q_embedding = self.embedder.embed(question)
        
        # 2. 在向量庫中搜索最相關的文檔
        relevant = self.vector_db.search(q_embedding, k)
        
        # 3. 將文檔作為上下文注入
        context = "\n\n".join(relevant)
        prompt = f"""
        基於以下資訊回答問題：
        
        相關資訊：
        {context}
        
        問題：{question}
        答案："""
        
        # 4. LLM 生成答案
        return self.llm.generate(prompt)
```

### 向量資料庫的選擇

| 資料庫 | 類型 | 優點 | 適合場景 |
|-------|------|------|---------|
| Pinecone | 雲端 | 託管式、高可用 | 生產環境 |
| Weaviate | 雲端/本地 | 內建 GraphQL | 中型應用 |
| Chroma | 嵌入式 | 輕量、易用 | 開發原型 |
| Qdrant | 雲端/本地 | 高效能過濾 | 大規模系統 |
| Milvus | 分散式 | 超高效能 | 企業級部署 |

## 長期記憶系統

### 記憶的層次結構

受到人類記憶系統的啟發，AI Agent 的記憶也分為多個層次：

```
人類記憶層次            AI Agent 對應
────────────────────────────────────
感官記憶 (～1秒)     → 即時感知輸入
短期記憶 (～30秒)    → 上下文視窗
工作記憶 (～數分)    → 當前任務狀態
長期記憶 (數年)      → 向量資料庫 + 知識圖譜

長期記憶又分為：
├── 情節記憶（Episodic）→ 過去的互動記錄
├── 語意記憶（Semantic）→ 事實性知識
└── 程序記憶（Procedural）→ 技能與流程
```

### 記憶系統的實作

```python
class AgentMemory:
    def __init__(self):
        self.episodic_memory = VectorDatabase()  # 情節記憶
        self.semantic_memory = VectorDatabase()  # 語意記憶  
        self.procedural_memory = SkillDatabase()  # 程序記憶
        self.short_term = []  # 短期記憶
        self.summary = ""  # 壓縮摘要
    
    def remember(self, event):
        # 存入短期記憶
        self.short_term.append(event)
        
        # 短期記憶過長時壓縮
        if len(self.short_term) > 20:
            self.compress()
    
    def compress(self):
        # 將短期記憶壓縮為摘要
        new_summary = self.llm.summarize(self.short_term)
        
        # 儲存到情節記憶
        self.episodic_memory.add(new_summary)
        
        # 更新摘要
        if self.summary:
            self.summary = self.llm.merge_summaries(
                self.summary, new_summary
            )
        else:
            self.summary = new_summary
        
        self.short_term = []
    
    def recall(self, query, k=5):
        # 從多個記憶來源檢索
        episodic_results = self.episodic_memory.search(query, k)
        semantic_results = self.semantic_memory.search(query, k)
        
        return {
            "short_term": self.short_term[-5:],
            "summary": self.summary,
            "episodic": episodic_results,
            "semantic": semantic_results
        }
```

### 記憶壓縮策略

隨著時間推移，Agent 的記憶會不斷累積。記憶壓縮是保持系統可管理性的關鍵：

```
壓縮策略：
─────────────────

1. 時間衰減（Temporal Decay）
   舊記憶的權重逐漸降低
   最近 1 小時：權重 1.0
   最近 1 天：權重 0.7
   最近 1 週：權重 0.3
   超過 1 月：權重 0.1

2. 重要性評分（Importance Scoring）
   只保留重要的記憶
   由 LLM 評估每個記憶的重要性
   重要性 < 門檻值的：刪除或壓縮

3. 摘要合併（Summary Merging）
   將多個相關記憶合併為摘要
   減少儲存量，保留關鍵資訊

4. 知識萃取（Knowledge Extraction）
   從具體記憶中萃取一般性知識
   具體：使用者說不喜歡吃魚
   萃取：使用者偏好是... 
```

## 知識圖譜與結構化記憶

### 為什麼需要知識圖譜？

向量資料庫擅長「相似度搜索」，但無法表達實體之間的關係。知識圖譜填補了這個空白：

```
向量資料庫：
「台北的天氣如何？」→ 找到「台北天氣」文件（相似度匹配）

知識圖譜：
「台北的天氣如何？」→ 
   台北 ─── isA ───→ 城市
   台北 ─── hasWeather ──→ 今天：25°C
   台北 ─── locatedIn ──→ 台灣
   台灣 ─── hasCapital ──→ 台北
   → 可以回答「台灣的首都天氣如何？」（關係推理）
```

### 記憶與知識圖譜的結合

```python
class KnowledgeGraphMemory:
    def __init__(self):
        self.kg = KnowledgeGraph()
        self.vector_db = VectorDatabase()
    
    def store_experience(self, experience):
        # 1. 萃取實體和關係
        entities_relations = self.llm.extract_kg(experience)
        
        # 2. 更新知識圖譜
        for entity, relations in entities_relations.items():
            self.kg.add_entity(entity)
            for rel, target in relations:
                self.kg.add_relation(entity, rel, target)
        
        # 3. 同時存入向量資料庫（雙重存儲）
        self.vector_db.add(experience)
    
    def query(self, question):
        # 1. 判斷是否需要關係推理
        if self.needs_reasoning(question):
            # 使用知識圖譜推理
            kg_result = self.kg.query(question)
            return kg_result
        
        # 2. 一般問題使用向量檢索
        return self.vector_db.search(question)
```

## 記憶管理的挑戰

### 1. 記憶衝突

Agent 的記憶中可能存在矛盾資訊：

```
問題：之前存儲的「使用者不喜歡吃魚」vs 新的「使用者點了鮭魚」
解決：版本化記憶 + 時間戳記 → 最新的資訊優先
```

### 2. 記憶遺忘

類似人類的「遺忘曲線」，Agent 也需要決定哪些記憶該保留、哪些該刪除：

```
Ebbinghaus 遺忘曲線（人類）：
20 分鐘後：遺忘 42%
1 小時後：遺忘 56%
1 天後：遺忘 74%
1 週後：遺忘 77%
1 月後：遺忘 79%

AI Agent 也需要類似的策略來管理記憶空間
```

### 3. 記憶檢索的準確性

向量相似度搜索並非完美：
- 語義偏移：同一個意思不同表達可能搜不到
- 檢索雜訊：回傳了大量不相關的結果
- 遺漏關鍵資訊：最重要的資訊可能未被檢索到

## 結語

記憶是智慧的核心。從無記憶的原始 LLM 到配備完整記憶系統的現代 AI Agent，記憶管理技術的進步是 Agent 能力提升的關鍵驅動力。

RAG 解決了「知識存取」問題，向量資料庫解決了「相似檢索」問題，知識圖譜解決了「關係推理」問題——將這些技術結合起來，才能打造真正有「記憶」的 AI Agent。

下一篇文章將介紹將這些技術整合在一起的 Agent 框架與生態系統。

---

## 延伸閱讀

- [RAG 論文](https://www.google.com/search?q=Retrieval-Augmented+Generation+paper)
- [向量資料庫比較](https://www.google.com/search?q=vector+database+comparison+2025)
- [Agent 記憶系統設計](https://www.google.com/search?q=AI+agent+memory+system+design)
- [知識圖譜與 LLM](https://www.google.com/search?q=knowledge+graph+LLM+integration)

---

*本篇文章為「AI 程式人雜誌 2026 年 5 月號」歷史回顧系列之一。*
