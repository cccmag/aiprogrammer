# BERT 微調分類任務

## 預訓練 + 微調範式

BERT 的強大之處在於：在大型語料上預訓練後，只需少量標註資料微調即可適應下游任務。

## 環境設置

```python
from transformers import (
    BertTokenizer, BertForSequenceClassification,
    Trainer, TrainingArguments
)
from datasets import load_dataset
import torch

# 載入繁體中文 BERT
model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)
```

## 資料準備

```python
# 自訂情感分析資料集
data = [
    ("這部電影太棒了，劇情緊湊，演員演技精湛", 1),
    ("浪費時間，劇情邏輯不通，不推薦", 0),
    ("還不錯，但結局有點失望", 1),
    ("畫面很美但故事空洞", 0),
]

def tokenize_function(examples):
    return tokenizer(
        examples["text"], padding="max_length",
        truncation=True, max_length=128
    )

# 轉換為 Dataset 格式
from datasets import Dataset
dataset = Dataset.from_dict({
    "text": [d[0] for d in data],
    "label": [d[1] for d in data]
})
tokenized = dataset.map(tokenize_function, batched=True)
```

## 模型載入與微調

```python
model = BertForSequenceClassification.from_pretrained(
    model_name, num_labels=2
)

training_args = TrainingArguments(
    output_dir="./bert-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir="./logs",
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    eval_dataset=tokenized,
)

trainer.train()
```

## 推論

```python
def predict_sentiment(text, model, tokenizer):
    inputs = tokenizer(
        text, return_tensors="pt",
        padding=True, truncation=True, max_length=128
    )
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    pred = torch.argmax(probs, dim=1).item()
    sentiment = "正面" if pred == 1 else "負面"
    confidence = probs[0][pred].item()
    return sentiment, confidence

# 測試
print(predict_sentiment("今天心情很好！", model, tokenizer))
# ("正面", 0.98)

print(predict_sentiment("這服務品質太差了", model, tokenizer))
# ("負面", 0.95)
```

## BERT 微調的關鍵參數

| 參數 | 建議值 | 說明 |
|------|--------|------|
| learning_rate | 2e-5 ~ 5e-5 | 比從頭訓練小很多 |
| batch_size | 8 ~ 32 | BERT 很吃記憶體 |
| epochs | 2 ~ 4 | 微調快速收斂 |
| max_length | 128 ~ 512 | 取決於文本長度 |
| warmup_steps | 10% of total | 穩定訓練 |

## 中文 BERT 模型選擇

- **bert-base-chinese**：Google 官方中文 BERT
- **roberta-base-chinese**：Facebook 優化版本
- **chinese-roberta-wwm-ext**：哈工大全詞遮罩版本
- **hfl/chinese-macbert-base**：MacBERT 改進版

## 更多任務

| 任務 | BERT 變體 | 輸出層 |
|------|-----------|--------|
| 情感分析 | BertForSequenceClassification | 分類頭 |
| 命名實體識別 | BertForTokenClassification | 序列標註 |
| 問答系統 | BertForQuestionAnswering | 跨度預測 |
| 句子相似度 | BertForSequenceClassification | 回歸頭 |

## 延伸閱讀

- [Hugging Face BERT 微調教學](https://www.google.com/search?q=Hugging+Face+BERT+fine+tuning+tutorial)
- [BERT 中文模型清單](https://www.google.com/search?q=chinese+BERT+pretrained+models+huggingface)
