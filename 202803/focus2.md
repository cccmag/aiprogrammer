# 知識圖譜建構與查詢（2012-2028）

## Google Knowledge Graph 的開端

2012 年 Google 發布 Knowledge Graph，改變搜尋引擎的運作方式。從關鍵詞匹配走向實體關係理解。

```
Apple ──is_a──> Company
Apple ──founded_by──> Steve Jobs
Apple ──headquarters──> Cupertino
```

## 圖譜建構技術

### 實體抽取（NER）

從非結構化文字中識別人名、地名、組織等實體。現代方法結合 LLM 進行 zero-shot 抽取。

```python
# LLM 輔助的實體關係抽取
def extract_entities_relations(text):
    entities = [
        Entity("e1", "Transformer", "model"),
        Entity("e2", "Attention", "mechanism"),
    ]
    relations = [
        Relation("e1", "e2", "uses"),
    ]
    return entities, relations
```

### 關係抽取與消歧

同一實體可能有多種稱呼（「蘋果、Apple, Inc.」），需要實體連結（Entity Linking）來消歧。2025 年後 LLM 可直接處理。

## 圖查詢語言

SPARQL 是 RDF 圖的標準查詢語言，Neo4j 使用 Cypher，TigerGraph 使用 GSQL。但對 LLM 來說，自然語言到圖查詢（Text-to-GraphQL）更實用。

```python
# 圖遍歷查詢
def query_knowledge_graph(kg, start_entity, max_depth):
    path = kg.shortest_path(start_entity, target_entity)
    neighbors = kg.get_neighbors(start_entity)
    return {"path": path, "neighbors": neighbors}
```

## 2025-2028 趨勢

2025 年 LLM-as-KG-builder 成為主流，2026 年自動圖譜更新與版本控制，2027 年去中心化知識圖譜（基于區塊鏈），2028 年多模態知識圖譜整合文字、圖像、音訊。

## 延伸閱讀

- [Google Knowledge Graph 2012](https://www.google.com/search?q=Google+Knowledge+Graph+2012)
- [SPARQL 查詢語言](https://www.google.com/search?q=SPARQL+W3C+standard)
- [Neo4j 圖資料庫](https://www.google.com/search?q=Neo4j+graph+database+RAG)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之二。*
