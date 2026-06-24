# 預訓練模型庫：Hugging Face Transformers

## 前言

Hugging Face Transformers 是 NLP 領域最重要的開源庫之一。

## 基本使用

```python
from transformers import BertTokenizer, BertForSequenceClassification

# 載入預訓練模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese')

# 簡單分類
text = "這部電影非常好看"
inputs = tokenizer(text, return_tensors='pt')
outputs = model(**inputs)
```

## Pipeline API

```python
from transformers import pipeline

# 情感分析
classifier = pipeline('sentiment-analysis')
result = classifier("這是一部很好的電影")
```

## 更多模型

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# 文字生成
input_text = "今天天氣很好，我"
inputs = tokenizer(input_text, return_tensors='pt')
outputs = model.generate(**inputs, max_length=50)
generated = tokenizer.decode(outputs[0])
```

## 延伸閱讀

- [Hugging Face Transformers](https://www.google.com/search?q=Hugging+Face+Transformers+tutorial)