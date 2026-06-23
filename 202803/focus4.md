# 結構化資料 RAG（2024-2028）

## 為什麼需要結構化 RAG？

企業資料多儲存在 SQL 資料庫、Excel、CSV 中。傳統 RAG 只處理非結構化文本，無法回答「上季營收最高的產品是什麼？」這類問題。

## Text-to-SQL 路線

最直接的方法：將自然語言轉換為 SQL 查詢，執行後返回結果。

```python
def text_to_sql_rag(query, db_schema):
    # LLM 生成 SQL (簡化示意)
    sql_prompt = f"""
    Schema: {db_schema}
    查詢: {query}
    生成 SQL:"""
    sql = llm_generate(sql_prompt)
    # 執行 SQL
    results = execute_sql(sql)
    # 用結果回答
    answer = llm_generate(
        f"根據資料 {results} 回答問題"
    )
    return answer
```

## 混合檢索策略

2024-2025 主流方案是 Hybrid RAG：同時檢索向量資料庫和結構化資料源，結果融合後送入 LLM。

```
查詢 ──┬──> 向量檢索 ──> 非結構化上下文
       ├──> Text-to-SQL ──> 表格結果
       └──> 知識圖譜 ──> 關係路徑
               │
               ▼
          合併排序 → LLM 生成
```

## 表格理解的進展

2024 年 TableLLaMA 專門處理表格，2025 年 Chain-of-Table 將表格操作分解為步驟，2026 年 StructGPT 統一結構化與非結構化，2027 年自動 Schema 發現，2028 年多資料庫聯合查詢。

## 工具使用模式

```python
def structured_rag_tool(query):
    tools = [
        {"name": "sql_query", "desc": "查詢 SQL"},
        {"name": "vector_search", "desc": "搜尋文檔"},
        {"name": "kg_query", "desc": "查詢圖譜"},
    ]
    selected = llm_select_tool(query, tools)
    return execute_tool(selected, query)
```

## 延伸閱讀

- [Text-to-SQL 方法](https://www.google.com/search?q=Text+to+SQL+LLM+2024)
- [Hybrid RAG 架構](https://www.google.com/search?q=hybrid+retrieval+augmented+generation)
- [StructGPT 統一檢索](https://www.google.com/search?q=StructGPT+structured+unstructured+2024)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之四。*
