# ChatGPT 的技術綜述

## ChatGPT 是什麼

ChatGPT 是 OpenAI 於 2022 年 11 月 30 日發布的對話 AI 系統，基於 GPT-3.5 系列模型，通過 InstructGPT 的 RLHF 微調技術進行訓練。

## InstructGPT 架構

ChatGPT 的基礎是 InstructGPT，這是對 GPT-3 進行微調後的版本，旨在更好地遵循使用者的指令。InstructGPT 的訓練分為三個階段：

### 第一階段：監督式微調（SFT）

收集人類標註者編寫的「指令-回應」對資料，對 GPT-3 進行監督式微調。這個階段讓模型學會遵循指令的基本能力。

### 第二階段：獎勵模型訓練

人類標註者對 SFT 模型的多個輸出進行排序，使用這些排序資料訓練一個獎勵模型（Reward Model, RM），用於預測人類偏好。

```
輸入：指令 + 多個候選回覆
輸出：人類偏好分數
```

### 第三階段：強化學習（PPO）

使用 PPO（近端策略優化）演算法，讓語言模型以獎勵模型為指導進行強化學習。模型在生成對話時，會傾向於產生獎勵模型偏好的回應。

## GPT-3.5 模型家族

ChatGPT 使用的 GPT-3.5 系列包括多個變體：

- **text-davinci-003**：InstructGPT 的最終版本
- **code-davinci-002**：針對程式碼優化的版本
- **GPT-3.5-turbo**：ChatGPT 使用的推理優化版本

## 核心能力

ChatGPT 展示了多項突破性能力：

- **連貫的長對話**：能夠維持長達數千輪的連貫對話
- **任務理解**：準確理解並執行複雜的指令
- **知識範圍廣**：涵蓋科學、歷史、文學、程式等多個領域
- **推理能力**：展現出初步的邏輯推理和分析能力

## 限制與挑戰

- **事實幻覺**：可能產生看似合理但實際上錯誤的資訊
- **偏見問題**：訓練資料中的社會偏見可能反映在輸出中
- **計算成本**：推理需要大量 GPU 計算資源

## 產業影響

ChatGPT 的發布引發了 AI 對話領域的激烈競爭。Google 推出 Bard、Meta 開源 LLaMA、微軟整合 ChatGPT 到 Bing，對話 AI 進入了一個全新的時代。

## 延伸閱讀

- [InstructGPT 論文](https://www.google.com/search?q=InstructGPT+RLHF+paper)
- [ChatGPT 官方介紹](https://www.google.com/search?q=ChatGPT+OpenAI+introduction)
- [RLHF 技術詳解](https://www.google.com/search?q=reinforcement+learning+from+human+feedback)
