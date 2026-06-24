# 大型語言模型競賽：GPT-4、PaLM、LLaMA

## 2022 年的 LLM 軍備競賽

2022 年是大型語言模型競爭最激烈的一年。Google、OpenAI、Meta、DeepMind 等科技巨頭輪番發布新模型，參數量從千億級突破到五千億級。這一章回顧這場競賽的核心玩家與技術路線。

## 參賽者

### Google PaLM（540B）

2022 年 4 月，Google 發表 Pathways Language Model（PaLM），以 5400 億參數成為當時最大的密集語言模型。PaLM 在數百個 NLP 基準測試中取得最先進成績，特別是在推理和程式碼生成任務上表現突出。

PaLM 的關鍵創新在於「Pathways」架構——一個可以跨多個 TPU v4 pod 高效訓練的系統。PaLM 在 6144 顆 TPU v4 上訓練了約 1200 萬美元等值的計算資源。

### OpenAI GPT-3.5 / GPT-4 預兆

OpenAI 的 GPT-3.5 系列包括 text-davinci-003 和 gpt-3.5-turbo。雖然 OpenAI 沒有公布 GPT-3.5 的具體參數量（據估計約 1750 億），但其在指令遵循和對話能力上超越了所有競爭對手。

值得注意的是，2022 年底已有 GPT-4 即將發布的傳聞。OpenAI 在 2022 年完成了 GPT-4 的訓練，其多模態能力（文字 + 影像輸入）在內部測試中已展現驚人表現。

### Meta LLaMA（2023 預告）

Meta 在 2022 年底完成了 LLaMA（Large Language Model Meta AI）的訓練，並於 2023 年 2 月發布。LLaMA 的核心論點是：**在更多數據上訓練的小模型可以達到與大模型相當的性能**。LLaMA-13B（130 億參數）在許多基準測試上超越了 GPT-3（1750 億參數）。

LLaMA 的開源授權引發了開源 LLM 運動，雖然其授權要求研究用途，但模型權重很快被洩漏到網路上。

### DeepMind Chinchilla

DeepMind 在 2022 年發表了 Chinchilla，一個 700 億參數的模型。Chinchilla 的核心結論是：**大多數 LLM 的訓練數據不足**。根據 DeepMind 的「Compute Optimal」理論，對於給定的計算預算，應該在更大的數據集上訓練更小的模型。Chinchilla 的訓練數據量是 GPT-3 的 5 倍。

### Anthropic Claude

由前 OpenAI 研究員成立的 Anthropic 在 2022 年開始測試 Claude 模型。Claude 聚焦於「憲法 AI」（Constitutional AI）——透過一組原則而非人類回饋來引導模型行為。這代表了 RLHF 之外的另一條安全路線。

## 湧現能力

2022 年的研究揭示了一個重要現象：**湧現能力**。當模型規模超過某個閾值時，它會突然獲得在較小模型上不存在的能力：

- **思維鏈推理**（Chain-of-Thought）：讓模型逐步推理的能力
- **指令遵循**：理解和執行複雜指令的能力
- **上下文學習**：僅從範例中學習新任務的能力

這些湧現能力是 ChatGPT 成功的根本原因，也是 LLM 競賽的核心驅動力。

## 訓練成本比較

| 模型 | 參數量 | 估計訓練成本 | 發布時間 |
|------|--------|-------------|---------|
| GPT-3 | 175B | ~400 萬美元 | 2020.06 |
| PaLM | 540B | ~1200 萬美元 | 2022.04 |
| Chinchilla | 70B | ~200 萬美元 | 2022.05 |
| GPT-3.5 | ~175B | 未公開 | 2022.03 |
| LLaMA-65B | 65B | ~500 萬美元 | 2023.02 |

## 2022 年 LLM 競賽的結論

1. **規模不是唯一答案**：Chinchilla 和 LLaMA 證明，數據質量和訓練效率同樣重要
2. **湧現能力改變遊戲規則**：找到正確的湧現閾值比無限制擴張更關鍵
3. **安全對齊成為核心議題**：模型越強大，確保其行為安全的難度越高
4. **開源陣營崛起**：LLaMA 的開源將在 2023 年引發新一波創新

## 延伸閱讀

- [PaLM 論文](https://www.google.com/search?q=PaLM+Scaling+Language+Modeling+with+Pathways)
- [Chinchilla 論文](https://www.google.com/search?q=Chinchilla+compute+optimal+large+language+models)
- [LLaMA 論文](https://www.google.com/search?q=LLaMA+Meta+open+efficient+foundation+language+models)
- [Emergent Abilities 論文](https://www.google.com/search?q=Emergent+Abilities+of+Large+Language+Models)
- [Scaling Laws](https://www.google.com/search?q=Scaling+Laws+for+Neural+Language+Models)
