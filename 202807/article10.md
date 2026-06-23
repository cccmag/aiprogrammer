# 生成式 AI 應用案例

## 案例一：程式碼審查 Agent

自動審查 Pull Request，檢查程式碼品質、安全漏洞與風格一致性。

```python
class CodeReviewAgent:
    def __init__(self, llm, rules):
        self.llm = llm
        self.rules = rules

    def review(self, diff_text):
        prompt = f"""請審查以下 diff：
{diff_text}

檢查項目：
{chr(10).join(f'- {r}' for r in self.rules)}

請回傳 JSON：{{"issues": [...], "score": 0-100}}"""
        result = self.llm.generate(prompt)
        return json.loads(result)
```

## 案例二：智慧客服系統

多步驟處理：意圖識別 → 知識庫檢索 → 答案生成 → 情感分析。

```python
class SmartSupportAgent:
    def route_intent(self, query):
        if "退貨" in query:
            return "return"
        elif "訂單" in query:
            return "order_status"
        return "general"

    def handle(self, query):
        intent = self.route_intent(query)
        policy = self.retrieve_policy(intent)
        draft = self.llm.generate(f"根據政策 {policy} 回答：{query}")
        sentiment = self.analyze_sentiment(draft)
        if sentiment["negative"]:
            draft = self.llm.generate(f"改寫為更友善：{draft}")
        return draft
```

## 案例三：資料分析 Agent

自然語言查詢資料庫，自動生成視覺化圖表。

```python
def data_analysis_pipeline(question):
    sql = llm.generate(f"將問題轉為 SQL：{question}")
    data = db.query(sql)
    chart_code = llm.generate(
        f"根據資料 {data} 生成 matplotlib 程式碼")
    exec(chart_code)
    return "chart.png"
```

## 案例四：個人寫作助理

多步驟生成：大綱 → 各節內容 → 摘要 → 關鍵字。搭配 ToT 選擇最佳結構。

## 總結

生成式 AI 從單一回應進化為多步驟、工具驅動的 Agent 系統。核心能力在於拆解任務、選擇工具、驗證結果、迭代修正。

更多應用案例請參考 https://www.google.com/search?q=generative+AI+agent+use+cases+2026。
