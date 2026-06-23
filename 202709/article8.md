# 自然語言查詢資料庫（NL2SQL）

## 1. NL2SQL 的發展與挑戰

NL2SQL（Natural Language to SQL）讓使用者用自然語言查詢資料庫，無需學習 SQL 語法。從 2017 年 Seq2SQL 到 2026 年的 LLM-based 方案，NL2SQL 的精確度從 60% 提升到了 90% 以上。然而，生產環境中的挑戰遠比基準測試複雜。

## 2. LLM-based NL2SQL 架構

### 2.1 Schema 感知的提示工程

```python
import openai
import sqlite3

class NL2SQLConverter:
    def __init__(self, schema_info, db_path):
        self.schema_info = schema_info
        self.conn = sqlite3.connect(db_path)

    def _build_prompt(self, question):
        return f"""
你是 SQLite 資料庫專家。根據以下資料庫 Schema：

{self.schema_info}

回答使用者的自然語言問題，只輸出 SQL 查詢語句。

使用者的問題：{question}

SQL 查詢：
"""

    def query(self, question):
        prompt = self._build_prompt(question)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt}
            ],
            temperature=0
        )
        sql = response.choices[0].message.content.strip()
        sql = self._clean_sql(sql)

        try:
            cursor = self.conn.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return sql, columns, results
        except Exception as e:
            return sql, None, f"執行錯誤：{e}"
```

### 2.2 Schema 表示策略

Schema 的表示方式直接影響轉換品質：

```python
schema_info = """
資料表：employees（員工）
- id INTEGER PRIMARY KEY：員工編號
- name TEXT NOT NULL：員工姓名
- department TEXT：所屬部門
- salary REAL：月薪
- hire_date DATE：到職日期

資料表：projects（專案）
- id INTEGER PRIMARY KEY：專案編號
- name TEXT UNIQUE：專案名稱
- budget REAL：預算金額
- manager_id INTEGER REFERENCES employees(id)：專案經理

常見查詢範例：
- 前 10 大專案：SELECT * FROM projects ORDER BY budget DESC LIMIT 10
- 各部門平均薪資：SELECT department, AVG(salary) FROM employees GROUP BY department
"""
```

## 3. 進階技術

### 3.1 少樣本學習（Few-shot）

在提示中加入與問題相似的範例可以顯著提升準確率：

```python
def get_few_shot_examples(question, example_db):
    """從範例資料庫中找出與問題最相似的範例查詢"""
    # 使用嵌入模型將問題和範例轉為向量
    question_vec = embed_model.encode(question)
    example_vecs = embed_model.encode(
        [ex["question"] for ex in example_db]
    )
    # 找到最相似的 3 個範例
    similarities = cosine_similarity(
        question_vec, example_vecs
    )
    top_indices = np.argsort(similarities)[-3:]
    return [example_db[i] for i in top_indices]
```

### 3.2 安全保護（Guardrails）

NL2SQL 最大的風險是**破壞性查詢**：

```python
import re

class SQLGuardrail:
    DANGEROUS_KEYWORDS = ["DROP", "DELETE", "TRUNCATE",
                          "ALTER", "UPDATE", "INSERT",
                          "CREATE", "GRANT", "EXEC"]

    DANGEROUS_PATTERNS = [
        r"DROP\s+(TABLE|DATABASE|INDEX)",
        r"DELETE\s+FROM",
        r"ALTER\s+TABLE.*DROP",
    ]

    def validate(self, sql):
        sql_upper = sql.upper()
        for keyword in self.DANGEROUS_KEYWORDS:
            if re.search(
                rf"\b{keyword}\b", sql_upper
            ):
                return False
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, sql_upper):
                return False
        return True
```

### 3.3 自我修正（Self-Correction）

當生成的 SQL 執行失敗時，讓 LLM 自行除錯：

```python
def query_with_self_correction(self, question, max_attempts=3):
    for attempt in range(max_attempts):
        sql, columns, results = self.query(question)
        if isinstance(results, str) and "錯誤" in results:
            error_msg = results
            prompt = f"""先前生成的 SQL 執行錯誤：
問題：{question}
SQL：{sql}
錯誤：{error_msg}
請修正 SQL 查詢："""
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            sql = response.choices[0].message.content.strip()
            self.last_attempt = attempt + 1
        else:
            return sql, columns, results
    return sql, None, "無法生成正確的 SQL"
```

## 4. 效能評估

| 模型 | Spider 準確率 | Bird 準確率 | 平均延遲 |
|------|-------------|------------|---------|
| GPT-4o | 87.6% | 72.3% | 1.2s |
| Claude 3.5 | 85.2% | 70.1% | 1.5s |
| CodeLlama 34B | 73.1% | 58.4% | 0.8s |
| Text2SQL 微調模型 | 79.4% | 63.7% | 0.3s |

## 5. 生產環境最佳實務

- **限制查詢時間**：設定 SQL 執行逾時（預設 5 秒）
- **限制回傳筆數**：自動加上 `LIMIT 100` 避免 OOM
- **查詢分類**：區分「查詢型」和「分析型」問題，使用不同的提示
- **語意快取**：相同語意的問題可直接回傳快取結果
- **人工審核**：寫入操作的 SQL 需經人工確認

## 6. 多輪對話上下文

```python
class ConversationalNL2SQL:
    def __init__(self, schema_info):
        self.schema_info = schema_info
        self.history = []

    def chat(self, question):
        context = "\n".join([
            f"Q: {h['q']}\nSQL: {h['sql']}"
            for h in self.history[-3:]
        ])
        prompt = f"Schema:\n{self.schema_info}\n\n歷史上下文：\n{context}\n\n問題：{question}\nSQL："
        sql = generate_sql(prompt)
        results = execute_sql(sql)
        self.history.append({"q": question, "sql": sql})
        return sql, results
```

## 參考資料

- [Spider NL2SQL 基準測試](https://www.google.com/search?q=Spider+NL2SQL+dataset+benchmark)
- [Bird-SQL 基準測試](https://www.google.com/search?q=Bird+SQL+benchmark+2024)
- [NL2SQL 提示工程](https://www.google.com/search?q=NL2SQL+prompt+engineering+best+practices)
