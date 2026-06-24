# GPT-3 API 入門：如何申請與使用

## 前言

2020 年 7 月，OpenAI 開放了 GPT-3 API 的申請通道。本文將帶領讀者了解如何申請、使用 GPT-3 API，以及相關的費用和限制。

---

## 一、申請流程

### 1.1 註冊 OpenAI 帳號

前往 [OpenAI 官方網站](https://openai.com/) 註冊帳號。

### 1.2 申請 API 訪問

由於 GPT-3 初期產能有限，需要申請訪問權限：

1. 填寫申請表單
2. 說明使用目的
3. 等待審核（通常數天至數週）

### 1.3 獲取 API Key

審核通過後，在 Dashboard 中取得 API Key：

```python
import openai

openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 二、基本使用

### 2.1 安裝 OpenAI Python 套件

```bash
pip install openai
```

### 2.2 最簡單的範例

```python
import openai

response = openai.Completion.create(
    engine="davinci",
    prompt="The quick brown fox jumps over the",
    max_tokens=50
)

print(response.choices[0].text)
```

### 2.3 使用 Curie 模型

不同模型的費用和速度不同：

| 模型 | 速度 | 費用 | 適用場景 |
|------|------|------|---------|
| Davinci | 慢 | 高 | 高品質任務 |
| Curie | 中 | 中 | 平衡選擇 |
| Babbage | 快 | 低 | 簡單任務 |
| Ada | 最快 | 最低 | 簡單分類 |

---

## 三、Prompt 設計

### 3.1 基本 Prompt

```python
response = openai.Completion.create(
    engine="davinci",
    prompt="Translate to French: Hello, how are you?",
    max_tokens=100
)
```

### 3.2 Few-shot Prompt

```python
prompt = """Sentiment Analysis:
Review: This movie is amazing! -> Positive
Review: Terrible service. -> Negative
Review: It was okay. -> Neutral
Review: I love the new design! ->"""

response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=10
)
```

### 3.3 溫度設定

```python
response = openai.Completion.create(
    engine="davinci",
    prompt="Write a short poem about AI:",
    max_tokens=100,
    temperature=0.8  # 越低越確定，越高越有創意
)
```

---

## 四、費用計算

### 4.1 按 Token 計費

API 按輸入和輸出的 token 數量收費：

```python
# Davinci 模型
# $0.06 / 1000 tokens (輸入)
# $0.06 / 1000 tokens (輸出)
```

### 4.2 成本優化

1. 使用適合任務的最小模型
2. 減少不必要的 max_tokens
3. 快取常見 Prompt 的結果

---

## 五、實際應用範例

### 5.1 文字分類

```python
def classify_sentiment(text):
    prompt = f"""Classify the sentiment as positive, negative, or neutral:
    
Text: {text}
Sentiment:"""
    
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=1
    )
    
    return response.choices[0].text.strip()

# 使用
result = classify_sentiment("I love using GPT-3!")
print(result)  # "positive"
```

### 5.2 文字摘要

```python
def summarize(text, max_length=50):
    prompt = f"""Summarize the following text in {max_length} words or less:
    
{text}

Summary:"""
    
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=max_length
    )
    
    return response.choices[0].text.strip()
```

### 5.3 程式碼生成

```python
def generate_code(description):
    prompt = f"""Write Python code for: {description}
    
```python
"""
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=200
    )
    
    return response.choices[0].text.strip()
```

---

## 六、最佳實踐

### 6.1 Prompt 設計技巧

1. **明確任務**：清晰說明你想要的輸出格式
2. **提供範例**：Few-shot 學習效果更好
3. **限制輸出**：使用 max_tokens 避免過長輸出

### 6.2 錯誤處理

```python
import openai
import time

def call_api_with_retry(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=100
            )
            return response.choices[0].text
        except openai.error.RateLimitError:
            time.sleep(2 ** i)  # 指數退避
    return None
```

### 6.3 安全考量

- 不要在 Prompt 中包含敏感資訊
- 對輸出進行驗證
- 實作速率限制

---

## 結語

GPT-3 API 為開發者提供了一個強大的 NLP 工具。雖然 2020 年時存取受限，但隨著時間推移，這些限制已逐步放寬。掌握 API 使用方法，將為你的應用程式帶來強大的語言處理能力。

---

*延伸閱讀：[OpenAI API 文檔](https://www.google.com/search?q=OpenAI+GPT-3+API+documentation+2020)*