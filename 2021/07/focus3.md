# 主題三：GPT 系列與生成式 AI

## 從 GPT-2 到 GPT-3 的演進

### 1. GPT 系列的起源

Generative Pre-trained Transformer（GPT）系列由 OpenAI 開發，首個版本於 2018 年發表。GPT 的核心思想是：**通過大規模無監督預訓練，讓模型學習通用的語言表示，然後在特定任務上進行微調**。

GPT-1：1.17 億參數
GPT-2：15 億參數（2019 年）
GPT-3：1750 億參數（2020 年）

### 2. GPT 與 BERT 的區別

雖然 GPT 和 BERT 都基於 Transformer，但它們的設計哲學截然不同：

**GPT 是 Autoregressive（自回歸）模型**：
- 只能看到左側上下文
- 適合生成任務
- 訓練時預測下一個 token

**BERT 是 Bidirectional（雙向）模型**：
- 可以看到左右兩側上下文
- 不適合生成任務（會「偷看」答案）
- 適合理解任務

### 3. GPT-2 的創新

GPT-2 於 2019 年發表，最大的創新是展示了強大的文本生成能力：

```python
def generate_text(model, prompt, max_length=100, temperature=1.0, top_k=50):
    """文字生成示例"""
    model.eval()
    input_ids = encode(prompt)

    for _ in range(max_length):
        logits = model(input_ids)
        next_token_logits = logits[-1, :] / temperature

        if top_k > 0:
            indices = torch.topk(next_token_logits, top_k).indices
            next_token_logits = torch.full_like(next_token_logits, -float('inf'))
            next_token_logits[indices] = logits[-1, indices]

        probs = F.softmax(next_token_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)

        input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=1)

        if next_token.item() == EOS_TOKEN:
            break

    return decode(input_ids)
```

GPT-2 的論文甚至提到「考慮是否延遲發布」，因為生成的文字太過流暢，引發了對 deepfake 文字的擔憂。

### 4. GPT-3 的突破

GPT-3 於 2020 年發表，1750 億參數的規模使其成為當時最大的語言模型。GPT-3 的關鍵突破是 **Few-shot Learning** 能力：

**傳統方法對比**：
- **Zero-shot**：完全不給範例
- **One-shot**：給一個範例
- **Few-shot**：給少量範例（通常 10-100 個）

```python
prompt = """翻譯以下文字為英文：

範例：
中文：我愛學習
英文：I love learning

任務：
中文：今天天氣很好
英文："""
```

GPT-3 可以在不進行梯度更新的情況下，僅通過 prompt 中的範例就能完成任務。

### 5. GPT-3 的架構與訓練

GPT-3 的架構與 GPT-2 類似，但有幾項改進：

- **Sparse Attention**：提高長序列處理效率
- **Alternating Layers**：交替使用局部和全局注意力
- **更大規模預訓練**：45TB 文字資料，3000 億 token

GPT-3 的訓練成本估計約 460 萬美元，這使其難以被一般研究者複製。

### 6. GPT-3 的應用與限制

**應用場景**：
- 文字生成與創意寫作
- 程式碼生成（Codex 的基礎）
- 問答系統
- 翻譯與摘要
- 教學輔助

**限制與挑戰**：
- **幻覺問題**：可能生成看似流暢但實際錯誤的內容
- **時效性**：無法知道最新資訊
- **計算成本**：推理需要大量計算資源
- **偏見問題**：可能學習並再現訓練資料中的偏見

### 7. 從 GPT-3 到 GPT-3.5

2021 年，OpenAI 基於 GPT-3 推出了多個變體：

- **GPT-3.5**：在 GPT-3 基礎上加入人類回饋增強學習（RLHF）
- **Codex**：專門針對程式碼訓練的版本
- **ChatGPT 的前身**：為對話優化的版本

這些模型為後續的 GPT-4 和 ChatGPT 奠定了基礎。

---

## 延伸閱讀

- [GPT-2 論文](https://www.google.com/search?q=GPT-2+language+models+are+unsupervised+multitask+learners)
- [GPT-3 論文](https://www.google.com/search?q=GPT-3+language+models+are+few-shot+learners)
- [OpenAI API 文档](https://www.google.com/search?q=OpenAI+API+GPT-3+documentation)