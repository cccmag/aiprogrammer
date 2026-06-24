# 自然語言推理任務

## NLI 任務定義

自然語言推理（Natural Language Inference, NLI）又稱為文本蘊含（Textual Entailment），任務定義：

給定一個前提（premise）和一個假設（hypothesis），判斷它們之間的語義關係：
- **Entailment（蘊含）**：若前提為真，則假設必定為真
- **Contradiction（矛盾）**：前提為真時，假設必定為假
- **Neutral（中立）**：前提為真時，假設可能為真也可能為假

## NLI 的重要性

NLI 是 NLP 領域的核心任務之一，因為理解句子間的語義關係是很多進階 NLP 應用的基礎：
- 閱讀理解需要判斷問題與文章內容的關係
- 對話系統需要理解使用者意圖與系統回覆的關係
- 自動摘要需要判斷摘要與原文的一致性

## 基準資料集

### SNLI（Stanford Natural Language Inference）
- 57 萬個人工标注的句子對
- 由圖書描述與英文 Flickr 描述生成
- 三大類別均衡分布

### MultiNLI
- 43 萬句子對
- 涵蓋口語與書面語
- 考驗模型的泛化能力

### MNLI-m（matched）與 MNLI-mm（mismatched）
測試集與訓練集領域匹配/不匹配的表現。

## BERT 在 NLI 的表現

BERT 在 NLI 任務上顯著超越以往方法：

| 模型 | 準確率 |
|------|--------|
| ESIM | 78.9% |
| DIIN | 78.8% |
| BERT-base | 84.6% |
| BERT-large | 86.7% |

提升來自於：
1. 雙向預訓練學習深層語義表示
2. 預訓練時的 NSP 任務直接學習句子關係
3. Transformer 有效捕捉長距離依賴

## BERT 處理 NLI 的方式

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# 編碼前提與假設
premise = "A soccer game with multiple males playing."
hypothesis = "Some men are playing a sport."
encoded = tokenizer(premise, hypothesis, return_tensors='pt', padding=True)

# 預測
outputs = model(**encoded)
prediction = torch.argmax(outputs.logits, dim=-1)
# 0: entailment, 1: neutral, 2: contradiction
```

## 實務技巧

1. **資料增強**：同義詞替換、回譯
2. **類別加權**：若類別不平衡，使用加權損失
3. **學習率调度**：使用 warmup 策略
4. **Early stopping**：避免過擬合

## 參考資源

- https://www.google.com/search?q=NLI+自然语言推理+任务+文本蕴含+SNLI+MultiNLI+详解
- https://www.google.com/search?q=BERT+NLI+自然语言推理+BERT-base+accuracy+performance+comparison
- https://www.google.com/search?q=BERT+处理+NLI+任务+代码+示例+PyTorch+教程