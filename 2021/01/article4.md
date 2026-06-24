# Hugging Face Transformers

## 主流 NLP 框架

### 框架簡介

Hugging Face Transformers 是目前最流行的 NLP 函式庫，提供：

- 數千個預訓練模型
-統一的 API 介面
- PyTorch、TensorFlow、JAX 支援

```python
from transformers import AutoModel, AutoTokenizer

model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
```

## 預訓練模型的使用

### 文字分類

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("這篇文章寫得真好！")
# [{'label': 'POSITIVE', 'score': 0.99}]
```

### 文字生成

```python
generator = pipeline("text-generation", model="gpt2")
result = generator("今天天氣真好，", max_length=50)
```

### 機器翻譯

```python
translator = pipeline("translation_en_to_zh")
result = translator("Hello, world!")
# [{'translation_text': '你好，世界！'}]
```

## 模型共享與 Hub

Hugging Face Hub 是最大的 ML 模型平台：

- 50,000+ 預訓練模型
- 支援模型版本管理
- 簡易的上傳與下載

---

## 延伸閱讀

- [Hugging Face 官方網站](https://www.google.com/search?q=Hugging+Face+Transformers)
- [預訓練模型列表](https://www.google.com/search?q=pretrained+models+hugging+face+hub)
- [BERT+使用教學](https://www.google.com/search?q=BERT+tutorial+hugging+face)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*