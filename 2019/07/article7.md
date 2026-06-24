# BERT 的一年：預訓練模型的蓬勃發展

## 前言

2018 年 10 月，Google 發布了 BERT（Bidirectional Encoder Representations from Transformers）。到 2019 年 10 月，BERT 正好發布一周年。這一年裡，BERT 徹底改變了 NLP 領域的格局，預訓練 + 微調成為新的標準範式。

## BERT 核心思想

### 雙向 Transformer 編碼器

BERT 使用雙向 Transformer 編碼器，這是與之前 GPT（單向）的關鍵區別：

```
┌─────────────────────────────────────────────────────┐
│        BERT 雙向Attention vs GPT 單向                │
├─────────────────────────────────────────────────────┤
│                                                     │
│   GPT (單向):                                       │
│   ┌────┐   ┌────┐   ┌────┐   ┌────┐               │
│   │The │ → │cat │ → │sat │ → │on  │               │
│   └────┘   └────┘   └────┘   └────┘               │
│                                                     │
│   BERT (雙向):                                      │
│   ┌────┐ ↔ ┌────┘ ↔ ┌────┐ ↔ ┌────┐               │
│   │The │   │cat │   │sat │   │on  │               │
│   └────┘ ↔ └────┘ ↔ └────┘ ↔ └────┘               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 預訓練任務

BERT 透過兩個任務進行預訓練：

**1. Masked Language Model (MLM)**

```python
# 輸入: "The [MASK] sat on the mat"
# 目標: 預測被遮罩的詞 "cat"
```

**2. Next Sentence Prediction (NSP)**

```python
# 輸入: "He went to the store [SEP] He bought milk"
# 目標: 判斷是否是下一句
```

---

## BERT 的成功應用

### 各項任務的突破

| 任務 | 之前最佳 | BERT 最佳 | 提升 |
|------|----------|-----------|------|
| SQuAD 2.0 | 66.3% | 83.1% | +16.8 |
| MNLI | 72.2% | 86.7% | +14.5 |
| SST-2 | 94.9% | 95.5% | +0.6 |
| NER | 92.2% | 96.4% | +4.2 |

### 應用場景

```python
# 使用 BERT 進行文字分類
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("This is a great movie!", return_tensors="pt")
outputs = model(**inputs)
```

---

## BERT 家族的蓬勃發展

### DistilBERT

更小更快的版本：

```python
# DistilBERT：6 層，保留 97% 性能，減少 40% 參數
distilbert = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
```

### RoBERTa

Facebook 的強化版本：

- 移除 NSP 任務
- 更多訓練數據
- 更長訓練時間
- 動態遮罩

### ALBERT

引數共享版本：

```python
# ALBERT：跨層共享參數，大幅減少記憶體
albert = AlbertForSequenceClassification.from_pretrained('albert-base-v2')
```

### BERT-wikihow

針對 how-to 文字的特殊版本。

---

## 中文 BERT

### BERT-Whitening

中文 NLP 社群的重要貢獻。

### 預訓練中文 BERT

```python
# 中文 BERT 使用
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

inputs = tokenizer("今天天氣很好", return_tensors="pt")
outputs = model(**inputs)
```

---

## 結語

BERT 的成功告訴我們：

1. **雙向 attention 的威力**：能同時看到上下文
2. **預訓練的有效性**：在大規模數據上學習通用表示
3. **遷移學習的價值**：微調比從頭訓練更有效

這一年，預訓練模型從一個研究想法，變成了 NLP 領域的基礎設施。

---

**延伸閱讀**

- [BERT Paper](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional)
- [BERT+Google+2018](https://www.google.com/search?q=BERT+Google+2018)
- [NLP+pretrained+models](https://www.google.com/search?q=pretrained+models+NLP+2019)