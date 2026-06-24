# ChatGPT 技術解密

## 不僅是聊天機器人

ChatGPT 看起來像一個聊天機器人，但它的技術深度遠超於此。從底層模型到產品面設計，ChatGPT 整合了 OpenAI 多年來在多個方向的研究成果。

## 底層模型：GPT-3.5

ChatGPT 基於「gpt-3.5-turbo」引擎。這個引擎是 text-davinci-003 的對話優化版本，它繼承了 GPT-3 的架構，但經過了多輪改進：

### GPT-3 → GPT-3.5 的進化

| 能力 | GPT-3 (2020) | GPT-3.5 (2022) |
|------|-------------|----------------|
| 指令遵循 | 差 | 優 |
| 多輪對話 | 無上下文 | 維持數千 token |
| 安全性 | 弱 | 強（RLHF） |
| 程式碼 | 基礎 | Codex 級別 |
| 推理能力 | 弱 | Chain-of-Thought |

## RLHF：人類回饋強化學習

這是 ChatGPT 最核心的技術創新。RLHF 解決了 LLM 的一個根本問題：模型在大量網路文本上訓練，學會了網路上的所有模式——包括有害、偏見和虛假的內容。

### 三步驟訓練流程

```
步驟 1: 監督微調（SFT）
  收集人工撰寫的對話範例
  在這些高品質數據上微調 GPT-3.5
  輸出: SFT 模型

步驟 2: 獎勵模型（RM）
  對同一提示生成多個回應
  人工排序這些回應的品質
  訓練一個獎勵模型來預測人類偏好
  輸出: 獎勵模型

步驟 3: PPO 強化學習
  使用 PPO 演算法根據獎勵模型優化 SFT 模型
  避免模型偏離 SFT 模型太遠（KL 懲罰）
  輸出: ChatGPT
```

### PPO 的目標函數

```python
# 簡化的 PPO 目標
objective = expected_reward - beta * kl_divergence
# expected_reward: 獎勵模型的評分
# kl_divergence: 與原始 SFT 模型的距離
# beta: 控制探索範圍
```

## 對話格式的秘密

ChatGPT 的對話能力來自特殊的訓練格式。每個對話被表示為：

```
<|im_start|>system
你是一個有用的 AI 助手。<|im_end|>
<|im_start|>user
Python 如何排序列表？<|im_end|>
<|im_start|>assistant
你可以使用 sorted() 函式或 .sort() 方法。<|im_end|>
```

這個格式讓模型學會了三個關鍵能力：

- **角色辨識**：區分 system / user / assistant 三種角色
- **上下文維持**：理解對話歷史，保持連貫性
- **邊界處理**：知道何時開始和結束回應

## ChatGPT 的限制

儘管驚人，ChatGPT 仍有重要限制：

- **幻覺（Hallucination）**：可以自信地給出錯誤答案
- **知識截止**：訓練數據截止於 2021 年 9 月
- **數學計算**：基本算術可能出錯
- **偏見**：訓練數據中的社會偏見仍然存在
- **Token 限制**：一次對話約 4096 token 的上限

## 延伸閱讀

- [ChatGPT 官方介紹](https://www.google.com/search?q=ChatGPT+OpenAI+overview+2022)
- [InstructGPT / RLHF 論文](https://www.google.com/search?q=Training+Language+Models+to+Follow+Instructions+with+Human+Feedback)
- [PPO 演算法](https://www.google.com/search?q=Proximal+Policy+Optimization+algorithms)
- [ChatGPT 對話格式](https://www.google.com/search?q=ChatGPT+chat+format+system+user+assistant)
- [GPT-3.5 技術細節](https://www.google.com/search?q=GPT-3.5+technical+details+OpenAI)
