# GPT-3 發表：語言模型的新突破

## 2020 年 7 月：NLP 領域的轉折點

### 歷史背景

2020 年 7 月，OpenAI 發表了 GPT-3 論文「Language Models are Few-Shot Learners」。這篇論文標誌著大型語言模型（Large Language Model, LLM）時代的來臨。

### GPT-3 的規模

GPT-3 擁有 **1750 億參數**，是當時史上最大的語言模型：

| 版本 | 發布時間 | 參數數量 |
|------|---------|---------|
| GPT-1 | 2018 年 6 月 | 1.17 億 |
| GPT-2 | 2019 年 2 月 | 15 億 |
| GPT-3 | 2020 年 7 月 | 1750 億 |

這意味著 GPT-3 的參數量是 GPT-2 的 **117 倍**。

### 論文的主要貢獻

1. **展示少樣本學習能力**：GPT-3 可以在完全未見過的任務上表現良好，只需在輸入中提供少量範例。

2. **顛覆傳統認知**：過去認為需要大規模標記資料才能完成任務，GPT-3 證明了大量無監督預訓練的威力。

3. **統一的模型架構**：使用單一的語言模型完成各式各樣的任務。

### 為何規模如此重要

規模的提升帶來了「湧現能力」（Emergent Abilities）：

- **較小模型**（GPT-2 等）：需要大量任務相關的監督資料
- **超大模型**（GPT-3）：開始展現泛化和推理能力

### GPT-3 的架構

GPT-3 採用 Transformer 解碼器架構：
- 96 層 Transformer
- 每層 96 個注意力頭
- Embedding 維度 12288
- 使用 Sparse Attention 技術

### 訓練資料

GPT-3 的訓練資料來自：
- Common Crawl（60%）
- WebText2（22%）
- Books1（8%）
- Books2（8%）
- Wikipedia（3%）

### 歷史的意義

GPT-3 的發表開啟了大型語言模型的競爭時代。各大科技公司開始競相訓練更大規模的模型，推動了 NLP 領域的快速發展。

---

**下一步**：[Few-shot Learning：從頭訓練到提示學習](focus2.md)

## 延伸閱讀

- [GPT-3 論文原文](https://www.google.com/search?q=GPT-3+Language+Models+are+Few-Shot+Learners+paper+2020)
- [OpenAI+GPT-3+官方部落格](https://www.google.com/search?q=OpenAI+GPT-3+announcement+2020)
- [大型語言模型發展歷程](https://www.google.com/search?q=history+large+language+models+LLM)