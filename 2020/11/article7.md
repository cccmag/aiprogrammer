# GPT-3 開放 API：大型語言模型的商業化

## 前言

GPT-3 於 2020 年 6 月發布後，OpenAI 在 2020 年 11 月開始向特定合作夥伴開放 API，開創了 AI 即服務的新商業模式。

## GPT-3 API

```python
import openai

openai.api_key = "your-api-key"

response = openai.Completion.create(
    engine="davinci",
    prompt="翻譯成中文: Hello, how are you?",
    max_tokens=50,
    temperature=0.7
)

print(response.choices[0].text.strip())
```

## 應用場景

```
GPT-3 應用：
────────────────────────────────

1. 文案生成
   └── 廣告、郵件、社交媒體

2. 程式碼輔助
   └── 程式碼補全、解釋

3. 對話系統
   └── 客服、個人助理

4. 知識問答
   └── 問答系統、研究輔助
```

## 商業模式

```
AI 即服務：
────────────────────────────────

- 按 token 計費
- 適合各種規模的應用
- 降低 AI 應用開發門檻
- 開啟新的商業模式
```

## 延伸閱讀

- [OpenAI API 文檔](https://www.google.com/search?q=OpenAI+GPT-3+API+documentation)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*