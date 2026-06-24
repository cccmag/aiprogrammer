# 4. GPT-3 API 與應用

## API 訪問方式

GPT-3 透過 OpenAI API 提供服務（2020 年中的付費測試階段）：

```python
import openai
openai.api_key = "your-api-key"

response = openai.Completion.create(
    model="davinci",  # 最強大的模型
    prompt="Translate to French: Hello, world!",
    max_tokens=50,
    temperature=0.7
)
print(response.choices[0].text)
```

## 可用模型

GPT-3 API 提供多個版本：

| 模型 | 參數量 | 特性 | 適合場景 |
|------|--------|------|---------|
| davinci | 175B | 最強大 | 複雜任務 |
| curie | 6.7B | 平衡 | 翻譯、分類 |
| babbage | 1.3B | 快速 | 簡單任務 |
| ada | 350M | 最快 | 文字處理 |

## 應用場景

### 文字生成

```python
response = openai.Completion.create(
    model="davinci",
    prompt="Once upon a time in a distant galaxy",
    max_tokens=200,
    temperature=0.8
)
```

### 程式碼生成

GPT-3 展現了令人驚艷的程式碼生成能力：

```python
response = openai.Completion.create(
    model="davinci",
    prompt="""Write a Python function to calculate fibonacci:
def fibonacci(n):""",
    max_tokens=100
)
```

### 問答系統

```python
response = openai.Completion.create(
    model="davinci",
    prompt="""Q: What is the capital of France?
A: Paris

Q: What is the capital of Germany?
A:""",
    max_tokens=20
)
```

### 文字分類

```python
response = openai.Completion.create(
    model="curie",
    prompt="""Classify the sentiment as positive or negative:
Text: This movie is amazing!
Sentiment: positive

Text: This food was terrible.
Sentiment: negative

Text: Great experience!
Sentiment:""",
    max_tokens=1
)
```

## API 參數

```python
response = openai.Completion.create(
    model="davinci",
    prompt="...",
    max_tokens=100,      # 最大生成 token 數
    temperature=0.7,     # 生成隨機性 (0-1)
    top_p=1.0,           # nucleus 採樣
    n=1,                 # 生成候選數量
    stop=None,           # 停止符號
    presence_penalty=0,  # 存在懲罰
    frequency_penalty=0  # 頻率懲罰
)
```

## 成本計算

API 按使用的 token 數量計費：
- davinci: $0.06/1000 tokens
- curie: $0.006/1000 tokens
- babbage: $0.0012/1000 tokens
- ada: $0.0008/1000 tokens

## 參考資源

- https://www.google.com/search?q=OpenAI+GPT-3+API+Python+tutorial+completion+2020
- https://www.google.com/search?q=GPT-3+davinci+curie+babbage+ada+model+comparison+capabilities
- https://www.google.com/search?q=GPT-3+API+pricing+costs+tokens+calculation+usage