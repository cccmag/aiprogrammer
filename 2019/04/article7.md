# BERT 實戰：文字分類與命名實體識別

## 前言

BERT（Bidirectional Encoder Representations from Transformers）已成為 NLP 的標杆模型。本篇文章展示 BERT 在實際任務中的應用。

## 環境設置

```bash
pip install torch transformers
```

## 文字分類

### 使用 Hugging Face Transformers

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

text = "這部手機性價比很高，值得購買"
inputs = tokenizer(text, return_tensors='pt', max_length=128, truncation=True)

with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1)
print(f"預測類別：{prediction.item()}")  # 1 = 正面, 0 = 負面
```

### 微調 BERT

```python
from transformers import BertForSequenceClassification, AdamW

model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=3)
optimizer = AdamW(model.parameters(), lr=2e-5)

for epoch in range(3):
    for batch in train_dataloader:
        optimizer.zero_grad()
        inputs = tokenizer(batch['text'], padding=True, truncation=True, return_tensors='pt')
        outputs = model(**inputs, labels=batch['label'])
        loss = outputs.loss
        loss.backward()
        optimizer.step()
```

## 命名實體識別（NER）

```python
from transformers import BertForTokenClassification

model = BertForTokenClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=7  # B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, O
)

def extract_entities(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    labels = [model.config.id2label[p.item()] for p in predictions[0]]

    entities = []
    current_entity = None
    for token, label in zip(tokens, labels):
        if label.startswith('B-'):
            if current_entity:
                entities.append(current_entity)
            current_entity = {'type': label[2:], 'token': token}
        elif label.startswith('I-') and current_entity:
            current_entity['token'] += token
        else:
            if current_entity:
                entities.append(current_entity)
                current_entity = None

    return entities
```

## 結論

BERT 的预训练+微调范式在各种 NLP 任务上都取得了 SOTA 结果。使用 Hugging Face Transformers 库可以快速应用 BERT 到实际项目中。

---

**延伸閱讀**

- [Hugging Face Transformers](https://www.google.com/search?q=Hugging+Face+Transformers+tutorial)
- [BERT 微調指南](https://www.google.com/search?q=BERT+fine-tuning+tutorial)