# GPT 系列與生成式預訓練

## 自回歸語言模型

GPT（Generative Pre-trained Transformer）系列與 BERT 不同，採用了**自回歸**（autoregressive）的架構——從左到右逐步生成文字：

```
P(sequence) = P(t_1) * P(t_2|t_1) * P(t_3|t_1,t_2) * ...
```

這與傳統語言模型的定義完全一致，但 GPT 使用了 Transformer 的解碼器（遮蔽自注意力）來實現。

## GPT 的演進

### GPT-1（2018）

首次展示了「生成式預訓練 + 微調」在 NLP 任務上的有效性：

```
預訓練：大型無標註語料上的語言模型目標
微調：下游任務（分類、推理等）的有標註學習
```

參數量：117M。

### GPT-2（2019）

展示了語言模型在 zero-shot 設定下的驚人能力：

- **規模擴大到 1.5B 參數**
- **zero-shot 表現**：無需微調即可完成翻譯、問答等任務
- **生成品質**：生成文本的連貫性達到令人驚訝的水準

OpenAI 最初因安全考慮延後發布完整模型，引發了 AI 社群的廣泛討論。

### GPT-3（2020）

GPT-3 將規模推至 1750 億參數，展示了**in-context learning**的能力：

```python
# Few-shot 範例：情感分類
prompt = """
文字：這部電影太棒了！
情感：正面

文字：劇情無聊透頂
情感：負面

文字：演員表現很普通
情感："""

# GPT-3 無需參數更新，直接透過提示完成任務
response = gpt3.complete(prompt)
# 輸出: 負面
```

**In-context learning** 有三種形式：
- **Zero-shot**：只給任務描述，不給範例
- **One-shot**：給一個範例
- **Few-shot**：給多個範例

所有這些都不需要梯度更新——模型從提示中「理解」任務。

## 關鍵技術

**Transformer 解碼器**：GPT 的核心是 Masked Self-Attention，確保每個位置只能關注左側的詞：

```python
# 遮蔽注意力遮罩
mask = np.tril(np.ones((seq_len, seq_len)))  # 下三角矩陣
# 每個 token 只能看到自己和之前的 token
attention = softmax(Q @ K.T / sqrt(d_k) + mask)
```

**擴展法則**（Scaling Laws）：Kaplan 等人發現語言模型的性能與參數量、資料量、計算量之間存在冪律關係。這驅動了後續模型規模的不斷增長。

## GPT 與 BERT 的對比

| 特性 | GPT | BERT |
|------|-----|------|
| 架構 | Transformer 解碼器 | Transformer 編碼器 |
| 注意力 | 遮蔽自注意力（單向） | 雙向自注意力 |
| 訓練目標 | 自回歸語言模型 | MLM + NSP |
| 擅長任務 | 生成（翻譯、摘要、對話） | 理解（分類、標註、推理） |
| 使用方式 | 提示工程 / 微調 | 微調 |

## 生成式 AI 的開端

GPT-3 的出現標誌著生成式 AI 時代的來臨。後續發展包括：

- **Codex**（2021）：GPT-3 在程式碼上的微調變體，GitHub Copilot 的基礎
- **InstructGPT**（2022）：使用 RLHF（人類回饋強化學習）進行對齊
- **ChatGPT**（2022）：基於 InstructGPT 的對話模型，引發全球熱潮

---

**下一步**：[文章集錦首篇](article1.md)

## 延伸閱讀

- [GPT-3 論文](https://www.google.com/search?q=GPT-3+language+models+are+few+shot+learners)
- [Scaling Laws 論文](https://www.google.com/search?q=scaling+laws+for+neural+language+models)
- [In-context Learning 解讀](https://www.google.com/search?q=in+context+learning+GPT+3+explained)
