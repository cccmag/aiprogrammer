# Hugging Face Transformers 入門

Hugging Face 的 Transformers 庫是當今最流行的 NLP 工具之一。本文介紹如何快速入門。

## 1. 安裝

```bash
pip install transformers torch
```

## 2. 基本使用：pipline

最簡單的使用方式是使用預訓練的 pipeline：

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I love learning about AI!")
print(result)
```

## 3. 使用 BERT 進行文字分類

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
labels = torch.tensor([1]).unsqueeze(0)
outputs = model(**inputs, labels=labels)
```

## 4. 文字生成

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

input_text = "Once upon a time"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs['input_ids'], max_length=50)
generated_text = tokenizer.decode(outputs[0])
```

## 5. 結論

Hugging Face Transformers 讓使用預訓練模型變得非常簡單，是 NLP 開發者的必備工具。

---

## 延伸閱讀

- [Hugging Face 官方網站](https://www.google.com/search?q=Hugging+Face+Transformers+official)
- [Transformers 教學](https://www.google.com/search?q=Transformers+quick+tutorial)