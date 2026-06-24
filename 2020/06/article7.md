# GPT-3 程式碼生成能力

## Codex 簡介

Codex 是基於 GPT-3 的程式碼生成模型，支援十餘種程式語言。GitHub Copilot 即基於 Codex 技術。

## 基本程式碼生成

```python
def generate_code(description):
    prompt = f"""Write Python code for the following:

{description}

```python
"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text
```

## 生成範例

### 排序演算法

```python
prompt = """Write a quicksort algorithm in Python:

```python
def quicksort(arr):"""
response = openai.Completion.create(model="davinci", prompt=prompt, max_tokens=200)
```

### API 端點

```python
prompt = """Write a Flask API endpoint that returns JSON:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello')"""
response = openai.Completion.create(model="davinci", prompt=prompt, max_tokens=200)
```

### SQL 查詢

```python
prompt = """Write a SQL query to find the top 10 customers by order total:

```sql
SELECT"""
response = openai.Completion.create(model="davinci", prompt=prompt, max_tokens=100)
```

## 程式碼解釋

```python
def explain_code(code):
    prompt = f"""Explain what this Python code does:

```python
{code}
```

Explanation in plain English:"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text
```

## 程式碼除錯

```python
def debug_code(code, error_message):
    prompt = f"""Find and fix the bug in this code:

Error message: {error_message}

```python
{code}
```

Fixed code:"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text
```

## 程式碼翻譯

```python
def translate_code(code, from_lang, to_lang):
    prompt = f"""Translate this {from_lang} code to {to_lang}:

```{from_lang}
{code}
```

```{to_lang}
"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text
```

## 測試生成

```python
def generate_tests(function_code):
    prompt = f"""Write unit tests for this code:

```python
{function_code}
```

```python
import unittest
"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text
```

## 限制

1. **複雜度限制**：複雜架構可能生成錯誤
2. **上下文限制**：只能看到部分程式碼
3. **最新 API**：可能不了解最新的函式庫變化
4. **安全問題**：可能生成有漏洞的程式碼

## 參考資源

- https://www.google.com/search?q=GitHub+Copilot+Codex+GPT-3+code+generation+tutorial+2020
- https://www.google.com/search?q=AI+code+generation+Python+examples+GPT-3+capabilities
- https://www.google.com/search?q=code+generation+limitations+debugging+testing+language+model