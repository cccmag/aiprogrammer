# Neo4j 與知識圖譜

## 前言

當知識圖譜的規模成長到數百萬個實體時，記憶體中的圖結構已不敷使用。Neo4j 作為最成熟的圖資料庫，提供了 ACID 交易、Cypher 查詢語言、以及圖演算法套件。本文探討如何用 Neo4j 儲存知識圖譜，並整合到 RAG 管線中。

## Cypher 查詢語言

Cypher 是 Neo4j 的宣告式查詢語言，語法直觀。建立實體與關係：

```cypher
CREATE (t:Entity {id: 'e1', name: 'Transformer', type: 'model'})
CREATE (a:Entity {id: 'e2', name: 'Attention', type: 'mechanism'})
CREATE (t)-[:USES]->(a)
```

查詢實體的鄰居與路徑：

```cypher
MATCH (t:Entity {name: 'Transformer'})-[:USES|BASED_ON*1..3]->(related)
RETURN related.name, related.type
```

## Python 整合 Neo4j

使用 `neo4j` Python driver 串接知識圖譜：

```python
from neo4j import GraphDatabase

class Neo4jKnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_entity(self, entity_id: str, name: str, type_: str):
        with self.driver.session() as session:
            session.run(
                "MERGE (e:Entity {id: $id}) "
                "SET e.name = $name, e.type = $type",
                id=entity_id, name=name, type=type_
            )

    def add_relation(self, source: str, target: str,
                     relation: str, weight: float = 1.0):
        with self.driver.session() as session:
            session.run(
                "MATCH (s:Entity {id: $src}), (t:Entity {id: $tgt}) "
                "MERGE (s)-[r:REL {type: $rel}]->(t) "
                "SET r.weight = $weight",
                src=source, tgt=target, rel=relation, weight=weight
            )

    def get_neighbors(self, entity_id: str, max_depth: int = 2):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (e:Entity {id: $id})-[:REL*1..$depth]->(n) "
                "RETURN DISTINCT n.id, n.name, n.type",
                id=entity_id, depth=max_depth
            )
            return [record.data() for record in result]
```

## 圖檢索增強生成

將 Neo4j 整合到 RAG 檢索器的關鍵在於將 Cypher 查詢結果轉換為自然語言上下文：

```python
def neo4j_context_retriever(driver, query_entities: list[str]) -> str:
    kg = Neo4jKnowledgeGraph(driver, "neo4j", "password")
    context_parts = []
    for eid in query_entities:
        neighbors = kg.get_neighbors(eid, max_depth=2)
        for n in neighbors:
            context_parts.append(
                f"{n['name']} ({n['type']})"
            )
    return "相關知識：\n" + "\n".join(context_parts)
```

## 圖演算法與 RAG 的結合

Neo4j 內建 PageRank、Betweenness Centrality 等圖演算法，可用於評估實體的重要性：

```cypher
CALL gds.pageRank.stream('knowledgeGraph')
YIELD nodeId, score
MATCH (e:Entity) WHERE id(e) = nodeId
RETURN e.name, score
ORDER BY score DESC
```

將 PageRank 分數作為檢索排序的加權因子，讓重要的實體在檢索結果中獲得更高權重，可以有效提升 RAG 的回答品質。

## 生產考量

使用 Neo4j 做為知識圖譜後端時需注意：建立適當的索引以加速實體查詢；使用 Cypher 參數化查詢避免注入攻擊；對大型圖譜使用批次寫入；考慮使用 Neo4j AuraDB 雲端服務降低運維成本。

## 總結

Neo4j 為知識圖譜提供了穩固的儲存與查詢基礎。透過 Cypher 的圖模式匹配能力，RAG 系統可以進行彈性的多跳檢索，並結合 PageRank 等圖演算法提升檢索品質。下一篇文章將比較不同的多跳檢索策略。

---

**參考資料**

- https://www.google.com/search?q=Neo4j+Cypher+query+language+tutorial
- https://www.google.com/search?q=Neo4j+Python+driver+RAG
- https://www.google.com/search?q=Neo4j+graph+algorithms+PageRank+knowledge+graph
- https://www.google.com/search?q=Neo4j+AuraDB+cloud+knowledge+graph
