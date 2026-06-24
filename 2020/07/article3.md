# Hugging Face Transformers 庫使用指南

## 前言

Hugging Face 的 Transformers 庫是 NLP 領域最受歡迎的開源工具之一。本文將介紹如何使用這個強大的庫來處理各種自然語言處理任務。

---

## 一、安裝與環境設定

### 1.1 安裝

```bash
pip install transformers
```

### 1.2 GPU 支援（可選）

```bash
pip install torch
```

---

## 二、基本概念

### 2.1 Pipeline

Pipeline 是最高層次的 API，可以快速完成常見任務：

```python
from transformers import pipeline

# 情感分析
classifier = pipeline("sentiment-analysis")
result = classifier("I love using Hugging Face!")
print(result)
```

### 2.2 預訓練模型

Transformers 提供了數千個預訓練模型：

```python
from transformers import AutoModel, AutoTokenizer

# 載入 BERT 模型
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
```

---

## 三、常用任務

### 3.1 文字分類

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="bert-base-uncased")
result = classifier("This movie is amazing!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

### 3.2 命名實體識別

```python
ner = pipeline("ner", grouped_entities=True)
result = ner("John works at Google in Mountain View.")
# 識別人名、組織、地點
```

### 3.3 問答系統

```python
qa_pipeline = pipeline("question-answering")
context = "Hugging Face is a company based in New York."
question = "Where is Hugging Face based?"
result = qa_pipeline(question=question, context=context)
# {'answer': 'New York', 'score': 0.99}
```

### 3.4 文字生成

```python
generator = pipeline("text-generation", model="gpt2")
result = generator("Once upon a time in a distant land", max_length=50)
print(result[0]['generated_text'])
```

### 3.5 翻譯

```python
translator = pipeline("translation_en_to_fr")
result = translator("Hello, how are you?")
print(result[0]['translation_text'])
```

---

## 四、Tokenizer 使用

### 4.1 基本用法

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# 單一文字
encoded = tokenizer("Hello, world!")
print(encoded)

# 多個文字（批次）
encoded_batch = tokenizer(["Hello", "World"], padding=True, truncation=True, return_tensors="pt")
print(encoded_batch)
```

### 4.2 常用參數

| 參數 | 說明 |
|------|------|
| padding | 填充短序列 |
| truncation | 截斷長序列 |
| max_length | 最大長度 |
| return_tensors | 返回張量格式 |

---

## 五、模型微調

### 5.1 Trainer API

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### 5.2 自訂訓練循環

```python
import torch
from torch.utils.data import DataLoader

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

for epoch in range(3):
    for batch in DataLoader(train_dataset, batch_size=8):
        outputs = model(**batch)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

---

## 六、常用模型架構

### 6.1 BERT 系列

```python
from transformers import BertModel, BertForSequenceClassification

# 基礎 BERT
bert = BertModel.from_pretrained("bert-base-uncased")

# BERT for 分類
bert_classifier = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
```

### 6.2 GPT-2

```python
from transformers import GPT2Model, GPT2LMHeadModel

# 基礎 GPT-2
gpt2 = GPT2Model.from_pretrained("gpt2")

# GPT-2 語言模型
gpt2_lm = GPT2LMHeadModel.from_pretrained("gpt2")
```

### 6.3 T5

```python
from transformers import T5Model, T5ForConditionalGeneration

t5 = T5ForConditionalGeneration.from_pretrained("t5-small")
```

---

## 七、實用技巧

### 7.1 使用 GPU

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
```

### 7.2 模型量化

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    load_in_8bit=True  # 8 位元量化
)
```

### 7.3 快取模型

```python
# 避免重複下載
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", cache_dir="./cache")
model = AutoModel.from_pretrained("bert-base-uncased", cache_dir="./cache")
```

---

## 結語

Hugging Face Transformers 庫大幅簡化了 NLP 模型的開發流程。從快速 prototyping 到生產環境部署，這個庫提供了完整的工具鏈。建議讀者多加練習，掌握這個必備工具。

---

*延伸閱讀：[Hugging Face Transformers 文檔](https://www.google.com/search?q=Hugging+Face+Transformers+documentation+2020)*