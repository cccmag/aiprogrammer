# GPT-3 API 與應用開發

## OpenAI API 實務

### API 存取方式

GPT-3 API 提供 RESTful 接口，支持多種程式語言：

```python
import openai

openai.api_key = "your-api-key"

response = openai.Completion.create(
    model="davinci",
    prompt="翻譯成英文：你好，今天天氣如何？",
    max_tokens=100
)
```

### 可用模型

| 模型 | 參數 | 說明 |
|------|------|------|
| davinci | 175B | 最強大，適合複雜任務 |
| curie | 6.7B | 平衡效能與速度 |
| babbage | 1.3B | 簡單任務，高速 |
| ada | 350M | 最快，最輕量 |

### API 參數詳解

```python
{
    "model": "davinci",        # 模型選擇
    "prompt": "...",           # 輸入提示
    "max_tokens": 100,         # 最大生成的詞元數
    "temperature": 0.7,         # 創造性（0-1）
    "top_p": 1.0,              # 核採樣機率
    "n": 1,                    # 生成數量
    "stop": None               # 停止符號
}
```

### 應用場景

1. **文字生成**：文章、故事、詩歌
2. **程式碼輔助**：代碼補全、解釋、轉換
3. **對話系統**：聊天機器人、客服
4. **內容改寫**：摘要、翻譯、校對

### 費用考量

API 按使用的詞元計費：
- Davinci：$0.06/1000 tokens
- Curie：$0.006/1000 tokens
- Ada：$0.0008/1000 tokens

### 開發建議

- 從小模型開始測試
- 使用 caching 減少費用
- 妥善處理 rate limit

---

## 延伸閱讀

- [OpenAI API 官方文檔](https://www.google.com/search?q=OpenAI+API+documentation)
- [API Pricing](https://www.google.com/search?q=OpenAI+API+pricing+davinci+curie)
- [Best Practices+API+Usage](https://www.google.com/search?q=OpenAI+API+best+practices)