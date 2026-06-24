# 使用 Hugging Face Transformers

## Transformers 庫簡介

Hugging Face 的 transformers 庫是目前最流行的 NLP 模型庫，提供了 GPT-2、BERT、RoBERTa、T5 等數千個預訓練模型。

## 主要類別

### AutoModel 與 AutoTokenizer

```python
from transformers import AutoModel, AutoTokenizer

# 自動識別模型類型
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")
```

### GPT2LMHeadModel

專門用於文字生成的 GPT-2 模型類別。

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
```

### BertTokenizer 與 BertModel

```python
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
```

## Tokenizer 使用

```python
# 單文字編碼
inputs = tokenizer("Hello, world!")
print(inputs)

# 批次編碼
inputs = tokenizer(["Hello", "World"], padding=True, truncation=True, max_length=512)

# 解碼
decoded = tokenizer.decode([72, 101, 108, 108, 111])
```

## 模型推理

```python
import torch

# 單筆推理
inputs = tokenizer("Hello", return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# 取得隱藏狀態
hidden_states = outputs.last_hidden_state

# 使用 GPT-2 生成文字
inputs = tokenizer("The capital of France is", return_tensors="pt")
outputs = model.generate(**inputs, max_length=20)
print(tokenizer.decode(outputs[0]))
```

## Pipeline API

最簡單的使用方式：

```python
from transformers import pipeline

# 文字生成
generator = pipeline('text-generation', model='gpt2')
result = generator("Once upon a time", max_length=50)

# 情感分析
classifier = pipeline('sentiment-analysis')
result = classifier("I love this movie!")
```

## 資料處理

```python
from transformers import Dataset

# 從文字檔案建立資料集
dataset = Dataset.from_text("data.txt")

# Tokenize 資料集
def tokenize(examples):
    return tokenizer(examples["text"], padding=True, truncation=True)

tokenized_dataset = dataset.map(tokenize, batched=True)
```

## 參考資源

- https://www.google.com/search?q=Hugging+Face+transformers+library+tutorial+Python+API+2020
- https://www.google.com/search?q=AutoModel+AutoTokenizer+pretrained+model+loading+guide
- https://www.google.com/search?q=transformers+pipeline+API+text+generation+classification+usage