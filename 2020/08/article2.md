# Hugging Face Transformers 實戰

## 前言

Hugging Face Transformers 是目前最流行的 NLP 工具庫。本文介紹如何使用它來處理各種 NLP 任務。

---

## 一、安裝

```bash
pip install transformers torch
```

---

## 二、Pipeline API

### 基本用法

```python
from transformers import pipeline

# 情感分析
classifier = pipeline("sentiment-analysis")
result = classifier("I love using Hugging Face!")
print(result)
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

### 常用 Pipeline

| 任務 | Pipeline 名稱 |
|------|--------------|
| 情感分析 | sentiment-analysis |
| 命名實體識別 | ner |
| 問答 | question-answering |
| 文字生成 | text-generation |
| 翻譯 | translation_xx_to_yy |
| 摘要 | summarization |

---

## 三、預訓練模型使用

### 載入模型

```python
from transformers import AutoModel, AutoTokenizer

# BERT
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# GPT-2
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
```

### 基本前向傳播

```python
inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)

# 最後一層隱藏狀態
last_hidden_states = outputs.last_hidden_state

# [CLS] token 的表示
cls_embedding = outputs.last_hidden_state[0, 0]
```

---

## 四、微調模型

### Trainer API

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### 自訂訓練循環

```python
import torch

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

for epoch in range(3):
    for batch in train_dataloader:
        inputs, labels = batch
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

---

## 五、常用任務

### 文字分類

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

inputs = tokenizer("This is great!", return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
predictions = torch.argmax(logits, dim=-1)
```

### 問答

```python
from transformers import pipeline

qa = pipeline("question-answering")
result = qa(
    question="What is the capital of France?",
    context="France is a country in Europe. Its capital is Paris."
)
print(result)
# {'answer': 'Paris', 'score': 0.99}
```

### 文字生成

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")
result = generator(
    "Once upon a time",
    max_length=50,
    num_return_sequences=3
)
```

---

## 六、模型儲存與載入

### 儲存模型

```python
model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")
```

### 載入模型

```python
model = AutoModel.from_pretrained("./my_model")
tokenizer = AutoTokenizer.from_pretrained("./my_model")
```

---

## 七、多語言模型

```python
# 多語言 BERT
model = AutoModel.from_pretrained("bert-base-multilingual-cased")

# XLM-RoBERTa
model = AutoModel.from_pretrained("xlm-roberta-base")

# 處理多語言文字
inputs = tokenizer("Bonjour le monde", return_tensors="pt")
outputs = model(**inputs)
```

---

## 八、最佳化技巧

### 使用 GPU

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
```

### 模型量化

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    load_in_8bit=True
)
```

---

## 結語

Hugging Face Transformers 提供了從研究到生產的完整工具鏈。掌握這個庫是現代 NLP 開發者的必備技能。

---

*延伸閱讀：[Hugging+Face+Transformers+tutorial+2020](https://www.google.com/search?q=Hugging+Face+Transformers+tutorial+2020)*