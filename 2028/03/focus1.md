# 從 RAG 到 GraphRAG（2023-2028）

## RAG 的起源

2023 年，Lewis 等人提出 RAG（Retrieval-Augmented Generation），解決 LLM 知識過時與幻覺問題。基本流程：檢索相關文件 → 注入上下文 → 生成回答。

```
查詢 ──→ 向量搜尋 ──→ 相關文檔 ──→ LLM ──→ 回答
```

## 從平面檢索到結構化知識

傳統 RAG 的問題：文檔之間缺乏關聯，無法處理需要多個事實推理的查詢。例如「Transformer 的作者還發明了什麼？」無法靠單篇文檔回答。

## GraphRAG 的誕生

2024 年，Microsoft 發表 GraphRAG：先從文檔中提取實體和關係，建構知識圖譜，再結合圖遍歷與向量搜尋進行檢索。

```python
# GraphRAG 檢索流程
class GraphRAG:
    def retrieve(self, query, entities, kg):
        # 向量搜尋找相關實體
        relevant = [e for e in entities
                    if self.vector_sim(query, e.text) > 0.7]
        # 圖遍歷擴展上下文
        context = []
        for e in relevant:
            context.append(e.text)
            for n in kg.get_neighbors(e.id):
                context.append(n.text)
        return "\n".join(context)
```

## 2025-2028 發展

2025 年 LightRAG 提出輕量級圖索引，2026 年 FastGraphRAG 引入流式圖建構，2027 年 Hierarchical GraphRAG 支援多層次摘要，2028 年走向即時圖譜更新。

## 核心結論

GraphRAG 的優勢在於：保留了實體間的語義關係，支援社群摘要（community summarization），對全局性問題的回答質量顯著優於傳統 RAG。

## 延伸閱讀

- [Microsoft GraphRAG](https://www.google.com/search?q=Microsoft+GraphRAG+2024)
- [LightRAG 輕量圖 RAG](https://www.google.com/search?q=LightRAG+2025+paper)
- [Hierarchical GraphRAG 多層次](https://www.google.com/search?q=Hierarchical+GraphRAG+2027)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之一。*
