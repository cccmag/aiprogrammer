# 1. GPT-3 技術架構

## 模型規格

GPT-3 採用與 GPT-2 相同的 Transformer 架構，但規模大幅提升：

| 版本 | 參數量 | 層數 | 注意力頭數 | 隱藏維度 |
|------|--------|------|-----------|---------|
| GPT-2 Small | 1.17 億 | 12 | 12 | 768 |
| GPT-2 Medium | 3.45 億 | 24 | 16 | 1024 |
| GPT-2 Large | 7.62 億 | 36 | 16 | 1280 |
| GPT-2 XL | 15.83 億 | 48 | 25 | 1600 |
| GPT-3 | 1750 億 | 96 | 96 | 12288 |

## 架構改進

GPT-3 相比 GPT-2 的改進：

1. **稀疏注意力**：在某些層使用局部關注與跨躍關注的組合，提升長序列處理能力
2. **旋轉位置編碼（RoPE）**：更有效的位置表示方法
3. **改進的正規化**：使用預規範化（Pre-Norm）與縮放因子

## 訓練資料

GPT-3 的訓練資料來自多個來源：
- Common Crawl（60%）
- WebText2（22%）
- Books（8%）
- Wikipedia（3%）
- 其他（7%）

總計約 3000 億個 tokens，涵蓋多種領域與語言。

## 訓練過程

GPT-3 的訓練需要龐大計算資源：
- 使用約 1000-10000 張 A100 GPU
- 訓練時間：數週至數月
- 估計計算成本：1200 萬美元

## 評估結果

GPT-3 在多個 benchmark 上刷新紀錄：
- LAMBADA（語言建模）：67%
- TriviaQA（問答）：64%
- CoQA（對話問答）：85%
- WebQuestions（知識問答）：45%

## 限制

GPT-3 仍有一些限制：
- 對事實性問題可能產生幻覺
- 數學推理能力有限
- 無法訪問即時資訊
- 對抗性攻擊的脆弱性

## 參考資源

- https://www.google.com/search?q=GPT-3+architecture+175B+parameters+Transformer+OpenAI+technical+paper+2020
- https://www.google.com/search?q=GPT-3+training+data+Common+Crawl+WebText+3000B+tokens+details
- https://www.google.com/search?q=GPT-3+sparse+attention+rotary+position+encoding+RoPE+improvements