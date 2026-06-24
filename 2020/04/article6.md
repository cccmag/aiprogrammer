# OpenAI API 整合應用

## API 取得與設定

```bash
pip install openai
```

```python
import openai
openai.api_key = "your-api-key"
```

## 基本使用

```python
response = openai.Completion.create(
    model="davinci",
    prompt="The capital of France is",
    max_tokens=50,
    temperature=0.7
)
print(response.choices[0].text)
```

## GPT-3 模型選項

2020 年中可用的模型包括：
- `davinci`：最強大的模型
- `curie`：平衡效能與速度
- `babbage`：較快，較簡單任務
- `ada`：最快的模型

## 文字補全參數

```python
response = openai.Completion.create(
    model="davinci",
    prompt="Write a Python function to calculate fibonacci:",
    max_tokens=100,
    temperature=0.8,
    top_p=1.0,
    n=3,  # 生成多個候選
    stop=["\n\n"]  # 停止符號
)
```

## 情感分析範例

```python
def analyze_sentiment(text):
    response = openai.Completion.create(
        model="davinci",
        prompt=f"""Classify the sentiment of this text as positive, negative, or neutral:
        
        Text: {text}
        
        Sentiment:""",
        max_tokens=1,
        temperature=0.0
    )
    return response.choices[0].text.strip()

result = analyze_sentiment("I really enjoyed the movie!")
print(result)  # "positive"
```

## 錯誤處理

```python
import time

def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except openai.error.RateLimitError:
            if i < max_retries - 1:
                time.sleep(2 ** i)
            else:
                raise
        except openai.error.APIError as e:
            print(f"API Error: {e}")
            raise

response = retry_with_backoff(lambda: openai.Completion.create(
    model="davinci",
    prompt="Hello"
))
```

## 成本優化

```python
def estimate_cost(prompt, model="davinci"):
    # 估算 token 數量
    num_tokens = len(prompt.split()) * 1.3
    cost_per_1000_tokens = {
        "davinci": 0.06,
        "curie": 0.006,
        "babbage": 0.0012,
        "ada": 0.0008
    }
    return num_tokens / 1000 * cost_per_1000_tokens.get(model, 0.06)
```

## 參考資源

- https://www.google.com/search?q=OpenAI+API+GPT-3+text+completion+Python+tutorial+2020
- https://www.google.com/search?q=openai+api+parameters+temperature+top_p+max_tokens+guide
- https://www.google.com/search?q=openai+api+rate+limit+error+handling+retry+best+practices