# BERT 帶來的 NLP 革新

## 前言

2018 年 10 月，Google 發布了 BERT，這是一款徹底改變自然語言處理領域的預訓練模型。2019 年 10 月，正值 BERT 週年之際，本篇文章將回顧 BERT 如何革新了 NLP 領域。

## BERT 之前的 NLP

### 傳統方法的局限

在 BERT 出現之前，NLP 任務通常採用以下方法：

1. **特徵工程**：人工設計特徵
2. **任務特定模型**：每個任務需要專門設計模型
3. **少量標註資料**：難以獲得大規模標註資料

```
典型 NLP pipeline：
文字 → 特徵提取 → 分類/標註 → 輸出
```

### Word2Vec 的時代

Word2Vec 等詞嵌入方法雖然在一定程度上提升了效能，但仍是靜態表示：

```python
# Word2Vec 的限制
word2vec["bank"] = 平均向量（無法區分「銀行」和「河岸」）
```

## BERT 的核心創新

### 雙向 Transformer 編碼器

BERT 使用雙向 Transformer 編碼器，能夠同時利用左右上下文：

```
傳統方法：left-to-right 或 shallow bidirectional
BERT：Deep bidirectional Transformer
```

### Masked Language Model

BERT 的訓練目標是預測被隨機遮蔽的 token：

```python
輸入："The [MASK] is a pet animal"
標籤："cat"
```

這種方法允許模型學習雙向上下文表示。

### 預訓練+微調範式

BERT 開創了預訓練+微調的新範式：

```
預訓練：在大型無標注文本上學習語言表示
    ↓
微調：在特定任務的小規模標註資料上調整
```

## BERT 帶來的突破

### 各任務的效能提升

| 任務 | 之前最佳 | BERT | 提升 |
|------|----------|------|------|
| 問答（SQuAD） | 91.2 | 93.2 | +2.0 |
| 情感分析（SST-2） | 94.9 | 95.3 | +0.4 |
|  Natural Language Inference | 76.8 | 86.7 | +9.9 |

### 減少任務特定工程

BERT 之前：
```
每個 NLP 任務需要：
- 設計特定的模型架構
- 人工設計特徵
- 大量任務特定的資料
```

BERT 之後：
```
同一個預訓練模型：
- 更換最後一層即可處理不同任務
- 大幅減少任務特定的資料需求
```

## BERT 的應用場景

### 文字分類

```python
from transformers import BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
outputs = model(input_ids, attention_mask, labels)
loss = outputs.loss
logits = outputs.logits
```

### 問答系統

```python
from transformers import BertForQuestionAnswering

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
outputs = model(input_ids, token_type_ids, attention_mask)
start_logits = outputs.start_logits
end_logits = outputs.end_logits
```

### 命名實體識別

```python
from transformers import BertForTokenClassification

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=9  # B-PER, I-PER, B-ORG, ...
)
```

## BERT 的影響

### 對研究的影響

BERT 的出現推動了 NLP 研究的多個方向：

1. **預訓練模型的改進**：RoBERTa、XLNet、ALBERT
2. **更有效的預訓練方法**：ELECTRA、CoVe
3. **跨語言模型**：mBERT、XLM

### 對產業的影響

BERT 也深刻影響了 NLP 產業應用：

```
Google 搜尋：2019 年起使用 BERT 改善搜尋結果
Amazon Alexa：使用類似技術提升理解能力
客服系統：更準確的意圖識別和實體提取
```

## BERT 的變體

### 壓縮版本

| 模型 | 參數量 | 壓縮比 |
|------|--------|--------|
| BERT BASE | 110M | 1x |
| ALBERT BASE | 12M | 9x |
| DistilBERT | 66M | 1.7x |
| TinyBERT | 14M | 8x |

### 特定領域版本

- **BioBERT**：生物醫學領域
- **SciBERT**：科學文獻
- **FinBERT**：金融領域
- **BERT-je**：日語優化

## 批評與討論

### 計算成本

BERT 的訓練和使用需要大量計算資源：

```
BERT LARGE 訓練：
- 需要 16 個 TPU（約 4 萬美元）
- 訓練時間：約 4 天
```

### 模型複雜性

BERT 模型的複雜性也帶來了挑戰：

- 推理延遲
- 部署成本
- 可解釋性

## 結論

BERT 的出現標誌著 NLP 領域的範式轉變。從任務特定的模型到預訓練+微調，從靜態詞嵌入到動態上下文表示，BERT 開創了一個新時代。雖然 BERT 本身已經有了很多改進版本，但其核心思想——使用大型預訓練模型學習通用語言表示——將繼續影響 NLP 的未來發展。

---

**延伸閱讀**

- [BERT+原始論文](https://www.google.com/search?q=BERT+pre+training+deep+bidirectional+transformers)
- [Google+BERT+Blog](https://www.google.com/search?q=Google+BERT+natural+language+processing)
- [BERT+應用場景](https://www.google.com/search?q=BERT+applications+NLP)