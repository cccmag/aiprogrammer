# Agentic RAG 架構（2025-2028）

## 從被動檢索到主動代理

傳統 RAG 是單向的：查詢 → 檢索 → 生成。Agentic RAG 讓 LLM 自主決定何時檢索、用什麼工具、是否需要更多資訊。

```
Agent Loop:
  1. 理解查詢
  2. 選擇工具（搜尋/計算/查詢）
  3. 執行並觀察結果
  4. 判斷是否足夠
  5. 生成回答或繼續搜尋
```

## Self-RAG 與反思

2024 年 Self-RAG 引入自我反思：LLM 判斷檢索到的文檔是否相關、是否足夠、是否需要更多輪次。

```python
class AgenticRAG:
    def answer(self, query, max_steps=5):
        context = []
        for step in range(max_steps):
            # 選擇檢索策略
            strategy = self.select_strategy(query, context)
            if strategy == "vector_search":
                docs = self.vector_search(query)
            elif strategy == "kg_query":
                docs = self.kg_query(query)
            elif strategy == "sql_query":
                docs = self.sql_query(query)
            context.extend(docs)
            # 自我評估
            if self.is_sufficient(query, context):
                break
        return self.generate(query, context)
```

## 2025-2028 發展

2025 年 ReAct 模式廣泛用於 Agentic RAG，2026 年多代理協作（檢索代理、推理代理、驗證代理），2027 年記憶驅動的 Agentic RAG（長期記憶+短期記憶），2028 年自主規劃式 RAG（LLM 制定多步檢索計畫）。

## 關鍵設計模式

```python
# 工具註冊與選擇
TOOLS = {
    "search": "Google 搜尋",
    "wiki": "維基百科查詢",
    "calc": "數學計算",
    "db": "資料庫查詢",
}
def agentic_rag(query):
    plan = llm_plan(query)           # 制定計畫
    for step in plan:
        result = execute(step.tool)  # 執行步驟
        if llm_check(result):        # 驗證結果
            continue
        else:
            step = llm_revise(step)  # 修正步驟
    return llm_synthesize(query)
```

## 延伸閱讀

- [Self-RAG 自我反思](https://www.google.com/search?q=Self+RAG+self+reflection+retrieval+2024)
- [ReAct Agent 模式](https://www.google.com/search?q=ReAct+agent+LLM+pattern+2023)
- [多代理 RAG 系統](https://www.google.com/search?q=multi+agent+RAG+system+2026)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之五。*
