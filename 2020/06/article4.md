# 如何申請 GPT-3 API

## 申請流程

### 1. 前往 OpenAI 網站

前往 https://openai.com 並註冊帳戶。

### 2. 驗證電子郵件

完成驗證後，選擇適合的方案：
- Free tier：有一定額度的免費使用量
- Paid tier：付費使用更多額度

### 3. 取得 API Key

完成申請後，在 Dashboard 中取得 API Key：

```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 環境設定

```bash
pip install openai

# 設定 API key
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```python
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
# 或直接設定
openai.api_key = "sk-xxxxxxxxxxxxxx"
```

## 基本使用

```python
response = openai.Completion.create(
    model="davinci",
    prompt="Hello, world!",
    max_tokens=50
)
print(response.choices[0].text)
```

## 模型選擇

```python
# 根據任務選擇適合的模型
models = {
    "text-davinci-003": "最新最強大（2020/11）",
    "davinci": "GPT-3 系列最強",
    "curie": "平衡效能與速度",
    "babbage": "簡單任務",
    "ada": "最快，最簡單任務"
}
```

## 使用限額

```python
# 檢查使用量
import openai

usage = openai.Usage.retrieve()
print(f"已使用: {usage['total_tokens']} tokens")
print(f"限額: {usage['limit']} tokens")
```

## 錯誤處理

```python
import openai

try:
    response = openai.Completion.create(
        model="davinci",
        prompt="Hello"
    )
except openai.error.RateLimitError:
    print("已達到速率限制，請稍後再試")
except openai.error.AuthenticationError:
    print("API Key 無效")
except openai.error.InvalidRequestError as e:
    print(f"請求錯誤: {e}")
```

## 成本優化技巧

```python
# 1. 使用較小的模型（如果足夠）
# "curie" 比 "davinci" 便宜 10 倍

# 2. 最小化 Prompt
prompt = "Translate to French: Hello"  # 簡潔
prompt = "Please translate the following English text to French language. Thank you. Text: Hello"  # 冗長

# 3. 控制 max_tokens
response = openai.Completion.create(
    model="curie",
    prompt=prompt,
    max_tokens=50  # 只取需要的长度
)
```

## 組織管理

```python
# 設定組織
openai.organization = "org-xxxxxxxxxxxxx"

# 列出所有 API keys
keys = openai.api_key.list()
print(keys)
```

## 參考資源

- https://www.google.com/search?q=OpenAI+API+GPT-3+application+tutorial+signup+2020
- https://www.google.com/search?q=OpenAI+API+key+Python+setup+authentication+pricing
- https://www.google.com/search?q=OpenAI+API+usage+limits+rate+limit+error+handling