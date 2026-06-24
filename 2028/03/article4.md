# SQL + Vector 混合查詢

## 前言

現實世界的知識管理系統中，結構化資料（關聯式資料庫）與非結構化資料（文件）並存。SQL + Vector 混合查詢讓 RAG 系統能同時查詢這兩個世界，從資料庫中取得精確的事實資料，再從向量庫中補充語意相關的上下文。

## 架構設計

混合查詢架構的核心是一個路由層（router），根據查詢意圖決定如何分派到 SQL 資料庫和向量資料庫：

```python
class HybridRouter:
    def __init__(self, db_conn, vector_store):
        self.db = db_conn
        self.vector_store = vector_store

    def query(self, natural_language_query: str) -> str:
        # Step 1: Classify intent
        intent = self._classify_intent(natural_language_query)

        # Step 2: Route to appropriate source(s)
        sql_results = []
        vector_results = []

        if intent in ("factual", "mixed"):
            sql_query = self._nl_to_sql(natural_language_query)
            sql_results = self.db.execute(sql_query).fetchall()

        if intent in ("semantic", "mixed"):
            vector_results = self.vector_store.similarity_search(
                natural_language_query, k=5
            )

        # Step 3: Merge results
        return self._merge_results(sql_results, vector_results)
```

## 自然語言轉 SQL

將使用者問題轉換為 SQL 查詢是此架構的核心。LLM 在此扮演關鍵角色：

```python
def nl_to_sql(natural_query: str, schema: str, llm) -> str:
    prompt = f"""資料庫 Schema：
{schema}

將以下自然語言轉換為 SQL：
「{natural_query}」

僅回傳 SQL，不要解釋。"""
    return llm.generate(prompt).strip()
```

為了安全，SQL 生成後應經過語法驗證與權限檢查：

```python
import sqlparse

def validate_sql(sql: str) -> bool:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False
    forbidden = {"DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE"}
    tokens = [t.value.upper() for t in parsed[0].flatten()]
    return not any(f in tokens for f in forbidden)
```

## 混合檢索的結果融合

將 SQL 結果（精確資料）與向量結果（語意相關）合併為統一的 LLM 上下文，需要考慮優先級：

```python
def merge_results(sql_rows: list[tuple],
                  vector_docs: list[str]) -> str:
    context_parts = ["=== 結構化資料 (SQL) ==="]
    for row in sql_rows:
        context_parts.append(" | ".join(str(cell) for cell in row))

    context_parts.append("\n=== 非結構化資料 (Vector) ===")
    for doc in vector_docs:
        context_parts.append(doc)

    return "\n".join(context_parts)
```

## 實戰範例

假設一個企業知識庫包含「員工資料表」和「專案文件向量庫」：

```python
# 使用者問：「去年 Q3 業績最好的銷售員是誰？他的專案文件提到哪些技術？」
sql = nl_to_sql(
    "去年 Q3 業績最好的銷售員",
    "employees(id,name,dept,revenue,quarter,year)",
    llm
)
# SQL: SELECT name, revenue FROM employees
#       WHERE dept='sales' AND quarter='Q3' AND year=2025
#       ORDER BY revenue DESC LIMIT 1

top_sales = db.execute(sql).fetchone()  # ('王大明', 5200000)
tech_docs = vector_store.similarity_search("王大明的專案技術", k=3)
context = merge_results([top_sales], tech_docs)
```

## 挑戰與解法

挑戰一：**SQL 生成不準確**。解法：提供完整的 schema 資訊與範例查詢（few-shot）。

挑戰二：**混合結果的上下文過長**。解法：對 SQL 結果進行摘要，僅保留關鍵欄位。

挑戰三：**延遲**。解法：LLM 路由判斷若為純 SQL 查詢則跳過向量檢索，反之亦然。

```python
def optimized_hybrid(query: str) -> str:
    intent = quick_classify(query)  # 輕量分類器
    if intent == "factual":
        return sql_only(query)
    elif intent == "semantic":
        return vector_only(query)
    else:
        return full_hybrid(query)
```

## 總結

SQL + Vector 混合查詢讓 RAG 系統不再被限制於非結構化資料。精確的事實查詢走 SQL 通道，語意模糊的探索走向量通道，兩者互補。關鍵在於可靠的 NL-to-SQL 轉換與結果融合策略。

---

**參考資料**

- https://www.google.com/search?q=SQL+vector+hybrid+retrieval+RAG
- https://www.google.com/search?q=natural+language+to+SQL+LLM+tutorial
- https://www.google.com/search?q=structured+unstructured+data+hybrid+search
- https://www.google.com/search?q=text+to+SQL+validation+security
