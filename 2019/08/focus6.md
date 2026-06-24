# BERT 與預訓練革命

## 雙向 Transformer 的勝利

2018 年 10 月，Google 發布了 BERT（Bidirectional Encoder Representations from Transformers），這是 NLP 領域的里程碑事件。BERT 展示了雙向 Transformer 的威力，開創了「預訓練 + 微調」的新範式。

---

## BERT 的核心創新

### 雙向 Transformer

與之前 GPT（單向從左到右）和 ELMo（獨立訓練的兩個方向的 LSTM）不同，BERT 同時利用雙向上下文：

```
┌─────────────────────────────────────────────────────┐
│         單向 vs 雙向表示學習                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   GPT (單向):                                       │
│   The | cat | sat | on | the | mat | [MASK]        │
│        →      →      →      →      →      →        │
│                                                     │
│   ELMo (獨立的雙向):                                 │
│   The → LSTM →                                      │
│        ← LSTM ←                                     │
│                                                     │
│   BERT (雙向):                                      │
│   The ↔ cat ↔ sat ↔ on ↔ the ↔ mat ↔ [MASK]        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 遮罩語言模型（MLM）

BERT 的預訓練使用一種新的任務：

```python
# 輸入: "The cat sat on the [MASK]"
# 目標: 預測被遮罩的詞 "mat"

# 這讓模型能夠同時看到左邊和右邊的上下文
```

### 下一句預測（NSP）

```python
# 正樣本：連續的句子
# Sentence A: "He went to the store"
# Sentence B: "He bought some milk"
# 標籤: IsNext

# 負樣本：非連續的句子
# Sentence A: "He went to the store"
# Sentence B: "The sky is blue"
# 標籤: NotNext
```

---

## BERT 架構

### 配置

```python
# BERT-Base 配置
bert_base_config = {
    "vocab_size": 30522,
    "hidden_size": 768,
    "num_hidden_layers": 12,      # Transformer 編碼器層數
    "num_attention_heads": 12,
    "intermediate_size": 3072,
    "hidden_dropout_prob": 0.1,
    "attention_probs_dropout_prob": 0.1,
    "max_position_embeddings": 512,
    "type_vocab_size": 2,        # 句子 A, 句子 B
}
# 參數總量: 110M

# BERT-Large 配置
bert_large_config = {
    "hidden_size": 1024,
    "num_hidden_layers": 24,
    "num_attention_heads": 16,
    "intermediate_size": 4096,
}
# 參數總量: 340M
```

---

## 預訓練任務

### 任務 1: 遮罩語言模型

```python
def mlm_pre训练(batch, model, tokenizer):
    # 隨機遮罩 15% 的 tokens
    masked_input, labels = mask_tokens(batch, tokenizer)

    # 前向傳播
    logits = model(masked_input)

    # 計算損失
    loss = cross_entropy(logits[labels], labels)

    return loss
```

### 任務 2: 下一句預測

```python
def nsp_pre训练(sentence_a, sentence_b, model):
    # 連接句子
    input_ids = [CLS] + sentence_a + [SEP] + sentence_b + [SEP]

    # BERT 的 [CLS] token 包含句子級別的資訊
    logits = model(input_ids)[0, 0, :]  # [CLS] 的輸出

    # 二分類預測
    is_next = classifier(logits)

    return cross_entropy(is_next, label)
```

---

## 下游任務微調

### 微調的方式

```python
# BERT 微調示例：文字分類

class BertClassifier(nn.Module):
    def __init__(self, bert_model, num_classes):
        super().__init__()
        self.bert = bert_model
        self.classifier = nn.Linear(768, num_classes)

    def forward(self, input_ids, attention_mask, labels):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled = outputs[0][:, 0]  # [CLS] token
        logits = self.classifier(pooled)

        loss = F.cross_entropy(logits, labels)
        return loss
```

### 四種典型任務

| 任務 | 輸入 | 輸出 | BERT 層使用 |
|------|------|------|-------------|
| 文字分類 | 句子 | 類別 | [CLS] |
| 序列標註 | 句子 | 每詞標籤 | 每詞輸出 |
| 問答 | 問題+段落 | 答案span | 開始/結束位置 |
| 句子對 | 句子A+句子B | 關係 | [CLS] |

---

## 實驗結果

### GLUE 基準

| 模型 | 平均分數 |
|------|----------|
| 之前 SOTA | 72.8 |
| BERT-base | 79.6 |
| BERT-large | 82.1 |

### 各任務提升

| 任務 | 之前最佳 | BERT-large | 提升 |
|------|----------|-------------|------|
| SQuAD 1.1 | 91.2 | 93.2 | +2.0 |
| SQuAD 2.0 | 89.4 | 90.9 | +1.5 |
| SWAG | 86.3 | 95.6 | +9.3 |

---

## BERT 的影響

### 開源模型

```python
# 使用預訓練 BERT
from transformers import BertModel, BertTokenizer

model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

inputs = tokenizer("The capital of France is Paris.", return_tensors='pt')
outputs = model(**inputs)
```

### 大量衍生模型

```
BERT 家族：
- RoBERTa: 優化訓練
- ALBERT: 引數共享
- DistilBERT: 模型蒸餾
- TinyBERT: 更小更快
- SpanBERT: 更好的span表示
- Sentence-BERT: 句子嵌入
- BioBERT: 醫學領域
- SciBERT: 科學領域
- multilingual-BERT: 多語言
```

---

## 中文 BERT

### BERT-Whitening

中文 NLP 社群的重要貢獻。

### 中文預訓練模型

```python
# 使用中文 BERT
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

inputs = tokenizer("今天天氣很好", return_tensors='pt')
outputs = model(**inputs)
```

---

## 總結

BERT 的貢獻：

1. **雙向 Transformer**：同時利用前後上下文
2. **預訓練 + 微調**：先通用預訓練，再任務微調
3. **簡單有效**：MLM + NSP 兩個簡單任務
4. **開源推進**：大幅推動 NLP 發展

BERT 不僅是技術創新，更開創了一種新的研究範式。

---

## 延伸閱讀

- [BERT Paper](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional)
- [Google+BERT+2018](https://www.google.com/search?q=Google+BERT+2018+paper)
- [BERT+fine-tuning](https://www.google.com/search?q=BERT+fine-tuning+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之六。*