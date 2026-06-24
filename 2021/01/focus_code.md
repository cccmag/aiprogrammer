# GPT-3 API 實作範例

## 前言

本篇文章展示如何使用 Python 呼叫 OpenAI GPT-3 API，進行文字生成和 Few-shot Learning 任務。

完整的 Python 實作請參考：[_code/gpt3_demo.py](_code/gpt3_demo.py)

## 核心程式碼

### 基本呼叫

```python
import openai

openai.api_key = "your-api-key"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="請用 Python 寫一個 Hello World 程式",
    max_tokens=100,
    temperature=0.7
)

print(response.choices[0].text)
```

### Few-shot Learning 範例

```python
def few_shot_translation():
    prompt = """將中文翻譯成英文：

範例：
"你好" → "Hello"
"謝謝" → "Thank you"
"對不起" → "Sorry"

待翻譯：
"我愛你" →"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )

    return response.choices[0].text
```

### 對話系統範例

```python
def chat_with_model():
    messages = [
        {"role": "system", "content": "你是個有用的助理"},
        {"role": "user", "content": "什麼是 Python？"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content
```

## 常見任務 Prompt 模板

### 文字摘要

```python
def summarize(text):
    prompt = f"""請用一句話總結以下文字：

{text}

摘要："""
    # ... API 呼叫
```

### 程式碼解釋

```python
def explain_code(code):
    prompt = f"""解釋以下 Python 程式碼的功能：

```python
{code}
```

解釋："""
    # ... API 呼叫
```

## 實作要點

### 錯誤處理

```python
try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt
    )
except openai.error.RateLimitError:
    print("配額用盡，請稍後再試")
except openai.error.APIError as e:
    print(f"API 錯誤：{e}")
```

### Token 計算

```python
import tiktoken

def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

## 執行結果

```
=== 翻譯範例 ===
輸入：我愛你
輸出：I love you

=== 程式碼解釋 ===
輸入：print("Hello")
輸出：這行程式碼在主控台印出 "Hello" 文字

=== 文字摘要 ===
輸入：Python 是一種廣泛使用的高階程式語言...
輸出：Python 是一種易學易用的程式語言
```

## 設計要點

### Prompt 優化技巧

1. **明確角色**：賦予模型特定身份
2. **結構化輸出**：指定 JSON 或 Markdown 格式
3. **逐步推理**：使用 Chain of Thought

### 成本優化

1. 選擇適合任務的模型大小
2. 使用 short polling 避免冗長來回
3. 快取常見的 prompt

---

## 延伸閱讀

- [OpenAI API 官方文檔](https://www.google.com/search?q=OpenAI+API+Python+sdk)
- [Prompt Engineering 指南](https://www.google.com/search?q=prompt+engineering+best+practices)
- [ tiktoken+Token計算](https://www.google.com/search?q=tiktoken+token+counting+python)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」補充文章。*