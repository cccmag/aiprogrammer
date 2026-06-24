# BERT 文字分類實作

## 任務設定

使用 BERT 進行文字分類（如情感分析）。

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

text = "I love this product! It's amazing."
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
labels = torch.tensor([1]).unsqueeze(0)

outputs = model(**inputs, labels=labels)
loss = outputs.loss
logits = outputs.logits
```

## 完整訓練流程

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.datasets import fetch_20newsgroups

# 載入範例資料
newsgroups_train = fetch_20newsgroups(subset='train')
newsgroups_test = fetch_20newsgroups(subset='test')

# Tokenize
train_encodings = tokenizer(list(newsgroups_train.data), truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(list(newsgroups_test.data), truncation=True, padding=True, max_length=512)
```

## 建立 Dataset 類別

```python
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
    def __len__(self):
        return len(self.labels)

train_dataset = NewsDataset(train_encodings, newsgroups_train.target)
test_dataset = NewsDataset(test_encodings, newsgroups_test.target)
```

## 訓練設定

```python
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    evaluation_strategy="epoch",
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()
```

## 評估與預測

```python
trainer.evaluate()

# 預測新文字
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    return prediction

result = predict("The stock market is crashing today!")
print(f"預測類別: {result}")
```

## 使用快取模型

為了加速推理，可以使用量化或模型蒸餾：

```python
# 匯出為 ONNX 格式
import torch.onnx

model.eval()
torch.onnx.export(
    model,
    (inputs["input_ids"],),
    "bert_classifier.onnx",
    input_names=["input_ids"],
    output_names=["logits"]
)
```

## 參考資源

- https://www.google.com/search?q=BERT+text+classification+tutorial+PyTorch+fine-tuning+2020
- https://www.google.com/search?q=transformers+BertForSequenceClassification+sentiment+analysis+example
- https://www.google.com/search?q=BERT+news+classification+20newsgroups+training+evaluation+guide