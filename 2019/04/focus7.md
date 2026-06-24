# 預訓練語言模型

## 從 Word2Vec 到 BERT

從 2013 年 Word2Vec 誕生到 2018 年 BERT 橫空出世，這五年間 NLP 經歷了革命性的變化。

---

## Word2Vec 的局限性

Word2Vec 使用靜態詞嵌入，每個詞只有一個向量，無法處理：

```
「銀行」在以下句子的不同含義：
- 我去銀行存款（金融機構）
- 河岸的銀行（河岸）

Word2Vec 只能給出一個向量，無法區分這兩種意義
```

---

## 預訓練語言模型的興起

### 為什麼需要預訓練？

1. **大量無標籤資料**：網路上有大量文字，但標註資料昂貴
2. **遷移學習**：在大型通用語料上預訓練，再在特定任務上微調
3. **提升效能**：預訓練模型通常比從頭訓練效果更好

### 預訓練 + 微調流程

```
大規模無標籤語料     特定任務少量標籤資料
    │                      │
    ▼                      ▼
┌────────┐           ┌────────┐
│預訓練  │           │ 微調   │
│語言模型│──────────►│特定任務│
└────────┘           └────────┘
```

---

## ELMo：上下文表示

ELMo（Embeddings from Language Models）於 2018 年提出，使用雙向 LSTM 產生上下文相關的詞表示。

### ELMo 的核心思想

```python
# ELMo 使用雙向語言模型
# 每個詞的表示 = 輸入嵌入 + 前向 LSTM 隱藏 + 後向 LSTM 隱藏

class ELMo:
    def __init__(self):
        self.forward_lm = LSTMLanguageModel()
        self.backward_lm = LSTMLanguageModel()

    def get_embedding(self, word, context):
        # 前向表示（基於左側上下文）
        forward_repr = self.forward_lm.get_hidden_state(word, context)

        # 後向表示（基於右側上下文）
        backward_repr = self.backward_lm.get_hidden_state(word, context)

        # 拼接
        return torch.cat([forward_repr, backward_repr], dim=-1)
```

### ELMo 的特點

- **雙向**：同時考慮左右上下文
- **層次化**：不同層捕捉不同類型的資訊
- **任務相關**：可以學習任務相關的表示

---

## BERT 革命

BERT（Bidirectional Encoder Representations from Transformers）於 2018 年 10 月發表，是 NLP 領域的重大突破。

### BERT 的核心創新

1. **雙向 Transformer**：使用注意力機制同時考慮左右上下文
2. **Masked Language Model**：透過預測被遮罩的詞來學習
3. **下一句預測**：學習句子間的關係

### BERT 架構

```
輸入表示
    │
    ├── Token Embeddings（詞嵌入）
    ├── Segment Embeddings（段落嵌入）
    └── Position Embeddings（位置嵌入）
    │
    ▼
Transformer 編碼器（多層）
    │
    ▼
輸出表示
```

### BERT 的預訓練任務

**1. Masked Language Model (MLM)**

```python
# 輸入：[CLS] 我 去 [MASK] 銀行 [SEP]
# 目標：預測 [MASK] = 「存款」

# 15% 的詞被遮罩
# 80% 換成 [MASK]
# 10% 隨機替換
# 10% 保持不變
```

**2. Next Sentence Prediction (NSP)**

```python
# 輸入：[CLS] A [SEP] B [SEP]
# 目標：B 是 A 的下一句嗎？ → Yes/No
```

### BERT 的影響

| 之前 | BERT 之後 |
|-----|----------|
| 從頭訓練 | 預訓練 + 微調 |
| 單向 LSTM | 雙向 Transformer |
| 任務專用模型 | 通用語言理解 |

---

## Transformer 基礎

Transformer 是 BERT 的基礎，於 2017 年提出。

### 自注意力機制

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.query = nn.Linear(hidden_dim, hidden_dim)
        self.key = nn.Linear(hidden_dim, hidden_dim)
        self.value = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x):
        # x: (seq_len, batch, hidden_dim)

        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        # 注意力分數
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (hidden_dim ** 0.5)
        attention = F.softmax(scores, dim=-1)

        # 加權值
        output = torch.matmul(attention, V)

        return output, attention
```

### 多頭注意力

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, hidden_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads

        self.q_linear = nn.Linear(hidden_dim, hidden_dim)
        self.k_linear = nn.Linear(hidden_dim, hidden_dim)
        self.v_linear = nn.Linear(hidden_dim, hidden_dim)
        self.out_linear = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x):
        batch_size = x.size(0)

        # 線性變換並分頭
        Q = self.q_linear(x).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_linear(x).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_linear(x).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attention = F.softmax(scores, dim=-1)
        output = torch.matmul(attention, V)

        # 合併頭
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.head_dim)

        return self.out_linear(output)
```

---

## BERT 的應用

### 文字分類

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

text = "這部電影非常好看！"
inputs = tokenizer(text, return_tensors='pt')
outputs = model(**inputs)
```

### 命名實體識別

```python
from transformers import BertForTokenClassification

model = BertForTokenClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=7  # B-PER, I-PER, B-LOC, I-LOC, ...
)

inputs = tokenizer(text, return_tensors='pt')
outputs = model(**inputs)
```

### 問答系統

```python
from transformers import BertForQuestionAnswering

model = BertForQuestionAnswering.from_pretrained('bert-base-chinese')

question = "誰發明了 Word2Vec？"
context = "Word2Vec 由 Tomas Mikolov 於 2013 年在 Google 發明。"

inputs = tokenizer(question, context, return_tensors='pt')
outputs = model(**inputs)
```

---

## 未來展望

### 更大的模型

- GPT（2018）：1.17 億參數
- GPT-2（2019）：15 億參數
- BERT-Large（2018）：3.4 億參數

### 多語言模型

- mBERT：104 種語言
- XLM：跨語言預訓練

### 更高效的模型

- DistilBERT：蒸餾壓縮
- ALBERT：共享參數
- ELECTRA：替換標記檢測

---

## 延伸閱讀

- [BERT 原始論文](https://www.google.com/search?q=BERT+Devlin+2018+paper)
- [Transformer 論文](https://www.google.com/search?q=Attention+Is+All+You+Need+2017)
- [ELMo 論文](https://www.google.com/search?q=ELMo+Peters+2018)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*