# BERT 與預訓練語言模型

## BERT 的創新

### 雙向預訓練

BERT 使用「遮罩語言模型」（MLM）：
- 隨機遮罩 15% 的 tokens
- 雙向編碼器同時考慮上下文
- 不同於 GPT 的單向語言模型

```
BERT 預訓練任務：
輸入：[CLS] 今天 [MASK] 很好 [SEP]
預測：[MASK] = 天氣
```

### 下游任務微調

BERT 在各種 NLP 任務上微調：
- 文字分類
- 問答系統
- 命名實體識別

## 預訓練-微調範式

```
預訓練階段：
- 大規模無標籤文字
- 學習通用語言表示

微調階段：
- 小規模特定任務資料
- 調整模型適應任務
```

## BERT 的變體

| 模型 | 參數量 | 創新 |
|------|--------|------|
| BERT-base | 110M | 基準模型 |
| BERT-large | 340M | 更大規模 |
| RoBERTa | 355M | 去除 Next Sentence Prediction |
| ALBERT | 12M | 參數共享 |

---

## 延伸閱讀

- [BERT+原始論文](https://www.google.com/search?q=BERT+pre-training+of+deep+bidirectional)
- [預訓練語言模型比較](https://www.google.com/search?q=BERT+vs+GPT+pretraining+differences)
- [RoBERTa+改進](https://www.google.com/search?q=RoBERTa+optimization+BERT)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*