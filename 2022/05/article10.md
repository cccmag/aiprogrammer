# 從語言模型到對話 AI

## 對話系統的演進

從 1960 年代的 Eliza 到 2022 年的 ChatGPT，對話 AI 經歷了漫長的發展歷程。

## 第一代：規則驅動

### Eliza（1966）

Eliza 是最早的聊天機器人，使用模式匹配和模板回應：

```
用戶：我今天心情不好
Eliza：為什麼你覺得心情不好？
用戶：因為我失戀了
Eliza：失戀是什麼感覺？
```

Eliza 使用簡單的規則（將「我」替換為「你」、關鍵詞觸發等），但許多用戶仍然覺得它在「理解」他們。

## 第二代：檢索式

檢索式對話系統從知識庫中選取最合適的回應：

```python
def retrieve_response(query, knowledge_base):
    # TF-IDF 計算語義相似度
    query_vec = tfidf_vectorize(query)
    best_score = -1
    best_response = None

    for question, answer in knowledge_base:
        question_vec = tfidf_vectorize(question)
        score = cosine_similarity(query_vec, question_vec)
        if score > best_score:
            best_score = score
            best_response = answer

    return best_response if best_score > threshold else "我不太明白你的意思"
```

## 第三代：生成式

Seq2Seq 模型讓對話系統可以「生成」而非「選擇」回應：

```python
class Seq2SeqChatbot:
    def __init__(self):
        self.encoder = LSTMEncoder()
        self.decoder = AttentionDecoder()

    def respond(self, user_input):
        # 編碼：將輸入轉為向量
        context = self.encoder(user_input)
        # 解碼：逐步生成回應
        response = self.decoder.generate(context)
        return response
```

## 第四代：大規模預訓練模型

GPT 系列的出現徹底改變了對話 AI 的格局：

### GPT-3 對話能力

GPT-3 在 zero-shot 設定下就能進行合理的對話：

```python
prompt = """
以下是人類和 AI 助理的對話。

人類：你好，請問今天天氣如何？
AI：您好！我目前無法查詢即時天氣資訊，但我可以幫您分析天氣相關的問題。

人類：推薦一本程式設計的書
AI："""
```

### RLHF：對齊人類偏好

ChatGPT 的核心技術是 RLHF（Reinforcement Learning from Human Feedback）：

```
1. 收集人類對模型輸出的偏好資料
2. 訓練獎勵模型（Reward Model）預測人類偏好
3. 使用強化學習（PPO）優化語言模型
```

## 對話 AI 的核心挑戰

| 挑戰 | 說明 | 進展 |
|------|------|------|
| 一致性 | 不矛盾 | RLHF 改善 |
| 事實性 | 不胡說 | 檢索增強生成 |
| 安全性 | 不有害 | 內容過濾 |
| 個性化 | 記住用戶 | 記憶機制 |
| 多輪 | 上下文管理 | 長上下文視窗 |

## 重要里程碑

- **2014**：Seq2Seq + Attention（Vinyals & Le）
- **2017**：Transformer（Vaswani）
- **2019**：GPT-2 對話能力
- **2020**：GPT-3 in-context learning
- **2022**：ChatGPT（RLHF + GPT-3.5）

## 未來方向

- **多模態對話**：文字 + 圖像 + 語音
- **工具使用**：API 調用、程式執行
- **長期記憶**：持續學習與記憶
- **協作決策**：與人類共同解決複雜問題

## 延伸閱讀

- [RLHF 解釋](https://www.google.com/search?q=reinforcement+learning+from+human+feedback+explained)
- [ChatGPT 技術分析](https://www.google.com/search?q=how+ChatGPT+works)
- [對話 AI 歷史](https://www.google.com/search?q=history+of+conversational+AI+chatbots)
