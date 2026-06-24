# 5. 微調策略與應用

## 預訓練 + 微調範式

BERT 的核心優勢之一是「預訓練 + 微調」範式。預訓練階段，模型在大規模通用語料上學習語言表示；微調階段，針對特定任務調整模型參數。這種遷移學習方式大幅降低了 NLP 任務的資料需求。

微調時，整個 BERT 模型連接任務特定輸出層，採用任務相關的損失函數進行訓練。由於預訓練已經提供了良好的初始參數，微調通常收斂快速且效果優異。

## 常見 NLP 任務的微調方式

### 分類任務
加入 [CLS] token 的分類層，輸出類別機率。適用於情感分析、垃圾郵件檢測等。

### 問答任務
加入問答跨度預測層，輸出答案的起始與結束位置。適用於 SQuAD 等閱讀理解任務。

### 序列標注
每個 token 位置輸出標籤，適用於命名實體識別、詞性標注等。

### 句子對任務
將兩個句子拼接，預測關係類別。適用於自然語言推理、語義相似度等。

## 微調超參數建議

| 任務 | 學習率 | 批次大小 | Epochs |
|------|--------|----------|--------|
| 分類 | 2e-5 ~ 5e-5 | 16 ~ 32 | 2 ~ 4 |
| 問答 | 3e-5 ~ 5e-5 | 32 ~ 48 | 2 ~ 4 |
| 序列標注 | 2e-5 ~ 5e-5 | 16 ~ 32 | 3 ~ 5 |

較大的學習率通常效果較好，但需配合 warmup 策略。

## 資料增強技巧

微調時可採用以下資料增強方法：
- **回譯**：將文本翻譯為其他語言再翻回
- **同義詞替換**：隨機替換為同義詞
- **Back-translation**：用 BERT 預測 [MASK] 位置替換原詞
- **EDA**：隨機刪除、交換、替換詞彙

## 注意事項

1. **任務適配性**：不是所有任務都適合 BERT，某些簡單任務可能殺雞焉用牛刀
2. **計算資源**：大模型微調需要 GPU 記憶體足夠（Base 模型約需 12GB GPU）
3. **過擬合**：微調資料少時容易過擬合，可使用較小的學習率或 early stopping

## 參考資源

- https://www.google.com/search?q=BERT+fine-tuning+strategy+pre-trained+transfer+learning+NLP+tasks
- https://www.google.com/search?q=BERT+fine-tuning+hyperparameters+learning+rate+batch+size+recommendations
- https://www.google.com/search?q=BERT+fine-tuning+text+classification+question+answering+NER+applications