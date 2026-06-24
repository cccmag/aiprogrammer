# ELMo、BERT 與雙向編碼

## 從靜態到動態詞嵌入

Word2vec 的詞向量是靜態的——無論上下文如何，「銀行」這個詞的向量始終相同。但「我去銀行存錢」和「河岸銀行崩塌」中的「銀行」顯然有不同的含義。

**ELMo**（Embeddings from Language Models）在 2018 年首次提出了上下文相關的詞表示：

```python
# ELMo 的雙向 LSTM
forward_lstm: "我去____存錢" → "銀行" (從左到右)
backward_lstm: "存錢____我去" → "銀行" (從右到左)
# 最終表示 = 融合雙向的隱藏狀態
```

ELMo 的詞向量是**函數**而非**查找表**——相同的詞在不同上下文中有不同的向量。

## BERT：雙向編碼器表示

BERT（Bidirectional Encoder Representations from Transformers）由 Google 在 2018 年提出，是 NLP 領域的里程碑。它的核心創新是**深度雙向預訓練**：

```
# 傳統語言模型：從左到右
P(w_t | w_1, ..., w_{t-1})

# BERT：同時利用左右上下文
P(w_t | w_1, ..., w_{t-1}, w_{t+1}, ..., w_n)
```

### 預訓練任務

BERT 使用了兩個預訓練任務：

**Masked Language Model（MLM）**：隨機遮蓋 15% 的詞，讓模型預測被遮蓋的詞：

```
輸入：我 [MASK] 去銀行 [MASK] 錢
目標：我 "要" 去銀行 "存" 錢
```

**Next Sentence Prediction（NSP）**：判斷兩個句子是否連續：

```
[CLS] 今天天氣真好 [SEP] 我們去散步吧 [SEP] → IsNext
[CLS] 今天天氣真好 [SEP] 地球是圓的 [SEP] → NotNext
```

### BERT 架構

BERT 基於 Transformer 的編碼器，有兩個主要版本：

| 模型 | 層數 | 隱藏維度 | 注意力頭數 | 參數量 |
|------|------|----------|-----------|--------|
| BERT-base | 12 | 768 | 12 | 110M |
| BERT-large | 24 | 1024 | 16 | 340M |

## 微調（Fine-tuning）

BERT 的強大之處在於：預訓練後的模型可以透過簡單的微調適應各種下游任務：

```python
from transformers import BertForSequenceClassification

# 載入預訓練模型 + 分類頭
model = BertForSequenceClassification.from_pretrained(
    "bert-base-chinese", num_labels=2
)

# 微調
model.train()
for batch in dataloader:
    outputs = model(**batch)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
```

只需在 BERT 頂部加上一個簡單的分類層，就能在 GLUE 基準測試上超越所有先前模型。

## ELMo vs BERT

| 特性 | ELMo | BERT |
|------|------|------|
| 架構 | 雙向 LSTM | Transformer |
| 方向性 | 淺層拼接 | 深層雙向 |
| 預訓練方式 | 語言模型 | MLM + NSP |
| 微調 | 特徵提取 | 端到端微調 |

## 影響

BERT 的發布引發了 NLP 領域的「ImageNet 時刻」。在 BERT 之後，預訓練 + 微調成為了 NLP 的標準範式。BERT 的變體（RoBERTa、ALBERT、DistilBERT 等）持續推動著性能極限。

---

**下一步**：[GPT 系列與生成式預訓練](focus7.md)

## 延伸閱讀

- [BERT 原始論文](https://www.google.com/search?q=BERT+pre-training+of+deep+bidirectional+transformers)
- [ELMo 論文](https://www.google.com/search?q=ELMo+deep+contextualized+word+representations)
- [Hugging Face BERT 教學](https://www.google.com/search?q=Hugging+Face+BERT+fine+tuning+tutorial)
