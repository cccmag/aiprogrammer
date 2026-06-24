# BERT 微調教程

## 前言

本文介紹如何在不同任務上微調 BERT 模型。

---

## 一、任務類型

| 任務 | BERT 輸出 | 範例 |
|------|----------|------|
| 句子分類 | [CLS] token | 情感分析 |
| 標記分類 | 每個 token | NER |
| 問答 | 起始/結束位置 | SQuAD |
| 句子對分類 | [CLS] token | 自然語言推論 |

---

## 二、準備資料

### 格式

```python
# 句子分類
{
    "input_ids": [...],
    "attention_mask": [...],
    "labels": 1  # 或 0
}

# 問答
{
    "input_ids": [...],
    "attention_mask": [...],
    "start_positions": 5,
    "end_positions": 10
}
```

---

## 三、句子分類微調

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

texts = ["This is great!", "This is terrible!"]
labels = [1, 0]

inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
inputs["labels"] = torch.tensor(labels)

outputs = model(**inputs)
loss = outputs.loss
logits = outputs.logits

predictions = torch.argmax(logits, dim=-1)
print(predictions)  # [1, 0]
```

---

## 四、NER 微調

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=9  # B-PER, I-PER, B-ORG, ...
)

text = "John works at Google in Mountain View."
inputs = tokenizer(text, return_tensors="pt")

outputs = model(**inputs)
logits = outputs.logits
predictions = torch.argmax(logits, dim=-1)

# 解碼
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
predicted_labels = [model.config.id2label[p.item()] for p in predictions[0]]

for token, label in zip(tokens, predicted_labels):
    if label != "O":
        print(f"{token}: {label}")
```

---

## 五、問答微調

```python
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch

model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

context = "Hugging Face is a company based in New York."
question = "Where is Hugging Face based?"

inputs = tokenizer(question, context, return_tensors="pt")
outputs = model(**inputs)

start_logits = outputs.start_logits
end_logits = outputs.end_logits

start_idx = torch.argmax(start_logits)
end_idx = torch.argmax(end_logits)

answer_tokens = inputs["input_ids"][0][start_idx:end_idx+1]
answer = tokenizer.decode(answer_tokens)
print(answer)  # "New York"
```

---

## 六、訓練配置

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_steps=500,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)
```

---

## 七、完整訓練流程

```python
from transformers import Trainer, AutoModelForSequenceClassification
from datasets import load_dataset

# 載入資料
dataset = load_dataset("glue", "sst2")

# 前處理
def tokenize_function(examples):
    return tokenizer(examples["sentence"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 模型
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
)

trainer.train()
```

---

## 八、常見問題

### 1. 微調時是否凍結 BERT 層？

初期可以凍結，後期再解凍：
```python
for param in model.bert.parameters():
    param.requires_grad = False
```

### 2. 學習率設定

- BERT 層：1e-5 到 2e-5
- 任務層：1e-4 到 5e-4

### 3. 過擬合怎麼辦？

- 增加 dropout
- 減少訓練 epochs
- 使用 early stopping

---

## 結語

BERT 的微調是 NLP 實務中最常見的任務。掌握各種任務的微調技巧，是每個 NLP 工程師的必備技能。

---

*延伸閱讀：[BERT+fine-tuning+tutorial+2020](https://www.google.com/search?q=BERT+fine-tuning+tutorial+2020)*