# RoBERTa：強化版 BERT 的訓練策略

## 前言

2019 年 7 月，Facebook AI 發布了 RoBERTa（Robustly Optimized BERT Approach），這是對 BERT 的重新訓練版本，展示了訓練策略對模型性能的重要影響。

## RoBERTa 與 BERT 的主要區別

### 訓練策略對比

```
┌─────────────────────────────────────────────────────┐
│         BERT vs RoBERTa 訓練策略                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│   BERT              RoBERTa                        │
│   ─────────────────────────────────────────────    │
│    Books + Wiki     Books + Wiki + Web              │
│    16GB             160GB                          │
│                                                     │
│   MLM + NSP         MLM only                       │
│   固定遮罩          動態遮罩                        │
│                                                     │
│   256 tokens        512 tokens                      │
│   1M steps          300K steps                      │
│   批次 256          批次 8K                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 關鍵改進 1：移除 NSP 任務

```python
# BERT 使用 MLM + NSP
loss = mlm_loss + nsp_loss

# RoBERTa 只使用 MLM
loss = mlm_loss

# 實驗證明 NSP 任務反而傷害性能
```

### 關鍵改進 2：動態遮罩

```python
# BERT：每個訓練 epoch 遮罩相同
masked_tokens = static_masking(input_ids)

# RoBERTa：每次訓練時動態遮罩
masked_tokens = dynamic_masking(input_ids)
```

### 關鍵改進 3：更大的批次

```python
# BERT：批次 256
# RoBERTa：批次 8192
# 更大的批次 = 更穩定的梯度
```

---

## 實驗結果

### GLUE 基準測試

| 模型 | MNLI | QQP | QNLI | SST-2 | CoLA | STS-B | MRPC | RTE | 平均 |
|------|------|-----|------|-------|------|-------|------|-----|------|
| BERT-base | 86.6 | 91.3 | 92.3 | 94.9 | 60.6 | 87.1 | 92.0 | 70.4 | 84.4 |
| RoBERTa | 88.6 | 92.2 | 94.2 | 95.4 | 67.6 | 91.2 | 93.0 | 79.4 | 88.2 |

### 改進幅度

RoBERTa 在多數任務上比 BERT-base 有顯著提升：

```
MNLI: +2.0%
SST-2: +0.5%
CoLA: +7.0%  (最大提升)
RTE: +9.0%
```

---

## 訓練細節

### 數據增強

```python
# RoBERTa 使用的數據來源
roberta_data = {
    "books_corpus": "Books Corpus",
    "english_wikipedia": "Wikipedia",
    "cc_news": "CommonCrawl News",
    "open_webtext": "Open WebText",
    "stories": "Stories dataset",
}
```

### 超參數

```python
roberta_config = {
    "max_position_embeddings": 514,
    "hidden_size": 768,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "intermediate_size": 3072,
    "attention_probs_dropout_prob": 0.1,
    "hidden_dropout_prob": 0.1,
}
```

---

## 為什麼這些改進有效？

### 1. NSP 的負面影響

NSP 任務迫使模型學習句子關係，但：
- 簡單的正負樣本區分不能提升 MLM
- 損失的信號被稀釋

### 2. 動態遮罩的好處

- 每個 epoch 看到不同的遮罩模式
- 增加有效訓練樣本數量

### 3. 大批次的必要性

大批次訓練：
- 提供更穩定的梯度估計
- 允許更大的學習率
- 最終收斂到更好的局部最優

---

## 程式碼實作

### 使用 RoBERTa

```python
from transformers import RobertaTokenizer, RobertaModel

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaModel.from_pretrained('roberta-base')

inputs = tokenizer("RoBERTa is an optimized BERT!", return_tensors="pt")
outputs = model(**inputs)
```

---

## 結語

RoBERTa 的成功告訴我們：預訓練過程中的每個細節都很重要。

從數據選擇到訓練策略，從超參數到遮罩方式，這些都會影響最終模型的性能。RoBERTa 的貢獻不僅是提出了一個更好的模型，更重要的是展示了一種科學的模型改進方法。

---

**延伸閱讀**

- [RoBERTa Paper](https://www.google.com/search?q=RoBERTa+paper+Facebook+AI)
- [RoBERTa GitHub](https://www.google.com/search?q=RoBERTa+GitHub+Facebook)
- [BERT+training+strategies](https://www.google.com/search?q=BERT+training+strategies+improvement)